# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
BAK = "_bak_glossary_cycl9.txt"
shutil.copyfile(G, BAK)

lines = io.open(G, encoding="utf-8").read().split("\n")


def has_key(key):
    for l in lines:
        if "=" in l and not l.startswith("#") and not l.startswith(" "):
            if l.split("=")[0].strip() == key:
                return True
    return False


def add_entries(header, entries):
    """Chèn các mục từ (mỗi mục MỘT dòng) ngay trước header section kế tiếp."""
    new = []
    for zh, vi in entries:
        if has_key(zh):
            print("  da co, bo qua:", zh)
            continue
        new.append("%s = %s" % (zh, vi))
    if not new:
        return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]
            print("  + %d muc truoc %s" % (len(new), header[:28]))
            return
    print("  CANH: khong thay header", header)


def insert_prose(header_prefix, block):
    """Chèn khối văn (section ### / mục LƯU Ý) ngay trước header_prefix."""
    first = block.strip().split("\n")[0]
    if any(l.strip() == first for l in lines):
        print("  skip (da co):", first)
        return
    for i, l in enumerate(lines):
        if l.startswith(header_prefix):
            lines[i:i] = block.strip("\n").split("\n") + ["", ""]
            print("  + block truoc", header_prefix[:28])
            return
    print("  CANH: khong thay", header_prefix)


def replace_line(prefix, new):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            print("  SUA:", l[:60], "->", new[:60])
            lines[i] = new
            return
    print("  CANH: khong thay dong", prefix)


# ── 1. SỬA LỖI: 楚霸王 là biệt hiệu CỦA DIỆP SỞ, không phải Vương Tam Thông ──
replace_line("楚霸王 =",
             '楚霸王 = Sở Bá Vương (biệt hiệu võ đạo của DIỆP SỞ ở Ngục Long Đàm, có được nhờ "đánh khắp Ngục Long Đàm vô địch thủ" (ch.1, 81); từ ch.106 cả Giang Đô biết chủ trang viên hồ Quảng Lăng là "Sở Bá Vương" — KHÔNG phải biệt hiệu của Vương Tam Thông)')
replace_line("王三通 =",
             '王三通 = Vương Tam Thông (chủ trang viên hồ Quảng Lăng đã tặng lại Diệp Sở, hiệu Lâu Vương Giang Nam; hai lần được Diệp Sở cứu, dịch được một viên Liệu Thương Đan ở ch.96; người chi nhánh Giang Đô của Đông Hải Vương gia, ch.81–83, 93, 95–98, 103, 105)')

# ── 2. GIA TỘC DIỆP ───────────────────────────────────────────────
add_entries("## ══════ GIA TỘC KHƯƠNG", [
    ("叶郑坤", 'Diệp Trịnh Khôn (lão gia/người đứng đầu nhà họ Diệp, cha Diệp Thiên Thành và Diệp Thiên Trì, gọi con cả là "lão đại"; đầu ch.111 họp gia tộc truy chuyện Diệp Sở, ch.112 chủ trương "không dùng được thì ép ra giá trị", phái Diệp Đình Đình đi đánh bài tình cảm — ch.111–112)'),
    ("叶天驰", 'Diệp Thiên Trì (叶家老二/lão nhị nhà họ Diệp, em trai Diệp Thiên Thành, con trai Diệp Trịnh Khôn; trước mặt cha chế giễu anh cả ở ch.111–112 — nhân vật THẬT, KHÔNG phải biến thể viết sai của Diệp Thiên Thành)'),
    ("叶婷婷", 'Diệp Đình Đình (con riêng 私生女 của Diệp Trịnh Khôn sinh ở bên ngoài, 27–28 tuổi, vừa du học về; lớn hơn Diệp Sở, vì cùng thân phận "con riêng" nên từ nhỏ chăm sóc Diệp Sở — người nhà họ Diệp thân với Diệp Sở nhất, bị sai đi đánh bài tình cảm và đòi điều kiện làm gia chủ — ch.112, 118–119)'),
])

# ── 3. NHÂN VẬT PHỤ ──────────────────────────────────────────────
add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("蛮熊", 'Mãn Hùng (thành viên Hộ Long Vệ, trẻ tuổi nóng tính, gọi Mã Tứ Thủy là "đội trưởng", gọi Vương Tam Thông là "Vương tiên sinh"; định đập bệnh viện vì tưởng tìm bác sĩ vô dụng, sau đó ấn đầu Kim Bằng bắt quỳ xin Diệp Sở — VIẾT "Mãn Hùng", ch.96–98, 113)'),
    ("司徒朝", 'Tư Đồ Triều (đệ tử 高徒 của Y Thánh Kim Lăng, em trai Tư Đồ Tĩnh, đi cùng Kim Bằng tới bệnh viện chữa Mã Tứ Thủy; tự phụ, cãi lệnh rút ngân châm làm bệnh nhân nguy kịch — CHÚ Ý: source ch.97 có 6 chỗ tự gõ lẫn thành 司马朝/司马神医 cho CÙNG một nhân vật, bản dịch chốt "Tư Đồ Triều"/"Tư Đồ thần y", KHÔNG bày ra nhân vật thứ hai "Tư Mã Triều"; ch.97–98, 113)'),
    ("司徒静", 'Tư Đồ Tĩnh (chị Tư Đồ Triều, thân truyền đệ tử của Y Thánh Kim Lăng, da màu lúa mạch, đồng tử xanh lục nhạt; tới Giang Đô ch.113, liếc qua ngân châm đã nhận ra Diêm La Thập Bát Châm và tuyên bố không cần ra tay nữa; về nhà gọi điện nhờ tra thân phận Diệp Sở — ch.98, 113)'),
    ("徐美静", 'Từ Mỹ Tĩnh (bạn học của Hàn Mộng Quan, trưởng khoa Cục Y tế, phụ trách kỳ thi chứng chỉ hành nghề y; lúc đầu vênh váo đòi quốc thủ bảo lãnh, khi Lý Chính Nguyên và La Vân cùng đứng ra thì đổi thái độ — KHÁC HOÀN TOÀN với 陈美静 = Trần Mỹ Tĩnh dâu lớn nhà họ Khương, ch.113–115)'),
    ("熊明", 'Hùng Minh (một trong mấy vị phó cục trưởng Cục Y tế, bị Tần Đông Dương gọi điện gài đi bắt Diệp Sở tội quay cóp; bản dịch chốt gọi hắn "Cục phó Hùng" — không viết "Cục trưởng Hùng", ch.114–115)'),
    ("罗云", 'La Vân (cục trưởng Cục Y tế, bạn cũ của Lý Chính Nguyên, tự xưng "bỉ nhân La Vân", Lý Chính Nguyên gọi thân mật "lão La"; chính là người đứng ra bảo lãnh thủ tục thi cho Diệp Sở — ch.113, 115)'),
    ("王虎", 'Vương Hổ (hội chủ Hắc Hổ Hội, trụ ở Kim Lăng; được nhà họ Tư Mã ở Kim Lăng nâng lên ngũ phẩm tông sư, cùng Tả Tu Đao làm nội ứng phản Bạch Hiểu Hiểu, giết Hoa Hồng Máu; bị Diệp Sở một quyền xuyên ngực đánh chết ở ch.109 — Tư Mã Quyền gọi hắn là "chó của bản thiếu", ch.107–109)'),
    ("司马权", 'Tư Mã Quyền (đệ tam đại tử đệ 三代子弟 của nhà họ Tư Mã ở Kim Lăng, tự xưng "tại hạ Tư Mã Quyền"; chèo thuyền nhỏ tới trang viên hồ Quảng Lăng bái phỏng bị Chung San từ chối rồi bị Diệp Sở chém một đạo khí nhận; sau đó bị Diệp Sở bóp gãy cổ ở tổng bộ Bạch Lang Hội — ch.105–110)'),
    ("王正玄", 'Vương Chính Huyền (trưởng tử Vương Hạ Niên, được cha sai về bảo khố lấy Long Dương Thảo quỳ tặng Diệp Sở, tiếc vì cây đó để dành cho cha đột phá đại tông sư — ch.105)'),
    ("王子腾", 'Vương Tử Đằng (trưởng tôn nhà họ Vương Giang Đô, "thiếu niên tông sư" 26–27 tuổi từng du học; đòi cưới Khương Quân Dao, dọa giết Diệp Sở từ xa, hẹn vài ngày nữa tới cửa cầu hôn; bị Diệp Sở một ngón tay đánh trọng thương ở Giang Hoài Các, sau đó nhà họ Vương hủy hôn — ch.101–104, 111)'),
    ("林北鹤", 'Lâm Bắc Hạc (một trong hai phó thống lĩnh thành vệ quân Giang Đô; dẫn thành vệ cầm súng tới định bắt Diệp Sở tội câu kết nhà họ Tư Mã, bị Chu Bẩm Thiên bắt ngược tội thông đồng với thế lực đen — ch.110)'),
    ("蔷薇", 'Hoa Hồng Máu (血蔷薇, thành viên nữ của Bạch Lang Hội, bị Vương Hổ bóp cổ giết ở ch.107; Diệp Sở dặn Bạch Hiểu Hiểu hậu táng và bồi thường gia quyến — ch.107, 110)'),
    ("黄夫人", 'Hoàng phu nhân (người bệnh từng được Diệp Sở chữa khỏi; Lý Chính Nguyên lấy tên nàng để giới thiệu Diệp Sở với cục trưởng La Vân — ch.113)'),
    ("张医圣", 'Trương y thánh (cách source ch.97 gọi Y Thánh Kim Lăng — thầy của Tư Đồ Triều và Tư Đồ Tĩnh; chỉ viết "Trương y thánh" đúng chỗ source ghi 张医圣, còn lại dùng "Y Thánh Kim Lăng")'),
])

# ── 4. THẾ LỰC - TỔ CHỨC ─────────────────────────────────────────
add_entries("## ══════ ĐỊA DANH", [
    ("卫健局", 'Cục Y tế (cơ quan quản lý y tế Giang Đô, nơi tổ chức thi và cấp chứng chỉ hành nghề; cục trưởng La Vân, phó cục trưởng Hùng Minh, trưởng khoa Từ Mỹ Tĩnh — bản dịch ĐÃ CHỐT "Cục Y tế", KHÔNG viết "Sở Y tế" dù source ch.111 có chỗ ghi 卫健委, ch.113–115)'),
    ("金陵司马家", 'nhà họ Tư Mã ở Kim Lăng (source ch.105–110 ghi đủ 金陵司马家; đứng sau Tư Mã Quyền, giúp Vương Hổ lên ngũ phẩm tông sư; từng định mua trang viên hồ Quảng Lăng mà không nổi — xem LƯU Ý 32, giữ "nhà họ Tư Mã", chỉ thêm "ở Kim Lăng" khi source ghi 金陵)'),
    ("东海省", 'tỉnh Đông Hải (tỉnh chứa Giang Đô, có tông môn Chân Vũ Tông; Long gia ở Giang Đô vừa bắt được dây với Chân Vũ Tông — ch.110)'),
    ("真武宗", 'Chân Vũ Tông (tông môn võ đạo ở tỉnh Đông Hải, có mấy vị Hóa Kình đại tông sư; Long gia vừa bắt được dây với tông môn này, Vân Băng Uyển coi là mối đe dọa lớn hơn cả "cáo sơn" — ch.107, 110)'),
])

# ── 5. Y HỌC - THUẬT NGỮ ────────────────────────────────────────
add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("化煞丹", 'Hóa Sát Đan (Diệp Sở luyện cho Vân Băng Uyển để hóa sát khí trong Cửu Âm Sát Thể, tam phẩm có đan văn, một viên đủ hiệu lực ba tháng, sáu viên dùng một năm — ch.105–107; KHÁC HẲN 祛煞丹 = Khu Sát Đan ở ch.58, KHÔNG được dịch 化煞丹 thành "Khu Sát Đan")'),
    ("龙阳草", 'Long Dương Thảo (dược liệu hỏa thuộc tính trong bảo khố nhà họ Vương, tăng khí huyết cải thiện thể chất, hợp nhất với người âm thuộc tính thể chất như Cửu Âm Sát Thể; Vương Hạ Niên để dành xung khai Nhâm Đốc nhị mạch nhưng đành đem tặng Diệp Sở — ch.105)'),
    ("任督二脉", 'Nhâm Đốc nhị mạch (hai mạch cuối phải xung khai mới đột phá được đại tông sư; Vương Hạ Niên khí huyết suy bại nên mãi không mở nổi — ch.105)'),
    ("阎罗十八针", 'Diêm La Thập Bát Châm (châm pháp truyền thuyết của đông y, sắp kim theo một thứ tự riêng, tương truyền người đã nửa bước vào điện Diêm La cũng kéo lại được; Tư Đồ Tĩnh nhận ra trên người Mã Tứ Thủy, Diệp Sở dùng suốt 30 phút cứu mạng — VIẾT ĐẦY ĐỦ "Diêm La Thập Bát Châm", không cắt thành "La Thập Bát Châm", ch.96, 113)'),
    ("分经错骨", 'phân kinh thác cốt (thủ pháp đông y thượng thừa: làm toàn bộ khớp xương đối phương trật ra, đau tới mức tưởng chết, cần lâm sàng phong phú — Diệp Sở dùng ngay tại phòng thi để trị Tần Đông Dương, ch.115)'),
    ("接骨复位", 'nối xương hồi vị (thủ pháp ghép lại khung xương đã trật, thương nặng tới đâu cũng nối được; Diệp Sở biểu diễn ngay sau phân kinh thác cốt rồi mỉa mai cả phòng thi, ch.115)'),
])

# ── 6. THUẬT NGỮ CHUNG ──────────────────────────────────────────
add_entries("## ══════ CẤM TỪ (TUYỆT ĐỐI KHÔNG XUẤT HIỆN TRONG BẢN DỊCH)", [
    ("行医资格证", 'chứng chỉ hành nghề y (kỳ thi lấy chứng chỉ đông y hoặc tây y của Cục Y tế, phải có "quốc thủ" đứng ra bảo lãnh mới được thi; Diệp Sở chọn đông y — giữ "chứng chỉ hành nghề y", không viết "giấy phép hành nghề", ch.111, 113–115)'),
    ("卧龙凤雏", 'Ngọa Long Phượng Sồ (thành ngữ chỉ hai nhân vật kiệt xuất; Diệp Sở dùng theo nghĩa mỉa mai giới y học Giang Đô trong phòng thi — giữ nguyên "Ngọa Long Phượng Sồ", không dịch thoát nghĩa, ch.115)'),
    ("化气成刃", 'hóa khí thành nhận (khí kình của Hóa Kình đại tông sư ngưng thành lưỡi dao phóng ra ngoài; dấu hiệu để cả Giang Đô nhận ra chủ trang viên là đại tông sư — ch.106)'),
    ("以气御针", 'dĩ khí ngự châm (dùng khí kình điều khiển ngân châm thay vì tay; Diệp Sở cứu Mã Tứ Thủy bằng cách này suốt 30 phút — ch.96)'),
])

# ── 7. QUY TẮC XƯNG HÔ: subsection mới ──────────────────────────
insert_prose("## ══════ THUẬT NGỮ CHUNG", """
### Nhà họ Diệp đời lão gia (ch.111–112):
- Diệp Trịnh Khôn được con cái gọi "bố", người nhà gọi "lão gia"; ông gọi Diệp Thiên Thành là "lão đại" (老大), Diệp Thiên Trì là "lão nhị" (老二).
- Diệp Thiên Trì gọi Diệp Thiên Thành là "đại ca"; Diệp Thiên Thành gọi ông già là "bố".
- Diệp Đình Đình: con riêng của Diệp Trịnh Khôn nhưng lớn hơn Diệp Sở và từ nhỏ đã chăm sóc hắn — giữ cách gọi thân mật "chị Đình Đình"/"Đình Đình", KHÔNG gọi "cô" dù vai vế là cô ruột.
- Diệp Dật Không gọi Diệp Sở là "phế vật"/"đồ tạp chủng" như cũ.

### Cục Y tế & kỳ thi chứng chỉ hành nghề (ch.113–115):
- Từ Mỹ Tĩnh được gọi "Trưởng khoa Từ" (徐主任); nàng gọi Diệp Sở là "cậu trai" (小伙子)/"Tiểu Diệp" (小叶); Diệp Sở gọi nàng "dì Từ" (徐阿姨).
- Hùng Minh được gọi "Cục phó Hùng" (熊局); La Vân là "cục trưởng", Lý Chính Nguyên gọi thân mật "lão La".
- Lý Chính Nguyên được gọi "Lý lão"/"Lý quốc thủ"; hắn giới thiệu Diệp Sở với người ngoài là "Diệp thần y".
- Tần Đông Dương là "Tần thiếu"/"đại thiếu gia nhà họ Tần"; hắn gọi Hùng Minh là "cậu" (舅舅).

### Trang viên hồ Quảng Lăng tiếp khách (ch.105–106):
- Chung San gọi Diệp Sở là "gia chủ", xưng với người ngoài là "trang chủ của chúng tôi"; nàng gọi Tư Mã Quyền là "Tư Mã công tử".
- Tư Mã Quyền tự xưng "tại hạ", gọi Diệp Sở là "các hạ"/"các vị"; tông sư áo dài gọi chủ là "thiếu gia", gọi Diệp Sở là "tiểu tử"/"thằng nhãi".
""")

# ── 8. LƯU Ý ĐẶC BIỆT: mục 32–38 ────────────────────────────────
insert_prose("## ══════ VĂN PHONG", """
32. 司徒 (Tư Đồ) và 司马 (Tư Mã) là HAI họ khác nhau, dịch "Tư Đồ" và "Tư Mã" tương ứng — không được đồng nhất. Source ch.97 tự gõ lẫn: cùng một nhân vật 司徒朝 nhưng có 6 chỗ viết 司马朝/司马神医; bản dịch giữ "Tư Đồ Triều"/"Tư Đồ thần y" cho suốt ch.97 vì câu giới thiệu đầu chương ghi họ 司徒. Nhà họ Tư Mã ở Kim Lăng (司马权, ch.105–110) là dòng riêng; source ch.8–10 cũng dùng 司马家 cho thế lực đứng sau Tư Mã Tài nên bản dịch vẫn giữ "nhà họ Tư Mã" cho cả hai, chỉ thêm "ở Kim Lăng" khi source ghi 金陵司马家.
33. 徐美静 = Từ Mỹ Tĩnh (bạn học Hàn Mộng Quan, trưởng khoa Cục Y tế, ch.113–115) KHÁC HẲN 陈美静 = Trần Mỹ Tĩnh (dâu lớn nhà họ Khương, từ ch.3). Hai tên chỉ lệch một chữ nhưng là hai người hoàn toàn khác — không được "đồng nhất" tên.
34. 楚霸王 = Sở Bá Vương là biệt hiệu của DIỆP SỞ ở Ngục Long Đàm (ch.1, 81), từ ch.106 cả Giang Đô gọi chủ trang viên hồ Quảng Lăng bằng danh hiệu này. TUYỆT ĐỐI không gán biệt hiệu này cho Vương Tam Thông.
35. 长衫老者 ở ch.105–109 là tông sư tóc bạc đi theo Tư Mã Quyền, source KHÔNG nêu tên — giữ "lão già áo dài"/"lão giả", không tự đặt tên. (Khác 长衫老者 ch.46–49 vốn là Cát đại sư trước khi lộ tên.)
36. Ba cha con nhà họ Diệp đã rõ: 叶郑坤 = Diệp Trịnh Khôn (lão gia), 叶天成 = Diệp Thiên Thành (lão đại), 叶天驰 = Diệp Thiên Trì (lão nhị). Diệp Thiên Trì là nhân vật THẬT ch.111–112, không phải biến thể của Diệp Thiên Thành. 叶婷婷 = Diệp Đình Đình là con riêng của Diệp Trịnh Khôn (叶郑坤在外的私生女), KHÔNG phải con riêng của Diệp Thiên Thành.
37. 化煞丹 = Hóa Sát Đan (Diệp Sở luyện cho Vân Băng Uyển, ch.105–107) KHÁC 祛煞丹 = Khu Sát Đan (đan sư phụ ban cho đệ tử, ch.58). Source chỉ dùng 化煞丹 ở ch.105–107; bản dịch ch.106–107 đã được sửa từ "Khu Sát Đan" về "Hóa Sát Đan".
38. Cách gọi đã chốt ở ch.96–115, KHÔNG viết lại: "Tư Đồ Triều"/"Tư Đồ Tĩnh"/"Tư Đồ thần y", "Y Thánh Kim Lăng"/"Trương y thánh", "Từ Mỹ Tĩnh"/"Trưởng khoa Từ"/"dì Từ", "Cục Y tế" (không "Sở Y tế"), "Cục phó Hùng" (không "Cục trưởng Hùng"), "La Vân"/"lão La", "Hùng Minh", "Diệp Trịnh Khôn", "Diệp Thiên Trì", "Diệp Đình Đình", "Mãn Hùng", "Tư Mã Quyền", "Vương Hổ", "Vương Chính Huyền", "Vương Tử Đằng" (không "Vương Tử Đằng" thành "Vương Tử Đào"), "Lâm Bắc Hạc", "Hoa Hồng Máu", "Chân Vũ Tông", "tỉnh Đông Hải", "Hóa Sát Đan", "Long Dương Thảo", "Nhâm Đốc nhị mạch", "Diêm La Thập Bát Châm", "phân kinh thác cốt", "nối xương hồi vị", "chứng chỉ hành nghề y", "Ngọa Long Phượng Sồ", "hóa khí thành nhận", "dĩ khí ngự châm".
""")

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG phan 1. tong so dong:", len(lines))