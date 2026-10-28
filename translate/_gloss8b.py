# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl8b.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")


def has_key(key):
    return any("=" in l and not l.startswith("#") and not l.startswith(" ")
               and l.split("=")[0].strip() == key for l in lines)


def add_entries(header, entries):
    new = ["%s = %s" % (zh, vi) for zh, vi in entries if not has_key(zh)]
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]
            print("  + %d muc: %s" % (len(new), ", ".join(z for z, v in entries)))
            return


add_entries("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("玄字号", 'Huyền tự (tự hiệu của thành viên Hộ Long Vệ — "thành viên Huyền tự của Hộ Long Vệ"; '
              'ĐÃ CHOT: viết "Huyền tự", KHÔNG viết "hạng Huyền")'),
    ("玄虎队", 'đội Huyền Hổ (nhóm bốn người Hộ Long Vệ do Mã Tứ Thủy dẫn đầu tới Giang Đô vây bắt '
              'Lạc Thiên Tuyệt, Kim Bằng xin đi theo; trong nhóm có gã mập lùn, gã cao lớn xăm rồng đen '
              'trên cánh tay, gã vạm vỡ tên Mãn Hùng và gã thanh niên âm nhu — ch.93)'),
    ("特殊部门", 'bộ phận đặc biệt (Hộ Long Vệ là bộ phận đặc biệt của Đại Hạ, ngầm giữ yên ổn cho đất '
              'nước, tập hợp tinh anh cả nước — ch.91, 92)')
])

add_entries("## ══════ NHÂN VẬT PHỤ", [
    ("杨阿姨", 'dì Dương (phụ nữ trung niên đi cùng Chu Bẩm Thiên; Chu Tử Nghĩa gọi là "dì Dương"; '
               'Chu Bẩm Thiên đem lòng theo đuổi sau khi nàng vô tình xông nhầm phòng — ch.87)')
])

# Ghi chu vao LƯU Ý ĐẶC BIỆT (muc 31)
first = "31. "
if not any(l.startswith(first) for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("## ══════ VĂN PHONG"):
            lines[i:i] = ['31. 玄字号 luôn dịch là "Huyền tự" (đã sửa toàn bộ ch.92–93, không còn chỗ nào '
                          'viết "hạng Huyền"); 玄虎队 là "đội Huyền Hổ", 特殊部门 là "bộ phận đặc biệt". '
                          'Source ch.91–92 gọi Long Quốc là 大夏 — giữ nguyên "Đại Hạ" theo từng chỗ '
                          '(xem mục 19), không tự đổi thành "Long Quốc".', "", ""]
            print("  + LƯU Ý muc 31")
            break

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG:", len(lines), "dong")
