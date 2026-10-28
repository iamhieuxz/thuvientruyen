# -*- coding: utf-8 -*-
"""Xem cach xung ho thuc te giua Diem So va bo/me chong trong nguon."""
import pathlib, re

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
pats = {
    "ba": r"(?:爸|爸爸|岳父|伯父|叔叔)",
    "me": r"(?:妈|妈妈|岳母|伯母|阿姨)",
    "con": r"(?:儿子|闺女|女儿|con)",
}
cnt = {k: 0 for k in pats}
samples = []
for f in sorted(D.glob("*.txt")):
    if not f.name[0].isdigit():
        continue
    t = f.read_text(encoding="utf-8", errors="replace")
    for k, p in pats.items():
        for m in re.finditer(p, t):
            cnt[k] += 1
            s = t[max(0, m.start() - 40):m.end() + 30].replace("\n", " ")
            if k in ("con",) and len(samples) < 40:
                samples.append((f.name, s))
print(cnt)
for n, s in samples:
    print(n, "|", s)
