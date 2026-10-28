# -*- coding: utf-8 -*-
"""Sua sai ten o ch.108 (Kinh ca -> Ly Dau Troc) va quy uoc 'ngan' o ch.97."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"F:\taitruyen\data\can_bao_chan_long_vi"

FIX = {
    "0108": [(u"K\u00ednh ca", u"L\u00fd \u0110\u1ea7u Tr\u1ecdc")],
    "0097": [(u"c\u00e1c v\u1ecb ng\u00e0n v\u1ea1n l\u1ea7n kh\u00f4ng \u0111\u01b0\u1ee3c \u0111\u1ed9ng v\u00e0o",
              u"c\u00e1c v\u1ecb tuy\u1ec7t \u0111\u1ed1i kh\u00f4ng \u0111\u01b0\u1ee3c \u0111\u1ed9ng v\u00e0o")],
}

for stem, pairs in FIX.items():
    p = next(os.path.join(OUT, f) for f in os.listdir(OUT) if f.startswith(stem + "_"))
    s = io.open(p, encoding="utf-8").read()
    n = 0
    for a, b in pairs:
        n += s.count(a)
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("%s: thay %d choi" % (stem, n))

# kiem tra toan lo 96-115 khong con 'Kinh ca' o ngoai cac chuong cu (66-70)
for f in sorted(os.listdir(OUT)):
    if f[:4].isdigit() and 96 <= int(f[:4]) <= 115 and u"K\u00ednh ca" in io.open(
            os.path.join(OUT, f), encoding="utf-8").read():
        print("CANH: van con Kinh ca ở", f)
print("scan xong")
