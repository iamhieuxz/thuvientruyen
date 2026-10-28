# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl17.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

def has_key(k):
    return any("=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == k for l in lines)

def add(header, entries):
    new = ["%s = %s" % (z, v) for z, v in entries if not has_key(z)]
    if not new:
        print("  (da co)", header[:18]); return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]; print("  +%d truoc %s" % (len(new), header[:22])); return

add("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("廖青山", 'Liêu Thanh Sơn (đường chủ Vũ Tôn của Giang Nam Hổ, kiêm hộ pháp; tới ép Hoàng Phủ Thi Nguyệt gả cho cháu Giang Nam Hổ, bị Diệp Sở đá bay rồi bẻ nát xương tay, sau bị giết ở ch.285)'),
    ("曹庆阳", 'Tào Khánh Dương (phó bang chủ Thanh Bang, luyện Thiết Sa Chưởng, bị Diệp Sở dùng Hình Ý Quyền đánh ngất — ch.273)'),
    ("蓝莲", 'Lam Liên (đệ tử Nga Mi tới nhà họ Khương, biết Thục Sơn Lệnh nằm trong tay "tiền phu quân" của Khương Quân Dao — ch.269)'),
    ("玄尘子", 'Huyền Trần Tử (đạo sĩ phái Long Hổ Sơn, dùng Ngũ Lôi Phù, bị Diệp Sở giết trong cơn bạo phát Oán Long Khí — ch.279–282)'),
    ("黑龙道人", 'Hắc Long đạo nhân (cựu Huyền Long đạo nhân, dùng Hắc Long Diễm, cùng Tà Tăng tìm long khí; bị Diệp Sở giết — ch.277–282)'),
    ("苗舵主", 'Miêu đà chủ (nữ đà chủ mặc áo trắng của Vu Cổ Giáo, bát phẩm Vũ Tôn, dùng tượng gỗ thế mạng; bị thiêu bằng Chu Tước Thần Hỏa — ch.280)'),
    ("蛇护法", 'Xà hộ pháp (hộ pháp Vu Cổ Giáo, bị Tư Đồ Tĩnh đánh ngất — ch.281)'),
])

add("## ══════ ĐỊA DANH", [
    ("形意门", 'Hình Ý Môn (môn phái võ học, trưởng lão nộp Hình Ý Quyền tâm pháp cho Diệp Sở — ch.257–258; KHÁC 形意拳 = Hình Ý Quyền là môn quyền pháp)'),
    ("白鹤门", 'Bạch Hạc Môn (môn phái võ học, nộp Bạch Hạc Quyền — ch.257–258)'),
    ("青帮", 'Thanh Bang (bang hội lớn ở Giang Nam, phó bang chủ là Tào Khánh Dương; hứa nhường nửa tỉnh Đông Hải — ch.257–273)'),
    ("长生制药", 'Trường Sinh Chế Dược (công ty dược Hoàng Phủ Thi Nguyệt lập riêng sau khi bị tước dự án — ch.266–269)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("千户", 'thiên hộ (chức vụ Hộ Long Vệ cao hơn bách hộ; Diệp Sở được thăng thiên hộ ở ch.272)'),
    ("千幻术", 'Thiên Huyễn Thuật (thuật dịch dung/biến hóa, Diệp Sở đổi lấy bằng đan dược — ch.271)'),
    ("凝神丹", 'Ngưng Thần Đan (đan ổn định tinh thần, Diệp Sở tặng Khương Quân Dao khi thấy nàng sắp sinh tâm ma — ch.274)'),
    ("魂丹", 'Hồn Đan (đan chữa tổn thương hồn phách, Diệp Sở luyện — ch.260)'),
    ("五蛊之毒", 'Ngũ Cổ chi độc (độc cổ do Vu Cổ Giáo phóng ra, bị Oán Long Khí nuốt sạch — ch.279)'),
    ("咒杀术", 'Chú Sát Thuật (thuật nguyền giết của Vu Cổ Giáo, khiến Diệp Sở tê liệt — ch.279)'),
    ("人蛊大阵", 'Nhân Cổ đại trận (đại trận Vu Cổ Giáo bày ở cứ điểm; ch.283 gọi lẫn thành 人巫大阵 = Nhân Vu đại trận — CÙNG một trận, bản dịch dùng "Nhân Cổ đại trận")'),
    ("蜀山令", 'Thục Sơn Lệnh (lệnh bài của phái Thục Sơn, hiện nằm trong tay "tiền phu quân" của Khương Quân Dao — ch.269)'),
    ("黄榜", 'Hoàng Bảng (bảng xếp hạng cao thủ do triều đình/phía trên lập, Chu Huyên nhắc tới — ch.283)'),
    ("武音", 'Vũ Âm (ứng dụng video ngắn, nơi Đỗ Linh Nhi đăng clip về Diệp Sở — ch.283)'),
    ("铁砂掌", 'Thiết Sa Chưởng (công phu luyện tay cứng như sắt của Tào Khánh Dương — ch.273)'),
])

BLOCK = """### Đã xảy ra — chương 256–285:
- Ch.256: Diệp Sở đốt đứt Tam Hồn Tỏa bằng Chu Tước Thần Hỏa nhưng lửa mất khống chế; Thôn Thôn ném Vạn Niên Băng Liên, hắn lên Vũ Tôn cửu phẩm.
- Ch.257: Hình Ý Môn, Bạch Hạc Môn và Thanh Bang tới nhà họ Vân đòi giao yêu xà; một gã Thanh Bang đánh lén Vân Băng Uyển, bị Diệp Sở đánh bay. Hắn học trộm Hình Ý Quyền khi đấu với trưởng lão Hình Ý Môn; Lâm Tự Tại nhận ra hắn là Diệp đại sư.
- Ch.258: Trưởng lão Hình Ý Môn nộp Hình Ý Quyền tâm pháp; Bạch Hạc Môn nộp Bạch Hạc Quyền. Gã Thanh Bang hứa nhường nửa tỉnh Đông Hải.
- Ch.259: Trần Mỹ Tĩnh đòi ghế tổng tài của Khương Quân Dao, nói với Hàn Mộng Quan rằng Diệp Sở là thiếu niên tông sư. Hắn đáp đã nghe hết lời khen.
- Ch.260: Diệp Sở nói Khương Quân Dao sẽ lên Nga Mi tu hành nên định trả công ty cho nhà họ Khương. Hắn luyện Hồn Đan, phát hiện Oán Long Khí đã nuốt trọn long khí.
- Ch.261: Hắn cho Khương Quân Dao uống đan, cô tỉnh; Chu Thanh Thanh nói hắn đã cứu cô và chính là Diệp đại sư. A Binh ở lại trang viên hồ Quảng Lăng.
- Ch.262: Hoàng Phủ Thi Nguyệt bị thương kinh mạch, nghi nhà họ Tư Mã đánh lén trong cổ mộ. Diệp Sở chữa khỏi, cô đột phá tông sư viên mãn.
- Ch.263: Long Trấn Sơn báo Giang Nam Hầu Vân Thiên Cừu rằng Long Đỉnh Thiên chết, mất long khí; nói Diệp Sở là con riêng nhà họ Diệp, có nhà họ Phong bảo lãnh. Một thanh niên bí ẩn xúi Vân Thiên Cừu mách Giang Nam Hổ rằng Diệp Sở là con rể nhà họ Khương và chủ tập đoàn Bách Dược.
- Ch.264: Đông Mai báo Hoàng Phủ Kiệt được thả. Ông nội nhà họ Hoàng Phủ giao dự án Giang Đô cho hắn; Giang Nam Hổ là trùm giới ngầm tỉnh Giang Nam.
- Ch.265: Hoàng Phủ Kiệt có Liêu Thanh Sơn — đường chủ Vũ Tôn của Giang Nam Hổ — tuyên bố cháu Giang Nam Hổ sẽ cưới Hoàng Phủ Thi Nguyệt. Diệp Sở đá Liêu Thanh Sơn bay máu rồi bẻ nát xương tay gã.
- Ch.266: Hoàng Phủ Minh giao Giang Đô cho Hoàng Phủ Kiệt, bắt Hoàng Phủ Thi Nguyệt về Kim Lăng kết hôn; cô lập Trường Sinh Chế Dược. Diệp Sở để lộ mình là Diệp đại sư; Tư Mã Giang xuất hiện đòi gặp Sở Bá Vương.
- Ch.267: Diệp Sở chối mình là Sở Bá Vương; Tư Mã Giang hỏi về Tư Mã Quyền, hắn đáp "bị ta giết rồi". Tư Mã Giang bị đánh gục rồi giẫm gãy ngực chết.
- Ch.268: Giang Nam Hổ lộ tên thật Trần Giang Nam. Hắn biết bị Giang Nam Hầu lợi dụng, sai lão tam tới Giang Đô và bảo Hoàng Phủ Kiệt phá tập đoàn Bách Dược.
- Ch.269: Lam Liên của Nga Mi tới nhà họ Khương, biết Thục Sơn Lệnh nằm trong tay tiền phu quân của Khương Quân Dao. Diệp Sở chọn nhà họ Vương làm bình phong cho Trường Sinh Chế Dược.
- Ch.270: Diệp Sở tặng Vương Hạ Niên Đại Chân Nguyên Đan. Lâm Hào dẫn Triệu Ngũ và sư phụ Tào Ưng — môn chủ Ưng Trảo Môn ở Cô Tô — tới; Tào Ưng bị hạ bằng một ngón tay, cầu xin tha.
- Ch.271: Diệp Sở lộ giọng Diệp đại sư; Tào Ưng quy phục. Hắn lấy Ưng Trảo Công, tung danh Sở Bá Vương, đổi đan lấy Thiên Huyễn Thuật.
- Ch.272: Chu Huyên cần Diên Thọ Hoàn cho bà ngoại. Lâm Tự Tại tiết lộ đan là của Diệp Sở; Chu Huyên cho biết hắn đã được thăng thiên hộ, nhiều thế lực kéo tới trang viên hồ Quảng Lăng.
- Ch.273: Diệp Sở hóa trang đại hán, một chiêu Ưng Trảo Công bóp nát xương tay gã Thanh Bang. Phó bang chủ Tào Khánh Dương dùng Thiết Sa Chưởng bị hắn dùng Hình Ý Quyền đánh ngất.
- Ch.274: Khương Hải Vân nịnh Sở Bá Vương; Diệp Sở từ chối, gọi Hàn Mộng Quan là bá mẫu. Hắn thấy Khương Quân Dao sắp sinh tâm ma, tặng Ngưng Thần Đan.
- Ch.275: Chu Huyên đòi Diên Thọ Hoàn. Thôn Thôn đọc ngọc giản giúp hắn nhận ra Đại Vu Thiên Kinh; Gia Cát Triết Nhã tới, hắn đòi cô đổi thân xác lấy dự án.
- Ch.276: Gia Cát Triết Nhã đồng ý làm người phụ nữ của Diệp Sở, bắt hắn thề rồi quan hệ. Sau đó cô mượn Đại Vu Thiên Kinh cho bạn nghiên cứu chữ Nam Cương; hắn nghi cô bị Tư Đồ Tĩnh nhập bằng Vu Khôi Thuật.
- Ch.277: Diệp Sở giữ Gia Cát Triết Nhã. Tà Tăng và Hắc Long đạo nhân dùng la bàn tìm long khí; hắn bám theo tới cứ điểm Vu Cổ Giáo, nơi Tư Đồ Tĩnh giao Đại Vu Thiên Kinh.
- Ch.278: Diệp Sở nhận ra đối thủ toàn Vũ Tôn. Bạch Hạc chân nhân hỏi vì sao diệt Chân Vũ Tông, hắn đáp "đáng giết" nên Võ Đang rút; Tà Tăng bị Ưng Trảo Công xuyên ngực.
- Ch.279: Hắn né đòn; Vu Cổ Giáo phóng Ngũ Cổ chi độc, hắn nuốt sạch. Hắc Long đạo nhân tung Hắc Long Diễm, Huyền Trần Tử dùng Ngũ Lôi Phù; Vu Cổ Giáo dùng Chú Sát Thuật khiến hắn tê liệt.
- Ch.280: Miêu đà chủ — bát phẩm Vũ Tôn — xé tay hình nhân. Hắn phát hiện tượng gỗ cháy phần nào thì cơ thể tương ứng thoát phong tỏa, bèn giẫm nát tay và thiêu bà bằng Chu Tước Thần Hỏa; áo đen lập Nhân Cổ đại trận.
- Ch.281: Cổ trùng hồi sinh liên tục, Oán Long Khí nuốt độc giúp hắn; hắn giả yếu, làm trọng thương Xà hộ pháp. Tư Đồ Tĩnh bất ngờ đánh ngất bà ta; hắn hỏi cảm giác bị tính kế thế nào rồi cho tượng gỗ bay vào cổ áo đen.
- Ch.282: Tượng gỗ cắm vào cổ áo đen rồi tự cháy, thiêu thành tro — đà chủ thứ hai của Vu Cổ Giáo chết; Tư Đồ Tĩnh hiểu mình trúng Vu Khôi Thuật. Oán Long Khí bạo phát: Diệp Sở giết Hắc Long đạo nhân, Tà Tăng, Huyền Trần Tử và đệ tử Long Hổ Sơn.
- Ch.283: Một thanh niên bí ẩn cứu Diệp Sở; Bạch Hạc chân nhân đoán thực lực hắn vượt Vũ Tôn. Đỗ Linh Nhi đăng video lên ứng dụng Vũ Âm; Chu Huyên bàn về Hoàng Bảng, trận pháp được gọi là Nhân Cổ đại trận.
- Ch.284: Hoàng Phủ Thi Nguyệt đưa Diệp Sở hôn mê về biệt thự của Vân Băng Uyển. Hoàng Phủ Kiệt dẫn Liêu Thanh Sơn và phó bang chủ Thanh Bang mặt đen tới; cô trọng thương vẫn ôm chân gã.
- Ch.285: Diệp Sở tỉnh, bẻ gãy cổ tay rồi đá lõm ngực giết Liêu Thanh Sơn; phó bang chủ Thanh Bang mặt đen bế Hoàng Phủ Kiệt chạy, hắn tái phát thương nên chúng thoát. Về trang viên, hắn thừa nhận với Võ Đang "ta chính là Sở Bá Vương"; Khương Hải Vân hứa với Thanh Bang sẽ dụ hắn xuất hiện.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 256-285"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.285: Diệp Sở trọng thương tái phát, Hoàng Phủ Kiệt và phó bang chủ Thanh Bang mặt đen chạy thoát; Khương Hải Vân hứa với Thanh Bang sẽ dụ Diệp Sở xuất hiện. Hắn vừa công khai với Võ Đang rằng mình chính là Sở Bá Vương (ch.283–285).
- Chân Vũ Tông đã bị diệt sạch (Hướng Phi Vũ, Tiêu Mộc và toàn bộ đệ tử chết ở ch.239); lão tổ tông môn và Chân Vũ lão tổ vẫn chưa xuất hiện. Vu Cổ Giáo mất hai đà chủ, Tà Tăng và Hắc Long đạo nhân đã chết trong cơn bạo phát Oán Long Khí (ch.239, 279–282).
- Nhà họ Long suy tàn: Long Đỉnh Thiên chết (ch.249), Long Trấn Sơn đoạn tuyệt cha con với Vân Băng Uyển và quỳ xin lỗi, hai Vũ Tôn bát phẩm bị A Binh giết; Giang Nam Hầu Vân Thiên Cừu và Giang Nam Hổ Trần Giang Nam đều đang nhắm vào Diệp Sở (ch.240–268).
- Diệp Sở đã là Vũ Tôn cửu phẩm, sở hữu Chu Tước Thần Hỏa, Long Quyền, Ưng Trảo Công, Hình Ý Quyền, Thiên Huyễn Thuật, A Binh và Thôn Thôn; Oán Long Khí đã nuốt trọn long khí trong cổ mộ (ch.256–282).
- Tam Hồn Tỏa trong cơ thể hắn đã bị đốt đứt nhưng manh mối về mẹ ruột Lâm Huyển Huyển, quý nữ tóc đỏ và Chân Long Cốt bị moi vẫn bỏ ngỏ; hắn nghi ký ức bị ngụy tạo và có kẻ giật dây (ch.233, 255–256).
- Danh tính đã lộ với: Lâm Tự Tại (ch.257/272), Tôn Ngữ Nhu (ch.274), Chu Huyên (ch.275), Võ Đang (ch.285), Hồng Vân và Chu Thanh Thanh (ch.253), Vân Băng Uyển (ch.192). Khương Quân Dao, Hàn Mộng Quan, nhà họ Khương, nhà họ Diệp, Giang Nam Hầu/Hổ vẫn chưa biết hắn là Sở Bá Vương.
- Pháp bảo/đan dược then chốt còn giữ: ba bảo vật nhà họ Long, ngọc giản hình kiếm (chưa nhận), Đại Vu Thiên Kinh, Bát Quái Bàn Mao Sơn (Thanh Vi nhặt), Diên Thọ Hoàn mà Chu Huyên đòi (ch.272–275).
- Không đổi cách gọi đã chốt (LƯU Ý 44–52): 江南侯 = Giang Nam Hầu (Vân Thiên Cừu) KHÁC 江南虎 = Giang Nam Hổ (Trần Giang Nam); "Vũ Tôn" (không viết "Võ Tôn"); "Chân Vũ Tông" cho cả 真武宗 lẫn 真武门; "Thệ Tâm Cổ"; "Tư Đồ Tĩnh = U Lan"; "Tường Vi"; "Diên Thọ Hoàn"; "tập đoàn Bách Dược"; "Nhân Cổ đại trận".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc rebind theo ch.285 (%d dong)" % len(NEW.strip().split("\n")))
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 256-285. tong dong:", len(lines))