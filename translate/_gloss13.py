# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl13.txt")
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


add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("朱萱", 'Chu Huyên (nữ bách hộ của Hộ Long Vệ, con gái Vương tộc Chu gia, mặc đồ đỏ, được Tô Định Hạ phái tới Giang Đô hỗ trợ điều tra cổ mộ; bề ngoài hòa nhã, trong lòng toan tính — ch.167–215)'),
    ("周青青", 'Chu Thanh Thanh (nữ đệ tử phái Nga Mi, sư tỷ của Khương Quân Dao, tính tình dịu dàng, tới Giang Đô cùng sư phụ Hồng Vân — ch.185–191)'),
    ("秦思慕", 'Tần Tư Mộ (bạn thân của Gia Cát Triết Nhã, tính kiêu ngạo, mắc bệnh lạ mất nước trầm trọng, được đưa tới Giang Đô nhờ Diệp Sở chữa — ch.214–219)'),
    ("杜灵儿", 'Đỗ Linh Nhi (nữ đệ tử của Bạch Hạc chân nhân, gọi ông là "sư tôn", theo sư môn tới Thần Nông Giá tìm dược liệu — ch.219–221)'),
    ("白鹤真人", 'Bạch Hạc chân nhân (cao thủ của phái Võ Đang, trung niên gầy gò, dẫn đồ đệ tới Thần Nông Giá; về sau giao chiến với Diệp Sở — ch.220–222)'),
    ("朱家", 'Vương tộc Chu gia (vương tộc danh giá của Đại Hạ, gia tộc của Chu Huyên; trong lịch sử từng có lão Vũ Vương đánh lui liên quân các nước — ch.186)'),
])

add_entries("## ══════ ĐỊA DANH", [
    ("京口机场", 'sân bay Kinh Khẩu (nơi Diệp Sở đáp xuống khi tới thành Kinh Khẩu — ch.154)'),
    ("西蜀", 'Tây Thục (vùng đất phía tây, nơi có phái Nga Mi — ch.177)'),
    ("神农架", 'Thần Nông Giá (vùng núi hoang có dược liệu quý và dị hỏa, nơi phái Võ Đang và các thế lực kéo tới — ch.219–225)'),
])

add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("延寿丸", 'Diên Thọ Hoàn (đan kéo dài tuổi thọ, Diệp Sở sai Bạch Hiểu Hiểu thu gom dược liệu để luyện — ch.170)'),
    ("龙虎筋骨丹", 'Long Hổ Cân Cốt Đan (đan phương Diệp Sở đưa ra để chữa bát mạch cho Long Đỉnh Thiên, còn giúp tăng thể phách — ch.184–190)'),
    ("火凤凰", 'Hỏa Phượng Hoàng (châm pháp thượng cổ do Thần Nông sáng tạo, dùng khí nóng cực mạnh để trục độc — ch.190)'),
    ("望闻问切", 'vọng văn vấn thiết (bốn bước chẩn bệnh của đông y: nhìn, nghe, hỏi, bắt mạch — ch.190)'),
    ("武尊", 'Vũ Tôn (cảnh giới võ đạo cao hơn đại tông sư, dùng cho các cường giả ở Thần Nông Giá — VIẾT "Vũ Tôn", ch.219–225)'),
    ("圣子", 'thánh tử (người kế vị được tông môn bồi dưỡng, như thánh tử Chân Vũ Tông — ch.181–183)'),
    ("省首", 'tỉnh trưởng (chức quan đứng đầu một tỉnh; công tử nhà tỉnh trưởng là chỗ dựa của Hoàng Phủ Bích Nguyệt — ch.165)'),
    ("异火", 'dị hỏa (ngọn lửa kỳ dị trong truyền thuyết, cực mạnh khi luyện đan; Diệp Sở vào Thần Nông Giá tìm nó — ch.219–225)'),
    ("蛟龙血", 'giao long huyết (máu giao long, nguyên liệu quý — ch.220)'),
])

add_entries("## ══════ QUY TẮC XƯNG HÔ", [
    ("无量天尊", 'Vô Lượng Thiên Tôn (câu niệm cửa miệng của đạo sĩ — giữ nguyên, ch.181–191)'),
    ("姜师妹", 'Khương sư muội (cách Chu Thanh Thanh và các đệ tử Nga Mi gọi Khương Quân Dao — ch.177)'),
    ("林公子", 'Lâm công tử (cách Khương Hải Vân gọi Lâm Hào — ch.172)'),
    ("龙卫总部", 'tổng bộ Hộ Long Vệ (đặt tại đế đô, nơi Tô Định Hạ làm việc — ch.167)'),
    ("诸国联军", 'liên quân các nước (đội quân nhiều nước từng bị lão Vũ Vương nhà họ Chu đánh bại — ch.186)'),
])

replace_key("红云", '红云 = Hồng Vân (đạo cô phái Nga Mi, tức 红云真人 = Hồng Vân chân nhân, sư phụ của Chu Thanh Thanh; tự xưng "bần ni", tính thẳng thắn, cảnh cáo Diệp Sở rằng Chân Vũ Tông sẽ không bỏ qua vụ giết Đông Hải Dược Vương — ch.179–191)')

insert_prose("## ══════ VĂN PHONG", """
49. 红云 (ch.179) và 红云真人 (ch.179, cách Long Trấn Nhạc gọi) là CÙNG một người — Hồng Vân, đạo cô phái Nga Mi. 朱萱 là bách hộ Hộ Long Vệ thuộc Vương tộc Chu gia, KHÔNG phải nha hoàn hay người hầu; 朱家 là vương tộc, khác hẳn các gia tộc thương nhân.
""")

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG chu ky 13. tong so dong:", len(lines))