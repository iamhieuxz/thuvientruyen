# Luật dự án (bắt buộc)

## 0. Bảo vệ dữ liệu đã dịch (TUYỆT ĐỐI — ưu tiên cao nhất)
- **KHÔNG BAO GIỜ xoá file chương đã dịch** trong `data/<out>/` của bất kỳ truyện nào: file `NNNN_*.md` đã có, draft `_NNNN_nhap.md`/`_cat.md` đang chờ xử lý tay, và `book.json`.
- **CẤM dùng `dich.py --reset`** trên dữ liệu thật: `--reset` xoá TOÀN BỘ thư mục output và reset state về rỗng — đây là nguyên nhân mất 993 chương Cao Nhị Phân Khoa ngày 2026-11-03. Muốn dịch lại MỘT chương: xoá đúng file/chapter đó bằng tay (hoặc đưa nó vào `failed`), KHÔNG dùng `--reset`.
- Lệnh xoá/move/rm bất kỳ file trong `data/` nào phải dừng và xin người dùng xác nhận trước, kể cả khi kịch bản tự động có vẻ hợp lý.
- State `done` phải khớp thực tế trên đĩa: reset state chỉ khi file tương ứng đã mất thật sự, và phải backup state + output trước.
- Trước khi chạy script hàng loạt chạm vào `data/`, đọc hàm xóa/ghi của script đó trước (grep `unlink|rmtree|shutil|remove`), xác nhận không có tác dụng phụ hủy dữ liệu.

## 1. Model và sub-agent
- Sub-agent (Agent/Explore/Plan/general-purpose…) **chỉ được dùng model cùng cấp với câu hỏi** và với model chính đang cấu hình trong `F:\taitruyen\.env`.
- **Không được tự khởi động, tự đổi hoặc gọi model khác** (kể cả qua endpoint/API khác, kể cả khi model hiện tại lỗi 404/402) nếu chưa được người dùng cho phép rõ ràng.
- Mọi thay đổi `OPENAI_MODEL`, `OPENAI_BASE_URL`, `OPENAI_API_KEY` phải do người dùng quyết định; ghi thay đổi vào `.env` bằng Python + UTF-8 và backup trước.
- Sub-agent mặc định chỉ đọc và báo cáo; không tự sửa dữ liệu dịch, không tự chạy pipeline trừ khi được giao cụ thể.
- Không bao giờ in API key ra output; model ID và base URL thì được phép.
- Hết hạn mức/số dư thật sự (HTTP 402 insufficient_quota, HET HAN MUC không kèm 429): **dừng runner ngay**, không chunk-translate tiếp, ghi log và chờ người dùng xử lý.
- Riêng 429 rate limit tạm thời (15 request/phút): nghỉ 20–60 giây rồi tiếp, không dừng hẳn — nếu dừng mỗi 429 thì không thể dịch liên tục.

## 2. Sách nói (TTS)
- Không dùng ký hiệu phân cách giữa các khối: `---`, `***`, `===`, `~~~`, `###`, `•`, `※`, `◆`, `◇`, `■`, `▲`, `●`, gạch ngang dài.
- Ngăn đoạn bằng **một dòng trống**; không chèn dòng ký hiệu, không dấu chấm lửng trang trí.
- `check.py` coi dòng ký hiệu là lỗi `[E]`; `_qdcd_auto.sanitize_seps()` tự xoá sau promote; `_clean_seps.py` dọn toàn bộ corpus.
- **Đoạn phải ngắn: tối đa ~180 ký tự/đoạn** (khoảng 2 câu). Máy đọc render trọn một đoạn thành một file âm thanh, đoạn dài khiến người nghe phải chờ lâu và mất mạch truyện. `dich.split_long_paras()` tự cắt đoạn dài tại ranh giới câu (và tại dấu phẩy nếu một câu quá dài), tự đóng/mở lại ngoặc kép khi cắt giữa lời thoại, giữ cân bằng `“ ”` toàn bài. Hàm này chạy trong `dich.py` (lúc dịch) và `promote.py` (lúc nâng nháp); đổi ngưỡng bằng biến môi trường `MAX_PARA`.
- Áp lại cho chương đã dịch: gọi `dich.split_long_paras()` trên phần thân, giữ nguyên dòng `<!-- ... -->` và `# Chương N`, rồi chạy `check.py` lại (kiểm ngoặc kép lệch).

## 3. Nhịp dịch và QA
- Khi hết hạn mức: **dừng dịch ngay**, sau đó tự động rà soát lại từ chương 1 (`check.py --from 1 --to <max>` + `check.py --names`) để đồng bộ tên nhân vật, ngữ cảnh và glossary trước khi dịch tiếp.
- Quan Đạo (`quan_dao_chi_dien`): 20 chương/lô, sau mỗi lô rà tên nhân vật + ngữ cảnh + lỗi câu từ, cập nhật glossary.
- Khai Cục Đình Chức (`khai_cuc_dinh_chuc`): 20 chương/lô (1191→3221 chương đang ra). Bắt buộc theo `glossary_khai_cuc_dinh_chuc.txt`, mục “QUY TẮC RIÊNG CỦA BỘ TRUYỆN”: (a) phân biệt 书记 = bí thư / 秘书 = thư ký / 秘书长 = Tổng thư ký; (b) mỗi lô chạy `check.py --book khai_cuc_dinh_chuc --names` để bắt biến thể tên (hiện đã biết: 邹晨 = 顾晨 → “Cố Thần”; 市医院 = 灵云市中心医院); (c) tên bị nguồn che giữ `……`, không bịa tên; (d) mốc thời gian 2008 và các chi tiết chứng khoán (ST Diêm Hồ) giữ đúng, không hiện đại hoá; (e) giữ thuật ngữ quan trường Hán Việt, không paraphrase.
- Không dịch lại chương đã đúng nội dung; sửa draft `_NNNN_nhap.md`/`_cat.md` rồi `promote.py`.
- Lên kệ: `promote.py` xong là truyện tự hiện trên reader (port 8080, cache 3 giây). Runner phải gọi `update_shelf()` (tương đương `python translate/shelf.py --book <key>`) sau mỗi lô để cập nhật `data/<out>/book.json`; không xóa/viết tay các trường `title/author/desc/genre/cover` đã chọn.

## 4. Giao diện & SEO: bộ kỹ năng ưu tiên
Bộ skill đã cài sẵn trong `C:\Users\iamhieuxz\.agents\skills` (mọi phiên đều thấy, không copy vào repo). Gọi bằng tool `skill` **trước khi** sửa giao diện, đừng sửa chay rồi mới trang trí.

| Việc | Skill phải gọi |
|---|---|
| Sửa `reader/static/*` (kệ, trang truyện, trang đọc) | `anti-ui-slop` (chống UI công nghiệp) + `design-taste-frontend` (kỷ luật thẩm mỹ) |
| Thiết kế mới (bìa, trang mới, khối mới) | thêm `frontend-design`, `ui-ux-pro-max` (màu + typography) |
| Chọn hướng thẩm mỹ | **một** trong hai: `minimalist-ui` (sạch, editorial) hoặc `high-end-visual-design` (sang, agency) — không trộn |
| Dọn UI đang rối | `baseline-ui` (spacing, thứ bậc, chữ) |
| Vi tương tác | `design-spells` — tối đa 1–2 chỗ, không rải khắp trang |
| Trước khi báo "xong" | `tastegate` (chạy trên trình duyệt thật) + `accessibility-compliance-accessibility-audit` nếu có đổi màu/tương tác |
| `shelf.html`, `book.html`, metadata | `seo-technical` |

- **Sandbox chặn Chrome** (named pipe / mojo): `tastegate` và `scripts\gate.py` phải chạy ngoài sandbox hoặc xin quyền. Chưa chạy được thì **không được nói "đã kiểm tra bằng trình duyệt"** — nói rõ là mới kiểm bằng ảnh dựng/HTTP.
- `ui-skills` chỉ là **stub** (132 từ, trỏ về repo, không có ràng buộc nào) — đừng trông vào nó.
- Kiểm tra bộ này còn đủ và còn thật: `python .tools\audit_skills.py` (11/12 dùng được; `ui-skills` là stub).
- Bìa sách: nguồn duy nhất là `python reader\cover_design.py` (ảnh gốc ở `reader/static/img/art/`); không sửa tay `cover-*.jpg`, không nhờ model sinh ảnh có chữ tiếng Việt.
- Font giao diện/bìa: Sitka + Candara (Windows, đủ dấu) — không đổi sang font không có bộ dấu Việt.
