# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl11.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")


def has_key(key):
    for l in lines:
        if "=" in l and not l.startswith("#") and not l.startswith(" "):
            if l.split("=")[0].strip() == key:
                return True
    return False


def add_entries(header, entries):
    new = []
    for zh, vi in entries:
        if has_key(zh):
            print("  DA CO (bo qua):", zh)
            continue
        new.append("%s = %s" % (zh, vi))
    if not new:
        return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]
            print("  + %d muc truoc %s" % (len(new), header[:26]))
            return
    print("  CANH: khong thay header", header)


def insert_prose(header_prefix, block):
    first = block.strip().split("\n")[0]
    if any(l.strip() == first for l in lines):
        print("  skip (da co):", first)
        return
    for i, l in enumerate(lines):
        if l.startswith(header_prefix):
            lines[i:i] = block.strip("\n").split("\n") + ["", ""]
            print("  + block truoc", header_prefix[:26])
            return
    print("  CANH: khong thay", header_prefix)


def replace_key(key, new_line):
    for i, l in enumerate(lines):
        if "=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == key:
            print("  SUA", key, "->", new_line[:70])
            lines[i] = new_line
            return
    print("  CANH: khong thay khoa", key)


# ── NHÂN VẬT PHỤ ────────────────────────────────────────────────
add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("龙灿阳", 'Long Xán Dương (thiếu gia nhị phòng nhà họ Long, anh trai Long Tuyết Phi; hống hách ở tiệc nhà họ Tần rồi bị Diệp Sở dạy cho một trận — ch.140–145)'),
    ("龙雪菲", 'Long Tuyết Phi (tiểu thư nhị phòng nhà họ Long, em gái Long Xán Dương, kiêu căng; bị Đông Mai tát ở ch.141 — ch.140–145)'),
    ("龙鼎天", 'Long Đỉnh Thiên (lão gia/nguyên gia chủ nhà họ Long, "định hải thần châm" của Long gia, cha Long Trấn Sơn; ch.146 ra mặt tha cho Khương Quân Dao vì nợ ơn Hồng Liên chân nhân và vì "phía đế đô có người che chở Diệp Sở")'),
    ("红莲真人", 'Hồng Liên chân nhân (chưởng môn phái Nga Mi, sư phụ của Khương Quân Dao, có ơn với nhà họ Long — ch.145–146)'),
    ("郑轩", 'Trịnh Hiên (đệ tử của Y Thánh Kim Lăng, gọi Tư Đồ Tĩnh là "sư muội", tham lam đóa Hoàng Tuyền Hoa, nhiều lần bị Diệp Sở bẽ mặt — ch.155–162)'),
    ("林自如", 'Lâm Tự Như (gia chủ nhà họ Lâm ở Kinh Khẩu, trung niên, con của vị "ông cụ" bị người ta gieo hạt Hoàng Tuyền Hoa vào não; gọi Lý Chính Nguyên là "Lý thúc" — ch.155–159)'),
    ("安小舞", 'An Tiểu Vũ (nữ hơn hai mươi, tóc búi tròn, mặt bầu bĩnh, đệ tử mới của Lý Chính Nguyên, lái xe đưa ông tới Kinh Khẩu ch.154; PHẢN BỘI: chính là kẻ hạ Tam Thi độc lên nhà họ Lâm rồi thảm sát cả nhà ở ch.163 — không được tả như nhân vật phụ vô hại)'),
    ("法藏", 'Pháp Tàng (đại sư trụ trì chùa Kim Sơn ở Kinh Khẩu, gọi Lâm Tự Như là "Lâm thí chủ", nuôi Kim Thiền để ăn hạt hoa trong não người — ch.155–162)'),
    ("金蝉", 'Kim Thiền (con tằm vàng cỡ hạt gạo, sủng vật của Pháp Tàng, chui vào não ăn hạt Hoàng Tuyền Hoa — ch.157–158)'),
    ("赵森", 'Triệu Sâm (đại thiếu gia nhà họ Triệu ở thành Kinh Khẩu, kẻ từng sai người "dạy dỗ" Diệp Sở; mẹ bị trúng Tam Thi độc, ch.163 vu Diệp Sở diệt sạch nhà họ Lâm — ch.155–163)'),
    ("张大师", 'Trương đại sư (võ giả Đoán Thể tám đoạn được nhà họ Tần cúng dưỡng, bị Đông Mai bẻ gãy cổ tay — ch.141)'),
    ("东梅", 'Đông Mai (nha hoàn/thân tín của Hoàng Phủ Thi Nguyệt, người dò tin tức cho nàng; bị Hoàng Phủ Kiệt gọi là "nô tài nhà họ Hoàng Phủ" — ch.95–165)'),
])

# ── THẾ LỰC / ĐỊA DANH ─────────────────────────────────────────
add_entries("## ══════ ĐỊA DANH", [
    ("峨眉派", 'phái Nga Mi (môn phái ở xa Giang Đô, chưởng môn là Hồng Liên chân nhân; Khương Quân Dao là đệ tử — ch.145–146)'),
    ("峨眉令", 'Nga Mi lệnh (ngọc bài khắc hai chữ "Nga Mi", dùng chứng minh thân phận đệ tử Nga Mi — ch.145)'),
    ("京口林家", 'nhà họ Lâm ở Kinh Khẩu (gia tộc của Lâm Tự Tại, gia chủ là Lâm Tự Như; bị An Tiểu Vũ hạ độc rồi thảm sát — ch.154–163)'),
    ("秦家", 'nhà họ Tần (một trong bốn đại hào tộc Giang Đô, gia tộc của Tần Đông Dương; tổ chức tiệc tối và ngấm ngầm đánh phá Vân Mộng Dược Nghiệp — ch.137–153)'),
    ("京口市", 'thành Kinh Khẩu (thành phố bên cạnh Giang Đô, nơi có nhà họ Lâm và chùa Kim Sơn — VIẾT "Kinh Khẩu", KHÔNG viết "Kim Khẩu", ch.154–159)'),
    ("金山寺", 'chùa Kim Sơn (chùa ở thành Kinh Khẩu, nơi Pháp Tàng trụ trì — ch.155–162)'),
])

# ── Y HỌC / THUẬT NGỮ ──────────────────────────────────────────
add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("黄泉花", 'Hoàng Tuyền Hoa (linh hoa độc dị: hạt gieo vào não người, hút máu nuôi hạt, khiến vật chủ mất trí nhớ và suy kiệt; Diệp Sở cần để luyện đan — ch.155–161)'),
    ("龙胆草", 'Long Đảm Thảo (dược liệu quý nhà họ Lâm trả làm thù lao cho Diệp Sở — ch.156–159)'),
    ("三尸毒", 'Tam Thi độc (độc khiến võ giả mất sức chiến đấu; An Tiểu Vũ dùng để hạ cả nhà họ Lâm, Oán Long Khí trong người Diệp Sở ăn được độc này — ch.163)'),
    ("八戒面具", 'mặt nạ Bát Giới (mặt nạ kẻ bí ẩn đeo ở ch.159)'),
])

add_entries("## ══════ QUY TẮC XƯNG HÔ", [
    ("龙少", 'Long thiếu (cách người ngoài gọi Long Xán Dương — VIẾT "Long thiếu", ch.140)'),
    ("皇甫少爷", 'Hoàng Phủ thiếu gia (cách gọi Hoàng Phủ Kiệt — ch.141)'),
    ("司徒姑娘", 'Tư Đồ cô nương (cách gọi Tư Đồ Tĩnh — ch.160)'),
    ("林施主", 'Lâm thí chủ (cách Pháp Tàng gọi Lâm Tự Như — ch.157)'),
    ("李叔", 'Lý thúc (cách Lâm Tự Như gọi Lý Chính Nguyên — ch.154–155)'),
    ("叶小友", 'Diệp tiểu hữu (cách Lâm Tự Như và giới y học gọi Diệp Sở — ch.157)'),
])

# ── CẬP NHẬT ENTRY CŨ ───────────────────────────────────────────
replace_key("皇甫杰", '皇甫杰 = Hoàng Phủ Kiệt (thiếu gia nhà họ Hoàng Phủ, ngang ngược háo sắc, coi Đông Mai là "nô tài nhà họ Hoàng Phủ"; quấy rối Đông Mai ch.142, âm mưu thâu tóm Vân Mộng Dược Nghiệp và hạ bệ Hoàng Phủ Thi Nguyệt — ch.137–165)')
replace_key("老爷子", '老爷子 = ông cụ (cách gọi chung vị gia chủ/lão bối đứng đầu một gia tộc, KHÔNG riêng nhà họ Khương: ông cụ nhà họ Khương, ông cụ nhà họ Tần, ông cụ nhà họ Lâm…; KHÁC 老爷 = "lão gia" trong lời quản gia gọi chủ nhân, ch.1, 3, 93)')

# ── LƯU Ý ĐẶC BIỆT 39–42 ───────────────────────────────────────
insert_prose("## ══════ VĂN PHONG", """
39. 老爷子 luôn dịch "ông cụ" cho MỌI gia tộc (đã đồng nhất toàn bộ: sửa "lão gia"/"Lão gia tử"/"Lão gia nhà họ Tần" ở ch.15, 16, 39, 140, 146, 155–157, 161). NHƯNG 老爷 trong lời quản gia gọi chủ nhân vẫn là "lão gia" — ch.1, 3, 93 giữ nguyên, không được đổi.
40. 京口 = "Kinh Khẩu" (đã sửa "Kim Khẩu" ở ch.155–156). 京口林家 = "nhà họ Lâm ở Kinh Khẩu"; 金山寺 = "chùa Kim Sơn".
41. 皇甫杰 ≠ Hoàng Phủ Thi Nguyệt, hắn là thiếu gia ngang ngược trong tộc, gọi Đông Mai là "nô tài nhà họ Hoàng Phủ" (Đông Mai là nha hoàn của Hoàng Phủ Thi Nguyệt, KHÔNG phải người tự do). Source ch.155 có một chỗ gõ nhầm 李家主 trong khi người nói là Lâm Tự Như — bản dịch giữ "Lâm gia chủ", không bày ra nhân vật họ Lý thứ hai.
42. 安小舞 là đệ tử mới của Lý Chính Nguyên (ch.154) nhưng chính là hung thủ hạ Tam Thi độc rồi thảm sát nhà họ Lâm (ch.163); 林自在 là bách hộ Hộ Long Vệ, con trai vị "ông cụ" nhà họ Lâm, phải sống sót nhờ bảo vật giữ mạng. Không được tả hai người này như nhân vật phụ vô hại.
""")

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG chu ky 11. tong so dong:", len(lines))