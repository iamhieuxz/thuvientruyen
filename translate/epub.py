# -*- coding: utf-8 -*-
"""
TXT / Markdown -> EPUB 3 (cho doc tren dien thoai).

Day la BUOC CUOI trong chuoi:
    txt goc (truyendich_scraper/baojian)
      -> dich.py dich sang tieng Viet  (data/baojian_vi/*.md)
      -> epub.py dong goi               (output/*.epub)

Chi dung thu vien chuan Python, khong can cai them.
Mac dinh doc thu muc ban dich Viet; can doc nguyen van thi them --src.

Dung:
  python epub.py                                  # ban dich Viet -> output/
  python epub.py --first 1 --last 20              # thu 20 chuong
  python epub.py --split 50                       # tach moi 50 chuong / file
  python epub.py --check                          # kiem tra, khong ghi file
  python epub.py --cover "bia.jpg" --title "Bao Giam" --author "Tac gia"

Tuy chon:
  --src THU_MUC   noi dung dau vao (mac dinh data/baojian_vi)
  --out FILE      file epub dau ra (mac dinh output/<ten thu muc>.epub)
  --first N / --last M   gioi han chuong
  --split N       tach moi N chuong ra file rieng
  --cover FILE    anh bia
  --title / --author
  --translate-titles   thay cum Han trong tieu de bang tu dien glossary
  --han --zh      chi dung khi muon ep ban goc tieng Trung
  --check
"""
import argparse
import html
import re
import sys
import unicodedata
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────── Hằng số EPUB ───────────────────────────

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

# Dùng đường dẫn tương đối ascii de moi may doc deu hieu
NCX = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="vi">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{uid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{title}</text></docTitle>
  <navMap>{nav}</navMap>
</ncx>
"""

OPF = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"
         xml:lang="vi">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:{uid}</dc:identifier>
    <dc:title>{title}</dc:title>
    <dc:creator>{author}</dc:creator>
    <dc:language>vi</dc:language>
    <dc:date>{date}</dc:date>
    <meta property="dcterms:modified">{date}</meta>
    <meta name="generator">txt2epub</meta>
  </metadata>
  <manifest>
{manifest}
  </manifest>
  <spine toc="ncx" page-progression-direction="ltr">
{spine}
  </spine>
</package>
"""

XHTML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
{body}
</body>
</html>
"""

CSS = """@charset "utf-8";
body { line-height: 1.65; text-align: justify; }
p { margin: 0 0 0.9em 0; text-indent: 2em; text-align: justify; }
p.first, p.noindent { text-indent: 0; }
h1 { font-size: 1.25em; text-align: center; margin: 0 0 1em 0;
     page-break-after: avoid; }
"""


# ─────────────────────────── Tiện ích ───────────────────────────

def num_key(name):
    m = re.match(r"^(\d+)", name)
    return (int(m.group(1)) if m else 10**9, name)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def clean(t):
    """Làm sạch văn bản đầu vào."""
    t = t.replace("\ufffd", "").replace("\u66f0", "\u65e5")  # ký tự hỏng, 曰->日
    t = re.sub(r"^\s*\d+\|[ \t]*$", "", t, flags=re.M)     # marker dòng scraper
    t = re.sub(r"^[ \t]*Variation[-—]*[ \t]*$", "", t, flags=re.M)
    t = re.sub(r"\r\n?", "\n", t)
    t = t.replace("\xa0", " ").replace("\u3000", " ")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{4,}", "\n\n\n", t)
    return t.strip()


# ─────────────────────────── Tên chương ───────────────────────────

HAN_DIGIT = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
             "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
HAN_UNIT = {"十": 10, "百": 100, "千": 1000}


def han_to_int(s):
    """'一千零四十九' -> 1049.  Hỗ trợ tới hàng nghìn (đủ cho tiểu thuyết)."""
    s = s.strip()
    if s.isdigit():
        return int(s)
    if not s:
        return None

    total, section, number = 0, 0, 0
    ok = False
    for ch in s:
        if ch in HAN_DIGIT:
            number = HAN_DIGIT[ch]
            ok = True
        elif ch in HAN_UNIT:
            unit = HAN_UNIT[ch]
            section += (number if number else 1) * unit
            number = 0
            ok = True
        else:
            return None
    total = section + number
    return total if ok else None


CN_NUM = {n: f"{i+1}" for i, n in enumerate(
    ["mot", "hai", "ba", "bon", "nam", "sau", "bay", "tam", "chin", "muoi"])}


def title_to_vi(t):
    """'第一章 兄妹' -> 'Chương 1: Anh Em' (dùng cho tiêu đề khi --han)."""
    m = re.match(r"^第\s*([零〇一二三四五六七八九十百千两\d]+)\s*[章回節节]\s*(.*)$", t)
    if not m:
        return t
    num, name = m.group(1), m.group(2).strip()
    n = han_to_int(num)
    head = f"Chương {n}" if n else f"Chương {num}"
    return f"{head}: {name}" if name else head


# ─────────────────────────── Markdown ───────────────────────────

def md_to_html(md, first_p=False):
    """Chuyển 1 khối Markdown rút gọn sang HTML. Trả về (html, is_first)."""
    md = md.strip()
    if not md:
        return "", False

    # tiêu đề
    if md.startswith("#"):
        m = re.match(r"^(#{1,6})\s*(.+)$", md)
        if m:
            return f"<h1>{esc(m.group(2).strip())}</h1>", first_p

    lines = md.split("\n")
    out, buf = [], []

    def flush(idx):
        nonlocal buf
        if not buf:
            return
        txt = " ".join(x.strip() for x in buf if x.strip())
        txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt)
        txt = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", txt)
        cls = " class=\"first\"" if idx == 0 else ""
        out.append(f"<p{cls}>{txt}</p>")
        buf = []

    idx = 0
    for ln in lines:
        s = ln.strip()
        if not s:
            flush(idx)
            idx += 1
            continue
        if s.startswith("#"):
            flush(idx)
            idx += 1
            out.append(f"<h1>{esc(s.lstrip('#').strip())}</h1>")
            continue
        if re.fullmatch(r"[-*_]{3,}", s):
            flush(idx)
            idx += 1
            out.append("<hr/>")
            continue
        if s.startswith(">"):
            s = re.sub(r"^>\s?", "", s)
        buf.append(s)
    flush(idx)

    # gộp class first vào đoạn đầu
    html_out = "\n".join(out)
    if first_p:
        html_out = html_out.replace("<p>", "<p class=\"first\">", 1)
    return html_out, first_p


def md_body_to_html(text):
    """Tách theo khối rỗng, dịch từng khối thành HTML."""
    parts, cur, seen = [], [], 0

    def flush():
        nonlocal cur, seen
        if cur:
            h, _ = md_to_html("\n\n".join(cur), first_p=(seen == 0))
            if h:
                parts.append(h)
                seen += 1
            cur = []

    for line in text.split("\n"):
        if line.strip():
            cur.append(line)
        else:
            flush()
    flush()
    return "\n".join(parts)


def txt_body_to_html(text):
    """Văn bản thuần: mỗi đoạn ngắn là một <p>. Dòng bắt đầu bằng dấu nháy là thoại."""
    out = []
    for i, para in enumerate(re.split(r"\n\s*\n", text)):
        para = para.strip()
        if not para:
            continue
        para = re.sub(r"\s*\n\s*", " ", para)
        cls = "first" if i == 0 else "noindent" if para.startswith(("\"", "“")) else ""
        attr = f' class="{cls}"' if cls else ""
        out.append(f"<p{attr}>{esc(para)}</p>")
    return "\n".join(out)


# ─────────────────────────── Ghép EPUB ───────────────────────────

def make_epub(chapters, meta, out_path, cover=None, zh=False):
    """
    chapters: list[(number, title, html_body)]
    """
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"taitruyen-{meta['title']}-{len(chapters)}"))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    files = {}
    manifest = []
    spine = []
    nav = []

    # style
    files["OEBPS/style.css"] = CSS
    manifest.append('<item id="css" href="style.css" media-type="text/css"/>')

    # toc
    files["OEBPS/toc.ncx"] = NCX.format(
        uid=uid, title=esc(meta["title"]),
        nav="".join(
            f'<navPoint id="np{i}" playOrder="{i}">'
            f'<navLabel><text>{esc(t)}</text></navLabel>'
            f'<content src="ch{i:04d}.xhtml"/></navPoint>'
            for i, (_, t, _) in enumerate(chapters, 1)))
    manifest.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

    if cover:
        ext = Path(cover).suffix.lower().lstrip(".")
        mt = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
              "png": "image/png", "gif": "image/gif"}.get(ext, "image/jpeg")
        data = Path(cover).read_bytes()
        files[f"OEBPS/cover.{ext}"] = data
        manifest.append(
            f'<item id="cover-img" href="cover.{ext}" media-type="{mt}" '
            f'properties="cover-image"/>')

    # từng chương
    for i, (num, title, body) in enumerate(chapters, 1):
        fn = f"ch{i:04d}.xhtml"
        lang = "zh" if zh else "vi"
        files[f"OEBPS/{fn}"] = XHTML.format(
            lang=lang, title=esc(title), body=body)
        manifest.append(
            f'<item id="ch{i}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="ch{i}"/>')
        nav.append((i, title))

    files["OEBPS/content.opf"] = OPF.format(
        uid=uid, title=esc(meta["title"]), author=esc(meta["author"]),
        date=now, manifest="\n".join(manifest), spine="\n".join(spine))

    files["mimetype"] = "application/epub+zip"
    files["META-INF/container.xml"] = CONTAINER

    out_path.parent.mkdir(parents=True, exist_ok=True)
    # mimetype phai la file dau tien, khong nén
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        for name, data in files.items():
            if name == "mimetype":
                continue
            z.writestr(name, data.encode("utf-8") if isinstance(data, str) else data)
    return out_path


# ─────────────────────────── Thu thập chương ───────────────────────────

def collect(src, ext, title_from_file=True):
    files = sorted((p for p in src.glob(f"*{ext}")), key=lambda p: num_key(p.name))
    out = []
    for p in files:
        out.append((num_key(p.name)[0], p))
    return out


# ─────────────────── Từ điển Hán → Việt (lấy từ glossary) ───────────────────

def load_dict(glossary_path):
    """Đọc các dòng '| 秦风 | Tần Phong |' trong glossary.md thành dict."""
    d = {}
    if not glossary_path or not glossary_path.exists():
        return d
    for line in glossary_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        han, vi = cells[0], cells[1]
        han = re.sub(r"[*`\s]+", "", han)
        vi = re.sub(r"[*`\s]+", " ", vi).strip()
        if not han or not vi:
            continue
        if not re.fullmatch(r"[\u4e00-\u9fff ]{1,12}", han):
            continue
        d[han] = vi
    # sap xep giam dan do dai de khop chuoi dai truoc
    return dict(sorted(d.items(), key=lambda kv: -len(kv[0])))


def apply_dict(title, d):
    """Thay cac cum Han trong tieu de bang tu viet. OFF mac dinh."""
    if not d:
        return title
    out = title
    for han, vi in d.items():
        if han in out:
            out = out.replace(han, vi)
    return out


def build_chapters(items, args):
    chaps = []
    for num, p in items:
        raw = p.read_text(encoding="utf-8", errors="replace")
        text = clean(raw)

        # .md: bỏ comment HTML đầu file
        text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.S)

        # tiêu đề
        title = ""
        mh = re.search(r"^#{1,3}\s*(.+)$", text, re.M)
        if mh:
            title = mh.group(1).strip()
            text = text[:mh.start()] + text[mh.end():]
        else:
            stem = p.stem
            title = re.sub(r"^\d+[\s_]+", "", stem)
            if args.han:
                title = title_to_vi(title)

        if args.han and not mh:
            title = title_to_vi(title)
        if not title:
            title = f"Chương {num}" if not args.han else f"第{num}章"
        if args.translate_titles:
            title = apply_dict(title, getattr(args, "_dict", {}) or {})

        # thân
        if p.suffix.lower() == ".md":
            body = md_body_to_html(text)
        else:
            body = txt_body_to_html(text)

        if not body.strip():
            continue
        chaps.append((num, title, body))
    return chaps


# ─────────────────────────── Chính ───────────────────────────

def main():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("--src", type=Path,
                    default=Path(r"f:\taitruyen\data\baojian_vi"),
                    help="thu muc chua .md hoac .txt")
    ap.add_argument("--out", type=Path, default=None, help="file epub dau ra")
    ap.add_argument("--title", default="Bao Giam")
    ap.add_argument("--author", default="Khac rong")
    ap.add_argument("--ext", default=None, choices=[".md", ".txt"])
    ap.add_argument("--han", action="store_true",
                    help="ten chuong dang Chu -> Vie")
    ap.add_argument("--zh", action="store_true",
                    help="sac ky tu Trung Quoc")
    ap.add_argument("--split", type=int, default=0,
                    help="moi file bao nhieu chuong")
    ap.add_argument("--cover", type=Path, default=None)
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--last", type=int, default=0)
    ap.add_argument("--no-number", action="store_true")
    ap.add_argument("--translate-titles", action="store_true",
                    help="dung tu dien glossary de dich cum Han trong tieu de "
                         "(mac dinh: giu tieu de Han nguyen ven)")
    ap.add_argument("--glossary", type=Path,
                    default=Path(r"f:\taitruyen\translate\glossary.md"),
                    help="dung de thay cum Han trong tieu de")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--outname", default=None,
                    help="ten file epub bo dau (mac dinh lay tu --title)")
    a = ap.parse_args()

    a._dict = load_dict(a.glossary)

    if not a.src.exists():
        sys.exit(f"Khong tim thay thu muc: {a.src}")

    ext = a.ext or (".md" if list(a.src.glob("*.md")) else ".txt")
    items = collect(a.src, ext)

    if not items:
        sys.exit(f"Khong co file {ext} trong {a.src}")

    items = [it for it in items if it[0] not in ()]
    if a.first:
        items = [it for it in items if it[0] >= a.first]
    if a.last:
        items = [it for it in items if it[0] <= a.last]

    chaps = build_chapters(items, a)
    if not chaps:
        sys.exit("Khong tao duoc chuong nao.")

    total = sum(len(c[2]) for c in chaps)
    print(f"Nguon   : {a.src}")
    print(f"Dinh dang: {ext}   Chuong: {len(chaps)}   ({chaps[0][1]} ... {chaps[-1][1]})")
    print(f"Tong dung: {total:,} ky tu HTML")

    if a.check:
        print("\n--- 3 chuong dau ---")
        for num, t, b in chaps[:3]:
            print(f"  [{num}] {t}  ({len(b)} ky tu)")
        print("\nOK (chua tao file).")
        return

    meta = {"title": a.title, "author": a.author}
    outdir = a.out.parent if a.out else Path(r"f:\taitruyen\output")
    # ten file: --outname, hoac --title, hoac ten thu muc
    stem = a.outname or a.title or a.src.name
    stem = re.sub(r'[\\/:*?"<>|]+', "", stem).strip().replace(" ", "-") or "sach"

    if a.split and a.split > 0:
        outdir.mkdir(parents=True, exist_ok=True)
        n = 0
        for i in range(0, len(chaps), a.split):
            part = chaps[i:i + a.split]
            lo, hi = part[0][0], part[-1][0]
            pm = dict(meta)
            pm["title"] = f"{a.title} ({lo}-{hi})" if len(part) < len(chaps) else a.title
            p = outdir / f"{stem}_{lo:04d}-{hi:04d}.epub"
            make_epub(part, pm, p, a.cover, a.zh)
            print(f"  ✓ {p.name}  ({len(part)} chuong, {p.stat().st_size/1048576:.1f} MB)")
            n += 1
        print(f"\nDa tao {n} file epub trong {outdir}")
        return

    out = a.out or (outdir / f"{stem}.epub")
    make_epub(chaps, meta, out, a.cover, a.zh)
    print(f"\n✓ {out}  ({out.stat().st_size/1048576:.1f} MB, {len(chaps)} chuong)")
    print(f"  mo bang: Calibre, Kobo, Apple Books, Google Play Books, hoac trinh duyet.")


if __name__ == "__main__":
    main()