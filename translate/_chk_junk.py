# -*- coding: utf-8 -*-
"""Xem cac file nguon moi co rac quang ca / ghi chu tac gia."""
import pathlib, re

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
for f in sorted(D.glob("*.txt")):
    if not f.name[0].isdigit():
        continue
    t = f.read_text(encoding="utf-8", errors="replace")
    if re.search(r"微信|ps：|P\.S|作者的话", t):
        print("=== ", f.name)
        print(t[-600:])
        print()
