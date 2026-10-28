# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl18.txt")
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
    ("向少坤", 'Hướng Thiếu Khôn (thiếu gia nhà họ Hướng ở Đông Hải, ve vãn Vân Băng Uyển, bị Diệp Sở dùng ngân châm phế chân một năm — ch.296–306)'),
    ("向少乾", 'Hướng Thiếu Can (anh của Hướng Thiếu Khôn, dẫn hai trưởng lão bát phẩm Vũ Tôn lẻn vào trang viên, bị A Binh đóng băng đập vỡ cả ba — chết ch.305)'),
    ("云冲", 'Vân Xung (con trai út của Giang Nam Hầu Vân Thiên Cừu, hôn phu được sắp đặt của Gia Cát Triết Nhã; kiêu ngạo, mang 30 ám vệ súng đặc chế tới Giang Đô, bị Diệp Sở một chưởng giết ở ch.314)'),
    ("李洪全", 'Lý Hồng Toàn (cung phụng của phủ Giang Nam Hầu, truyền nhân Bát Quái Môn đất Lỗ, từng thua Mã Tam Đao hạng mười Hoàng Bảng; thực chất theo Giang Nam Hổ, bày kế điệu hổ ly sơn — ch.309–314)'),
    ("黑狼", 'Hắc Lang (nghĩa đệ của Giang Nam Hổ, phụ trách thâu tóm Giang Đô, bàn với Hoàng Phủ Kiệt và Khương Hải Vân — ch.302–304)'),
    ("诸葛正", 'Gia Cát Chính (anh của Gia Cát Triết Nhã, truyền lệnh ông nội buộc nàng đính hôn với Vân Xung trước cuối năm — ch.307)'),
    ("江别", 'Giang Biệt (thống lĩnh thành vệ quân Giang Đô, anh của một người làm ở phủ Giang Nam Hầu; kéo tới bắt Diệp Sở không cần bằng chứng — ch.311)'),
    ("张自力", 'Trương Tự Lực (phó thị trưởng Giang Đô, có anh làm ở phủ Giang Nam Hầu, đi cùng Giang Biệt — ch.311)'),
    ("叶潜", 'Diệp Tiềm (thiếu niên 16–17 tuổi, em của Chu Huyên, trốn cấm túc tới Giang Đô để thách đấu hạng mười Hoàng Bảng; mẹ hắn chờ xem "huynh đệ tương tàn" — ch.304–308)'),
])

add("## ══════ ĐỊA DANH", [
    ("东海向家", 'nhà họ Hướng ở Đông Hải (thế lực chỉ kém Thanh Bang, gia tộc của Hướng Thiếu Khôn và Hướng Thiếu Can — ch.296–305)'),
    ("八卦门", 'Bát Quái Môn (môn phái võ học ở đất Lỗ, có tuyệt kỹ Đơn Hoán Chưởng và Du Long Chưởng; Lý Hồng Toàn là truyền nhân — ch.309)'),
    ("玄武岛", 'Huyền Vũ Đảo (hòn đảo viễn cổ bị trận pháp phong ấn dưới Đông Hải, có bão cương khí giúp đột phá Đại Vũ Tôn — ch.314–315)'),
    ("东城区", 'khu Đông Thành (khu mới của Giang Đô, nơi có khách sạn Thanh Bang và hội đấu giá của Long Cửu gia — ch.286–297)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("罡气境", 'Cương Khí Cảnh (cảnh giới chuyển chân khí thành cương khí, bước vào hàng Đại Vũ Tôn — ch.304–314)'),
    ("大武尊", 'Đại Vũ Tôn (cấp trên Vũ Tôn, đạt được khi vào Cương Khí Cảnh; Giang Nam Hổ muốn mượn khí vận mười ba thành để đột phá — ch.304–315)'),
    ("王级", 'Vương Cấp (cảnh giới cao hơn Đại Vũ Tôn, mô tả Đông Hải Hầu — ch.307)'),
    ("试万户", 'Thí Vạn Hộ (chức Hộ Long Vệ phá lệ phong cho người ngoài, trên thiên hộ; Diệp Sở được phong nhờ giết hai hung nhân Ám Bảng — ch.299–311)'),
    ("忍者", 'Nhẫn Giả (ninja Đông Doanh, hệ Giáp Hạ Lưu, dùng Ảnh Phân Thân và Ảnh Vũ Sĩ — VIẾT "Nhẫn Giả"; 上忍 = Thượng Nhẫn, 影分身 = Ảnh Phân Thân, 影武士 = Ảnh Vũ Sĩ — ch.288–291)'),
    ("九头凤凰", 'Cửu Đầu Phượng Hoàng (dị tượng kết thành trong khí hải sau khi huyết mạch Tư Đồ Tĩnh giác tỉnh, đùa với Oán Long Khí — ch.294)'),
    ("血脉觉醒", 'huyết mạch giác tỉnh (máu chuyển màu cửu sắc, thức tỉnh huyết mạch yêu tộc — ch.294)'),
    ("百毒不侵之体", 'Bách Độc Bất Xâm Chi Thể (thể chất miễn nhiễm mọi độc, giúp Diệp Sở không trúng độc ở tiệc — ch.288)'),
    ("延寿液", 'Diên Thọ Dịch (bản pha loãng của Diên Thọ Hoàn do Diệp Sở cải tiến để sản xuất hàng loạt — ch.301)'),
    ("补气丸", 'Bổ Khí Hoàn (đan bổ khí Vân Xung mượn cớ nhờ luyện để khiêu khích — ch.309)'),
])

BLOCK = """### Đã xảy ra — chương 286–315:
- Ch.286: Khương Quân Dao gọi Hoàng Phủ Thi Nguyệt hỏi tin Diệp Sở, bị đáp lạnh nhạt nên bóp nát điện thoại. Oán Long Khí đã ăn một phần năm kinh mạch hắn; hắn song tu cả đêm với Hoàng Phủ Thi Nguyệt để cầm cự. Khương Hải Vân lén tới khách sạn ở khu Đông Thành gặp Thanh Bang: Tào Khánh Dương, một gã đại hán và một người đeo kính hỏi hắn định dụ Diệp Sở ra bằng cách nào.
- Ch.287: Tiệc sinh nhật Khương Quân Dao do Hàn Mộng Quan sắp xếp; Chu Thanh Thanh cho biết Diệp Sở vừa vào Hoàng Bảng hạng mười — hệ Thiên Địa Huyền Hoàng, mỗi bảng mười người, Hoàng Bảng dành cho Vũ Tôn. A Binh hiện nguyên hình mãng xà băng lam trước Hoàng Phủ Thi Nguyệt. Giữa tiệc người Thanh Bang xông vào, Lam Liên đứng ra.
- Ch.288: Lam Liên đấu Tào Khánh Dương thì nôn máu — cả bàn trúng độc, chỉ Diệp Sở miễn nhiễm nhờ Bách Độc Bất Xâm Chi Thể; Hàn Mộng Quan nghi Khương Hải Vân. Tào Khánh Dương tưởng hắn mất chân khí nên lao vào, bị túm chân ném vào tường rồi đá nát ngực — chết. Năm ninja áo đen hiện ra; gã đeo kính đòi long khí.
- Ch.289: A Binh đấu gã đeo kính — cửu phẩm Vũ Tôn. Năm ninja là Ảnh Phân Thân của một Thượng Nhẫn hệ Giáp Hạ Lưu; Diệp Sở giả trúng độc, giết một kẻ, thu năm thanh đao vào tiểu đỉnh. Năm thân hợp nhất đạt Vũ Tôn viên mãn; gai trên chuôi đao đâm thủng tay, vai trái hắn trúng đao.
- Ch.290: Diệp Sở dùng Long Quyền, điều khiển vũ khí địch phản chém rồi đấm nát lưng giết tên ninja. Một Ảnh Vũ Sĩ ẩn trong bóng đâm xuyên ngực hắn; A Binh hóa khổng lồ đấu gã đeo kính. Khương Quân Dao lao vào đỡ nhát đâm vào tim — hết chương.
- Ch.291: Khương Quân Dao chỉ nói "chuyện trước kia, xin lỗi" rồi ngất; Diệp Sở cất nàng vào tiểu đỉnh và cưỡng đoạt sức Oán Long Khí, mắt đỏ rực. Hai đấm một đạp giết Ảnh Vũ Sĩ; gã đeo kính phá cửa sổ chạy. Hắn mất kiểm soát, nôn máu, phải nhốt Oán Long Khí lại; Lam Liên cứu Khương Quân Dao, Hàn Mộng Quan cảnh cáo Khương Hải Vân.
- Ch.292: Khương Quân Dao hôn mê, Lam Liên đưa về Nga Mi; Diệp Sở tặng Chu Thanh Thanh một Trú Nhan Đan để chuyển cho nàng, tặng Hồng Vân Thục Sơn Lệnh, hứa sẽ lên Nga Mi. Hắn cho Hàn Mộng Quan uống Trú Nhan Đan, bà trẻ ra mười tuổi; Hoàng Phủ Kiệt gọi Khương Hải Vân. Tư Đồ Tĩnh gọi: Đại Vu Thiên Kinh tự cháy, hỏi cách gỡ phong ấn.
- Ch.293: Tư Đồ Tĩnh đến trang viên hồ Quảng Lăng; Diệp Sở khám thấy nàng không có đặc thù thể chất, bèn ra điều kiện "ngủ một đêm" để gỡ ấn. Nàng từ chối, A Binh chặn cửa, hắn dọa giết, nàng miễn cưỡng nhận. Đại Vu Thiên Kinh là bảo điển vu thuật thượng cổ, trấn giáo chi bảo của Vu Cổ Giáo; khi song tu, Oán Long Khí hưng phấn hút luồng năng lượng cửu sắc.
- Ch.294: Năng lượng cửu sắc phát từ huyết mạch Tư Đồ Tĩnh — máu chuyển cửu sắc, huyết mạch giác tỉnh, kết thành Cửu Đầu Phượng Hoàng trong khí hải, đùa với Oán Long Khí, oán khí giảm còn bảy mươi phần trăm. Diệp Sở nhận ra Chân Hoàng Thể/Chân Long Thể là thể song tu tốt nhất, nghĩ tới Khương Quân Dao. Sau một ngày một đêm Tư Đồ Tĩnh ngất; hắn thú nhận chỉ phong ấn bìa sách, nàng tức giận bỏ đi, thề trả thù.
- Ch.295: Diệp Sở chữa cho Vân Băng Uyển tỉnh, tự nhận là Sở Bá Vương, cho nàng uống Trú Nhan Đan trẻ ra bảy tám tuổi. Đêm đó dự đấu giá ở khu Đông Thành cùng Võ Đang, tặng Đỗ Linh Nhi một Trú Nhan Đan; Bạch Hạc chân nhân hỏi Diên Thọ Hoàn có kéo dài thọ cho Vũ Tôn — hắn đáp gần như vô ích. Vương Hạ Niên cùng thuộc hạ cung kính gọi "Sở Bá Vương".
- Ch.296: Diệp Sở giao đan dược cho Vương Hạ Niên. Hướng Thiếu Khôn — thiếu gia nhà họ Hướng ở Đông Hải, thế lực chỉ kém Thanh Bang — bắt chuyện Vân Băng Uyển; Diệp Dật Không gọi nàng là quả phụ, bị Đỗ Linh Nhi tát bay. Diệp Dật Thần, Diệp Dật Phi lăng mạ Diệp Sở, nói hắn đã chết; nhà họ Diệp đang nhờ Diệp Đình Đình bám nhà họ Hướng.
- Ch.297: Diệp Sở xuất hiện, một tiếng quát làm Diệp Dật Không ngã chảy máu thất khiếu; hắn buộc Hướng Thiếu Khôn và nhà họ Diệp xin lỗi Vân Băng Uyển, Đỗ Linh Nhi rồi đuổi đi. Hội đấu giá ba tầng của Long Cửu gia: tầng một đồ cổ/trang sức, tầng hai tranh chữ, tầng ba phòng đấu giá. Phía trước, Chu Tử Nghĩa làm vỡ bình thanh hoa và đụng Hướng Thiếu Khôn.
- Ch.298: Chu Tử Nghĩa là con của cố thành vệ thống lĩnh Chu Bẩm Thiên; Ngô Thiếu Binh và chị Ngô Thiến Thiến lừa sạch tiền anh qua công ty ma rồi bỏ rơi. Diệp Dật Không ra lệnh bắt anh quỳ, tự tát mười cái; Hướng Thiếu Khôn thêm "đánh gãy hai chân", Ngô Thiếu Binh đánh đến nôn máu.
- Ch.299: Diệp Sở một đòn hạ Ngô Thiếu Binh, cho Chu Tử Nghĩa đan dược và nhận lời báo thù; Vương Hạ Niên một cú điện thoại lo nhà họ Ngô phá sản. Hắn dùng ngân châm phế chân Hướng Thiếu Khôn một năm. Chu Huyên báo hắn được phá lệ phong Thí Vạn Hộ của Hộ Long Vệ nhờ giết hai hung nhân Ám Bảng; Diệp Sở nghi Hộ Long Vệ nhắm long khí.
- Ch.300: Hắc Long đạo nhân và người Long Hổ Sơn được xác nhận đã chết. Hướng Thiếu Can — anh Hướng Thiếu Khôn — kéo nhà họ Diệp tới, cùng Diệp Thiên Thành, Tạ Vũ San. Diệp Đình Đình khuyên Diệp Sở chữa chân và xin lỗi; hắn tuyên bố "trước kia ta đã nhìn nhầm người, từ nay về sau giữa chúng ta không còn liên quan". Một bát phẩm Vũ Tôn của nhà họ Hướng ra tay, bị một chưởng đánh trọng thương.
- Ch.301: Đấu giá Diên Thọ Hoàn thu hàng trăm tỷ; Diệp Sở đưa Hoàng Phủ Thi Nguyệt công thức Diên Thọ Dịch để sản xuất hàng loạt. Chu Huyên về nhà họ Chu ở nam đế đô, gặp Lâm Huyển Huyển — quản gia; bà báo cho một mỹ phụ tuyệt sắc, người này gọi Diệp Sở là "nghiệt chủng", muốn giữ hắn làm đá mài cho "Tiểu Vũ" và sai Lâm Huyển Huyển giúp "cháu trai" đang bị cấm túc trốn ra. Hướng Thiếu Can và nhà họ Diệp đến trang viên xin gặp Sở Bá Vương, bị Chung San từ chối.
- Ch.302: Diệp Sở nói Sở Bá Vương là bạn mình nên không hợp tác. Khương Hải Vân xin vào phòng nghiên cứu tập đoàn Bách Dược lấy công thức Thập Toàn Đại Bổ Hoàn, Bách Hoa Lộ; Hàn Mộng Quan cho vào nhưng sai người theo dõi. Hắn gặp Hoàng Phủ Kiệt và Hắc Lang — nghĩa đệ của Giang Nam Hổ; Hoàng Phủ Kiệt hứa hai mươi phần trăm cổ phần tập đoàn Khương thị, Hắc Lang nhận việc thâu tóm Giang Đô. Diệp Sở đột phá Vũ Tôn đại viên mãn; Bạch Hiểu Hiểu đến cầu cứu.
- Ch.303: Hoàng Phủ Kiệt đòi Bạch Hiểu Hiểu quy phục, bị từ chối, bị Lý Đầu Trọc đá ngã, bèn lôi Giang Nam Hổ ra dọa. Diệp Sở bước ra; Hoàng Phủ Kiệt quỳ lạy, bị đá gãy xương ống chân, khai Giang Nam Hổ muốn thống nhất giới ngầm mười ba thành tỉnh Giang Nam. Diệp Sở bảo nhắn Giang Nam Hổ tránh xa Bạch Lang Hội, nếu không sẽ đánh lên Kim Lăng.
- Ch.304: Hắc Lang đổi kế, lập bang mới. Diệp Tiềm — 16–17 tuổi, em Chu Huyên — trốn cấm túc theo cô về Giang Đô để thách đấu hạng mười Hoàng Bảng; mẹ hắn nói "huynh đệ tương tàn" sẽ thú vị. Lâm Huyển Huyển điều tra: ba năm trước Diệp Sở là người thường, vào Ngục Long Đàm thay tội cho trưởng tử đại phòng nhà họ Diệp, ra tù có võ công — nghi bị sửa ký ức. Diệp Sở luyện chuyển chân khí thành cương khí để vào Cương Khí Cảnh; đêm đó Hướng Thiếu Can cùng hai bát phẩm Vũ Tôn lẻn vào.
- Ch.305: A Binh một đòn sét băng đóng băng rồi đập vỡ cả ba — Hướng Thiếu Can và hai trưởng lão chết, Diệp Sở không hay. Hàn Mộng Quan quỳ xin Sở Bá Vương tha chồng, khai Khương Hải Vân đã lấy tài liệu công thức; Diệp Sở đưa công thức giả để "tương kế tựu kế". Bà nói quý hắn vì giống "một cố nhân", khiến hắn nghi về cha mẹ ruột.
- Ch.306: Diệp Sở tặng Tôn Ngữ Nhu Trú Nhan Đan; nàng là Chân Vũ Linh Thể, đã Đoán Thể chín đoạn. Hắn xin lỗi Gia Cát Triết Nhã, tặng Trú Nhan Đan, không ép nữa; nàng mềm lòng rồi nhận cuộc gọi khiến sắc mặt biến đổi. Diệp Tiềm và Chu Huyên xuống sân bay Giang Đô. Hướng Thiếu Khôn lo Hướng Thiếu Can mất tích; Diệp Đình Đình nhắc yến nhà họ Long đón nhân vật phủ Giang Nam Hầu.
- Ch.307: Gia Cát Chính truyền lệnh ông nội: Gia Cát Triết Nhã phải đính hôn với Vân Xung — con út Giang Nam Hầu — trước cuối năm và nhường mảng Bách Dược Tửu. Chu Huyên trao thẻ Thí Vạn Hộ, cảnh cáo Giang Nam Hầu dính tới Đông Hải Hầu — "đệ nhất hầu" Đại Hạ, gốc Đông Doanh, cảnh Vương Cấp. Tại yến nhà họ Long, Long Trấn Sơn kể xấu Diệp Sở; Vân Xung nói "đỡ cho ta phải đích thân đi tìm hắn".
- Ch.308: Vân Băng Uyển đến yến vì nhà họ Long hứa tiết lộ thân thế; Gia Cát Triết Nhã và Diệp Tiềm cũng có mặt. Long Trấn Sơn giới thiệu Vân Xung là con út Giang Nam Hầu. Vân Xung định giết kẻ cắm sừng mình, bắt Gia Cát Triết Nhã về Kim Lăng, nhưng đổi ý muốn giữ nàng; hắn bước tới chào "Triết Nhã, lâu rồi không gặp".
- Ch.309: Vân Xung mượn cớ nhờ luyện Bổ Khí Hoàn để khiêu khích; Diệp Sở bịa hắn "liệt dương ba phút", đòi giảm giá hai mươi phần trăm. Vân Xung sai Lý Hồng Toàn — truyền nhân Bát Quái Môn đất Lỗ, từng thua Mã Tam Đao hạng mười Hoàng Bảng — ra tay. Diệp Sở dùng Ưng Trảo Công đánh lui bảy tám bước; Lý Hồng Toàn nhận ra hắn đã chạm cương khí, nhận thua.
- Ch.310: Vân Xung lôi thân phận Giang Nam Hầu, cho ba mươi ám vệ mang súng đặc chế bao vây; Diệp Sở dùng thân pháp rắn né đạn, hạ toàn bộ trong chưa đầy mười lăm phút. Lý Hồng Toàn từ chối tham chiến. Vân Xung dọa xin lệnh bắt qua thành vệ; Diệp Sở chỉ đáp "cứ tự nhiên".
- Ch.311: Thống lĩnh thành vệ quân Giang Biệt và phó thị trưởng Trương Tự Lực — có anh làm ở phủ Giang Nam Hầu — kéo tới bắt không cần bằng chứng. Diệp Sở ném thẻ Thí Vạn Hộ của Hộ Long Vệ; hai người chết sững, Vân Xung gọi là đồ giả, định xé. Kết: tiếng quát của Chu Huyên.
- Ch.312: Chu Huyên xưng là bách hộ Hộ Long Vệ, người vương tộc Chu gia; Vân Xung xuống nước xin lỗi. Diệp Sở viện luật "tấn công Thí Vạn Hộ" (năm đến mười năm tù), sai Lâm Tự Tại bắt Vân Xung; Chu Huyên đồng ý sau khi được hứa Trú Nhan Đan. Long Trấn Sơn khai Vân Băng Uyển không phải con mình — Giang Nam Hầu sai nhà họ Long nuôi như con riêng.
- Ch.313: Nhà họ Long (cả Long Trấn Nhạc) khai định mượn tay Vân Xung báo thù; Long Trấn Sơn nôn máu, thừa nhận. Diệp Sở phạt nhà họ Long chuyển hai trăm tỷ cho nhà họ Vân trong ba ngày. Giang Nam Hầu cứu Vân Xung, mắng và đuổi về Kim Lăng, nhưng hắn ở lại toan chiếm tập đoàn Bách Dược, thu phục Sở Bá Vương, "nếu không thì giết". Diệp Sở chỉ ngưng được một tia cương khí; Vân Xung và Lý Hồng Toàn đột nhập trang viên, A Binh giao chiến.
- Ch.314: Diệp Sở dùng Ưng Trảo Công đánh trọng thương Lý Hồng Toàn, kẻ này đoán ra hắn là Sở Bá Vương. Diệp Sở một chưởng giết Vân Xung; Lý Hồng Toàn đổi mạng bằng tin Đông Hải có Huyền Vũ Đảo lộ ra, có bão cương khí giúp đột phá. Thực ra Lý Hồng Toàn đã theo Giang Nam Hổ: đây là kế điệu hổ ly sơn, dụ Diệp Sở rời Giang Đô để Hắc Lang chiếm thành, giúp Giang Nam Hổ mượn khí vận mười ba thành đột phá Đại Vũ Tôn.
- Ch.315: Bạch Hạc chân nhân xác nhận Huyền Vũ Đảo bị trận pháp phong ấn dưới biển, cảnh báo mượn cương khí đột phá là chín chết một sống; hai ngày nữa lên đường, hẹn ở Đông Hải. Diệp Sở giúp Hoàng Phủ Thi Nguyệt đột phá đại tông sư, dặn nàng ở trang viên; thú nhận giết Vân Xung với Gia Cát Triết Nhã và dàn xếp cho nàng ở cùng. Hắn định đưa Vân Băng Uyển đi Huyền Vũ Đảo, để Tôn Ngữ Nhu về trang viên.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 286-315"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.315: hai ngày nữa Diệp Sở rời Giang Đô ra Đông Hải tìm Huyền Vũ Đảo để mượn bão cương khí đột phá Đại Vũ Tôn; đây là kế điệu hổ ly sơn của Giang Nam Hổ (Hắc Lang sẽ chiếm Giang Đô, Giang Nam Hổ mượn khí vận mười ba thành). Giang Nam Hầu Vân Thiên Cừu sẽ truy sát vì cái chết của Vân Xung (ch.313–315).
- Diệp Sở đã giết Vân Xung; Lý Hồng Toàn bị trọng thương và đã đoán ra hắn là Sở Bá Vương. Đông Hải Hầu — "đệ nhất hầu" Đại Hạ, gốc Đông Doanh, cảnh Vương Cấp — có quan hệ với Giang Nam Hầu và chưa xuất hiện (ch.307–314).
- Thân thế: Vân Băng Uyển không phải con Long Trấn Sơn mà do Giang Nam Hầu gửi nuôi (ch.312). Mẹ ruột Diệp Sở là Lâm Huyển Huyển — quản gia nhà họ Chu ở nam đế đô — và một mỹ phụ tuyệt sắc gọi hắn là "nghiệt chủng", muốn dùng hắn làm đá mài cho "Tiểu Vũ"; bà ta sai Lâm Huyển Huyển giúp "cháu trai" bị cấm túc trốn ra (ch.301, 304).
- Khương Hải Vân là nội gián: lấy công thức cho Hoàng Phủ Kiệt/Hắc Lang nhưng bị đưa công thức giả (ch.302–305). Hàn Mộng Quan đã quỳ xin tha cho ông ta; bà quý Diệp Sở vì giống "một cố nhân" (ch.305).
- Hộ Long Vệ: Diệp Sở được phong Thí Vạn Hộ, đã công khai thân phận trước nhà họ Vân, họ Diệp, họ Khương, họ Hướng, Gia Cát gia và nhà họ Long (ch.311–312). Chu Huyên đang chờ Trú Nhan Đan; Diệp Tiềm — em cô, thách đấu hạng mười Hoàng Bảng — đang ở Giang Đô (ch.299–308).
- Hoàng Phủ Thi Nguyệt đã đột phá đại tông sư (ch.315); tập đoàn Bách Dược do Tôn Ngữ Nhu làm chủ tịch, Hàn Mộng Quan làm tổng giám đốc; Gia Cát Triết Nhã bị buộc đính hôn với Vân Xung trước cuối năm nhưng Vân Xung đã chết (ch.307, 314).
- Không đổi cách gọi đã chốt (LƯU Ý 44–52): "Sở Bá Vương" là Diệp Sở; 江南侯 = Giang Nam Hầu (Vân Thiên Cừu) KHÁC 江南虎 = Giang Nam Hổ (Trần Giang Nam); "Vũ Tôn"/"nữ Vũ Tôn"; "Chân Vũ Tông"; "Thệ Tâm Cổ"; "Tư Đồ Tĩnh = U Lan"; "Diên Thọ Hoàn"; "tập đoàn Bách Dược"; "Đông Hải Hầu"; "Nhẫn Giả".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc rebind theo ch.315 (%d dong)" % len(NEW.strip().split("\n")))
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 286-315. tong dong:", len(lines))