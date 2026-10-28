# translate — dịch truyện Trung → Việt theo glossary

Bước giữa của pipeline: đọc bản gốc `.txt` trong `truyendich_scraper/<slug>/`, gọi LLM dịch từng chương, ép thuật ngữ theo glossary của từng bộ, tự kiểm tra rồi ghi bản dịch `.md` vào `data/<truyện>_vi/`. Cuối cùng đóng gói EPUB.

Chỉ dùng **thư viện chuẩn Python** (không cần `pip install`).

## Thành phần

| File | Việc |
|---|---|
| `dich.py` | Dịch song song nhiều chương qua Gemini hoặc backend tương thích OpenAI; state/resume; tự kiểm; ghi bản nháp khi lỗi |
| `check.py` | QA bản dịch theo 9 nhóm lỗi E + cảnh báo W; `--names` đồng nhất tên riêng |
| `promote.py` | Sửa tay bản nháp `_NNNN_cat.md` / `_NNNN_nhap.md` rồi nâng thành chương chính thức, không gọi API |
| `epub.py` | Đóng gói Markdown/TXT thành EPUB 3; tách lô, bìa, dịch tiêu đề sót Hán |
| `checkepub.py` | Kiểm cấu trúc EPUB (zip, OPF, nav, XHTML) |
| `pipeline.py` | Chạy `check.py` → `epub.py` → `checkepub.py` (không dịch, không gọi API) |
| `glossary.md`, `glossary_*.txt` | Từ điển thuật ngữ từng bộ — nguồn chuẩn duy nhất |
| `chapter_map.json` | Ánh xạ số file nguồn → số chương truyện (chỉ Bảo Giám) |
| `test_dich.py`, `test_epub.py` | Test bộ lọc/đóng gói, chạy offline |
| `analyze*.py`, `_*.py` | Script phân tích/sửa một lần dùng trong quá trình QA; không thuộc pipeline |

## Cài đặt

Tạo `F:\taitruyen\.env` từ mẫu (file mẫu nằm ở gốc repo):

```powershell
cd F:\taitruyen
copy .env.example .env
```

| Biến | Ý nghĩa |
|---|---|
| `BACKEND` | `gemini` (mặc định) hoặc `openai` |
| `GEMINI_API_KEY` | key Google AI Studio ([lấy tại đây](https://aistudio.google.com/apikey)) |
| `GEMINI_MODEL` / `GEMINI_MODELS` | một model, hoặc danh sách phân tách phẩy để tự chuyển khi hết hạn mức; bỏ trống → `MODEL_FALLBACK` trong `dich.py` |
| `GEMINI_MAX_TOKENS` | mặc định 65536 |
| `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_MAX_TOKENS` | cho backend `openai` (OpenAI, DeepSeek, vpsnodelab…) |
| `BOOK` | truyện mặc định cho `check.py`/`promote.py`/`dich.py` |
| `WORKERS` | số chương dịch song song, mặc định 4 |

> Đường dẫn gốc đang hardcode `F:\taitruyen` trong `dich.py`, `check.py`, `pipeline.py`, `epub.py`, `test_*.py`. Clone đúng vị trí đó, hoặc sửa `ROOT`/`--src`.

## Truyện đã cấu hình

Khai báo trong `BOOKS` của `dich.py` (mỗi bộ trỏ tới thư mục nguồn, thư mục bản dịch, glossary, notes, state, titles riêng):

| `--book` | Nguồn | Bản dịch | Glossary |
|---|---|---|---|
| `baojian` | `truyendich_scraper/baojian/` | `data/baojian_vi/` | `glossary.md` |
| `can_bao_chan_long` | `truyendich_scraper/canh-bao-chan-long-xuat-nguc/` | `data/can_bao_chan_long_vi/` | `glossary_can_bao_chan_long.txt` |
| `nhi_huu_thien_nhan` | `truyendich_scraper/nhi-huu-thien-nhan-.../` | `data/nhi_huu_thien_nhan_vi/` | `glossary_nhi_huu_thien_nhan.txt` |
| `nien_dai_58` | `truyendich_scraper/nien-dai-nga-tai-58-.../` | `data/nien_dai_58_vi/` | `glossary_nien_dai_58.txt` |

`check.py` mặc định `can_bao_chan_long`, `dich.py`/`promote.py` mặc định theo biến `BOOK` (không có thì `baojian`). Luôn truyền `--book` cho chắc.

## Quy trình

### 1. Dịch

```powershell
cd F:\taitruyen\translate

python dich.py --book can_bao_chan_long --status
python dich.py --book can_bao_chan_long --from 1 --to 40 --limit 5   # thử 5 chương
python dich.py --book can_bao_chan_long --from 1 --to 40             # dịch cả lô
python dich.py --book can_bao_chan_long --retry                      # dịch lại chương lỗi
python dich.py --book baojian --reset                                # XOÁ bản dịch cũ rồi làm lại
```

- Chạy lại nhiều lần an toàn: chương đã có file `.md` hoặc nằm trong `state.failed` sẽ bị bỏ qua (trừ `--retry`/`--reset`).
- Gặp `429`: script ghi mốc hết hạn mức vào `models_quota.json`, chuyển model khác, hết model thì dừng và lưu state. Chạy lại sau là tiếp tục.
- Bản dịch bị cắt → `_NNNN_cat.md`; vi phạm kiểm tra → `_NNNN_nhap.md`. Hai loại nháp này bị `check.py` báo E9 cho tới khi xử lý.

### 2. QA

```powershell
python check.py --book can_bao_chan_long --from 1 --to 40
python check.py --book can_bao_chan_long --names          # đồng nhất tên riêng
python check.py --book can_bao_chan_long --quiet          # chỉ E + tổng kết
python check.py --book can_bao_chan_long --json           # máy đọc
```

- `[E]` → phải sửa, exit code 1. `[W]` → rà rồi quyết định.
- Nhóm kiểm: Hán sót; tên lệch dạng chuẩn glossary; dấu kiểm duyệt `*`/`[***]`; đại từ cấm (`ngươi`, `lão tử`, `lão phu`, `ngài`); xưng "con" sai; cấu trúc bài (`# Chương N`, số chương lệch tên file, ngoặc kép lệch, markdown, tiêu đề chép giữa bài); bản dịch bị cắt so với nguồn; rác scraper; file nháp/thiếu/trùng/state.failed; thuật ngữ mới chưa vào glossary.
- Chu kỳ hợp lý: QA mỗi 20–30 chương, cập nhật glossary và mục NGỮ CẢNH cuối file trước khi sang lô tiếp.

### 3. Sửa tay và promote

Mở `_NNNN_cat.md` hoặc `_NNNN_nhap.md`, sửa trực tiếp phần thân (giữ dòng `<!-- ... -->` đầu file), rồi:

```powershell
python promote.py --book can_bao_chan_long
```

Script kiểm lại độ đầy đủ so với nguồn + `validate`, cần có tiêu đề trong `titles_*.json`, rồi ghi file chính thức và xoá nháp. Không tốn request API.

### 4. Đóng gói

```powershell
python epub.py --src ..\data\can_bao_chan_long_vi --title "Cảnh Báo! Chân Long Xuất Ngục" --author "Hồng Thấu Bán Biên Thiên"
python epub.py --src ..\data\baojian_vi --split 50          # mỗi file 50 chương
python epub.py --src ..\data\baojian_vi --check             # chỉ kiểm, không ghi
python checkepub.py                                         # quét output\*.epub
python checkepub.py ..\output\can_bao_chan_long.epub        # hoặc một file cụ thể

# hoặc cả chuỗi kiểm tra + đóng gói (cấu hình Bảo Giám trong pipeline.py)
python pipeline.py --to 50
```

`epub.py` mặc định đọc `data\baojian_vi`, ghi ra `output\`. Các cờ đáng chú ý: `--first/--last`, `--cover`, `--translate-titles --glossary <file>` (thay cụm Hán trong tiêu đề), `--han`/`--zh` (ép bản gốc), `--no-number`, `--outname`.

## Định dạng chương đầu ra

`data/<truyện>_vi/NNNN_<tiêu đề Hán>.md` — 4 số đầu là số chương truyện, reader đọc theo số này:

```markdown
<!-- chuong 0001 | 第一章 兄妹 | dich boi AI + glossary -->

# Chương 1: Huynh muội

“Anh, em nhặt được một tấm phiếu lương thực năm cân!”
...
(Còn tiếp)
```

- Dòng `<!-- ... -->` giữ tiêu đề gốc để đối chiếu.
- `# Chương N: ...` lấy từ `titles_*.json`; thiếu tiêu đề thì chương vẫn được ghi nhưng reader hiển thị tên mặc định.
- Kết thúc bằng `(Còn tiếp)` — `check.py` coi đây là một phần cấu trúc.

## Glossary

Glossary là **kênh duy nhất** truyền quy tắc dịch cho model; `dich.py` đọc toàn bộ file và nhét vào prompt.

- `glossary.md` (Bảo Giám): bảng Markdown `| Hán | Việt | Ghi chú |`, kèm mục quy tắc bất biến.
- `glossary_can_bao_chan_long.txt` và hai bộ còn lại: mỗi dòng `Hán = Hán Việt (ghi chú)`, chia mục theo dòng `## ══════ TÊN MỤC ══════`. Cuối file là mục **NGỮ CẢNH** mô tả tình huống các chương gần nhất.
- Thuật ngữ mới do model đề xuất được gom vào `notes_*.txt`; rà rồi chuyển mục chắc chắn vào glossary. `notes_*.txt`, `state*.json`, `titles_*.json` là file tự sinh, không commit.
- Thêm bộ truyện mới: thêm khối vào `BOOKS` **và** một mục `FORBID` trong `dich.py` (danh sách chuỗi Hán không được sót). Nếu bỏ qua `FORBID`, validator dùng nhầm danh sách của Bảo Giám.

## Thêm truyện mới — checklist

1. Cào nguồn vào `truyendich_scraper/<slug>/NNNN_*.txt` (xem README scraper).
2. Thêm khối `BOOKS[<khóa>]` trong `dich.py` (src, out, glossary, notes, state, titles, chapter_map).
3. Tạo `glossary_<khóa>.txt` (hoặc `.md`) với nhân vật, địa danh, thuật ngữ, quy tắc xưng hô.
4. Thêm `FORBID[<khóa>]` trong `dich.py`.
5. Nếu số file nguồn không trùng số chương: tạo `chapter_map.json` dạng `{"<số file>": {"story": <số chương>, "note": "..."}}`.
6. Dịch thử 3–5 chương, chạy `check.py`, chỉnh glossary, rồi chạy lô lớn.

## Xử lý sự cố

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Dừng với `HET HAN MUC` | 429/quota | chạy lại; kiểm `models_quota.json`, đổi `GEMINI_MODEL` hoặc `BACKEND` |
| Nhiều `BI CAT` | `maxOutputTokens` thấp so với chương dài | tăng `GEMINI_MAX_TOKENS`/`OPENAI_MAX_TOKENS`; sửa nháp rồi `promote.py` |
| `_NNNN_cat.md` rỗng | hết token ngay từ đầu | chạy `--retry --from N --to N` |
| `KIEM THU FAIL` lặp lại | glossary thiếu tên/quy tắc, hoặc model dịch sai | đọc lỗi, bổ sung glossary, `--retry` |
| `check.py` báo lệch số chương | tên file/`# Chương` sai | sửa tay hoặc promote lại |
| EPUB thiếu tiêu đề tiếng Việt | `titles_*.json` chưa có mục | chạy lại `dich.py` cho chương đó hoặc thêm tay rồi promote |
| `checkepub.py` FAIL | zip/OPF/nav hỏng | chạy lại `epub.py`, xem file lỗi; `--check` trước khi ghi |

## Test

```powershell
python test_dich.py
python test_epub.py
```
