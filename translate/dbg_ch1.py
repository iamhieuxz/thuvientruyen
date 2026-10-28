# -*- coding: utf-8 -*-
"""Kiem tra ban dich chuong 1 bang chinh validate() + check_complete() cua dich.py."""
import sys, io, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"f:\taitruyen\translate")
import dich

ROOT = Path(r"f:\taitruyen")
src = dich.clean((ROOT / "truyendich_scraper" / "baojian" / "0001_第一章 兄妹.txt")
                 .read_text(encoding="utf-8", errors="replace"))
vi_path = ROOT / "data" / "baojian_vi" / "0001_第一章 兄妹.md"
raw = vi_path.read_text(encoding="utf-8")
body = re.sub(r"^<!--.*?-->\s*", "", raw, flags=re.S)
glossary = (ROOT / "translate" / "glossary.md").read_text(encoding="utf-8")

print("=== validate() ===")
errs = dich.validate(body, glossary)
print("  loi:", errs if errs else "KHONG CO")

print()
print("=== check_complete() ===")
ok, why = dich.check_complete(src, body)
print(f"  ok={ok}  why={why!r}")

sp, sq = dich.count_units(src)
dp, dq = dich.count_units_vi(body)
print(f"  doan:  goc {sp} -> vi {dp}")
print(f"  dau:   goc {sq} -> vi {dq}")
print(f"  ky tu: goc {len(src)} -> vi {len(body)}")

print()
print("=== FORBID / Han sot ===")
han = re.findall(r"[\u4e00-\u9fff]+", body)
print("  chu Han con lai:", han if han else "KHONG CO")

print()
print("=== xung ho 'con' ===")
for m in re.finditer(r"(?i)(?:toi|anh|chu|bo|me|chau)\b[^.!?\n]{0,14}?\bcon\b(?![\wàáảãạăâêôơưý])", body):
    print("  ", repr(m.group(0)))

print()
print("=== kiem tra cac ten phai khop glossary ===")
for han_t, viet in [("秦风", "Tần Phong"), ("秦葭", "Tần Gia"), ("胡保国", "Hồ Bảo Quốc"),
                    ("胡大叔", "chú Hồ"), ("大黄", "Đại Hoàng"), ("仓州", "Thương Châu"),
                    ("粮票", "phiếu lương thực"), ("烧饼", "bánh nướng"),
                    ("废品收购站", "trạm mua bán phế liệu"), ("铁路小学", "trường Tiểu học Đường sắt")]:
    print(f"  {han_t:12} -> {viet:28} trong ban dich: {'CO' if viet.lower() in body.lower() else 'KHONG'}")

print()
print("=== marker / Variation ===")
print("  marker so:", len(re.findall(r"^\s*\d+\|\s*$", body, flags=re.M)))
print("  'Variation':", body.count("Variation"))
print("  ufffd:", body.count("\ufffd"))