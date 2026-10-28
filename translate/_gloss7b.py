# Chu kỳ 7 (phần 2): LƯU Ý ĐẶC BIỆT + NGỮ CẢNH ch.66–75
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "F:/taitruyen/translate/glossary_can_bao_chan_long.txt"


def cur():
    return io.open(G, encoding="utf-8").read().split("\n")


def insert_after(prefix, block):
    ls = cur()
    if any(l.startswith(block.split("\n")[0][:12]) for l in ls):
        print("  (da co)", prefix[:26])
        return
    for i, l in enumerate(ls):
        if l.startswith(prefix):
            ls[i + 1: i + 1] = block.split("\n")
            io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(ls))
            print("  + sau:", prefix[:30])
            return
    print("  !! missing anchor:", prefix[:40])


insert_after("19. Source đổi", """20. Chữ "Đao ca" trỏ HAI người khác nhau tùy chương: ch.67 → Mạnh Tiểu Đao (孟小刀), ch.74–75 → Tả Tu Đao (左修刀). Đao Sẹo Trần (刀疤陈) luôn là "Đao Sẹo ca" khi được gọi 刀疤哥 — không bao giờ viết tắt thành "Đao ca".
21. Source gõ nhầm 梦小刀 một chỗ ở ch.68 → bản dịch vẫn là "Mạnh Tiểu Đao" (không có nhân vật thứ hai tên Mộng Tiểu Đao).
22. Long Cửu Dương (龙九阳, ch.72–73, thiếu chủ Long gia) và Long Cửu gia (龙九爷, ch.39–58, người đứng tổ chức buổi đấu giá ngầm, tự giới thiệu "tại hạ Long Cửu") nhiều khả năng cùng một nhân vật, nhưng source viết hai dạng khác nhau → dịch sát theo từng chỗ, KHÔNG tự gộp thành một tên.
23. Vương Triều Dạ (夜王朝, ch.75, khu Đông Thành, tổng bộ Hắc Hổ Hội) và "câu lạc bộ đêm Vương Triều" (王朝夜总会, ch.16–17, ở Thành Nam) là hai dạng source khác nhau của cùng hệ thống "Vương Triều" — giữ đúng dạng theo chương, không tự đổi tên.
24. Cách gọi đã chốt ở ch.66–75, KHÔNG viết lại: "lão đại" (老大), "đại ca" (大哥), "hội chủ"/"phó hội chủ" (会长/会主, không viết "hội trưởng"), "đường chủ", "Báo ca", "Đao ca", "Đao Sẹo ca", "A Báo", "Mạnh Tiểu Đao", "Trần Tử Báo", "Tả Tu Đao", "Bạch Hạc lão nhân", "Kính ca", "Bạch Hiểu Hiểu", "Tường Vi", "Đường Thiên Nhận", "Long Trấn Sơn", "Long Cửu Dương", "Chân Vũ Tông", "Vương Triều Dạ", "đan văn", "lò luyện", "Khai Mạch Đan", "thuốc kích dục", "độc dược", "phí giáo dục", "tỉnh thành" (省会 — không viết "thành phố tỉnh"), "Bạch Hạc Quyền", "hoành luyện".
""")

EVENTS = """### Đã xảy ra — chương 66–75:
- Ch.66: Kính ca (đầu gấu tóc cua đeo kính, thuộc hạ Hắc Hổ Hội) mang quà hơn mười vạn tới quán ép Tôn Ngữ Nhu chia tay bạn trai; Diệp Sở đánh trọng thương đám người, bắt Kính ca về nhắn "lão đại Hắc Hổ Hội an phận, không thì tôi không ngại diệt sạch".
- Ch.67: La Tam Béo và Úy Trì Hùng cầu viện; Trần Tử Báo (Báo ca, đường chủ mạnh nhất Hắc Hổ Hội) cùng Mạnh Tiểu Đao, Bạch Hạc lão nhân xuất quân trả thù. Phe Bạch Lang Hội (Lý Đầu Trọc, Đao Sẹo Trần, Tường Vi) chuẩn bị sống mái: hội chủ đã đi tỉnh thành/Kim Lăng, Đao Sẹo Trần bị thương nặng vì mất "cơ duyên" (viên đan từng đấu giá bị cướp).
- Ch.68: Tại quán mì, Diệp Sở một tát đánh bay Mạnh Tiểu Đao (Đoán Thể bảy đoạn, tinh thông phi đao). Đao Sẹo Trần ngồi trong xe thương vụ nhìn thấy, thấy Diệp Sở quen mắt; Tường Vi phản đối chuyện đầu nhập vào thế lực khác.
- Ch.69: Bạch Hạc lão nhân (Đoán Thể chín đoạn, Bạch Hạc Quyền) không đỡ nổi một quyền của Diệp Sở — "một quyền hai mươi năm công phu, mày đỡ nổi không"; Diệp Sở bắt La Tam Béo trả "phí giáo dục" mười vạn mỗi người (hơn bốn triệu), rồi gọi thẳng ba người Bạch Lang Hội trong xe thương vụ ra.
- Ch.70: Tôn Tú Anh do dự vì Diệp Sở đã kết hôn — thời trẻ bà từng bị một công tử có vợ lừa, thành "vợ bé" bị vợ cả tìm tới cửa sỉ nhục, nên phản đối con gái đi bước; Diệp Sở chuyển ngay hai trăm triệu (两亿) bảo đổi nhà cho hai mẹ con. Tôn Ngữ Nhu chọn tin Diệp Sở.
- Ch.71: Diệp Sở gặp phó hội chủ Bạch Lang Hội Bạch Hiểu Hiểu (đang bị thương), tuyên bố thu Bạch Lang Hội làm đàn em; lấy hai viên Tiểu Chân Nguyên Đan ban cho Đao Sẹo Trần và Lý Đầu Trọc, Đao Sẹo Trần đột phá Khai Mạch tông sư. Diệp Sở dặn họ thu thập dược liệu để hắn luyện đan nâng sức cho thuộc hạ.
- Ch.72: Sinh nhật Vân Băng Uyển; bà lão Long gia tới ép nàng về làm "thiếp" cho một lão già Chân Vũ Tông. Diệp Sở đón sinh nhật cùng nàng, tặng Tử Vi Tinh và nói "tôi đã nói sẽ chịu trách nhiệm với cô". Nàng gọi video cho Gia Cát Triết Nhã vì Tử Vi Tinh vốn là món nhà họ Gia Cát mua để tặng Long Cửu Dương; Gia Cát Triết Nhã đang bận thử Bách Dược Tửu.
- Ch.73: Thân thế Vân Băng Uyển — con riêng của Long Trấn Sơn với bà bảo mẫu (bị cưỡng bức thời trẻ), mang Cửu Âm Sát Thể; nhà họ Long định gả nàng cho lão già Chân Vũ Tông làm "thiếp", thực chất là lò luyện đổi cho thiếu chủ Long Cửu Dương bái nhập tông môn. Diệp Sở luyện đan thấy đan văn, ép bà lão Long gia làm "chó" giám sát nhà họ Long.
- Ch.74: Hắc Hổ Hội tra ra Diệp Sở chỉ là kẻ ở rể nhà họ Khương; Khương Quân Hổ thuê Trần Tử Báo hủy danh Diệp Sở (thuốc kích dục + mấy gã đồng tính, tung ảnh lên mạng) để ép Khương Quân Dao ly hôn. Tả Tu Đao đổi thuốc kích dục thành độc dược, phục người chờ ra tay. Diệp Sở luyện được Khai Mạch Đan, ban hai viên; Bạch Hiểu Hiểu uống, Đao Sẹo Trần mở thêm một mạch, Lý Đầu Trọc đạt bán bộ tông sư.
- Ch.75: Diệp Sở đơn thân tới Vương Triều Dạ (tổng bộ Hắc Hổ Hội) vì biết Bạch Lang Hội đã đánh chiếm; Trần Tử Báo, Tả Tu Đao và đám đường chủ bị bắt sống, thương tích nặng. Hắn buộc Hắc Hổ Hội làm chó cho Bạch Lang Hội, dùng ngân châm khiến cả đám đau muốn chết không được, dặn "dám phản bội sẽ để các người đau đớn tới chết"; Trần Tử Báo lập tức khai âm mưu của Khương Quân Hổ ngay lúc Khương Quân Hổ gọi điện tới.
"""

ls = cur()
if not any(l.startswith("### Đã xảy ra — chương 66–75") for l in ls):
    for i, l in enumerate(ls):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            ls[i:i] = EVENTS.split("\n")
            io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(ls))
            print("  + block Da xay ra 66-75")
            break
else:
    print("  (da co) block 66-75")

RANGBUOC = """### Ràng buộc cho các chương sau:
- Âm mưu hủy danh Diệp Sở của Khương Quân Hổ (độc dược + mấy gã đồng tính, tung ảnh để ép Khương Quân Dao ly hôn) đã bị Trần Tử Báo khai ra ở cuối ch.75; Diệp Sở biết rõ và đang chuẩn bị phản đòn — chương tới là màn trả thù trực tiếp với nhà họ Khương/Khương Quân Hổ. Đừng để nhân vật "quên" chuyện này.
- Hắc Hổ Hội đã quy phục trên danh nghĩa: Tả Tu Đao (phó hội chủ) giả vờ tuân phục, trong đầu chỉ chờ "hội chủ trở về" để phản; Trần Tử Báo và đám đường chủ bị ngân châm chế ngự, hận nhưng không dám cãi. Hội chủ Hắc Hổ Hội vẫn CHƯA lộ diện; chỗ dựa ở Kim Lăng của Hắc Hổ Hội (thế lực từng dựng hội để kiềm chế Bạch Lang Hội) vẫn còn treo.
- Bạch Lang Hội thành đàn em của Diệp Sở và tiếp quản địa bàn Hắc Hổ Hội: Bạch Hiểu Hiểu, Đao Sẹo Trần, Lý Đầu Trọc, Tường Vi gọi hắn "đại nhân". Đao Sẹo Trần đã là Khai Mạch tông sư, Lý Đầu Trọc đạt bán bộ tông sư, Bạch Hiểu Hiểu đang tiến bộ nhờ Khai Mạch Đan. Bạch Lang Vương (hội chủ) vẫn vắng mặt vì thương tích — không cho xuất hiện tùy tiện, và đó là mắt xích còn treo.
- Thù cá nhân chưa xong: La Tam Béo mất hơn bốn triệu "phí giáo dục", Úy Trì Hùng thổ huyết, Kính ca bị đánh trọng thương, Mạnh Tiểu Đao bị một tát đánh bay, Bạch Hạc lão nhân thua một chiêu — không nhân vật nào trong số này được phép "hòa giải" quên lãng. Tiền Hào Sâm (ủy viên Thương hội Giang Nam) vẫn ấm ức vì bị Gia Cát Triết Nhã phạt đền tiền; Văn Tiêu Sơn (liệt chân trái) đã méc chuyện Tôn Ngữ Nhu với Tôn Tú Anh.
- Tử Vi Tinh đã tặng Vân Băng Uyển (ch.72) trong khi nhà họ Gia Cát mua nó để tặng Long Cửu Dương; Gia Cát Triết Nhã đang thử Bách Dược Tửu, chưa biết món quà đi đâu, và vẫn nghi công thức bị giấu một phần. Trái Tim Rừng Xanh vẫn để Tôn Ngữ Nhu đeo (linh khí bị cơ thể nàng hấp thu vì là Chân Vũ Linh Thể).
- Xung đột với nhà họ Long đang mở: Long Trấn Sơn muốn gả Vân Băng Uyển cho lão già Chân Vũ Tông làm lò luyện để đổi lấy việc Long Cửu Dương được bái nhập; bà lão Long gia bị Diệp Sở thu làm "chó" nhưng trong lòng định bẩm báo gia chủ trừ khử hắn (ch.73). Vân Băng Uyển là con riêng, mang Cửu Âm Sát Thể, và Diệp Sở vẫn nghi nàng có huyết mạch Long Tộc — nàng chưa biết hắn đã biết thân thế.
- Tôn Ngữ Nhu: Diệp Sở đã chuyển hai trăm triệu, Tôn Tú Anh mềm lòng nhưng vẫn phản đối con gái làm "vợ bé"; vết thương lòng của Tôn Tú Anh (từng bị một công tử có vợ lừa, bị vợ cả tìm tới cửa sỉ nhục) là mắt xích phải giữ.
- Không đổi cách gọi đã chốt (LƯU Ý ĐẶC BIỆT mục 20–24): "lão đại" ≠ "đại ca"; "hội chủ"/"phó hội chủ" (không viết "hội trưởng"); "Đao Sẹo ca" không viết tắt thành "Đao ca"; "Mạnh Tiểu Đao" (không viết "Mộng"); "Vương Triều Dạ" (夜王朝) khác "câu lạc bộ đêm Vương Triều" (王朝夜总会); "Long Cửu Dương" (龙九阳) khác "Long Cửu gia" (龙九爷); "tỉnh thành" (省会). Source viết lẫn 龙国/大夏 và 会长/会主 — dịch sát từng chỗ, không tự gộp.
"""
ls = io.open(G, encoding="utf-8").read().split("\n")
head = []
for i, l in enumerate(ls):
    if l.startswith("### Ràng buộc cho các chương sau:"):
        head = ls[:i]
        break
else:
    i = None
if i is not None:
    new = head + RANGBUOC.rstrip("\n").split("\n") + [""]
    if io.open(G, encoding="utf-8").read() != "\n".join(new):
        io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(new))
        print("  + rebind Rang buoc")
print("TONG DONG:", len(io.open(G, encoding="utf-8").read().split("\n")))
