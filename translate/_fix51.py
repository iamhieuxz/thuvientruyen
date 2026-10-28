# QA chu ky 5 — sua text cac chuong 46-55 (data/can_bao_chan_long_vi).
# Idempotent: moi lieu in so lan khop; chay lai lan 2 thi tat 0.
import sys, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

D = pathlib.Path(r"F:\taitruyen\data\can_bao_chan_long_vi")

# noi dung theo file cu the (ten file bat dau bang 4 chu so)
EDITS = {
"0046": [
    ("Thật không giấu gì, tôi nhân suy thận", "Thật không giấu gì, lão phu nhân suy thận"),
    ("Độc mà tôi nhân trúng", "Độc mà lão phu nhân trúng"),
    ("có tôi ở đây, tôi nhân sẽ không sao", "có tôi ở đây, lão phu nhân sẽ không sao"),
    ("bắt đầu bắt mạch cho tôi nhân", "bắt đầu bắt mạch cho lão phu nhân"),
    ("“Đại sư Cát, làm phiền ông ra tay", "“Cát đại sư, làm phiền ông ra tay"),
],
"0047": [
    ("Thận của tôi nhân suy kiệt nghiêm trọng", "Thận của lão phu nhân suy kiệt nghiêm trọng"),
    ("kéo dài tuổi thọ cho tôi nhân", "kéo dài tuổi thọ cho lão phu nhân"),
    ("đã cho tôi nhân uống Bạch Thảo Hoàn", "đã cho lão phu nhân uống Bạch Thảo Hoàn"),
    ("uống vào không lâu, tôi nhân liền từ trong cơn hôn mê tỉnh lại",
     "uống vào không lâu, lão phu nhân liền từ trong cơn hôn mê tỉnh lại"),
    ("Trong phòng ngủ biệt thự, tôi nhân nhìn ra ngoài cửa",
     "Trong phòng ngủ biệt thự, lão phu nhân nhìn ra ngoài cửa"),
    ("tôi nhân gật đầu, thần sắc đột nhiên nghiêm trọng",
     "Lão phu nhân gật đầu, thần sắc đột nhiên nghiêm trọng"),
    ("tôi nhân tháo chiếc nhẫn sắt trên tay xuống", "Lão phu nhân tháo chiếc nhẫn sắt trên tay xuống"),
    ("tôi nhân lắc đầu, “Không, chiếc nhẫn này", "Lão phu nhân lắc đầu, “Không, chiếc nhẫn này"),
    ("tôi nhân đột nhiên mở miệng, lời nói ra kinh thiên động địa",
     "Lão phu nhân đột nhiên mở miệng, lời nói ra kinh thiên động địa"),
    ("tôi thời gian không còn nhiều", "thời gian của tôi không còn nhiều"),
    ("nhớ kỹ, ngàn vạn lần không thể để người thứ hai biết", "nhớ kỹ, tuyệt đối không thể để người thứ hai biết"),
    ("“Cậu là ai? Mau tới người...”", "“Cậu là ai? Mau gọi người tới...”"),
    ("hạ cổ lên lão thái nhà họ Lý", "thả cổ trùng lên bà cụ nhà họ Lý"),
    ("“To gan tặc nhân, dám cướp đồ mà Thánh Giáo tôi để mắt, đừng chạy.”",
     "“Tên tặc nhân to gan, dám cướp đồ mà Thánh Giáo tôi để mắt, đứng lại.”"),
    ("“Đồ già, tôi ngược lại muốn xem cậu là thứ gì?”",
     "“Đồ già kia, tôi ngược lại muốn xem cậu là thứ gì?”"),
],
"0048": [
    ("“Lý tiên sinh yên tâm, có tôi ở đây, tôi nhân sẽ không sao.”",
     "“Lý tiên sinh yên tâm, có tôi ở đây, lão phu nhân sẽ không sao.”"),
    ("vị trí gia chủ, cổ phần ngân hàng, ngay cả vật tổ truyền cũng muốn cho mày",
     "vị trí gia chủ, cổ phần ngân hàng, ngay cả vật gia truyền cũng muốn cho mày"),
    ("hắn từng thăm dò hỏi chuyện vật tổ truyền", "hắn từng thăm dò hỏi chuyện vật gia truyền"),
    ("Đoán rằng bà lão phần nhiều sẽ khai ra chuyện vật tổ truyền",
     "Đoán rằng bà lão phần nhiều sẽ khai ra chuyện vật gia truyền"),
    ("Xem ra không cho các người chút khổ đầu, các người không biết lợi hại.",
     "Xem ra không cho các người nếm mùi đau khổ, các người chẳng biết thế nào là lợi hại."),
],
"0049": [
    ("lấy ra một chiếc sáo cốt nhanh chóng thổi", "lấy ra cây sáo xương nhanh chóng thổi"),
    ("bóp nát chiếc sáo cốt trong tay", "bóp nát cây sáo xương trong tay"),
    ("hôm nay tôi cho cậu biết sự lợi hại của Thánh Giáo tôi",
     "hôm nay tôi cho mày biết sự lợi hại của Thánh Giáo tôi"),
    ("“Hắc hắc, mỹ nhân nhỏ, cậu không chạy thoát được đâu.”",
     "“Hắc hắc, mỹ nhân nhỏ, mày không chạy thoát được đâu.”"),
    ("lát nữa tôi nhất định sẽ thương yêu cậu cho đàng hoàng",
     "lát nữa tôi nhất định sẽ thương yêu mày cho đàng hoàng"),
],
"0051": [
    ("Lão nhị, một phạm nhân cải tạo đúng là làm nhục môn đình",
     "Lão nhị, một tên tù cải tạo đúng là làm nhục môn đình"),
    ("còn rất thân với hành trưởng chi nhánh thành Giang Đô của ngân hàng Giang Nam",
     "còn rất thân với giám đốc chi nhánh Giang Đô của ngân hàng Giang Nam"),
    ("vị hành trưởng Lý đó rất tán thưởng Tiểu Đào nhà tôi",
     "vị giám đốc Lý đó rất tán thưởng Tiểu Đào nhà tôi"),
    ("Hành trưởng chi nhánh thành Giang Đô, đó là nhân vật ghê gớm.",
     "Giám đốc chi nhánh Giang Đô, đó là nhân vật ghê gớm."),
    ("Tiểu hữu tuổi còn trẻ đã được hành trưởng Lý coi trọng",
     "Tiểu hữu tuổi còn trẻ đã được giám đốc Lý coi trọng"),
],
"0052": [
    ("“Đúng vậy, thế phong nhật hạ, nhân tâm bất cổ a.”",
     "“Đúng vậy, thế đạo suy mạt, lòng người chẳng còn như xưa.”"),
],
"0053": [
    ("“Hai thúc, không đáng tức giận", "“Nhị thúc, không đáng tức giận"),
    ("bạn của phạm nhân cải tạo tám phần cũng là phạm nhân cải tạo",
     "bạn của tù cải tạo tám phần cũng là tù cải tạo"),
    ("nhất định là Lý hành trưởng tặng cho Tiểu Đào", "nhất định là Giám đốc Lý tặng cho Tiểu Đào"),
],
"0054": [
    ("Khương Hải Vân vội vàng xua tay: “Mỹ Tĩnh, chị mau đừng nói vậy",
     "Khương Hải Vận vội vàng xua tay: “Mỹ Tĩnh, chị mau đừng nói vậy"),
    ("Khương Hải Vân cũng bước lên mỉa mai: “Mộng Quan, nghe nói con rể nhà em",
     "Khương Hải Vận cũng bước lên mỉa mai: “Mộng Quan, nghe nói con rể nhà em"),
    ("Khương Hải Vân thở dài: “Haizz, Mộng Quan, không phải chị cả không giúp em",
     "Khương Hải Vận thở dài: “Haizz, Mộng Quan, không phải chị cả không giúp em"),
    ("Khương Hải Vân không nhịn được nói: “Quản lý, cô có nhầm không?",
     "Khương Hải Vận không nhịn được nói: “Quản lý, cô có nhầm không?"),
    ("Khương Hải Vân không thể chấp nhận, “Còn rượu lúc nãy",
     "Khương Hải Vận không thể chấp nhận, “Còn rượu lúc nãy"),
    ("Khương Hải Vân thân hình loạng choạng, suýt đứng không vững",
     "Khương Hải Vận thân hình loạng choạng, suýt đứng không vững"),
    ("Khi nói, cố ý nhìn Khương Hải Vân với vẻ trêu cợt: “Chị cả, con rể chị",
     "Khi nói, cố ý nhìn Khương Hải Vận với vẻ trêu cợt: “Chị cả, con rể chị"),
    ("Khương Hải Vân tức đến thân hình run rẩy, hô hấp cũng không thông",
     "Khương Hải Vận tức đến thân hình run rẩy, hô hấp cũng không thông"),
    ("Nhưng chị nửa ngày, lại không nói ra được một câu.",
     "Nhưng nghẹn nửa ngày, lại không nói ra được một câu."),
    ("Khương Hải Vân thân hình run càng dữ dội, ánh mắt chết chết nhìn Hàn Mộng Quan.",
     "Khương Hải Vận thân hình run càng dữ dội, ánh mắt chằm chằm nhìn Hàn Mộng Quan."),
    ("Sao con lại quen Lý hành trưởng?", "Sao con lại quen Giám đốc Lý?"),
],
"0055": [
    ("Quân Long nay đã toàn diện đạt được hợp tác với nhà họ Hoàng,",
     "Quân Long nay đã toàn diện đạt được hợp tác với nhà họ Hoàng Phủ,"),
],
}

total = 0
for stem, pairs in EDITS.items():
    files = sorted(D.glob(f"{stem}*.md"))
    assert len(files) == 1, (stem, files)
    f = files[0]
    t = t0 = f.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        total += n
        if n:
            t = t.replace(old, new)
        print(f"{n} x {stem}: {old[:52]}")
    if t != t0:
        f.write_text(t, encoding="utf-8", newline="\n")
print("== tong so lieu thay:", total)
