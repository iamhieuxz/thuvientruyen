# -*- coding: utf-8 -*-
"""Kiem tra ham check_complete bang du lieu that."""
import sys, io, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"f:\taitruyen\translate")
import dich

SRC = dich.SRC
OUT = dich.OUT

print("=== 1. ban dich BI CAT (truoc khi sua) ===")
old = Path(r"f:\taitruyen\translate\_old_ch2.md")
p = OUT / "0002_第二章 偷师（上）.md"
print("  file 0002 ton tai:", p.exists())

print()
print("=== 2. doan goc chuong 1 ===")
src1 = dich.clean((SRC / dich.all_chapters()[1]).read_text(encoding="utf-8"))
sp, sq = dich.count_units(src1)
print(f"  doan={sp}  dau cau={sq}")

print()
print("=== 3. mau kiem tra ===")
# bản dịch tốt (lấy từ file _old nếu co, hoac dung ban dich chap 1 hien tai)
for f in sorted(OUT.glob("*.md")):
    if f.name.startswith("_"):
        continue
    n = int(re.match(r"^(\d+)_", f.name).group(1))
    src = dich.clean((SRC / dich.all_chapters()[n]).read_text(encoding="utf-8"))
    vi = f.read_text(encoding="utf-8")
    ok, why = dich.check_complete(src, vi)
    sp, sq = dich.count_units(src)
    dp, dq = dich.count_units_vi(vi)
    print(f"  ch{n:04d}: {'OK ' if ok else 'FAIL'}  "
          f"doan {dp}/{sp}  dau cau {dq}/{sq}  {why}")

print()
print("=== 4. truong hop cat cut gia lap ===")
full = "Đoạn một. Đoạn hai.\n\nĐoạn ba. Đoạn bốn."
cut = "Đoạn một. Đoạn hai."
print("  ban day du :", dich.check_complete(full, full))
print("  ban cat    :", dich.check_complete(full, cut))
print("  het giua chung:", dich.check_complete(full, "Đoạn một. Đoạn"))