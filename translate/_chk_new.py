# -*- coding: utf-8 -*-
"""Kiem tra nhanh nguon moi: doan/cau, do dai, ky tu la."""
import pathlib, re, collections

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
fs = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
ps, qs, ls = [], [], []
for f in fs:
    t = f.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"^[ \t]*\d+\|[ \t]*$", "", t, flags=re.M)
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    ps.append(len(paras))
    qs.append(len(re.findall(r"[。！？…”]", t)))
    ls.append(len(t))
print("files", len(fs))
print("paras min/max/avg", min(ps), max(ps), round(sum(ps) / len(ps), 1))
print("marks min/max/avg", min(qs), max(qs), round(sum(qs) / len(qs), 1))
print("len  min/max/avg", min(ls), max(ls), round(sum(ls) / len(ls)))
print("paras dist", sorted(collections.Counter(ps).items())[:6])
# ky tu Han con lai trong tieu de -> se ra ten file
bad = set()
for f in fs:
    t = f.name.split("_", 1)[1].rsplit(".", 1)[0]
    for ch in t:
        if ch in "\\/:*?\"<>|":
            bad.add(ch)
print("illegal filename chars:", bad)
