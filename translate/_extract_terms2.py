# -*- coding: utf-8 -*-
"""Canh gioi vo dao + to chuc + dia danh trong nguon moi."""
import pathlib, re, collections

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
files = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
text = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)

c = collections.Counter()
for m in re.finditer(r"([\u4e00-\u9fff]{1,4}境)", text):
    c[m.group(1)] += 1
print("=== CANH GIOI ===")
for k, v in c.most_common(40):
    print(v, k)

c2 = collections.Counter()
for m in re.finditer(r"([\u4e00-\u9fff]{2,6}(?:宫|殿|阁|殿|山|宗|派|城|谷|海|域|州|郡|县|阁|楼|府|殿|盟|会|教|殿))", text):
    c2[m.group(1)] += 1
print("\n=== TO CHUC / DIA DANH ===")
for k, v in c2.most_common(50):
    print(v, k)

c3 = collections.Counter()
for m in re.finditer(r"([\u4e00-\u9fff]{2,4}(?:体|脉|骨|气|功|诀|丹|针|剑|刀|枪|拳|印|符|阵|纹|珠|丹))", text):
    c3[m.group(1)] += 1
print("\n=== THUAT NGU ===")
for k, v in c3.most_common(60):
    print(v, k)
