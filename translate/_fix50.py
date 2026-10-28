# Sua tay draft _0050_nhap.md: dai tu "con"->"cháu" (Quan Ho noi voi nhi thuc/nhi tham),
# quy uoc "giám đốc" thay "đổng sự trưởng", va vai cum thieu tu nhien.
# Chay idempotent: lieu nao da ap dung thi dem 0.
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = pathlib.Path(r"F:\taitruyen\data\can_bao_chan_long_vi\_0050_nhap.md")
t = p.read_text(encoding="utf-8")

REPL = [
    # Dai tu cua Khương Quan Ho khi noivoi chu / thi
    ("“Nhị thẩm đừng giận, con chỉ nói đùa thôi.”",
     "“Nhị thẩm đừng giận, cháu chỉ nói đùa thôi.”"),
    ("“Ông nội họ ở phòng bao tầng thượng, mọi người lên trước đi, con đợi đại cô họ một chút.”",
     "“Ông nội đang ở phòng bao tầng thượng, mọi người lên trước đi, cháu đợi đại cô một chút.”"),
    ("“Nhị thúc, để anh rể ở lại đi, con một mình rảnh rỗi vô vị, muốn tìm người trò chuyện.”",
     "“Nhị thúc, để anh rể ở lại đi, cháu đang rảnh quá hóa phiền, muốn tìm người trò chuyện.”"),
    ("“Tên đó vừa nãy nói có chút việc rời đi một lát, nửa ngày không về, con đành dẫn đại cô họ lên trước.”",
     "“Tên đó vừa nãy nói có chút việc rời đi một lát, nửa ngày không về, cháu đành dẫn đại cô lên trước.”"),
    # 董事长 / 李董 -> theo quy uoc "giám đốc" cua toan bo ban dich
    ("chỉ đến chào hỏi Lý đổng một tiếng", "chỉ đến chào hỏi Giám đốc Lý một tiếng"),
    ("“Đổng sự trưởng, không ngờ ông còn nhớ tôi, thật là vinh hạnh của thuộc hạ.”",
     "“Giám đốc, không ngờ ông còn nhớ tôi, thật là vinh hạnh của thuộc hạ.”"),
    ("tôi chỉ thấy đổng sự trưởng, muốn đến chào hỏi một tiếng",
     "tôi chỉ thấy giám đốc, muốn đến chào hỏi một tiếng"),
    ("“Đổng sự trưởng đi thong thả.”", "“Giám đốc đi thong thả.”"),
    # Cum tu may moc
    ("Nói xong liền trong sự hộ tống của hai vệ sĩ bước vào khách sạn.",
     "Nói xong, ông ta được hai vệ sĩ hộ tống rồi bước vào khách sạn."),
    ("làn da trắng như ngọc điểm những vết hằn, kể lại sự điên cuồng của đêm qua",
     "làn da trắng như ngọc lốm đốm vết sẹo, kể lại sự điên cuồng của đêm qua"),
    ("Nhất định phải nghĩ cách giải quyết Vân Băng Uyển", "nhất định phải nghĩ cách lo liệu cho Vân Băng Uyển"),
    ("nhất định phải nghĩ cách giải quyết Vân Băng Uyển", "nhất định phải nghĩ cách lo liệu cho Vân Băng Uyển"),
    ("chiếc Rolls-Royce phiên bản kéo dài chạy tới", "chiếc Rolls-Royce thân dài chạy tới"),
    ("“涛哥", "“anh Đào"),
    ("thằng đó một phạm nhân cải tạo", "thằng đó là cái tên tù cải tạo"),
    ("Ngoài ba người Khương Hải Vân ra", "Ngoài ba người nhà Khương Hải Vân ra"),
    ("vị kia lẽ nào chính là hành trưởng chi nhánh Giang Đô của ngân hàng Giang Nam Lý Quảng Lăng?",
     "vị kia lẽ nào chính là Lý Quảng Lăng — giám đốc chi nhánh Giang Đô của ngân hàng Giang Nam?"),
    ("hỏi đại cô họ một nhà đã đến đâu", "hỏi cả nhà đại cô đã đến đâu"),
]

for old, new in REPL:
    n = t.count(old)
    if n:
        t = t.replace(old, new)
    print(f"{n} x {old[:45]}")

# Xoa dong chu loi o dau file (da sua xong)
head = "<!-- chuong 0050 | LOI: xưng 'con' sai: ...anh rể ở lại đi, con... -->\n\n"
if t.startswith(head):
    t = t[len(head):]
    print("1 x bo dong chu loi")

p.write_text(t, encoding="utf-8", newline="\n")
print("OK", len(t))
