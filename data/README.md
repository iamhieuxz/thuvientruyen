# data — bản dịch mà reader đọc

Thư mục này là **đầu ra của `translate/`** và **đầu vào của `reader/`**. Nội dung truyện không được đưa lên repo (dung lượng + bản quyền); chỉ file README này được giữ.

## Bố cục

```
data/
├─ baojian_vi/                 mỗi thư mục = một bộ truyện
│  ├─ book.json                tuỳ chọn: metadata + tên ảnh bìa
│  ├─ cover.jpg                tuỳ chọn
│  ├─ 0001_第一章 兄妹.md
│  ├─ 0002_第二章 偷师（上）.md
│  └─ ...
├─ can_bao_chan_long_vi/
├─ nhi_huu_thien_nhan_vi/
└─ nien_dai_58_vi/
```

Tên thư mục chính là `book` id trên URL (`/sach/baojian_vi`). Reader coi **mọi thư mục con** có ít nhất một file `.md` bắt đầu bằng 4 chữ số là một bộ truyện — không cần đăng ký.

## Định dạng một chương

Tên file: `NNNN_<tiêu đề gốc>.md`, `NNNN` là số chương (4 chữ số, tăng dần). Reader lấy số từ 4 ký tự đầu, nên phần sau không bắt buộc.

```markdown
<!-- chuong 0001 | 第一章 兄妹 | dich boi AI + glossary -->

# Chương 1: Huynh muội

“Anh, em nhặt được một tấm phiếu lương thực năm cân!”

Theo một tiếng reo mừng rỡ, bên cạnh một đống rác cao như núi...

(Còn tiếp)
```

Quy ước reader dựa vào:

| Thành phần | Vai trò |
|---|---|
| `<!-- chuong N \| tiêu đề Hán \| ghi chú -->` | tuỳ chọn; lưu tiêu đề gốc để đối chiếu, không hiển thị |
| `# Chương N: Tiêu đề` | tiêu đề hiển thị; thiếu thì reader tự đặt `Chương N` |
| `【...】` trong tiêu đề | được tách thành nhãn (tag) hiển thị riêng |
| Dòng phân cách `---`, `===`, `***`… | hiển thị thành dấu ngắt cảnh |
| `(Còn tiếp)` / `(Hết)` / `(Kết)` | dòng kết chương, hiển thị riêng |
| Các đoạn cách nhau bằng dòng trống | mỗi đoạn thành một block |

## Metadata tuỳ chọn — `book.json`

```json
{
  "title": "Cảnh Báo! Chân Long Xuất Ngục",
  "author": "Hồng Thấu Bán Biên Thiên",
  "desc": "Mô tả ngắn hiển thị trên kệ sách",
  "source": "ixdzs8",
  "cover": "cover.jpg"
}
```

Không có `book.json` thì reader lấy tên thư mục làm tiêu đề (`baojian_vi` → “Baojian Vi”). Ảnh bìa mặc định tìm `cover.jpg`, `cover.jpeg`, `cover.png`, `cover.webp`.

## Ghi chú vận hành

- Reader cache kết quả parse theo `(mtime, size)` và quét lại mỗi 3 giây, nên thêm/sửa chương không cần restart.
- `python translate/shelf.py --book <key>` (hoặc `--all`) tự sinh/cập nhật `book.json` từ `_meta.json` của scraper + số chương đã dịch trong thư mục này; runner `_qdcd_auto.py` tự gọi sau mỗi lô promote nên truyện **lên kệ ngay khi có chương hợp lệ**, không cần thao tác thủ công. Các trường đã viết tay (`title`, `author`, `desc`, `genre`, `cover`) luôn được giữ, chỉ trường tiến độ (`status`, `translated_chapters`, `last_chapter`, `updated_at`) là tự cập nhật.
- Chương thiếu số sẽ không xuất hiện; chương trùng số thì file đứng sau trong danh sách sort có thể ghi đè hiển thị. Đặt tên đúng `NNNN_` để tránh.
- File nháp `_NNNN_nhap.md` / `_NNNN_cat.md` nằm cùng thư mục nhưng reader bỏ qua (tên không bắt đầu bằng số).
- Không commit thư mục truyện: `.gitignore` đã chặn `data/*` trừ `data/README.md`.
