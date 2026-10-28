# -*- coding: utf-8 -*-
"""Test epub.py: so Han, tu dien, md, txt, tao file, validate."""
import sys, io, zipfile, subprocess, tempfile, shutil
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = Path(r"f:\taitruyen\translate")
PY = sys.executable
ok_all = True


def run(*args, expect_ok=True):
    global ok_all
    r = subprocess.run([PY, str(HERE / "epub.py"), *args],
                       capture_output=True, text=True, encoding="utf-8")
    tag = "  OK  " if (r.returncode == 0) == expect_ok else "  FAIL"
    if tag == "  FAIL":
        ok_all = False
    print(f"{tag} epub.py {' '.join(args[:4])}")
    if tag == "  FAIL":
        print("   stdout:", r.stdout[-500:])
        print("   stderr:", r.stderr[-500:])
    return r


def ok(name, cond):
    global ok_all
    print(("  OK  " if cond else "  FAIL") + f" {name}")
    if not cond:
        ok_all = False
    return cond


print("=== 1. chay co ban (md) ===")
tmp = Path(tempfile.mkdtemp())
run("--check")
run("--out", str(tmp / "a.epub"))

print()
print("=== 2. nguyen van, 8 chuong ===")
run("--src", r"f:\taitruyen\truyendich_scraper\baojian",
    "--han", "--zh", "--first", "1", "--last", "8",
    "--out", str(tmp / "b.epub"), "--title", "Bao Giam")

print()
print("=== 3. tach thanh nhieu file ===")
run("--src", r"f:\taitruyen\truyendich_scraper\baojian",
    "--han", "--first", "1", "--last", "8", "--split", "3",
    "--out", str(tmp / "c.epub"))

print()
print("=== 4. dich tieu de ===")
run("--src", r"f:\taitruyen\truyendich_scraper\baojian",
    "--han", "--translate-titles", "--first", "1", "--last", "3",
    "--out", str(tmp / "d.epub"))

print()
print("=== 5. validate tat ca file vua tao ===")
files = sorted(tmp.glob("*.epub"))
r = subprocess.run([PY, str(HERE / "checkepub.py"), *[str(f) for f in files]],
                   capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-700:] if r.returncode == 0 else "LOI:\n" + r.stdout[-900:])
ok("checkepub pass het", r.returncode == 0)

print()
print("=== 6. kiem tra noi dung file ===")
b = tmp / "b.epub"
if b.exists():
    with zipfile.ZipFile(b) as z:
        names = z.namelist()
        ok("co mimetype", "mimetype" in names)
        ok("mimetype dau tien", names[0] == "mimetype")
        ok("co 8 chuong", sum(1 for n in names if n.endswith(".xhtml")) == 8)
        x = z.read("OEBPS/ch0001.xhtml").decode("utf-8")
        ok("chua bi cat doi", x.rstrip().endswith("</html>"))
        ok("co p thuong", "<p" in x)
        toc = z.read("OEBPS/toc.ncx").decode("utf-8")
        ok("toc co 8 muc", toc.count("<navPoint") == 8)

print()
print("=== 7. xu ly truong hop bien ===")
# 7a: file rong bi bo qua, file hop van duoc giu
bad = tmp / "bad"
bad.mkdir()
(bad / "1_a.txt").write_text("Noi dung A.", encoding="utf-8")
(bad / "2_rong.txt").write_text("", encoding="utf-8")          # rong -> bo qua
(bad / "3_c.txt").write_text("   \n\n  \n", encoding="utf-8")  # toan khoang trang
run("--src", str(bad), "--check", "--out", str(tmp / "e.epub"))
e = tmp / "e.epub"
if e.exists():
    with zipfile.ZipFile(e) as z:
        n = sum(1 for x in z.namelist() if x.endswith(".xhtml"))
        ok("bo qua 2 file rong", n == 1)

# 7b: thu muc khong ton tai -> phai bao loi
run("--src", str(tmp / "khong_ton_tai"), "--check", expect_ok=False)

# 7c: thu muc rong -> phai bao loi
empty = tmp / "empty"
empty.mkdir()
run("--src", str(empty), "--check", expect_ok=False)

# 7d: ky tu hong va marker trong txt -> phai duoc lam sach
dirty = tmp / "dirty"
dirty.mkdir()
(dirty / "0001_x.txt").write_text(
    "Tiêu đề X\n\n   10|\n\ufffd\ufffdSáu ngày\ufffd\ufffd ăn cơm.\n", encoding="utf-8")
run("--src", str(dirty), "--check", "--out", str(tmp / "f.epub"))
f_ = tmp / "f.epub"
if f_.exists():
    with zipfile.ZipFile(f_) as z:
        txt = "".join(z.read(x).decode("utf-8")
                      for x in z.namelist() if x.endswith(".xhtml"))
        ok("da bo marker dong", "10|" not in txt)
        ok("da bo ky tu hong", "\ufffd" not in txt)

shutil.rmtree(tmp, ignore_errors=True)
print()
print("KET QUA:", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)