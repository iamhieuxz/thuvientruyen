# -*- coding: utf-8 -*-
from pathlib import Path

D = Path(r"F:\taitruyen\data\baojian_vi")


def fix(fn, reps):
    p = D / fn
    s = p.read_text(encoding="utf-8")
    orig = s
    for old, new in reps:
        n = s.count(old)
        if n == 0:
            print(f"[MISS] {fn}: {old[:80]!r}")
            continue
        s = s.replace(old, new)
        print(f"[OK {n}] {fn}: {old[:50]!r}")
    if s != orig:
        p.write_text(s, encoding="utf-8")


fix("_0101_cat.md", [
    ("vua cờ bạc Diệp Hán, thánh cờ bạc", "vua cờ bạc họ Diệp, thánh cờ bạc"),
    ("vẫn một mặt khó xử", "vẫn vẻ mặt khó xử"),
    ("thiếu tướng năm năm lăm", "thiếu tướng năm 1955"),
    ("các bộ ủy quan trọng", "các bộ và ủy ban quan trọng"),
    ("Nghe lời lão Thái", "Nghe lời lão Vân"),
    ("bảo Hiên mang ít nước", "bảo Hiên Tử mang ít nước"),
    ("Ông Vân, hôm nay tôi chỉ dắt Đại Hoàng ra dạo cho khuây khỏa, cũng không định tham gia chọi chó gì đâu",
     "Chú Vân, hôm nay con chỉ dắt Đại Hoàng ra dạo cho khuây khỏa, cũng không định tham gia chọi chó gì đâu"),
])

fix("_0102_cat.md", [
    ("Thiếu gia Thái", "Cậu Thái"),
    ("thiếu gia Đinh", "cậu Đinh"),
    ("nể mặt già này của lão Thường ta thì bỏ qua đi", "nể mặt lão Thường tôi thì bỏ qua đi"),
    ("sao con dám gây chuyện trong trang viên của người chứ?", "sao cháu dám gây chuyện trong trang viên của ông chứ?"),
    ("Tứ ca, người nói gì vậy", "Tứ ca, anh nói gì vậy"),
    ("giới thiệu với người một người bạn lâu năm", "giới thiệu với anh một người bạn lâu năm"),
    ("nếu không thì hắn cũng không dẫn được Tạ Đại Chí", "nếu không thì ông ta cũng không dẫn được Tạ Đại Chí"),
    ("sáng ý của cậu thật không tồi", "ý tưởng của cậu thật không tồi"),
    ("người cứ tùy ý chọn", "ông cứ tùy ý chọn"),
    ("cứ nửa đỏ nửa không", "nửa nổi nửa chìm"),
    ("một Phật ra đời hai Phật lên trời", "tức đến mức lộn ruột"),
    ("về nhà đừng có học lỏm mẹ mày", "về nhà đừng có mách mẹ mày"),
    ("giả làm cháu con", "giả làm cháu ngoan"),
    ("người phụ nữ dáng cao đi ngang qua", "người phụ nữ dáng cao ráo đi ngang qua"),
    ("Tạ Hiên cười gian, cậu biết bố chỉ nói cho vui", "Tạ Hiên cười gian, cậu ta biết bố chỉ nói cho vui"),
    ("đương trường đứng dậy ra khỏi hội sở", "lập tức đứng dậy ra khỏi hội sở"),
])

fix("_0103_cat.md", [
    ("**chẳng sai là bao", "chẳng sai là bao"),
    ("**trong lòng Tần Phong bỗng giảm đi rất nhiều", "nỗi khao khát trong lòng Tần Phong bỗng giảm đi rất nhiều"),
    ("khi bị **thôi thúc", "khi bị dục vọng thôi thúc"),
    ("tìm rắc rối cho cậu ta", "tìm rắc rối cho hắn"),
    ("Phong ca", "anh Phong"),
    ("Phong lão đại", "anh Phong"),
    ("chỉ là hôm nay cậu chỉ muốn dắt Đại Hoàng ra ngoài chạy nhảy tự do, chọi gà không hấp dẫn cậu lắm",
     "chỉ là hôm nay hắn chỉ muốn dắt Đại Hoàng ra ngoài chạy nhảy tự do, chọi gà không hấp dẫn hắn lắm"),
    ("cậu không muốn hại người sống", "hắn không muốn hại người sống"),
    ("lão Vân đang bận rộn ở đó thấy cậu", "lão Vân đang bận rộn ở đó thấy hắn"),
])

fix("_0104_cat.md", [
    ("một ly vang đỏ", "một ly rượu vang đỏ"),
    ("Hiên tử", "Hiên Tử"),
    ("đồ cổ giả cao cấp", "đồ cổ nhái cao cấp"),
    ("chạm trường", "đụng trường"),
    ("chó ngao Kavkaz", "chó ngao Nga"),
    ("thỉnh thoảng có Tây Tạng Ngao", "thỉnh thoảng có chó ngao Tây Tạng"),
    ("Gấu Chó", "Gấu"),
    ("con chó Thổ Tá ông nuôi", "con chó Tosa Ngô Binh nuôi"),
    ("ông chủ Mã tỉnh Ký", "ông chủ Mã ở tỉnh Ký"),
    ("trường đua ngựa bể bơi", "trường đua ngựa, bể bơi"),
    ("cậu không biết cuộc sống đó rốt cuộc là như thế nào", "hắn không biết cuộc sống đó rốt cuộc là như thế nào"),
    ("Đại Hoàng của cậu và chó ngao Nga của Thái Đông", "Đại Hoàng của hắn và chó ngao Nga của Thái Đông"),
    ("ngoài hai con của chú cháu ta ra", "ngoài hai con của chú cháu mình ra"),
])

fix("_0105_cat.md", [
    ("Chương Một Trăm Linh Năm: Chọi Chó (Bảy)\n\n", ""),
    ("ai bảo mày dùng con chó đất Tosa của lũ Nhật Bản chứ?", "ai bảo mày dùng con chó Tosa của bọn Nhật chứ?"),
    ("chó chỉ điểm Đức, chó bun Phanh, chó Mastiff, chó Đại Đan và chó ngao Pháp",
     "chó chỉ điểm Đức, chó Bull Terrier Anh, chó Mastiff, chó Đan Mạch và chó ngao Pháp"),
    ("hắn không ngờ lão Tề lại có lượng bụng nhỏ nhen đến thế", "ông ta không ngờ lão Tề lại có độ lượng nhỏ nhen đến thế"),
    ("nếu hắn thua thì sau này còn mặt mũi nào", "nếu ông ta thua thì sau này còn mặt mũi nào"),
    ("bảo hắn đàng hoàng vứt bỏ chuyện làm ăn", "bảo ông ta đàng hoàng vứt bỏ chuyện làm ăn"),
    ("lão Tề rất thiếu đức", "lão Tề chơi rất xấu"),
    ("mấy năm trước hắn đầu tư hơn một triệu tệ", "mấy năm trước ông ta đầu tư hơn một triệu tệ"),
    ("người bạn hợp tác kia của hắn đã nảy sinh", "người bạn hợp tác kia của ông ta đã nảy sinh"),
    ("bạn thân từ nhỏ lớn lên cùng nhau", "bạn thân từ nhỏ"),
    ("hắn không thể nào đem mối làm ăn", "ông ta không thể nào đem mối làm ăn"),
    ("khẽ kéo nhẹ vạt áo hắn", "khẽ kéo nhẹ vạt áo ông ta"),
    ("Tần Phong nhẹ giọng nói bên tai hắn", "Tần Phong nhẹ giọng nói bên tai ông ta"),
    ("sau này tôi mà thấy hắn là tránh", "sau này tôi mà thấy lão ta là tránh"),
    ("cho nên hắn chiếm hơn nửa số cổ phần", "cho nên ông ta chiếm hơn nửa số cổ phần"),
    ("lão Triệu muốn đuổi hắn đi, đánh vào cái chủ ý rắn nuốt voi, khiến hắn vì không giữ được thể diện",
     "lão Triệu muốn đuổi ông ta đi, toan tính rắn nuốt voi, khiến ông ta vì không giữ được thể diện"),
    ("đối xử với cậu thật sự không tệ", "đối xử với hắn thật sự không tệ"),
    ("thân giá mới lên được vạn", "thân giá mới lên tới một vạn"),
    ("cậu cũng không đành lòng nhìn Ngô Binh", "hắn cũng không đành lòng nhìn Ngô Binh"),
    ("là vì hắn không muốn bị đối phương dắt mũi", "là vì ông ta không muốn bị đối phương dắt mũi"),
    ("hắn biết lão Tề có thân gia ba chục triệu", "ông ta biết lão Tề có thân gia ba chục triệu"),
    ("phải phong chó!", "phải cách ly chó!"),
    ("Cái gọi là phong chó", "Cái gọi là cách ly chó"),
])

fix("_0106_cat.md", [
    ("Phong tỏa chó tám mươi phút?", "Cách ly chó tám mươi phút?"),
    ("yêu cầu hắn đợi một tiếng đồng hồ", "yêu cầu ông ta đợi một tiếng đồng hồ"),
    ("đòi phong tỏa chó", "đòi cách ly chó"),
    ("chỉ có điều hắn không ngờ đối phương", "chỉ có điều ông ta không ngờ đối phương"),
    ("hắn không biết tại sao lại tin Tần Phong", "ông ta không biết tại sao lại tin Tần Phong"),
    ("người phân xử xem", "ông phân xử xem"),
    ("tôi sẽ làm công chứng", "tôi sẽ đứng ra làm chứng"),
    ("cái danh Thường Lão Tứ", "cái danh Thường Tứ gia"),
    ("lời người tôi tin được", "lời ông tôi tin được"),
    ("làm phiền Tứ gia làm công chứng", "làm phiền Tứ gia làm chứng"),
    ("ông ta hút nước tới mười phần trăm", "ông ta hút thành mười phần trăm"),
    ("kiếm chắc được 100 vạn", "kiếm chắc được một trăm vạn"),
    ("một ván chọi chó mà số tiền đặt cược hai bên lên tới một ngàn vạn", "một ván chọi chó mà số tiền đặt cược hai bên lên tới mười triệu"),
    ("người không cần nói thêm nữa", "ông không cần nói thêm nữa"),
    ("trông coi chó của A Binh và Tổng giám đốc Tề cho ta", "trông coi chó của A Binh và Tổng giám đốc Tề cho tôi"),
    ("người yên tâm, không ai có thể giở trò", "ông yên tâm, không ai có thể giở trò"),
    ("mười phần trăm hút nước", "mười phần trăm hút thành"),
    ("làm nghề xin giấy phép", "chạy giấy phép"),
    ("tuy số tiền cá cược trận này xa không bằng", "tuy số tiền cá cược trận này còn xa mới bằng"),
    ("qua màu lông của chó phân biệt", "dựa vào màu lông của chó để phân biệt"),
    ("cậu phát hiện người vẫn còn giữ được bình tĩnh", "hắn phát hiện người vẫn còn giữ được bình tĩnh"),
    ("trong lòng Ngô Binh vẫn sẽ có chút căng thẳng", "trong lòng Ngô Binh vẫn có chút căng thẳng"),
])

fix("_0107_cat.md", [
    ('Tần Phong cười dắt "Zorro" từ trong chuồng ra, cười nói', 'Tần Phong mỉm cười dắt "Zorro" từ trong chuồng ra, nói'),
    ("cậu mới bằng lòng ra tay giúp", "hắn mới bằng lòng ra tay giúp"),
    ("thấy cậu vuốt ve chó một cái", "thấy hắn vuốt ve chó một cái"),
    ("Pitbull thật sự không thể để vua gặp vua", "Pitbull đúng là không thể để hai con vua gặp nhau"),
    ("Đầu tàu hỏa", "Đầu Tàu"),
    ("đầu tàu hỏa", "Đầu Tàu"),
    ("Đầu tàu, giết nó đi", "Đầu Tàu, giết nó đi"),
])

fix("_0108_cat.md", [
    ("CHƯƠNG 109: CHỌI CHÓ (10)\n\n", ""),
    ("Đầu Máy Xe Lửa", "Đầu Tàu"),
    ("con chó Thổ Tá năm ấy", "con chó Tosa năm ấy"),
    ("Thường Lão Tứ tôi đây", "Thường Tứ gia tôi đây"),
    ("nhân phẩm của Thường Lão Tứ", "nhân phẩm của Thường Tứ gia"),
    ("được lệnh đi phong tỏa chó", "được lệnh đi cách ly chó"),
    ("tôi không nói ngài", "tôi không nói ông"),
    ("ngài dạy phải", "ông dạy phải"),
    ("ngài thật lợi hại", "ông thật lợi hại"),
    ("Tứ ca, phiền ngài bận tâm rồi.", "Tứ ca, phiền anh bận tâm rồi."),
    ("ngài cứ bận, ta nói chuyện sau.", "anh cứ bận, mình nói chuyện sau."),
    ("phát hiện cậu và Tạ Hiên", "phát hiện hắn và Tạ Hiên"),
    ("ăn cơm nhà thờ tổ đập nồi nhà thờ tổ", "ăn cháo đá bát"),
    ("tiêm cho nó một mũi bôi ít thuốc đã", "tiêm cho nó một mũi, bôi chút thuốc đã"),
    ("khiến cậu chỉ muốn nôn, cậu cũng chẳng có chút khẩu vị nào", "khiến cậu ta chỉ muốn nôn, cậu ta cũng chẳng có chút khẩu vị nào"),
    ("Thằng nhóc cậu, đúng là một kẻ quái dị.", "Thằng nhóc này, đúng là một kẻ quái dị."),
])

fix("_0109_cat.md", [
    ("CHƯƠNG 110: KHIÊU KHÍCH (THƯỢNG)\n\n", ""),
    ("chú Ngô ta dù bỏ cả cái thân này cũng làm cho cháu xong", "chú Ngô dù bỏ cả cơ nghiệp này cũng làm cho cháu xong"),
    ("hơn nữa cậu đúng là không định", "hơn nữa hắn đúng là không định"),
    ("dưới sự mưa dầm thấm lâu của Tái Thị", "dưới sự ảnh hưởng lâu ngày của Tái Thị"),
    ("khi bạn sa sút lâm nạn", "khi con người ta sa sút lâm nạn"),
    ("Không muốn ở thì ta đi thôi", "Không muốn ở thì chúng ta đi thôi"),
    ("sự xung kích mà cái máu me và tàn khốc đó mang lại cho tâm lý con người", "cú sốc mà sự máu me và tàn khốc đó gây ra cho tâm lý con người"),
    ("chó ngao Kavkaz", "chó ngao Nga"),
    ("quy củ 'chạm sàn'", "quy củ 'đụng trường'"),
    ("Ái, tôi nói này", "Này, tôi nói này"),
    ("năm xưa khi cậu dắt em gái nhặt rác ăn xin", "năm xưa khi hắn dắt em gái nhặt rác ăn xin"),
    ("Khích tướng đối với cậu mà nói", "Khích tướng đối với hắn mà nói"),
    ("Tần Phong trong lòng sốt ruột, cậu biết tính khí Đại Hoàng", "Tần Phong trong lòng sốt ruột, hắn biết tính khí Đại Hoàng"),
    ("lộ ra một cỗ chiến ý", "lộ ra một luồng chiến ý"),
    ("khiến sắc mặt Ngô Binh mấy người cũng có chút biến đổi", "khiến sắc mặt Ngô Binh và mấy người cũng có chút biến đổi"),
])

fix("_0110_cat.md", [
    ("CHƯƠNG 111: KHIÊU KHÍCH (HẠ)\n\n", ""),
    ("“Gâu… gâu…”", "“Gừ… gừ…”"),
    ("“Gâu… gâu gâu…”", "“Gừ… gừ gừ…”"),
    ("Thái tiên sinh, nhà ngài nghiệp lớn thế", "Ông Thái, nhà ông nghiệp lớn thế"),
    ("Cuộc sống đã dạy anh từ lâu rồi", "Cuộc sống đã dạy hắn từ lâu rồi"),
    ("chuyện này không liên quan đến ngài chứ nhỉ", "chuyện này không liên quan đến ông chứ nhỉ"),
    ("sới của ngài chẳng lẽ không phải để chọi chó sao", "sới của ông chẳng lẽ không phải để chọi chó sao"),
    ("chó ngao Kavkaz", "chó ngao Nga"),
    ("Sỉ nhục anh không sao", "Sỉ nhục hắn không sao"),
    ("như người thân của anh vậy", "như người thân của hắn vậy"),
    ("chắn trước mặt anh", "chắn trước mặt hắn"),
    ("'bính trường'", "'đụng trường'"),
    ("định trường và bính trường", "định trường và đụng trường"),
    ("Bính trường, vừa mới hẹn xong", "Đụng trường, vừa mới hẹn xong"),
    ("xin lỗi ông mày một câu", "xin lỗi ông đây một câu"),
    ("Hắn cùng Thái Đông và Ngô Binh một ý nghĩ", "Hắn và Thái Đông cùng một ý nghĩ"),
    ("Ngài nói gì thế?", "Ông nói gì thế?"),
    ("Anh không muốn dính dáng", "Hắn không muốn dính dáng"),
    ("Thằng nhóc tôi nghèo", "Tôi nghèo"),
    ("Lấy chó ngao Nga so với chó nhà nuôi, cũng hay lắm nhỉ.", "Lấy chó ngao Nga so với chó nhà nuôi, cũng không biết ngượng à."),
])
