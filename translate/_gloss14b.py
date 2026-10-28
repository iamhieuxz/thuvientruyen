# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl14b.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

BLOCK = """### Đã xảy ra — chương 166–195:
- Ch.166: Tại Giang Hoài Các, Hoàng Phủ Kiếm khuyên Hoàng Phủ Thi Nguyệt đừng giao du với "kẻ không ra gì"; Hoàng Phủ Kiệt tuyên bố đã tiếp nhận dự án Giang Đô và Thi Nguyệt sẽ sớm bị gọi về Kim Lăng gả người. Hoàng Phủ Kiệt cho Sơn thúc ngừng tay; Diệp Sở hứa sẽ khiến hắn "cút", bàn kế mở công ty dược và bán đan trường thọ cho người giàu; Đông Mai được cử về Kim Lăng thu mua dược liệu.
- Ch.167: Diệp Sở qua đêm với Hoàng Phủ Thi Nguyệt rồi gọi Vương Tam Thông vay ba tỷ; Vương Tam Thông đang bị thương, giấu một món đồ, Lão Khang khuyên giao ra nhưng bị từ chối. Diệp Sở gọi Tô Định Hạ — thống lĩnh Hộ Long Vệ ở đế đô — tự xưng là sư đệ chưa từng gặp mặt và được nhận lời giúp. Tô Định Hạ cử Chu Huyên đi Giang Đô, dặn tránh xung đột toàn diện với Vu Cổ Giáo.
- Ch.168: Diệp Sở chuyển hai tỷ cho Hoàng Phủ Thi Nguyệt, giữ một tỷ. Bạch Lang Hội bị nhà họ Long cho ba ngày để quy phục; Lý Đầu Trọc mua được dược liệu tốt ở Thần Nông Giá. Diệp Sở luyện đan thì Oán Long Khí bạo động phải dừng. Chu Huyên dẫn người phong tỏa công trường; Hoàng Phủ Kiệt tới quát, bị cô hỏi ngược "định làm gì ta?".
- Ch.169: Chu Huyên bẻ gãy cổ tay Khương Quân Long, đá bay Sơn thúc, gọi Hộ Long Vệ bắt Hoàng Phủ Kiếm, Hoàng Phủ Kiệt và Khương Quân Long. Hoàng Phủ Kiệt dọa "chị rể là con trai tỉnh trưởng Giang Nam", Chu Huyên đáp tỉnh trưởng tới cũng phải khách sáo; hắn nghi Diệp Sở giở trò rồi tự phủ nhận. Ở Bạch Lang Hội, Bạch Hiểu Hiểu — thất phẩm tông sư — thắng một lão già thất phẩm nhưng bị bà lão bát phẩm đánh văng vào tường.
- Ch.170: Diệp Sở xuất hiện, bà lão quỳ xin tha và tự tát ba cái; lão già ăn một chưởng rồi thần phục. Tin tức: Long Cửu Dương từ tỉnh Đông Hải về; ba ngày sau nhà họ Long mở cuộc luyện đan thưởng một tỷ; nhà họ Long muốn Bạch Lang Hội vì sắp tới Giang Đô sẽ loạn. Diệp Sở đưa năm trăm triệu cho Bạch Hiểu Hiểu mua dược liệu. Hoàng Phủ Thi Nguyệt về Kim Lăng, buộc Hoàng Phủ Bích Nguyệt phải cầu xin.
- Ch.171: Hoàng Phủ Minh đồng ý trả lại quyền kiểm soát dự án; công trường mở lại, chỉ còn khu mộ cổ bị phong tỏa; Hoàng Phủ Bích Nguyệt phải xin lỗi trước mặt mọi người. Hoàng Phủ Kiệt được thả, tưởng "anh rể" cứu.
- Ch.172: Hoàng Phủ Kiếm bàn với Hoàng Phủ Kiệt phá công trình để Hoàng Phủ Thi Nguyệt không hoàn thành nổi. Lâm Hào — công tử nhà họ Lâm ở Cô Tô — nhận vơ công cứu Khương Quân Long, được nhà họ Khương mời; hắn định chiếm Khương Quân Dao và biết ngôi mộ là của Quảng Lăng Vương nhờ sư phụ. Diệp Sở tới Giang Hoài Các, bị Lâm Hào bảo tránh xa Khương Quân Dao.
- Ch.173: Khương Hải Vân định tát Diệp Sở, bị giữ tay; Lâm Hào đòi ra tay thì Hoàng Phủ Thi Nguyệt tới tuyên bố "ai dám động vào đàn ông của ta". Nàng — lục phẩm tông sư — đánh với vệ sĩ thất phẩm của Lâm Hào, thắng nhờ Diệp Sở bí mật bắn một luồng khí. Nàng tuyên bố đã lấy lại dự án và sẽ chấm dứt hợp tác với nhà họ Khương.
- Ch.174: Khương Quân Long gọi Tần Đông Dương xác nhận; Lâm Hào hứa nhờ ông nội nhưng thực chất lừa, sai Triệu Ngũ — vệ sĩ thất phẩm tông sư — đến Bạch Lang Hội chiêu mộ người làm pháo hôi thám hiểm mộ cổ.
- Ch.175: Diệp Sở gặp Diệp Đình Đình, đưa điều kiện: 51 phần trăm cổ phần tập đoàn Diệp thị và họp báo lập cô làm người thừa kế; nhà họ Diệp nổi giận. Triệu Ngũ bị Bạch Lang Hội đánh nhừ tử; Bạch Hiểu Hiểu định giả vờ quy phục nhà họ Long để "chó cắn chó". Diệp Trịnh Khôn gọi "ông nội", Diệp Sở đáp "ông nội ta chết lâu rồi".
- Ch.176: Diệp Sở luyện đan từ Hoàng Tuyền Hoa và Long Đảm Thảo: tinh thần lực từ ba mươi mét lên năm mươi mét, đột phá Vũ Tôn tứ phẩm trong cảnh đồng bì thiết cốt. Nhà họ Diệp chấp nhận điều kiện, Diệp Đình Đình nắm quyền. Hoàng Phủ Thi Nguyệt đồng ý không hủy hợp đồng với nhà họ Khương, chỉ muốn họ "chảy máu".
- Ch.177: Khương Quân Dao đón Hồng Vân và Chu Thanh Thanh tại sân bay; sư phụ nàng là Hồng Liên — sư tỷ của Hồng Vân — bị hoãn chuyến. Hồng Vân giao Khu Sát Đan và gọi cho Hoàng Phủ Minh. Diệp Sở biết muốn dự cuộc luyện đan phải có người tiến cử và phải chẩn ra bệnh kín của Long Đỉnh Thiên. Tại nhà họ Khương, Khương Quân Dao mắng "một phái hồ ngôn" và đuổi hắn; hắn từ bỏ ý định với cô.
- Ch.178: Hàn Mộng Quan tặng Diệp Sở thẻ một trăm triệu. Long Cửu gia gọi mời hắn làm người tiến cử; lão là em Long Trấn Sơn, từng tranh vị gia chủ và thua. Diệp Sở dịch dung thành đạo sĩ trẻ; Triệu Hổ đến đón; Long Xán Dương chế giễu ở cổng trang viên.
- Ch.179: Trong trang viên nhà họ Long có Hoàng Hải Quân — thị trưởng — và vợ, Gia Cát Triết Nhã, Y Thánh Kim Lăng cùng Tư Đồ Tĩnh, Long Cửu Dương cùng Đông Hải Dược Vương (lão gù) và Tiêu Mộc, Hồng Vân, Khương Quân Dao, Chu Thanh Thanh; cuối cùng Vân Băng Uyển bị đưa ra. Đông Hải Dược Vương đòi Vân Băng Uyển ngồi cạnh mình.
- Ch.180: Vân Băng Uyển né tay Dược Vương, bị Long Trấn Nhạc tát; Diệp Sở bẻ gãy cổ tay hắn. Long Cửu gia đối đầu Long Trấn Nhạc, bị Đông Hải Dược Vương đánh chảy máu. Diệp Sở che cho Vân Băng Uyển, gọi Dược Vương là "gà đất chó sành".
- Ch.181: Tiêu Mộc — tông sư viên mãn — bị một chưởng đánh văng, nôn máu, ngất vì nhục. Diệp Sở giật gậy của Dược Vương đánh sáu cái gãy gậy. Long Đỉnh Thiên và Long Trấn Sơn đến cùng Chu Huyên.
- Ch.182: Diệp Sở đá vào hạ bộ Dược Vương, phế luôn "con đường thứ ba" của lão. Long Cửu gia xưng tên thật Long Trấn Nam, tuyên bố đoạn tuyệt nhà họ Long; Long Đỉnh Thiên bỏ qua. Cuộc thi bắt đầu bằng chẩn bệnh; Diệp Sở nói "ông sắp chết".
- Ch.183: Diệp Sở chẩn bát mạch hư hại nặng; Hồng Vân và Y Thánh Kim Lăng khám lại, xác nhận. Diệp Sở đòi năm tỷ.
- Ch.184: Long Đỉnh Thiên từ chối. Ba bảo vật đem ra thưởng: Huyết Linh Chi, tàn thiên võ kỹ trên da dê và Đại Yêu Giao Long Huyết; ai luyện tốt nhất chọn một món cộng một tỷ. Long Đỉnh Thiên loại Diệp Sở khỏi phần luyện đan; Diệp Sở cảnh báo "đừng hối hận".
- Ch.185: Vân Băng Uyển nói đã có người trong lòng; Chu Thanh Thanh giới thiệu bản thân; Khương Quân Dao và Vân Băng Uyển là sư tỷ muội Nga Mi. Tư Đồ Tĩnh bắt tay, bí mật để lại một ấn ký trên tay Diệp Sở; Chu Huyên mời hắn gia nhập Hộ Long Vệ.
- Ch.186: Diệp Sở từ chối chức bách hộ. Gia Cát Triết Nhã kể nhà họ Chu là vương tộc, tước Trấn Nam Vương; Chu Vũ là "tiểu bá vương", mắt trọng đồng, Trấn Tây đại tướng quân, Quán Quân Hầu. Lò đan của Dược Vương nổ (do Diệp Sở ám toán từ lúc đánh gậy); Long Đỉnh Thiên uống hai viên Tiểu Hoàn Đan, đột phá ngũ phẩm đại tông sư rồi gục.
- Ch.187: Khí hải Long Đỉnh Thiên vỡ; Diệp Sở giải thích công pháp gây tổn thương tích tụ. Diệp Sở đòi cả ba bảo vật cộng năm tỷ; Long Trấn Sơn gọi quân.
- Ch.188: Chiến đội Thanh Long thuộc chiến khu Đông bộ do Lý Chiến Ưng dẫn vào. Diệp Sở hạ lính bằng ngân châm, bóp cổ Lý Chiến Ưng; Dược Vương bắn khí xuyên bụng Lý Chiến Ưng, lính nổ súng; Diệp Sở không hề hấn.
- Ch.189: Hồng Vân nhận ra Diệp Sở là Vũ Tôn. Long Trấn Sơn quỳ, bị Diệp Sở chụp ảnh đăng mạng; hắn thu ba bảo vật vào pháp bảo trữ vật. Diệp Sở giết Dược Vương — đại trưởng lão Chân Vũ Tông, cha là Chân Vũ lão tổ — bằng chân khí, tự xưng là thánh tử Vu Cổ Giáo để "họa thủy đông dẫn"; Tư Đồ Tĩnh tím mặt. Năm tỷ về tài khoản; hắn dùng dĩ khí thành châm.
- Ch.190: Diệp Sở thi triển Hỏa Phượng Hoàng — châm pháp do Thần Nông sáng tạo — cứu Long Đỉnh Thiên. Y Thánh Kim Lăng xin bái sư, bị từ chối. Hắn kê danh sách thuốc cho Long Hổ Cân Cốt Đan, cố tình viết thêm mười vị. Khương Quân Dao xin kết bạn, bị từ chối vì "thực lực quá yếu".
- Ch.191: Hồng Vân cảnh báo Chân Vũ Tông sẽ không bỏ qua; Long Đỉnh Thiên bảo Vân Băng Uyển giữ liên lạc với Diệp Sở. Long Trấn Sơn tiết lộ Vân Băng Uyển không phải con riêng, không mang máu nhà họ Long, và việc đưa cô vào Chân Vũ Tông là ý của "vị kia". Diệp Sở đột nhập phòng Vân Băng Uyển.
- Ch.192: Diệp Sở gỡ dịch dung, Vân Băng Uyển nhận ra người mình thương, khóc rồi đồng ý để hắn bảo vệ.
- Ch.193: Vân Băng Uyển kể ngôi mộ ở nam Giang Đô là của Quảng Lăng Vương triều Thiên Hán, giỏi thuật Vu Cổ; chiếc nhẫn của nhà họ Lý là chìa khóa mở mộ. Cô là ký danh đệ tử Nga Mi do nhà họ Long trao đổi lợi ích để trấn âm sát khí.
- Ch.194: Diệp Sở mớm giao long huyết cho Vân Băng Uyển; cô luyện hóa một phần, phá mấy mạch còn lại, đạt tông sư viên mãn, phần huyết khí dư bị hắn phong trong khí hải.
- Ch.195: Diệp Sở hứa bày trận pháp tụ linh khí tăng tốc dược liệu, chuyển mười tỷ; Vân Băng Uyển trao nhẫn sắt đen của nhà họ Lý, thề tự báo thù Long Trấn Sơn cho cái chết của mẹ. Diệp Sở về trang viên hồ Quảng Lăng, nhỏ máu lên tấm da dê võ kỹ — máu thấm vào và dị biến xảy ra.
"""

first = BLOCK.strip().split("\n")[0]
if any(l.strip() == first for l in lines):
    print("skip (da co):", first)
else:
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block Da xay ra 166-195")
            break
    else:
        print("  CANH: khong thay ### Ràng buộc")

i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Diệp Sở đang giữ ba bảo vật của nhà họ Long (Huyết Linh Chi, tàn thiên võ kỹ trên da dê, Đại Yêu Giao Long Huyết) và năm tỷ; tấm da dê đã xảy ra "dị biến" khi hắn nhỏ máu lên — mở đầu ch.196 phải tiếp đúng cảnh này (ch.184–195).
- Hắn vừa giết Đông Hải Dược Vương — đại trưởng lão Chân Vũ Tông, cha là Chân Vũ lão tổ — và tự xưng là thánh tử Vu Cổ Giáo để hướng họa về phía đó. Chân Vũ Tông chắc chắn trả thù; Hồng Vân đã cảnh cáo (ch.181–191).
- Diệp Sở đã đột phá Vũ Tôn tứ phẩm, tinh thần lực năm mươi mét; Vân Băng Uyển biết đạo sĩ chính là hắn, đạt tông sư viên mãn nhờ giao long huyết, đang giữ bí mật và đã thề báo thù Long Trấn Sơn (ch.176, 191–195).
- Danh tính Sở Bá Vương vẫn chưa lộ thêm: Tư Đồ Tĩnh nghi "Diệp đại sư" chính là Diệp Sở (tám phần chắc) nhưng chưa xác nhận; Vân Băng Uyển biết; Khương Quân Dao, Gia Cát Triết Nhã, Hồng Vân, Y Thánh Kim Lăng, Chu Huyên, Long Cửu Dương, Long Trấn Sơn đều chưa biết (ch.182–195).
- Vân Băng Uyển đã trao nhẫn sắt đen của nhà họ Lý — chìa khóa mở mộ Quảng Lăng Vương triều Thiên Hán ở nam Giang Đô, nơi giỏi thuật Vu Cổ; U Lan và Khương Quân Dao vẫn đang nhắm ngôi mộ này (ch.120, 193–195).
- Nhà họ Long: Long Trấn Sơn bị bắt quỳ và bị đăng ảnh, Long Trấn Nam đoạn tuyệt gia tộc; Long Đỉnh Thiên được cứu nhưng khí hải từng vỡ; Long Trấn Nhạc bị bẻ cổ tay (ch.180–190). Hoàng Phủ Kiệt, Hoàng Phủ Kiếm, Khương Quân Long từng bị Hộ Long Vệ bắt rồi được thả (ch.169–171).
- Tài chính: Diệp Sở đã chuyển mười tỷ cho Vân Băng Uyển làm trận pháp dược điền; hứa mở công ty dược với Hoàng Phủ Thi Nguyệt; nhà họ Diệp do Diệp Đình Đình nắm 51 phần trăm cổ phần (ch.165–176, 195).
- Không đổi cách gọi đã chốt (LƯU Ý ĐẶC BIỆT mục 44–50): "Chân Vũ Tông" cho cả 真武宗 lẫn 真武门; "Thệ Tâm Cổ" cho cả 同心蛊 lẫn 噬心蛊; "ông cụ" cho 老爷子; "Tư Đồ Tĩnh = U Lan"; "Hoàng Phủ Kiếm ≠ Hoàng Phủ Kiệt"; "Hoàng Phủ Minh ≠ Hoàng Vệ Minh"; "Đông Hải Dược Vương ≠ Dược Hoàng"; "Tiêu Mộc" (thánh tử Chân Vũ Tông); "Chu Huyên"; "Long Trấn Nam = Long Cửu gia"; "Vũ Tôn"; "Long Hổ Cân Cốt Đan".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc: da rebind theo ch.195 (%d dong)" % len(NEW.strip().split("\n")))

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 166-195. tong so dong:", len(lines))