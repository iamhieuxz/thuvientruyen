import io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = r"F:/taitruyen/data/can_bao_chan_long_vi/_0063_cat.md"
t = io.open(P, encoding="utf-8").read()

lines = t.split("\n")
if lines and lines[0].startswith("<!--"):
    lines = lines[1:]
body = "\n".join(lines).rstrip("\n")

frag = "“Hì hì, Diệp đại sư nói đùa rồi.” Nàng nhạt nhẽo cười, r"
assert frag in body, "fragment not found"
body = body[: body.index(frag)].rstrip("\n")

body = body.replace("Trái tim rừng", "Trái Tim Rừng Xanh")

TAIL = [
    "“Hì hì, Diệp đại sư nói đùa rồi.” Nàng nhạt nhẽo cười, tiện thể chuyển sang chuyện khác, “Diệp đại sư với cô bạn gái nhỏ của mình chơi sang thật đấy, ra tay một cái là mấy trăm triệu.”",
    "Vừa nói, ánh mắt nàng đã rơi lên sợi Trái Tim Rừng Xanh bên cổ Tôn Ngữ Nhu.",
    "Bị người hiểu lầm, khuôn mặt xinh đẹp của Tôn Ngữ Nhu đỏ bừng trong chớp mắt, nhưng hiếm thấy lại không giải thích.",
    "Trong đáy lòng còn dâng lên một tia mừng thầm.",
    "Diệp Sở cười nói: “Có là bao, nếu Gia Cát tiểu thư bằng lòng, tôi cũng có thể chơi sang như vậy.”",
    "Tên nhãi này, còn lên cơn nghiện trêu ghẹo nữa rồi… Gia Cát Triết Nhã thầm trợn mắt: “Diệp đại sư đừng nói đùa, để cô nương nhà người ta ghen lên thì sao.”",
    "Hai người trò chuyện vui vẻ, nhưng lại khiến đám đông xung quanh nhìn đến ngẩn ngơ.",
    "Đặc biệt là những người biết rõ thân phận Gia Cát Triết Nhã.",
    "Thân hình Tiền Hào Sâm run lên không ngớt, sắc mặt đã sớm trắng bệch không còn giọt máu.",
    "Trời ơi, bản thân mình đã gây ra những chuyện gì vậy?",
    "Đầu óc hắn choáng váng, suýt nữa đứng không vững.",
    "Tiền Hâm vội vàng đỡ lấy, thấp giọng hỏi han: “Bố, bố không sao chứ?”",
    "Hai mắt Tiền Hào Sâm đỏ ngầu, “Con nói xem có sao không?”",
    "Giờ phút này hắn chỉ muốn bóp chết cái đồ con hại cha này, rõ ràng bản thân đã nhịn xuống làm cháu nội rồi.",
    "Vậy mà tên đó lại thề thốt đảm bảo, Diệp Sở chẳng qua là một tên ở rể phế vật, không cần phải sợ.",
    "Bây giờ thì hay rồi, người ta quen biết Gia Cát Triết Nhã, quan hệ lại còn rất tốt.",
    "Đắc tội với người ta, hắn liệu có được kết cục tốt đẹp sao.",
    "Tiền Hâm run rẩy, không dám lên tiếng.",
    "Hắn sao có thể nghĩ tới, Diệp Sở một đứa con riêng ở rể, vậy mà quen biết nhân vật lớn như Gia Cát Triết Nhã.",
    "“Diệp đại sư, nói thử nghe xem, chuyện là thế nào?” Gia Cát Triết Nhã trò chuyện vài câu, hỏi sang chính sự.",
    "Diệp Sở không giấu giếm, đem sự tình thuật lại đúng như thực.",
    "Sắc mặt Gia Cát Triết Nhã hơi trầm xuống, đôi mắt lạnh lẽo nhìn Tiền Hào Sâm, giọng thăm thẳm: “Quả không hổ là ủy viên Thương hội Giang Nam chúng ta, bản lĩnh đổi trắng thay đen thật khiến người ta bội phục.”",
]

with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    f.write(body + "\n\n" + "\n\n".join(TAIL) + "\n")

print("paras:", len([l for l in (body + "\n" + "\n\n".join(TAIL)).split("\n") if l.strip()]))
print("CJK left:", [c for c in io.open(P, encoding='utf-8').read() if '\u4e00' <= c <= '\u9fff'][:5])
