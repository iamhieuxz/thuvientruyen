# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl15b.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

BLOCK = """### Đã xảy ra — chương 196–225:
- Ch.196: Diệp Sở nhỏ máu lên tấm da dê, một bóng áo xanh hiện ra múa Long Quyền ba thức; hắn học được võ kỹ cổ này (toàn bộ chín thức, da dê chỉ ghi ba). Oán Long Khí bạo loạn vì tiếng rồng gầm trong tiểu đỉnh. Tin "Diệp đại sư là Vũ Tôn" lan khắp Giang Đô. Tôn Ngữ Nhu mời hắn dự họp báo tập đoàn Bách Dược; tại cửa, Lâm Hào sai Triệu Ngũ đánh gãy tay chân hắn.
- Ch.197: Vương Hạ Niên xông ra đỡ, gọi hắn là "Diệp thần y" nhưng thua Triệu Ngũ — một cao phẩm tông sư. Bạch Hiểu Hiểu dẫn Bạch Lang Hội tới, đấm bay Triệu Ngũ rồi tát Lâm Hào của nhà họ Lâm ở Cô Tô đến hôn mê và đuổi đi. Lý Đầu Trọc dọa Khương Hải Vân cụp đầu. Bạch Hiểu Hiểu ngầm đoán Sở Bá Vương chính là Diệp Sở vì chủ tịch tập đoàn Bách Dược là Tôn Ngữ Nhu.
- Ch.198: Gia Cát Triết Nhã của nhà họ Gia Cát ở Kim Lăng ra đón, cho hắn vào. Vương Hạ Niên và Vương Chính Huyền mỉa mai Khương Phong Niên, Khương Hải Vân; Khương Phong Niên bỏ về. Hội trường tầng tám có bốn đại hào tộc và ba đại cổ tộc Giang Đô; Vân Băng Uyển xuất hiện, Diệp Dật Thần xin lỗi bị từ chối. Diệp Sở chủ động làm quen, nàng đáp "được thôi".
- Ch.199: Diệp Dật Thần tức hộc máu; Tạ Vũ San, Diệp Thiên Thành, Diệp Thiên Trì, Diệp Dật Không bị bẽ mặt, đám đông mắng nhà họ Diệp. Diệp Sở tuyên bố sẽ xóa tên nhà họ Diệp khỏi Giang Đô; Vương Hạ Niên và Bạch Lang Hội xin ra tay đàn áp, nhà họ Diệp bỏ đi. Vương Hạ Niên nghi "Diệp thần y" chính là "Diệp đại sư". Vân Băng Uyển ghen, biết Tôn Ngữ Nhu cũng là người của hắn và khuyên tránh xa Gia Cát Triết Nhã.
- Ch.200: Tôn Ngữ Nhu ra mắt Thập Toàn Đại Bổ Hoàn và Bách Hoa Lộ; Lý Đầu Trọc thử Bách Hoa Lộ, vết thương liền ngay trước mắt khách. Gia Cát Triết Nhã báo sẽ ra mắt Bách Dược Tửu. Tôn Ngữ Nhu mời Hàn Mộng Quan làm tổng giám đốc tập đoàn Bách Dược, Khương Hải Vân mừng rỡ. Khương Quân Long chen vào xin một chức.
- Ch.201: Tôn Ngữ Nhu từ chối Khương Quân Long, nói chỉ có ghế tổng giám đốc. Diệp Sở nếm Bách Dược Tửu làm từ trăm vị thuốc; Vân Băng Uyển đồng ý góp vốn. Hoàng Phủ Thi Nguyệt báo công trường khu Nam Thành liên tiếp xảy ra tai nạn chết người. Hoàng Phủ Kiệt, Hoàng Phủ Kiếm, Hoàng Phủ Dương, Hoàng Phủ Minh dẫn Trương đại sư của Long Hổ Sơn tới, nói nàng xung khắc với khu đất.
- Ch.202: Trương đại sư nói đây là dương cực chi địa, Hoàng Phủ Thi Nguyệt mang âm thể nên phạm xung, đòi đưa nàng về Kim Lăng. Diệp Sở thách: ai tìm ra lỗi phong thủy trước, kẻ thua phải quỳ. Lý Thục Anh dẫn Huyền Đức đạo trưởng Lý Huyền Đức của Mao Sơn tới; Trương đại sư mắng hắn là "nỗi nhục của Mao Sơn", đánh bay và làm nát Ngũ Đế Kiếm.
- Ch.203: Lý Thục Anh cảnh cáo Diệp Sở tránh xa con gái; Lý Huyền Đức gọi hắn là "Thiên Mệnh Yêu Tinh". Cả hai đều nhận ra dương cực chi địa. Diệp Sở khẳng định tai nạn do người làm và tố Trương đại sư dùng bản lĩnh hại người; lão đe dọa hắn "họa từ miệng mà ra".
- Ch.204: Diệp Sở vạch trần Trương đại sư chôn bốn hung khí dính máu theo thế Tứ Tượng Hung Sát. Lão lén triệu một linh hồn thể — bé gái tóc đỏ mặc yếm — nuốt cả bốn món rồi chui vào nhẫn đen. Công nhân đào không thấy gì, Hoàng Phủ Kiệt khẳng định Diệp Sở nói bừa. Trương đại sư đòi hắn quỳ lạy, nếu không sẽ đánh gãy tứ chi và cắt lưỡi.
- Ch.205: Diệp Sở giật nhẫn, thả bé gái, dụ bằng linh đan diệu dược để nó nhả bốn hung khí. Trương đại sư niệm chú hành hạ nó, bị Diệp Sở tát và bóp cổ; lão khai Hoàng Phủ Kiếm trả một trăm triệu, đã nhận mười triệu tiền cọc có tin nhắn làm chứng. Lão ném Tiểu Lôi Phù, Diệp Sở không hề hấn rồi bẻ gãy cổ lão. Bé gái — thực lực không kém đại tông sư — theo hắn; Hoàng Phủ Kiệt gọi thành vệ.
- Ch.206: Hoàng Phủ Kiếm ra điều kiện tha nếu Hoàng Phủ Thi Nguyệt không báo ông nội, nàng từ chối. Thống lĩnh thành vệ quân họ Trần bắt Diệp Sở không cần điều tra. Lâm Tự Tại và Chu Huyên của Hộ Long Vệ tới, tuyên bố Diệp Sở cũng là bách hộ; thống lĩnh sợ hãi rút lui. Hoàng Phủ Kiệt nhận ra Diệp Sở chính là người khiến mình bị bắt lần trước, hộc máu ngất; Hoàng Phủ Thi Nguyệt đưa ba người vào ngục.
- Ch.207: Hộ Long Vệ giải Hoàng Phủ Kiệt, Hoàng Phủ Kiếm, Hoàng Phủ Dương đi; Lý Thục Anh nhận ra Diệp Sở là "bạn trai" con gái. Chu Huyên từ đế đô, phụ trách cổ mộ, bắt tay thử uy bị hắn bóp đau. Cổ mộ nằm giữa dương cực chi địa; Diệp Sở đoán âm cực chi địa ở hồ Quảng Lăng. Trong mộ có đường đá xanh, dạ minh châu, điện đá với bát giác cao đài và thanh đồng quan phủ trận; Chu Huyên xúi hắn thử phá.
- Ch.208: Diệp Sở phá trận quanh đài rồi trận trên quan tài, mở nắp; độc vụ bị Oán Long Khí nuốt. Trong quan có giếng đứng xuống sâu và nhiều tùy táng phẩm, nổi bật là tượng ngọc nhỏ cao nửa mét; hắn thu hết vào tiểu đỉnh, chỉ để lại một cuộn tranh chữ. Chu Huyên chất vấn nhưng không có bằng chứng, đành kết thúc thăm dò.
- Ch.209: Diệp Sở xác nhận hồ Quảng Lăng là âm cực chi địa đối ứng dương cực chi địa, nghi mộ của Quảng Lăng Vương. Tấm ngọc bạch khắc lệ thư thời Thiên Hán ghi: Quảng Lăng Vương là con Vũ Đế, có long khí, dùng vu cổ chi thuật giết vua bất thành rồi thắt cổ tự vẫn. Tượng ngọc nhỏ kéo hồn hắn vào trong; hắn học Vu Khôi Thuật mất một ngày để thoát. Gia Cát Triết Nhã gọi mời ăn tối.
- Ch.210: Tại Giang Hoài Các, Gia Cát Triết Nhã cảm ơn vì Bách Dược Tửu bán chạy, dọn toàn món tráng dương và rượu Long Huyết Tửu tự nấu. Uống xong cả hai bốc hỏa; nàng nói đó là Tứ Dương Độc, Vũ Tôn cũng không áp chế nổi. Diệp Sở hỏi nàng rốt cuộc là ai.
- Ch.211: Kẻ nhập xác là Tư Đồ Tĩnh — thánh nữ Vu Cổ Giáo — dùng Vu Khôi Thuật chiếm thân Gia Cát Triết Nhã. Diệp Sở phong ấn ý niệm ả tại Dương Bạch, Đầu Duy, Ấn Đường; ả không có giải dược, cả hai bị độc dồn nên quan hệ nhiều giờ. Thả ả ra, ả tiết lộ Gia Cát Triết Nhã đã có hôn ước với con trai út của Giang Nam Hầu rồi rời đi; Gia Cát Triết Nhã tỉnh lại, mơ hồ.
- Ch.212: Gia Cát Triết Nhã đòi mười phần trăm cổ phần tập đoàn Bách Dược làm bồi thường, Diệp Sở đồng ý; nàng cấm kể chuyện này. Oán Long Khí dịu lại sau khi song tu. Nhà họ Long gọi báo đủ dược liệu; hắn đổi dung mạo tới nhà họ Long luyện đan cho Long Đỉnh Thiên. Bé gái linh hồn ăn mất ba trong bốn viên đan.
- Ch.213: Long Trấn Sơn nhận một viên, nghi Diệp Sở ăn bớt dược liệu. Long Đỉnh Thiên trao chiến thiếp của lão tổ Chân Vũ Tông, hẹn ba ngày sau tại núi Thần Cư; hắn nhận lời, sau đó nội thương Long Đỉnh Thiên khỏi hẳn. Gia Cát Triết Nhã gọi nhờ "Diệp đại sư" chữa bạn; hắn tới biệt thự.
- Ch.214: Bệnh nhân là Tần Tư Mộ, đi cùng Lý Lương; nàng khô héo vì hỏa độc. Bé gái linh hồn hút sạch hỏa độc, Diệp Sở truyền chân khí, da tóc hồi phục. Hắn nghi có dị hỏa phía sau.
- Ch.215: Tần Tư Mộ nói phát bệnh sau chuyến đi Thần Nông Giá. Lý Lương đưa séc hai trăm triệu, Diệp Sở từ chối và nói rồi hắn sẽ phải cầu xin; Lý Lương cũng nhiễm ít hỏa độc và định tới tập đoàn Bách Dược bàn hợp tác. Diệp Sở luyện đan, đột phá ngũ phẩm Vũ Tôn thất bại, dừng ở tứ phẩm đỉnh phong. Vương Tam Thông gọi cầu cứu.
- Ch.216: Vương Tam Thông bị Ám Bảng tập kích ở Thần Nông Giá, trọng thương. Bạch Hiểu Hiểu cho máy bay và hai cựu sát thủ; Diệp Sở nhảy từ độ cao hàng trăm mét, tìm thấy lão trong hang. Vương Tam Thông đưa ngọc giản tàn khuyết vẽ vị trí một tiểu động thiên.
- Ch.217: Vương Tam Thông nói Đại Hạ chỉ môn phái đỉnh cấp mới có động thiên phúc địa; Lão Khang chết che chắn cho lão, Diệp Sở hứa báo thù. Ở thị trấn, Lý Đầu Trọc và hai người Bạch Lang Hội bị nhà họ Đỗ vây; Lôi Minh — lục phẩm tông sư — hạ họ dưới mười chiêu. Diệp Sở tới, tát thiếu gia nhà họ Đỗ ngất xỉu.
- Ch.218: Diệp Sở tát Lôi Minh bay, đòi mỗi người mười triệu, nhà họ Đỗ trả hơn hai trăm triệu. Gia chủ nhà họ Đỗ sai Lôi Minh đi bắt; con gái Đỗ Linh Nhi mặc đạo bào trắng khuyên chờ chuyến vào động thiên. Vương Tam Thông cảnh báo nhiều thế lực đang đổ về.
- Ch.219: Đoàn vào sâu Thần Nông Giá; một trực thăng nổ khi đâm vào kết giới vô hình trên hồ. Bên kia hồ là người Võ Đang đi cùng nhà họ Đỗ; gã trung niên gầy được gọi "Hà tông sư"/"Hà thúc" (tức Lôi Minh). Đỗ Linh Nhi chất vấn Diệp Sở. Hắn cảm nhận dị hỏa sau kết giới và đại trận dưới lòng đất.
- Ch.220: Đỗ Linh Nhi đòi trả lại hơn hai trăm triệu, nộp cây thuốc và xin lỗi; sư huynh tông sư viên mãn ra tay bị Diệp Sở tát hộc máu. Bạch Hạc chân nhân — phó chưởng giáo Võ Đang, ngũ phẩm Vũ Tôn — đánh ngang ngửa cho tới khi Diệp Sở dùng Long Quyền đánh lão bay xuống bãi.
- Ch.221: Bạch Hạc chân nhân nhận thua, xin bỏ qua chuyện với nhà họ Đỗ; Diệp Sở cảnh cáo. Hai Vũ Tôn hợp sức phá kết giới bất thành; Diệp Sở tìm ra mấy chỗ nứt và cho mọi người đánh đồng loạt, kết giới vỡ vụn, hồ sôi lên. Bờ bên kia, một đạo cô áo đỏ có ấn sen đỏ giữa trán thấy trận biến mất.
- Ch.222: Hai bè tới đảo nhiều linh khí và dược liệu quý; Bạch Hạc chân nhân tách đi. Diệp Sở giết một trăn khổng lồ sắp hóa yêu, lấy xà đảm. Trong thung lũng, bốn người đánh một vượn vàng giữ cây Tử Kim Táo bảy quả; Vương Tam Thông nhận ra Thiết Sơn — hạng mười Ám Bảng — là kẻ giết Lão Khang.
- Ch.223: Vương Tam Thông trao ngọc giản cho Diệp Sở. Hồng Liên chân nhân — chưởng giáo Nga Mi, sư phụ Khương Quân Dao, thất phẩm Vũ Tôn — dùng Hồn Kiếm giết vượn vàng nhưng trọng thương. Ba kẻ kia quay lại đánh bại nàng; sư tăng dâm ác định làm nhục, nàng toan tự vẫn thì Diệp Sở lên tiếng.
- Ch.224: Thiết Sơn nhận ra Vương Tam Thông là người Đông Hải Vương gia; Diệp Sở dùng Long Quyền đánh nát tay và giết hắn. Sư tăng lục phẩm Vũ Tôn và lão mũi diều hâu Lão Hoắc ngũ phẩm Vũ Tôn hợp công; trượng tăng bắn kim tẩm Bách Trùng Độc. Diệp Sở giả trúng độc, một quyền xuyên ngực Lão Hoắc; sư tăng bỏ chạy.
- Ch.225: Sư tăng — Tà Tăng hạng tư Ám Bảng, biết Đạp Tuyết Vô Ngân học lỏm của nhà họ Tây Môn — chạy thoát. Hồng Liên chân nhân chia Tử Kim Táo bốn-ba rồi cùng đi; họ gặp thêm Trú Nhan Quả và một bảo vật tăng thần hồn, chia đôi. Nàng gả đồ đệ Khương Quân Dao cho hắn, hai bên ký hôn thư; hắn ký tên "Sở Dạ", nàng đoán hắn thuộc nhà họ Sở ở Kinh Châu. Hắn hẹn cuối năm lên Nga Mi cầu hôn.
"""

first = BLOCK.strip().split("\n")[0]
if any(l.strip() == first for l in lines):
    print("skip:", first)
else:
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 196-225"); break

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Cliffhanger ch.225: Diệp Sở — dưới tên giả "Sở Dạ" — vừa ký hôn thư hứa cưới Khương Quân Dao với Hồng Liên chân nhân, hẹn cuối năm lên Nga Mi cầu hôn; Khương Quân Dao KHÔNG hề biết. Dị hỏa ở Thần Nông Giá vẫn chưa tìm ra, Tà Tăng (hạng tư Ám Bảng) đã trốn thoát (ch.223–225).
- Chân Vũ Tông vẫn treo mối thù giết Đông Hải Dược Vương; lão tổ tông môn đã gửi chiến thiếp hẹn ba ngày sau tại núi Thần Cư (ch.213) — mốc này chưa được giải quyết trong 196–225.
- Bé gái linh hồn tóc đỏ (thực lực ngang đại tông sư) đang theo Diệp Sở, ăn mất ba trong bốn viên đan ở ch.212 — cần nhớ khi viết tiếp.
- Danh tính: Bạch Hiểu Hiểu nghi Sở Bá Vương là Diệp Sở (ch.197); Vương Hạ Niên nghi Diệp thần y là Diệp đại sư (ch.199); Hoàng Phủ Kiệt, Chu Huyên, Lâm Tự Tại và thành vệ biết Diệp Sở là bách hộ Hộ Long Vệ (ch.206–207); Lý Thục Anh biết hắn là bạn trai Hoàng Phủ Thi Nguyệt (ch.207); Tư Đồ Tĩnh đã nhận ra từ vụ nhà họ Long (ch.211). Khương Quân Dao, Hàn Mộng Quan, nhà họ Diệp, Long gia vẫn chưa biết.
- Tài sản/địa bàn: tập đoàn Bách Dược do Tôn Ngữ Nhu làm chủ tịch, Hàn Mộng Quan làm tổng giám đốc, Gia Cát Triết Nhã giữ mười phần trăm cổ phần; Diệp Sở thu toàn bộ tùy táng phẩm trong mộ Quảng Lăng Vương vào tiểu đỉnh, học Vu Khôi Thuật và ba thức Long Quyền (ch.200–212).
- Không đổi cách gọi đã chốt (LƯU Ý 44–51): "Vũ Tôn" (không viết "Võ Tôn"), "nữ Vũ Tôn", "Chu Huyên", "Long Quyền", "Vu Khôi Thuật", "Sở Dạ" chỉ là tên giả của Diệp Sở, "Đỗ Linh Nhi" (không dùng "Đỗ Cẩm Tú"), "Lôi Minh" (không dùng "Hà tông sư"), "Triệu Ngũ" (không dùng "Triệu Vũ"), "Tư Đồ Tĩnh = U Lan", "Thệ Tâm Cổ".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc rebind theo ch.225 (%d dong)" % len(NEW.strip().split("\n")))
io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 196-225. tong dong:", len(lines))