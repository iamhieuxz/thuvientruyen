# Thư viện truyện

Pipeline cá nhân để **cào truyện gốc tiếng Trung → dịch sang tiếng Việt có kiểm soát thuật ngữ → đọc và nghe trên web**.

Repo này chỉ chứa **mã nguồn, cấu hình và từ điển glossary**. Toàn bộ truyện đã cào, bản dịch, file EPUB, audio cache và log **không được đưa lên** (xem mục [Những gì không có trong repo](#những-gì-không-có-trong-repo)).

## Kiến trúc

```
truyendich_scraper/            translate/                    reader/
 bản gốc .txt tiếng Trung  →   LLM + glossary_*.txt      →   web reader + TTS
 (kcshu, ixdzs8, truyendich)   → data/<truyện>_vi/*.md        localhost:8080 / điện thoại
                               → output/*.epub
```

| Phần | Vai trò | README |
|---|---|---|
| [`truyendich_scraper/`](truyendich_scraper/README.md) | Cào bản gốc từ `kcshu.com`, `ixdzs8.com`, `truyendich.space`; vá chương thiếu từ `fxnzw` | [đọc](truyendich_scraper/README.md) |
| [`translate/`](translate/README.md) | Dịch từng chương bằng Gemini/OpenAI-compatible, ép thuật ngữ theo glossary, QA, đóng gói EPUB | [đọc](translate/README.md) |
| [`reader/`](reader/README.md) | Web đọc truyện mobile-first, kệ nhiều bộ, TTS offline (VieNeu) hoặc online (edge-tts) | [đọc](reader/README.md) |
| [`data/`](data/README.md) | Nơi nhận bản dịch `.md`; repo chỉ giữ README mô tả định dạng | [đọc](data/README.md) |

Luồng đầy đủ cho một bộ truyện:

1. **Cào** chương gốc vào `truyendich_scraper/<slug>/NNNN_<tiêu đề Hán>.txt`.
2. **Dịch** bằng `translate/dich.py` → `data/<truyện>_vi/NNNN_*.md`; chương lỗi để lại bản nháp `_NNNN_*.md`.
3. **QA** bằng `translate/check.py`, sửa tay bản nháp rồi `promote.py`, cập nhật glossary.
4. **Đóng gói** `translate/epub.py` (hoặc `pipeline.py` = check → epub → checkepub) ra `output/`.
5. **Đọc/nghe** bằng `reader/server.py`; reader tự quét mọi thư mục con trong `data/`.

## Yêu cầu

- **Python 3.10+**. `translate/` và `reader/` chỉ dùng thư viện chuẩn; `truyendich_scraper/` cần `pip install -r requirements.txt`; TTS offline cần một venv riêng.
- **Windows** là môi trường gốc. `translate/dich.py`, `check.py`, `pipeline.py`, `epub.py` đang hardcode gốc `F:\taitruyen` — clone đúng vào `F:\taitruyen`, hoặc sửa hằng `ROOT`/`--src` trong các file đó. `reader/` và scraper dùng đường dẫn tương đối, chạy ở đâu cũng được.
- Không cần Node, không cần database. Trạng thái nằm trong file JSON cạnh code.

## Cài đặt nhanh

```powershell
git clone https://github.com/iamhieuxz/thuvientruyen.git F:\taitruyen
cd F:\taitruyen

# Key dịch: sao chép mẫu rồi điền
copy .env.example .env

# Riêng scraper (package async + bs4)
cd truyendich_scraper
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Chạy thử

```powershell
# 1) Cào 10 chương đầu (ví dụ nguồn Bảo Giám từ kcshu)
cd F:\taitruyen\truyendich_scraper
python baojian_scraper.py --limit 10

# 2) Dịch thử 5 chương
cd F:\taitruyen\translate
python dich.py --book baojian --from 1 --to 10 --limit 5
python check.py --book baojian --from 1 --to 5

# 3) Đọc trên máy
cd F:\taitruyen
python reader\server.py            # http://localhost:8080
```

Chi tiết tham số, định dạng glossary, quy trình QA và cách thêm truyện mới nằm trong README từng phần.

## Truyện đang cấu hình

Khai báo trong `BOOKS` của [`translate/dich.py`](translate/dich.py). Thêm bộ mới = thêm một khối `BOOKS` + một mục `FORBID` (danh sách Hán không được sót), không phải sửa chỗ khác.

| Khóa `--book` | Tên | Thư mục nguồn | Thư mục bản dịch |
|---|---|---|---|
| `baojian` | Bảo Giám | `truyendich_scraper/baojian/` | `data/baojian_vi/` |
| `can_bao_chan_long` | Cảnh Báo! Chân Long Xuất Ngục | `truyendich_scraper/canh-bao-chan-long-xuat-nguc/` | `data/can_bao_chan_long_vi/` |
| `nhi_huu_thien_nhan` | Ngươi Có Thiên Nhãn… | `truyendich_scraper/nhi-huu-thien-nhan-bat-khu-do-thach-huu-tai-loan-khan/` | `data/nhi_huu_thien_nhan_vi/` |
| `nien_dai_58` | Niên Đại: Ở Năm 58 Có Một Thửa Ruộng | `truyendich_scraper/nien-dai-nga-tai-58-huu-khoi-dien/` | `data/nien_dai_58_vi/` |

Bộ `baojian` có `chapter_map.json` vì số file nguồn không trùng số chương truyện (file ghi chú, chương bị tách). Ba bộ còn lại đánh số trực tiếp.

## Cấu trúc repo

```
.
├─ .env.example                 mẫu key API (file .env thật bị gitignore)
├─ .cursor/rules/               quy ước làm việc với AI trong repo
├─ truyendich_scraper/
│  ├─ truyendich_scraper/       package async: config, http_client, parsers, scrapers, storage, cli
│  ├─ tests/                    smoke test parser (không cần mạng)
│  ├─ baojian_scraper.py        cào kcshu.com (Bảo Giám)
│  ├─ ixdzs_txt_scraper.py      tải TXT + tách chương từ ixdzs8.com
│  ├─ fxnzw_fill_gaps.py        vá chương thiếu từ fxnzw
│  └─ probe_meta.py, probe_pw.py   dò cấu trúc trang
├─ translate/
│  ├─ dich.py                   dịch + tự kiểm + state + nhiều backend
│  ├─ check.py                  QA 9 nhóm lỗi
│  ├─ promote.py                nhập bản nháp sửa tay thành chương chính thức
│  ├─ epub.py, checkepub.py     đóng gói và kiểm EPUB 3
│  ├─ pipeline.py               check → epub → checkepub
│  ├─ analyze*.py, _*.py        script phân tích/sửa một lần trong quá trình QA
│  ├─ glossary*.md|txt          từ điển từng truyện (nguồn chuẩn duy nhất)
│  └─ chapter_map.json          ánh xạ file nguồn → số chương (Bảo Giám)
├─ reader/
│  ├─ server.py                 HTTP server + API + ghép TTS + cache
│  ├─ tts_worker.py             worker VieNeu-TTS (venv riêng)
│  ├─ static/                   shelf + reader + font offline
│  ├─ start.bat, tunnel.bat     chạy nhanh trên Windows / Cloudflare quick tunnel
│  └─ TTS-REVIEW.md             đo đạc và các lỗi TTS đã sửa
└─ data/README.md               định dạng chương mà reader đọc
```

## Những gì không có trong repo

| Bị loại | Lý do | Tạo lại bằng |
|---|---|---|
| `.env`, `.env.bak_*` | chứa API key | `copy .env.example .env` rồi điền |
| `data/<truyện>_vi/`, `output/` | bản dịch/EPUB, dung lượng lớn, nội dung có bản quyền | chạy `dich.py` + `epub.py` |
| `truyendich_scraper/<slug>/`, `.../data/` | bản gốc tiếng Trung đã cào | chạy scraper tương ứng |
| `reader/cache/` | MP3 TTS (hàng trăm MB) | tự sinh khi nghe |
| `reader/*.log`, `logs/` | log vận hành | tự sinh |
| `translate/state*.json`, `notes*.txt`, `titles_*.json` | tiến độ và kết quả tự sinh | `dich.py` tạo lại |
| `.venv/`, `__pycache__/` | môi trường cục bộ | tạo venv mới |

## Ghi chú

- **Repo công khai**: không commit `.env` hay bất kỳ key nào. `.gitignore` đã chặn `.env*` (trừ `.env.example`).
- **Bản quyền**: truyện gốc và bản dịch chỉ dùng cho mục đích cá nhân/học tập; repo không phân phối nội dung truyện.
- **Truy cập từ xa**: `reader/tunnel.bat` mở Cloudflare quick tunnel tới cổng 8080. Tunnel **không có xác thực** — ai có URL đều đọc được và có thể đốt CPU khi gọi TTS. Chỉ bật khi cần.
- **TTS**: mặc định dùng edge-tts (cần mạng). VieNeu-TTS chạy offline trong `reader/.venv`, lần đầu tải model ~600 MB–1 GB. Xem [reader/README.md](reader/README.md).
