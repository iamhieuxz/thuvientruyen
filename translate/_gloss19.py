# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl19.txt")
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

add("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("朱灵儿", 'Chu Linh Nhi (em gái Chu Huyên, Vương tộc Chu gia; source có chỗ chép lẫn 楚灵儿 — cùng một người, bản dịch dùng "Chu Linh Nhi" — ch.316–329)'),
    ("韩山", 'Hàn Sơn (vệ sĩ cửu phẩm Vũ Tôn do "Vũ ca" phái theo bảo vệ Chu Linh Nhi — ch.316–329)'),
    ("秦元霸", 'Tần Nguyên Bá (chi chủ Thanh Bang, bán bộ Cương Khí Cảnh, cha ruột của Tần Như Ngọc, kẻ chủ mưu dùng con gái làm vật tế — ch.319–341)'),
    ("山本渡边", 'Sơn Bản Độ Biên (cao thủ Ảnh Vũ Môn của Đông Doanh, bán bộ Cương Khí Cảnh, thề trả thù cho Đại Hùng Quân — ch.319–341)'),
    ("伊川美智子", 'Y Xuyên Mỹ Trí Tử (nữ ninja Đông Doanh mạnh nhất nhóm, dùng thông linh thuật triệu Ảnh Quỷ — ch.330–342)'),
    ("服部团藏", 'Phục Bộ Đoàn Tàng (nhân vật Đông Doanh được nhắc tới, chưa xuất hiện trực tiếp — ch.330)'),
    ("地青真人", 'Địa Thanh chân nhân (nội môn trưởng lão Vũ Đang, Cương Khí Cảnh, dùng Huyết Thương Kiếm và Huyết Linh Đan cấm dược — ch.319–343)'),
    ("玄叶", 'Huyền Diệp (tên thật Trương Tự Nhất, Kim Linh Thể, Hoàng Bảng hạng tám, đệ tử Vũ Đang; bị Đông Doanh bắt — ch.319–336)'),
    ("三剑真人", 'Tam Kiếm chân nhân (đại trưởng lão Vũ Đang, đòi công đạo cho Huyền Diệp — ch.338–339)'),
    ("唐百户", 'Đường bách hộ (bách hộ Hộ Long Vệ phụ trách đưa đoàn ra Huyền Vũ Đảo — ch.320)'),
    ("秦如玉", 'Tần Như Ngọc (con gái bị Tần Nguyên Bá vứt bỏ, thân thể lưỡng tính do Âm Dương Linh Thể bị tổn thương trong thai; bị đưa về làm vật tế, được Diệp Sở cứu — ch.321–333)'),
    ("姬浩明", 'Cơ Hạo Minh (người nhà họ Cơ ở Trung Châu, chỉ bảo vệ Cơ Đức — ch.338)'),
    ("孔东南", 'Khổng Đông Nam (vạn hộ Hộ Long Vệ dẫn đoàn ra Huyền Vũ Đảo — ch.316–339)'),
    ("陈天南", 'Trần Thiên Nam (thiếu tướng chiến khu Đông Bộ, chỉ huy công phá truyền tống trận pháp — ch.339)'),
    ("龟老祖", 'Quy lão tổ (cự quy tu luyện lâu năm dưới hồ trên Huyền Vũ Đảo, tặng Diệp Sở một thạch đản phù văn — ch.335)'),
])

add("## ══════ ĐỊA DANH", [
    ("影武门", 'Ảnh Vũ Môn (tông môn ninja Đông Doanh, phe của Sơn Bản Độ Biên — ch.319–330)'),
    ("镇魔渊", 'Trấn Ma Uyên (nơi đặt Huyền Vũ Đỉnh trong tiểu thế giới, có thần hồn đỉnh canh giữ — ch.330)'),
    ("小世界", 'tiểu thế giới (bí cảnh bên trong Huyền Vũ Đảo, chứa di tích thượng cổ tông môn và dược viên — ch.327–340)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("黄金葵", 'Hoàng Kim Quỳ (linh thực canh bởi Ngân Bối Ngô Công, Diệp Sở luyện hóa khiến da chuyển màu đồng — ch.323–326)'),
    ("银背蜈蚣", 'Ngân Bối Ngô Công (con rết lưng bạc nghìn chân canh Hoàng Kim Quỳ, bị Diệp Sở giết — ch.323)'),
    ("翡翠藓", 'Phỉ Thúy Tiển (loại rêu quý làm chậm lão hóa, lấy từ đảo yêu ngạc — ch.333)'),
    ("离火诀", 'Ly Hỏa Quyết (công pháp khống hỏa ghi trong ngọc giản ở ngoại môn truyền công các — ch.340–341)'),
    ("忠贞纹", 'Trung Trinh Văn (còn gọi 忠贞印 — Trung Trinh Ấn; vu thuật Vu tộc trong Đại Vu Thiên Kinh khiến người bị in chỉ chung thủy với người thi thuật — ch.345)'),
    ("玄武真水", 'Huyền Vũ Chân Thủy (thần thủy bạn sinh của Huyền Vũ, thứ duy nhất tẩy được Trung Trinh Văn theo Thôn Thôn — ch.345)'),
    ("血灵丹", 'Huyết Linh Đan (cấm dược của Vũ Đang, Địa Thanh uống để tăng chiến lực — ch.337)'),
    ("军体拳", 'Quân Thể Quyền (bộ quyền của quân đội, đội trưởng thân vệ đội dùng — ch.328–329)'),
    ("血煞拳", 'Huyết Sát Quyền (quyền pháp dùng huyết khí, bị Thanh Sắc Thần Long của Diệp Sở phá — ch.328–329)'),
    ("影鬼", 'Ảnh Quỷ (linh thể do Y Xuyên Mỹ Trí Tử triệu bằng thông linh thuật, không sợ Chu Tước Thần Hỏa, bị Oán Long Khí nuốt — ch.341–342)'),
    ("九色战矛", 'cửu sắc chiến mâu (binh khí Tư Đồ Tĩnh dùng sau khi huyết mạch giác tỉnh — ch.343)'),
    ("金灵体", 'Kim Linh Thể (thể chất đặc biệt của Huyền Diệp/Trương Tự Nhất — ch.324)'),
    ("阴阳灵体", 'Âm Dương Linh Thể (thể chất của Tần Như Ngọc; bị tổn thương trong thai nên thành "ngụy Âm Dương Linh Thể", khiến thân thể lưỡng tính — ch.327)'),
])

BLOCK = """### Đã xảy ra — chương 316–345:
- Ch.316: Diệp Sở thăm Hàn Mộng Quan, giấu việc đi Đông Hải; bà lo Khương Quân Dao chưa tỉnh. Hắn hóa Sở Bá Vương quay lại, biết Khương Hải Vân đã trộm công thức giả, dặn bà chớ tự hành động. Vân Băng Uyển nhận lời đi Huyền Vũ Đảo. Chu Huyên đón em Chu Linh Nhi và vệ sĩ Hàn Sơn do "Vũ ca" phái; đội Khổng Đông Nam đi trước.
- Ch.317: Diệp Tiềm — 16–17 tuổi, thất phẩm đỉnh phong Vũ Tôn — tới nhà họ Vân khiêu chiến. Diệp Sở đánh bằng Ưng Trảo Công, Hổ hình, Long Quyền kèm Chu Tước Thần Hỏa; đối thủ đỡ bằng Kim Cương Quyền tạo Kim Thân Phật Đà, Sư Hầu Quyền, Sư Tử Hầu nhưng hao khí cực nhanh.
- Ch.318: Diệp Sở suýt phá Kim Thân Phật Đà; Diệp Tiềm bỏ chạy bằng thân pháp quỷ dị, trúng một quyền lửa rồi biến mất. Ở sân bay, Bạch Hạc chân nhân bao máy bay, Đỗ Linh Nhi đẹp hơn hẳn. Hàn Sơn ra tay bị đẩy lùi; Chu Huyên tiết lộ Diệp Sở là Thí Vạn Hộ. Đỗ Linh Nhi nói Chu Huyên đẹp nhờ Trú Nhan Đan của hắn.
- Ch.319: Tại Thanh Bang, Tần Nguyên Bá bàn với Sơn Bản Độ Biên của Ảnh Vũ Môn về vật tế; nhà họ Viên không mắc bẫy nên hắn quyết hy sinh con gái Tần Như Ngọc. Sơn Bản Độ Biên thề trả thù cho Đại Hùng Quân. Bên Vũ Đang, Huyền Diệp — cửu phẩm Vũ Tôn, Hoàng Bảng hạng tám — buộc Diệp Sở tự chặt một tay vì Chân Vũ Tông; Địa Thanh chân nhân can ngăn.
- Ch.320: Huyền Diệp rút. Chu Huyên giải thích nội môn/ngoại môn của Vũ Đang; Đường bách hộ đưa đoàn đi thuyền. Sau một đêm chờ bão, thuyền vào bão cương khí; Diệp Sở triệu Long Hồn Hư Không Đỉnh.
- Ch.321: Hắn thu cả đoàn vào đỉnh nhưng bị sóng cuốn xuống biển, đỉnh thất lạc; tỉnh trong hang, được Tần Như Ngọc — người lưỡng tính — cứu, băng bó. Hắn đạt bán bộ Cương Khí Cảnh nhưng chưa chuyển hết chân khí. Sáng sau nàng mất tích; hắn thấy nàng bị Thanh Bang vây, cầm đầu là gã nho nhã từng đánh úp mình.
- Ch.322: Gã nho nhã đe giết em trai nàng là A Trương. Diệp Sở dùng cương khí phong nhận giết ba cao thủ, chém đôi một võ sĩ Đông Doanh, chặt đầu gã nho nhã; một tên Đông Doanh trốn bằng độn thuật. Tần Như Ngọc kể mình là con gái bị Tần Nguyên Bá vứt bỏ, nay bị đưa về làm vật tế.
- Ch.323: Nhiều ngày tìm Vân Băng Uyển bất thành; Diệp Sở thấy dấu trận pháp dưới đất, đoán là di tích thượng cổ tông môn. Hắn giết Ngân Bối Ngô Công canh Hoàng Kim Quỳ. Huyền Diệp dẫn đệ tử Vũ Đang tới đuổi hắn để chiếm Hoàng Kim Quỳ; hắn từ chối.
- Ch.324: Tần Nguyên Bá và Sơn Bản Độ Biên — đều bán bộ Cương Khí Cảnh — cùng bốn người Đông Doanh tới; Tần Nguyên Bá đe giết mẹ nuôi và em trai Tần Như Ngọc, nhận ra Diệp Sở là kẻ mang long khí ở Giang Đô. Hắn gọi tên thật của Huyền Diệp là Trương Tự Nhất, Kim Linh Thể. Kiếm của Huyền Diệp không phá nổi thân thể máu tím của Tần Nguyên Bá nhưng vẫn đâm thủng vai trái; Diệp Sở ngửi thấy khí tức yêu tộc.
- Ch.325: Tần Nguyên Bá dùng bí thuật máu rồi Bá Quyền; Sơn Bản Độ Biên nhập cuộc khiến Huyền Diệp trọng thương. Diệp Sở ra tay, kẹp võ sĩ đao bằng hai ngón, đánh Hình Ý Quyền; Long Quyền phá Bá Quyền, Vu Khôi Thuật điều khiển đao của Sơn Bản Độ Biên đâm chủ, tiếp đó Ưng Kích Trường Không.
- Ch.326: Sơn Bản Độ Biên trốn bằng Ảnh Độn Thuật, Tần Nguyên Bá cũng chạy; Diệp Sở giết hết tay sai Thanh Bang, mỉa mai Huyền Diệp khiến hắn bỏ đi. Hắn luyện hóa Hoàng Kim Quỳ hai ngày, da chuyển màu đồng, rồi giết một thanh sư tử gần Cương Khí Cảnh. Lý Huyền Đức xuất hiện.
- Ch.327: Lý Huyền Đức đổi thông tin: sâu trong đảo có tiểu thế giới chứa di tích thượng cổ, dược viên và công pháp, xin dẫn đường. Lão xem tay Tần Như Ngọc: nàng vốn là Âm Dương Linh Thể, bị tổn thương trong thai nên thành ngụy Âm Dương Linh Thể. Hai ngày sau, Diệp Sở cảm ứng được đỉnh, thấy Chu Linh Nhi, Hàn Sơn và nhóm người đang đánh ban lan cự mãng; một gã vác thanh đồng đỉnh nứt.
- Ch.328: Chu Linh Nhi không chịu nói Chu Huyên ở đâu; đội trưởng thân vệ đội của Trấn Tây đại tướng quân — Cương Khí Cảnh — đòi đỉnh. Hắn hứa trả đỉnh nếu Diệp Sở thắng Thiết Chùy; Diệp Sở một quyền hất Thiết Chùy xuống hồ, đá bay một tên nữa, đấu hàng chục chiêu buộc đội trưởng dùng Quân Thể Quyền và Huyết Sát Quyền.
- Ch.329: Thanh sắc thần long của Diệp Sở phá Huyết Sát Quyền, đội trưởng phun máu. Hắn thu lại Long Hồn Hư Không Đỉnh, tát đám tay chân, Hàn Sơn và Chu Linh Nhi, cướp sạch dược liệu. Thôn Thôn trong đỉnh lộ diện là kẻ trộm thuốc. Nhóm đội trưởng được ninja Đông Doanh chào hợp tác, nhắc tới cổ kinh, và đồng ý.
- Ch.330: Tần Nguyên Bá, Sơn Bản Độ Biên và Y Xuyên Mỹ Trí Tử bị lựu đạn làm bị thương, quyết mở sớm tiểu thế giới để dụ và tiêu diệt tất cả; Phục Bộ Đoàn Tàng được nhắc. Trong tiểu thế giới, một nam tử tóc tím uống một giọt thanh sắc huyết dịch, biến thành quái vật tám đầu trước Huyền Vũ Đỉnh ở Trấn Ma Uyên; thần hồn đỉnh nói "kẻ dám xông vào Trấn Ma Uyên, chết". Tin lan ra; nhóm Diệp Sở gặp một gã mập bị yêu ngạc đuổi.
- Ch.331: Diệp Sở cầm chân yêu ngạc bằng dị hỏa để Lý Huyền Đức đưa Tần Như Ngọc đi; gã mập bắn đại bác rồi đưa chàng siêu hỏa tiễn giá hàng trăm triệu, giết phần lớn bầy, nhưng vai chàng bị thương. Gã tên Cơ Đức; Lý Huyền Đức xưng Huyền Đức Chân Quân. Cơ Đức bị đuổi vì trộm trứng ngạc nấu ăn.
- Ch.332: Cơ Đức nhập nhóm, có trữ vật giới; Lý Huyền Đức khoe quan hệ nhà họ Cơ ở Trung Châu và nhắc Cơ Thiên Nguyên — ông hai của Cơ Đức — khiến hắn nổi giận. Cả nhóm đi khoái đĩnh tới đảo yêu ngạc; bên kia hồ chính là trung tâm đảo.
- Ch.333: Họ dụ yêu ngạc ra, bắn chết con lớn bằng hỏa tiễn và lấy Phỉ Thúy Tiển. Sau nhiều ngày càn quét, họ tới đảo lớn có yêu quy mai cứng; trong thung lũng có hồ dược liệu, họ gặp Khương Quân Hồng và Khương Tiếu Tiếu của nhà họ Khương ở Trung Châu đang bị cự quy mai phù văn đuổi; Cơ Đức cứu.
- Ch.334: Cự quy không ra khỏi thung lũng vì trận pháp; Khương Quân Hồng và Cơ Đức đấu khẩu, lộ việc Cơ Đức có hôn ước với đường tỷ của Khương Quân Hồng. Vào trong, Long Hồn Hư Không Đỉnh rung lên; cự quy phong tỏa họ bằng kim sắc quang tráo rồi thốt tiếng người: "Long Hồn Hư Không Đỉnh!"
- Ch.335: Lão quy dẫn họ xuống đáy hồ tới Bát Quái Đài gặp Quy lão tổ; lão tặng Diệp Sở một thạch đản đầy phù văn, cộng hưởng với đỉnh, nói chàng mang nhiều nhân quả và nó sẽ giúp về sau; chỉ được hái thuốc phía đông. Lên bờ, họ gặp Vũ Đang; một đệ tử vu Diệp Sở khiến Huyền Diệp bị Đông Doanh bắt.
- Ch.336: Cơ Đức nói Đông Doanh cũng định bắt mình; Địa Thanh — Cương Khí Cảnh — đòi cơ duyên dưới hồ rồi ra tay, kiếm không phá nổi da đồng của Diệp Sở. Lão dùng Huyết Thương Kiếm; Diệp Sở cố ý chịu đòn để cảm ngộ cương khí hòng đột phá.
- Ch.337: Diệp Sở đột phá Cương Khí Cảnh, một chưởng đánh gãy thế kiếm, làm Địa Thanh bị thương. Địa Thanh uống Huyết Linh Đan; Diệp Sở đáp bằng siêu hỏa tiễn, thổi lão ra khỏi thung lũng. Cơ Đức cưỡng đoạt dược liệu và trữ vật giới.
- Ch.338: Địa Thanh nộp trữ vật giới. Bên kia hồ, hai ngọn núi thành thiên môn che cửa tiểu thế giới; Hộ Long Vệ, quân đội, Nga Mi, Vũ Đang, Vu Cổ Giáo, Cơ gia, Khương gia tụ tập. Tam Kiếm chân nhân đòi công đạo; Cơ Hạo Minh chỉ bảo vệ Cơ Đức; Khương Chính Hải từ chối giúp; Khương huynh muội bị phạt viết kiểm điểm.
- Ch.339: Chu Huyên viện dẫn chức Thí Vạn Hộ và thế lực Vương tộc Chu gia, Tam Kiếm đành rút. Khổng Đông Nam nhờ Diệp Sở phá truyền tống trận pháp; Trần Thiên Nam — thiếu tướng chiến khu Đông Bộ — chỉ huy công phá. Trận vỡ, xoáy nước hút tất cả, chia cắt từng người. Nhóm Đông Doanh cùng Hàn Sơn theo vào; Y Xuyên Mỹ Trí Tử nói trận đã bị động tay nên ai ra đòn đều mang lạc ấn — "giờ săn giết" bắt đầu.
- Ch.340: Diệp Sở rơi vào biển có núi đảo ngược — di tích thượng cổ tông môn; tại ngoại môn truyền công các, hắn tìm được ngọc giản ghi Ly Hỏa Quyết nhờ Thôn Thôn, và luyện khống hỏa. Ra ngoài, hắn bị Đông Doanh, Thanh Bang và nhóm đội trưởng vây.
- Ch.341: Diệp Sở tát bay Tần Nguyên Bá và Sơn Bản Độ Biên; dùng Ly Hỏa Quyết tạo quyền lửa, cung lửa nhưng không bắt kịp tốc độ Y Xuyên Mỹ Trí Tử. Hắn bắn siêu hỏa tiễn làm sập cổ điện. Y Xuyên Mỹ Trí Tử dùng thông linh thuật "Ảnh Quỷ giáng lâm" triệu Ảnh Quỷ — không sợ Chu Tước Thần Hỏa, tái sinh, liên tục cứa trọng thương chàng.
- Ch.342: Thôn Thôn thúc chàng dùng Oán Long Khí; tử hắc oán long hiện ra nuốt trọn Ảnh Quỷ. Y Xuyên Mỹ Trí Tử phun máu, trốn cùng Sơn Bản Độ Biên và Tần Nguyên Bá; đội trưởng trốn bằng ngọc phù. Diệp Sở kéo oán long về nhờ Thôn Thôn, kiệt sức. Địa Thanh và Huyền Lâm xuất hiện.
- Ch.343: Người tới phá tan kiếm khí là Tư Đồ Tĩnh, nay đã Cương Khí Cảnh; nàng hạ Huyền Lâm một chiêu, thắng Địa Thanh bằng cương khí độc xanh thẫm và cửu sắc chiến mâu, nói sẽ tự tay giết Diệp Sở. Thay vào đó nàng ép chàng uống thuốc phong khí hải và thuốc kích dục, trói lại, cho sơn trư và dã cẩu uống thuốc rồi bỏ đi với câu "hưởng thụ cho tốt".
- Ch.344: Nàng chỉ quay video cảnh chàng hoảng loạn; ra điều kiện chàng làm nam sủng, chàng vì thuốc mà đồng ý. Nàng vẽ phù văn bằng máu lên bụng cả hai rồi quan hệ, bảo chàng gọi mình là U Lan. Phù văn phát sáng khiến chàng say mê bất thường.
- Ch.345: U Lan giải thích đó là Trung Trinh Văn, vu thuật Vu tộc trong Đại Vu Thiên Kinh khiến chàng chỉ chung thủy với nàng; mỗi lần song tu lại mạnh thêm. Mục đích: giữ thiên tài cho Vu Cổ Giáo và giúp huyết mạch nàng thức tỉnh hoàn toàn. Trong khí hải, cửu thải phượng hoàng xoa dịu oán long; Thôn Thôn nói chỉ Huyền Vũ Chân Thủy mới tẩy được, nhưng cho là thứ không thể có.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 316-345"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.345: Diệp Sở bị Trung Trinh Văn (U Lan in bằng máu) trói buộc phải chung thủy với nàng; Thôn Thôn nói chỉ Huyền Vũ Chân Thủy mới tẩy được nhưng cho là không thể có. Hắn đang ở trong tiểu thế giới của Huyền Vũ Đảo, đã đột phá Cương Khí Cảnh (ch.337, 344–345).
- U Lan (Tư Đồ Tĩnh) đã đạt Cương Khí Cảnh, thắng cả Địa Thanh chân nhân; ả ép Diệp Sở làm nam sủng để giữ thiên tài cho Vu Cổ Giáo và giúp huyết mạch mình thức tỉnh hoàn toàn — ả vẫn đang ở trong tiểu thế giới (ch.343–345).
- Kẻ thù còn sống trong tiểu thế giới: Tần Nguyên Bá, Sơn Bản Độ Biên, Y Xuyên Mỹ Trí Tử (bị thương, đã trốn), đội trưởng thân vệ đội Trấn Tây, nhóm ninja Đông Doanh; Thôn Thôn đang giữ Oán Long Khí đã nuốt Ảnh Quỷ (ch.340–343).
- Bên ngoài: 江南虎 Trần Giang Nam và Hắc Lang chờ Diệp Sở vắng nhà để chiếm Giang Đô; Giang Nam Hầu Vân Thiên Cừu truy sát vì Vân Xung chết; nhà họ Khương ở Trung Châu (Khương Quân Hồng, Khương Tiếu Tiếu, Khương Chính Hải) và nhà họ Cơ ở Trung Châu (Cơ Đức, Cơ Hạo Minh, Cơ Thiên Nguyên) vừa xuất hiện (ch.316–338).
- Trong tay Diệp Sở: Long Hồn Hư Không Đỉnh (đã lấy lại), thạch đản phù văn của Quy lão tổ, Ly Hỏa Quyết, Hoàng Kim Quỳ đã luyện (da màu đồng), Trú Nhan Đan, A Binh và Thôn Thôn. Vân Băng Uyển vẫn thất lạc trong tiểu thế giới (ch.320–345).
- Quan hệ đã lộ: Hàn Mộng Quan biết hắn dưới thân phận Sở Bá Vương/Chu đổng nhưng chưa biết là Diệp Sở; Tần Nguyên Bá biết hắn mang long khí ở Giang Đô; công khai thân phận Thí Vạn Hộ trước Hộ Long Vệ, quân đội, Vũ Đang, Nga Mi (ch.316–339).
- Không đổi cách gọi đã chốt (LƯU Ý 44–52): "Sở Bá Vương" là Diệp Sở; 江南侯 = Giang Nam Hầu (Vân Thiên Cừu) KHÁC 江南虎 = Giang Nam Hổ (Trần Giang Nam); "Vũ Tôn"/"nữ Vũ Tôn"; "Chân Vũ Tông" cho cả 真武宗 lẫn 真武门; "Thệ Tâm Cổ"; "Tư Đồ Tĩnh = U Lan"; "Khương Quân Hồng ≠ Khương Quân Long"; "Diên Thọ Hoàn"; "tập đoàn Bách Dược"; "Đông Hải Hầu"; "Nhẫn Giả"; "Huyền Vũ Đảo" (khác "Huyền Vũ Đỉnh").
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc rebind theo ch.345 (%d dong)" % len(NEW.strip().split("\n")))
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 316-345. tong dong:", len(lines))