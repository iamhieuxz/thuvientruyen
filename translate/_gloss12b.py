# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl12b.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

BLOCK = """### Đã xảy ra — chương 136–165:
- Ch.136: Diệp Sở tặng Hoàng Phủ Thi Nguyệt hai bình ngọc Khai Mạch Đan và Đại Chân Nguyên Đan giúp đột phá đại tông sư; hai người tỏ tình và hôn nhau thì Đông Mai gọi báo công trường có sự cố.
- Ch.137: Hoàng Phủ Thi Nguyệt tới công trường khu Nam Thành nghi có cổ mộ. Diệp Sở đưa Khai Mạch Đan cho Vân Băng Uyển nhưng giữ lại Đại Chân Nguyên Đan; Tôn Ngữ Nhu đã đạt Đoán Thể ngũ đoạn, nhận Tiểu Chân Nguyên Đan và Khai Mạch Đan. Vân Mộng Dược Nghiệp bị nhà họ Tần ép bán vì nợ ngân hàng.
- Ch.138: Hàn Mộng Quan định bán đấu giá công ty. Khương Quân Dao về nhà trong thương tích: nàng cùng sư tỷ, U Lan và Hoàng Phủ Thi Nguyệt vào cổ mộ, cả ba tông sư đều bị thương. Tại khách sạn Giang Nam, Tần Đông Dương chặn cửa, tuyên bố "Diệp Sở và chó không được vào".
- Ch.139: Ngô Thiếu Binh bêu Diệp Sở là kẻ ở rể; Khương Hải Phong định ra tay. Lý Quảng Lăng — gia chủ nhà họ Lý — tới chào "Diệp thần y", dọa đuổi cả nhà họ Tần khỏi khách sạn; Tần Đông Dương đành nhượng bộ.
- Ch.140: Long Xán Dương và Long Tuyết Phi, con nhị phòng nhà họ Long, tới dự. Ngô Thiếu Binh vu cáo Diệp Sở khinh thường nhà họ Long; Long Xán Dương bắt quỳ lạy, tự tát một trăm cái, còn hất mặt Lý Quảng Lăng. Đông Mai đỡ đòn, đẩy lùi Long Xán Dương.
- Ch.141: Đông Mai tát Long Tuyết Phi, hạ vệ sĩ nhà họ Tần, bẻ gãy cổ tay Trương đại sư — người được nhà họ Tần cúng dưỡng, Đoán Thể tám đoạn — và bị nhận ra là tông sư. Hoàng Phủ Kiệt tới cùng Triệu Vũ Tuyên và nhận ra Đông Mai.
- Ch.142: Triệu Vũ Tuyên đánh bại Đông Mai sau hơn trăm hiệp, định phế khí hải của nàng thì Diệp Sở đỡ đòn, quật ngã, đấm lõm ngực rồi đá nát khí hải Triệu Vũ Tuyên. Diệp Sở chỉ vào nhà họ Diệp nói "giết chết cũng được". Lâm Bắc Hạc dẫn thành vệ tới.
- Ch.143: Lâm Bắc Hạc thấy Diệp Sở liền rút lui. Diệp Sở tát Hoàng Phủ Kiệt hai cái rụng răng, cảnh cáo; tát Ngô Thiếu Binh; Long Xán Dương thề trả thù. Diệp Đình Đình báo Diệp Trịnh Khôn rằng nhà họ Khương đã ký hợp tác.
- Ch.144: Nhà họ Diệp quyết cắt đứt quan hệ với Diệp Sở; Khương Phong Niên ra lệnh ly hôn. Hoàng Phủ Thi Nguyệt kể chuyện cổ mộ; Hàn Mộng Quan gọi Diệp Sở về nhà.
- Ch.145: Khương Quân Dao dứt khoát đồng ý ly hôn; Hàn Mộng Quan lén đưa chìa khóa một căn nhà riêng. Ly hôn xong, Khương Quân Dao tới nhà họ Long cầu xin, xuất trình Nga Mi lệnh và nói sư phụ mình là Hồng Liên chân nhân, chưởng môn phái Nga Mi.
- Ch.146: Long Đỉnh Thiên — lão gia chủ nhà họ Long — tha bổng vì nợ ơn Hồng Liên chân nhân, nhưng nói riêng: "phía đế đô có người muốn bảo vệ hắn". Một mũi nỏ bắn sượt tai Hoàng Phủ Kiệt kèm thư cảnh cáo (hắn nghi Hoàng Phủ Thi Nguyệt). Tại Giang Hoài Các, Diệp Đình Đình nói nhà họ Diệp phản lời; Diệp Sở hứa sẽ khiến nhà họ Diệp phải cầu xin nàng.
- Ch.147: Hoàng Phủ Thi Nguyệt tự nấu ăn, rủ Diệp Sở làm vệ sĩ; gọi tập đoàn Khương thị buộc lấy Diệp Đình Đình làm đối tác. Diệp Trịnh Khôn tuyên bố Diệp Đình Đình làm thiếu gia chủ kiêm tổng giám đốc tập đoàn Diệp thị.
- Ch.148: Diệp Sở và Hoàng Phủ Thi Nguyệt dự buổi đấu giá của Thương hội Giang Nam; Khương Quân Long chế nhạo. Tần Đông Dương vừa lấy lại chức thiếu gia chủ, khiêu khích Hàn Mộng Quan; Vân Mộng Dược Nghiệp được đem bán đấu giá.
- Ch.149: Giá khởi điểm mười tỷ, Tần Đông Dương trả mười một tỷ; Diệp Sở trong phòng VIP nâng tới mười tám tỷ, buông "Hoàng Phủ Kiệt là cái gì", tuyên bố cứ tới trang viên hồ Quảng Lăng tìm. Cả hội trường nhận ra "Sở Bá Vương".
- Ch.150: Tần Đông Dương rút lui, Vân Mộng Dược Nghiệp bán với giá mười tám tỷ. Hoàng Phủ Kiệt biết Sở Bá Vương là đại tông sư, lệnh phá công trường nam thành và nhận tin nhắn số lạ "Hoàng Phủ Thi Nguyệt, cô xong rồi". Hoàng Phủ Thi Nguyệt rủ Diệp Sở về nhà nàng.
- Ch.151: Hai người thành đôi; Hoàng Phủ Thi Nguyệt đòi làm "vợ cả". Oán Long Khí giảm nhờ hấp thụ nguyên âm nhưng sẽ phục hồi, buộc phải tìm Chân Long Cốt. Diệp Sở cho nàng xem vảy rồng và vảy ngược, nhờ nàng thu thập tin về Long tộc.
- Ch.152: Bạch Lang Hội đã thống nhất giới ngầm Giang Đô, Bạch Hiểu Hiểu từ chối quy phục nhà họ Long; nhà họ Tư Mã ở Kim Lăng đang vướng chuyện. Diệp Sở luyện Đoán Thể Đan, Tiểu Chân Nguyên Đan, Khai Mạch Đan; Lý Đầu Trọc báo Hoàng Phủ Kiệt chỉ cần Vân Mộng Dược Nghiệp đổi chủ. Diệp Sở định giao công ty cho Tôn Ngữ Nhu.
- Ch.153: Diệp Sở nhờ Gia Cát Triết Nhã hợp tác, giao bài thuốc Thập Toàn Đại Bổ Hoàn và Bách Hoa Lộ. Tôn Ngữ Nhu và Gia Cát Triết Nhã tiếp nhận Vân Mộng Dược Nghiệp; Khương Quân Dao đòi mua lại bị từ chối; Hàn Mộng Quan xin hãy làm công ty lớn mạnh.
- Ch.154: Hộ Long Vệ do Lâm Tự Tại dẫn tới cổ mộ, công trường đình công; U Lan quyết ngồi chờ. Diệp Sở tới thành Kinh Khẩu khám bệnh, gặp An Tiểu Vũ — đệ tử mới của Lý Chính Nguyên — và gặp lại Tư Đồ Tĩnh.
- Ch.155: Gia chủ nhà họ Lâm ở Kinh Khẩu là Lâm Tự Như. Triệu Sâm dẫn Pháp Tàng — hòa thượng chùa Kim Sơn — tới và gọi Diệp Sở là lừa đảo; Trịnh Hiên, sư huynh của Tư Đồ Tĩnh, kiêu ngạo. Ông cụ nhà họ Lâm mắc bệnh lạ tỏa hương, Diệp Sở phát hiện hạt Hoàng Tuyền Hoa trong não.
- Ch.156: Trịnh Hiên và Tư Đồ Tĩnh bó tay; Pháp Tàng dùng tinh thần lực thấy "hạt giống"; Diệp Sở nói rõ là Hoàng Tuyền Hoa. Lâm Tự Như hứa thưởng Long Đảm Thảo trăm năm; Trịnh Hiên đòi gọi sư phụ Y Thánh Kim Lăng.
- Ch.157: Pháp Tàng đề nghị cho Kim Thiền vào ăn hạt; Lâm Tự Như chọn Pháp Tàng, phớt lờ cảnh báo của Diệp Sở rằng trong hạt có cổ trùng.
- Ch.158: Kim Thiền trúng độc, hắc khí tràn ra, ông cụ nhà họ Lâm suy kiệt nhanh; Lâm Tự Như cầu xin. Lâm Tự Tại về — là con thứ ba nhà họ Lâm — nhận ra Diệp Sở chính là Diệp thần y. Diệp Sở dùng ngân châm kéo hạt xuống bắp chân trái; Tư Đồ Tĩnh bí mật kết ấn.
- Ch.159: Hạt bùng nổ, Diệp Sở chém đứt bắp chân ông cụ nhà họ Lâm; Hoàng Tuyền Hoa nở, cổ trùng tan thành nhụy đen. Diệp Sở giữ hoa, nhận Long Đảm Thảo trăm năm; Pháp Tàng đổi liên lạc, mời tới chùa Kim Sơn. Triệu Sâm thuê người phục kích bị Diệp Sở đánh bại; một hắc y nhân đeo mặt nạ Bát Giới xuất hiện.
- Ch.160: Hắc y nhân là bán bộ đại tông sư; Diệp Sở không điều động được chân khí vì trúng độc, lần đầu bị thương từ khi ra tù. Hắn dùng khí huyết bẻ gãy tay đối thủ, lột mặt nạ: là Trịnh Hiên. Diệp Sở phế khí hải Trịnh Hiên; Tư Đồ Tĩnh đâm dao, bị đồng bì thiết cốt chặn.
- Ch.161: Tư Đồ Tĩnh khai mình chính là thánh nữ Vu Cổ Giáo tên U Lan; độc là Tam Thi độc gồm Hoàng Tuyền Hoa, Thi Cốt Trùng và U Minh Thảo, ngầm ý An Tiểu Vũ mang U Minh Thảo. Nàng rút súng bắn tỉa; Pháp Tàng xuất hiện, giao chiến.
- Ch.162: Oán Long Khí nuốt sạch Tam Thi độc và mạnh thêm. Tư Đồ Tĩnh thắng Pháp Tàng; Diệp Sở bắt nàng, bẻ gãy tay. Nàng nói đã gieo Đồng Tâm Cổ vào Khương Quân Dao (kiểm chứng thấy có cổ trong tim nàng). Diệp Sở đánh vào mông rồi thả; nàng bóp cổ Trịnh Hiên, hòa tan xác bằng nước xanh.
- Ch.163: An Tiểu Vũ hạ độc rồi giết toàn bộ hạt nhân nhà họ Lâm, chỉ Lâm Tự Tại sống; nói "năm năm trước, núi Vạn Xà Nam Cương". Tô Định Hạ từng dẫn Hộ Long Vệ diệt Vu Cổ Giáo, Lâm Tự Tại ra tay trước với đại yêu nên thành bách hộ trẻ nhất. Diệp Sở hút độc cứu Lâm Tự Tại, Triệu Sâm và Lâm Tự Mỹ.
- Ch.164: Diệp Sở suy ra Tư Đồ Tĩnh có huyết mạch yêu tộc và hận mình vì mình là sư đệ Tô Định Hạ; quyết kiếm tiền mua thiên tài địa bảo để áp chế Oán Long Khí. Hoàng Phủ Kiếm — chú hai Hoàng Phủ Thi Nguyệt — tới tiếp quản công ty; Hoàng Phủ Thi Nguyệt mất quyền, Đông Mai bị tát.
- Ch.165: Hoàng Phủ Bích Nguyệt bám được công tử nhà tỉnh trưởng nên Hoàng Phủ Thi Nguyệt mất dự án; nàng giấu Diệp Sở. Diệp Sở đề nghị mở công ty dược, nàng đồng ý dù đã ứng mười tám tỷ. Tại Giang Hoài Các gặp Hoàng Phủ Kiệt, Diệp Thiên Thành, Khương Quân Long; Khương Quân Dao bị cách chức tổng giám đốc. Hoàng Phủ Kiệt sai Sơn thúc ra tay, Hoàng Phủ Thi Nguyệt bước ra chắn trước Diệp Sở.
"""

first = BLOCK.strip().split("\n")[0]
if any(l.strip() == first for l in lines):
    print("skip (da co):", first)
else:
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block Da xay ra 136-165")
            break
    else:
        print("  CANH: khong thay ### Ràng buộc")

# ── Rebind Ràng buộc theo trạng thái ch.165 ─────────────────────
i0 = next(i for i, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
del lines[i0:]
NEW = """### Ràng buộc cho các chương sau:
- Diệp Sở và Khương Quân Dao ĐÃ LY HÔN (ch.145); Hàn Mộng Quan vẫn coi hắn là con rể và lén đưa chìa khóa nhà riêng. Khương Quân Dao mất chức tổng giám đốc tập đoàn Khương thị (ch.165), tới nhà họ Long cầu cứu đã được Long Đỉnh Thiên tha (ch.146).
- Danh tính Sở Bá Vương: Hoàng Phủ Thi Nguyệt đã biết từ ch.130–131; công chúng chỉ biết "Sở Bá Vương là đại tông sư chủ trang viên hồ Quảng Lăng và là người mua Vân Mộng Dược Nghiệp" (ch.149–150). Khương Quân Dao, Hàn Mộng Quan, Khương Hải Vân, nhà họ Diệp, nhà họ Long, nhà họ Tần, Hoàng Phủ Kiệt đều CHƯA biết mặt. Hàn Mộng Quan từng thấy giọng quen (ch.134) nhưng bị gạt đi.
- TWIST: Tư Đồ Tĩnh chính là U Lan, thánh nữ Vu Cổ Giáo (lộ ch.161). Nàng đã gieo Đồng Tâm Cổ vào tim Khương Quân Dao, giết Trịnh Hiên, thắng cả Pháp Tàng; Diệp Sở thả nàng đi sau khi bẻ gãy tay. An Tiểu Vũ (đệ tử Lý Chính Nguyên) là hung thủ hạ Tam Thi độc và thảm sát nhà họ Lâm (ch.163) — cả hai đều đang tự do.
- Nhà họ Lâm ở Kinh Khẩu tàn phá: ông cụ mất một bắp chân nhưng sống, Lâm Tự Tại sống sót, Lâm Tự Mỹ được cứu; Diệp Sở nợ Pháp Tàng một lời hẹn tới chùa Kim Sơn (ch.157–163).
- Tài chính: Diệp Sở mua Vân Mộng Dược Nghiệp giá mười tám tỷ (ch.149–150) rồi giao cho Tôn Ngữ Nhu và Gia Cát Triết Nhã (ch.153); Hoàng Phủ Thi Nguyệt đã ứng mười tám tỷ và bị Hoàng Phủ Kiếm tước quyền (ch.164–165). Hai người định mở công ty dược mới (ch.165).
- Cliffhanger ch.165: tại Giang Hoài Các, Hoàng Phủ Kiệt sai Sơn thúc ra tay với Diệp Sở; Hoàng Phủ Thi Nguyệt bước ra chắn trước mặt hắn, lạnh lùng đáp "Thì sao?" khi bị chất vấn. Diệp Sở chưa biết nàng vừa mất công ty và đang giấu. Mở đầu ch.166 phải tiếp đúng cảnh này.
- Chân Vũ Tông vẫn treo: Đông Hải Dược Vương bị Diệp Sở giết (ch.181), tông môn có thánh tử tông sư viên mãn và đại trưởng lão, Hồng Vân đã cảnh cáo sẽ trả thù. Vân Băng Uyển vẫn bị nhà họ Long ép gả vào Chân Vũ Tông.
- Oán Long Khí: sau khi nuốt Tam Thi độc càng mạnh, phải tìm Chân Long Cốt hoặc song tu với người có thể chất đặc biệt mới áp chế được (ch.151, 162). Hoàng Phủ Thi Nguyệt biết bí mật vảy rồng/vảy ngược và gọi hắn là "chân long chi tử".
- Không đổi cách gọi đã chốt (LƯU Ý ĐẶC BIỆT mục 39–48): "ông cụ" cho 老爷子 (nhưng "lão gia" cho 老爷 trong lời quản gia), "Kinh Khẩu", "Chân Vũ Tông" cho cả 真武宗 lẫn 真武门, "Tư Đồ Tĩnh = U Lan", "Diệp Thiên Trì ≠ Diệp Thiên Thành", "Hoàng Phủ Kiếm ≠ Hoàng Phủ Kiệt", "Hoàng Phủ Minh ≠ Hoàng Vệ Minh", "Đông Hải Dược Vương ≠ Dược Hoàng", "Tường Vi", "Mãn Hùng", "Tô Định Hạ".
"""
lines.extend(NEW.rstrip("\n").split("\n"))
print("  Rang buoc: da rebind theo ch.165 (%d dong)" % len(NEW.strip().split("\n")))

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 136-165. tong so dong:", len(lines))