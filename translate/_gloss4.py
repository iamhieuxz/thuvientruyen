# -*- coding: utf-8 -*-
"""Chu ky 4 (ch.36-45): chen muc tu moi + viet NGU CANH vao glossary. Idempotent."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "glossary_can_bao_chan_long.txt"

FIX = [(
    '皇甫诗月 = Hoàng Phủ Thi Nguyệt (tiểu thư nhà họ Hoàng Phủ; từ ch.11 nhận Diệp Sở làm em kết nghĩa, Diệp Sở gọi "chị Thi Nguyệt", cô gọi lại "Diệp tiên sinh" → "tiểu đệ")',
    '皇甫诗月 = Hoàng Phủ Thi Nguyệt (tiểu thư nhà họ Hoàng Phủ; từ ch.11 nhận Diệp Sở làm em kết nghĩa, Diệp Sở gọi "chị Thi Nguyệt"; cô gọi lại "Diệp tiên sinh", chỗ thân mật từ ch.36 gọi "em trai" — KHÔNG viết "tiểu đệ"/"đệ đệ")',
)]

INSERTS = [
    ("舵主 = đà chủ", [
        '王子豪 = Vương Tử Hào (công tử nhà họ Vương ở Giang Đô, em trai Vương Tử Đằng; tới buổi đấu giá ngầm cùng Khương Quân Lan, tranh Tiểu Chân Nguyên Đan với Diệp Sở, ch.37–43)',
        '王子腾 = Vương Tử Đằng (trưởng tử nhà họ Vương, giỏi cả thương nghiệp lẫn võ đạo, từng được xem là xứng đôi nhất với Khương Quân Dao, đang ở nước ngoài, ch.38)',
        '王老爷子 = ông cụ nhà họ Vương ("Vương lão gia tử"); Long Cửu gia bảo Vương Tử Hào về nhắn rằng nợ nhân tình với ông coi như xoá sạch, ch.39)',
        '龙九爷 = Long Cửu gia (nhân vật lớn nhà họ Long — "nhất môn" trong một môn hai hội ba tộc bốn nhà, chủ buổi đấu giá ngầm; cả Giang Đô phải nể, ch.38–43)',
        '龙九 = Long Cửu (cách tự giới thiệu của Long Cửu gia ở ch.39, kèm câu "rất hân hạnh được gặp")',
        '赵虎 = Triệu Hổ (một trong hai tâm phúc của Long Cửu gia, cường giả Đoán Thể tám đoạn, uống Tiểu Chân Nguyên Đan rồi đột phá lên chín đoạn ngay trên sân khấu, ch.42)',
        '刀疤陈 = Đao Sẹo Trần (đường chủ đứng đầu bốn đại đường chủ Bạch Lang Hội, tâm phúc còn lại của Long Cửu gia, Đoán Thể đỉnh phong, mặt có sẹo dài; giữ "Đao Sẹo Trần", ch.42)',
        '丹丹 = Đan Đan (người dẫn chương trình buổi đấu giá ngầm, cầm micro giới thiệu từng món, ch.40–43)',
        '赵队长 = đội trưởng Triệu (đội trưởng vệ sĩ phụ trách trật tự buổi đấu giá, đi theo Vương Tử Hào, bị Long Cửu gia đuổi vì thiên vị — KHÁC với 赵虎 Triệu Hổ, ch.38–39)',
    ]),
    ("冯汉三 = Phùng Hán Tam", [
        '<!-- Phong Han Tam con la su huynh cua To Van Son; nha ho Diep nho tri Diep So (ch.36) -->',
    ]),
    ("万药斋 = Vạn Dược Trai", [
        '王家 = nhà họ Vương (một trong ba tộc lớn ở Giang Đô, mạnh nhất trong ba đại cổ tộc vì là võ đạo gia tộc, có Khai Mạch tông sư ngồi ghế, ch.38)',
        '地下拍卖会 = buổi đấu giá ngầm (Long Cửu gia đứng tổ chức dưới tầng hầm, phải có thư mời mới vào được; NHẤT QUÁN viết "buổi đấu giá ngầm", ch.37–43)',
        '地下交易会 = chợ giao dịch ngầm (cách gọi khác của cùng nơi đó ở ch.38 — không bịa ra tên riêng khác)',
    ]),
    ("金陵市 = thành Kim Lăng", [
        '神农架 = Thần Nông Giá (vùng núi rậm nổi tiếng về dược liệu, ch.41)',
        '百药谷 = Bách Dược Cốc (thung lũng trăm vị thuốc trong Thần Nông Giá, nơi người hái thuốc tìm được Trú Nhan Thảo, ch.41 — KHÁC 百药阁 Bách Dược Các ở ch.32–33, tuyệt đối không trộn)',
    ]),
    ("百毒不侵 = bách độc bất xâm", [
        '光明体 = Quang Minh Thể (thể chất đặc biệt của Gia Cát Triết Nhã, không kém Nguyệt Hoa chi thể, ch.40)',
        '气海 = khí hải (bể khí trong cơ thể; từ ch.45 tiểu đỉnh ngụ trong khí hải. Nguồn ghi 气海 ở ch.45 nhưng 丹田 "đan điền" ở ch.31 — dịch đúng từng chỗ, không gộp hai khái niệm)',
        '内视 = nội thị (nghiêng mắt nhìn vào trong để xem khí hải, ch.45)',
        '开脉境 = Khai Mạch cảnh (cảnh giới sau Đoán Thể đỉnh phong; Hoàng Phủ Thi Nguyệt chạm đỉnh phong Đoán Thể ở ch.36, Khương Quân Dao lên Khai Mạch cảnh ở ch.44)',
    ]),
    ("万蚁噬心毒 = Vạn Nghĩ Phệ Tâm độc", [
        '小真元丹 = Tiểu Chân Nguyên Đan (đan Diệp Sở luyện bằng nồi cơm điện; võ giả Đoán Thể uống vào có thể đột phá, uống liên tiếp càng mạnh — VIẾT HOA, ch.36–43)',
        '解毒丹 = Giải Độc Đan (giải bách độc — VIẾT HOA "Giải Độc Đan", không viết "Giải độc đan", ch.36, 42–43)',
        '驻颜草 = Trú Nhan Thảo (linh chi từ Bách Dược Cốc trong Thần Nông Giá, ăn vào giữ dung mạo mười năm không già; chủ dược của Trú Nhan Đan, ch.41–44)',
        '驻颜丹 = Trú Nhan Đan (giữ dung mạo ba mươi năm, ch.44)',
        '驻颜果 = Trú Nhan Quả (hơn Trú Nhan Thảo, giữ thanh xuân vĩnh viễn, cực khó tìm, ch.44)',
        '炼药师 = luyện dược sư (người luyện đan; Long Cửu gia, Đan Đan và cả hội trường gọi Diệp Sở là "Diệp đại sư")',
    ]),
    ("银针 = ngân châm", [
        '青铜鼎 = đỉnh đồng (ch.40, khi nguồn gọi đầy đủ — KHÔNG biến thành tên riêng "Thanh Đồng Đỉnh")',
        '青铜小鼎 = đỉnh đồng nhỏ (ch.40–41)',
        '小鼎 = tiểu đỉnh (ch.41–45, dạng rút gọn của cùng một vật, theo đúng mức rút gọn của nguồn)',
        '龙魂虚空鼎 = Long Hồn Hư Không Đỉnh (do Hư Không Thần Kim chế tạo, luyện chân long chi hồn vào trong; Diệp Sở nhỏ máu nhận chủ nhờ Chân Long huyết mạch, ch.45)',
        '虚空神金 = Hư Không Thần Kim (kim loại vừa mang chức năng trữ vật vừa chống được đòn của Đoán Thể đỉnh phong, ch.45)',
        '储物功能 = chức năng trữ vật (khoảng chứa riêng bên trong tiểu đỉnh, ch.45)',
        '电饭煲 = nồi cơm điện (Diệp Sở dùng thay đỉnh luyện đan, ch.36 — cùng nghĩa với 电饭锅)',
        '电饭锅 = nồi cơm điện (ch.37 — giữ "nồi cơm điện" cho cả hai từ)',
        '真火 = chân hỏa (lửa trên đầu ngón tay khi luyện đan, ch.37)',
        '药鼎 = dược đỉnh (đỉnh luyện đan; Diệp Sở chưa có nên tạm dùng nồi cơm điện, ch.36)',
        '皇家一号 = Royal One (nước hoa Hoàng Phủ Thi Nguyệt dùng, hai triệu một chai — GIỮ NGUYÊN "Royal One" như ch.44)',
        '帝王绿佛珠 = chuỗi Phật châu Đế Vương Lục (món đắt nhất nửa đầu buổi đấu giá, bốn trăm triệu, tương truyền thời Đường, ch.40)',
        '夜明珠 = dạ minh châu (món đấu giá thứ nhất, chốt một trăm triệu, ch.40)',
        '滴血认主 = nhỏ máu nhận chủ (Diệp Sở làm theo lời Dược Hoàng, ch.44–45)',
        '邀请函 = thư mời (phải có thư mời mới vào được buổi đấu giá ngầm, ch.37–38)',
        '验资 = xác nhận tài sản (quy định chứng minh số dư trước khi trả giá; Đan Đan nói chỗ này KHÔNG có quy định đó, ch.42–43)',
        '流拍 = bị ế / rớt (đấu giá không ai trả giá — KHÔNG viết "lưu phái", ch.40)',
    ]),
    ("### Thánh Giáo (ch.31):", [
        "### Nhà họ Long / buổi đấu giá ngầm (ch.36–45):",
        '- 叶大师 → "Diệp đại sư"; 九爷 → "Cửu gia"; 龙九爷 → "Long Cửu gia"; 龙九 (tự giới thiệu) → "Long Cửu"',
        '- 王少 → "Vương thiếu"; 王家 → "nhà họ Vương"; 陈堂主 → "Trần đường chủ" (tức Đao Sẹo Trần); 赵队长 → "đội trưởng Triệu"',
        '- 叶神医 → "Diệp thần y" (Vân Băng Uyển gọi, ch.45); 云姑娘 → "cô Vân" (Diệp Sở gọi Vân Băng Uyển, nhất quán toàn ch.45); 叶小友 → "Diệp tiểu hữu" (Vân Băng Uyển gọi, ch.40)',
        '- 弟弟 (Hoàng Phủ Thi Nguyệt gọi Diệp Sở) → "em trai"; Đông Mai gọi Diệp Sở là "Diệp đại sư"',
        '- Khương Quân Lan / Vương Tử Hào → Diệp Sở: "đồ vô dụng", "cậu nhóc"; giữ đúng ngôi kể, không đổi vai giữa Vương Tử Hào và đội trưởng Triệu',
    ]),
]

TAIL_ITEMS = [
    "",
    "8. Quy đổi tiền (đã kiểm chứng lại toàn bộ ch.36–45): 1亿 tương đương 100 TRIỆU (KHÔNG phải 1 tỷ); 1万 tương đương 10 nghìn.",
    '   Ví dụ: 两千万 → "hai mươi triệu"; 一亿 → "một trăm triệu"; 三十七亿 → "ba tỷ bảy trăm triệu"; 七十一亿 → "bảy tỷ một trăm triệu"; 四亿五千万 → "bốn trăm năm mươi triệu"; 三亿 → "ba trăm triệu".',
    '   Chỉ giữ chữ "vạn" khi nhân vật nói thẳng theo 万 (2.000 vạn ở ch.26–33). Không đổi thang đo giữa chừng trong cùng một cảnh.',
    "",
    "9. Bách Dược CỐC (thung lũng ở Thần Nông Giá, ch.41 — nơi có Trú Nhan Thảo) KHÁC Bách Dược CÁC (tiệm dược nhà họ Vân ở chợ Nam Thành, ch.32–33). Không dùng lẫn.",
    "10. Vương Tử Hào, Đao Sẹo Trần và đội trưởng Triệu là ba người khác nhau; Triệu Hổ là tâm phúc của Long Cửu gia, KHÔNG phải đội trưởng Triệu đi kèm Vương Tử Hào.",
    '11. Đan dược luôn VIẾT HOA: Tiểu Chân Nguyên Đan, Giải Độc Đan, Trú Nhan Đan/Thảo/Quả. Hoàng Phủ Thi Nguyệt gọi Diệp Sở là "em trai" — không dịch 弟弟 thành "tiểu đệ" hay "đệ đệ".',
]

CONTEXT = """### Đã xảy ra — chương 36–45:
- Ch.36: Nhà họ Diệp nhờ Diệp Sở "hẹn gặp Khương tiểu thư" để nối lại hợp tác; hắn mặc cả từ một trăm triệu xuống hai mươi triệu, nhận chuyển khoản xong để họ chờ dài cổ. Diệp Thiên Thành bí mật nhờ Tô Vạn Sơn giới thiệu sư huynh của y là Phùng Hán Tam (Đoán Thể tám đoạn, Ưng Trảo Công) để trị Diệp Sở. Cùng lúc, tại biệt thự nhà họ Hoàng Phủ, Diệp Sở đi mượn NỒI CƠM ĐIỆN để luyện đan; Hoàng Phủ Thi Nguyệt uống đan đột phá lên Đoán Thể đỉnh phong (chỉ còn một cơ duyên nữa là tới Khai Mạch cảnh), xin thêm đan và cho cả Đông Mai.
- Ch.37: Diệp Sở luyện đan dưới tầng hầm biệt thự (Giải Độc Đan trước, Tiểu Chân Nguyên Đan sau), cho Đông Mai một viên — y uống xong đột phá lên Đoán Thể. Ba người tới buổi đấu giá ngầm thì va phải Khương Quân Lan đi cùng Vương Tử Hào; hai kẻ này chê Diệp Sở là "đồ vô dụng", không xứng với Khương Quân Dao, dọa "anh cả tôi về thì cậu hối không kịp".
- Ch.38: Vương Tử Hào ra lệnh cho Diệp Sở ly hôn, khoe anh cả Vương Tử Đằng (đang ở nước ngoài) và thế lực nhà họ Vương — tộc mạnh nhất trong ba đại cổ tộc vì có Khai Mạch tông sư. Hắn gọi đội trưởng Triệu kiểm tra thư mời để đuổi Diệp Sở; bên nhà họ Hoàng Phủ ra mặt, "xem ai dám động vào hắn".
- Ch.39: Đông Mai đánh hai cái tát vào mặt Khương Quân Lan. Long Cửu gia — chủ buổi đấu giá, áo tím, ngoài dịu trong dữ — tới, quát đội trưởng Triệu, đích thân xin lỗi Hoàng Phủ Thi Nguyệt vì "ngự hạ không nghiêm", rồi đuổi đội trưởng Triệu vì tội thiên vị. Với Vương Tử Hào, ông nói hôm nay không truy cứu, "về nhắn Vương lão gia tử: phần nợ nhân tình giữa ông ấy và tôi coi như xóa sạch". Sau đó ông gọi Diệp Sở là "Diệp đại sư", tự giới thiệu "tại hạ Long Cửu".
- Ch.40: Nửa đầu buổi đấu giá: dạ minh châu chốt một trăm triệu, đồ cổ thời Hán một trăm năm mươi triệu, chuỗi Phật châu Đế Vương Lục bốn trăm triệu. Gia Cát Triết Nhã và Vân Băng Uyển xuất hiện; Diệp Sở thả ra một tia chân khí dò ra Gia Cát Triết Nhã mang QUANG MINH THỂ (thể chất đặc biệt không kém Nguyệt Hoa chi thể) nên để ý ngay. Món thứ mười là một cái đỉnh đồng nhỏ vỡ nát, suýt bị ế, Diệp Sở trả mười một triệu mua, bị cười là mua đồ vỡ.
- Ch.41: Trú Nhan Thảo ra sàn, khởi điểm một trăm triệu; Hoàng Phủ Thi Nguyệt và Gia Cát Triết Nhã tranh nhau, Diệp Sở giảng hòa "cây này giao tôi, luyện thành đan mỗi người một viên" → chốt một tỷ, Gia Cát Triết Nhã mua. Một cuốn công pháp vũ đạo (chỉ tu tới Đoán Thể đỉnh phong) chốt một tỷ hai trăm triệu.
- Ch.42: Long Cửu gia cho Triệu Hổ (một trong hai tâm phúc) uống đan ngay trên sân khấu, Đoán Thể tám đoạn lên chín đoạn, cả trường bùng nổ. Bốn viên Giải Độc Đan (khởi điểm mỗi viên một trăm triệu) bán chậm; ba viên Tiểu Chân Nguyên Đan khởi điểm năm trăm triệu: viên nhất bị Vân Băng Uyển giành bằng danh nghĩa nhà họ Vân, viên nhì Đao Sẹo Trần (đứng đầu bốn đường chủ Bạch Lang Hội, Đoán Thể đỉnh phong) trả một tỷ một trăm triệu nên không ai dám tranh.
- Ch.43: Viên thứ ba thành cuộc chiến giá giữa Vương Tử Hào và Diệp Sở — Vương Tử Hào tố Diệp Sở không có tiền, Đan Đan đáp chỗ này không có quy định xác nhận tài sản; Diệp Sở mỗi lần chỉ tăng hai mươi triệu, ép đối phương tới một tỷ năm trăm triệu. Ba viên tổng cộng ba tỷ bảy trăm triệu, toàn bộ vào túi Diệp Sở; bốn viên Giải Độc Đan chỉ được bốn trăm năm mươi triệu. Long Cửu gia chuyển đủ bảy tỷ một trăm triệu — Diệp Sở tưởng bị trừ ba mươi phần trăm phí, chỉ còn năm tỷ, ai ngờ ông miễn phí vì nể Hoàng Phủ Thi Nguyệt. Cùng chương: trong lòng Khương Quân Dao đã phỏng đoán "Diệp đại sư" chính là Diệp Sở; ở nhà, Hàn Mộng Quan kiểm tra thẻ thấy một triệu bà đưa cho Diệp Sở còn số dư 0, Khương Hải Vân được thể hô ly hôn; Diệp Sở đoán ông ta gọi ngân hàng chuyển tiền đi, nhưng Hàn Mộng Quan quát "cậu thật sự khiến tôi quá thất vọng".
- Ch.44: Diệp Sở chuyển trả một triệu một trăm nghìn, nói dối "một người bạn mở sòng bạc nhờ đầu tư, thắng được mười vạn"; Hàn Mộng Quan hết giận, Khương Hải Vân không hiểu tiền ở đâu ra. Khương Quân Dao vẫn nghi vì ngửi mùi nước hoa Royal One (hai triệu một chai) trên áo hắn, tuyên bố "tìm phụ nữ tùy ý, đừng dắt về nhà", rồi uống đan đột phá Đoán Thể đỉnh phong lên Khai Mạch cảnh. Diệp Sở về phòng nhỏ máu lên đỉnh đồng theo lời Dược Hoàng; lớp gỉ đồng rơi hết, lộ ra Long Hồn Hư Không Đỉnh.
- Ch.45: Tiểu đỉnh hóa một đạo thanh quang nhập KHÍ HẢI của Diệp Sở; vì mang Chân Long huyết mạch nên y nhận chủ dễ dàng, Oán Long Khí từ đó không còn phản phệ. Trong đỉnh có chữ cổ rất huyền ảo nhưng y không đọc được. Vân Băng Uyển gọi mời Diệp Sở đi khám cho mẹ của một người bạn, cảm ơn năm đó hắn nói giúp nhà họ Vân trước Lý Tĩnh Huyên, rồi ngỏ ý "giới thiệu mấy cô gái ưu tú" → Diệp Sở: "cô Vân như vậy là không tệ rồi, tôi rất thích."

"""

REBIND = """### Ràng buộc cho các chương sau:
- Quan hệ Diệp Sở – Khương Quân Dao vẫn là vợ chồng trên danh nghĩa; cô vẫn nghi hắn nuôi vợ bé (mùi nước hoa Royal One) nhưng đã uống đan của hắn để lên Khai Mạch cảnh. Diệp Sở cần tiếp xúc thể chất đặc biệt để đàn áp Oán Long Khí — đã xác nhận Gia Cát Triết Nhã mang Quang Minh Thể, mục tiêu mới.
- Diệp Sở đã có Long Hồn Hư Không Đỉnh ngụ trong khí hải (chức năng trữ vật, chịu được đòn Đoán Thể đỉnh phong) và Chân Long huyết mạch giúp Oán Long Khí ổn định, không còn cảnh phản phệ như ch.31. Đan dược là nguồn thu chính: đã bán khoảng bảy tỷ một trăm triệu qua buổi đấu giá ngầm.
- Quan hệ mới: Long Cửu gia (nhà họ Long — "nhất môn" của Giang Đô) coi Diệp Sở là "Diệp đại sư", đã xoá nợ nhân tình với Vương lão gia tử để bênh hắn; Hoàng Phủ Thi Nguyệt và Đông Mai đã uống đan của y, Thi Nguyệt gọi y là "em trai" và ngày càng mềm lòng; Vân Băng Uyển chủ động tiếp cận (đã nhờ đi khám bệnh); Gia Cát Triết Nhã trả một tỷ mua Trú Nhan Thảo và được hứa chia đan.
- Xung đột chưa giải quyết: nhà họ Vương (Vương Tử Hào mất mặt, Vương Tử Đằng ở nước ngoài sắp về — ch.38); Bạch Lang Hội (Đao Sẹo Trần mua đan nhưng chưa phục); Thánh Giáo (đà chủ Kim Lăng vẫn điều tra cái chết Cửu trưởng lão và "thu lưới bên nhà họ Lý"); Tiền Hâm và bố (ủy viên Thương hội Giang Nam); Hắc Hổ Hội; Khương Quân Lan cùng Trần Mỹ Tĩnh vẫn thù; đặc biệt nhà họ Diệp đã nhờ Phùng Hán Tam trị Diệp Sở (ch.36) và vẫn giục hắn sắp xếp cho gặp Khương tiểu thư.
- Treo: thân thế Diệp Sở chưa kể (ch.35); chữ cổ trong đỉnh chưa dịch được (ch.45); hợp tác Hoàng Phủ – Khương chưa chốt; Khương Quân Long sắp nhậm chức tổng giám đốc Tập đoàn Khương Thị; vụ "một triệu trong thẻ" đã qua mặt Hàn Mộng Quan nhưng Khương Hải Vân và Khương Quân Dao vẫn nghi; bệnh nhân mà Vân Băng Uyển nhờ khám là mẹ của ai (ch.45).
- Không đổi cách gọi đã chốt ở mục "LƯU Ý ĐẶC BIỆT" (Hàn Mộng Quan, Tạ Vũ Sâm, Lâm Huyển Huyển, Hoàng Phủ, Lý Đầu Trọc, Thệ Tâm Cổ, Bạch Lang Hội, Đao Sẹo Trần, "Hoàng phu nhân", "Tam gia", "em trai", "Diệp đại sư", "Long Cửu gia"/"Cửu gia").
"""

text = io.open(P, encoding="utf-8").read()
lines = text.split("\n")


def has(sub):
    return any(s.strip() == sub for s in lines)


for old, new in FIX:
    if old in text:
        lines = [new if l.strip() == old.strip() else l for l in lines]
        print("fix:", new[:44])

for anchor, block in INSERTS:
    if has(block[0]):
        print("bo qua (da co):", anchor)
        continue
    idx = next((i for i, l in enumerate(lines) if l.strip().startswith(anchor)), None)
    if idx is None:
        print("!! KHONG TIM THAY ANCHOR:", anchor)
        continue
    lines[idx + 1:idx + 1] = block
    print("chen sau", anchor, "->", len(block), "dong")

if not any(l.startswith("8. Quy đổi tiền") for l in lines):
    i = next(k for k, l in enumerate(lines) if l.startswith("## ══════ VĂN PHONG"))
    lines[i:i] = TAIL_ITEMS + [""]
    print("them LƯU Ý ĐẶC BIỆT item 8-11")

if not any(l.startswith("### Đã xảy ra — chương 36–45") for l in lines):
    i = next(k for k, l in enumerate(lines) if l.startswith("### Ràng buộc"))
    lines[i:i] = CONTEXT.strip("\n").split("\n") + [""]
    print("them block NGỮ CẢNH 36-45")

if any("vợ chồng trên danh nghĩa; Diệp Sở cần tiếp xúc thể chất đặc biệt để tu luyện" in l for l in lines):
    i = next(k for k, l in enumerate(lines) if l.startswith("### Ràng buộc"))
    lines[i:] = REBIND.strip("\n").split("\n")
    print("viet lai Ràng buộc")

out = "\n".join(lines).rstrip("\n") + "\n"
io.open(P, "w", encoding="utf-8", newline="\n").write(out)
print("==>", len(out), "chars,", out.count("\n"), "lines")
