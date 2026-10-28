# -*- coding: utf-8 -*-
"""Chay lai dinh dang tren file da dich: bo marker "   10|", sua loi ghep."""
import re, sys
from pathlib import Path

OUT = Path(r"f:\taitruyen\data\baojian_vi")

# loi chung: cat nga giua "sau." va dau cau moi
PAT = re.compile(r'([.!?])\s*\n\s*Variation---|([.!?])\s*\n\s*\n\s*\n')


def fix(p):
    t = p.read_text(encoding="utf-8")
    orig = t
    t = re.sub(r'^[ \t]*\d+\|[ \t]*$', '', t, flags=re.M)
    t = re.sub(r'\n{3,}', '\n\n', t)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for f in sorted(OUT.glob("*.md")):
        if fix(f):
            n += 1
            print("fixed:", f.name)
    print(f"\n{len(list(OUT.glob('*.md')))} file, sua {n}")


main()