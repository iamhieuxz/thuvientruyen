# Chu kỳ 7: cập nhật glossary + ngữ cảnh sau ch.66–75 (idempotent)
import io, shutil, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "F:/taitruyen/translate/glossary_can_bao_chan_long.txt"
BAK = "F:/taitruyen/translate/_bak_glossary_cycl7.txt"
shutil.copyfile(G, BAK)

txt = io.open(G, encoding="utf-8").read()
lines = txt.split("\n")


def has(prefix):
    return any(l.startswith(prefix) for l in io.open(G, encoding="utf-8").read().split("\n"))


def insert_after(prefix, block):
    ls = io.open(G, encoding="utf-8").read().split("\n")
    if has(block.split("\n")[0][:14]):
        print("  (da co) ", prefix[:24])
        return
    for i, l in enumerate(ls):
        if l.startswith(prefix):
            ls[i + 1: i + 1] = block.split("\n")
            io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(ls))
            print("  + sau:", prefix[:30])
            return
    print("  !! KHONG THAY ANCHOR:", prefix[:40])


def insert_before(prefix_header, block):
    ls = io.open(G, encoding="utf-8").read().split("\n")
    if has(block.split("\n")[0][:14]):
        print("  (da co) ", prefix_header[:24])
        return
    for i, l in enumerate(ls):
        if l.startswith(prefix_header):
            ls[i:i] = block.split("\n")
            io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(ls))
            print("  + truoc:", prefix_header[:30])
            return
    print("  !! KHONG THAY ANCHOR:", prefix_header[:40])


# ─────────── NHÂN VẬT PHỤ ───────────
insert_after("岳珊 = Nhạc San", """陈子豹 = Trần Tử Báo (đường chủ Hắc Hổ Hội thực lực mạnh nhất, đàn em gọi "Báo ca", Tả Tu Đao gọi tắt "A Báo"; ch.67–75)
孟小刀 = Mạnh Tiểu Đao (đường chủ Hắc Hổ Hội xếp chót trong các đường chủ, Đoán Thể bảy đoạn, một tay phi đao cực lợi hại, đàn em gọi "Đao ca"; ch.67–69)
梦小刀 = Mạnh Tiểu Đao (source gõ nhầm 梦小刀 đúng một chỗ ở ch.68 — bản dịch CHỈ dùng "Mạnh Tiểu Đao", tuyệt đối không viết "Mộng Tiểu Đao")
白鹤老人 = Bạch Hạc lão nhân (đường chủ Hắc Hổ Hội, Đoán Thể chín đoạn, một tay Bạch Hạc Quyền, thực lực chỉ thua Trần Tử Báo; bị Diệp Sở một quyền đánh gục ở ch.69)
眼镜哥 = Kính ca (đầu gấu tóc cua đeo kính, cầm đầu đám quấy rối Tôn Ngữ Nhu ở ch.66, thuộc hạ Hắc Hổ Hội; đàn em gọi "Kính ca")
左修刀 = Tả Tu Đao (phó hội chủ Hắc Hổ Hội, anh em với Trần Tử Báo, đàn em gọi "Đao ca"; kẻ bày trò đổi thuốc kích dục thành độc dược để hãm hại Diệp Sở, ch.74–75)
唐千刃 = Đường Thiên Nhận (tay chân tra xét của Hắc Hổ Hội, người tra ra Diệp Sở là kẻ ở rể nhà họ Khương; Tả Tu Đao gọi tắt "Thiên Nhận", ch.74)
白晓晓 = Bạch Hiểu Hiểu (phó hội chủ Bạch Lang Hội, da màu lúa mạch, phong thái hoang dã, đang mang thương; Lý Đầu Trọc và Đao Sẹo Trần gọi "lão đại"; được Diệp Sở ban đan dược và thu phục ở ch.71–74)
蔷薇 = Tường Vi (nữ đường chủ Bạch Lang Hội, gọi Đao Sẹo Trần là "Đao Sẹo ca", phản đối đầu nhập thế lực khác, ch.67–68)
龙镇山 = Long Trấn Sơn (trưởng bối nhà họ Long, cha ruột Vân Băng Uyển; năm xưa cưỡng bức bà bảo mẫu nên sinh ra nàng, nay ép nàng gả cho một lão già Chân Vũ Tông, ch.72–73)
龙九阳 = Long Cửu Dương (thiếu chủ nhà họ Long; nhà họ Long gả Vân Băng Uyển cho lão già Chân Vũ Tông để đổi lấy việc cho hắn bái nhập tông môn, ch.72–73)""")

# ─────────── THẾ LỰC ───────────
insert_after("王朝夜总会 = câu lạc bộ đêm Vương Triều", """夜王朝 = Vương Triều Dạ (câu lạc bộ đêm số một thành Giang Đô, khu Đông Thành, chín tầng, đồng thời là tổng bộ Hắc Hổ Hội, ch.75 — source viết 夜王朝, khác với 王朝夜总会 ở ch.16–17, dịch đúng từng chỗ)
真武宗 = Chân Vũ Tông (tông môn mà nhà họ Long muốn cho Long Cửu Dương bái nhập; một lão già của tông môn này lấy Vân Băng Uyển làm "thiếp", thực chất là lò luyện, ch.72–73)""")

# ─────────── VŨ ĐẠO ───────────
insert_after("武道宗师 = võ đạo tông sư", """白鹤拳 = Bạch Hạc Quyền (công pháp của Bạch Hạc lão nhân, ch.69)
横练 = hoành luyện (thuật luyện thân thể cứng rắn; "hoành luyện vô địch" — Diệp Sở chê Bạch Hạc lão nhân, ch.69)""")

# ─────────── Y HỌC ───────────
insert_after("祛煞丹 = Khu Sát Đan", """开脉丹 = Khai Mạch Đan (đan dược Diệp Sở luyện riêng ở ch.74, "có thể giúp Khai Mạch tông sư đột phá", ban hai viên cho Bạch Hiểu Hiểu; VIẾT HOA)
毒药 = độc dược (thứ Tả Tu Đao đổi thay thuốc kích dục trong âm mưu hãm hại Diệp Sở, ch.74)""")

# ─────────── THUẬT NGỮ CHUNG ───────────
insert_after("江南大曲 = Giang Nam Đại Khúc", """丹纹 = đan văn (vân nổi trên đan dược khi luyện thành, dấu hiệu đan chất cao, ch.73)
炉鼎 = lò luyện (người bị dùng như dụng cụ tu luyện để bồi bổ kẻ khác; Vân Băng Uyển bị nhà họ Long định gả làm "thiếp", thực chất là lò luyện, ch.73)
教育费 = phí giáo dục (Diệp Sở bắt La Tam Béo trả "mỗi người mười vạn" sau khi đánh đám Hắc Hổ Hội, ch.69)
催情药 = thuốc kích dục (thứ Khương Quân Hổ định hạ Diệp Sở, bị Tả Tu Đao đổi thành độc dược, ch.74)""")

# ─────────── ĐỊA VỊ - CHỨC VỤ ───────────
insert_after("钱总 = Tiền tổng", """老大 = lão đại (kẻ đứng đầu một thế lực — 白狼会老大 → "lão đại Bạch Lang Hội"; KHÔNG dịch thành "đại ca")
大哥 = đại ca (xưng hô anh em/bề trên — 几位大哥 → "mấy vị đại ca"; KHÁC hẳn 老大)
会主 = hội chủ (source dùng lẫn 会长 và 会主 cho cùng một chức — bản dịch nhất quán "hội chủ", KHÔNG viết "hội trưởng")
副会主 = phó hội chủ (nhất quán cho cả 副会长: Tả Tu Đao bên Hắc Hổ Hội, Bạch Hiểu Hiểu bên Bạch Lang Hội)
阿豹 = A Báo (Tả Tu Đao gọi tắt Trần Tử Báo, ch.75)
豹哥 = Báo ca (đàn em Hắc Hổ Hội gọi Trần Tử Báo)
刀哥 = Đao ca (đàn em gọi Mạnh Tiểu Đao ở ch.67 VÀ gọi Tả Tu Đao ở ch.74–75 — hai người khác nhau, phải dựa vào chương để phân biệt)
刀疤哥 = Đao Sẹo ca (đàn em Bạch Lang Hội gọi Đao Sẹo Trần — KHÔNG viết tắt thành "Đao ca")""")

# ─────────── QUY TẮC XƯNG HÔ ───────────
insert_before("### Thánh Giáo (ch.31):", """### Hắc Hổ Hội / Bạch Lang Hội (ch.66–75):
- Đàn em Hắc Hổ Hội: gọi Trần Tử Báo → "Báo ca"; gọi Mạnh Tiểu Đao (ch.67) và Tả Tu Đao (ch.74–75) → "Đao ca"; Tả Tu Đao gọi Trần Tử Báo → "A Báo".
- Đàn em Bạch Lang Hội: gọi Đao Sẹo Trần → "Đao Sẹo ca"; gọi Bạch Hiểu Hiểu → "lão đại" (theo 老大) hoặc "phó hội chủ" (theo 副会主).
- Lý Đầu Trọc, Đao Sẹo Trần gọi Diệp Sở → "đại nhân", tự xưng "thuộc hạ"/"chúng tôi".
- Trần Tử Báo, Tả Tu Đao, Bạch Hạc lão nhân lúc chưa biết thân phận → "nhóc con"/"thằng nhóc"/"tiểu bối"; sau khi biết là tông sư → "vị tiền bối này", "đại nhân".
- Khương Quân Hổ gọi Diệp Sở → "anh rể" (miệt thị), gọi Trần Tử Báo → "Báo ca".
- Tôn Tú Anh gọi Diệp Sở → "Tiểu Diệp"/"cậu trai"; Vân Băng Uyển gọi → "cậu"/"kẻ ở rể"; bà lão Long gia gọi → "các hạ" rồi "tiểu hữu" rồi "chủ nhân" sau khi bị thuần phục.
- Chức trong hai hội: 会长/会主 → "hội chủ", 副 → "phó hội chủ", 堂主 → "đường chủ", 老大 → "lão đại".""".rstrip("."))

print("--- LƯU Ý ĐẶC BIỆT + NGỮ CẢNH ---")
