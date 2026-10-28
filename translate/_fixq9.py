# -*- coding: utf-8 -*-
"""Dong nhat chu ky 9 (ch.96-115): Tu Ma/Tu Do, Te Y te/Cuc Y te, Cuc truong Hung/Cuc pho Hung.
Idempotent, scope tung file."""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"F:\taitruyen\data\can_bao_chan_long_vi"

FIX = {
    "0097": [(u"T\u01b0 M\u00e3 Tri\u1ec1u", u"T\u01b0 \u0110\u1ed3 Tri\u1ec1u"),
             (u"T\u01b0 M\u00e3 th\u1ea7n y", u"T\u01b0 \u0110\u1ed3 th\u1ea7n y")],
    "0114": [(u"S\u1edf Y t\u1ebf", u"C\u1ee5c Y t\u1ebf")],
    "0115": [(u"C\u1ee5c tr\u01b0\u1edfng H\u00f9ng", u"C\u1ee5c ph\u00f3 H\u00f9ng")],
}

done = []
for stem, pairs in FIX.items():
    p = next((os.path.join(OUT, f) for f in os.listdir(OUT) if f.startswith(stem + "_")), None)
    if not p:
        print("CANH: khong co file", stem)
        continue
    s = io.open(p, encoding="utf-8").read()
    before = s
    for a, b in pairs:
        s = s.replace(a, b)
    if s != before:
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        done.append(stem)
    else:
        print("khong doi:", stem)

print("Da sua:", done)
# kiem tra khong con sot
for stem in FIX:
    p = next((os.path.join(OUT, f) for f in os.listdir(OUT) if f.startswith(stem + "_")), None)
    s = io.open(p, encoding="utf-8").read()
    bad = [w for a, b in FIX[stem] for w in [a] if a in s]
    print("  sot", stem, bad or "khong con")
