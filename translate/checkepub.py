# -*- coding: utf-8 -*-
"""Kiem tra file EPUB co hop le khong (EPUB 3 + tuong thich EPUB 2)."""
import sys, zipfile, re
from pathlib import Path
from xml.etree import ElementTree as ET

OK, BAD = "  OK  ", "  FAIL"


def check(p):
    errs, warns = [], []

    if not p.exists():
        return ["khong ton tai file"], []

    with zipfile.ZipFile(p) as z:
        names = z.namelist()

        # 1. mimetype phai dung dau tien, khong nen
        if not names or names[0] != "mimetype":
            errs.append("mimetype khong phai file dau tien")
        else:
            if z.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
                errs.append("mimetype bi nen (phai ZIP_STORED)")
            if z.read("mimetype") != b"application/epub+zip":
                errs.append("noi dung mimetype sai")

        # 2. container.xml tro toi opf
        if "META-INF/container.xml" not in names:
            errs.append("thieu META-INF/container.xml")
        else:
            root = ET.fromstring(z.read("META-INF/container.xml"))
            ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
            rf = root.find(".//c:rootfile", ns)
            if rf is None:
                errs.append("container.xml khong co rootfile")
            else:
                opf_path = rf.get("full-path")
                if opf_path not in names:
                    errs.append(f"opf khong ton tai: {opf_path}")
                else:
                    errs += check_opf(z, opf_path)

        # 3. moi file xhtml phai XML hop le
        for n in names:
            if n.endswith(".xhtml") or n.endswith(".html"):
                try:
                    ET.fromstring(z.read(n))
                except ET.ParseError as e:
                    errs.append(f"XML hong {n}: {e}")

        # 4. cac file trong manifest phai ton tai
        warns.append(f"tong {len(names)} file trong epub")

    return errs, warns


def check_opf(z, opf_path):
    errs = []
    root = ET.fromstring(z.read(opf_path))
    ns = {"o": "http://www.idpf.org/2007/opf",
          "dc": "http://purl.org/dc/elements/1.1/"}
    names = z.namelist()
    base = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""

    def full(href):
        return f"{base}/{href}" if base else href

    # metadata bat buoc
    for tag in ("identifier", "title", "language"):
        if root.find(f".//dc:{tag}", ns) is None:
            errs.append(f"thieu dc:{tag} trong metadata")

    # manifest
    mitems = root.findall(".//o:manifest/o:item", ns)
    if not mitems:
        errs.append("manifest rong")
    for it in mitems:
        h = it.get("href")
        if h and full(h) not in names:
            errs.append(f"manifest tro toi file thieu: {h}")

    # spine phai co item
    spine = root.findall(".//o:spine/o:itemref", ns)
    if not spine:
        errs.append("spine rong (khong co chuong nao)")

    ids = {it.get("id") for it in mitems}
    for sr in spine:
        if sr.get("idref") not in ids:
            errs.append(f"spine tro idref khong ton tai: {sr.get('idref')}")

    # toc
    toc = root.find(".//o:spine", ns)
    if toc is not None and toc.get("toc"):
        if toc.get("toc") not in ids:
            errs.append("spine toc tro toi manifest khong co")

    return errs


def main():
    args = sys.argv[1:]
    if not args:
        files = sorted(Path("f:\\taitruyen\\output").glob("*.epub"))
    else:
        files = [Path(a) for a in args]

    if not files:
        print("Khong co file epub de kiem tra.")
        return 0

    total = 0
    for f in files:
        errs, warns = check(f)
        size = f.stat().st_size / 1048576
        print(f"\n{'='*60}\n{f.name}  ({size:.2f} MB)")
        for w in warns:
            print(f"  ·    {w}")
        if errs:
            for e in errs:
                print(f"{BAD} {e}")
            total += len(errs)
        else:
            print(f"{OK} EPUB hop le")
    print(f"\n{'='*60}")
    print("TAT CA HOP LE" if total == 0 else f"{total} LOI")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())