# Báo cáo rà soát Quan Đạo Chi Điện (官道之巅) — 2026-11-01

Phạm vi: toàn bộ 259 chương đã dịch, rà theo **lô 50 chương/lần** (6 lô), đủ 4 mặt: glossary, ngữ cảnh, tên nhân vật, câu từ.
Trạng thái cuối: **E = 0 ở cả 6 lô**, 0 bản nháp tồn, `state.failed = 0`, Hán sót trong thân bài = 0.

## 1. Kết quả theo lô

| Lô | Bài | E | W | Ghi chú |
|---|---|---|---|---|
| 1–50 | 50 | 0 | 8 | |
| 51–100 | 50 | 0 | 11 | 0083 nội dung bịa (xem mục 5) |
| 101–150 | 50 | 0 | 12 | |
| 151–200 | 50 | 0 | 3 | |
| 201–250 | 50 | 0 | 8 | 12 chương mới promote |
| 251–259 | 9 | 0 | 2 | |

Số chương dịch được nâng từ **247 → 259/1191** (12 chương trước nằm ở dạng nháp lỗi, giờ đã hợp thức).

## 2. Lỗi E đã sửa

| Nhóm | Số lượng | Cách sửa |
|---|---|---|
| Bản nháp chưa duyệt (`_NNNN_nhap.md`) | 12 chương: 244–248, 250–253, 257–259 | Sửa tay từng cụm Hán sót trong draft rồi `promote.py`, không dịch lại |
| Hán sót trong draft | 185 cụm ở 12 draft | Dịch sát nguồn (VD `Đồng厅` → “Đồng sảnh trưởng”, `驻省办` → “Văn phòng đại diện huyện tại tỉnh”) |
| Chương mất đuôi mà `check_complete` bỏ sót | 0219 (68/102 đoạn, tỉ lệ ký tự 2.30 vs trung vị 3.21) | Dịch bù 34 đoạn đuôi từ nguồn, chèn trước “(Còn tiếp)” |
| Text phản hồi của model rò vào bài | 86 đoạn ở 28 chương | Xóa (`_strip_leaks.py`), đã kiểm tra từng đoạn trước khi ghi |
| Ngoặc kép rỗng `“”` (di sản của doan can bang ngoac kep) | 97 chỗ ở 9 chương | Xoa cặp rong, trạt lại ngoặc mo; GIU LAI file nao lech can bang |
| Tên riêng lệch chuẩn glossary | 68 chỗ / 8 biến thể | Đồng nhất toàn corpus (xem mục 3) |
| Rác pipeline (`Mã tác vụ: …`, `Đoạn văn cần sửa:` + đoạn trùng) | 3 dòng + 1 đoạn trùng ở 0252, 0224 | Xóa dòng rác; xóa 1 trong 2 đoạn gần trùng (ratio 0.92) |
| Sai người nói | 0245 “Đinh Minh Lễ 摆毅道” → đúng là **Đồng Đức Nghị** | Sửa theo nguồn |
| Sai chức danh | 0246 “trưởng tỉnh trưởng Đồng” → “sảnh trưởng”; 0244 “trưởng tỉnh Công an” → “sảnh trưởng Sở Công an tỉnh” | Sửa theo nguồn + chuẩn chức danh |
| Title chứa Hán | 0258 `Văn phòng驻 tỉnh`, 0259 `Việc khó办` | Sửa titles json → “Văn phòng đại diện tại tỉnh”, “Việc khó lo liệu” |
| Từ vựng dính liền không dấu cách | `tổngTóm`, `VănBách`, `gọiTưởng`, `bàiWeibo`, `làĐới` … | Tách lại dấu cách |
| Đại từ cấm `ngươi` | 0257 | Sửa thành “hắn” |

## 3. Tên nhân vật — đã đồng nhất

Đều đã đối chiếu lại chữ Hán trong nguồn trước khi đổi:

| Biến thể sai (số lần) | Chuẩn | Chữ Hán |
|---|---|---|
| Mục Văn Bách (15) | Từ Văn Bách | 徐文柏 |
| Tân Dũng Quân (11), Tôn Dũng Quân (6) | Đàm Dũng Quân | 谭勇军 |
| Dương Vũ Ninh (8) | Đới Vũ Ninh | 戴宇宁 |
| Vệ Tư Thần (11), Vệ Phương Xuân (3) | Vi Tư Thần / Vi Phương Xuân | 韦思晨 / 韦芳春 |
| Niếp Hạo Quảng (10) | Nhiếp Hạo Quảng | 聂浩广 |
| Lí Gia Bá (6) | Lý Gia Bá | 李家坝 |
| Cố Nhia (15), Nhiêu Nhia (2) | Cố Nhiêu, Nhiêu Nhiêu | 顾娆 / 娆娆 |
| Triệu Phồn Điền (15) | Triệu Phúc Điền | 赵福田 |
| Vương Gia Cán (3) | Uông Gia Cam | 汪家淦 |
| Vương Nguyệt Mỹ (1) | Vương Duyệt Mỹ | 王悦美 |
| Tiểu Nhụ (3) | Tiểu Như | 小茹 |
| Tập đoàn Kaller (11) | Tập đoàn Ca Lặc | 卡勒集团 |

`check.py --names` còn 31 nhóm gần trùng, tất cả là dạng gọi tắt hợp lệ của cùng một tên hoặc cặp hai nhân vật khác nhau (Trần Tiểu Phàm / Trần Tiểu Phi).

Cùng lượt: `ngài/Ngài` → `ông/Ông` (22 chỗ), `ngàn vạn` → `nghìn vạn` (3), `tỉnh sảnh` → `Sở Công an tỉnh` (2) để khớp 24 chỗ còn lại trong corpus.

## 4. Glossary và ngữ cảnh

- Merge **382 mục từ mới** từ `state.new_terms` sau khi kiểm: (a) chữ Hán có thật trong nguồn, (b) không xung đột nghĩa đã gán, (c) không phải từ loãng. 84 mục chỉ xuất hiện 1 lần trong nguồn vẫn được giữ; 1 mục (`港岛廉政公署`) không có trong nguồn → loại.
- Sửa **key sai**: `王逸川` → `王一川` (nguồn: 王逸川 x0, 王一川 x46).
- Sửa **giá trị quá dài** — đây là nguồn gốc của ~20 cảnh báo W: `县委`, `县政府`, `镇党委`, `市纪委`, `精神文明奖` chuyển sang dạng `Hán = thuật ngữ ngắn (chú thích)`, đúng cách `load_glossary` cắt括호.
- Thêm tên còn thiếu: 韦思晨, 苏兴怀, 李天放, 李淑芬, 聂浩广; thêm biến thể nguồn viết lẫn: 蔡秀芝, 郝秀萍, 晨星医疗集团.
- `state.new_terms`: 729 → 24. Glossary: 490 → **726 mục từ**, file 1007 dòng.
- Viết lại `### Đã xảy ra — chương 244–259` và `### Ràng buộc cho các chương sau` (danh sách tên đã đồng nhất + cấm đổi lại, chuẩn chức danh, mạch truyện đang mở, cảnh báo hành vi model free).

**Lưu ý chi phí:** glossary tăng từ ~60KB lên **105KB** và nguyên file này được nhét vào prompt mỗi lần dịch. Nếu muốn gọn, chạy bước tỉa: giữ tên người/tổ chức/chức danh, bỏ các cụm thành ngữ thông dụng model đã dịch đúng.

## 5. Còn tồn đọng — cần bạn quyết

1. **0083 (谢婉淑与谢莹莹) có nội dung bị bịa.** Bài dài 17.5k ký tự trong khi nguồn 2.2k; các cảnh “Cừu A Tường ở thôn Tiền Hà”, “chộp cổ dao”… không tồn tại trong nguồn ch.73–90 (`仇阿祥`, `钱河` xuất hiện 0 lần). Không thể sửa bằng cách xóa cơ học vì phần bịa xen kẽ phần đúng → **cần dịch lại chương này** (tốn hạn mức API, nên tôi không tự chạy).
2. **0257 còn 29 dấu ngoặc kép ASCII.** Số dấu là số lẻ nên một lượt thoại bị thiếu ngoặc đóng; script chuyển đổi đã được giữ lại (không ghi) để tránh làm sai. Cần sửa tay.
3. 44 W còn lại là hint mềm: 采摘节/西山矿业/省厅/微博/信访 (bài dùng biến thể tự nhiên, không sai), xưng “con” với cha mẹ (hợp lệ), 2 bài “gộp đoạn không phải cắt” (0079, 0086), W2 do model gợi ý tên Hán nhưng thực ra là tổ hợp hàm danh (杨县长, 谢谢您…).
4. **Nên chạy cùng bộ rà cho các bộ khác.** Lấy mẫu 70 chương của Bảo Giám cho tỉ lệ ký tự trung vị 3.21 nhưng **min 1.23** — dấu hiệu có chương bị cắt tương tự 0219.

## 6. Thay đổi trong công cụ (đều có thể rollback bằng git)

`translate/check.py`:
- Thêm quan hệ thân thuộc (mẹ/ba/bố/cha/dì/thím/nội/ngoại) vào `HONORIFIC` → hết lỗi giả “Mẹ Cố Nhiêu” thành biến thể tên.
- `run()`: “thiếu đoạn” chỉ còn là **W** khi tỉ lệ ký tự VI/Hán ≥ 2.8 (tiếng Việt gộp thoại), và thêm **E “cắt theo độ dài”** khi tỉ lệ < 2.5 → chính rule này đã bắt được 0219 mà `check_complete` bỏ sót.

Script mới trong `translate/` (không đụng pipeline dịch): `_fix_apply.py` (áp patch TSV, từ chối bảng lệch cột), `_precheck.py` (kiểm điều kiện promote), `_draft_qa.py` (rà tên cho draft), `_gloss_merge.py` (merge có đối chiếu nguồn), `_strip_leaks.py`, `_tail_audit.py`, `_fix_empty_quotes.py`, `_ai_leak_report.py`, `_leak_align.py`, `_why_name.py`, `_align.py`. Log: `_audit_qdcd_*.log`, `_names_final.log`, `_tail_audit.out`, `_leak_all.txt`.

## 7. Backup

- Snapshot toàn bộ trước khi sửa: `_backup_audit/20261101_1806/` (269 file: corpus + glossary/notes/state/titles).
- 78 file `.bak_*` cạnh từng chương đã sửa (`.bak_fix`, `.bak_names`, `.bak_leak`, `.bak_quotes`, `.bak_style`, `.bak_tail`) và `glossary_*.bak_merge`, `titles_*.bak_titles`, `state_*.bak_merge`.
- `data/` và `state*.json` đang bị gitignore nên **không có** rollback bằng git cho nội dung truyện — chỉ dùng các file backup trên.

## 8. Chạy tiếp lô mới (260–309)

```bash
cd F:/taitruyen/translate
python dich.py --book quan_dao_chi_dien --from 260 --to 309   # dich
python check.py --book quan_dao_chi_dien --from 260 --to 309  # E phải = 0
python check.py --book quan_dao_chi_dien --names --from 1 --to 309
python _strip_leaks.py quan_dao_chi_dien 260 309              # kiem tra text model roi
python _tail_audit.py quan_dao_chi_dien 260 309               # kiem tra mat duoi
python _gloss_merge.py --book quan_dao_chi_dien --min 1       # doi chieu nguon roi --write
```
