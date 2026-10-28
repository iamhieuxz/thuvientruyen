# Chu ky 8 (b): dong nhat cach goi + doi title chua tu cam (88, 90)
# Moi rule gan voi file cu the, co guard idempotent.
import io, os, re, sys, glob, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DATA = "F:/taitruyen/data/can_bao_chan_long_vi"
TJ = "F:/taitruyen/translate/titles_can_bao_chan_long.json"

T82 = "Chương 82: Trang Viên Hồ Quảng Lăng"
T88 = "Chương 88: Xem anh trị em thế nào"
T90 = "Chương 90: Tại ông quá yếu"

# (prefix, chu_so, doi_thay)  — doi_thay la (old, new) kieu replace chuoi thuong
PLAIN = [
    ("0081", "Đường đường là Vua Lầu Giang Nam", "Đường đường là Lâu Vương Giang Nam"),
    ("0085", "biệt thự Quảng Lăng Hồ", "biệt thự hồ Quảng Lăng"),
    ("0091", "giúp Tôn Ngữ Nhu thối thể", "giúp Tôn Ngữ Nhu tối thể"),
    ("0092", "thành viên hạng Huyền của Hộ Long Vệ", "thành viên Huyền tự của Hộ Long Vệ"),
]

TITLES = [("0082", "82", T82), ("0088", "88", T88), ("0090", "90", T90)]

doi = []
for prefix, old, new in PLAIN:
    p = glob.glob(os.path.join(DATA, prefix + "_*.md"))[0]
    txt = io.open(p, encoding="utf-8").read()
    if new in txt:
        continue
    if old not in txt:
        print("CANH: khong thay chuoi o %s -> %r" % (prefix, old[:40]))
        continue
    io.open(p, "w", encoding="utf-8", newline="\n").write(txt.replace(old, new))
    doi.append(os.path.basename(p))

tj = json.load(io.open(TJ, encoding="utf-8"))
for prefix, num, newtitle in TITLES:
    p = glob.glob(os.path.join(DATA, prefix + "_*.md"))[0]
    txt = io.open(p, encoding="utf-8").read()
    lines = txt.split("\n")
    idx = [i for i, l in enumerate(lines) if l.lstrip("# ").startswith("Chương %s:" % num)]
    if len(idx) != 1:
        print("CANH: %s co %d dong match title -> bo qua file" % (prefix, len(idx)))
        continue
    lines[idx[0]] = "# " + newtitle          # PHAI du "# "
    new = "\n".join(lines)
    if new != txt:
        io.open(p, "w", encoding="utf-8", newline="\n").write(new)
        doi.append(os.path.basename(p))
    if tj.get(num) != newtitle:
        tj[num] = newtitle
        doi.append("titles json [%s]" % num)
io.open(TJ, "w", encoding="utf-8", newline="\n").write(
    json.dumps(tj, ensure_ascii=False, indent=2))

sot = []
for p in glob.glob(os.path.join(DATA, "*.md")):
    t = io.open(p, encoding="utf-8").read()
    for bad in ("Quảng Lăng Hồ", "Vua Lầu", "thối thể", "hạng Huyền",
                "Ngươi Tưởng", "trừng trị ngươi", "Là ngươi"):
        if bad in t:
            sot.append("%s: %s" % (os.path.basename(p)[:4], bad))
print("Da sua:", ", ".join(doi) if doi else "khong co gi doi")
print("Con sot:", sot if sot else "khong con")
