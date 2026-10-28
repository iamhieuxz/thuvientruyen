import io, json, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"F:/taitruyen/data/can_bao_chan_long_vi"

# 1) ghep ten trang suc phat sinh o ch.60/62/64 -> dung o ch.65
for p in glob.glob(OUT + r"\0065_*.md"):
    t = io.open(p, encoding="utf-8").read()
    n = t.count("Sâm Lâm Chi Tâm")
    if n:
        t = t.replace("Sâm Lâm Chi Tâm", "Trái Tim Rừng Xanh")
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(t)
    print("0065:", n, "luot doi")

# 2) title ch.60 khop cach goi dung trong body (trung tam trang suc Giang Nam)
TP = r"F:/taitruyen/translate/titles_can_bao_chan_long.json"
titles = json.load(io.open(TP, encoding="utf-8"))
OLD = "Chương 60: Tiệm châu báu Giang Nam"
NEW = "Chương 60: Trung tâm trang sức Giang Nam"
if titles.get("60") != NEW:
    titles["60"] = NEW
    with io.open(TP, "w", encoding="utf-8", newline="\n") as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)
    print("title json ok")

for p in glob.glob(OUT + r"\0060_*.md"):
    t = io.open(p, encoding="utf-8").read()
    if OLD in t:
        t = t.replace(OLD, NEW)
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(t)
        print("heading ok:", p[-20:])
