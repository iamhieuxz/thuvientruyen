# truyendich_scraper — cào bản gốc tiếng Trung

Bộ công cụ tải truyện gốc và tách thành từng chương `.txt` để đưa sang `translate/`. Gồm hai lớp:

- **Package async** `truyendich_scraper/` — crawler tổng quát cho `truyendich.space` (Next.js SSR): rate-limit, retry/backoff, cache JSON, resume, xuất JSON/TXT.
- **Script độc lập** cho từng nguồn thật đang dùng, mỗi nguồn có cấu trúc HTML/TXT khác nhau.

> Repo **không chứa truyện đã cào** (`baojian/`, `canh-bao-.../`, `data/`, log). Chạy lại script để tạo; xem [.gitignore](../.gitignore).

## Nguồn dữ liệu

| Nguồn | Script | Dùng cho | Đặc điểm phải xử lý |
|---|---|---|---|
| `kcshu.com` | `baojian_scraper.py` | Bảo Giám (book 122187) | mục lục 13 trang; mỗi chương bị cắt thành 2–4 phần `{id}_2.html`…; hay trả 502 |
| `ixdzs8.com` | `ixdzs_txt_scraper.py` | 3 bộ: 555557, 610184, 560049 | tải ZIP → TXT GB18030; tiêu đề chương đôi khi dính cuối đoạn trước; có bộ thiếu hẳn tiêu đề/11 chương rỗng |
| `fxnzw` (飞翔鸟中文) | `fxnzw_fill_gaps.py` | Vá 11 chương thiếu của bộ 610184 | đọc `_meta.json`, tải chương thiếu, cập nhật `_toc.txt`/`_thieu-noi-dung.txt` |
| `truyendich.space` | `python -m truyendich_scraper.cli` | Danh mục truyện + bản dịch tham khảo | HTML SSR, parser dựa `section.prose-novel` |

## Cài đặt

```powershell
cd F:\taitruyen\truyendich_scraper
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Cấu hình là tuỳ chọn. Package đọc `.env` ở **gốc repo** (`F:\taitruyen\.env`), không phải trong thư mục này. Mặc định trong code đã dùng được; nếu cần đổi, **thêm** các biến từ `.env.example` vào file `.env` gốc (đừng ghi đè — file đó còn chứa key dịch).

Các biến chính: `MAX_CONCURRENT` (3), `REQUESTS_PER_SECOND` (0.7), `MAX_RETRIES`, `RAW_DIR`, `NOVEL_DIR`, `SAVE_RAW_HTML`, `ENABLE_UA_ROTATION`. Đừng tăng tốc độ: mặc định đã lịch sự với server.

## Cách dùng

### 1. Package async — `truyendich.space`

Chạy từ thư mục `truyendich_scraper/`:

```powershell
# Cào một truyện theo slug, khoảng chương
python -m truyendich_scraper.cli scrape --slug bao-giam --start 1 --end 1184

# Thử một chương, in JSON ra màn hình
python -m truyendich_scraper.cli test --slug bao-giam --chapter 1

# Lấy danh mục truyện từ sitemap
python -m truyendich_scraper.cli novels --from-sitemap --output data/novels/index.json

# Gộp cache thành một file
python -m truyendich_scraper.cli export --slug bao-giam --format json
```

Cache (resume được, chạy lại không tải lại):

```
data/novels/<slug>/meta.json
data/novels/<slug>/chapters/00001.json
```

Đường dẫn gốc lấy từ `NOVEL_DIR`/`RAW_DIR` trong `.env`; mặc định tính từ gốc repo. `--force` bỏ qua cache.

### 2. Bảo Giám — `kcshu.com`

```powershell
python baojian_scraper.py                 # tải đủ 1282 chương
python baojian_scraper.py --limit 10      # thử 10 chương
python baojian_scraper.py --start 500     # tải tiếp từ chương 500
python baojian_scraper.py --epub          # đóng EPUB sau khi tải
```

Kết quả: `baojian/NNNN_<tiêu đề Hán>.txt` (UTF-8, không BOM). Script bỏ qua file đã có nên chạy lại an toàn.

### 3. Ba bộ từ `ixdzs8.com`

```powershell
python ixdzs_txt_scraper.py                # tải + tách cả 3 bộ trong BOOKS
python ixdzs_txt_scraper.py --only 555557  # chỉ một bộ
python ixdzs_txt_scraper.py --force        # tải lại TXT dù đã có
python ixdzs_txt_scraper.py --epub         # kèm EPUB
```

Mỗi bộ ra một thư mục slug tương ứng, gồm:

```
0001_<tiêu đề>.txt
_meta.json            metadata + ghi chú lỗi nguồn
_toc.txt              mục lục
_thieu-noi-dung.txt   chương chỉ có tiêu đề (nếu có)
```

`ixdzs_txt_scraper.py` tìm mọi `第N章` theo thứ tự tăng dần thay vì split theo dòng, nên xử lý được tiêu đề bị dính vào cuối đoạn trước.

### 4. Vá chương thiếu

```powershell
python fxnzw_fill_gaps.py
```

Chỉ dành cho bộ 610184 (Cảnh Báo! Chân Long Xuất Ngục) sau khi đã chạy `ixdzs_txt_scraper.py`. Script cập nhật lại `_meta.json` và xoá các số chương khỏi `_thieu-noi-dung.txt` khi đã vá xong.

### 5. Dò cấu trúc trang

`probe_meta.py`, `probe_pw.py` là công cụ một lần để xem HTML/meta của nguồn khi viết parser. Không cần cho pipeline.

## Test

```powershell
python tests\test_chapter_parser.py
```

Smoke test parser chạy offline. Có thể chạy bằng `pytest` nếu đã cài.

## Cấu trúc package

```
truyendich_scraper/
├─ config.py            # Settings từ .env
├─ http_client.py       # aiohttp session, rate-limit, retry/backoff
├─ models.py            # Chapter, Novel (pydantic)
├─ parsers/             # chapter.py, novel.py
├─ scrapers/            # chapter_scraper.py, novel_scraper.py, novel_list_scraper.py
├─ storage/             # cache.py (JSON), exporter.py (JSON/TXT)
├─ logging_config.py
└─ cli.py               # scrape | test | novels | export
```

## Khi nguồn đổi cấu trúc

Parser là phần dễ gãy nhất. Sửa theo thứ tự:

1. `parsers/chapter.py` — selector lấy nội dung (`section.prose-novel`), tiêu đề, tác giả.
2. `parsers/novel.py` — mục lục và tổng số chương.
3. Chạy `cli test --slug ... --chapter 1` để xem JSON trước khi cào hàng loạt.
4. Với script độc lập: sửa regex/selector tương ứng trong file `.py`, thử `--limit 2`.

## Lưu ý

- Chỉ dùng cho mục đích cá nhân/học tập; tôn trọng `robots.txt` và giới hạn tốc độ của từng site.
- Truyện gốc có bản quyền — không đăng lại nội dung, không commit thư mục chương vào repo.
- Các site hay đổi tên miền/HTML; nếu 404 hàng loạt, kiểm tra lại URL gốc trước khi sửa parser.
