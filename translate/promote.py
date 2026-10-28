# -*- coding: utf-8 -*-
"""Hop thuc hoa cac ban nhap _NNNN_nhap.md / _NNNN_cat.md da sua thu cong.

Ban nhap do dich.py ghi ra khi chuong bi 'invalid' (validate fail) hoac 'cut'
(bi cat). Sua tay xong thi chay lenh nay de chuyen thanh file chinh thuc,
KHONG can goi API dich lai.

Dung:
  python promote.py --book can_bao_chan_long
  python promote.py --book baojian
Duong dan/glossary/titles/state lay tu dich.py BOOKS theo --book.
"""
import argparse, json, os, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
for _s in (sys.stdout, sys.stderr):        # Windows cp1252 lam crash khi in chu Han
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import dich  # noqa: E402


def src_of(story, cmap, src):
    """Tra (ten_chuong_han_goc, van_ban_goc_da_chuan_hoa) cua so chuong truyen."""
    row = next((v for v in cmap.values() if v.get("story") == story), None)
    if row is None:
        f = next(pathlib.Path(src).glob(f"{story:04d}_*.txt"))
        raw = f.name.split("_", 1)[1].rsplit(".", 1)[0]
        text = f.read_text(encoding="utf-8", errors="replace")
    else:
        raw = row["title"]
        text = (pathlib.Path(src) / f"{row['file']:04d}_{raw}.txt").read_text(
            encoding="utf-8", errors="replace")
    return raw, dich.dedup_repeats(dich.strip_src_junk(dich.clean(text)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=os.environ.get("BOOK", "can_bao_chan_long"),
                    choices=sorted(dich.BOOKS))
    a = ap.parse_args()
    dich.set_book(a.book)

    cmap = dich.load_chapter_map()
    titles = dich.load_titles()
    st = dich.load_state()
    drafts = sorted(dich.OUT.glob("_*.md"))
    if not drafts:
        print("Khong co ban nhap nao.")
        return

    for p in drafts:
        s = int(p.name[1:5])
        parts = p.read_text(encoding="utf-8").split("\n\n", 1)
        if len(parts) < 2:
            print(f"BO QUA {p.name}: file rong/chua comment loi, chua co than bai")
            continue
        body = re.sub(r"(?m)^={2,}[^\n]*={0,}$", "", parts[1])
        body = dich.strip_markdown(body).strip()
        try:
            fname, stext = src_of(s, cmap, dich.SRC)
        except StopIteration:
            print(f"BO QUA {s:04d}: khong tim thay chuong goc")
            continue
        comp, why = dich.check_complete(stext, body)
        errs = dich.validate(body, "")
        if not comp or errs:
            print(f"GIU LAI {s:04d}: complete={comp} {why} errs={errs[:2]}")
            continue
        title = titles.get(s)
        if not title:
            print(f"THIEU TEN {s:04d} (chua co trong titles json)")
            continue
        if not body.endswith("(Còn tiếp)"):
            body += "\n\n(Còn tiếp)"
        hdr = f"<!-- chuong {s:04d} | {fname} | dich boi AI + glossary -->\n\n"
        dst = dich.OUT / f"{s:04d}_{fname}.md"
        dst.write_text(hdr + f"# {title}\n\n" + body + "\n", encoding="utf-8")
        p.unlink()
        if s in st["failed"]:
            st["failed"].remove(s)
        if s not in st["done"]:
            st["done"].append(s)
        dich.save_state(st)
        print(f"XUC TIEN {s:04d} -> {dst.name}")

    print("con drafts:", [x.name for x in dich.OUT.glob("_*.md")])


if __name__ == "__main__":
    main()
