# reader — web đọc truyện + nghe TTS

HTTP server nhỏ (chỉ thư viện chuẩn) phục vụ thư viện truyện đã dịch trong `data/`, giao diện mobile-first, lưu tiến độ đọc, và đọc thành tiếng bằng hai engine:

- **VieNeu-TTS** — offline, chạy trong venv riêng, chất lượng tốt hơn; lần đầu tải model ~600 MB–1 GB.
- **edge-tts** — online (giọng Microsoft), nhẹ, dùng khi chưa cài VieNeu hoặc cần giọng khác.

## Chạy

```powershell
cd F:\taitruyen
python reader\server.py                 # http://localhost:8080
python reader\server.py --port 8888     # khi 8080 đã có tiến trình khác
python reader\server.py --no-vieneu     # chỉ dùng edge-tts
```

Hoặc nhấp `reader\start.bat` (tự `cd` về gốc repo). Server bind `0.0.0.0`, in kèm địa chỉ LAN để mở trên điện thoại cùng WiFi. Nếu cổng đang có reader khác, script báo và không mở trùng.

Yêu cầu dữ liệu: mỗi bộ truyện là một thư mục con trong `data/` chứa file `NNNN_*.md` — định dạng ở [data/README.md](../data/README.md). Reader tự quét lại khi thư mục thay đổi, không cần khởi động lại.

## Cài TTS

edge-tts (tuỳ chọn, cần mạng) — cài vào **đúng Python đang chạy server**:

```powershell
pip install edge-tts
```

VieNeu (offline) — venv riêng, server tự nhận nếu thấy `reader\.venv\Scripts\python.exe`:

```powershell
cd F:\taitruyen
python -m venv reader\.venv
reader\.venv\Scripts\pip install vieneu
```

- Lần chạy đầu, worker tải model từ HuggingFace; xem tiến trình ở `reader\vieneu.log`.
- `/api/voices` trả trạng thái `ready` / `loading` / `error`; giao diện hiện cảnh báo tương ứng.
- Thiếu VieNeu thì reader vẫn chạy với edge-tts; `vieneu_state = missing`.
- Cache âm thanh nằm ở `reader/cache/` (sha1 của `engine|voice|text`), tự dọn còn 1.500 file theo LRU.

## Tính năng giao diện

- **Kệ sách** (`/`): hero truyện đang đọc, dải “đang đọc dở”, sổ chương mới toàn tủ, lọc theo thể loại, lưới bìa có tiến độ.
- **Trang truyện** (`/sach/<book>`): bìa + tựa gốc, bảng thông tin (tác giả, số chương, cập nhật, trạng thái, thể loại, bản dịch), tiến độ dịch so với bản gốc, giới thiệu đầy đủ, mục lục **200 chương/trang** có tìm/sort/lọc chưa đọc, chỗ đang đọc.
- **Trang đọc** (`/sach/<book>/chuong/<n>`): mục lục, tìm chương, đánh dấu đã đọc, tiến độ từng chương lưu `localStorage`.
- 4 theme (giấy, cũ, đêm, mực), chỉnh cỡ chữ/giãn dòng/căn lề, chế độ tự cuộn.
- TTS: chọn engine + giọng, tốc độ 0.85–1.35× (giữ cao độ), tự sang đoạn/chương, resume đúng đoạn và giây, `mediaSession` (khoá màn hình), `wakeLock` khi đang nghe, prefetch 3 đoạn.
- Audio một thẻ `<audio>` duy nhất, server hỗ trợ `Range` nên tua trong đoạn hoạt động thật.
- JSON nén gzip + `ETag`/`304`; `scan()` dùng lại kết quả parse theo `(mtime, size)` và chỉ công bố index sau khi quét xong (không trả mục lục rỗng khi hai request song song).

Chi tiết đo đạc, lỗi đã sửa và các điểm còn lại: [TTS-REVIEW.md](TTS-REVIEW.md).

## Bìa sách

Bảy bộ có bảy bìa riêng, dựng bằng `reader/cover_design.py` (Pillow, không cần mạng):

- **Ảnh gốc chưa chữ** nằm ở `static/img/art/<key>.jpg` — sửa/thay ảnh ở đây rồi chạy lại script, phần chữ được vẽ đè lên.
- **Bìa hoàn chỉnh** ghi ra `static/img/cover-*.jpg` (900 × 1350, JPEG q90); `covers.js` trỏ thẳng vào các file này nên không phải sửa JS.
- Mỗi bộ một bố cục: `classic` (Bảo Giám), `poster` (Chân Long), `modern` (Khai Cục), `relic` (Thiên Nhãn), `band` (Niên đại), `quiet` (Quan Đạo — bìa sáng, chữ đậm), `novel` (Phân Ban — chữ hoa/thường xen kẽ, số năm in mờ).
- Dùng chung một "ngữ pháp" in: nhãn `TRUYỆN DỊCH` + số thứ tự, gáy sách bên trái, viền chỉ mảnh, hạt phim, tên gốc tiếng Trung chạy dọc.
- Chữ vẽ bằng Sitka (serif) + Candara (sans) của Windows — **có đủ dấu tiếng Việt**, không bị lỗi font như khi nhờ model sinh ảnh có chữ.
- Thêm bộ mới: bỏ ảnh gốc vào `art/<key>.jpg`, thêm một mục trong bảng `BOOKS`, thêm một dòng vào `COVER_ART` trong `covers.js`, chạy `python reader\cover_design.py --only <key>`.

```powershell
python reader\cover_design.py                 # vẽ lại cả 7 bìa
python reader\cover_design.py --only quan_dao # một bộ
```

Sửa tiêu đề, tác giả, màu nhấn, thể loại: bảng `BOOKS` ở cuối `cover_design.py`.

## HTTP API

| Endpoint | Việc |
|---|---|
| `GET /` | kệ sách (`shelf.html`) |
| `GET /sach/<book>` | trang truyện: thông tin, tiến độ dịch, mục lục (`book.html`) |
| `GET /sach/<book>/chuong/<n>` | trang đọc chương |
| `GET /api/books` | danh sách bộ truyện + số chương, số chữ, tiến độ dịch |
| `GET /api/book?book=` | metadata một bộ + số liệu quét từ thư mục + tiến độ dịch |
| `GET /api/latest?limit=` | các chương vừa cập nhật trên toàn tủ |
| `GET /api/cover?book=` | ảnh bìa nếu có |
| `GET /api/chapters?book=` | mục lục nhẹ (số, tên, số ký tự, phút đọc) |
| `GET /api/chapter/<n>?book=` | nội dung chương đã parse thành block |
| `GET /api/hint?book=&n=` | chương trước/sau gợi ý |
| `GET /api/voices` | giọng edge-tts + trạng thái VieNeu |
| `GET /api/tts?engine=&voice=&text=` | trả audio (mp3/wav), tối đa 3.000 ký tự; hỗ trợ `Range` |
| `GET /api/reload?book=` | quét lại thư mục ngay |
| `GET /api/ping` | health check (`{"app":"baogiam-reader"}`) |

`book` mặc định là `baojian_vi` (`DEFAULT_BOOK` trong `server.py`); giọng mặc định `Ngọc Huyền`.

## Cấu trúc

```
reader/
├─ server.py        HTTP server, scan/parse chương, API, cache, điều phối worker
├─ tts_worker.py    worker VieNeu (chạy bằng reader\.venv\Scripts\python.exe)
├─ cover_design.py  dựng 6 bìa sách (Pillow) từ ảnh gốc trong static/img/art/
├─ static/
│  ├─ shelf.html    kệ sách
│  ├─ book.html     trang thông tin một bộ truyện
│  ├─ index.html    trang đọc chương
│  ├─ shelf.js, book.js, app.js, store.js, covers.js
│  ├─ library.css   khung chung (thanh thương hiệu, nhãn, nút, chân trang)
│  ├─ shelf.css, book.css, style.css, fonts.css, fonts/ (woff2 offline)
│  ├─ img/          cover-*.jpg (bìa thành phẩm) + art/ (ảnh gốc chưa chữ)
├─ start.bat        chạy server
├─ tunnel.bat       mở Cloudflare quick tunnel tới :8080
├─ cache/           MP3/WAV tự sinh (gitignore)
└─ TTS-REVIEW.md    đo đạc hiệu năng + nhật ký sửa lỗi
```

## Truy cập từ xa

`tunnel.bat` giả định `cloudflared.exe` nằm ở `C:\Program Files (x86)\cloudflared\` và mở quick tunnel:

```
cloudflared tunnel --url http://localhost:8080
```

URL đổi mỗi lần chạy và **không có xác thực**: ai có URL đều đọc được truyện và gọi TTS (đốt CPU). Chỉ dùng tạm khi ra ngoài, tắt cửa sổ là mất URL. Tunnel cần máy không ngủ.

## Giới hạn đã biết

- Hardcode đường dẫn venv `reader/.venv/Scripts/python.exe` (Windows).
- Chuyển đoạn vẫn có khoảng lặng ~50–150 ms (đổi `src` của một thẻ audio); muốn gapless tuyệt đối phải dùng `AudioContext`, đánh đổi mất background playback trên iOS.
- Chưa streaming từ VieNeu (`infer_stream`): đoạn rất dài (trên 2.000 ký tự) phải chờ sinh xong mới phát.
- Tunnel công khai không auth — xem cảnh báo trên.
