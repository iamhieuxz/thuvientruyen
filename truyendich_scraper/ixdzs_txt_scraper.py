"""Tải bản gốc tiếng Trung từ ixdzs8.com và tách thành từng chương.

Nguồn: https://ixdzs8.com/read/{book_id}/
File TXT: https://down7.ixdzs8.com/{book_id}.zip  (bên trong là 1 file .txt, GB18030)

Đặc điểm dữ liệu cần xử lý:
  - TXT có header metadata + dòng quảng cáo, sau đó là "------章节内容开始-------".
  - Phần lớn tiêu đề chương nằm đầu dòng, nhưng một số bị dính vào cuối
    đoạn văn của chương trước ("...身子猛地一第1346章嫣然骂街").
  - Vì vậy không thể chỉ split theo dòng; phải tìm mọi "第N章" theo đúng
    thứ tự tăng dần rồi cắt tại đó.
  - Chương 175 của bộ 555557 bị thiếu hẳn tiêu đề trong TXT gốc; nội dung
    có thể nằm cuối chương 174. Script ghi nhận vào _meta.json.

Cách chạy:
  python ixdzs_txt_scraper.py                 # tải + tách truyện, không tạo EPUB
  python ixdzs_txt_scraper.py --only 555557   # chỉ 1 bộ
  python ixdzs_txt_scraper.py --epub          # tạo thêm EPUB
  python ixdzs_txt_scraper.py --force         # tải lại dù đã có TXT
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "data", "raw", "ixdzs8")

BOOKS = [
    {
        "id": "555557",
        "slug": "nhi-huu-thien-nhan-bat-khu-do-thach-huu-tai-loan-khan",
        "title": "你有天眼不去赌石，又在乱看",
        "author": "燃烧飞鹰",
        "notes": "Chương 175 thiếu tiêu đề trong TXT gốc; nội dung có thể nằm cuối chương 174.",
    },
    {
        "id": "610184",
        "slug": "canh-bao-chan-long-xuat-nguc",
        "title": "警报！真龙出狱！",
        "author": "红透半边天",
        "notes": "Nguồn ixdzs8 thiếu nội dung 11 chương (trang chương trả '内容还在处理中').",
    },
    {
        "id": "560049",
        "slug": "nien-dai-nga-tai-58-huu-khoi-dien",
        "title": "年代：我在58有块田",
        "author": "风中折腰",
        "notes": "Một số tiêu đề chương bị dính vào cuối đoạn trước trong TXT gốc; đã cắt theo số chương.",
    },
]

CH_START = "------章节内容开始-------"
CHAPTER_RE = re.compile(r"第(\d+)章")
JUNK_PREFIXES = (
    "『还在连载中",
    "更多电子书请访问",
    "爱下电子书Txt版",
    "爱下电子书TXT版",
)
CN_ONLY_TITLE_RE = re.compile(r"^第[零〇一二三四五六七八九十百千两]+章[ \t　]*$")

INVALID_FILENAME = re.compile(r'[\\/:*?"<>|]')


def log(msg: str) -> None:
    print(msg, flush=True)


def http_get(url: str, retries: int = 4, timeout: int = 90) -> bytes:
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_err = exc
            wait = 2 + attempt * 3
            log(f"  ! loi tai {url}: {exc}; thu lai sau {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Khong tai duoc {url}: {last_err}")


def raw_txt_path(book: dict) -> str:
    return os.path.join(RAW_DIR, f"{book['id']}_{safe_name(book['title'])}.txt")


def safe_name(name: str, limit: int = 80) -> str:
    name = INVALID_FILENAME.sub("_", name).strip(" .")
    return name[:limit] or "untitled"


def fetch_raw_text(book: dict, force: bool = False) -> str:
    """Tải zip, giải nén, chuyển GB18030 -> UTF-8, lưu vào data/raw."""
    os.makedirs(RAW_DIR, exist_ok=True)
    out = raw_txt_path(book)
    if os.path.exists(out) and not force:
        log(f"  = dung cache {out}")
        return out

    url = f"https://down7.ixdzs8.com/{book['id']}.zip"
    log(f"  + tai {url}")
    blob = http_get(url)
    tmp_zip = out + ".zip"
    with open(tmp_zip, "wb") as f:
        f.write(blob)

    with zipfile.ZipFile(tmp_zip) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".txt")]
        if not names:
            raise RuntimeError(f"Zip {url} khong co file .txt")
        raw = z.read(names[0])

    for enc in ("utf-8-sig", "gb18030", "utf-16"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError(f"Khong decode duoc {names[0]}")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.remove(tmp_zip)
    log(f"  -> {out} ({len(text):,} ky tu)")
    return out


def parse_chapters(text: str) -> tuple[list[dict], list[int]]:
    """Trả về (chapters, missing_numbers)."""
    start = text.find(CH_START)
    body = text[start + len(CH_START):] if start >= 0 else text

    markers = list(CHAPTER_RE.finditer(body))
    accepted: list[tuple[int, re.Match]] = []
    last = 0
    for m in markers:
        n = int(m.group(1))
        # Chỉ nhận số kế tiếp (hoặc nhảy cóc <= 5 để không bỏ cả bộ khi
        # nguồn thiếu 1-2 tiêu đề). Số lùi/trùng trong body bị loại.
        if n == last + 1 or (last < n <= last + 5):
            accepted.append((n, m))
            last = n

    chapters: list[dict] = []
    for idx, (n, m) in enumerate(accepted):
        nl = body.find("\n", m.start())
        if nl < 0:
            nl = len(body)
        head = body[m.start():nl].strip()
        title = head[len(f"第{n}章"):].strip(" \t　～")
        title = html.unescape(title).strip() or f"第{n}章"

        bstart = nl + 1
        bend = accepted[idx + 1][1].start() if idx + 1 < len(accepted) else len(body)
        raw = body[bstart:bend]

        lines = []
        for line in raw.split("\n"):
            s = line.replace("\xa0", " ").strip(" \t\u3000")
            if not s:
                continue
            s = html.unescape(s)
            if s.startswith(JUNK_PREFIXES):
                continue
            if CN_ONLY_TITLE_RE.fullmatch(s):
                continue
            lines.append(s)

        # Một số chương bị lặp tiêu đề ngay đầu body, dính liền với câu
        # đầu tiên (vd "第316章纺织厂工会&妇联第二天，...").
        if lines:
            prefix = f"第{n}章"
            first = lines[0]
            if first.startswith(prefix):
                rest = first[len(prefix):].strip(" \t\u3000")
                if rest.startswith(title):
                    rest = rest[len(title):].strip(" \t\u3000")
                if rest:
                    lines[0] = rest
                else:
                    lines.pop(0)

        chapters.append(
            {
                "number": n,
                "title": title,
                "text": "\n\n".join(lines),
            }
        )

    got = {c["number"] for c in chapters}
    missing = [n for n in range(1, last + 1) if n not in got]
    return chapters, missing


def write_chapters(book: dict, chapters: list[dict]) -> tuple[str, int, int, list[int]]:
    out_dir = os.path.join(ROOT, book["slug"])
    os.makedirs(out_dir, exist_ok=True)

    # Xóa file chương cũ (chỉ file dạng 0001_*.txt) để không còn file rỗng
    # hoặc tiêu đề cũ sau khi parser thay đổi.
    for old in os.listdir(out_dir):
        if re.fullmatch(r"\d{4}_.*\.txt", old):
            os.remove(os.path.join(out_dir, old))
    stale = os.path.join(out_dir, "_thieu-noi-dung.txt")
    if os.path.exists(stale):
        os.remove(stale)

    total_chars = 0
    toc = []
    written = 0
    empty: list[int] = []

    for i, ch in enumerate(chapters, 1):
        n = ch["number"]
        title = ch["title"]
        text = ch["text"].strip()

        if not text:
            empty.append(n)
            toc.append(f"{n:04d}\t第{n}章 {title}\t[nguồn thiếu nội dung]")
            continue

        fname = f"{n:04d}_{safe_name(title)}.txt"
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"第{n}章 {title}\n\n")
            f.write(text)
            f.write("\n")
        total_chars += len(text)
        written += 1
        toc.append(f"{n:04d}\t第{n}章 {title}")

        if i % 250 == 0:
            log(f"    ... {i}/{len(chapters)} chuong")

    with open(os.path.join(out_dir, "_toc.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(toc) + "\n")

    if empty:
        with open(
            os.path.join(out_dir, "_thieu-noi-dung.txt"),
            "w",
            encoding="utf-8",
            newline="\n",
        ) as f:
            f.write(
                "Các chương sau không có nội dung trên nguồn ixdzs8 "
                "(trang chương trả \"内容还在处理中\"):\n\n"
            )
            for n in empty:
                title = next(c["title"] for c in chapters if c["number"] == n)
                f.write(f"{n:04d}\t第{n}章 {title}\n")

    return out_dir, total_chars, written, empty


def build_epub(book: dict, chapters: list[dict], out_path: str) -> str:
    """EPUB 3 đơn giản, không cần thư viện ngoài."""
    from xml.sax.saxutils import escape

    css = (
        "body{font-family:serif;line-height:1.8;margin:1em}"
        "h1{font-size:1.2em;text-align:center;margin:1.2em 0}"
        "p{text-indent:2em;margin:0.35em 0}"
    )
    items, spine, nav_items, files = [], [], [], []

    for i, ch in enumerate(chapters, 1):
        xhtml_name = f"c{i}.xhtml"
        paras = "".join(
            f"<p>{escape(p.strip())}</p>"
            for p in ch["text"].split("\n\n")
            if p.strip()
        )
        xhtml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh">'
            "<head><meta charset=\"utf-8\"/>"
            f"<title>第{ch['number']}章 {escape(ch['title'])}</title>"
            f"<link rel=\"stylesheet\" href=\"style.css\"/></head>"
            f"<body><h1>第{ch['number']}章 {escape(ch['title'])}</h1>{paras}</body></html>"
        )
        files.append((xhtml_name, xhtml))
        items.append(
            f'<item id="c{i}" href="{xhtml_name}" media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="c{i}"/>')
        nav_items.append(
            f'<li><a href="{xhtml_name}">第{ch["number"]}章 {escape(ch["title"])}</a></li>'
        )

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
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:identifier id="uid">urn:uuid:ixdzs8-{book["id"]}</dc:identifier>'
        f'<dc:title>{escape(book["title"])}</dc:title>'
        f'<dc:creator>{escape(book["author"])}</dc:creator>'
        "<dc:language>zh</dc:language>"
        "</metadata>"
        f"<manifest>{''.join(items)}"
        '<item id="css" href="style.css" media-type="text/css"/>'
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" '
        'properties="nav"/></manifest>'
        f"<spine>{''.join(spine)}</spine></package>"
    )
    nav = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops"><head>'
        '<meta charset="utf-8"/><title>Mục lục</title></head><body>'
        '<nav epub:type="toc"><h1>Mục lục</h1><ol>'
        + "".join(nav_items)
        + "</ol></nav></body></html>"
    )

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container)
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav)
        z.writestr("OEBPS/style.css", css)
        for name, data in files:
            z.writestr(f"OEBPS/{name}", data)
    return out_path


def process(book: dict, force: bool = False, make_epub: bool = False) -> dict:
    log(f"\n=== {book['title']} ({book['id']}) ===")
    raw_path = fetch_raw_text(book, force=force)
    with open(raw_path, encoding="utf-8") as f:
        text = f.read()

    chapters, missing = parse_chapters(text)
    if not chapters:
        raise RuntimeError("Khong tim thay chuong nao")

    out_dir, total_chars, written, empty = write_chapters(book, chapters)
    log(
        f"  -> {written:,}/{len(chapters):,} chuong co noi dung, "
        f"{total_chars:,} ky tu -> {out_dir}"
    )
    if missing:
        log(f"  ! thieu tieu de chuong: {missing[:20]}")
    if empty:
        log(f"  ! nguon thieu noi dung {len(empty)} chuong: {empty[:20]}")

    epub_path = None
    if make_epub:
        epub_path = os.path.join(ROOT, f"{book['slug']}.epub")
        build_epub(book, chapters, epub_path)
        log(f"  -> EPUB {epub_path} ({os.path.getsize(epub_path)/1e6:.1f} MB)")

    meta = {
        "title_cn": book["title"],
        "author_cn": book["author"],
        "slug": book["slug"],
        "source": f"https://ixdzs8.com/read/{book['id']}/",
        "source_txt": f"https://down7.ixdzs8.com/{book['id']}.zip",
        "book_id": book["id"],
        "chapters_in_source": len(chapters),
        "chapters_written": written,
        "first_chapter": chapters[0]["number"],
        "last_chapter": chapters[-1]["number"],
        "missing_chapter_headings": missing,
        "empty_chapters": empty,
        "total_chars": total_chars,
        "scraped_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "raw_txt": os.path.relpath(raw_path, ROOT),
        "notes": book.get("notes", ""),
        "epub": os.path.relpath(epub_path, ROOT) if epub_path else None,
    }
    with open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="chi xu ly book id nay")
    ap.add_argument("--force", action="store_true", help="tai lai TXT")
    ap.add_argument("--epub", action="store_true", help="tao them EPUB")
    args = ap.parse_args()

    selected = [b for b in BOOKS if not args.only or b["id"] == args.only]
    if not selected:
        raise SystemExit(f"Khong co book id {args.only}")

    results = []
    for b in selected:
        results.append(process(b, force=args.force, make_epub=args.epub))

    log("\n=== TONG KET ===")
    for m in results:
        miss = f", thieu {len(m['missing_chapter_headings'])} tieu de" if m["missing_chapter_headings"] else ""
        empty = f", {len(m['empty_chapters'])} chuong trong" if m["empty_chapters"] else ""
        log(
            f"{m['title_cn']}: {m['chapters_written']:,}/{m['chapters_in_source']:,} chuong "
            f"(1..{m['last_chapter']}{miss}{empty}), {m['total_chars']:,} ky tu"
        )


if __name__ == "__main__":
    main()
