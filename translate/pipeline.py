# -*- coding: utf-8 -*-
"""
Duong ong: ban dich Viet (data/baojian_vi, dich san, khong dung API) -> kiem tra -> epub.

  python pipeline.py --to 50         # kiem tra + dong goi chuong 1..50
  python pipeline.py --split 50      # tach moi 50 chuong / file
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"f:\taitruyen")
TR = ROOT / "translate"
PY = sys.executable


def run(script, *args, title=""):
    print()
    print("=" * 66)
    print(f">>> {title or script}")
    print("=" * 66, flush=True)
    r = subprocess.run([PY, str(TR / script), *args],
                       encoding="utf-8", errors="replace")
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--to", dest="hi", type=int, default=1282)
    ap.add_argument("--split", type=int, default=0)
    ap.add_argument("--title", default="Bao Giam")
    ap.add_argument("--author", default="Dai Nham")
    ap.add_argument("--outname", default="")
    a = ap.parse_args()

    run("check.py", title="Kiem tra ban dich")

    eargs = ["--title", a.title, "--author", a.author,
             "--first", str(a.first), "--last", str(a.hi)]
    if a.split:
        eargs += ["--split", str(a.split)]
    if a.outname:
        eargs += ["--outname", a.outname]
    run("epub.py", *eargs, title="Dong goi epub")
    run("checkepub.py", title="Kiem tra file epub")

    print()
    print("=" * 66)
    print("XONG. File epub nam trong:", ROOT / "output")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
