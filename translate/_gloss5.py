# QA chu ky 5 — cap nhat glossary_can_bao_chan_long.txt cho ch.46-55.
# Chen theo ANCHOR (nguyen van dau mot dong); idempotent: block da co thi bo qua.
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = pathlib.Path(r"F:\taitruyen\translate\glossary_can_bao_chan_long.txt")
lines = P.read_text(encoding="utf-8").split("\n")

INSERTS = [
    ("姜君龙 = Khương Quân Long", [
        "姜丰年 = Khương Phong Niên (tên thật của \"ông cụ\"/老爷子 — gia chủ nhà họ Khương, người ngồi ghế trên cùng trong gia yến và phòng họp, ch.50–55)",
        "姜海风 = Khương Hải Phong (đại phòng, anh cả Khương Hải Vân, chồng Trần Mỹ Tĩnh, bố Khương Quân Long — KHÔNG nhầm với Khương Hải Vân)",
        "姜海韵 = Khương Hải Vận (đại cô/大姑, trưởng nữ nhà họ Khương, mẹ Trương Bích Nguyệt, mẹ chồng tương lai của Tôn Đào — chỉ lệch một chữ với 姜海云 Khương Hải Vân, phải dựa vào source để phân biệt, ch.50–55)",
        "姜君虎 = Khương Quân Hổ (con trai đại phòng, em họ Khương Quân Dao; gọi Khương Hải Vân là \"Nhị thúc\", Hàn Mộng Quan là \"Nhị thẩm\", tự xưng \"cháu\" — KHÁC với Khương Quân Lan, ch.50–54)",
        "张碧月 = Trương Bích Nguyệt (con gái Khương Hải Vận, bạn gái Tôn Đào; source viết theo họ cha nên là 张碧月 — KHÔNG viết \"Khương Bích Nguyệt\", ch.50–54)",
        "孙涛 = Tôn Đào (bạn trai Trương Bích Nguyệt, quản lý bộ phận chi nhánh khu Đông ngân hàng Giang Nam, hay khoa rằng quen Giám đốc Lý, ch.50–54)",
    ]),
    ("管家 = quản gia", [
        "",
        "## ══════ GIA TỘC LÝ (ch.46–55) ══════",
        "",
        "李广陵 = Lý Quảng Lăng (gia chủ nhà họ Lý, giám đốc chi nhánh Giang Đô của ngân hàng Giang Nam; được Diệp Sở cứu mẹ nên một lòng kết thân, ch.46–55)",
        "李广寒 = Lý Quảng Hàn (chị cả nhà họ Lý, đã gả đi, ngang ngược đa nghi; chồng làm phó cục trưởng cục cảnh sát; source vẫn gọi bà là 李小姐 \"Lý tiểu thư\" và 李女士 \"Lý nữ sĩ\" — giữ nguyên, đừng sửa thành \"Lý đại tỷ\")",
        "李广江 = Lý Quảng Giang (em trai út nhà họ Lý, đồ đệ của Cát đại sư, tự hạ cổ trùng lên mẹ mình để ép khai vật gia truyền, bị Diệp Sở phế tứ chi, ch.46–49)",
        "张莹 = Trương Oánh (vợ Lý Quảng Lăng, bạn thân của Vân Băng Uyển; Vân Băng Uyển gọi \"chị Oánh\" vì bà lớn hơn, ch.46–48)",
        "葛大师 = Cát đại sư (lão già áo dài, cổ sư theo Thánh Giáo, thầy của Lý Quảng Giang; diễn kịch đôi để \"cứu\" lão phu nhân. CHỈ viết \"Cát đại sư\", không viết \"đại sư Cát\")",
        "长衫老者 = lão già áo dài (cách source gọi Cát đại sư trước khi lộ tên — giữ \"lão già áo dài\", ch.46–49)",
        "江南银行 = ngân hàng Giang Nam (ngân hàng tư nhân lớn nhất tỉnh Giang Nam, phía sau là nhà họ Mộ Dung ở Cô Tô, ch.50–51)",
        "江南大酒店 = khách sạn Giang Nam (khách sạn năm sao duy nhất của Giang Đô, thuộc nhà họ Lý, nơi mở gia yến, ch.50–55)",
    ]),
    ("地下交易会 = chợ giao dịch ngầm", [
        "李家 = nhà họ Lý (một trong ba đại cổ tộc ở Giang Đô; võ đạo thua nhà họ Vương nhưng tài lực đứng đầu, ch.50–51)",
        "慕容家 = nhà họ Mộ Dung (gia tộc ở Cô Tô đứng sau ngân hàng Giang Nam, ch.50)",
    ]),
    ("百药谷 = Bách Dược Cốc", [
        "江都分行 = chi nhánh Giang Đô (chi nhánh ngân hàng Giang Nam tại Giang Đô, Lý Quảng Lăng làm giám đốc, ch.50–51)",
        "东区 = khu Đông (nơi Tôn Đào làm việc theo lời Lý Quảng Lăng ở ch.50)",
        "北区 = khu Bắc (ch.51 Tôn Đào tự giới thiệu ở chi nhánh khu Bắc — source hai chương nói khác nhau, dịch đúng từng chương, không tự \"sửa\")",
        "东城区 = Đông Thành khu (nơi Gia Cát Triết Nhã định xây tòa thành thương nghiệp, ch.52)",
    ]),
    ("开脉境 = Khai Mạch cảnh", [
        "九阴煞体 = Cửu Âm Sát Thể (thể chất đặc biệt của Vân Băng Uyển phát hiện ở ch.50; hấp dẫn Oán Long Khí nên khiến nó bạo động, sau khi âm dương giao hợp thì oán khí nhạt đi)",
        "阴阳交合 = âm dương giao hợp (cách source nói chuyện Diệp Sở và Vân Băng Uyển ở ch.50)",
        "龙族血脉 = huyết mạch Long Tộc (Vân Băng Uyển hình như mang huyết mạch liên quan Long tộc, ch.50)",
    ]),
    ("炼药师 = luyện dược sư", [
        "骨笛 = cây sáo xương (nhạc khí điều khiển cổ trùng của Lý Quảng Giang và Cát đại sư; ch.48 source còn gọi 白骨短笛 = \"cây sáo ngắn bằng xương trắng\". NHẤT QUÁN \"cây sáo xương\" — không viết \"sáo cốt\" hay \"cốt sáo\")",
        "白草丸 = Bạch Thảo Hoàn (cổ phương gia truyền của Cát đại sư, kéo dài mạng người sắp chết thêm nửa năm; source viết lẫn 白草丸 và 百草丸 trong cùng ch.47 → bản dịch NHẤT QUÁN \"Bạch Thảo Hoàn\")",
        "蛊师 = cổ sư (người dùng cổ; Diệp Sở biết lão già áo dài là cổ sư ở ch.49)",
        "窃听器 = thiết bị nghe lén (Lý Quảng Giang gắn hai cái trong phòng ngủ để nghe di ngôn của lão phu nhân, ch.47)",
        "祖传之物 = vật gia truyền (nhà họ Lý dùng cho chiếc nhẫn sắt — NHẤT QUÁN \"vật gia truyền\", không viết \"vật tổ truyền\", ch.47–48)",
        "铁戒指 = chiếc nhẫn sắt (vật gia truyền của nhà họ Lý, tưởng là tín vật định tình, chứa một bí mật lớn — thứ Thánh Giáo nhắm tới, ch.47)",
        "老夫人 = lão phu nhân (mẹ nhà họ Lý, bệnh thận; CHỈ viết \"lão phu nhân\", không viết \"tôi nhân\", ch.46–48)",
        "老妇人 = bà lão (source đổi cách gọi ngay trong cảnh ch.48–49 — dịch \"bà lão\", giữ khác với \"lão phu nhân\")",
        "老太太 = bà cụ (cách Diệp Sở nói về mẹ nhà họ Lý ở ch.47; bản dịch dùng \"bà cụ nhà họ Lý\")",
        "双簧 = kịch đôi (\"màn kịch đôi của hắn và Cát đại sư\", ch.48)",
    ]),
    ("总裁 = tổng giám đốc", [
        "行长 = giám đốc chi nhánh (李行长 → \"Giám đốc Lý\"; không viết \"hành trưởng\")",
        "董事长 = giám đốc (ch.50 source gọi Lý Quảng Lăng là 董事长 lẫn 行长 — bản dịch giữ \"giám đốc\" cho cả hai, không bày \"đổng sự trưởng\")",
        "李董 = Giám đốc Lý (Tôn Đào nói ở ch.50)",
        "李总 = Lý tổng (Tôn Đào nói ở ch.53)",
        "部门经理 = quản lý bộ phận (chức của Tôn Đào, ch.51)",
        "副局长 = phó cục trưởng (chồng Lý Quảng Hàn, ch.49)",
        "城卫军 = thành vệ quân (lực lượng bảo an thành phố; 统帅 → \"thống lĩnh\", chức của Chu Bẩm Thiên, ch.52)",
        "财务部长 = bộ trưởng tài chính (chức của Tôn Vĩ Minh, ch.52)",
        "副市长 = phó thị trưởng (chức của Thường Quang Viễn, ch.52)",
        "总经理 = tổng giám đốc (bà quản lý khách sạn Giang Nam tự giới thiệu là tổng giám đốc khách sạn, ch.53)",
        "至尊会员卡 = thẻ hội viên chí tôn (khách sạn Giang Nam tặng Diệp Sở, giảm một phần mười khi tiêu dùng, ch.54)",
        "飞天茅台 = Mao Đài Phi Thiên (hai chai ba mươi năm, khách sạn tặng thay mặt ông chủ nhà họ Lý, ch.53)",
        "罗曼尼康帝 = Romanée-Conti (hai chai rượu vang, ch.53)",
    ]),
    ("王少 = Vương thiếu", [
        "周禀天 = Chu Bẩm Thiên (thống lĩnh thành vệ quân Giang Đô, trung niên mất vợ, tính thẳng, cố ý thử Diệp Sở coi quẻ ở bàn rượu ch.52)",
        "孙伟明 = Tôn Vĩ Minh (bộ trưởng tài chính, ngồi bàn rượu ch.52)",
        "常光远 = Thường Quang Viễn (phó thị trưởng, hỏi Gia Cát Triết Nhã chuyện khu thương nghiệp Đông Thành, ch.52)",
    ]),
]

INSERT_BEFORE = [
    ("### Thánh Giáo (ch.31):", [
        "### Nhà họ Lý (ch.46–55):",
        "- 叶神医 → \"Diệp thần y\" (Lý Quảng Lăng và người nhà họ Lý gọi); 叶医生 → \"Bác sĩ Diệp\" (Lý Quảng Lăng gọi theo nghề y ở ch.46 — giữ \"bác sĩ\", không nâng thành \"thần y\"); 叶先生 → \"Diệp tiên sinh\" (nữ quản lý khách sạn, ch.54)",
        "- 云小姐 → \"cô Vân\" (nhà họ Lý gọi Vân Băng Uyển); 莹姐 → \"chị Oánh\" (Vân Băng Uyển gọi Trương Oánh); 大姐 → \"chị cả\" (Lý Quảng Lăng gọi Lý Quảng Hàn)",
        "- 小友 → \"tiểu hữu\" (lão phu nhân và Trương Oánh gọi Diệp Sở); 小兄弟 → \"tiểu huynh đệ\" (Lý Quảng Lăng, Chu Bẩm Thiên gọi); 孙小友 → \"Tôn tiểu hữu\" (người nhà họ Khương gọi Tôn Đào, ch.51)",
        "- Lý Quảng Giang gọi Cát đại sư là \"sư tôn\"; Cát đại sư tự xưng \"tôi\" khi ra vẻ cao nhân",
        "- Lý Quảng Hàn → Diệp Sở: \"cậu\" khinh miệt, \"thằng nhóc này\"; Diệp Sở → bà: \"cô\" / \"Lý tiểu thư\"; KHÔNG đổi vai giữa Lý Quảng Hàn (chị cả) và Lý Quảng Giang (em út)",
        "",
        "### Đại phòng nhà họ Khương (ch.50–55):",
        "- Khương Quân Hổ → Khương Hải Vân: \"Nhị thúc\"; → Hàn Mộng Quan: \"Nhị thẩm\"; → Khương Quân Dao: \"chị họ\"; → Diệp Sở: \"anh rể\"; tự xưng \"cháu\" (KHÔNG xưng \"con\" với chú thím)",
        "- Khương Hải Vận (đại cô) → Hàn Mộng Quan: \"em\"/\"Mộng Quan\", tự xưng \"chị cả\"; Trương Bích Nguyệt → bà: \"mẹ\", → Khương Quân Hổ: \"em họ\"; Khương Quân Hổ → Trương Bích Nguyệt: \"chị họ\", → bà: \"đại cô\"",
        "- Trần Mỹ Tĩnh/Khương Hải Vận/Khương Quân Hổ → Diệp Sở: \"thằng nhóc này\", \"tên đó\", \"đồ vô dụng\"; Hàn Mộng Quan bênh con rể bằng \"con rể tôi\"",
        "- Khương Phong Niên tự xưng \"tôi\", gọi Khương Hải Vân là \"Lão nhị\", Khương Hải Phong là \"Lão đại\"; cháu gái Khương Quân Dao xưng \"cháu\" với ông",
        "- Khương Quân Dao → Hàn Mộng Quan: \"mẹ\"; → Khương Hải Vân: \"bố\"; Trần Mỹ Tĩnh → Tôn Đào: \"cậu Tiểu Tôn\", \"anh Tôn\"",
        "",
    ]),
]

REPLACE = [
    ("劳改犯 = phạm nhân cải tạo (KHÔNG viết \"phạm nhân cải tạo lao động\")",
     "劳改犯 = tù cải tạo (bản dịch ch.50–53 đã chốt \"tù cải tạo\" — KHÔNG viết \"phạm nhân cải tạo\", không viết \"nhân viên lao cải\")"),
]

TAIL_ITEMS = [
    "",
    "12. BA người nhà họ Khương chỉ lệch nhau một chữ, phải tra source từng câu: 姜海云 = Khương Hải Vân (bố vợ Diệp Sở, nhị phòng, NAM), 姜海风 = Khương Hải Phong (anh cả, đại phòng), 姜海韵 = Khương Hải Vận (chị cả, đại cô, NỮ). Riêng ch.54 có tới 9 lượt lời của Khương Hải Vận dễ bị ghi nhầm thành \"Khương Hải Vân\". Ngoài ra 姜君虎 = Khương Quân Hổ (cháu trai đại phòng) KHÁC 姜君兰 = Khương Quân Lan (cháu gái đại phòng).",
    "13. Ba chị em nhà họ Lý: 李广陵 = Lý Quảng Lăng (gia chủ), 李广寒 = Lý Quảng Hàn (chị cả), 李广江 = Lý Quảng Giang (em út phản diện). Nhà họ Lý này KHÔNG liên quan tới 李正元 (Lý Chính Nguyên), 李正熊 (Lý Chính Hùng), 李静萱 (Lý Tĩnh Huyên), 李木端 (Lý Mộc Đoan).",
    "14. \"Giám đốc Lý\" trong ch.46–55 luôn chỉ Lý Quảng Lăng (source dùng 李董/李行长/董事长 lẫn lộn). Nhưng ở ch.7, \"Giám đốc Lý\" từng là chi nhánh Bạch Lang An Bảo, còn ch.11–12 \"Lý quản lý\" là Lý Mộc Đoan — phải dựa vào chương để phân biệt.",
    "15. Cách gọi đã chốt ở ch.46–55, KHÔNG viết lại: \"cây sáo xương\" (骨笛), \"Bạch Thảo Hoàn\" (白草丸/百草丸), \"Cát đại sư\" (葛大师), \"lão phu nhân\" (老夫人), \"bà lão\" (老妇人), \"vật gia truyền\" (祖传之物), \"gia yến\" (家宴), \"tù cải tạo\" (劳改犯), \"cô Vân\" cho 云姑娘 kể cả trong tiêu đề chương 49.",
]

CONTEXT = [
    "",
    "### Đã xảy ra — chương 46–55:",
    "- Ch.46: Vân Băng Uyển đưa Diệp Sở đến biệt thự nhà họ Lý khám cho mẹ Trương Oánh (lão phu nhân, đã đổi thận mấy năm trước). Diệp Sở bắt mạch xong kết luận thận bà không bị bài thải mà trúng cổ độc, nghi liên quan Thánh Giáo. Lý Quảng Hàn (chị cả) và Lý Quảng Giang (em út) xông vào mắng y là đồ lừa đảo rồi gọi \"Cát đại sư\" — lão già áo dài đứng cạnh Lý Quảng Giang — ra tay. Vân Băng Uyển bênh Diệp Sở, cả ba bị đuổi về; Lý Quảng Hàn nặng lời chê Trương Oánh kết bạn với \"góa phụ sát chồng\".",
    "- Ch.47: Cát đại sư tuyên bố thận lão phu nhân đã suy kiệt, chỉ kéo dài được nửa năm bằng Bạch Thảo Hoàn, từ chối nhận trả giá. Diệp Sở để ý lão già vỗ vai mình rồi để lại một luồng ấn ký nên nửa đêm lẻn vào biệt thự, dùng tinh thần lực phát hiện hai thiết bị nghe lén, nghe được lão phu nhân trao chiếc nhẫn sắt (vật gia truyền chứa bí mật lớn, dặn tuyệt đối không cho người thứ hai biết) cho Lý Quảng Lăng. Một bóng đen phá cửa cướp nhẫn rồi nhảy cửa sổ chạy; Cát đại sư đuổi theo.",
    "- Ch.48: Lý Quảng Giang và Cát đại sư là thầy trò, diễn kịch đôi: y hạ cổ trùng lên mẹ, gắn máy nghe lén ép bà khai vật gia truyền; vì bà vẫn chọn Lý Quảng Lăng nên y lật bài, dùng cây sáo xương điều khiển cổ trùng làm Lý Quảng Hàn và Lý Quảng Lăng đau lăn lộn, đòi gia chủ vị trí cùng toàn bộ cổ phần. Diệp Sở xuất hiện, một cái tát giết chết cổ trùng, phế tứ chi Lý Quảng Giang, cho bà lão và Lý Quảng Lăng mỗi người một viên Giải Độc Đan, rồi ném cho Lý Quảng Hàn một viên.",
    "- Ch.49: Lý Quảng Hàn không cảm ơn mà bắt Diệp Sở phải bồi thường rồi chờ cảnh sát (chồng bà là phó cục trưởng), lão phu nhân quát lớn bà mới lui; bà lão hành lễ tạ ơn, hứa ngày khác tự bày tiệc. Diệp Sở lần theo ấn ký tới công viên hẻo lánh, thấy Cát đại sư đang giao chiến với bóng đen — hóa ra là Vân Băng Uyển (Khai Mạch cảnh bốn năm trọng). Lão già dùng bột phấn kích dục, nàng trúng nên thua; Diệp Sở ra một đòn đánh trọng thương, lão tự bóp nát cây sáo xương để cổ trùng của mình ăn tim mà chết, trối lại \"Thánh Giáo sẽ báo thù cho tôi\". Diệp Sở thiêu xác, phát hiện nàng là Cửu Âm Sát Thể lại dường như mang huyết mạch Long Tộc; Oán Long Khí bạo động nên hắn bế nàng vào khách sạn gần đó — \"Cô Vân, đắc tội rồi\".",
    "- Ch.50: Đêm đó hai người thật sự xảy ra chuyện. Sáng ra Vân Băng Uyển lạnh lùng dọa giết nếu tiết lộ, vì Diệp Sở đã cướp lần đầu của nàng (tin đồn nàng là góa phụ là không đúng); Oán Long Khí của y từ đó không còn bạo động như trước. Hàn Mộng Quan gọi y về dự gia yến ở khách sạn Giang Nam vì hôm sau Khương Quân Long nhậm chức tổng giám đốc. Ở đại sảnh, Khương Quân Hổ (cháu đại phòng) cố ý giữ Diệp Sở lại để y mất mặt rồi dẫn đại cô Khương Hải Vận, con gái bà là Trương Bích Nguyệt và bạn trai Tôn Đào đi trước. Tôn Đào được chính Lý Quảng Lăng — giám đốc chi nhánh Giang Đô, gia chủ nhà họ Lý — nhớ mặt, nên cả nhà tưởng y quen nhân vật lớn.",
    "- Ch.51: Trong gia yến, Khương Phong Niên công khai bảo nhị phòng \"bảo Quân Dao ly hôn\" vì Diệp Sở là tù cải tạo, rồi tuyên bố hai chuyện: Khương Quân Long nhận chức tổng giám đốc toàn quyền lo hợp tác với nhà họ Hoàng Phủ, và ra mắt bạn trai của Trương Bích Nguyệt. Trần Mỹ Tĩnh, Khương Hải Vận, Khương Quân Hổ thay nhau chế nhạo nhị phòng. Cùng lúc Lý Quảng Lăng bắt gặp Diệp Sở ở đại sảnh, kéo y vào một phòng bao để giới thiệu nhân mạch.",
    "- Ch.52: Bàn rượu có Chu Bẩm Thiên (thống lĩnh thành vệ quân), Tôn Vĩ Minh (bộ trưởng tài chính), Thường Quang Viễn (phó thị trưởng) và Gia Cát Triết Nhã — nàng tổ chức tiệc, định xây khu thương nghiệp ở Đông Thành. Cả bàn khinh Diệp Sở \"ba năm trước mới học y\"; Chu Bẩm Thiên cố ý thử coi quẻ, Diệp Sở đoán đúng ông trung niên tang thê nhưng nói \"gần đây sẽ gặp nhân duyên tiếp theo\" nên bị cho là nói bừa. Gia Cát Triết Nhã đã điều tra: ba năm trước Diệp Sở chỉ là con riêng nhà họ Diệp, chẳng biết y thuật, đoán học nghề trong tù — nàng chỉ nghĩ tới hai chữ \"thiên tài\".",
    "- Ch.53: Nhị phòng tiếp tục bị công kích; Khương Quân Dao lần đầu lên tiếng bênh Diệp Sở (\"Diệp Sở là đàn ông của tôi\"), đồng thời vạch Khương Quân Long \"lục thân bất nhận\" khiến y hoảng. Ông cụ ra lệnh con rể nhà họ Khương \"phải ưu tú như cậu Tiểu Tôn\". Khách sạn Giang Nam cử tổng giám đốc mang tới hai chai Mao Đài Phi Thiên ba mươi năm và hai chai Romanée-Conti kèm lời \"ông chủ gửi\" — cả nhà tưởng tặng Tôn Đào, chỉ Diệp Sở hiểu là tặng mình.",
    "- Ch.54: Trần Mỹ Tĩnh và Khương Hải Vận còn miệt thị nhị phòng, dọa xin cho Diệp Sở vào ngân hàng \"làm bảo vệ\". Nữ quản lý khách sạn mang thẻ hội viên chí tôn tận tay Diệp Sở, xác nhận rượu và thẻ đều do ông chủ nể mặt \"Diệp tiên sinh\"; cả nhà sững sờ, Tôn Đào không biết chui vào đâu, Khương Hải Vận suýt ngã và tức đến nghẹn. Diệp Sở tặng thẻ cho Hàn Mộng Quan; trên xe bà hỏi ra mới biết y đã cứu Lý Quảng Lăng một mạng. Khương Quân Dao nhận điện thoại rồi bỏ đi một mình.",
    "- Ch.55: Hóa ra Khương Quân Dao đã phát hiện người của Khương Quân Long theo dõi, chủ động tách khỏi cả nhà để tự xử: nàng đánh gãy tay tên võ giả Đoán Thể sáu đoạn, ép hắn gọi điện báo \"bắt cóc thành công\". Đêm đó Hoàng Phủ Thi Nguyệt cam đoan Khương Quân Long không thể nhậm chức tổng giám đốc trừ khi nhà họ Hoàng Phủ không muốn hợp tác nữa. Sáng hôm sau, họp nội bộ ở trụ sở Tập đoàn Khương Thị (ngành địa ốc, tháp trăm mét): Khương Phong Niên nhắc quy định \"ai đạt được hợp tác với nhà họ Hoàng Phủ thì làm tổng giám đốc\", rồi tuyên bố Khương Quân Long đã làm được — Khương Hải Phong, Khương Hải Vận và đám giám đốc đều \"không có ý kiến\". Hàn Mộng Quan phản đối vì hợp tác rõ ràng do Khương Quân Dao đàm phán, và đúng lúc đó có tiếng từ ngoài cửa: \"Tôi cũng có ý kiến.\"",
]

REBIND = [
    "### Ràng buộc cho các chương sau:",
    "- Diệp Sở và Vân Băng Uyển đã thật sự qua đêm với nhau (ch.50): nàng mang Cửu Âm Sát Thể và dường như có huyết mạch Long Tộc, Oán Long Khí của y đã bớt bạo động sau lần giao hợp. Nàng dọa giết nếu y nói ra, còn y thì tuyên bố \"sẽ chịu trách nhiệm\" và muốn ở bên nàng. Gia Cát Triết Nhã (Quang Minh Thể) vẫn là mục tiêu kế tiếp; nhà họ Vân có động cơ riêng với chiếc nhẫn sắt.",
    "- Chiếc nhẫn sắt (vật gia truyền nhà họ Lý, chứa bí mật lớn) là thứ Thánh Giáo nhắm tới. Lý Quảng Giang bị phế tứ chi, Cát đại sư tự tử; Lý Quảng Hàn không cảm ơn mà tố Diệp Sở \"diễn kịch đôi\" với Cát đại sư và sẽ gọi chồng là phó cục trưởng tới. Lão phu nhân đã hành lễ tạ ơn và hứa bày tiệc; Lý Quảng Lăng một lòng kết thân, đã giới thiệu y vào bàn rượu nhân mạch và tặng thẻ hội viên chí tôn qua khách sạn Giang Nam.",
    "- Nhân mạch mới của Diệp Sở: Long Cửu gia (gọi \"Diệp đại sư\"), Lý Quảng Lăng (gia chủ nhà họ Lý + giám đốc chi nhánh Giang Đô), Chu Bẩm Thiên/Tôn Vĩ Minh/Thường Quang Viễn (chưa phục, coi y là kẻ thổi phồng — sẽ \"bốp bốp vả mặt\" về sau), Gia Cát Triết Nhã (đã điều tra thân thế y: từng là con riêng nhà họ Diệp, học nghề trong tù).",
    "- Nhà họ Khương: Khương Phong Niên ép nhị phòng cho Diệp Sở ly hôn và đẩy Khương Quân Long lên tổng giám đốc ngay hôm sau; Trần Mỹ Tĩnh, Khương Hải Vận, Khương Quân Hổ công khai thù nhị phòng; Khương Quân Dao bắt đầu bênh Diệp Sở và nắm thóp Khương Quân Long (ch.53). Hợp tác với nhà họ Hoàng Phủ chưa chốt; cuối ch.55 có người bước vào phòng họp nói \"Tôi cũng có ý kiến\" (cliffhanger).",
    "- Xung đột còn treo: Thánh Giáo (đà chủ Kim Lăng vẫn điều tra cái chết Cửu trưởng lão, nay thêm vụ Cát đại sư chết); nhà họ Vương (Vương Tử Đằng sắp về); Bạch Lang Hội (Đao Sẹo Trần); Tiền Hâm; Hắc Hổ Hội; nhà họ Diệp đã mượn Phùng Hán Tam trị Diệp Sở; Khương Quân Long cho người bắt cóc hụt Khương Quân Dao và tên võ giả kia đang bị nàng sai làm việc.",
    "- Treo: chữ cổ trong Long Hồn Hư Không Đỉnh chưa dịch được; bí mật của chiếc nhẫn sắt nhà họ Lý chưa sáng tỏ; Vân Băng Uyển xử lý thế nào với đêm đã qua; nhân vật nói \"Tôi cũng có ý kiến\" ở cuối ch.55 là ai.",
    "- Không đổi cách gọi đã chốt ở mục \"LƯU Ý ĐẶC BIỆT\" (Hàn Mộng Quan, Tạ Vũ Sâm, Lâm Huyển Huyển, Hoàng Phủ, Lý Đầu Trọc, Thệ Tâm Cổ, Bạch Lang Hội, Đao Sẹo Trần, \"Hoàng phu nhân\", \"Tam gia\", \"em trai\", \"Diệp đại sư\", \"Long Cửu gia\"/\"Cửu gia\", \"cô Vân\", \"chị Oánh\", \"Nhị thúc\"/\"Nhị thẩm\", \"cây sáo xương\", \"Bạch Thảo Hoàn\", \"Cát đại sư\", \"lão phu nhân\", \"tù cải tạo\", \"giám đốc chi nhánh\").",
]

changed = 0

def has(prefix):
    return any(ln.startswith(prefix) for ln in lines)

for anchor, block in INSERTS:
    key = next((ln.split(" =")[0] for ln in block if ln.strip() and "=" in ln), "")
    assert key, f"block khong co dong moi: {anchor}"
    if has(key):
        print(f"skip (da co) sau {anchor[:18]}")
        continue
    idx = next((i for i, ln in enumerate(lines) if ln.startswith(anchor)), None)
    assert idx is not None, f"ANCHOR MISS: {anchor}"
    lines[idx + 1:idx + 1] = block
    changed += len(block)
    print(f"chen {len(block)} dong sau {anchor[:18]}")

for anchor, block in INSERT_BEFORE:
    if has(block[0]):
        print(f"skip (da co) truoc {anchor[:18]}")
        continue
    idx = next((i for i, ln in enumerate(lines) if ln.startswith(anchor)), None)
    assert idx is not None, f"ANCHOR MISS: {anchor}"
    lines[idx:idx] = block
    changed += len(block)
    print(f"chen {len(block)} dong truoc {anchor[:18]}")

for old, new in REPLACE:
    idx = next((i for i, ln in enumerate(lines) if ln == old), None)
    if idx is None:
        print(f"KHONG TIM THAY: {old[:40]}")
    else:
        lines[idx] = new
        changed += 1
        print(f"thay the: {old[:32]}")

a11 = next((i for i, ln in enumerate(lines) if ln.startswith("11. Đan dược luôn VIẾT HOA")), None)
assert a11 is not None, "anchor 11 miss"
if not any(ln.startswith("12. BA người nhà họ Khương") for ln in lines):
    lines[a11 + 1:a11 + 1] = TAIL_ITEMS
    changed += len(TAIL_ITEMS)
    print(f"chen {len(TAIL_ITEMS)} dong LƯU Ý ĐẶC BIỆT")
else:
    print("skip (da co) LƯU Ý ĐẶC BIỆT 12-15")

idx_rb = next((i for i, ln in enumerate(lines) if ln.startswith("### Ràng buộc cho các chương sau:")), None)
assert idx_rb is not None, "anchor ràng buộc miss"
if not any(ln.startswith("- Ch.50: Đêm đó hai người") for ln in lines):
    lines[idx_rb:idx_rb] = CONTEXT
    changed += len(CONTEXT)
    print(f"chen {len(CONTEXT)} dong NGỮ CẢNH 46-55")
    idx_rb = next((i for i, ln in enumerate(lines) if ln.startswith("### Ràng buộc cho các chương sau:")), None)
else:
    print("skip (da co) NGỮ CẢNH 46-55")

end = len(lines)
while end - 1 > idx_rb and not lines[end - 1].strip():
    end -= 1
old_block = lines[idx_rb:end]
if old_block != REBIND:
    lines[idx_rb:end] = REBIND
    changed += 1
    print(f"viet lại Ràng buộc: {len(old_block)} dong -> {len(REBIND)} dong")

P.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
print("== so thay doi:", changed, "| tong dong:", len(lines))
