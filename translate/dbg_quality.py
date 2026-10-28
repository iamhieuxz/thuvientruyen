# -*- coding: utf-8 -*-
"""So sanh goc vs ban dich: do dai, so doan, phat hien cat cut."""
import sys, io, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"f:\taitruyen")
SRC = ROOT / "truyendich_scraper" / "baojian"
OUT = ROOT / "data" / "baojian_vi"


def paras(t):
    t = re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    return [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]


print(f"{'CH':>5} {'GOC ky tu':>10} {'DICH ky tu':>11} {'DOAN goc':>9} "
      f"{'DOAN dich':>10} {'ty le':>7}  ket")
print("-" * 78)

for n in sorted(int(re.match(r"^(\d+)_", f.name).group(1))
                for f in OUT.glob("*.md")):
    src = list(SRC.glob(f"{n:04d}_*.txt"))
    dst = list(OUT.glob(f"{n:04d}_*.md"))
    if not src or not dst:
        continue
    s = src[0].read_text(encoding="utf-8", errors="replace")
    d = dst[0].read_text(encoding="utf-8", errors="replace")

    sp = paras(s)
    dp = paras(d)
    slen = sum(len(x) for x in sp)
    dlen = sum(len(x) for x in dp)
    ratio = dlen / slen if slen else 0

    # so doan hinh thuc ("...") doi chieu
    sq = sum(x.count("“") for x in sp)
    dq = sum(x.count("“") for x in dp)

    warn = []
    if ratio < 0.75:
        warn.append("NGHI DOAN BI CAT")
    if sq and dq < sq * 0.9:
        warn.append(f"NGHI THIEO THOAI ({dq}/{sq})")
    if d and not d.rstrip().endswith((".", "”", "!", "?", '"')):
        warn.append("KHONG KET THUC CAU")
    if len(d) < 2000:
        warn.append("NGHI QUA NGAN")

    print(f"{n:5d} {slen:10,} {dlen:11,} {len(sp):9d} {len(dp):10d} "
          f"{ratio:6.2f}x  {'; '.join(warn) or 'ok'}")

print()
print("=== so sanh chi tiet chuong 2 ===")
s = list(SRC.glob("0002_*.txt"))[0].read_text(encoding="utf-8", errors="replace")
d = list(OUT.glob("0002_*.md"))[0].read_text(encoding="utf-8", errors="replace")
sp, dp = paras(s), paras(d)
print(f"doan goc={len(sp)}  doan dich={len(dp)}")
print()
print("3 doan goc cuoi:")
for p in sp[-3:]:
    print("  G|", p[:110])
print()
print("3 doan dich cuoi:")
for p in dp[-3:]:
    print("  D|", p[:110])