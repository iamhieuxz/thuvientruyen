# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl22.txt")
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
    ("唐门", 'Đường Môn (môn phái ám khí/độc ở Thục Địa, có một Thục Sơn Lệnh — ch.406–415)'),
    ("唐月", 'Đường Nguyệt (nữ đệ tử Đường Môn, bị Khương Quân Hồng giết — ch.407–408)'),
    ("唐山", 'Đường Sơn (phó môn chủ Đường Môn, đòi lại ám khí rồi phải xin lỗi Cơ Hạo Minh — ch.415–416)'),
    ("十三姑", 'Thập Tam Cô (bà lão dẫn đầu đội nhà họ Khương ở Trung Châu — ch.408)'),
    ("姜君元", 'Khương Quân Nguyên (tùy tùng của Khương Quân Thiên, bị Khương Quân Hồng bẻ gãy tay — ch.411)'),
    ("姜君贤", 'Khương Quân Hiền (tùy tùng của Khương Quân Thiên, bị hạ — ch.411)'),
    ("四海真人", 'Tứ Hải chân nhân (chưởng giáo nội môn Võ Đang, mang một Thục Sơn Lệnh tới — ch.414–425)'),
    ("姬大德", 'Cơ Đại Đức (anh của Cơ Đức, thiên tài nhà họ Cơ — ch.417)'),
    ("文老", 'Văn lão (lão giả Hộ Long Vệ đọc cổ tự trên cửa Thục Sơn — ch.417)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("凰血果", 'Hoàng Huyết Quả (linh quả giúp Khương Quân Dao thức tỉnh Chân Hoàng Thể — ch.406)'),
    ("真凰体", 'Chân Hoàng Thể (thể chất đặc biệt của Khương Quân Dao, đối ứng Chân Long Thể — ch.406–412)'),
    ("紫云焰", 'Tử Vân Diễm (dị hỏa được ban cho Khương Quân Thiên — ch.411)'),
    ("剑经", 'Kiếm Kinh (bí kíp kiếm đạo của Thục Sơn mà Mã Lương truy tìm — ch.410)'),
    ("剑胚", 'Kiếm Phôi (phôi kiếm từ thiên ngoại trong quan 9 Thục Sơn, chứa cổ kinh, Thục Sơn không rèn nổi — ch.421–432)'),
    ("蜀山九剑", 'Thục Sơn Cửu Kiếm (chín thanh kiếm ở quan 8, mỗi người chỉ được lấy một — ch.420–421)'),
    ("百变甲", 'Bách Biến Giáp (giáp Bạch Hổ bắt Diệp Sở mặc, chỉ cởi được khi thắng người tới sau — ch.421–430)'),
    ("拔剑术", 'Bạt Kiếm Thuật (kiếm kỹ Diệp Tiềm nhận sau khi thắng khôi lôi — ch.417)'),
    ("惊雷剑", 'Kinh Lôi Kiếm (kiếm Cơ Đức nhận được — ch.418)'),
    ("人皇拳", 'Nhân Hoàng Quyền (quyền pháp chỉ huyết mạch Hoàng tộc Đại Hạ luyện được; Diệp Tiềm đổi lấy Hám Sơn Quyền — ch.419–432)'),
    ("撼山拳", 'Hám Sơn Quyền (quyền pháp Diệp Sở đổi cho Diệp Tiềm — ch.429)'),
    ("庚金之气", 'Canh Kim Chi Khí (khí kim loại Bạch Hổ tặng Diệp Sở — ch.431–435)'),
    ("白虎杀经", 'Bạch Hổ Sát Kinh (kinh sát phạt Bạch Hổ truyền cho Diệp Sở — ch.431)'),
    ("红莲业火", 'Hồng Liên Nghiệp Hỏa (loại hỏa của Hồng Liên chân nhân, nàng là chuyển thế của một tia linh vận loại hỏa này — ch.425, 435)'),
    ("焚天诀", 'Phần Thiên Quyết (quyết pháp Diệp Sở tặng Hồng Liên — ch.425)'),
    ("武王", 'Vũ Vương (cách gọi khác của Chân Ý Cảnh — ch.431)'),
])

block = """54. Source ch.406–435: 姜君洪 có chỗ chép 姜君红 (cùng một người — giữ "Khương Quân Hồng"); 皇甫师月 (ch.435) là gõ nhầm của 皇甫诗月; 青龙鼎 = Long Hồn Hư Không Đỉnh (cùng một đỉnh, khí linh là Thanh Long); 安小舞 nay lộ là đệ tử Vu Cổ Giáo (ch.420), khớp vụ thảm sát nhà họ Lâm ch.163."""
if not any(l.strip() == block for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("## ══════ VĂN PHONG"):
            lines[i:i] = block.split("\n") + ["", ""]; print("  + LƯU Ý 54"); break

BLOCK = """### Đã xảy ra — chương 406–435:
- Ch.406: Hồng Liên dẫn Nga Mi vào sâu Thục Sơn; Cơ Đức, Khương Quân Hồng, Khương Tiếu Tiếu lạc vào trận truyền tống tới nội vi. Khương Quân Dao ăn Hoàng Huyết Quả, thức tỉnh Chân Hoàng Thể gây dị tượng hỏa phượng; Đường Môn kéo tới đòi cơ duyên.
- Ch.407: Đường Nguyệt cùng sư huynh và tam thúc đánh Chu Thanh Thanh bị thương; Cơ Đức tới thổi bay ám khí độc, khinh Đường Môn, tam thúc nổi giận ra tay.
- Ch.408: Cơ Đức dụ tam thúc đuổi rồi nổ chết; Khương Tiếu Tiếu đánh Đường Nguyệt sưng mặt; Khương Quân Hồng giết cả ba người Đường Môn. Khương Quân Dao đột phá Vũ Tôn; Thập Tam Cô dẫn nhà họ Khương tới, cử Khương Quân Thiên đi tìm Chân Hoàng Thể.
- Ch.409: Khương Quân Hồng kể tổ tiên nhà họ Khương từng cưới Chân Hoàng, tộc là thế gia nghìn năm ở Trung Châu; Cơ Đức lừa hai nữ rằng sư phụ tìm cho Khương Quân Dao một Đại Vũ Tôn. Diệp Sở trong Bạch Hổ Đỉnh luyện vung kiếm hai năm rưỡi, chuyển sang đâm xuyên trụ đá.
- Ch.410: Mã Lương lùng Kiếm Kinh vào hạch tâm Thục Sơn. Nhóm Khương Quân Dao gặp Linh Nhãn đầy Xích Kim Huyết Liên; Cơ Đức và Khương Quân Hồng nhờ đó đột phá Cương Khí Cảnh, rồi Khương Quân Thiên xuất hiện quát hỏi.
- Ch.411: Khương Quân Hồng bẻ gãy tay Khương Quân Nguyên, hạ Khương Quân Hiền rồi đánh Khương Quân Thiên dùng Tử Vân Diễm. Cơ Đức bắn hỏa tiễn; Khương Quân Thiên sống nhờ thanh đồng thuẫn.
- Ch.412: Khương Quân Dao hiện Chân Hoàng Thể khiến Khương Quân Thiên bỏ đi báo tin. Linh Nhãn phun linh lực triều tịch do chín đỉnh hội tụ; Diệp Sở đâm thủng trụ sau năm năm rưỡi, bắt đầu luyện kiếm kỹ.
- Ch.413: Bạch Hổ đưa Diệp Sở tới cửa đồng lớn khóa bằng chín Thục Sơn Lệnh; qua chín quan là thành Kiếm Ý. Khôi lôi đen-vàng nâng theo cảnh giới đối thủ, bị hắn một kiếm chém đôi; Bạch Hổ không cho lấy bảo vật, bảo để cho người sau.
- Ch.414: Cơ Đức bắn hỏa tiễn không phá nổi cửa, cần đủ chín Thục Sơn Lệnh (nhà Cơ hai, Khương một, Nga Mi một). Tứ Hải chân nhân tới với một lệnh; đệ tử Võ Đang chế giễu, Cơ Đức xưng là người nhà họ Cơ.
- Ch.415: Tứ Hải kể Đường Môn, Vu Cổ Giáo, Long Hổ Sơn, Hộ Long Vệ mỗi bên một lệnh, còn thiếu một. Phó môn chủ Đường Sơn tới đòi lại ám khí; Tứ Hải cản vì nể hai nhà. Cơ Đức ăn vạ khi trưởng bối vừa tới.
- Ch.416: Cơ Hạo Minh buộc Đường Sơn xin lỗi và đền bù, mắng Cơ Đức vì đánh trọng thương Khương Quân Thiên. Bà lão nhà họ Khương mời Khương Quân Dao về tộc; Hồng Liên nói người đính hôn đã tự rút, Khương Quân Dao từ chối.
- Ch.417: Chín lệnh mở cửa; Văn lão Hộ Long Vệ dịch cổ tự: thắng khôi lôi để lấy Kiếm Kỹ. Diệp Tiềm — 16–17 tuổi đã Cương Khí Cảnh — dùng Kim Cương Quyền thắng sau hơn trăm hiệp, nhận Bạt Kiếm Thuật; Cơ Đức thấy hắn hao hao Diệp Sở.
- Ch.418: Cơ Đức nhận Kinh Lôi Kiếm; phần lớn người khác thất bại. Diệp Sở qua quan 1–3 dễ, quan 4 bị đâm thủng, quan 5 làm hắn bị thương nhưng nhập cảnh giới ngộ Kiếm Ý rồi chém đôi; quan 6 là khôi lôi xanh-vàng.
- Ch.419: Khương Quân Dao hạ khôi lôi vàng; quan 5 là trận pháp. Diệp Tiềm thi triển Nhân Hoàng Quyền, phá khôi lôi lục kim, lộ thân phận Hoàng tộc Đại Hạ. Diệp Sở hạ khôi lôi lam kim, xác nhận đã ngộ Kiếm Ý; quan 8 có tám thanh kiếm.
- Ch.420: Diệp Sở bị khôi lôi tím-vàng đánh trọng thương liên tục mà vẫn đánh. Qua quan 6 chỉ còn mười người, có Hồng Liên, U Lan, Diệp Tiềm, Cơ Đại Đức, Mã Lương; Hồng Liên giết khôi lôi lam kim bằng Phần Tịch, U Lan dùng Đại Vu Thiên Kinh khống chế khôi lôi. Quan 8 là Thục Sơn Cửu Kiếm.
- Ch.421: Hồng Liên hạ khôi lôi tím-vàng bằng Thất Tinh Phần Diệt và Hoa Mãn Thiên, chọn Xích Liên Kiếm; mỗi người chỉ được một thanh. Diệp Sở tới quan 9, thấy Kiếm Phôi; Bạch Hổ bắt mặc Bách Biến Giáp, chỉ cởi được khi thắng người đến sau.
- Ch.422: Bạch Hổ nói giáp sẽ nhận chủ sau khi thắng; bốn kiếm còn lại bay vào quan 9. Chỉ Hồng Liên, Tứ Hải, U Lan, Mã Lương đủ tư cách khiêu chiến; bốc thăm ra thứ tự U Lan, Tứ Hải, Hồng Liên, Mã Lương. Diệp Sở giả khôi lôi, hứa thưởng theo chiến tích.
- Ch.423: U Lan dùng phù xích hút chân khí, kiếm độc và Đại Vu Thiên Nhãn định thân. Diệp Sở dùng Chu Tước Thần Hỏa phá phù, đoạt kiếm, ôm giữ nàng, đòi gọi "hảo ca ca".
- Ch.424: U Lan nhục nhã gọi "hảo ca ca" hai lần; hắn thả nàng, nhận chủ nhẫn trữ vật, tặng nàng một bộ nhuyễn giáp. Tứ Hải thi triển Chân Vũ Kiếm Pháp · Bách Biến Thiên Huyễn Kiếm.
- Ch.425: Diệp Sở đỡ trọn đòn của Tứ Hải, chỉ bị vài vết xước; Tứ Hải nhận thua. Hồng Liên dùng Cửu Tinh Phần Thiên — Khương Chính Hải nhận ra Hồng Liên Nghiệp Hỏa; hắn vô sự nhờ Chu Tước Thần Hỏa và Huyền Vũ Chân Thủy, rồi tặng nàng Phần Thiên Quyết và gọi Mã Lương.
- Ch.426: Mã Lương dùng trường thương chứa Vô Địch Thương Ý của Đại tướng quân; Chu Linh Nhi nhận ra khí tức "Vũ ca", Chu Huyên nghi Chu Vũ phái hắn. Diệp Sở bị xuyên ngực, gãy xương, vẫn lao lên chụp mũi thương.
- Ch.427: Diệp Sở đột phá Chân Ý Cảnh giữa trận, ném Mã Lương; Hồng Liên khẳng định hắn là người. Hắn chém đứt hai chân Mã Lương, bị Chu Linh Nhi ngăn, Chu Huyên xin lỗi kéo đi; hắn thì thầm "nỗi nhục ngày đó, hôm nay trả" rồi bẻ cổ giết Mã Lương.
- Ch.428: Khương Quân Dao nhận hai trong bốn kiếm còn lại, tặng Chu Thanh Thanh một thanh; Cơ Đức quỳ gọi "hảo ca ca" để đổi lấy kiếm trong nhẫn Mã Lương. Diệp Tiềm đấu quyền với hắn, Nhân Hoàng Quyền làm cả hai cùng văng; Diệp Sở đòi học quyền ấy.
- Ch.429: Diệp Tiềm đổi Nhân Hoàng Quyền (viết bằng máu) lấy Hám Sơn Quyền. Diệp Sở lấy Kiếm Phôi; Bạch Hổ nói kiếm phôi từ thiên ngoại, chứa cổ kinh, Thục Sơn không rèn nổi. Các thế lực rời đi, chỉ Nga Mi ở lại; Hồng Liên hỏi "còn giả vờ sao?".
- Ch.430: Hồng Liên nói nhận ra khí tức Chu Tước Thần Hỏa; Diệp Sở nhỏ máu nhận chủ Bách Biến Giáp, lộ mặt trước Nga Mi, Khương Quân Dao, Chu Thanh Thanh, anh em nhà họ Khương. Hồng Liên gọi hắn "Sở Dạ"; Chu Thanh Thanh nhận ra Sở Dạ chính là Diệp Sở.
- Ch.431: Diệp Sở giấu Bạch Hổ; Bạch Hổ tặng Canh Kim Chi Khí, Bạch Hổ Sát Kinh và linh tuyền vào Càn Khôn Hồ. Long Hồn Hư Không Đỉnh hồi phục nhờ linh tuyền, lộ khí linh là Thanh Long. Ra ngoài, khí hải nở gấp chục lần, cương khí chứa Kiếm Ý; Chân Ý Cảnh còn gọi Vũ Vương.
- Ch.432: Diệp Sở định cứu Vân Băng Uyển rồi lên đế đô tìm thân thế. Thôn Thôn đọc được vài chữ trên kiếm phôi, ở lại Càn Khôn Hồ tránh Oán Long; hắn luyện thành Nhân Hoàng Quyền ngay lần đầu. Ra khỏi Thục Sơn, A Binh đạt Cương Khí Cảnh đỉnh phong nhờ truyền thừa đại yêu Thục Sơn.
- Ch.433: Bà lão nhà họ Khương thuyết phục, Hồng Liên vẫn chặn; Diệp Sở khuyên để Khương Quân Dao đi, hứa nếu nhà họ Khương trở mặt sẽ đích thân đòi người. Khương Quân Dao chọn nửa tháng sau; Hồng Liên cảnh cáo nhà họ Khương rồi về Nga Mi. Chiều tối, hắn nắm tay, ôm eo nàng bên vách núi.
- Ch.434: Hắn hôn nàng nhưng dừng, vì Oán Long Khí chưa phát tác và Chân Hoàng Thể cần để song tu sau; hắn kể chuyện bị nhà họ Diệp đẩy ra nhận tội, nàng xin lỗi. Nửa tháng sau Khương Quân Dao theo nhà họ Khương rời Nga Mi; Diệp Sở về Giang Đô, qua Thần Nông Giá thì Thanh Long đòi ghé thăm Chu Tước.
- Ch.435: Diệp Sở thấy đại trận dưới hồ bị động tay; gặp Chu Tước, bị chê yếu nhưng nhờ Canh Kim Chi Khí và Huyền Vũ Chân Thủy mà được cho nửa bản nguyên thần diễm, cất vào Càn Khôn Hồ chưa luyện. Chu Tước nói Hồng Liên là chuyển thế của một tia linh vận Hồng Liên Nghiệp Hỏa, khuyên song tu, hắn từ chối. Về Giang Đô, Chung San báo có thùng lớn chờ hắn tự mở.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 406-435"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.435: Chung San báo có người lạ gửi một chiếc thùng lớn, dặn chỉ Diệp Sở về tự tay mở — nội dung chưa lộ. Hắn vừa về Giang Đô sau khi rời Thục Sơn (ch.435).
- Diệp Sở đã đạt Chân Ý Cảnh (Vũ Vương), có Kiếm Ý, Bách Biến Giáp, Kiếm Phôi, Canh Kim Chi Khí, Bạch Hổ Sát Kinh, Nhân Hoàng Quyền, nửa bản nguyên thần diễm của Chu Tước; A Binh đạt Cương Khí Cảnh đỉnh phong (ch.427–435).
- Hạn một tháng cứu Vân Băng Uyển khỏi Dẫn Sát Trận của Đông Hải Hầu (đặt từ ch.396) vẫn đang chạy; Vân Băng Uyển còn trong tay Đông Hải Hầu (ch.396–435).
- Khương Quân Dao đã biết Sở Dạ = Diệp Sở, được Hồng Liên và cả Nga Mi công nhận; nàng theo nhà họ Khương về Trung Châu với hẹn nửa tháng, Diệp Sở hứa sẽ đòi người nếu họ trở mặt (ch.430–434).
- Các thế lực mới nổi ở Thục Sơn: Đường Môn (Đường Sơn), nhà họ Khương Trung Châu (Thập Tam Cô, Khương Quân Thiên), nhà họ Cơ (Cơ Hạo Minh, Cơ Đại Đức), Võ Đang (Tứ Hải chân nhân); U Lan đã Cương Khí Cảnh đỉnh phong và bị Diệp Sở làm nhục (ch.406–431).
- Không đổi cách gọi đã chốt (LƯU Ý 44–54): "Sở Bá Vương" là Diệp Sở; "Sở Dạ" cũng là tên giả của hắn; "Khương Quân Hồng" (không phải Khương Quân Long); "Chân Ý Cảnh"/"Vũ Vương"; "Thanh Long" (khí linh đỉnh) KHÁC "Thanh Liên" (người); "Huyền Vũ Đảo" khác "Huyền Vũ Đỉnh" khác "Bạch Hổ Đỉnh".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  rebind ch.435 xong")
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 406-435. tong dong:", len(lines))