"""Tải toàn bộ bản gốc Trung của 宝鉴 (tác giả 打眼) từ kcshu.com.

Site này không dùng Cloudflare, không cần đăng nhập, robots.txt cho phép.

Cấu trúc site:
  /book/122187/               -> trang mục lục, 13 trang /book/122187/index_{n}.html
  /book/122187/{id}.html      -> chương, phần 1
  /book/122187/{id}_2.html    -> phần 2   } mỗi chương bị cắt thành 2..4 phần,
  /book/122187/{id}_3.html    -> phần 3   } phần không tồn tại trả 404
  /book/122187/{id}_{n}.html  -> "上一章" = trước đó, "下一章" = id kế tiếp

Cách chạy:
  python baojian_scraper.py              # tải hết
  python baojian_scraper.py --limit 10   # thử 10 chương
  python baojian_scraper.py --epub       # tạo EPUB sau khi tải xong
"""

import argparse
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

BOOK_ID = "122187"
BASE = f"http://www.kcshu.com/book/{BOOK_ID}"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baojian")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": BASE + "/",
}

DELAY = 0.35  # giữa các request, lịch sự với server
RETRY = 4      # số lần thử lại khi gặp 502 (server này hay lỗi tạm thời)
RETRY_WAIT = 4.0

# Site chia ID chương thành dãy liên tục: chương 1 = 56234, chương 376 = 56625
# (56625 - 376 = 56249... hãy kiểm lại: 56625 - 376 = 56249, lệch 15 với 56234,
# nên dãy KHÔNG hoàn toàn liên tục). Ta dùng mốc đã xác minh trực tiếp:
# chương 1 = 56234. Mọi ID khác sẽ được đối chiếu tiêu đề sau khi tải.
FIRST_ID = 56233

# Tiêu đề chương dạng "第一章 兄妹" / "第一千二百三十六章 天堂岛 大结局"
CH_TITLE_RE = re.compile(r"^第[一二三四五六七八九十百千零〇两]+章\s*\S+")
# Chỉ số phần ở cuối trang: "第(1/3)页"
PAGE_MARK_RE = re.compile(r"第\s*\(\s*\d+\s*/\s*\d+\s*\)\s*页")

# Thẻ nhiễu: menu, quảng cáo, điều hướng
JUNK_TAGS = ["script", "style", "nav", "header", "footer", "ins", "iframe"]
JUNK_TEXT_PREFIX = (
    "上一章", "下一章", "目录", "存书签", "首页", "玄幻", "武侠", "都市",
    "历史", "网游", "科幻", "言情", "其他", "排行", "完本", "字体",
    "换手", "全屏阅读", "关灯", "搜索", "大", "中", "小",
    "本站所有收录的内容均来自互联网",
    "微信公众号", "本站书友",
    "非法请求",          # quảng cáo chèn cuối trang
    "新书推荐",
)


def get(sess, url):
    """GET có retry. Trả (response|None). 502 ở đây là lỗi tạm thời của server."""
    for attempt in range(RETRY):
        try:
            r = sess.get(url, timeout=25)
        except requests.RequestException:
            time.sleep(RETRY_WAIT)
            continue
        if r.status_code in (502, 503, 504):
            time.sleep(RETRY_WAIT)
            continue
        return r
    return None


def new_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def fetch_toc(sess):
    """Không dùng: mục lục site hay lỗi 502. Giữ lại để tham khảo tiêu đề nếu cần."""
    chapters = []
    page = 1
    while True:
        url = f"{BASE}/" if page == 1 else f"{BASE}/index_{page}.html"
        r = get(sess, url)
        if r is None or r.status_code != 200:
            print(f"  ! muc luc trang {page}: khong lay duoc, dung lai")
            break

        r.encoding = r.apparent_encoding or "utf-8"
        soup = BeautifulSoup(r.text, "lxml")

        found = 0
        for a in soup.find_all("a", href=True):
            m = re.fullmatch(rf"/book/{BOOK_ID}/(\d+)\.html", a["href"])
            if not m:
                continue
            title = a.get_text(strip=True)
            if CH_TITLE_RE.match(title):
                chapters.append((int(m.group(1)), title))
                found += 1

        print(f"  muc luc trang {page}: +{found} chuong (tong {len(chapters)})")
        if found == 0:
            break
        page += 1
        if page > 30:
            break
        time.sleep(DELAY)

    seen, ordered = set(), []
    for cid, title in chapters:
        if cid not in seen:
            seen.add(cid)
            ordered.append((cid, title))
    return ordered


def clean_lines(lines):
    """Lọc rác, chuẩn hoá khoảng trắng, gộp câu bị ngắt dòng."""
    out = []
    for raw in lines:
        s = raw.replace("\xa0", " ").strip()
        s = re.sub(r"[ \t]+", " ", s)
        if not s:
            continue
        # chỉ dấu phân trang
        if PAGE_MARK_RE.fullmatch(s):
            continue
        if any(s.startswith(p) for p in JUNK_TEXT_PREFIX):
            continue
        # dòng rác kiểu "第十章 xxx" lặp lại do template -> chỉ giữ dòng đầu
        out.append(s)

    merged = []
    for s in out:
        # câu Trung không kết thúc bằng dấu câu nghĩa cuối -> nối dòng sau vào
        if merged and not merged[-1][-1] in "。！？…”』】）" and not s[0] in "“‘（【《":
            merged[-1] += s
        else:
            merged.append(s)
    return merged


def fetch_chapter(sess, chapter_id, max_parts=6):
    """Ghép các phần của một chương. Trả (title, text) hoặc (None, None)."""
    lines = []
    title = None

    for part in range(1, max_parts + 1):
        url = (f"{BASE}/{chapter_id}.html" if part == 1
               else f"{BASE}/{chapter_id}_{part}.html")
        r = get(sess, url)
        if r is None:
            # 502/503/504 het lan thu -> BO QUA phan nay, thu tiep phan sau.
            # (truoc day dung `break` -> chap bi cat ngan, ra file rong)
            time.sleep(RETRY_WAIT)
            continue
        if r.status_code == 404:
            break  # het phan
        if r.status_code != 200:
            time.sleep(RETRY_WAIT)
            continue

        r.encoding = r.apparent_encoding or "utf-8"
        soup = BeautifulSoup(r.text, "lxml")

        for t in soup(JUNK_TAGS):
            t.decompose()

        # Tiêu đề chỉ lấy ở phần 1.
        # Trang không có <h1> tiêu đề chương; tiêu đề nằm trong <title> dạng
        # "宝鉴_打眼_第一章 兄妹_八一中文网" hoặc trong onclick addMark(n,id,'...')
        if part == 1:
            if not title:
                t = soup.title
                if t:
                    m = CH_TITLE_RE.search(t.get_text(strip=True))
                    if m:
                        title = m.group(0).strip()
            if not title:
                for a in soup.find_all("a", onclick=True):
                    m = re.search(r"'([^']*第[^']*章[^']*)'", a["onclick"])
                    if m:
                        title = m.group(1).strip()
                        break

        # Nội dung nằm trong <article class="font_max">, ngăn cách đoạn bằng <br>
        # (không phải <p>). Lấy <article> nếu có, nếu không thì tìm div chứa <p>.
        art = soup.find("article")
        if art is not None:
            # <br> và </p> đều là ranh giới đoạn -> thay bằng newline rồi tách
            for br in art.find_all("br"):
                br.replace_with("\n")
            for p in art.find_all("p"):
                p.insert_before("\n")
                p.insert_after("\n")
            raw = art.get_text("\n")
            lines.extend([ln for ln in raw.split("\n")])
        else:
            best, best_len = None, 0
            for div in soup.find_all(["div", "article"]):
                ps = div.find_all("p")
                if not ps:
                    continue
                n = sum(len(p.get_text(strip=True)) for p in ps)
                if n > best_len:
                    best, best_len = div, n
            if best is not None:
                for p in best.find_all("p"):
                    lines.append(p.get_text(" ", strip=True))
            else:
                text = soup.get_text("\n", strip=True)
                lines.extend(text.split("\n"))

        if part > 1:
            time.sleep(DELAY)

    body = clean_lines(lines)
    if not body:
        return title, ""
    return title, "\n\n".join(body)


def write_chapter(idx, total, cid, title, text, out_dir):
    safe = re.sub(r'[\\/:*?"<>|]', "_", title or f"第{idx}章")
    name = f"{idx:04d}_{safe}.txt"
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{title or name}\n\n")
        f.write(text)
        f.write("\n")
    return path, len(text)


def build_epub(out_dir):
    """Gộp các .txt thành EPUB đơn giản, không cần thư viện ngoài."""
    files = sorted(f for f in os.listdir(out_dir) if f.endswith(".txt"))
    if not files:
        print("Khong co file .txt de goi EPUB.")
        return None

    import zipfile
    from xml.sax.saxutils import escape

    uuid = "urn:uuid:baojian-dayan"
    title = "宝鉴"

    def esc(s):
        return escape(s)

    items, spine = [], []
    for i, fn in enumerate(files, 1):
        with open(os.path.join(out_dir, fn), encoding="utf-8") as f:
            txt = f.read()
        paras = "".join(
            f"<p>{esc(p.strip())}</p>" for p in txt.split("\n\n") if p.strip()
        )
        items.append(
            f'<item id="c{i}" href="c{i}.xhtml" '
            f'media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="c{i}"/>')

    manifest = "\n".join(items)
    spine_xml = "\n".join(spine)

    container = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<container version="1.0" '
        'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" '
        'media-type="application/oebps-package+xml"/></rootfiles></container>'
    )

    opf = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="uid">'
        f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:identifier id="uid">{uuid}</dc:identifier>'
        f'<dc:title>{esc(title)}</dc:title>'
        '<dc:language>zh</dc:language>'
        '<dc:creator>打眼</dc:creator>'
        f'</metadata><manifest>{manifest}</manifest>'
        f'<spine>{spine_xml}</spine></package>'
    )

    nav = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops">'
        '<head><title>nav</title></head><body><nav epub:type="toc">'
        '<ol>' + "".join(f'<li><a href="c{i}.xhtml">C{i}</a></li>'
                          for i in range(1, len(files) + 1)) +
        '</ol></nav></body></html>'
    )

    epub_path = os.path.join(os.path.dirname(out_dir), "宝鉴.epub")
    with zipfile.ZipFile(epub_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container)
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav)
        for i, fn in enumerate(files, 1):
            with open(os.path.join(out_dir, fn), encoding="utf-8") as f:
                txt = f.read()
            paras = "".join(
                f"<p>{esc(p.strip())}</p>" for p in txt.split("\n\n") if p.strip()
            )
            xhtml = (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<html xmlns="http://www.w3.org/1999/xhtml">'
                '<head><meta charset="utf-8"/>'
                f'<title>{esc(fn[:-4])}</title></head>'
                f'<body>{paras}</body></html>'
            )
            z.writestr(f"OEBPS/c{i}.xhtml", xhtml)
    return epub_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="chi tai N chuong")
    ap.add_argument("--start", type=int, default=1, help="bat dau tu chuong thu may")
    ap.add_argument("--total", type=int, default=0, help="tong so chuong (mac dinh 1282)")
    ap.add_argument("--epub", action="store_true", help="goi EPUB sau khi tai")
    ap.add_argument("--workers", type=int, default=6,
                    help="so chuong tai song song (mac dinh 6)")
    ap.add_argument("--out", default=OUT_DIR)
    args = ap.parse_args()

    total = args.total or 1282
    print(f"Quy luat ID: chuong n -> {FIRST_ID}+n")
    print(f"Se tai chuong {args.start}..{total}\n")

    os.makedirs(args.out, exist_ok=True)
    end = min(args.start + args.limit - 1, total) if args.limit else total
    todo = list(range(args.start, end + 1))
    span = len(todo)
    print(f"Tai {span} chuong, {args.workers} luong song song -> {args.out}\n")

    # Site phản hồi nhanh (~1s) nhưng hay 502. Tải song song nhiều chương,
    # mỗi luong một session riêng. Kết quả ghi theo thứ tự chương để log dễ đọc.
    lock = threading.Lock()
    done = [0]
    total_chars = [0]
    empty = []

    def worker(idx):
        sess = new_session()
        cid = FIRST_ID + idx
        t, text = fetch_chapter(sess, cid)
        t = t or f"第{idx}章"
        if not text:
            # thu lai voi session moi + cham them (server hay 502 khi tai song song)
            time.sleep(2.0)
            sess2 = new_session()
            t2, text = fetch_chapter(sess2, cid)
            t = t2 or t

        if not text:
            with lock:
                empty.append(idx)
                done[0] += 1
                print(f"[{done[0]}/{span}] {idx:4d} {t}  -> RONG")
            return

        _, n = write_chapter(idx, total, cid, t, text, args.out)
        with lock:
            total_chars[0] += n
            done[0] += 1
            d = done[0]
            msg = f"[{d}/{span}] {idx:4d} {t}  ({n} chu)"
            if d % 25 == 0:
                msg += f"  | tong {total_chars[0]:,} chu"
            print(msg)

    t_start = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(worker, i): i for i in todo}
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as e:  # không để 1 chương chết cả lô
                idx = futures[fut]
                with lock:
                    empty.append(idx)
                print(f"  ! chuong {idx} loi: {e}")

    elapsed = time.time() - t_start
    print(f"\nXong trong {elapsed/60:.1f} phut "
          f"({span/max(elapsed,1)*60:.0f} chuong/phut).")
    print(f"{span-len(empty)} chuong co noi dung, {len(empty)} rong.")
    if empty:
        print("Chuong rong:", sorted(empty)[:60])
    print(f"Tong ky tu: {total_chars[0]:,}")

    # ── VÁ LẠI chương rỗng: tải tuần tự 1 luồng ──
    # Server hay trả 502 khi tải song song; chạy 1 luồng thì ổn định.
    if empty:
        print(f"\n=== VÁ LẠI {len(empty)} CHƯƠNG RỖNG (1 luồng) ===")
        fixed = []
        for idx in sorted(empty):
            s = new_session()
            t, text = fetch_chapter(s, FIRST_ID + idx)
            if text:
                write_chapter(idx, total, FIRST_ID + idx, t or f"第{idx}章", text, args.out)
                fixed.append(idx)
                print(f"  ✓ chuong {idx} da va ({len(text)} chu)")
            else:
                print(f"  ✗ chuong {idx} van rong")
            time.sleep(1.0)
        if fixed:
            print(f"Da va {len(fixed)}/{len(empty)} chuong.")
            empty = [i for i in empty if i not in fixed]

    if args.epub:
        print("Doi tao EPUB...")
        p = build_epub(args.out)
        print(f"EPUB: {p} ({os.path.getsize(p)/1e6:.1f} MB)" if p else "EPUB that bai.")


if __name__ == "__main__":
    main()