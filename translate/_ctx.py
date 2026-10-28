# -*- coding: utf-8 -*-
"""Xem ngu canh cua ten can xac nhan (de them vao glossary)."""
import pathlib, re, sys

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
names = sys.argv[1:]
files = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
for nm in names:
    print("########", nm)
    n = 0
    for f in files:
        t = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(re.escape(nm), t):
            s = t[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
            print("  ", s)
            n += 1
            if n >= 6:
                break
        if n >= 6:
            break
    print()
