# Chu kỳ 7: đồng nhất thuật ngữ + sửa title ch.69 (toàn corpus, idempotent)
import io, os, re, sys, glob, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DATA = "F:/taitruyen/data/can_bao_chan_long_vi"

REP = [
    # 刀疤陈 (Đao Sẹo Trần) bị dịch hụt "Sẹo": nguồn 刀疤哥, không phải 刀哥
    ("cơ duyên của Đao ca", "cơ duyên của Đao Sẹo ca"),
    ("“Đao ca, anh không sao chứ?”", "“Đao Sẹo ca, anh không sao chứ?”"),
    # nguồn viết nhầm 梦小刀 1 chỗ -> Mạnh Tiểu Đao
    ("Mộng Tiểu Đao", "Mạnh Tiểu Đao"),
    # 老大 = lão đại (thủ lĩnh), phân biệt với 大哥 = đại ca (xưng hô anh em)
    # Chu y: 0006/0019 la 几位大哥 => van giu "Mấy vị đại ca"; chi 0068 moi la 几位老大.
    ("không ngờ đại ca của Bạch Lang Hội lại là một cô gái",
     "không ngờ lão đại của Bạch Lang Hội lại là một cô gái"),
    ("“Đại ca, vị này chính là Diệp tông sư.”", "“Lão đại, vị này chính là Diệp tông sư.”"),
    ("“Cô chính là đại ca của Bạch Lang Hội?”", "“Cô chính là lão đại của Bạch Lang Hội?”"),
    ("“Mấy vị đại ca, mục tiêu của Hắc Hổ Hội", "“Mấy vị lão đại, mục tiêu của Hắc Hổ Hội"),
    # 会长 / 会主 -> hội chủ (nhất quán theo ch.61, 67, 68, 71, 75)
    ("Phó hội trưởng và hội trưởng", "Phó hội chủ và hội chủ"),
    ("hội trưởng hai hội", "hội chủ hai hội"),
    ("Phó hội trưởng Tả Tu Đao", "Phó hội chủ Tả Tu Đao"),
    ("bên hội trưởng đã thành công", "bên hội chủ đã thành công"),
    ("“Đợi hội trưởng trở về", "“Đợi hội chủ trở về"),
    ("trước khi hội trưởng trở về", "trước khi hội chủ trở về"),
    # 省会城市 -> tỉnh thành (theo ch.62, 67)
    ("chuẩn bị tiến quân vào thành phố tỉnh", "chuẩn bị tiến quân vào tỉnh thành"),
    # 将他给轮了 -> "làm nhục" làm mất nghĩa
    ("rồi tìm mấy gã đồng tính, làm nhục hắn", "rồi tìm mấy gã đồng tính, thay nhau cưỡng bức hắn"),
]

doi = []
for f in sorted(glob.glob(os.path.join(DATA, "*.md"))):
    txt = io.open(f, encoding="utf-8").read()
    body = txt
    for a, b in REP:
        if a in body:
            body = body.replace(a, b)
    if body != txt:
        io.open(f, "w", encoding="utf-8", newline="\n").write(body)
        doi.append(os.path.basename(f))

# title ch.69: nguồn 你挡得住吗 nói với Bạch Hạc lão nhân (nam), không phải "cô"
NEW69 = "Chương 69: Một quyền hai mươi năm công phu, mày đỡ nổi không?"
TP = "F:/taitruyen/translate/titles_can_bao_chan_long.json"
t = json.load(io.open(TP, encoding="utf-8"))
if t.get("69") != NEW69:
    t["69"] = NEW69
    json.dump(t, io.open(TP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("titles json: cap nhat 69")

for f in sorted(glob.glob(os.path.join(DATA, "0069_*.md"))):
    txt = io.open(f, encoding="utf-8").read()
    new = re.sub(r"(?m)^#? ?Chương 69:.*$", "# " + NEW69, txt)
    if new != txt:
        io.open(f, "w", encoding="utf-8", newline="\n").write(new)
        print("heading 69 doi")

print("Files doi:", len(doi))
for k in doi:
    print("  ", k)
