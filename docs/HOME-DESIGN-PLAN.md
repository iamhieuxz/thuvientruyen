# Kế hoạch thiết kế trang chủ — truyendochay reader (port 8080)

Ngày: 2026-11-03 · Phong cách tham chiếu: TruyenDich.ai (2 ảnh chụp đính kèm yêu cầu)
Trạng thái: kế hoạch đã duyệt chờ triển khai — 6 task trên board (t-mw0cgyd0 … t-mw0cgydy).

## 1. Định hướng thẩm mỹ: "Midnight Stream"

Giao diện đọc truyện đêm: nền xanh đen chìm, nội dung dày đặc nhưng có thứ bậc,
bìa sách là vật chính, badge màu làm tín hiệu chức năng (không phải trang trí).

- **Tone:** cinematic dark + entertainment dense (chọn 1 hướng chính theo skill
  `high-end-visual-design`; KHÔNG trộn `minimalist-ui`).
- **Differentiation anchor:** hero mosaic bất đối xứng (thẻ lớn + lưới 2×2)
  kẹp giữa icon-sidebar trái và right-sidebar "Đọc tiếp" — nhận ra ngay dù bỏ logo.
- **DFII ước tính:** Impact 4 · Fit 5 · Feasibility 5 · Performance 4 − Risk 2 = **16** (excellent).

## 2. Design tokens (home.css `:root`)

| Nhóm | Giá trị |
|---|---|
| Nền | `--bg: #0B0E1A` (không dùng đen thuần), `--sf: #141827` (surface), `--line: #232A3D` |
| Chữ | `--tx: #EDEEF4`, `--body: #B8BDCE`, `--dim: #7C8298` |
| Accent chính (1 màu) | `--acc: #F2B33D` (vàng cam, độ bão hòa <80%) — dùng cho CTA, số liệu, hover |
| Badge chức năng | AI `#7C4DFF` · HOT `#E5484D` · FULL `#2FA36B` · Vừa xong `#2FA36B` outline |
| Font | **Sitka** (display) + **Candara** (body) — theo AGENTS.md, đủ dấu Việt, không đổi font khác |
| Radius | thẻ 8px · chip 6px · ảnh 8px (góc vuông hơn thẻ cũ, bớt "dashboard") |
| Motion | 150–300ms `cubic-bezier(.16,1,.3,1)`, chỉ `transform/opacity`, tôn trọng `prefers-reduced-motion` |
| Density | VISUAL_DENSITY ≈ 7 (nhiều ảnh, chip số liệu dạng tabular-nums) |

Quy tắc chống slop: không gradient tím neon, không glow quanh nút, không card
đổ bóng mặc định; tách nhóm bằng `border` + khoảng thở; **không bịa số liệu**
(lượt xem không có trong dữ liệu → chỉ hiển thị số chương, % tiến độ, chương mới).

## 3. Cấu trúc trang (home.html mới, giữ shelf.html làm fallback)

```
┌────────┬───────────────────────────────────────────┬───────────┐
│ ICON   │ TOP NAV: logo · THỂ LOẠI▾ · DANH SÁCH▾ ·  │ RIGHT     │
│ RAIL   │ [tìm truyện, tác giả…          ] [Tìm]    │ SIDEBAR   │
│ 64px   ├───────────────────────────────────────────┤ 300px     │
│ Trang  │ HERO MOSAIC: thẻ lớn + lưới 2×2           │ Đọc tiếp  │
│ chủ ✦  │ 🔥 Truyện Hot — rail cuộn ngang + snap    │ (từ      │
│ Lịch sử│ ✨ Dịch bởi AI — rail từ /api/latest      │ localSt.) │
│ Kệ sách│ 📚 Tất cả truyện — filter thể loại + lưới │ Hôm nay   │
│ Thêm + │ footer                                    │ đọc gì?   │
│ Hồ sơ  │                                           │ 🎲 random │
└────────┴───────────────────────────────────────────┴───────────┘
```

- **Icon rail trái:** Trang chủ, Lịch sử, Kệ sách, Thêm, Hồ sơ — SVG inline,
  active state bằng accent, `aria-current`. Mobile: thành bottom nav.
- **Top nav:** dropdown THỂ LOẠI (từ trường `genre` của /api/books), DANH SÁCH
  (Hoàn thành / Đang dịch / Mới cập nhật), search gợi ý qua `/api/hint`.
- **Responsive:** ≥1200 3 cột · 768–1200 ẩn right-sidebar · <768 1 cột + bottom nav.

## 4. Dữ liệu (API sẵn của server.py — không cần backend mới)

| Nguồn | Dùng cho |
|---|---|
| `/api/books` | hero mosaic (featured = tiến độ cao nhất), section Tất cả, random picker |
| `/api/latest` | section "Dịch bởi AI" (badge Vừa xong) |
| `/api/hint` | gợi ý search |
| `store.js` (localStorage) | "Đọc tiếp": truyện + chương gần nhất |
| Badge logic | FULL = status hoàn thành · HOT = đang dịch & cập nhật gần · AI = mặc định |

## 5. Skill pipeline (theo AGENTS.md §4 — đã nạp khi lên kế hoạch)

| Giai đoạn | Skill |
|---|---|
| Lên kế hoạch (xong) | `anti-ui-slop` · `design-taste-frontend` · `frontend-design` · `ui-ux-pro-max` |
| Chọn hướng thẩm mỹ | `high-end-visual-design` (1 hướng duy nhất) |
| Dọn spacing/thứ bậc khi dựng xong | `baseline-ui` |
| Vi tương tác (tối đa 1–2 chỗ: hover thẻ bìa + nút random) | `design-spells` |
| Trước khi báo xong | `tastegate` + `accessibility-compliance-accessibility-audit` (chạy **ngoài sandbox**, sandbox chặn Chrome) |
| Metadata `home.html` | `seo-technical` |

## 6. Tiến độ (6 task trên board)

1. `t-mw0cgyd0` Design system & tokens
2. `t-mw0cgyd7` Khung layout: icon sidebar + top nav + 3 cột
3. `t-mw0cgydc` Hero mosaic + section rails
4. `t-mw0cgydg` Right sidebar: Đọc tiếp + Hôm nay đọc gì
5. `t-mw0cgyds` Responsive + states + a11y
6. `t-mw0cgydy` Gate: tastegate trình duyệt thật + SEO + đổi route `/` → home.html

## 7. Ràng buộc dự án (AGENTS.md)

- Font Sitka + Candara; bìa chỉ từ `reader/cover_design.py`, không sinh ảnh có chữ Việt.
- `ui-skills` là stub — không dùng. Kiểm tra bộ skill: `python .tools\audit_skills.py`.
- Không nói "đã kiểm tra bằng trình duyệt" nếu mới chỉ kiểm bằng ảnh dựng/HTTP.
- Không tự đổi model/API khi thực thi các task.
