# -*- coding: utf-8 -*-
import io, glob, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = "F:/taitruyen/data/can_bao_chan_long_vi/"

# 化煞丹 (ch.105-107) bi dich nham thanh "Khu Sat Dan" o ch.106-107
# -> phai la "Hoa Sat Dan" (Khu Sat Dan la 祛煞丹, dan khac o ch.58)
FIX = {"0106": [("Khu Sát Đan", "Hóa Sát Đan")],
       "0107": [("Khu Sát Đan", "Hóa Sát Đan")]}

for num, pairs in FIX.items():
    path = glob.glob(OUT + num + "_*.md")[0]
    s = io.open(path, encoding="utf-8").read()
    tot = 0
    for a, b in pairs:
        n = s.count(a)
        s = s.replace(a, b)
        tot += n
        print("%s: %r -> %r x%d" % (num, a, b, n))
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("  ghi", path, "tong thay", tot)

# kiem tra sot
for num in FIX:
    s = io.open(glob.glob(OUT + num + "_*.md")[0], encoding="utf-8").read()
    print(num, "con 'Khu Sat Dan':", s.count("Khu Sát Đan"))
