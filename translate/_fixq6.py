import io, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"F:/taitruyen/data/can_bao_chan_long_vi"
TP = r"F:/taitruyen/translate/titles_can_bao_chan_long.json"

# (old, new) — ap dung toan bo cac bai da promote
GLOBAL = [
    ("Trung tâm trang sức Giang Nam", "Hiệu kim hoàn Giang Nam"),
    ("trung tâm trang sức Giang Nam", "hiệu kim hoàn Giang Nam"),
    ("Tiệm trang sức Giang Nam", "Hiệu kim hoàn Giang Nam"),
    ("tiệm trang sức Giang Nam", "hiệu kim hoàn Giang Nam"),
    ("Hàng trang sức Giang Nam", "Hiệu kim hoàn Giang Nam"),
    ("hàng trang sức Giang Nam", "hiệu kim hoàn Giang Nam"),
    ("Tiệm trang sức", "Hiệu kim hoàn"),
    ("tiệm trang sức", "hiệu kim hoàn"),
    ("bảo vật trấn điếm", "bảo vật trấn tiệm"),
    ("Tiền Sâm Hào", "Tiền Hào Sâm"),
    ("nữ hướng dẫn viên", "nữ nhân viên bán hàng"),
    ("Nữ hướng dẫn viên", "Nữ nhân viên bán hàng"),
    ("tử la lan", "Tử La Lan"),
    ("trăm phương ngàn kế", "trăm phương nghìn kế"),
    ("đấu giá được giá mười trăm triệu", "đấu giá được cái giá trên trời tới một tỷ"),
]

log = []
for p in sorted(glob.glob(OUT + r"\00*.md")):
    t = io.open(p, encoding="utf-8").read()
    orig = t
    for old, new in GLOBAL:
        if old in t:
            t = t.replace(old, new)
    if t != orig:
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(t)
        log.append(p.split("\\")[-1][:4])
print("files doi:", log)

titles = json.load(io.open(TP, encoding="utf-8"))
titles["60"] = "Chương 60: Hiệu kim hoàn Giang Nam"
with io.open(TP, "w", encoding="utf-8", newline="\n") as f:
    json.dump(titles, f, ensure_ascii=False, indent=2)
print("title 60 ->", titles["60"])
