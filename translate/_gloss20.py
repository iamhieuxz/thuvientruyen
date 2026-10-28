# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl20.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

def has_key(k):
    return any("=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == k for l in lines)

def add(header, entries):
    new = ["%s = %s" % (z, v) for z, v in entries if not has_key(z)]
    if not new:
        print("  (da co)", header[:16]); return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]; print("  +%d truoc %s" % (len(new), header[:20])); return

def fix(k, v):
    for i, l in enumerate(lines):
        if "=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == k:
            lines[i] = v; print("  SUA", k); return

add("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("苏队长", 'Tô đội trưởng (đội trưởng hộ vệ của Trấn Tây đại tướng quân, uống Vương Huyết Đan, khai hợp tác Đông Doanh rồi bị xử bắn nên tự sát — ch.348–358)'),
    ("雷秀梅", 'Lôi Tú Mai (mẹ nuôi của Tần Như Ngọc, cựu y tá, chủ động bán tin và đưa con vào nhà họ Tần dù biết con sẽ bị hiến tế — ch.350)'),
    ("陈元青", 'Trần Nguyên Thanh (cháu của Giang Nam Hổ, tới Giang Đô đòi Hàn Mộng Quan và Hoàng Phủ Thi Nguyệt; source ch.365 có chỗ chép 陈远青 = Trần Viễn Thanh, cùng một người — ch.362–366)'),
    ("何叔", 'Hà thúc (hộ vệ Đại Vũ Tôn của Trần Nguyên Thanh — CHÚ Ý: khác "Hà thúc" ở ch.219–220 vốn là Lôi Minh do source gõ lẫn — ch.365)'),
    ("云无忧", 'Vân Vô Ưu (mẹ của Vân Băng Uyển, bị Thanh Bang bắt dâng cho Đông Hải Hầu rồi sinh ra nàng — ch.374)'),
])

add("## ══════ ĐỊA DANH", [
    ("千药集团", 'Thiên Dược tập đoàn (công ty do Hoàng Phủ Kiệt lập để đối đầu tập đoàn Bách Dược — ch.359)'),
    ("雄鹰帝国", 'Hùng Ưng đế quốc (quốc gia đang săn người có huyết mạch đặc biệt để chế tạo chiến binh gien, có quan hệ với Đông Hải Hầu — ch.375)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("王血丹", 'Vương Huyết Đan (đan dược giúp tăng liền mấy tiểu cảnh giới, Tô đội trưởng dùng — ch.348)'),
    ("七星灵血大阵", 'Thất Tinh Linh Huyết đại trận (đại trận hiến tế cần đủ Ngũ Hành linh thể và Âm Dương linh thể, chỉ phá được nếu một người trong trận tự hy sinh — ch.349–352)'),
    ("玄武真经", 'Huyền Vũ chân kinh (cổ kinh khắc trên tượng Huyền Vũ, Diệp Sở thu được bằng cách nhỏ máu — ch.347, 372)'),
    ("玄武印", 'Huyền Vũ ấn (ấn pháp Diệp Sở luyện từ Huyền Vũ chân kinh, đánh bay cả Đại Vũ Tôn — ch.373–375)'),
    ("无垢道体", 'Vô Cấu đạo thể (thể chất Diệp Sở đạt được sau khi Huyền Vũ tái tạo thân thể — ch.358)'),
    ("九鼎", 'Cửu Đỉnh (chín đỉnh do Đại Vũ đúc để trấn khí vận Đại Hạ; Huyền Vũ Đỉnh là một trong số đó — ch.354)'),
    ("百花膏", 'Bách Hoa Cao (sản phẩm Thiên Dược tập đoàn tung ra để cạnh tranh — ch.359)'),
    ("十全地黄丸", 'Thập Toàn Địa Hoàng Hoàn (sản phẩm Thiên Dược tập đoàn nhắm vào tập đoàn Bách Dược — ch.359)'),
    ("重瞳", 'trọng đồng (mắt có hai con ngươi, đặc điểm của Chu Vũ — ch.357)'),
    ("基因战士", 'chiến binh gien (loại vũ khí người do Hùng Ưng đế quốc chế tạo từ người có huyết mạch đặc biệt — ch.375)'),
])

add("## ══════ QUY TẮC XƯNG HÔ", [
    ("大夏小霸王", 'Đại Hạ Tiểu Bá Vương (biệt hiệu của Chu Vũ, Trấn Tây đại tướng quân — ch.357)'),
    ("麻衣", 'ma y (lão mặc áo gai, Đại Vũ Tôn của phủ Giang Nam Hầu — ch.375)'),
])

fix("朱羽", '朱羽 = Chu Vũ (Trấn Tây đại tướng quân, có trọng đồng, biệt hiệu "Đại Hạ Tiểu Bá Vương", Quán Quân Hầu; ch.357–358 nghe Tô đội trưởng báo cáo rồi xử lý, biết Diệp Sở là Sở Bá Vương — ch.186, 357–358)')
fix("服部团藏", '服部团藏 = Phục Bộ Đoàn Tàng (thủ lĩnh nhóm Đông Doanh, dùng huyết phù đen triệu Ảnh Quỷ, bị Oán Long của Diệp Sở nuốt — ch.330, 349–354)')

BLOCK = """### Đã xảy ra — chương 346–375:
- Ch.346: U Lan ép Diệp Sở làm nam sủng rồi cùng nàng lục di tích cổ tông môn, bị cướp sạch dược liệu. Phe Vũ Đang của Tam Kiếm chân nhân tới tranh đoạt, bị cốt địch của nàng đánh cho thất khiếu chảy máu; Diệp Sở trốn, giết Lưu Tam Đao của Thanh Bang, dùng Thiên Huyễn Thuật giả dạng hắn để lần theo cổ kinh.
- Ch.347: Tần Nguyên Bá dẫn Thanh Bang và Y Xuyên Mỹ Trí Tử tới hòn đảo không một sinh vật; thạch đản trong Long Hồn Hư Không Đỉnh phản ứng, dẫn Diệp Sở tới vực nước lạnh. Hắn giết người đồng hành, lặn xuống thấy một giọt Huyền Vũ Chân Thủy bị trứng hút cạn; trứng đâm vỡ tảng đá, lộ tượng Huyền Vũ khắc chữ vàng — nghi là cổ kinh.
- Ch.348: Tần Nguyên Bá phát hiện Diệp Sở; Tô đội trưởng — hộ vệ của Trấn Tây đại tướng quân — uống Vương Huyết Đan tăng mấy tiểu cảnh giới, hợp với Sơn Bản Độ Biên vây công. Diệp Sở mượn Oán Long Khí chạy thoát, hóa bà lão tóc trắng; tới quảng trường ngũ giác thấy Tần Như Ngọc và năm người bị treo lên trụ đá làm huyết tế.
- Ch.349: Lý Huyền Đức nói đó là Thất Tinh Linh Huyết đại trận, cần đủ ngũ hành linh thể và âm dương linh thể, chỉ phá được nếu một người trong trận tự hy sinh. Tần Nguyên Bá cố kích oán hận Tần Như Ngọc để trận viên mãn; thủ lĩnh Đông Doanh Phục Bộ Đoàn Tàng ra lệnh dùng hậu thủ.
- Ch.350: Tần Nguyên Bá mở video: mẹ nuôi Lôi Tú Mai — cựu y tá — chủ động bán tin, biết con sẽ bị hiến tế vẫn đưa vào nhà họ Tần. Tần Như Ngọc sụp đổ, mất ý chí sống; Diệp Sở lộ chân dung khuyên sống để báo thù, cô nhóm lại hận ý.
- Ch.351: Diệp Sở lộ mặt trước Khương Quân Hồng và mọi người. Cột sáng thất thải hóa bảy quang long lao xuống biển, hợp với áo tím đánh Huyền Vũ hư ảnh; mặt biển nổi sóng dữ, Tần Nguyên Bá tuyên bố kế hoạch thành công, Đại Hạ sắp diệt vong.
- Ch.352: Huyền Diệp và Chu Linh Nhi công khai xúi Tần Như Ngọc đi chết, nhiều thế lực hùa theo; Chu Huyên từ chối ngăn em gái. Tuyệt vọng, cô cắn độc giấu trong răng tự sát trước mặt Tần Nguyên Bá; trận mất góc quan trọng nhất, màn sáng nứt vỡ.
- Ch.353: Diệp Sở đưa thi thể Tần Như Ngọc vào Long Hồn Hư Không Đỉnh, rồi giết Tam Kiếm chân nhân bằng ba quyền một cước và bóp nát đầu Địa Thanh dù Vũ Đang van xin. Khổng Đông Nam của Hộ Long Vệ bao vây đám Đông Doanh; Huyền Vũ Đỉnh nứt nẻ trồi lên giữa biển, áo tím đang đập phá.
- Ch.354: Mọi người nhận ra áo tím là Đông Hải Hầu; Lý Huyền Đức nói Huyền Vũ Đỉnh là một trong Cửu Đỉnh do Đại Vũ đúc trấn khí vận Đại Hạ. Phục Bộ Đoàn Tàng hiến máu đen triệu Ảnh Quỷ giết hàng loạt, bị Oán Long của Diệp Sở nuốt chửng; Đông Hải Hầu tóm Diệp Sở, nhận ra khí tức quen thuộc. Tư Đồ Tĩnh định cứu nhưng bị người Vu Cổ Giáo giữ lại.
- Ch.355: Huyền Vũ Đỉnh hút Diệp Sở vào trong, Huyền Vũ hiện thân rồi nhập vào hắn. Hắn ném đỉnh khổng lồ, dùng một giọt Huyền Vũ Chân Thủy nặng như núi đè Đông Hải Hầu — kẻ hiện nguyên hình giao long tím; giao long phá vảy xanh chạy thoát.
- Ch.356: Diệp Sở chặt tay chân, phá khí hải Tần Nguyên Bá thành "nhân trệ" chờ chết, rồi giết sạch nhóm Đông Doanh còn lại. Hắn phế Huyền Diệp, chặt một tay một chân để trả ơn cứu mạng Bạch Hạc chân nhân, tát Chu Linh Nhi hai lần; vào đỉnh với kinh mạch gần đứt hết.
- Ch.357: Huyền Vũ dùng biển Huyền Vũ Chân Thủy tái tạo thân thể, làm tan Trung Trinh Ấn. U Lan rời đi; Chu Huyên cứu Diệp Tiềm, biết Vân Băng Uyển bị Đông Hải Hầu bắt. Cảnh sang Tây cảnh: Chu Vũ — Trấn Tây đại tướng quân, có trọng đồng, biệt hiệu "Đại Hạ Tiểu Bá Vương" — nghe Tô đội trưởng báo cáo rồi bẻ nát chân hắn.
- Ch.358: Tô đội trưởng khai hợp tác Đông Doanh, bị Chu Vũ xử bắn nên tự sát sau khi xin báo thù Diệp Sở; Chu Vũ nhìn về đông: "Sở Bá Vương sao, thú vị". Tô Định Hạ — thống lĩnh Hộ Long Vệ — gọi Diệp Sở là sư đệ. Diệp Sở thành Vô Cấu đạo thể, đột phá Cương Khí Cảnh nhị trọng; Huyền Vũ đòi hắn tìm viễn cổ đại yêu lấy tinh huyết gia cố phong ấn.
- Ch.359: Huyền Vũ cho Diệp Sở một cục Huyền Vũ Chân Thủy tẩy Oán Long Khí, nói muốn triệt tiêu phải song tu với nữ có huyết mạch mạnh. Ở Giang Đô: Hắc Lang Hội nuốt Bạch Lang Hội, Hoàng Phủ Kiệt lập Thiên Dược tập đoàn tung Bách Hoa Cao, Thập Toàn Địa Hoàng Hoàn nhắm tập đoàn Bách Dược; Khương Hải Vân nhận hai mươi phần trăm cổ phần nhà họ Khương, sau lưng là Giang Nam Hổ.
- Ch.360: Hoàng Phủ Kiệt tra tấn Lý Đầu Trọc: đánh gãy chân, dội nước sôi, nhưng ông không cầu xin. Long Trấn Nhạc ép Bạch Hiểu Hiểu gả Long Xán Dương, cưỡng bức uống độc dược; Long Trấn Sơn lén đưa giải dược, tính đẩy em trai chịu tội nếu Diệp Sở trở về.
- Ch.361: Khương Hải Vân công bố nắm năm mươi hai phần trăm cổ phần tập đoàn Khương thị, đoạt ghế chủ tịch, đuổi Khương Phong Niên. Tiền có từ việc bán đứng Diệp Sở cho Thanh Bang; Hàn Mộng Quan vẫn cho mở chuỗi trực doanh, ngầm nói "để chúng nhảy nhót thêm chút".
- Ch.362: Hàn Mộng Quan biết Khương Hải Vân trộm phương thuốc, đòi ly hôn. Trần Nguyên Thanh — cháu Giang Nam Hổ — tới Giang Đô tìm Hoàng Phủ Thi Nguyệt; ông nội Hoàng Phủ Minh gọi điện, lấy cha mẹ cô ra uy hiếp.
- Ch.363: Hoàng Phủ Thi Nguyệt định đi gặp, Gia Cát Triết Nhã hiến kế dàn cảnh ở nông trại ngoại ô do nàng mua. Trần Nguyên Thanh đòi có bằng được Hàn Mộng Quan; Khương Hải Vân đồng ý giao vợ, hẹn ăn bữa cuối trước ly hôn.
- Ch.364: Khương Hải Vân chuốc thuốc mê Hàn Mộng Quan, đưa tới nông trại dâng cho Trần Nguyên Thanh, khai đã hạ dược. Ba nữ Hoàng Phủ Thi Nguyệt, Gia Cát Triết Nhã, Đông Mai phẫn nộ; A Binh phục sẵn để giết sạch.
- Ch.365: A Binh — giao long băng lam — đại chiến Hà thúc, hộ vệ Đại Vũ Tôn của Trần Nguyên Thanh. Hoàng Phủ Thi Nguyệt đá nát hạ bộ và hai đầu gối hắn; Hắc Lang và Lý Hồng Toàn tới bắt cô, A Binh nuốt ba nữ kia chạy thoát, Khương Hải Vân trốn.
- Ch.366: Diệp Sở về Giang Đô, chặt chân rồi chém đầu Ngô Thiếu Binh của Hắc Lang Hội đang ức hiếp Chung San ở trang viên hồ Quảng Lăng. Gia Cát Triết Nhã báo Hoàng Phủ Thi Nguyệt bị bắt, bị gả làm thiếp Trần Nguyên Thanh sau một tuần; trước đó kẻ bí ẩn đánh cắp quan tài Tần Như Ngọc.
- Ch.367: Giang Nam Hổ xuất quan, đạt Cương Khí Cảnh ngũ trọng nhờ luyện khí vận. Lý Hồng Toàn tới Trường Sinh Chế Dược bức Vương Hạ Niên, Long Cửu gia, Tào Ưng thần phục; Diệp Sở hiện thân, một chưởng đánh trọng thương Vũ Tôn đỉnh phong.
- Ch.368: Diệp Sở chém đầu Lý Hồng Toàn, một chiêu giết Hắc Lang, giải cứu Lý Đầu Trọc bị Hoàng Phủ Kiệt tra tấn. Hắn tới khách sạn Giang Nam nơi nhà họ Long làm lễ đính hôn cho Bạch Hiểu Hiểu và Long Xán Dương.
- Ch.369: Diệp Sở xuất hiện, lộ việc "Diệp đại sư" và "Sở Bá Vương" là một người trước toàn bộ khách dự tiệc. Long Trấn Nhạc đổ tội Long Trấn Sơn nhưng bị phản đòn; Diệp Sở đánh gãy chân, phế tu vi cha con Long Trấn Nhạc và Long Xán Dương; Long Trấn Sơn bồi một trăm ức để Bạch Lang Hội tái lập.
- Ch.370: Khương Hải Vân định bán tập đoàn Khương thị, đẩy ngã Khương Phong Niên, đuổi cả nhà ra ngoài. Diệp Sở xuất hiện trước cửa, chế giễu "Khương đổng sự trưởng oai phong quá".
- Ch.371: Diệp Sở châm kim khiến Khương Hải Vân mỗi ngày chịu đau xé ruột bốn lần vĩnh viễn vì tội hại Hàn Mộng Quan. Sau đó hắn gặp Tôn Ngữ Nhu; Chu Huyên tiết lộ Vân Băng Uyển đã bị Đông Hải Hầu bắt.
- Ch.372: Diệp Sở nhỏ máu lên tượng đá, thu trọn Huyền Vũ chân kinh; Diệp Tiềm thách đấu bị một chưởng đánh bại. Ở Kim Lăng, Hoàng Phủ Chính và Lý Thục Anh ép Hoàng Phủ Thi Nguyệt gả, cho biết Giang Nam Hổ đã thành Đại Vũ Tôn.
- Ch.373: Giang Nam Hổ có nhà họ Phong chống lưng. Diệp Sở luyện thành Huyền Vũ ấn, đột phá Cương Khí Cảnh tam trọng, cùng Tào Ưng tới Kim Lăng, đánh gục toàn bộ vệ binh phủ Giang Nam Hầu.
- Ch.374: Giang Nam Hầu Vân Thiên Cừu thừa nhận Vân Băng Uyển là cháu ngoại: mẹ nàng là Vân Vô Ưu, bị Thanh Bang bắt dâng cho Đông Hải Hầu rồi sinh ra nàng. Hắn khai từng đẩy cô vào Nga Mi rồi Vũ Đang để mượn đao giết Đông Hải Hầu, nay muốn mượn tay Diệp Sở — thừa nhận lợi dụng hắn.
- Ch.375: Lão ma y — Đại Vũ Tôn của phủ Giang Nam Hầu — bị Huyền Vũ ấn của Diệp Sở đánh bay một chiêu. Vân Thiên Cừu tiết lộ Đông Hải Hầu tiếp người Hùng Ưng đế quốc đang săn người có huyết mạch đặc biệt để chế chiến binh gien, và Giang Nam Hổ nhờ luyện khí vận mười ba thành phố tỉnh Giang Nam mà liền phá mấy cảnh giới.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 346-375"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.375: Vân Thiên Cừu hé lộ Giang Nam Hổ đã dùng khí vận mười ba thành phố tỉnh Giang Nam để liền phá mấy cảnh giới (đạt Cương Khí Cảnh ngũ trọng), ngầm mời Diệp Sở lấy phương pháp đó; Vân Băng Uyển đang trong tay Đông Hải Hầu, và Hùng Ưng đế quốc nhắm vào huyết mạch của cô để chế chiến binh gien (ch.374–375).
- Danh tính đã LỘ CÔNG KHAI: từ ch.369, cả khách dự tiệc ở khách sạn Giang Nam (nhà họ Long, nhà họ Diệp, Diệp Đình Đình, Diệp Thiên Thành…) đều biết "Diệp đại sư" = "Sở Bá Vương"; Chu Vũ biết từ ch.358; Hắc Lang Hội và Lý Hồng Toàn biết trước đó (ch.366–369).
- Diệp Sở hiện là Cương Khí Cảnh tam trọng, Vô Cấu đạo thể, có Huyền Vũ ấn, Huyền Vũ chân kinh, Huyền Vũ Chân Thủy, Long Hồn Hư Không Đỉnh, A Binh và Thôn Thôn; Trung Trinh Ấn đã được tẩy (ch.357–373).
- Quan hệ mới: Chu Vũ — Trấn Tây đại tướng quân, "Đại Hạ Tiểu Bá Vương", biết Diệp Sở là Sở Bá Vương và đang chú ý; Tô Định Hạ gọi Diệp Sở là sư đệ; Huyền Vũ đòi hắn tìm viễn cổ đại yêu lấy tinh huyết (ch.354–358).
- Giang Đô: Bạch Lang Hội bị Hắc Lang Hội nuốt rồi được tái lập sau khi Diệp Sở giết Hắc Lang; Hoàng Phủ Kiệt lập Thiên Dược tập đoàn; Khương Hải Vân bị châm kim chịu đau bốn lần mỗi ngày; Hàn Mộng Quan đòi ly hôn; Khương Phong Niên bị đuổi khỏi tập đoàn Khương thị (ch.359–371).
- Không đổi cách gọi đã chốt (LƯU Ý 44–52): "Sở Bá Vương" là Diệp Sở; 江南侯 = Giang Nam Hầu (Vân Thiên Cừu) KHÁC 江南虎 = Giang Nam Hổ (Trần Giang Nam); "Vũ Tôn"/"nữ Vũ Tôn"; "Chân Vũ Tông"; "Hắc Lang" (người) KHÁC "Hắc Lang Hội" (bang); "Lưu Tam Đao" KHÁC "Lý Tam Đao"; "Hoàng Phủ Chính" KHÁC "Hoàng Phủ Minh"; "Hà thúc" ở ch.365 là người khác với Lôi Minh ở ch.219–220; "linh thể" viết thường; "Huyền Vũ Đảo" khác "Huyền Vũ Đỉnh".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc rebind theo ch.375 (%d dong)" % len(NEW.strip().split("\n")))
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 346-375. tong dong:", len(lines))