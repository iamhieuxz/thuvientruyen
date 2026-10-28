# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
BAK = "_bak_glossary_cycl8.txt"
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


# ── 1. GIA TỘC DIỆP ───────────────────────────────────────────────
add_entries("## ══════ GIA TỘC KHƯƠNG", [
    ("叶逸空", 'Diệp Dật Không (二房长子/trưởng tử nhị phòng nhà họ Diệp, từ nhỏ hay bắt nạt Diệp Sở; là nhân vật THỨ BA, KHÔNG phải biến thể viết sai của Diệp Dật Phi hay Diệp Dật Thần — ch.86–90)'),
])

# ── 2. NHÂN VẬT PHỤ ──────────────────────────────────────────────
add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("王三通", 'Vương Tam Thông (chủ trang viên hồ Quảng Lăng, hiệu Lâu Vương Giang Nam, biệt danh võ đạo Sở Bá Vương; hai lần được Diệp Sở cứu, tặng trang viên; người chi nhánh Giang Đô của Đông Hải Vương gia — ch.81–83, 93, 95)'),
    ("楚霸王", 'Sở Bá Vương (biệt hiệu võ đạo của Vương Tam Thông, có được nhờ "đánh khắp Ngục Long Đàm vô địch thủ", ch.81)'),
    ("叶神医", 'Diệp thần y (cách Vương Tam Thông, Lão Khang và giới y học Giang Đô gọi Diệp Sở từ ch.81 — VIẾT THƯỜNG chữ "thần y" trừ khi đứng đầu câu)'),
    ("钟珊", 'Chung San (quản gia trang viên hồ Quảng Lăng, phụ nữ trung niên; gọi Diệp Sở là "gia chủ" từ khi trang viên đổi chủ, ch.83)'),
    ("康老", 'Lão Khang (bảo tiêu thân tín của Vương Tam Thông; nhận lệnh thẩm vấn hai kẻ Ám Bảng ch.81, xuống đón Diệp Sở ở bệnh viện Giang Nam ch.95 — bản dịch đã chốt "Lão Khang", KHÔNG viết "Khang lão")'),
    ("吴少兵", 'Ngô Thiếu Binh (đại thiếu gia nhà họ Ngô, chủ cửa hàng cổ vật ở chợ chim hoa cổ vật, bị Lý Đầu Trọc đánh tả tơi; em trai Ngô Thiến Thiến, người yêu của Chu Khả Nhi — ch.86–88)'),
    ("吴倩倩", 'Ngô Thiến Thiến (chị của Ngô Thiếu Binh, đang qua lại với con trai Chu Bẩm Thiên; bản dịch đã chốt "Ngô Thiến Thiến", KHÔNG viết "Ngô Thi Thi" — ch.87–88)'),
    ("朱可儿", 'Chu Khả Nhi (bạn học cũ của Tôn Ngữ Nhu, người giới thiệu mẹ con Tôn vào cửa hàng cổ vật để gài bẫy ép bồi tiền, ch.86–88)'),
    ("周子义", 'Chu Tử Nghĩa (con trai Chu Bẩm Thiên, theo cha tới chợ chim hoa cổ vật, quen Ngô Thiến Thiến nhưng không dám nhận, ch.87–88)'),
    ("洛千绝", 'Lạc Thiên Tuyệt (cường giả đứng hạng dưới hai mươi của Ám Bảng, hung danh lẫy lừng; đại phòng nhà họ Khương thuê giết Diệp Sở; đơn thân đánh lên Vương gia, giết hai thành viên Hộ Long Vệ và làm trọng thương Mã Tứ Thủy rồi đào tẩu — ch.91, 93, 95)'),
    ("马泗水", 'Mã Tứ Thủy (tông sư Hộ Long Vệ, trung niên tóc cắt ngắn, được phía trên điều tới vây bắt Lạc Thiên Tuyệt, bị đối phương trọng thương phải cấp cứu; Chu Bẩm Thiên gọi "Mã tông sư" — ch.93, 95)'),
    ("金鹏", 'Kim Bằng (thành viên Hộ Long Vệ mang hiệu Huyền tự, vừa ba mươi tuổi, dựa vào nhà họ Kim ở Kim Lăng; hộ tống Hoàng Phủ Thi Nguyệt, cảnh cáo Diệp Sở phải tránh xa — ch.92–93)'),
    ("王贺年", 'Vương Hạ Niên (lão gia, gia chủ nhà họ Vương ở Giang Đô, cha Vương Tử Đằng; mở tiệc đãi Vương Tam Thông, xưng "tộc lão", ch.93)'),
    ("黄卫明", 'Hoàng Vệ Minh (viện trưởng bệnh viện Giang Nam, trung niên đầu trọc, nể Vương tổng, mời bác sĩ Smith đang nghỉ phép tới xem thương thế, ch.95)'),
    ("谢山", 'Tạ Sơn (đội trưởng bảo tiêu đi theo Tạ Vũ San, bị Diệp Sở bắt gọn đạn, ch.90)'),
    ("史密斯", 'Smith (bác sĩ ngoại khoa người nước ngoài đang nghỉ phép, được Hoàng Vệ Minh mời tới bệnh viện Giang Nam; GIỮ NGUYÊN "Smith", không phiên âm — ch.95)'),
])

# ── 3. THẾ LỰC - TỔ CHỨC ─────────────────────────────────────────
add_entries("## ══════ ĐỊA DANH", [
    ("护龙卫", 'Hộ Long Vệ (tổ chức vệ long trực thuộc phía trên, chia thành viên theo "tự hiệu": Huyền tự...; một ký danh đệ tử của Dược Hoàng từng làm thống lĩnh Hộ Long Vệ — ch.92–93, 95)'),
    ("暗榜", 'Ám Bảng (bảng xếp hạng cường giả ngầm ngoài chính đạo; người trong Ám Bảng không nể thế gia như Vương gia; hai kẻ tập kích Vương Tam Thông và Lạc Thiên Tuyệt đều ở bảng này — ch.78–95)'),
    ("三大古族", 'ba đại cổ tộc (ba gia tộc cổ ở Giang Đô, trong đó chỉ nhà họ Vương có tông sư ngồi ghế; KHÔNG gộp với "bốn đại hào tộc" — ch.91)'),
    ("四大豪族", 'bốn đại hào tộc (bốn thế gia giàu mạnh ở Giang Đô, nhà họ Ngô là một — KHÁC với "ba đại cổ tộc", dịch đúng từng chỗ theo source, ch.86)'),
    ("吴家", 'nhà họ Ngô (thế gia ở Giang Đô, có đại thiếu gia Ngô Thiếu Binh và Ngô Thiến Thiến, ch.86–88)'),
    ("金陵金家", 'nhà họ Kim ở Kim Lăng (gia tộc đứng sau Kim Bằng của Hộ Long Vệ, ch.92)'),
    ("东海王家", 'Đông Hải Vương gia (gia tộc gốc; nhà họ Vương ở Giang Đô chỉ là một phân chi mấy chục năm trước, ch.81, 93)'),
])

# ── 4. ĐỊA DANH ─────────────────────────────────────────────────
add_entries("## ══════ VŨ ĐẠO - CẢNH GIỚI - THỂ CHẤT", [
    ("广陵湖", 'hồ Quảng Lăng (giữa hồ có đảo rộng, thời cổ từng thuộc phủ Quảng Lăng Vương; VIẾT "hồ Quảng Lăng", không viết "Quảng Lăng Hồ")'),
    ("广陵湖庄园", 'trang viên hồ Quảng Lăng (trang viên sang trọng nhất Giang Do, vài vạn m2, có non bộ, suối, trường đua ngựa, trường đua xe, sân golf; Vương Tam Thông tặng Diệp Sở — ch.82–83)'),
    ("广陵王", 'Quảng Lăng Vương (tước hiệu thời cổ; tương truyền mộ ông nằm quanh vùng hồ Quảng Lăng, lý do Vương Tam Thông mua cả khu, ch.82–83)'),
    ("花鸟古玩市场", 'chợ chim hoa cổ vật (chợ hoa, chim và đồ cổ ở Giang Đô; nơi Ngô Thiếu Binh mở cửa hàng và gài bẫy mẹ con Tôn Ngữ Nhu, ch.85–88)'),
    ("江南医院", 'bệnh viện Giang Nam (bệnh viện tư thuộc nhà họ Vương, ch.95 — KHÁC "hiệu kim hoàn Giang Nam", "ngân hàng Giang Nam", "Giang Nam Đại Hotel")'),
    ("帝都", 'đế đô (kinh đô Long Quốc, tầng cao hơn Giang Đô; Diệp Sở dặn "lên đế đô" cuối ch.95 — giữ "đế đô", không viết "thủ đô")'),
    ("东海", 'Đông Hải (vùng đất phía đông, nơi có Đông Hải Vương gia; Vương Tam Thông lên Giang Đô để khảo sát hậu bối phân chi này, ch.81, 93)'),
])

# ── 5. VŨ ĐẠO ───────────────────────────────────────────────────
add_entries("## ══════ Y HỌC - THUẬT NGỮ", [
    ("化劲大宗师", 'Hóa Kình đại tông sư (bước thứ ba của võ đạo: Đoán Thể, Khai Mạch rồi Hóa Kình; khí kình phóng ra ngoài, đánh người cách không — VIẾT "Hóa Kình", KHÔNG viết "Hóa Cận", ch.89)'),
    ("淬体", 'tối thể (dùng nước thuốc tôi luyện cơ thể người mới bước vào Đoán Thể — KHÁC với cảnh giới "Đoán Thể", ch.89, 91)'),
    ("龙鳞", 'vảy rồng (vảy mọc ngược sau gáy Tôn Ngữ Nhu khi Chân Vũ Linh Thể hiện hình, ch.89)'),
    ("金色鳞片", 'mảnh vảy vàng (cách source gọi đúng chỗ vảy sau gáy Tôn Ngữ Nhu, nhỏ như móng tay, lạnh buốt, phần lớn bị tóc che, ch.89)'),
])

# ── 6. Y HỌC ────────────────────────────────────────────────────
add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("药浴", 'tắm thuốc (ngâm dược liệu đã nấu để tối thể; bản dịch giữ "tắm thuốc", không viết "dược dục", ch.89)'),
    ("疗伤丹", 'Liệu Thương Đan (đan dược Diệp Sở ban cho Trần Tử Báo đầu ch.76, cầm máu kết vảy rất nhanh; VIẾT HOA)'),
    ("元阴", 'nguyên âm (chữ source cho lần âm dương giao hợp đầu của Diệp Sở với Tôn Ngữ Nhu, dùng nuôi Oán Long Khí làm tan bớt oán khí, ch.89)'),
    ("奇经八脉", 'kỳ kinh bát mạch (Khai Mạch tông sư là khai thông kỳ kinh bát mạch, ch.89)'),
])

# ── 7. ĐỊA VỊ - CHỨC VỤ ─────────────────────────────────────────
add_entries("## ══════ QUY TẮC XƯNG HÔ", [
    ("庄主", 'trang chủ (chủ trang viên — Khương Hải Vân mê mẩn "vị trang chủ thần bí" mà không biết chính là Diệp Sở, ch.83–84)'),
    ("家主", 'gia chủ (người đứng đầu gia tộc; Vương Hạ Niên là gia chủ nhà họ Vương, Chung San và người trang viên gọi Diệp Sở "gia chủ" — ch.79–93)'),
    ("族老", 'tộc lão (bậc trưởng lão quản gia vụ trong tộc; Vương Hạ Niên xưng "tộc lão" khi tiếp đãi người phía trên, ch.93)'),
    ("江南楼王", 'Lâu Vương Giang Nam (danh hiệu của Vương Tam Thông — VIẾT "Lâu Vương Giang Nam", không viết "Vua Lầu Giang Nam", ch.81–83)'),
    ("王总", 'Vương tổng (cách tài xế, Chung San, Lão Khang và Hoàng Vệ Minh gọi Vương Tam Thông, ch.81–95)'),
    ("姜叔", 'Khương thúc (Tiền Hâm gọi Khương Hải Vân ở Giang Nam Đại Hotel, ch.79)'),
    ("姜少", 'Khương thiếu (cách người ngoài gọi Khương Quân Hổ, ch.76, 78)'),
    ("周统领", 'Chu thống lĩnh (cách gọi Chu Bẩm Thiên, thống lĩnh thành vệ quân Giang Đô, ch.87–93)'),
    ("吴家大少", 'đại thiếu gia nhà họ Ngô (Ngô Thiếu Binh tự xưng, dựa vào cha vợ làm thống lĩnh thành vệ quân, ch.86–87)'),
])

# ── 8. QUY TẮC XƯNG HÔ: subsection mới ───────────────────────────
insert_prose("## ══════ THUẬT NGỮ CHUNG", """
### Vương Tam Thông & trang viên hồ Quảng Lăng (ch.81–83, 93, 95):
- Vương Tam Thông gọi Diệp Sở là "Diệp thần y", tự xưng "lão hủ", Diệp Sở gọi lại hắn là "lão Vương" (老王).
- Chung San và người trong trang viên gọi Diệp Sở là "gia chủ", gọi Vương Tam Thông là "Vương tổng".
- Lão Khang gọi chủ là "Vương tổng", gọi Diệp Sở là "Diệp thần y" (ch.95).
- Không dịch "江南楼王" thành "Vua Lầu Giang Nam"; "楚霸王" là "Sở Bá Vương".

### Nhà họ Ngô & chợ chim hoa cổ vật (ch.85–88):
- Ngô Thiếu Binh bị gọi "A Binh" (阿兵); Ngô Thiến Thiến là chị, em gọi "chị". Chu Khả Nhi gọi Ngô Thiếu Binh là "Ngô thiếu".
- Mẹ con Tôn Ngữ Nhu gọi Diệp Sở là "Anh Diệp" (叶大哥) — đã chốt, KHÔNG viết "đại ca".
- Đám côn đồ xưng "Quang Đầu ca" (光头哥) tức Lý Đầu Trọc; với Diệp Sở vẫn gọi "đại nhân".
- Chu Bẩm Thiên được gọi "Chu thống lĩnh"; hắn gọi Diệp Sở là "Diệp đại sư".

### Hộ Long Vệ, Ám Bảng & bệnh viện Giang Nam (ch.91–95):
- "护龙卫玄字号成员" → "thành viên Huyền tự của Hộ Long Vệ" (không viết "hạng Huyền").
- Người Ám Bảng tự xưng "bọn ta người của Ám Bảng"; giữ "Ám Bảng" viết hoa.
- Mã Tứ Thủy được gọi "Mã tông sư" (马宗师); hắn gọi lại Chu Bẩm Thiên là "Chu thống lĩnh".
- Hoàng Phủ Thi Nguyệt gọi Diệp Sở là "em trai"/"A Sở"/"thối đệ đệ" theo mức thân mật đã chốt (xem mục Hoàng Phủ Thi Nguyệt); Diệp Sở gọi "chị Thi Nguyệt".
- Hoàng Vệ Minh gọi Diệp Sở là "vị tiểu hữu này"/"Diệp thần y"; tên ngoại quốc giữ nguyên "Smith".
""")

# ── 9. LƯU Ý ĐẶC BIỆT: mục 25–30 ────────────────────────────────
insert_prose("## ══════ VĂN PHONG", """
25. BA người nhà họ Diệp dễ lẫn, đều là nhân vật THẬT: 叶逸辰 = Diệp Dật Thần (đại ca), 叶逸飞 = Diệp Dật Phi (nhị ca), 叶逸空 = Diệp Dật Không (trưởng tử nhị phòng, kẻ bị Diệp Sở tát tơi bời ở chợ chim hoa cổ vật ch.86–88 và dọa nạt ở ch.90). KHÔNG được "đồng nhất" Diệp Dật Không về Diệp Dật Thần — cả ba tên cùng xuất hiện ở ch.5, 24, 90–91 trong source.
26. 暗榜 (Ám Bảng) và 护龙卫 (Hộ Long Vệ) là HAI tổ chức khác nhau: Ám Bảng là bảng cường giả ngầm, Hộ Long Vệ là lực lượng chính đạo chia theo "tự hiệu". Kim Bằng thuộc Hộ Long Vệ, Lạc Thiên Tuyệt thuộc Ám Bảng. Không viết lẫn.
27. 三大古族 (ba đại cổ tộc) và 四大豪族 (bốn đại hào tộc) ở Giang Đô là hai cách gọi khác nhau của source (ch.91 và ch.86) cho hai lớp thế lực — dịch đúng từng chỗ, không tự quy về một danh sách.
28. 淬体 (tối thể — ngâm thuốc tôi luyện) KHÁC 锻体 (Đoán Thể — cảnh giới võ đạo, VIẾT HOA). Đã chốt: 化劲大宗师 = "Hóa Kình đại tông sư" (không phải "Hóa Cận"), 药浴 = "tắm thuốc".
29. Source ch.79 gõ 钱森豪 một chỗ, thực chất là 钱豪森 = Tiền Hào Sâm (bố Tiền Hâm) — bản dịch giữ "Tiền Hào Sâm", không bày ra nhân vật thứ ba.
30. Cách gọi đã chốt ở ch.76–95, KHÔNG viết lại: "Diệp thần y", "Lâu Vương Giang Nam", "Sở Bá Vương", "trang viên hồ Quảng Lăng" (không viết "biệt thự Quảng Lăng Hồ"), "gia chủ"/"trang chủ"/"tộc lão", "Chu thống lĩnh", "Ngô Thiến Thiến", "Lão Khang" (không viết "Khang lão"), "Huyền tự", "đế đô", "bệnh viện Giang Nam", "Thiên Thanh Nhữ Diêu", "bốn đại hào tộc", "Smith".
""")

# ── 10. NGỮ CẢNH: header 10 -> 20 chương ─────────────────────────
for i, l in enumerate(lines):
    if l.startswith("## ══════ NGỮ CẢNH"):
        lines[i] = l.replace("cập nhật mỗi 10 chương", "cập nhật mỗi 20 chương")
        print("  header NGỮ CẢNH:", lines[i][:90])
        break

insert_prose("### Ràng buộc cho các chương sau:", """
### Đã xảy ra — chương 76–95:
- Ch.76: Diệp Sở đưa một viên Liệu Thương Đan cho Trần Tử Báo rồi sai hắn "hầu hạ" Khương Quân Hổ ở Vương Triều Dạ; Khương Quân Hổ bị chuốc thuốc, qua đêm với mấy gã đồng tính, suýt chết vì "tinh tận nhân vong", sáng ra tin lan khắp mạng, đại phòng chỉ nghi mà không có bằng chứng.
- Ch.77: Trần Mỹ Tĩnh xông tới định liều mạng; Hàn Mộng Quan đứng che con rể; Khương Quân Long giả vờ nhận lỗi thay em, quỳ xin ông nội Khương Phong Niên làm chủ; Khương Hải Phong quát đòi bằng chứng, Diệp Sở bật lại "đưa ra rồi hãy nói".
- Ch.78: Khương Quân Hổ gọi cho Trần Tử Báo xin đoạn camera ở Vương Triều Dạ, bị chơi ngược, biết ngay mình bị gài; Khương Phong Niên dập đám cãi nhau, tuyên bố sẽ dắt Khương Quân Dao đi dự tiệc xã giao để kén tuấn kiệt trẻ tuổi — đại phòng mừng thầm, Hàn Mộng Quan sa sầm mặt.
- Ch.79: Hàn Mộng Quan khẳng định "chừng nào mẹ còn, không ly hôn nổi"; Khương Hải Vân tới Giang Nam Đại Hotel gặp Tiền Hâm và Tiền Hào Sâm, bị dụ góp vốn dự án lớn ở Đông Thành khu; Diệp Sở cảnh cáo "việc này có chỗ quái dị" thì bị mắng "đồ phế vật chưa tốt nghiệp THCS".
- Ch.80: Diệp Sở tuyên bố mình quen chủ tịch thương hội Giang Nam và đại tiểu thư Hoàng Phủ, rằng vụ hợp tác của Khương Quân Dao là do hắn ngầm giúp; cả nhà không tin, Khương Quân Dao quát "đủ rồi, đừng làm mất mặt"; tối đó hai người nói riêng, nàng hứa tạm gác chuyện ly hôn để báo lại ông nội.
- Ch.81: Diệp Sở trèo cửa sổ đi dạo, gặp hai kẻ Ám Bảng tập kích xe Vương Tam Thông; ra tay cứu và nhận ra nhau vì Vương Tam Thông từng "được dạy dỗ" trong Ngục Long Đàm (biệt hiệu Sở Bá Vương). Đối phương khoe "Vương gia không dọa được người Ám Bảng"; Lão Khang nhận hai kẻ về thẩm vấn.
- Ch.82: Ở quán nướng, đám côn đồ tự xưng Bạch Lang Hội tới gây sự; Lý Đầu Trọc chạy tới, gọi Diệp Sở "đại nhân" và báo người đứng sau là nhà họ Khương (trả đũa vụ trước); Vương Tam Thông mời Diệp Sở ra đảo giữa hồ Quảng Lăng — khu đất từng là phủ Quảng Lăng Vương.
- Ch.83: Vương Tam Thông tặng trang viên hồ Quảng Lăng để tạ "lần thứ hai cứu mạng"; quản gia Chung San ra mắt, gọi Diệp Sở là "gia chủ"; nhà họ Long từng mua không nổi khu này; sáng hôm sau Hàn Mộng Quan báo đại phòng bị kẻ lạ đột nhập đánh một trận (chính là Lý Đầu Trọc).
- Ch.84: Khương Hải Vân hết lời khen "vị trang chủ thần bí" mà không biết là Diệp Sở; Khương Quân Dao bảo vụ đầu tư Đông Thành "không đáng tin"; Diệp Thiên Thành và Diệp Dật Thần tới đòi lại tiền rồi bàn nhau luồn qua đại phòng nhà họ Khương; Hàn Mộng Quan tới bệnh viện "hỏi thăm" đại phòng đang nằm viện, bọn tóc vàng trông thấy Diệp Sở hét lên.
- Ch.85: Trần Mỹ Tĩnh tố Diệp Sở sai đường chủ Bạch Lang Hội trả thù, Hàn Mộng Quan phản bác rằng gã tóc vàng là người của đại phòng; Khương Quân Hổ tức tới phun máu; Khương Quân Long tuyên bố sẽ liên hệ người Ám Bảng giết Diệp Sở. Cùng lúc ở chợ chim hoa cổ vật, hai vệ sĩ Bạch Hiểu Hiểu phái tới bảo vệ Tôn Ngữ Nhu (đều Đoán Thể ngũ đoạn) thảm bại; mẹ con nàng bị ép bồi chiếc bình "Thiên Thanh Nhữ Diêu đời Tống, giá một trăm triệu".
- Ch.86: Vệ sĩ khoe chủ là "đại thiếu gia nhà họ Ngô, một trong bốn đại hào tộc Giang Đô"; Chu Khả Nhi nhận là người giới thiệu để gài; Diệp Dật Không — trưởng tử nhị phòng nhà họ Diệp — tới chế giễu Diệp Sở "nuôi gái nhỏ"; Ngô Thiếu Binh và Lý Đầu Trọc đụng độ.
- Ch.87: Lý Đầu Trọc đánh Ngô Thiếu Binh thành "đầu lợn", một chiêu trọng thương tên hầu cận; Ngô Thiến Thiến gọi điện cầu cứu; Chu Bẩm Thiên cùng con trai Chu Tử Nghĩa tới chợ; Diệp Dật Không quay sang dọa, Diệp Sở ra tay tát tới tấp.
- Ch.88: Chu Bẩm Thiên cung kính mời "Diệp đại sư" ăn cơm, lệnh cho thành vệ quân bắt hết đám để thẩm vấn nghiêm; Ngô Thiến Thiến nhìn Chu Tử Nghĩa cầu cứu nhưng hắn không dám lên tiếng; Tôn Tú Anh chủ động rời đi, muốn thành toàn cho con gái; đêm đó Diệp Sở và Tôn Ngữ Nhu hôn nhau.
- Ch.89: Diệp Sở và Tôn Ngữ Nhu thành thân; nguyên âm của nàng nuôi dưỡng Oán Long Khí làm oán khí tan bớt; sau gáy nàng hiện "mảnh vảy vàng mọc ngược" (vảy rồng) — dấu hiệu Chân Vũ Linh Thể; Diệp Sở truyền công pháp, nàng đạt Đoán Thể nhất đoạn, hắn hứa mua dược liệu về nấu nước tắm thuốc để tối thể. Cùng lúc Diệp Thiên Thành mời Phùng Hán Tam tới trị Diệp Sở.
- Ch.90: Diệp Sở về nhà họ Diệp; Phùng Hán Tam từng bị hắn đánh bại nhưng không nhận ra nhau; một chiêu Ưng Trảo Công đánh Phùng Hán Tam bay ra; Tạ Vũ San hô Tạ Sơn bắn, Diệp Sở bắt trọn đạn bằng tay không rồi tát Diệp Dật Phi miệng mũi đổ máu.
- Ch.91: Diệp Sở ép Diệp Thiên Thành khai sạch; lão hối hận vì đã đẩy đi một vị tông sư trẻ (nhà họ Diệp chưa từng có tông sư; trong ba đại cổ tộc chỉ nhà họ Vương có). Đại phòng nhà họ Khương thuê Lạc Thiên Tuyệt; Hoàng Phủ Thi Nguyệt gọi Diệp Sở tới nhờ "giúp đỡ".
- Ch.92: Hoàng Phủ Thi Nguyệt giới thiệu Diệp Sở là bạn trai trước mặt Kim Bằng (thành viên Huyền tự của Hộ Long Vệ, ba mươi tuổi, dựa vào nhà họ Kim ở Kim Lăng); Kim Bằng đe dọa và khoe cảnh giới; Diệp Sở nhớ ra một trong mấy ký danh đệ tử của sư phụ từng làm thống lĩnh Hộ Long Vệ — tức hắn là sư đệ của thống lĩnh.
- Ch.93: Chia tay trước Giang Hoài Các; Kim Bằng đi trình diện phía trên; Mã Tứ Thủy từ chối để thành vệ quân nhúng tay, Chu Bẩm Thiên không vui nhưng ngoài mặt không than; nhà họ Vương mở tiệc đãi Vương Tam Thông vì Vương Tử Đằng vừa về nước — Vương Hạ Niên nhờ tộc lão, rồi quản gia báo "người phía trên tới".
- Ch.94: Hoàng Phủ Thi Nguyệt bắt Diệp Sở đi mua sắm cùng, hắn nhét cả đống túi vào Long Hư Không Đỉnh; hai người cá cược chuyện chiếc xe, nàng thua và chủ động hôn hắn, suýt lộ chuyện hắn đã sửa xe.
- Ch.95: Đông Mai báo Lạc Thiên Tuyệt đánh lên Vương gia, đại chiến với Hộ Long Vệ ngay trong Vương gia, giết hai thành viên và làm trọng thương Mã Tứ Thủy rồi đào tẩu; thành vệ quân phát lệnh truy nã toàn thành. Vương Tam Thông trọng thương nằm ở bệnh viện Giang Nam, nhờ Diệp Sở tới cứu; viện trưởng Hoàng Vệ Minh dẫn bác sĩ Smith đang nghỉ phép vào và công khai chê đông y.
""")

# ── 11. Rebind Ràng buộc ───────────────────────────────────────
i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Ám Bảng đang nhắm vào Diệp Sở: đại phòng nhà họ Khương (Khương Quân Long, Khương Hải Phong, Trần Mỹ Tĩnh) đã thuê Lạc Thiên Tuyệt — cường giả hạng dưới hai mươi của Ám Bảng — giết hắn, và hắn CHƯA BIẾT mình là mục tiêu. Lạc Thiên Tuyệt vừa đánh lên Vương gia, giết hai thành viên Hộ Long Vệ, làm trọng thương Mã Tứ Thủy, đang bị thành vệ quân truy nã toàn Giang Đô (ch.91, 93, 95).
- Mối dây với phía trên chưa cắt: Diệp Sở là sư đệ của thống lĩnh Hộ Long Vệ (một trong ký danh đệ tử của Dược Hoàng) — chưa ai biết; Kim Bằng (Huyền tự) đã cảnh cáo hắn phải tránh xa Hoàng Phủ Thi Nguyệt và đang báo công với Hộ Long Vệ. Mã Tứ Thủy nằm phòng cấp cứu, Hộ Long Vệ thương vong — xung đột Hộ Long Vệ / Ám Bảng sẽ lan tới Diệp Sở (ch.92–95).
- Vương Tam Thông mang nợ hai lần cứu mạng, đã sang tên trang viên hồ Quảng Lăng cho Diệp Sở (Chung San gọi "gia chủ"), coi hắn là "Diệp thần y"; nhà họ Vương Giang Đô chỉ là phân chi của Đông Hải Vương gia, bệnh viện Giang Nam thuộc Vương gia. Thương thế của Vương Tam Thông ở đầu ch.95 chính do Lạc Thiên Tuyệt gây ra — Diệp Sở sẽ nối được mối liên hệ (ch.81–83, 95).
- Xung đột với nhà họ Khương vẫn mở: Khương Quân Dao tạm gác chuyện ly hôn (ch.80) nhưng bị ông nội Khương Phong Niên ép đi kén chồng trong giới danh lưu; Tiền Hâm và Tiền Hào Sâm vẫn dụ Khương Hải Vân góp vốn dự án Đông Thành khu; Hàn Mộng Quan tuyệt đối không cho ly hôn (ch.76–80, 84).
- Nhà họ Diệp đã bị bầm dập: Diệp Thiên Thành không ép được, hối hận vì đã đẩy đi một tông sư; Diệp Dật Phi, Diệp Dật Không bị đánh tơi bời; Tạ Vũ San và đội trưởng bảo tiêu Tạ Sơn (có sủng) bị dọa khiếp via. Họ đang tìm cách luồn qua đại phòng nhà họ Khương để trả thù (ch.84, 90–91).
- Tôn Ngữ Nhu đã là người của Diệp Sở: sau gáy hiện "mảnh vảy vàng" (Chân Vũ Linh Thể), đạt Đoán Thể nhất đoạn, Diệp Sở hứa mua dược liệu nấu nước tắm thuốc để tối thể; Tôn Tú Anh muốn thành toàn. Nhắc lại: 叶大哥 là "Anh Diệp", không viết "đại ca" (ch.88–89).
- Hoàng Phủ Thi Nguyệt: nhờ Diệp Sở đóng vai bạn trai để chặn Kim Bằng, đã thua cá cược và chủ động hôn hắn; nàng CHƯA nhận ra Long Hư Không Đỉnh chính là chiếc đỉnh đồng ở buổi đấu giá ngầm; Đông Mai là người dò tin Ám Bảng cho nàng (ch.91–95).
- Cliffhanger ch.95: trong phòng bệnh ở bệnh viện Giang Nam, viện trưởng Hoàng Vệ Minh dẫn bác sĩ Smith vào và công khai chê đông y, Diệp Sở vừa bị yêu cầu dừng tay; Lão Khang đứng ngoài, thành vệ quân cầm sủng canh tầng, Vương Tam Thông trọng thương. Mở đầu ch.96 phải tiếp tục đúng cảnh này.
- Không đổi cách gọi đã chốt (LƯU Ý ĐẶC BIỆT mục 25–30): Diệp Dật Không ≠ Diệp Dật Phi ≠ Diệp Dật Thần; Ám Bảng ≠ Hộ Long Vệ; "tối thể" (淬体) ≠ "Đoán Thể" (锻体); "Huyền tự", "Hóa Kình đại tông sư", "Lâu Vương Giang Nam", "trang viên hồ Quảng Lăng", "hồ Quảng Lăng", "đế đô", "Thiên Thanh Nhữ Diêu", "Ngô Thiến Thiến", "Lão Khang", "Smith".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc: da rebind (%d dong)" % len(NEW.strip().split("\n")))

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG. tong so dong:", len(lines))
