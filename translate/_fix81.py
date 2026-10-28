# -*- coding: utf-8 -*-
import io, os, re

base = r"F:\taitruyen\data\baojian_vi"
p81 = os.path.join(base, "0081_第八十一章 原委.md")

s = io.open(p81, encoding="utf-8").read()

repl = [
    ("có chút giống như rồng qua sông.", "có chút giống kẻ ngoại lai không dễ chọc."),
    ("Tuy có đôi khi có những chuyện, người trong giới", "Tuy đôi khi có những chuyện, người trong giới"),
    ("Em trai tôi đều bị người ta giết chết rồi", "Em trai tao bị người ta giết chết rồi"),
    ("đâm chết anh em họ của Viên Bính Kỳ", "đâm chết em họ của Viên Bính Kỳ"),
    ("Tần Nam", "Sân Nam"),
    ("Tần Tử Khải", "Sân Tử Khải"),
    ("lão Tần", "lão Sân"),
    ("quen biết được một cán bộ lão thành lúc đó ở Tân Thiên có địa vị cao quyền trọng, muốn từ trên người ông ta mở ra đột phá khẩu, giải quyết cục diện khốn khó là trên đầu mình không có ai nói giúp.",
     "quen được một cán bộ lão thành lúc đó có địa vị cao, quyền thế lớn ở Tân Thiên, muốn tạo đột phá từ trên người ông ta, giải quyết tình cảnh khốn khó là trên đầu không có ai chống lưng."),
    ("thì luôn có **,", "thì luôn có điểm yếu,"),
    ("chỉ thích chữ vẽ thư pháp, hơn nữa bản thân viết một tay chữ đẹp.",
     "chỉ thích tranh chữ và thư pháp, hơn nữa bản thân viết chữ rất đẹp."),
    ("mời vị cán bộ lão thành này đề từ cho", "mời vị cán bộ lão thành này đề chữ cho"),
    ("tìm được mấy đao giấy tuyên \"Tứ Xích Đan\" đời Tống, còn có mực tùng yên đầu thời Thanh",
     "tìm được mấy xấp giấy Tuyên \"Tứ Xích Đan\" đời Tống, còn có mực tùng yên đầu đời Thanh"),
    ("như bảo vật truyền gia", "như bảo vật gia truyền"),
    ("phó hội trưởng hiệp hội thư pháp kinh thành", "phó chủ tịch Hiệp hội Thư pháp Kinh thành"),
    ("sau này trận tranh giành bãi hàng logistics", "sau này trong cuộc tranh giành bến bãi logistics"),
    ("với ông nội chết tiệt của hắn ta cùng một tính tình", "với ông nội chết tiệt của cậu ta cùng một tính tình"),
    ("con trai của ông chú ngốc của ông ta, tức là em họ ruột của ông ta, bị người ta đâm chết.",
     "con trai của ông chú ngốc, tức là em họ của ông ta, bị người ta đâm chết."),
    ("Ông nội đầy ác hạnh của Viên Bính Kỳ", "Ông nội tội ác đầy mình của Viên Bính Kỳ"),
    ("lão đại năm đó bất phục chính phủ xử bắn cha mình, dẫn một đám người cầm bao thuốc nổ đi xung kích cơ quan chính phủ, bị bắn chết tại chỗ",
     "người con cả năm đó bất phục việc chính quyền xử bắn cha mình, dẫn một đám người mang bao thuốc nổ đi tấn công cơ quan chính quyền, bị bắn chết tại chỗ"),
    ("Viên Bính Kỳ tuy đàn bà không ít", "Viên Bính Kỳ tuy có không ít đàn bà"),
    ("Nhà họ Viên cũ chỉ còn lại", "Nhà họ Viên chỉ còn lại"),
    ("lo liệu cho hắn ta cưới vợ, nếu không phải Viên Đông tính tình nóng nảy đánh vợ hắn ta sảy thai, nhiệm vụ truyền tông tiếp đại của nhà họ Viên đã sớm hoàn thành rồi.",
     "lo liệu cưới vợ cho hắn ta, nếu không phải Viên Đông tính tình nóng nảy đánh vợ mình sảy thai, thì trọng trách nối dõi tông đường của nhà họ Viên đã sớm hoàn thành rồi."),
    ("trong tập đoàn Viên Bính Kỳ, cũng là một tay đánh có số.",
     "trong tập đoàn của Viên Bính Kỳ, cũng là một tay đánh đấm có hạng."),
    ("Nói Viên Đông không thể nào giống một thằng côn đồ nhỏ đi làm chuyện theo dõi",
     "Nói cho cùng, Viên Đông không thể nào giống một thằng côn đồ nhỏ đi làm chuyện theo dõi"),
    ("Theo lý mà nói Lý Thiên Viễn", "Theo lý mà nói, Lý Thiên Viễn"),
    ("Tục ngữ nói chuyện giang hồ", "Tục ngữ nói, chuyện giang hồ"),
    ("không làm ầm lên đến công an cục", "không làm ầm lên tới công an"),
    ("－－－PS: khẩn thiết cần phiếu đề cử", "PS: khẩn thiết cần phiếu đề cử"),
]

for old, new in repl:
    if old not in s:
        print("MISS:", old[:60])
    s = s.replace(old, new)

io.open(p81, "w", encoding="utf-8").write(s)

# Normalize Shen Nan name in chapters 68, 69, 71, 76
for fn in ["0068_第六十八章 地头蛇（中）.md", "0069_第六十九章 地头蛇（下）.md",
           "0071_第七十一章 旧地.md", "0076_第七十六章 结仇（中）.md"]:
    p = os.path.join(base, fn)
    t = io.open(p, encoding="utf-8").read()
    n = t.count("Tần Nam")
    t = t.replace("Tần Nam", "Sân Nam").replace("Tần Tử Khải", "Sân Tử Khải")
    io.open(p, "w", encoding="utf-8").write(t)
    print(fn, "replaced", n)

han = re.findall(r"[\u4e00-\u9fff]", s.split("\n", 1)[1] if "\n" in s else s)
print("Han left in body:", len(han))
print("paragraphs:", len([x for x in s.split("\n\n") if x.strip()]))
