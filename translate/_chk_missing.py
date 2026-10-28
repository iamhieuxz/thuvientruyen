# -*- coding: utf-8 -*-
"""Ten han viet trong glossary chua co trong _names_new.txt (>= 8 lan)."""
import pathlib, re

G = pathlib.Path(r"f:/taitruyen/translate/glossary_can_bao_chan_long.txt")
gl = G.read_text(encoding="utf-8")
have = set(re.findall(r"[\u4e00-\u9fff]{2,4}", gl))

rows = []
for line in pathlib.Path(r"f:/taitruyen/translate/_names_new.txt").read_text(
        encoding="utf-8").splitlines():
    if not line.strip():
        continue
    n, name = line.split("\t", 1)
    if int(n) < 8:
        continue
    if name in have:
        continue
    rows.append((int(n), name))

for n, name in rows:
    print(n, name)
