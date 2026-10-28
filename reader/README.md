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

- Kệ sách nhiều bộ (`/`), mục lục, tìm chương, đánh dấu đã đọc, tiến độ từng chương lưu `localStorage`.
- 4 theme (giấy, cũ, đêm, mực), chỉnh cỡ chữ/giãn dòng/căn lề, chế độ tự cuộn.
- TTS: chọn engine + giọng, tốc độ 0.85–1.35× (giữ cao độ), tự sang đoạn/chương, resume đúng đoạn và giây, `mediaSession` (khoá màn hình), `wakeLock` khi đang nghe, prefetch 3 đoạn.
- Audio một thẻ `<audio>` duy nhất, server hỗ trợ `Range` nên tua trong đoạn hoạt động thật.
- JSON nén gzip + `ETag`/`304`; `scan()` dùng lại kết quả parse theo `(mtime, size)`.

Chi tiết đo đạc, lỗi đã sửa và các điểm còn lại: [TTS-REVIEW.md](TTS-REVIEW.md).

## HTTP API

| Endpoint | Việc |
|---|---|
| `GET /` | kệ sách (`shelf.html`) |
| `GET /sach/<book>/chuong/<n>` | trang đọc; `/sach/<book>` mở chương đầu/cuối đã đọc |
| `GET /api/books` | danh sách bộ truyện + số chương, số từ |
| `GET /api/book?book=` | metadata một bộ (tên, tác giả, bìa) |
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
├─ static/
│  ├─ shelf.html, index.html
│  ├─ shelf.js, app.js, store.js
│  ├─ style.css, fonts.css, fonts/ (woff2 offline)
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
