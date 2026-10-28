# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl10.txt")

lines = io.open(G, encoding="utf-8").read().split("\n")


def has_key(key):
    for l in lines:
        if "=" in l and not l.startswith("#") and not l.startswith(" "):
            if l.split("=")[0].strip() == key:
                return True, l
    return False, None


def add_entries(header, entries):
    new = []
    for zh, vi in entries:
        ok, old = has_key(zh)
        if ok:
            print("  DA CO (bo qua):", zh, "->", old[:80])
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


# ── NHÂN VẬT PHỤ ────────────────────────────────────────────────
add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("苏定夏", 'Tô Định Xạ (thống lĩnh Hộ Long Vệ, đầu cua, mặt cương nghị, mắt hổ không giận mà uy; ch.127–132 chủ trì việc xử lý vụ Diệp Sở giết người Hộ Long Vệ, sau quyết định chiêu mộ — VIẾT "Tô Định Xạ" theo bản dịch đã chốt, ch.127–135)'),
    ("陆展元", 'Lục Triển Nguyên (thành viên Địa tự của Hộ Long Vệ, mặt như dao đẽo, mắt như chim ưng; được phái tới Giang Đô tiếp quản việc truy bắt Lạc Thiên Tuyệt, cậy quyền áp Diệp Sở, là kẻ hại đồng đội để lập công — VIẾT "Lục Triển Nguyên", ch.121–133)'),
    ("林自在", 'Lâm Tự Tại (bách hộ Hộ Long Vệ, cấp dưới của Tô Định Xạ; ch.132–134 tới điều tra vụ Diệp Sở, trở mặt đòi hỏi tội rồi thua một chiêu, quay sang mời chào Diệp Sở gia nhập Hộ Long Vệ với chức bách hộ — ch.132–135)'),
    ("幽兰", 'U Lan (thánh nữ Vu Cổ Giáo, đeo mặt nạ, dung mạo yêu kiều; tìm Khương Quân Dao bàn chuyện hợp tác khai quật cổ mộ vì cho rằng cổ mộ bị trận pháp che giấu — VIẾT "U Lan", ch.119–127)'),
    ("李三刀", 'Lý Tam Đao (em họ của Trương Ma Tử, trung niên gây chuyện ở quán bar Tinh Nguyệt, bị Trương Ma Tử đá mắng — ch.119)'),
    ("张麻子", 'Trương Ma Tử (đại ca giang hồ khu Tây Thành Giang Đô, mặt rỗ, quản đám đàn em ở quán bar Tinh Nguyệt; vô cùng kính sợ Diệp Sở — ch.119)'),
    ("龙镇山", 'Long Trấn Sơn (gia chủ nhà họ Long, "thổ hoàng đế" Giang Đô; sau khi biết có Hóa Kình đại tông sư mới xuất hiện liền sai người điều tra Sở Bá Vương — ch.106, 110, 128–135)'),
    ("龙镇河", 'Long Trấn Hà (lão nhị nhà họ Long, em trai Long Trấn Sơn, chưa lộ diện nhiều — ch.134)'),
    ("龙百岳", 'Long Bách Nhạc (người nhà họ Long, được nhắc tới ở ch.133)'),
    ("金护法", 'Kim hộ pháp (hộ pháp Hộ Long Vệ, cùng bàn xử lý vụ Diệp Sở với Chu Bẩm Thiên ở thành vệ quân — ch.121)'),
])

# ── THẾ LỰC / ĐỊA DANH ──────────────────────────────────────────
add_entries("## ══════ ĐỊA DANH", [
    ("巫蛊教", 'Vu Cổ Giáo (giáo phái cổ thuật ở phương nam, thế lực mạnh nhưng thần bí quái dị, tổ chức theo "thánh nữ"/"hộ pháp"; Khương Quân Dao không tin nổi — VIẾT "Vu Cổ Giáo", ch.119–127)'),
    ("中州陆家", 'nhà họ Lục ở Trung Châu (thế lực đứng sau Lục Triển Nguyên của Hộ Long Vệ — ch.124, 126)'),
    ("中州", 'Trung Châu (vùng đất trung tâm, quê gốc của nhà họ Lục — VIẾT "Trung Châu", ch.124, 126)'),
    ("星月酒吧", 'quán bar Tinh Nguyệt (quán bar ở khu Tây Thành Giang Đô, địa bàn của Trương Ma Tử — ch.118–119)'),
    ("西城区", 'khu Tây Thành (một trong các quận của Giang Đô — VIẾT "khu Tây Thành", ch.118)'),
])

# ── VŨ ĐẠO / ĐỊA VỊ ─────────────────────────────────────────────
add_entries("## ══════ Y HỌC - THUẬT NGỮ", [
    ("百户", 'bách hộ (chức vụ trong Hộ Long Vệ, quyền ngang chức thị trưởng Giang Đô nhưng thực quyền lớn hơn; Lâm Tự Tại giữ chức này, đề nghị cho Diệp Sở làm bách hộ khi chiêu mộ — ch.132–135)'),
    ("地字号", 'Địa tự (một trong các "tự hiệu" chia thành viên Hộ Long Vệ, trên Huyền tự; Lục Triển Nguyên là thành viên Địa tự — ch.121)'),
])
add_entries("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("形意拳", 'Hình Ý Quyền (môn quyền pháp Lâm Tự Tại dùng đấu với Diệp Sở, dáng như hổ vồ — VIẾT "Hình Ý Quyền", ch.133)'),
    ("阵法", 'trận pháp (bố trí huyền bí che giấu cổ mộ khiến máy móc hiện đại không tìm ra — ch.120)'),
    ("令牌", 'lệnh bài (vật của Vu Cổ Giáo dùng để triệu tập/chứng minh thân phận — ch.120)'),
    ("古墓", 'cổ mộ (ngôi mộ cổ mà Khương Quân Dao đang tìm, bị trận pháp che giấu; nhiều thế lực cùng nhòm ngó — ch.120, 127, 129)'),
])
add_entries("## ══════ CẤM TỪ (TUYỆT ĐỐI KHÔNG XUẤT HIỆN TRONG BẢN DỊCH)", [
    ("小生机丹", 'Tiểu Sinh Cơ Đan (đan trị thương Diệp Sở luyện để cứu Mã Tứ Thủy, bổ sinh cơ mạnh — ĐAN DƯỢC LUÔN VIẾT HOA, ch.117–124)'),
    ("大真元丹", 'Đại Chân Nguyên Đan (đan dược cao cấp nhắc ở ch.120 — VIẾT HOA)'),
    ("气血丹", 'Khí Huyết Đan (đan bổ khí huyết, ch.121 — VIẾT HOA)'),
    ("大巫天经", 'Đại Vu Thiên Kinh (kinh điển/thần công của Vu Cổ Giáo — VIẾT "Đại Vu Thiên Kinh", ch.120)'),
    ("鸿门宴", 'Hồng Môn Yến (thành ngữ chỉ bữa tiệc có âm mưu hại người — giữ "Hồng Môn Yến", ch.123)'),
])

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG phan 1 chu ky 10. tong so dong:", len(lines))