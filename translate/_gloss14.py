# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl14.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")


def has_key(key):
    for l in lines:
        if "=" in l and not l.startswith("#") and not l.startswith(" "):
            if l.split("=")[0].strip() == key:
                return True
    return False


def add_entries(header, entries):
    new = []
    for zh, vi in entries:
        if has_key(zh):
            print("  DA CO (bo qua):", zh)
            continue
        new.append("%s = %s" % (zh, vi))
    if not new:
        return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]
            print("  + %d muc truoc %s" % (len(new), header[:26]))
            return
    print("  CANH: khong thay header", header)


def insert_prose(header_prefix, block):
    first = block.strip().split("\n")[0]
    if any(l.strip() == first for l in lines):
        print("  skip (da co):", first)
        return
    for i, l in enumerate(lines):
        if l.startswith(header_prefix):
            lines[i:i] = block.strip("\n").split("\n") + ["", ""]
            print("  + block truoc", header_prefix[:26])
            return
    print("  CANH: khong thay", header_prefix)


def replace_key(key, new_line):
    for i, l in enumerate(lines):
        if "=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == key:
            print("  SUA", key)
            lines[i] = new_line
            return
    print("  CANH: khong thay khoa", key)


# ── SỬA ENTRY SAI VAI ─────────────────────────────────────────
replace_key("萧木", '萧木 = Tiêu Mộc (thánh tử Chân Vũ Tông, cảnh giới tông sư viên mãn, kiêu ngạo khinh người; bị Diệp Sở một chưởng đánh văng nôn máu ở ch.181, về sau vẫn theo nhà họ Long — KHÔNG phải thầy thuốc của nhà họ Long, ch.180–189)')
replace_key("林豪", '林豪 = Lâm Hào (công tử nhà họ Lâm ở Cô Tô 姑苏林家, bạn học cũ của Khương Quân Dao, tự nhận vơ công cứu Khương Quân Long; định chiếm Khương Quân Dao và biết ngôi mộ là của Quảng Lăng Vương nhờ sư phụ; sai Triệu Ngũ đi chiêu mộ người thám mộ — ch.172–175)')
replace_key("同心蛊", '同心蛊 = Thệ Tâm Cổ (source còn gọi 噬心蛊 ở ch.172 cho CÙNG một loại cổ; U Lan gieo vào tim Khương Quân Dao để uy hiếp Diệp Sở — bản dịch thống nhất "Thệ Tâm Cổ", ch.162–172)')

add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("朱羽", 'Chu Vũ (nhân vật được nhắc ở ch.186: "tiểu bá vương" của Vương tộc Chu gia, mắt trọng đồng, chức Trấn Tây đại tướng quân, Quán Quân Hầu — chưa xuất hiện trực tiếp)'),
    ("李战鹰", 'Lý Chiến Ưng (đội trưởng chiến đội Thanh Long thuộc chiến khu Đông bộ; dẫn quân vào nhà họ Long, bị Diệp Sở hạ gục bằng ngân châm rồi bị Đông Hải Dược Vương bắn khí xuyên bụng — ch.188–189)'),
    ("赵五", 'Triệu Ngũ (biệt danh "Lão Ngũ", vệ sĩ thất phẩm tông sư của Lâm Hào, tới Bạch Lang Hội chiêu mộ người làm pháo hôi thám mộ cổ, bị đánh nhừ tử — ch.174–175)'),
    ("赵虎", 'Triệu Hổ (thuộc hạ của Long Cửu gia, được cử tới đón Diệp Sở — ch.178)'),
    ("黄海军", 'Hoàng Hải Quân (thị trưởng Giang Đô, khách mời trong buổi luyện đan của nhà họ Long — ch.179)'),
])

add_entries("## ══════ ĐỊA DANH", [
    ("姑苏林家", 'nhà họ Lâm ở Cô Tô (gia tộc của Lâm Hào; KHÁC nhà họ Lâm ở Kinh Khẩu của Lâm Tự Như — ch.172)'),
    ("青龙战队", 'chiến đội Thanh Long (đơn vị quân đội thuộc chiến khu Đông bộ, do Lý Chiến Ưng chỉ huy — ch.188)'),
])

add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("血灵芝", 'Huyết Linh Chi (một trong ba bảo vật nhà họ Long đem ra thưởng cho buổi luyện đan — ch.184)'),
    ("小还丹", 'Tiểu Hoàn Đan (đan chữa thương nhà họ Long cho Long Đỉnh Thiên uống, khiến ông đột phá ngũ phẩm đại tông sư rồi gục — ch.184–186)'),
    ("储物法宝", 'pháp bảo trữ vật (bảo vật không gian dùng cất đồ, Diệp Sở dùng để thu ba bảo vật của nhà họ Long — ch.189)'),
    ("以气成针", 'dĩ khí thành châm (dùng chân khí ngưng thành kim châm, cao hơn dĩ khí ngự châm — ch.189)'),
    ("镇西大将军", 'Trấn Tây đại tướng quân (chức của Chu Vũ, Vương tộc Chu gia — ch.186)'),
])

insert_prose("## ══════ VĂN PHONG", """
50. 同心蛊 (ch.162–168) và 噬心蛊 (ch.172) là CÙNG một loại cổ của U Lan gieo vào Khương Quân Dao — bản dịch đã thống nhất "Thệ Tâm Cổ" cho cả hai (đã sửa ch.162 và ch.168). 萧木 là thánh tử Chân Vũ Tông, KHÔNG phải thầy thuốc nhà họ Long. 姑苏林家 (nhà họ Lâm ở Cô Tô) KHÁC 京口林家 (nhà họ Lâm ở Kinh Khẩu).
""")

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG chu ky 14 phan 1. tong so dong:", len(lines))