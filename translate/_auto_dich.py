# -*- coding: utf-8 -*-
"""Chay dich theo cum nho, tu lui khi gap 429, cho den het file nguon."""
import subprocess
import sys
import time

LO, HI = 151, 528
CHUNK = 8
WORKERS = 2

s = LO
while s <= HI:
    e = min(s + CHUNK - 1, HI)
    for attempt in range(1, 9):
        print(f"\n=== cum {s}-{e} | lan {attempt} ===", flush=True)
        p = subprocess.run(
            [sys.executable, "-u", "dich.py", "--from", str(s), "--to", str(e),
             "--workers", str(WORKERS)],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        print(out[-6000:], flush=True)
        if "HẾT HẠN MỨC" not in out:
            break
        time.sleep(150)
    time.sleep(35)
    s = e + 1

print("\n=== HOAN TAT 997-1282 ===", flush=True)
