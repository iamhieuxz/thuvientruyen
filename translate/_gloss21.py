# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl21.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

def has_key(k):
    return any("=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == k for l in lines)

def add(header, entries):
    new = ["%s = %s" % (z, v) for z, v in entries if not has_key(z)]
    if not new:
        print("  (da co)"); return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]; print("  +%d" % len(new)); return

add("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("熊涛", 'Hùng Đào (huynh đệ kết nghĩa của Giang Nam Hổ, Vũ Tôn; source có chỗ chép 雄涛 — cùng một người — ch.377)'),
    ("马良", 'Mã Lương (罡气境 cửu trọng, tay sai của Chu Vũ, truy đoạt Huyền Vũ chân kinh; bị thanh niên đeo kính đen đánh bay cứu Diệp Sở — ch.377–385)'),
    ("曲鸿", 'Khúc Hồng (cúng phụng nhà họ Phong, 罡气境 thất trọng, dùng Kinh Lôi Trảm và Phong Thương Kiếm — ch.377–380)'),
    ("风行州", 'Phong Hành Châu (người nhà họ Phong, can ngăn báo thù — ch.387)'),
    ("风行玉", 'Phong Hành Ngọc (người nhà họ Phong, thề báo thù cho Phong Khánh Dương — ch.387)'),
    ("风潇潇", 'Phong Tiêu Tiêu (tiểu thư nhị phòng nhà họ Phong, gọi Hàn Mộng Quan là chị họ; tới Giang Đô đòi mua tập đoàn Bách Dược — ch.388–394)'),
    ("张虎", 'Trương Hổ (vệ sĩ 罡气境 bát trọng của Phong Tiêu Tiêu — ch.388–394)'),
    ("黑白无常", 'Hắc Bạch Vô Thường (hai sát thủ 罡气境 cửu trọng của Diêm La Điện, bị Diệp Sở một chiêu giết — ch.390–391)'),
    ("青玉真人", 'Thanh Ngọc chân nhân (chưởng giáo Nga Mi, giao Thục Sơn Lệnh và dặn tìm Thục Sơn kiếm kinh — ch.398)'),
])

add("## ══════ ĐỊA DANH", [
    ("阎罗殿", 'Diêm La Điện (tổ chức sát thủ, phái Hắc Bạch Vô Thường — ch.389–391)'),
    ("蜀山剑派", 'Thục Sơn kiếm phái (môn phái kiếm đạo ở Thục Địa, chỉ nhận võ giả dưới Chân Ý Cảnh — ch.387–403)'),
    ("横断山脉", 'dãy Hoành Đoạn (nơi có lối vào Thục Sơn — ch.400)'),
    ("江南名府", 'Giang Nam Danh Phủ (khách sạn tổ chức lễ cưới của Trần Nguyên Thanh — ch.377)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("真意境", 'Chân Ý Cảnh (cảnh giới ngộ được vũ đạo chân ý, trên Cương Khí Cảnh — ch.385–405)'),
    ("武道真意", 'Vũ Đạo chân ý (ý cảnh của võ đạo; đao ý/kiếm ý/thương ý là các dạng — ch.385–398)'),
    ("搜魂术", 'Sưu Hồn Thuật (thuật lục soát ký ức, Thôn Thôn truyền — ch.385)'),
    ("炼气术", 'Luyện Khí Thuật (thuật luyện hóa khí vận, mở Thiên Nhãn — ch.386)'),
    ("天眼", 'Thiên Nhãn (nhãn thuật nhìn thấy khí vận — ch.386)'),
    ("引煞阵", 'Dẫn Sát Trận (đại trận Đông Hải Hầu bày trong ngày Cực Âm để trữ sát khí bằng Cửu Âm Sát Thể của Vân Băng Uyển — ch.396)'),
    ("极阴之日", 'Cực Âm chi nhật (ngày âm khí cực thịnh, sau một tháng — ch.396)'),
    ("乾坤葫", 'Càn Khôn Hồ (bảo vật của Long Hổ Sơn, phun nước và kiếm quang; Diệp Sở đoạt được — ch.401–404)'),
    ("白虎鼎", 'Bạch Hổ Đỉnh (một trong Cửu Đỉnh, nhận ba mươi sáu thác nước trong lòng đất Thục Sơn — ch.403–405)'),
    ("三尺青锋", 'tam xích thanh phong (thanh kiếm Bạch Hổ giao cho Diệp Sở để luyện kiếm đạo — ch.405)'),
    ("先天火灵", 'Tiên Thiên Hỏa Linh (thân phận thật của Thôn Thôn do đạo sĩ Long Hổ Sơn nhận ra — ch.401)'),
    ("虎啸拳", 'Hổ Khiếu Quyền (quyền pháp của Giang Nam Hổ — ch.379)'),
    ("惊雷斩", 'Kinh Lôi Trảm (đao pháp của Khúc Hồng — ch.380)'),
    ("风伤剑", 'Phong Thương Kiếm (kiếm pháp của Khúc Hồng, có đặc tính phá giáp và trảm hình — ch.380)'),
])

block = """53. Source ch.376–405 gọi lẫn: 玄武神功 (ch.383–384) chính là 玄武真经 = Huyền Vũ chân kinh; 白狼会/黑狼会 (ch.376) là cùng một bang; 陈元青/陈远青 đều là Trần Nguyên Thanh; 熊涛/雄涛 đều là Hùng Đào. 江南虎 tên thật 陈江南. 青玉真人 là chưởng giáo Nga Mi (khác 红莲真人 là chưởng môn/sư phụ Khương Quân Dao)."""
if not any(l.strip() == block for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("## ══════ VĂN PHONG"):
            lines[i:i] = block.split("\n") + ["", ""]; print("  + LƯU Ý 53"); break

BLOCK = """### Đã xảy ra — chương 376–405:
- Ch.376: Diệp Sở hiểu Giang Nam Hổ diệt Bạch Lang Hội để đoạt khí vận Giang Đô, nhờ Vân Thiên Cừu theo dõi Đông Hải Hầu; Vân Vô Ưu xuất hiện. Hắn biết Khương Quân Dao đã vào nội môn Nga Mi và quyết mua quan tài mừng cưới. Giang Nam Hổ hạ lệnh giết hắn.
- Ch.377: Lễ cưới Trần Nguyên Thanh — tàn phế ngồi xe lăn — với Hoàng Phủ Thi Nguyệt tại Giang Nam Danh Phủ, Kim Lăng; khách có Trần Thiên Nam, Mã Lương, Chu Huyên, Phong Khánh Dương, Khúc Hồng.
- Ch.378: Hoàng Phủ Thi Nguyệt không đáp lời thề; Diệp Sở xông vào, ném quan tài đánh bay Giang Nam Hổ xuyên tường khiến cả sảnh tưởng hắn là Đại Vũ Tôn.
- Ch.379: Khúc Hồng nhận Diệp Sở chỉ Cương Khí Cảnh tam trọng, kém Giang Nam Hổ hai bậc. Giang Nam Hổ dùng Hổ Khiếu Quyền, uống huyết đan hóa cương khí đao, nhưng Diệp Sở nhờ Vô Cấu đạo thể đỡ được và hạ đối thủ bằng Long Quyền. Phong Khánh Dương đòi hắn quy phục, bị từ chối.
- Ch.380: Khúc Hồng lộ Cương Khí Cảnh thất trọng, dùng Kinh Lôi Trảm và Phong Thương Kiếm đâm thủng vai trái Diệp Sở. Diệp Sở xuất Huyền Vũ ấn đập Khúc Hồng trọng thương rồi tát Phong Khánh Dương hai cái.
- Ch.381: Chu Huyên ngăn Diệp Sở giết Phong Khánh Dương; Giang Nam Hổ bị ép tự phế tu vi và giao pháp môn khí vận nhưng dùng súng và con tin để trốn. Hoàng Phủ Thi Nguyệt tát chết Trần Nguyên Thanh; Diệp Sở giết Hoàng Phủ Kiệt bằng ngân châm.
- Ch.382: Chu Huyên tiết lộ Diệp Sở được Tô Định Hạ thăng Vạn Hộ. Hắn đuổi theo, phá trực thăng, chém đầu Phong Khánh Dương, đập nát chân Giang Nam Hổ nhưng không lấy được pháp môn khí vận.
- Ch.383: Mã Lương — Cương Khí Cảnh cửu trọng — hiện ra, đao khí xé Long Quyền, rạch vai và ngực Diệp Sở, làm Huyền Vũ ấn sứt mẻ; Long Hồn Hư Không Đỉnh chặn được. Diệp Sở bỏ chạy và bị đuổi kịp.
- Ch.384: Mã Lương đòi Huyền Vũ chân kinh và đỉnh; một thanh niên đeo kính đen bí ẩn búng tay đánh bay Mã Lương, cứu mạng Diệp Sở. Mã Lương rút, tuyên bố "đại nhân" sẽ đến lấy.
- Ch.385: Thanh niên giảng Chân Ý Cảnh và Vũ Đạo chân ý; Diệp Sở đoán chủ Mã Lương là Tiểu Bá Vương; người lạ dặn chưa đạt Chân Ý Cảnh thì chớ tìm Đông Hải Hầu. Thôn Thôn truyền Sưu Hồn Thuật; hắn biết Giang Nam Hổ sai Hoàng Phủ Kiệt lập Thiên Dược để hại Hàn Mộng Quan.
- Ch.386: Thôn Thôn truyền Luyện Khí Thuật luyện hóa khí vận, mở Thiên Nhãn. Hắn thấy khí vận tím của Giang Nam Hổ và cột khí vận Đại Hạ ở Kim Lăng, suýt mù; Oán Long Khí bị đỉnh trấn áp. Hắn nghi có người âm thầm bày cục.
- Ch.387: Tin thắng trận lan khắp Đại Hạ; Cơ Đức, Khương Quân Hồng, Khương Tiếu Tiếu bàn đi Thục Sơn kiếm phái. Nhà họ Phong họp: Phong Hành Ngọc thề báo thù, Phong Hành Châu can ngăn. Diệp Sở bóp cổ Giang Nam Hổ chết, thiêu phủ bằng Chu Tước Thần Hỏa.
- Ch.388: Hàn Mộng Quan gọi điện cho một người nhà họ Phong, được hứa gia tộc không ra tay công khai. Về Giang Đô, Diệp Sở thừa nhận mình là Sở Bá Vương với bà. Phong Tiêu Tiêu và Trương Hổ tới Giang Đô thuê sát thủ.
- Ch.389: Phong Tiêu Tiêu đến tập đoàn Bách Dược, gọi Hàn Mộng Quan là chị họ, đòi mua công ty, bị từ chối; ả dồn ép thị trường và thuê Diêm La Điện. Khương Hải Vân quỳ xin tha.
- Ch.390: Hàn Mộng Quan đưa đơn ly hôn; Khương Hải Vân đòi gỡ kim châm rồi sang Thiên Dược cầu cứu. Diệp Sở luyện hết khí vận, từ Cương Khí Cảnh tam trọng lên đại viên mãn, Huyền Vũ ấn mạnh hơn. Hắc Bạch Vô Thường đến ám sát.
- Ch.391: Diệp Sở một chiêu Huyền Vũ ấn giết cả Bạch Vô Thường lẫn Hắc Vô Thường — đều Cương Khí Cảnh cửu trọng. Phong Tiêu Tiêu dồn Bách Dược đến phá sản, trả giá một trăm triệu, đuổi Tôn Ngữ Nhu, tuyên bố Diệp Sở đã chết.
- Ch.392: Diệp Sở hiện ra, tát bay Trương Hổ — Cương Khí Cảnh bát trọng — và tát Phong Tiêu Tiêu hai cái. Hàn Mộng Quan kể mình là con gái đại phòng nhà họ Phong, bị hạ thuốc gài với Khương Hải Vân rồi bị trục xuất, đổi họ Hàn; nghi nhị phòng.
- Ch.393: Sản phẩm Thiên Dược gây dị ứng, bị phát hiện độc tố, còn Bách Dược đạt chuẩn và bán chạy. Diệp Sở khai Khương Hải Vân là người đưa phương thuốc giả; Phong Tiêu Tiêu thú nhận Khương Hải Vân chủ động hạ thuốc hại Hàn Mộng Quan.
- Ch.394: Diệp Sở lừa Phong Tiêu Tiêu rằng hắn và Hàn Mộng Quan cố ý gài bẫy, kể Khương Hải Vân bán phương thuốc giả cho Hoàng Phủ Kiệt; ả tin, sai Trương Hổ điều tra — mượn dao giết người.
- Ch.395: Tại Cục Dân chính, Khương Hải Vân chối tội; Hàn Mộng Quan ly hôn và cắt đứt, Diệp Sở gỡ kim châm. Khương Hải Vân thề trả thù. Giang Nam Hầu đến trang viên báo đã biết mục đích của Đông Hải Hầu.
- Ch.396: Đông Hải Hầu gom vật liệu bày Dẫn Sát Trận vào ngày Cực Âm sau một tháng, định dùng Cửu Âm Sát Thể của Vân Băng Uyển trữ sát khí, cho uống thuốc gien của Hùng Ưng đế quốc rồi nộp cô. Diệp Sở thề trong một tháng đánh vào phủ Đông Hải Hầu, phải đạt Chân Ý Cảnh.
- Ch.397: Khương Hải Vân bị đánh gãy tứ chi, ném khỏi Thiên Dược. Cơ Đức, Khương Quân Hồng, Khương Tiếu Tiếu mời Diệp Sở đi Thục Sơn; hắn nhận lời. Hồng Liên chân nhân về Nga Mi, đạt Cương Khí Cảnh đỉnh phong kèm một tia Vũ Đạo chân ý, được phong nội môn phó chưởng giáo, đưa hôn thư gả Khương Quân Dao cho "Sở Dạ"; Khương Quân Dao cùng Chu Thanh Thanh trốn đi Thục Sơn.
- Ch.398: Chu Vũ trao Mã Lương cây thương chứa thương ý cho chuyến Thục Sơn. Diệp Sở để Tào Ưng đột phá Vũ Tôn bảo vệ người nhà, nhờ Tô Định Hạ trông nhà họ Phong. Chưởng giáo Thanh Ngọc chân nhân giao Thục Sơn Lệnh, dặn tìm Thục Sơn kiếm kinh; chỉ võ giả dưới Chân Ý Cảnh mới được vào.
- Ch.399: Hồng Liên đón "Sở Dạ"; Chu Tước Thần Hỏa trong Diệp Sở xao động. Hồng Vân nhận ra và vạch trần Sở Dạ chính là Diệp Sở — chồng cũ của Khương Quân Dao. Hồng Liên sững sờ.
- Ch.400: Đoàn vào dãy Hoành Đoạn; A Binh hiện nguyên hình, hạ Cơ Đức nhờ Băng Lôi. Một đạo sĩ Long Hổ Sơn đang đánh A Binh, coi nó là yêu; Diệp Sở can thiệp.
- Ch.401: Đạo sĩ dùng phất trần, bùa lửa, bùa sấm rồi Càn Khôn Hồ của Long Hổ Sơn phun nước và kiếm quang; Diệp Sở đáp bằng Ly Hỏa Quyết, Hình Ý Quyền, Huyền Vũ ấn. Hồng Liên chém đứt tay trái đạo sĩ; Diệp Sở đoạt Càn Khôn Hồ, Thôn Thôn chế ngự nó. Đạo sĩ nhận ra Thôn Thôn là Tiên Thiên Hỏa Linh.
- Ch.402: Đạo sĩ đòi lại Càn Khôn Hồ và Tiên Thiên Hỏa Linh, đe Long Hổ Sơn trả thù rồi đi. Diệp Sở nhỏ máu nhận chủ, thấy ruộng thuốc và lá phù lục xanh chứa kiếm ý trong hồ. Đoàn tìm thấy vách đá có trận văn, bước vào Thục Sơn.
- Ch.403: Trong Thục Sơn, các đỉnh nối bằng xích sắt, có ruộng thuốc hoang. Linh khí triều tịch bùng nổ, Diệp Sở bị cuốn vào Long Hồn Hư Không Đỉnh trôi xuống biển ngầm, rồi tới không gian dưới đất có đại đỉnh trắng bạc nhận ba mươi sáu thác nước; hắn nhìn họa tiết hổ, chảy máu mắt.
- Ch.404: Đó là Bạch Hổ Đỉnh; hắn múc linh tuyền vào Càn Khôn Hồ. Xúc tu đen trồi lên bị Bạch Hổ hư ảnh nghiền bằng mưa kiếm; một bàn tay đen có mắt trong lòng bàn tay xuất hiện, bị vạn kiếm bắn thủng, rơi lại vực sâu, Bạch Hổ mờ đi.
- Ch.405: Bạch Hổ ban tạo hóa, nuốt Diệp Sở vào thế giới khác nơi thời gian trôi khác. Nó tu kiếm đạo "một kiếm phá vạn pháp"; Diệp Sở xin học kiếm đạo và nhận thanh tam xích thanh phong nặng trịch. Hắn luyện vung kiếm tới mức "như cánh tay", nghĩ tới Vân Băng Uyển và cha mẹ ruột.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 376-405"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.405: Diệp Sở đang trong không gian của Bạch Hổ, luyện vung thanh tam xích thanh phong, CHƯA ngộ kiếm ý; hạn một tháng cứu Vân Băng Uyển khỏi Dẫn Sát Trận của Đông Hải Hầu đang cận kề (ch.396, 405).
- Kẻ thù lớn: Đông Hải Hầu (giao long tím, cảnh Vương Cấp) bắt Vân Băng Uyển, hợp tác Hùng Ưng đế quốc chế chiến binh gien; Mã Lương (Cương Khí Cảnh cửu trọng, tay sai Chu Vũ) đang tìm Huyền Vũ chân kinh; thanh niên đeo kính đen bí ẩn (nghi Tiểu Bá Vương) đã cứu Diệp Sở và dặn phải đạt Chân Ý Cảnh mới được tìm Đông Hải Hầu (ch.383–396).
- Nhà họ Phong: Phong Khánh Dương và Giang Nam Hổ đều đã chết; Phong Tiêu Tiêu (nhị phòng) bị lừa, Trương Hổ bị đánh; Phong Hành Ngọc thề báo thù, Phong Hành Châu can ngăn; Hàn Mộng Quan là con gái đại phòng nhà họ Phong bị trục xuất (ch.387–395).
- Tình cảm: Hàn Mộng Quan đã ly hôn Khương Hải Vân; Khương Hải Vân bị đánh gãy tứ chi; Khương Quân Dao đã biết "Sở Dạ" và cùng Chu Thanh Thanh trốn đi Thục Sơn; Hồng Vân và Hồng Liên đều đã biết Sở Dạ là Diệp Sở (ch.395–399).
- Diệp Sở hiện là Vạn Hộ Hộ Long Vệ, Cương Khí Cảnh đại viên mãn, có Huyền Vũ ấn, Càn Khôn Hồ, Bạch Hổ Đỉnh, tam xích thanh phong, Thôn Thôn (Tiên Thiên Hỏa Linh) và A Binh (ch.382–405).
- Không đổi cách gọi đã chốt (LƯU Ý 44–53): "Sở Bá Vương" là Diệp Sở; 江南侯 = Giang Nam Hầu (Vân Thiên Cừu) KHÁC 江南虎 = Giang Nam Hổ (Trần Giang Nam); "Phong Khánh Dương" KHÁC "Tào Khánh Dương"; "Huyền Vũ chân kinh" (source cũng gọi Huyền Vũ thần công); "Chân Ý Cảnh"; "linh thể" thường; "Huyền Vũ Đảo" khác "Huyền Vũ Đỉnh" khác "Bạch Hổ Đỉnh".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  rebind ch.405 xong")
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 376-405. tong dong:", len(lines))