import io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GP = r"F:/taitruyen/translate/glossary_can_bao_chan_long.txt"
lines = io.open(GP, encoding="utf-8").read().split("\n")
text_all = "\n".join(lines)


def has(prefix):
    return any(l.startswith(prefix) for l in lines)


def insert_after(prefix, block, marker):
    """chen block sau dong bat dau bang prefix (idempotent qua marker)"""
    if has(marker):
        print("skip (co roi):", marker[:28])
        return
    idx = next((i for i, l in enumerate(lines) if l.startswith(prefix)), None)
    assert idx is not None, "khong thay anchor: " + prefix
    block = block.split("\n")
    lines[idx + 1 : idx + 1] = block
    print("chen sau", prefix[:20], "+", len(block), "dong")


def insert_before(prefix, block, marker):
    """chen block truoc dong bat dau bang prefix (idempotent qua marker)"""
    if has(marker):
        print("skip (co roi):", marker[:28])
        return
    idx = next((i for i, l in enumerate(lines) if l.startswith(prefix)), None)
    assert idx is not None, "khong thay anchor: " + prefix
    blk = block.split("\n")
    lines[idx:idx] = blk
    print("chen truoc", prefix[:20], "+", len(blk), "dong")


# ─────────── 1. NHAN VAT PHU ───────────
insert_after(
    "孙秀英 =",
    """萧媚 = Tiêu Mị (cửa hàng trưởng hiệu kim hoàn Giang Nam, sinh viên đại học Giang Đô khóa trên Tôn Ngữ Nhu, ghen vì bị cướp danh hoa khôi, ch.58–65)
罗三胖 = La Tam Béo (chủ cửa hàng ở phố kim hoàn, anh rể Úy Trì Hùng đường chủ Hắc Hổ Hội, ép Tôn Ngữ Nhu bồi một triệu cho chiếc vòng ngọc giá một vạn, ch.58–62)
文萧山 = Văn Tiêu Sơn (đối tượng xem mắt của Tôn Ngữ Nhu do họ hàng giới thiệu, đổ hết lỗi cho cô, bị Diệp Sở bắn ngân châm liệt chân trái, ch.58–60)
钱豪森 = Tiền Hào Sâm (tổng giám đốc hiệu kim hoàn Giang Nam, ủy viên Thương hội Giang Nam, BỐ của Tiền Hâm; source viết lẫn 钱森豪 ở ch.61–62 — bản dịch nhất quán "Tiền Hào Sâm", ch.61–64)
尉迟雄 = Úy Trì Hùng (đường chủ Hắc Hổ Hội, võ giả Đoán Thể tám đoạn, anh rể La Tam Béo, bị Diệp Sở một quyền đánh bay rồi tức giận công tâm thổ huyết, ch.61–62)
岳珊 = Nhạc San (thư ký riêng của Hoàng Phủ tiểu thư, thay lời tiểu thư tới cuộc họp ở Tập đoàn Khương Thị, ép Khương Phong Niên giao quyền hợp tác cho Khương Quân Dao, ch.56–57)""",
    "萧媚 =",
)

# ─────────── 2. THE LUC ───────────
insert_after(
    "江南商会 =",
    """江南珠宝行 = hiệu kim hoàn Giang Nam (hiệu kim hoàn lớn nhất Giang Đô, nằm giữa phố kim hoàn, sau lưng là Thương hội Giang Nam; NHẤT QUÁN "hiệu kim hoàn Giang Nam", KHÔNG viết "trung tâm trang sức Giang Nam", "tiệm trang sức Giang Nam", "hàng trang sức Giang Nam" hay "tiệm châu báu Giang Nam", ch.58–65)""",
    "江南珠宝行 =",
)

# ─────────── 3. DIA DANH ───────────
insert_after(
    "东城区 =",
    """珠宝街 = phố kim hoàn (phố tập trung hiệu kim hoàn ở trung tâm Giang Đô, một góc bị La Tam Béo cai trị, ch.58–59)""",
    "珠宝街 =",
)

# ─────────── 4. VU DAO - THE CHAT ───────────
insert_after(
    "龙族血脉 =",
    """真武灵体 = Chân Vũ Linh Thể (thể chất hiếm thấy của Tôn Ngữ Nhu, Diệp Sở phát hiện ở ch.65 nhờ thấy Trái Tim Rừng Xanh mờ đi; mạnh không kém Thật Hoàng Thể, trời sinh thích hợp luyện võ, cơ thể tự hấp thu linh khí trời đất)
武道宗师 = võ đạo tông sư (tông sư võ đạo; đại phòng tính chuyện liên hôn vì nhà họ Vương sắp có thêm một vị nữa, ch.57–58)""",
    "真武灵体 =",
)

# ─────────── 5. Y HOC - DAN DƯỢC ───────────
insert_after(
    "双簧 =",
    """百药酒 = Bách Dược Tửu (rượu thuốc Diệp Sở viết công thức tại chỗ cho Gia Cát Triết Nhã ở ch.64–65: trăm vị dược liệu ngâm theo tỷ lệ đặc biệt, rượu dưỡng sinh trị phong thấp, viêm khớp, đau lưng; đổi lấy Tử Vi Tinh và phần hợp tác)
祛煞丹 = Khu Sát Đan (đan dược sư phụ của Khương Quân Dao ban, Khương Quân Dao hứa sẽ xin thêm mấy viên cho sư tỷ, ch.58)""",
    "百药酒 =",
)

# ─────────── 6. THUAT NGU CHUNG ───────────
insert_after(
    "验资 =",
    """森林之心 = Trái Tim Rừng Xanh (bảo vật trấn tiệm của hiệu kim hoàn Giang Nam, khắc từ phần tinh túy nhất của một khối đế vương lục, giá 220 triệu; NHẤT QUÁN "Trái Tim Rừng Xanh", KHÔNG dịch thành "Sâm Lâm Chi Tâm", ch.60–65)
紫薇星 = Tử Vi Tinh (mặt dây chuyền phỉ thúy Tử La Lan cực phẩm khắc hình rồng tím, dây xích vàng nhạt, giá trên trời từng đấu giá một tỷ ở Kim Lăng; nhà họ Gia Cát đưa tới để làm quà nên không bán, Diệp Sở đổi bằng công thức Bách Dược Tửu, ch.64–65)
紫罗兰 = Tử La Lan (hàng phỉ thúy tím cực phẩm; VIẾT HOA "Tử La Lan", ch.58–64)
镇店之宝 = bảo vật trấn tiệm (món đắt nhất cửa hàng; KHÔNG viết "trấn điếm")
导购 = nữ nhân viên bán hàng (KHÔNG dịch thành "hướng dẫn viên")
店长 = cửa hàng trưởng (chức của Tiêu Mị, ch.60)
江南大曲 = Giang Nam Đại Khúc (rượu nổi tiếng khắp Đại Hạ do nhà họ Gia Cát nấu, ch.64)""",
    "森林之心 =",
)

# ─────────── 7. DIA VI - CHUC VU ───────────
insert_after(
    "贤侄 =",
    """堂主 = đường chủ (Hắc Hổ Hội chia đường; Úy Trì Hùng là đường chủ, gọi "Úy Trì đường chủ")
理事 = ủy viên (ủy viên Thương hội Giang Nam — Tiền Hào Sâm; KHÔNG viết "lý sự")
白狼王 = Bạch Lang Vương (biệt hiệu hội chủ trẻ tuổi của Bạch Lang Hội, hùng tâm bừng bừng muốn tiến quân vào Kim Lăng, ch.61)
叶大哥 = anh Diệp (cách Tôn Ngữ Nhu và Chu Tiểu Vân gọi Diệp Sở; KHÔNG viết "Diệp đại ca")
钱总 = Tiền tổng (cách Tiêu Mị và Úy Trì Hùng gọi Tiền Hào Sâm)""",
    "堂主 =",
)

# ─────────── 8. QUY TAC XUONG HO (block moi) ───────────
insert_before(
    "### Thánh Giáo (ch.31):",
    """### Hiệu kim hoàn Giang Nam / phố kim hoàn (ch.58–65):
- 叶大哥 → "anh Diệp" / "Anh Diệp" (Tôn Ngữ Nhu gọi Diệp Sở — KHÔNG viết "Diệp đại ca"; ch.23, 32, 62 đã chốt)
- 钱总 → "Tiền tổng"; 尉迟堂主 → "Úy Trì đường chủ"; La Tam Béo tự xưng "ông đây", gọi người khác là "tiểu tử", "thằng nhóc"
- Diệp Sở ↔ La Tam Béo / Văn Tiêu Sơn: hai bên xưng "tao – mày" khi đánh nhau; Văn Tiêu Sơn → La Tam Béo: "ông chủ"; Tôn Ngữ Nhu → Văn Tiêu Sơn: "anh"
- Tiền Hào Sâm → Diệp Sở: "tiểu hữu", "thằng nhóc" trước khi biết thẻ rồng Giang Nam; sau đó "đại nhân", tự xưng "tiểu nhân"
- Gia Cát Triết Nhã → Diệp Sở: "Diệp đại sư", trong bụng gọi "tên nhóc này", "thằng nhóc thối này"; tự xưng "tôi"
- Tôn Ngữ Nhu → Diệp Sở: "anh Diệp"; tự xưng "em"; Gia Cát Triết Nhã gọi nàng là "cô bạn gái nhỏ" theo hiểu lầm
""",
    "### Hiệu kim hoàn Giang Nam / phố kim hoàn (ch.58–65):",
)

# ─────────── 9. SUA dong 周小云 (叶大哥) ───────────
OLD_ZHOU = '- 周姐 → "Chu tỷ" (Trương Diệu Xuân gọi cô y tá Chu Tiểu Vân); 周小云 gọi Diệp Sở là "Diệp đại ca" (叶大哥)'
NEW_ZHOU = '- 周姐 → "Chu tỷ" (Trương Diệu Xuân gọi cô y tá Chu Tiểu Vân); 周小云 gọi Diệp Sở là "anh Diệp" (叶大哥, ch.32 đã chốt — không viết "Diệp đại ca")'
for i, l in enumerate(lines):
    if l.startswith(OLD_ZHOU):
        lines[i] = NEW_ZHOU
        print("da thay dong 周小云")
        break
else:
    print("KO thay dong 周小云 de sua")

# ─────────── 10. LUU Y DAC BIET (append) ───────────
TAIL_ITEMS = """
16. Tiền Hào Sâm (钱豪森 — bố, tổng giám đốc hiệu kim hoàn Giang Nam) và Tiền Hâm (钱鑫 — con, phú nhị đại từng bùng tiền room Vương Hầu ch.29–30) là HAI người khác nhau, tên chỉ lệch thứ tự chữ. Source còn viết nhầm 钱森豪 ở ch.61–62 — bản dịch nhất quán "Tiền Hào Sâm", KHÔNG bày ra "Tiền Sâm Hào".
17. Nhà họ Vương: Vương Tử Hào (bạn trai Khương Quân Lan, "anh Tử Hào") KHÁC Vương Tử Đằng (võ giả Đoán Thể đỉnh phong, còn thích Khương Quân Dao, sắp về và nhiều khả năng được viên Tiểu Chân Nguyên Đan → thành tông sư). Đại phòng định mượn Vương Tử Đằng ép Khương Quân Dao liên hôn, ch.57–58.
18. Cách gọi đã chốt ở ch.56–65, KHÔNG viết lại: "hiệu kim hoàn Giang Nam", "phố kim hoàn", "Trái Tim Rừng Xanh", "Tử Vi Tinh", "Tử La Lan", "bảo vật trấn tiệm", "nữ nhân viên bán hàng", "cửa hàng trưởng", "ủy viên Thương hội Giang Nam", "anh Diệp", "Tiền tổng", "Bách Dược Tửu", "Khu Sát Đan", "Chân Vũ Linh Thể", "Úy Trì Hùng", "La Tam Béo", "Văn Tiêu Sơn", "Tiêu Mị", "Nhạc San", "Giang Nam Đại Khúc".
19. Source đổi 龙国 / 大夏 lộn xộn ngay trong cùng chương (ch.64 nói "đệ nhất Long Quốc" rồi "đệ nhất Đại Hạ") — dịch đúng từng chỗ theo source, không tự gộp thành một tên.
""".strip("\n")

if "16. Tiền Hào Sâm" in text_all:
    print("skip TAIL (co roi)")
else:
    i = next(k for k, l in enumerate(lines) if l.startswith("## ══════ VĂN PHONG"))
    ins = TAIL_ITEMS.split("\n")
    j = i
    while not lines[j - 1].strip():
        j -= 1
    lines[j:j] = [""] + ins
    print("them 4 muc LƯU Ý, +", len(ins))

# ─────────── 11. NGU CANH 56-65 ───────────
CONTEXT = """### Đã xảy ra — chương 56–65:
- Ch.56: Khương Quân Dao tới cuộc họp cùng Nhạc San — thư ký riêng của Hoàng Phủ tiểu thư. Nàng công khai chê Khương Quân Long không xứng kế nghiệp, kéo được mấy vị nguyên lão (lão Vương dẫn đầu) ủng hộ mình; Khương Hải Phong và Khương Hải Vận phụ họa. Bí mật: mấy hôm nay nàng không lo hợp tác Hoàng Phủ (sư tỷ đã lo giùm) mà lo lôi kéo nguyên lão.
- Ch.57: Bị Nhạc San chuyển yêu cầu của tiểu thư nhà họ Hoàng Phủ ("hợp tác sau này vẫn do Khương tiểu thư chủ trì"), Khương Phong Niên buộc phải nhượng, tuyên bố Quân Dao tạm giữ chức tổng giám đốc, toàn quyền phụ trách hợp tác nhà họ Hoàng Phủ. Ông định dẫn Nhạc San đi tham quan để làm quen thì nàng từ chối. Đại phòng mưu tính tiếp: Khương Quân Long nghi vụ bắt cóc thất bại (tâm phúc mất liên lạc), đề xuất thuê người giết Quân Dao; Khương Hải Phong sợ ông cụ phát hiện; Khương Quân Lan đưa kế liên hôn nhà họ Vương, "chỉ cần giết chết tên vô dụng kia". Cliffhanger: nhà họ Vương sắp có thêm một vị võ đạo tông sư.
- Ch.58: Khương Quân Lan kể lại buổi đấu giá (giấu chuyện gặp Diệp Sở); cả nhà kinh thán vì viên đan có thể khiến người đột phá tông sư — Vương Tử Đằng nhiều khả năng được hưởng. Khương Quân Hổ nhận việc xử Diệp Sở qua Hắc Hổ Hội, Khương Quân Lan khuyên thăm dò phản ứng của nhà họ Lý (thực chất nàng sợ Long Cửu gia và người phụ nữ thần bí). Khương Quân Dao gọi điện cảm ơn sư tỷ, hứa xin sư phụ thêm Khu Sát Đan; sư tỷ nhắc nàng mau tìm "chỗ đó" và cảnh giác đại tiểu thư nhà họ Hoàng Phủ. Hàn Mộng Quan muốn xếp việc cho Diệp Sở nhưng bị Khương Hải Vân phá; Diệp Sở đi mua quà hòa giải với Vân Băng Uyển thì gặp Tôn Ngữ Nhu bị La Tam Béo ép bồi một triệu cho chiếc vòng ngọc một vạn — kẻ gây họa là Văn Tiêu Sơn, đối tượng xem mắt mà Tôn Tú Anh ép con gái đi gặp.
- Ch.59: La Tam Béo đòi Tôn Ngữ Nhu "bầu bạn một tháng" để miễn bồi thường; Văn Tiêu Sơn đẩy hết lỗi cho cô rồi xin đền mười vạn rồi chạy. Diệp Sở can thiệp, bắn ngân châm liệt chân trái Văn Tiêu Sơn, đánh ngã đám lực lưỡng. La Tam Béo khoe anh rể là đường chủ Hắc Hổ Hội, đòi Diệp Sở quỳ xin lỗi, để người phụ nữ của hắn ta bầu bạn mấy tháng, và về "làm chó" cho hắn.
- Ch.60: Diệp Sở một cước đá bay La Tam Béo, đập nát cửa kính; hắn gọi điện cầu cứu anh rể. Hai người vào hiệu kim hoàn Giang Nam; nữ nhân viên bán hàng trẻ tiếp đón và giới thiệu bảo vật trấn tiệm Trái Tim Rừng Xanh (khắc từ phần tinh túy nhất của đế vương lục, 220 triệu). Tiêu Mị — cửa hàng trưởng, cũng là sinh viên Giang Đô khóa trên, ghét Tôn Ngữ Nhu vì bị cướp danh hoa khôi — quát nhân viên, mỉa mai rồi đòi Diệp Sở phải xác nhận tài sản.
- Ch.61: Tiền Hào Sâm (tổng giám đốc hiệu kim hoàn, ủy viên Thương hội Giang Nam) định gán tội Diệp Sở để lấy lòng Hắc Hổ Hội; Úy Trì Hùng dẫn người xông vào, được Tiền Hào Sâm nhường "xử việc riêng". Úy Trì Hùng — võ giả Đoán Thể tám đoạn — bị Diệp Sở một quyền đánh bay, thổ huyết ngất. Tiền Hào Sâm khen "tiểu hữu" rồi cảnh báo Hắc Hổ Hội sẽ không cho đất diễn, đồng thời kể gốc gác: Hắc Hổ Hội do một thế lực lớn ở Kim Lăng nâng đỡ để kiềm chế Bạch Lang Hội (Bạch Lang Vương), hiện chỉ nhà họ Long mới đè nổi. Diệp Sở: "Chỉ là Hắc Hổ Hội, tôi lật tay là diệt được."
- Ch.62: Diệp Sở ép La Tam Béo bồi năm triệu "tổn thất tinh thần" chuyển cho Tôn Ngữ Nhu. Tiền Hào Sâm quay ra đổ cho Diệp Sở làm hỏng đồ và đòi thêm năm triệu; hắn chỉ cúi gằm khi Tiêu Mị nhận ra thẻ rồng Giang Nam, rồi gọi Diệp Sở là "đại nhân", tự xưng "tiểu nhân". Hắn tra ra thẻ đứng tên Lý Tĩnh Huyên (phu nhân thị trưởng, đại tiểu thư nhà họ Lý ở Kim Lăng) nên càng không dám lên tiếng. Diệp Sở lấy Trái Tim Rừng Xanh ra xem, thấy không hợp với khí chất Vân Băng Uyển (nàng tóc tím, hợp phỉ thúy tím hơn) nên đeo thử cho Tôn Ngữ Nhu.
- Ch.63: Tiền Hào Sâm đang định gọi người xử Diệp Sở thì Gia Cát Triết Nhã cùng thư ký xuất hiện. Tiền Hào Sâm tố Diệp Sở "gây sự trong tiệm, lại mạo dụng thẻ rồng Giang Nam của người khác" — chính con trai hắn là Tiền Hâm trước đó đã thề thốt Diệp Sở chỉ là tên ở rể phế vật, khiến hắn giờ muốn bóp chết "đồ con hại cha". Gia Cát Triết Nhã không để ý, đi thẳng tới trêu Diệp Sở, rồi lạnh lùng kết luận: "Không hổ là ủy viên Thương hội Giang Nam, bản lĩnh đổi trắng thay đen khiến người ta bội phục."
- Ch.64: Gia Cát Triết Nhã đuổi Tiền Hào Sâm (phạt đền tiền phỉ thúy hỏng), Tiền Hâm đi theo. Diệp Sở hỏi món cực phẩm mới về, nàng cho lấy Tử Vi Tinh trong kho — mặt dây chuyền Tử La Lan khắc rồng tím, chính là món từng đấu giá một tỷ ở Kim Lăng, thuộc loại nhà họ Gia Cát đưa tới để làm quà nên không bán. Diệp Sở nói dối "mua tặng bạn sắp sinh nhật" (kỳ thực cho Vân Băng Uyển). Hắn tiết lộ Bách Dược Tửu có thể khiến nhà máy rượu nhà họ Gia Cát thành đệ nhất Long Quốc; bối cảnh: nhà họ Gia Cát chủ yếu nấu rượu (Giang Nam Đại Khúc), đang cần chuyển ngành, ai thành công lớn sẽ thành người thừa kế. Điều kiện của hắn: đổi lấy Tử Vi Tinh.
- Ch.65: Gia Cát Triết Nhã trời sinh đa nghi — nghe chia "ba bảy" thì tưởng Diệp Sở muốn mình ba cô bảy, ai ngờ ý hắn là mình bảy đối phương ba; cứ thế hợp tác không cần hợp đồng, nhận công thức đầy đủ ngay tại chỗ. Nàng vẫn đoán công thức bị giấu một phần. Diệp Sở bắt mạch Tôn Ngữ Nhu, phát hiện nàng là Chân Vũ Linh Thể (Trái Tim Rừng Xanh mờ vì linh khí bị cơ thể nàng hấp thu); hắn quyết phải "giải quyết" Tôn Tú Anh trước, mua thêm mấy món phỉ thúy mấy chục triệu làm quà. Văn Tiêu Sơn méc với người giới thiệu, Tôn Tú Anh mắng con gái rồi gọi điện bắt về; Diệp Sở cùng Tôn Ngữ Nhu về gặp mặt.

"""

if "### Đã xảy ra — chương 56–65:" in text_all:
    print("skip CONTEXT (co roi)")
else:
    i = next(k for k, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
    lines[i:i] = CONTEXT.split("\n")
    print("chen NGỮ CẢNH 56–65")

# ─────────── 12. REBIND Rang buc ───────────
REBIND = """### Ràng buộc cho các chương sau:
- Khương Quân Dao đã ép được Khương Phong Niên cho tạm giữ chức tổng giám đốc và toàn quyền hợp tác nhà họ Hoàng Phủ (ch.56–57). Người giúp nàng là sư tỷ (và Nhạc San), KHÔNG phải "hiền điệt Tiền" như Khương Hải Vân đang tưởng — đừng để nhân vật biết sớm. Sư tỷ nhắc nàng tìm "chỗ đó" trước khi sư phụ xuất quan, và cảnh giác đại tiểu thư nhà họ Hoàng Phủ.
- Đại phòng chưa buông: Khương Quân Long đã phái người bắt cóc Khương Quân Dao nhưng thất bại, tâm phúc mất liên lạc; Khương Quân Hổ sẽ mượn Hắc Hổ Hội ra tay với Diệp Sở để thăm dò phản ứng của nhà họ Lý; Khương Quân Lan tính ép liên hôn với Vương Tử Đằng sau khi giết Diệp Sở. Vương Tử Hào (bạn trai Quân Lan) và Vương Tử Đằng là hai người khác nhau.
- Mâu thuẫn ở phố kim hoàn đã lộ: Diệp Sở đánh La Tam Béo + Úy Trì Hùng (Hắc Hổ Hội), Tiền Hào Sâm biết hắn giữ thẻ rồng Giang Nam đứng tên Lý Tĩnh Huyên và đã đổi thái độ 180 độ; La Tam Béo mất năm triệu, Văn Tiêu Sơn bị liệt chân trái và đã méc chuyện Tôn Ngữ Nhu. Hắc Hổ Hội có chỗ dựa ở Kim Lăng nên chắc chắn quay lại báo thù.
- Gia Cát Triết Nhã đã nhận công thức Bách Dược Tửu và coi như hợp tác "ba bảy" (nàng hiểu là cô bảy, Diệp Sở nghĩ là mình bảy); nàng vẫn nghi công thức không đầy đủ. Tử Vi Tinh về tay Diệp Sở — dự định tặng Vân Băng Uyển nhân sinh nhật mấy ngày nữa; Trái Tim Rừng Xanh vẫn để Tôn Ngữ Nhu đeo.
- Tôn Ngữ Nhu là Chân Vũ Linh Thể (ch.65): trời sinh thích hợp luyện võ, tự hấp thu linh khí, chính là lý do phỉ thúy "mờ" đi. Diệp Sở định chinh phục nàng và dự tính xử Tôn Tú Anh trước; Văn Tiêu Sơn + Tôn Tú Anh là mắt xích gây rối còn treo.
- Diệp Sở vẫn đang tìm bí mật thân thế: bên nhà họ Diệp hết hy vọng, hắn nghi Vân Băng Uyển mang huyết mạch Long Tộc nên mới chủ động hòa hoãn; hai người đã qua đêm ở ch.50, Oán Long Khí bớt bạo động.
- Chiếc nhẫn sắt (vật gia truyền nhà họ Lý) vẫn là thứ Thánh Giáo nhắm tới; Lý Quảng Giang bị phế tứ chi, Cát đại sư đã chết; đà chủ Kim Lăng vẫn điều tra.
- Không đổi cách gọi đã chốt ở mục "LƯU Ý ĐẶC BIỆT" (đặc biệt: Hàn Mộng Quan, Hoàng Phủ, Lý Đầu Trọc, "anh Diệp", "hiệu kim hoàn Giang Nam", "Trái Tim Rừng Xanh", "Tiền Hào Sâm" ≠ "Tiền Hâm"). Source dùng lẫn 龙国/大夏 — dịch đúng từng chỗ, không tự gộp."""

i = next(k for k, l in enumerate(lines) if l.startswith("### Ràng buộc cho các chương sau:"))
j = len(lines)
while j > i and not lines[j - 1].strip():
    j -= 1
if "ch.56–57" in "\n".join(lines[i:j]) and "Khương Quân Dao đã ép được" in "\n".join(lines[i:j]):
    print("skip REBIND (co roi)")
else:
    lines[i:j] = REBIND.split("\n")
    print("da rebind Ràng buộc")

with io.open(GP, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
print("tong so dong:", len(lines))
