# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl11b.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

BLOCK = """### Đã xảy ra — chương 116–135:
- Ch.116: Trong phòng thi Cục Y tế, Diệp Sở phóng châm không chạm người, thi triển Kim Châm Thích Huyệt khiến Tần Đông Dương toát mồ hôi đen, đại tiện ra quần trước đám đông. Hùng Minh — phó cục trưởng, cậu của Tần Đông Dương — gọi bảo vệ, nhưng La Vân và Lý Chính Nguyên tới kịp; La Vân tuyên bố Diệp Sở do Lý quốc thủ bảo lãnh. Từ Mỹ Tĩnh chính là người đã nhắn tin cầu cứu.
- Ch.117: Diệp Sở lấy được chứng chỉ hành nghề đông y, tới bệnh viện Giang Nam luyện Tiểu Sinh Cơ Đan (tam phẩm) cứu Mã Tứ Thủy; Mãn Hùng thề sẽ báo đáp. Tư Đồ Tĩnh nhận ra đan, tự giới thiệu và mời hắn bái Y Thánh Kim Lăng — sư phụ nàng — làm thầy, bị từ chối; nàng quát Tư Đồ Triều vì hỗn láo.
- Ch.118: Diệp Sở gặp Diệp Đình Đình tại quán bar Tinh Nguyệt; nàng kể bị nhà họ Diệp giám sát. Hắn hứa giúp nàng nắm nhà họ Diệp, đổi lại nàng phải đòi quyền thừa kế để hợp tác với nhà họ Khương. Nhóm Lý Tam Đao của Bạch Lang Hội quấy rối, bị hắn đánh bay.
- Ch.119: Trương Ma Tử nhận ra Diệp Sở, vội xin lỗi và lôi Lý Tam Đao đi; sau đó phát hiện có kẻ trả hai vạn tệ thuê gây sự ở quán bar Tinh Nguyệt. Tại Kim Lăng, một trung niên của Thánh Giáo báo với thánh nữ: đã tìm ra người liên quan cái chết của giáo chúng, nghi dính tới Dược Hoàng, và đã chuẩn bị "đại lễ".
- Ch.120: Khương Quân Dao cho người tìm cổ mộ vô ích; U Lan — thánh nữ Vu Cổ Giáo, đeo mặt nạ quỷ — đột nhập, nói ngôi mộ bị trận pháp che giấu và đề nghị hợp tác: giáo lấy 《Đại Vu Thiên Kinh》, sư môn nàng lấy lệnh bài. Nàng đồng ý; U Lan hứa hôm sau cử người tới. Ở trang viên hồ Quảng Lăng, Diệp Sở luyện Đại Chân Nguyên Đan cho Vân Băng Uyển và Tôn Ngữ Nhu đột phá Hóa Kình tông sư.
- Ch.121: Lục Triển Nguyên — thành viên Địa tự của Hộ Long Vệ — tới Giang Đô. Chu Bẩm Thiên tiết lộ đã bắt được Lạc Thiên Tuyệt khiến Kim Bằng bẽ mặt, rồi từ chối giao người. Lục Triển Nguyên bóp cổ giết Chu Bẩm Thiên, nói công lao của Hộ Long Vệ không để kẻ nhỏ nhen cướp.
- Ch.122: Tin Chu Bẩm Thiên bị Lạc Thiên Tuyệt giết lan ra; Vương Tam Thông hoảng hốt tới trang viên. Diệp Sở nghi ngờ vì chính tay hắn đã phế tu vi Lạc Thiên Tuyệt rồi giao cho Chu Bẩm Thiên, bèn tới tổng bộ thành vệ quân, gặp Lâm Bắc Hạc — phó thống lĩnh, chỗ dựa của Hắc Hổ Hội. Lính chĩa súng, hắn phóng ngân châm đoạt súng, đánh ngã tất cả, bẻ gãy một đầu gối của Lâm Bắc Hạc, buộc khai.
- Ch.123: Lâm Bắc Hạc khai Lục Triển Nguyên giết Chu Bẩm Thiên rồi ép hai phó thống lĩnh đổ tội cho Lạc Thiên Tuyệt; Diệp Sở tra tấn bằng châm năm phút, bắt quay video nhận tội. Mã Tứ Thủy gọi mời ăn tối tại Giang Hoài Các, Vương Tam Thông nghi là Hồng Môn Yến. Mã Tứ Thủy tỉnh nhờ đan, đột phá bán bộ tông sư rồi bàn với Lục Triển Nguyên, Kim Bằng đòi đan và phương thuốc; Mãn Hùng phản đối nên bị trói.
- Ch.124: U Lan nghe thuộc hạ báo Hộ Long Vệ nổi lòng tham, ngồi chờ kết quả. Tại phòng bao Đế Vương của Giang Hoài Các, Mã Tứ Thủy giới thiệu Lục Triển Nguyên xuất thân nhà họ Lục ở Trung Châu. Diệp Sở không nể, từ chối rượu, nói đã hết đan; Mã Tứ Thủy đòi phương thuốc, Vương Tam Thông mắng vong ân, Kim Bằng đứng dậy đòi dùng nắm đấm.
- Ch.125: Kim Bằng — tứ phẩm tông sư — lao vào bị Diệp Sở phóng đũa xuyên vai ghim vào tường; Mã Tứ Thủy — bán bộ đại tông sư — cũng bị đũa xuyên vai. Lục Triển Nguyên mời hắn gia nhập Hộ Long Vệ, bị từ chối, ra tay liền bị một chưởng đẩy lùi.
- Ch.126: Lục Triển Nguyên dùng hóa khí thành nhận bắn khí nhận, Diệp Sở vỗ tay bẻ gãy hết, đánh bay rồi giẫm gãy chân. Lục Triển Nguyên thừa nhận giết Chu Bẩm Thiên; Diệp Sở bóp cổ giết hắn. Mã Tứ Thủy và Kim Bằng quỳ khai tội trước camera rồi bị phế tu vi; hắn dặn Vương Tam Thông che thân phận khi đăng video.
- Ch.127: Mãn Hùng tới, kể bị trói, được giao giữ hai kẻ kia. Video lan truyền; tài khoản đăng lấy tên Sở Bá Vương trùng tên chủ trang viên hồ Quảng Lăng nên dân chúng đoán là một người. Tô Định Hạ — thống lĩnh Hộ Long Vệ — tại đế đô nghe Mãn Hùng trình bày rồi bỏ qua chuyện này, ra lệnh thanh tra nội bộ.
- Ch.128: Khương Hải Vân ca ngợi Sở Bá Vương, ước có con rể như vậy; Hàn Mộng Quan mắng. Bà khen Diệp Sở lấy được chứng chỉ, khuyên mở y quán, hắn từ chối. Tập đoàn Khương thị thiếu vốn, nguy cơ phá sản vì dồn tiền hợp tác nhà họ Hoàng Phủ; Hàn Mộng Quan không cho dùng thẻ của hắn (thực tế trong thẻ có mấy chục tỷ).
- Ch.129: Khương Quân Dao gọi điện hỏi sư tỷ về Sở Bá Vương, có chút động lòng nhưng đem so lại thấy Diệp Sở tầm thường. Diệp Đình Đình báo nhà họ Diệp đồng ý cho nàng làm gia chủ nếu hợp tác với nhà họ Khương. Diệp Sở nhờ Khương Quân Dao giúp, nàng đồng ý ngay nhưng nói còn tùy nhà họ Hoàng Phủ. Hôm sau Hoàng Phủ Thi Nguyệt gọi hắn tới nhà.
- Ch.130: Hoàng Phủ Thi Nguyệt nấu ăn, hai người thân mật như vợ chồng. Nàng cho xem video trận đấu, Diệp Sở thừa nhận mình chính là Sở Bá Vương và là đại tông sư. Nàng kinh ngạc; hắn trêu đòi hôn, nàng ngã vào lòng hắn rồi đồng ý cho hôn một cái.
- Ch.131: Đông Mai gọi báo Hoàng Phủ Kiệt sắp tới Giang Đô, cắt ngang nụ hôn. Hoàng Phủ Thi Nguyệt đồng ý giúp việc hợp tác Diệp gia và Khương gia, hỏi sao thành chủ trang viên hồ Quảng Lăng, rồi rủ ly hôn ở với nàng, nàng lấy hắn ngay; hắn từ chối. Hai người tới hồ, thấy đông người chờ diện kiến Sở Bá Vương.
- Ch.132: Diệp Sở bế Hoàng Phủ Thi Nguyệt lướt mặt hồ vào trang viên, tránh đám đông; Chung San đuổi khách. Lâm Tự Tại — bách hộ Hộ Long Vệ — cùng Mãn Hùng tới và được mời vào. Nhà họ Long, họ Lý, họ Khương và bốn đại hào tộc kéo tới; nhà họ Vương im lặng. Lâm Tự Tại quát "ngươi có biết tội".
- Ch.133: Lâm Tự Tại nói chỉ muốn thử thực lực, dùng Hình Ý Quyền (cổ quyền pháp Đại Hạ, mười hai hình); Diệp Sở học ngay tại chỗ, sau một khắc đánh vào sườn khiến đối phương nhận thua. Lâm Tự Tại mời vào Hộ Long Vệ, cho thẳng chức bách hộ; Diệp Sở nhận sau khi Hoàng Phủ Thi Nguyệt khuyên, với điều kiện không hạn chế tự do. Long Trấn Sơn — gia chủ nhà họ Long, cha là Long Bách Nhạc — tới hô xin gặp.
- Ch.134: Một cô gái nhà họ Long mắng Chung San; tiếng "Cút" từ trong trang viên làm cô ta chảy máu tai, ngã ngồi. Long Trấn Sơn kìm nén rút lui vì ngại đại tông sư và Lâm Tự Tại; Long Trấn Hà đòi gọi người. Vân Băng Uyển tới, bị Long Trấn Sơn cảnh cáo không được bám Sở Bá Vương; Vân Trung Hạc hỏi có bỏ không, nàng nói vẫn về. Hàn Mộng Quan thấy giọng quen, Khương Hải Vân gạt đi; Khương Quân Lan nghi ngờ nhưng nhớ lời cảnh báo của Vương Hạ Niên.
- Ch.135: Diệp Sở nói với Hoàng Phủ Thi Nguyệt rằng hắn có thù với nhà họ Long. Diệp Trịnh Khôn hứa với Diệp Đình Đình nhưng nói sẽ không giao cơ nghiệp cho con riêng, chỉ lợi dụng tình cảm với Diệp Sở; còn định cho con cháu dự tiệc nhà họ Tần đón một thiếu gia Kim Lăng. Đông Mai báo Hoàng Phủ Kiệt tới Giang Đô, ở nhà họ Tần, có thiệp mời; Hoàng Phủ Thi Nguyệt rủ Diệp Sở dự tiệc tối mai.
"""

first = BLOCK.strip().split("\n")[0]
if any(l.strip() == first for l in lines):
    print("skip (da co):", first)
else:
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block Da xay ra 116-135")
            break
    else:
        print("  CANH: khong thay ### Ràng buộc")

# LƯU Ý 43
block2 = """43. Source ch.116–135 tự gõ lẫn vài chỗ, bản dịch thống nhất một dạng: 周禀天 (ch.121–125) và 周斌天 (ch.126) là CÙNG một người — Chu Bẩm Thiên; 圣教 (ch.119) và 巫蛊教 (ch.120) là cùng một giáo phái — Vu Cổ Giáo; 金护法 và 金护卫 (ch.121) đều là Kim Bằng; 陆展元 được ghi "地字号成员" (ch.121) rồi "字号成员" (ch.126). Không bày ra nhân vật thứ hai cho bất kỳ cặp nào ở trên."""
if not any(l.strip() == block2 for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("## ══════ VĂN PHONG"):
            lines[i:i] = block2.split("\n") + ["", ""]
            print("  + LƯU Ý 43")
            break

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 116-135. tong so dong:", len(lines))