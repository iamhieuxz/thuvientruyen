# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl12.txt")
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


# ── NHÂN VẬT PHỤ (arc 136–165) ─────────────────────────────────
add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("皇甫明", 'Hoàng Phủ Minh (ông nội của Hoàng Phủ Thi Nguyệt, người đứng đầu nhà họ Hoàng Phủ ở Kim Lăng; ch.171–177 nghe cháu gái trình bày, giao lại quyền kiểm soát công trình Giang Đô — KHÁC HOÀN TOÀN với 黄卫明 = Hoàng Vệ Minh, viện trưởng bệnh viện Giang Nam)'),
    ("皇甫剑", 'Hoàng Phủ Kiếm (chú hai 二叔 của Hoàng Phủ Thi Nguyệt, cha Hoàng Phủ Kiệt, được gọi "nhị gia"; tham vọng đẩy con trai lên ghế thiếu gia tộc, ch.164–172 tiếp quản công ty của Thi Nguyệt — nhân vật THẬT, KHÔNG phải biến thể của Hoàng Phủ Kiệt)'),
    ("皇甫碧月", 'Hoàng Phủ Bích Nguyệt (chị gái Hoàng Phủ Kiệt, con gái Triệu Hoa Ngọc, đối thủ tranh quyền thừa kế với Hoàng Phủ Thi Nguyệt; bám được công tử nhà tỉnh trưởng nên cướp mất dự án của Thi Nguyệt — ch.165–172)'),
    ("赵华玉", 'Triệu Hoa Ngọc (nhị phu nhân nhà họ Hoàng Phủ, mẹ Hoàng Phủ Bích Nguyệt; luôn mỉa mai Hoàng Phủ Thi Nguyệt — ch.170–172)'),
    ("李淑英", 'Lý Thục Anh (mẹ của Hoàng Phủ Thi Nguyệt, dịu dàng thương con gái — ch.171–172)'),
    ("林豪", 'Lâm Hào (bạn học cũ của Khương Quân Dao, con nhà giàu tự phụ, ve vãn nàng và bị Diệp Sở bẽ mặt ngay ở nhà họ Khương — ch.172–175)'),
    ("红云", 'Hồng Vân (sư thái/nữ tu, tự xưng "bần ni", tính thẳng thắn; cảnh cáo Diệp Sở rằng Chân Vũ Tông sẽ không bỏ qua vụ giết Đông Hải Dược Vương — ch.179–191)'),
    ("东海药王", 'Đông Hải Dược Vương (Dược Vương vùng Đông Hải, người của Chân Vũ Tông, bị Diệp Sở giết ở ch.181 — KHÁC 药皇 = Dược Hoàng là sư phụ của Diệp Sở, tuyệt đối không lẫn)'),
    ("龙镇岳", 'Long Trấn Nhạc (lão nhị nhà họ Long — ch.180 được Long Cửu gia gọi "nhị ca"; tính ngang ngược, bị Diệp Sở bẻ gãy cổ tay — ch.179–191)'),
    ("龙镇南", 'Long Trấn Nam (tức 龙九爷/Long Cửu gia, "A Cửu", con thứ chín nhà họ Long đã đoạn tuyệt với gia tộc; mời Diệp Sở tới nhà họ Long chữa bệnh cho cha, sau đó lộ diện đối đầu Long Trấn Sơn — ch.178–191)'),
    ("萧木", 'Tiêu Mộc (thầy thuốc của nhà họ Long, tự phụ chê Diệp Sở, nhiều lần bị bẽ mặt — ch.180–189)'),
    ("赵武宣", 'Triệu Vũ Tuyên (vệ sĩ tông sư của Hoàng Phủ Kiệt; đánh bại Đông Mai sau hơn trăm hiệp, định phế khí hải của nàng thì bị Diệp Sở đấm lõm ngực, đá nát khí hải — ch.141–142)'),
    ("山叔", 'Sơn thúc (cao thủ của nhà họ Hoàng Phủ, được Hoàng Phủ Kiệt sai ra tay với Diệp Sở ở Giang Hoài Các — ch.165)'),
    ("林自美", 'Lâm Tự Mỹ (người nhà họ Lâm ở Kinh Khẩu, bị trúng Tam Thi độc trong vụ thảm sát, được Diệp Sở cứu — ch.163)'),
    ("林老", 'Lâm lão (cha của Lâm Tự Như và Lâm Tự Tại, bị gieo hạt Hoàng Tuyền Hoa vào não; Diệp Sở phải chém đứt bắp chân để cứu mạng — ch.155–159)'),
])

# ── THẾ LỰC / ĐỊA DANH ─────────────────────────────────────────
add_entries("## ══════ ĐỊA DANH", [
    ("南疆万蛇山", 'núi Vạn Xà ở Nam Cương (nơi An Tiểu Vũ nhắc tới: "năm năm trước ở núi Vạn Xà Nam Cương" — manh mối vụ thảm sát, ch.163)'),
    ("南城区", 'khu Nam Thành (khu có công trường nghi có cổ mộ — VIẾT "khu Nam Thành", ch.137–150)'),
])

# ── Y HỌC / ĐAN DƯỢC / ĐỘC ─────────────────────────────────────
add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("锻体丹", 'Đoán Thể Đan (đan Diệp Sở luyện hàng loạt để bán, ch.152 — VIẾT HOA)'),
    ("十全大补丸", 'Thập Toàn Đại Bổ Hoàn (bài thuốc bổ Diệp Sở giao cho Gia Cát Triết Nhã sản xuất — ch.153)'),
    ("百花露", 'Bách Hoa Lộ (sản phẩm nước hoa/dược mỹ phẩm giao cho Gia Cát Triết Nhã — ch.153)'),
    ("尸骨虫", 'Thi Cốt Trùng (một trong ba thành phần của Tam Thi độc — ch.161)'),
    ("幽冥草", 'U Minh Thảo (một trong ba thành phần của Tam Thi độc, An Tiểu Vũ mang theo — ch.161)'),
    ("同心蛊", 'Đồng Tâm Cổ (cổ trùng Tư Đồ Tĩnh/U Lan gieo vào tim Khương Quân Dao để uy hiếp Diệp Sở — ch.162)'),
    ("铜皮铁骨", 'đồng bì thiết cốt (công phu da thịt cứng như đồng sắt, chặn được dao đâm — ch.160)'),
    ("半步宗师", 'bán bộ tông sư (cảnh giới dưới tông sư một bậc; Mã Tứ Thủy đạt được sau khi uống đan — ch.123)'),
    ("半步大宗师", 'bán bộ đại tông sư (cảnh giới ngay dưới đại tông sư; Mã Tứ Thủy và hắc y nhân ch.160 ở mức này — VIẾT "bán bộ đại tông sư")'),
    ("高品宗师", 'cao phẩm tông sư (tông sư từ tứ phẩm trở lên — ch.125)'),
    ("宗师圆满", 'tông sư viên mãn (đỉnh của cảnh giới tông sư; thánh tử Chân Vũ Tông đạt mức này — ch.181)'),
    ("少家主", 'thiếu gia chủ (người được chọn kế vị gia chủ; Diệp Trịnh Khôn phong Diệp Đình Đình làm thiếu gia chủ, Tần Đông Dương giành lại chức này — ch.147–148)'),
])

# ── SỬA ENTRY CŨ (twist lớn) ───────────────────────────────────
replace_key("司徒静", '司徒静 = Tư Đồ Tĩnh (chị Tư Đồ Triều, bề ngoài là thân truyền đệ tử của Y Thánh Kim Lăng; da màu lúa mạch, đồng tử xanh lục nhạt; THÂN PHẬN THẬT lộ ở ch.161: chính là U Lan — thánh nữ Vu Cổ Giáo, thù Diệp Sở vì hắn là sư đệ của Tô Định Hạ — người từng dẫn Hộ Long Vệ diệt Vu Cổ Giáo; gieo Đồng Tâm Cổ vào tim Khương Quân Dao, giết Trịnh Hiên — ch.98, 113, 154–164)')
replace_key("幽兰", '幽兰 = U Lan (thánh nữ Vu Cổ Giáo, đeo mặt nạ quỷ, thân phận thật là Tư Đồ Tĩnh — "đệ tử Y Thánh Kim Lăng" chỉ là vỏ bọc; chủ mưu vụ Tam Thi độc và thảm sát nhà họ Lâm cùng An Tiểu Vũ, gieo Đồng Tâm Cổ vào Khương Quân Dao — ch.119–127, 154–164)')
replace_key("皇甫杰", '皇甫杰 = Hoàng Phủ Kiệt (thiếu gia nhà họ Hoàng Phủ, con trai Hoàng Phủ Kiếm, chị gái là Hoàng Phủ Bích Nguyệt; ngang ngược háo sắc, gọi Đông Mai là "nô tài nhà họ Hoàng Phủ", quấy rối nàng ch.142; âm mưu thâu tóm Vân Mộng Dược Nghiệp, thuê Sơn thúc ra tay với Diệp Sở — ch.137–165)')
replace_key("皇甫家", '皇甫家 = nhà họ Hoàng Phủ (đại gia tộc ở Kim Lăng, gia chủ là Hoàng Phủ Minh; đầu tư hàng trăm tỷ vào công trình Giang Đô, nội bộ tranh quyền giữa Hoàng Phủ Thi Nguyệt và phe Hoàng Phủ Kiếm — ch.11–172)')
replace_key("龙镇河", '龙镇河 = Long Trấn Hà (được source ch.134 ghi là "lão nhị nhà họ Long"; từ ch.180 trở đi người được gọi "nhị ca"/lão nhị lại là 龙镇岳 = Long Trấn Nhạc — xem LƯU Ý 44, KHÔNG tự gộp hai tên)')

# ── LƯU Ý 44–48 ────────────────────────────────────────────────
insert_prose("## ══════ VĂN PHONG", """
44. Nhà họ Long có nhiều nhân vật dễ lẫn: 龙镇山 = Long Trấn Sơn (gia chủ, lão đại), 龙镇河 = Long Trấn Hà (source ch.134 ghi lão nhị), 龙镇岳 = Long Trấn Nhạc (ch.180 được gọi "nhị ca"), 龙镇南 = Long Trấn Nam tức Long Cửu gia/阿九 (con thứ chín đã đoạn tuyệt gia tộc), 龙百岳 = Long Bách Nhạc (cha của Long Trấn Sơn), 龙鼎天 = Long Đỉnh Thiên (nguyên gia chủ), 龙九阳 = Long Cửu Dương (thiếu chủ). Source mâu thuẫn chuyện ai là "lão nhị" — giữ nguyên từng tên như source, không tự gộp và không đổi vai.
45. 皇甫剑 = Hoàng Phủ Kiếm là chú hai của Hoàng Phủ Thi Nguyệt và là CHA của Hoàng Phủ Kiệt; 皇甫明 = Hoàng Phủ Minh là ông nội nàng. Cả hai là nhân vật THẬT, KHÔNG phải biến thể viết sai của 皇甫杰 / 黄卫明 (check.py từng báo oan).
46. 真武门 và 真武宗 là HAI cách source gọi CÙNG một tông môn (ch.181, 183, 189, 191 dùng 门; ch.73, 107, 110, 170, 191 dùng 宗). Bản dịch thống nhất "Chân Vũ Tông" cho mọi chỗ.
47. TWIST LỚN: 司徒静 = Tư Đồ Tĩnh chính là 幽兰 = U Lan, thánh nữ Vu Cổ Giáo (lộ ở ch.161). Toàn bộ ch.98–160 tả nàng như đệ tử Y Thánh Kim Lăng chỉ là vỏ bọc. Nàng hận Diệp Sở vì hắn là sư đệ của 苏定夏 = Tô Định Hạ — người từng dẫn Hộ Long Vệ diệt Vu Cổ Giáo ở núi Vạn Xà Nam Cương. Không được tả hai tên như hai người.
48. 东海药王 (Đông Hải Dược Vương — người của Chân Vũ Tông, bị Diệp Sở giết ch.181) KHÁC HOÀN TOÀN 药皇 = Dược Hoàng (sư phụ của Diệp Sở). Tương tự 林老 = Lâm lão là cha của Lâm Tự Như/Lâm Tự Tại, không phải Lý lão.
""")

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG chu ky 12. tong so dong:", len(lines))