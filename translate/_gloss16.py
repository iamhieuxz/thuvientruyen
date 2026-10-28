# -*- coding: utf-8 -*-
import io, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
G = "glossary_can_bao_chan_long.txt"
shutil.copyfile(G, "_bak_glossary_cycl16.txt")
lines = io.open(G, encoding="utf-8").read().split("\n")

def has_key(k):
    return any("=" in l and not l.startswith(("#", " ")) and l.split("=")[0].strip() == k for l in lines)

def add(header, entries):
    new = ["%s = %s" % (z, v) for z, v in entries if not has_key(z)]
    if not new:
        print("  (da co)", header[:18]); return
    for i, l in enumerate(lines):
        if l.startswith(header):
            lines[i:i] = new + [""]; print("  +%d truoc %s" % (len(new), header[:22])); return

add("## ══════ THẾ LỰC - TỔ CHỨC", [
    ("向飞羽", 'Hướng Phi Vũ (lão tổ Chân Vũ Tông, tự nhận là khí đồ của Vũ Đang; âm mưu cưới Vân Băng Uyển để dụ Diệp Sở, bị đánh gãy ngực rồi giết ở ch.239 — source có chỗ chép lẫn 向飞语/向飞宇)'),
    ("葛老", 'Cát lão (cao thủ Huyền Môn của Hộ Long Vệ, nhận ra tử khí trong cổ mộ là long khí — ch.234–251)'),
    ("吞吞", 'Thôn Thôn (bé gái linh hồn tóc đỏ theo Diệp Sở từ ch.205, ăn đan dược, biết Ly Hồn Thuật và Ngự Thú Thuật; được đặt tên ở ch.232 — ch.204–255)'),
    ("陈长青", 'Trần Trường Thanh (truyền nhân phái Mao Sơn, đi cùng Thanh Vi chân nhân — ch.237–251)'),
    ("云万仇", 'Vân Vạn Cừu (tức Giang Nam Hầu, "vua không ngai" tỉnh Giang Nam, kẻ đứng sau nhà họ Tư Mã; có con trai út đã có hôn ước với Gia Cát Triết Nhã — ch.254)'),
    ("阿兵", 'A Binh (con cự mãng lam nhạt có sừng canh Vạn Niên Băng Liên dưới hàn đàm, bị Diệp Sở khắc Ngự Thú ấn thu phục, thu nhỏ thành vòng tay — ch.244–252)'),
    ("青莲", 'Thanh Liên (đệ nhất luyện dược sư của Nga Mi, được nhắc tới — ch.254)'),
])

add("## ══════ ĐỊA DANH", [
    ("万年寒潭", 'Vạn Niên Hàn Đàm (hàn đàm dưới sông ngầm trong cổ mộ, có yêu thú hóa hình canh giữ — ch.238–244)'),
    ("玄门", 'Huyền Môn (giới tu hành huyền thuật/đạo thuật, nơi Cát lão xuất thân — ch.237)'),
])

add("## ══════ ĐỊA VỊ - CHỨC VỤ", [
    ("三魂草", 'Tam Hồn Thảo (linh dược chữa tổn thương hồn phách, mọc ở vùng lõi cổ mộ; Diệp Sở cho Hồng Vân để cứu Khương Quân Dao — ch.236–250)'),
    ("三魂锁", 'Tam Hồn Tỏa (ba sợi xích phong ấn hồn phách bị cấy vào cơ thể Diệp Sở từ nhỏ; xích đồng đang nứt dưới sức thiêu của Chu Tước Thần Hỏa — ch.255)'),
    ("朱雀神火", 'Chu Tước Thần Hỏa (dị hỏa cấp cao trong đỉnh đồng đỏ dưới núi lửa; Diệp Sở luyện hóa được bản mệnh tử hỏa — ch.227–232)'),
    ("本命子火", 'bản mệnh tử hỏa (tia lửa con do Chu Tước Thần Hỏa tặng Diệp Sở — ch.229)'),
    ("离魂术", 'Ly Hồn Thuật (thuật tách hồn khỏi xác, Thôn Thôn truyền cho Diệp Sở — ch.228)'),
    ("驭兽术", 'Ngự Thú Thuật (thuật điều khiển yêu thú, bản tàn thiên do Thôn Thôn truyền — ch.246–247)'),
    ("血煞丹", 'Huyết Sát Đan (đan Diệp Sở uống dưới hàn đàm, để lại di chứng — ch.246–247)'),
    ("大生机丹", 'Đại Sinh Cơ Đan (đan cứu mạng cực mạnh, Diệp Sở luyện ba viên, dùng cứu Khương Quân Dao — ch.234–235)'),
    ("万年冰莲", 'Vạn Niên Băng Liên (linh liên mọc dưới đáy hàn đàm, Thôn Thôn lấy được — ch.245–246)'),
    ("斩妖剑", 'Trảm Yêu Kiếm (bảo kiếm của Thanh Vi chân nhân dùng đối phó yêu thú hàn đàm — ch.242–245)'),
    ("四赤阳阵", 'Tứ Xích Dương Trận (đại trận Diệp Sở bày để chắn hàn khí — ch.243)'),
    ("茅山八卦盘", 'Bát Quái Bàn Mao Sơn (bảo vật trấn phái Mao Sơn, dùng giải phóng long khí trong cổ mộ — ch.251)'),
    ("天罡地煞", 'Thiên Cương Địa Sát (danh hiệu nhóm cao thủ theo nhà họ Long vào cổ mộ — ch.238)'),
])

BLOCK = """### Đã xảy ra — chương 226–255:
- Ch.226: Ngày quyết chiến tại núi Thần Cư, Diệp Sở vắng mặt nên bị chửi là rùa rụt cổ; Chân Vũ Tông nhân đó gả Vân Băng Uyển cho lão tổ Hướng Phi Vũ để dụ hắn, nhà họ Long đồng ý. Khương Quân Dao phẫn nộ, Hồng Vân từ chối cứu; trên đảo, Thôn Thôn tỉnh dậy từ tiểu đỉnh và dẫn đường tìm lửa.
- Ch.227: Thôn Thôn dẫn Diệp Sở xuống đáy hồ, vào núi lửa chết có đài tròn khắc trận vân; thấy biển dung nham và đỉnh đồng đỏ khắc hình Chu Tước, ăn một tia lửa khiến đỉnh thức tỉnh.
- Ch.228: Thôn Thôn truyền Ly Hồn Thuật, nuốt hồn Diệp Sở đưa xuống. Hỏa điểu Chu Tước toan giết hắn nhưng dừng lại khi cảm nhận khí tức Thanh Long; hắn đoán là do Long Hồn Hư Không Đỉnh.
- Ch.229: Hỏa điểu thấy Long Hồn Hư Không Đỉnh đã vỡ thì kinh hãi; trận bạo phát, thanh quang từ đồ án Thanh Long cứu mạng hai người. Nó nói có hai đóa dị hỏa quá mạnh, bắt Hồng Liên chân nhân đi và tặng hắn bản mệnh tử hỏa của Chu Tước Thần Hỏa. Lên bờ, Tà Tăng và người Vũ Đang vây Vương Tam Thông đòi giao cơ duyên.
- Ch.230: Diệp Sở giết một kẻ bằng khí nhận, một quyền trọng thương Vũ Tôn tam phẩm gầy gò. Tà Tăng bỏ chạy, dọa Ám Bảng sẽ trả thù; Bạch Hạc chân nhân của Vũ Đang giữ trung lập. Hắn chia tay Vương Tam Thông, về Giang Đô.
- Ch.231: Khương Quân Dao hôn mê vì bị Chân Vũ Tông đánh trọng thương, sống nhờ Tiểu Sinh Cơ Đan của Nga Mi; tạng phủ, kinh mạch và hồn phách đều tổn hại. Bạch Hiểu Hiểu đã vào cổ mộ; Hộ Long Vệ tổn thất nặng, quan chức phong tỏa và mộ cao thủ làm pháo hôi.
- Ch.232: Tại trang viên hồ Quảng Lăng, Diệp Sở đặt tên cô bé là Thôn Thôn; nó đền tội bằng một tàn thiên đan điển. Hắn luyện hóa Chu Tước Thần Hỏa và suýt chết cháy.
- Ch.233: Cận kề cái chết, hắn thấy ký ức: Chân Long Cốt bị moi khỏi ngực khi còn là trẻ sơ sinh theo lệnh một quý nữ tóc đỏ, mẹ ruột Lâm Huyển Huyển nhìn lạnh lùng, rồi mắt hắn cũng bị móc. Hắn thề điều tra, ý chí bùng lên chống lại hỏa.
- Ch.234: Luyện hóa xong, hắn đột phá ngũ phẩm đỉnh phong Vũ Tôn, luyện được ba viên Đại Sinh Cơ Đan. Cát lão rút khỏi vùng lõi cổ mộ, định mời viện binh; Chu Huyên và Lâm Tự Tại lo ngại.
- Ch.235: Chu Thanh Thanh khinh miệt, bị hắn một chưởng đánh ngã. Hắn cho Khương Quân Dao uống Đại Sinh Cơ Đan và châm cứu, sinh mệnh ổn định; Hồng Vân kinh ngạc, hồn vẫn tổn thương.
- Ch.236: Thiếu Tam Hồn Thảo, Hồng Vân chỉ nó ở vùng lõi cổ mộ và kể vụ đính hôn, việc Khương Quân Dao cứu Vân Băng Uyển bị phục kích, việc bà thua lão tổ Chân Vũ Tông. Hắn nói "giết người", hóa trang thành Diệp đại sư; Oán Long Khí đánh nhau với Chu Tước Thần Hỏa trong khí hải.
- Ch.237: Cát lão nhận ra tử khí là long khí; Chu Huyên nghi có "vị kia" giấu mặt, quân chiến khu Đông bộ được điều tới. Mao Sơn cử chưởng giáo Thanh Vi chân nhân và Trần Trường Thanh. Hắn tới nhà họ Long; Long Tuyết Phi mỉa mai.
- Ch.238: Hắn bóp mặt Long Tuyết Phi đến hủy dung, giết hai đệ tử Chân Vũ Tông canh Vân Băng Uyển, trị thương giúp nàng đột phá đại tông sư. Dùng thẻ bách hộ của Hộ Long Vệ vào cổ mộ, xuống sông ngầm tới hàn đàm. Tay sai của Hầu gia báo tin; Thiên Cương Địa Sát đã theo nhà họ Long vào.
- Ch.239: Hắn thiêu Tiêu Nam thành tro bằng một tia lửa. Hướng Phi Vũ — khai là khí đồ Vũ Đang — bị đánh gãy ngực rồi bị giết; Tiêu Mộc quỳ lạy vô ích, cả Chân Vũ Tông bị diệt sạch. Hắn quay sang nhà họ Long: "Đến lượt các người."
- Ch.240: Hắn đòi Long Trấn Sơn quỳ, xin lỗi và đoạn tuyệt cha con với Vân Băng Uyển; Long Trấn Sơn nói nàng không phải máu mủ mình. Nữ Vũ Tôn trung niên của nhà họ Long ra tay, bị Ưng Trảo Công cào rách cổ; Tào Ưng và Lâm Hào của Ưng Trảo Môn chứng kiến.
- Ch.241: Long Đỉnh Thiên nhượng bộ; Long Trấn Sơn quỳ lạy, lớn tiếng xin lỗi, cắt tình cha con. Vạn Niên Hàn Đàm bị trận phong ấn, phá trận sẽ giải phóng hàn khí. Tào Ưng xin bái sư, được nhận làm "ưng khuyển".
- Ch.242: Tào Ưng và Lâm Hào quy phục; hắn trêu Tư Đồ Tĩnh chuyện "động tác mới". Thanh Vi chân nhân cảnh báo đáy hàn đàm có yêu thú hóa hình, đã mang Trảm Yêu Kiếm.
- Ch.243: Hắn bày Tứ Xích Dương Trận chắn hàn khí, Thanh Vi và Cát lão phá phong ấn. Lâm Hào mưu trả thù "phế vật Diệp Sở" mà không biết đó là Diệp đại sư. Bão hàn khí bùng nổ, đại trận trụ vững.
- Ch.244: Bạch Lang Hội qua hàn đàm an toàn; thuyền nhà họ Long bị cự mãng lam nhạt có sừng đánh chìm, cả thuyền chết. Thanh Vi chân nhân bị quật văng đóng băng; Cát lão cứu. Hắn trì hoãn để thử thực lực mới; Tư Đồ Tĩnh hô hắn ra tay.
- Ch.245: Hắn cầm Trảm Yêu Kiếm đấu mãng xà, dùng Chu Tước Thần Hỏa và Long Quyền. Bám đuôi rắn bị kéo xuống đáy; mọi người tưởng cả hai chết nên vượt đàm. Dưới đáy có thung lũng với Vạn Niên Băng Liên.
- Ch.246: Hắn uống Huyết Sát Đan; Thôn Thôn cướp Băng Liên vào tiểu đỉnh. Rắn nuốt tiểu đỉnh, bị hắn đốt dạ dày nên nhả ra và cầu xin; Thôn Thôn truyền Ngự Thú Thuật bản tàn thiên, cố ý làm hắn đau.
- Ch.247: Hắn khắc Ngự Thú ấn bằng máu lên đầu rắn; rắn chống lại rồi bị mua chuộc bằng đan dược, thần phục và thu nhỏ thành vòng tay. Nó khai từng bị một đạo sĩ đánh trọng thương. Hắn nổi lên với di chứng Huyết Sát Đan; Long Đỉnh Thiên đòi xem bảo vật.
- Ch.248: Đám đông tham lam ép giao thiên tài địa bảo; chỉ Hộ Long Vệ, nhà họ Vương và nhóm Y Thánh Kim Lăng không ra tay. Tào Ưng bước ra che chắn, được nhận làm tùy tùng; Diệp Sở thả cự mãng.
- Ch.249: Rắn đóng băng rồi quật nát Long Đỉnh Thiên — gia chủ nhà họ Long chết. Hắn bắt mọi người đi trước làm pháo hôi, nhà họ Long dẫn đầu. Chủ mộ thất có Tam Hồn Thảo, ngọc giản hình kiếm, cổ tịch bìa lam, quan tài đen phun tử khí và tám Thanh Đồng Giáp Sĩ; cạm bẫy giết nhiều người.
- Ch.250: Hắn đặt tên rắn là A Binh; nó lấy ba bảo vật. Hắn cho Hồng Vân Tam Hồn Thảo nhưng từ chối ngọc giản hình kiếm; Tư Đồ Tĩnh thèm cổ tịch bìa lam. Ba Vũ Tôn không phá nổi chiến trận giáp sĩ; một giáp sĩ bỗng nổ tung.
- Ch.251: Chiến trận bị phá, quan tài mở: long khí hóa tử long bị Ngũ Trảo Kim Long trên long bào cương thi khóa chặt. Người trung niên dùng Bát Quái Bàn Mao Sơn giải phóng nó; Thanh Vi kinh hãi vì đó là bảo vật trấn phái Mao Sơn. Long khí lao vào Diệp Sở, phá nát kinh mạch; Vân Băng Uyển buột miệng gọi "A Sở".
- Ch.252: Nhà họ Long khai đã tặng Giao Long Huyết để biến người luyện nó thành vật chứa long khí, nhưng hắn chưa luyện. A Binh đóng băng giết cặp Vũ Tôn bát phẩm của nhà họ Long; Thanh Vi nhặt Bát Quái Bàn. Ra cổ mộ, nó đóng băng toán lính chặn đường (không giết).
- Ch.253: Tại nhà họ Vân, Chu Thanh Thanh và Hồng Vân thấy mặt thật: Diệp đại sư chính là Diệp Sở — chồng cũ của Khương Quân Dao. Thôn Thôn đưa Tử Kim Táo và dược liệu; Vân Băng Uyển mớm thuốc bằng miệng. Oán Long Khí đánh nhau với long khí.
- Ch.254: Giang Nam Hầu Vân Vạn Cừu rút quân chờ thời; một mỹ phụ áo trắng giống Vân Băng Uyển muốn dùng Diệp đại sư làm quân cờ báo thù. Vũ Đang sai Bạch Hạc chân nhân đi Giang Đô, Nga Mi cử Thanh Liên. Oán Long Khí nuốt trọn long khí rồi đánh Chu Tước Thần Hỏa; khí hải vỡ, thân thể bốc cháy.
- Ch.255: Hồn hắn chìm trong bóng tối, nghe Vân Băng Uyển khóc nên gắng sống. Ký ức mới: lão đạo âm trầm cùng Lâm Huyển Huyển và quý nữ tóc đỏ cấy Tam Hồn Tỏa vào đứa bé bốn-năm tuổi. Hắn thấy trên mình cũng có ba sợi xích, xích đồng đang nứt; biết chỉ người thi thuật hoặc Niết Bàn mới giải được, và nghi có kẻ giật dây mọi chuyện.
"""

first = BLOCK.strip().split("\n")[0]
if not any(l.strip() == first for l in lines):
    for i, l in enumerate(lines):
        if l.startswith("### Ràng buộc cho các chương sau:"):
            lines[i:i] = BLOCK.strip("\n").split("\n") + ["", ""]
            print("  + block 226-255"); break

io.open(G, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("XONG block 226-255. tong so dong:", len(lines))