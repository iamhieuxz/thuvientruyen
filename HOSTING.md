# Đưa thư viện truyện lên online — so sánh hosting và phương án triển khai

*Khảo sát ngày 28/10/2026. Giá là giá niêm yết tham khảo, phần lớn chưa gồm VAT và có thể thay đổi theo khuyến mãi.*

## 1. Chốt nhanh

- **Muốn giữ nguyên code, có TTS, chạy 24/7:** thuê **VPS Việt Nam 2–4 GB RAM**. Phương án gọn nhất là **Vietnix VPS SSD 2** (2 vCPU / 4 GB / 40 GB, khoảng **250.000đ/tháng**) hoặc **AZDIGI Pro VPS Standard 2** (2 GB / 20 GB, khoảng **179.000đ/tháng** khi trả 12 tháng). Không cần sửa code; cập nhật truyện bằng `rsync`.
- **Chỉ cần đọc chữ, không cần nghe TTS:** **Cloudflare Pages** miễn phí, băng thông không giới hạn, nhưng phải viết thêm bước export tĩnh và lớp API tĩnh (khoảng nửa ngày công).
- **Muốn 0đ mà vẫn giữ nguyên app + VieNeu:** dùng **Cloudflare Tunnel tên miền riêng + Cloudflare Access** trỏ về PC ở nhà. URL cố định, có đăng nhập, nhưng PC phải bật.
- **0đ và không muốn quản lý PC:** **Oracle Cloud Always Free** (2 OCPU / 12 GB ARM) chạy được, nhưng có thể bị thu hồi nếu idle và không có SLA — chỉ nên dùng để thử.
- **Không nên:** shared hosting (không chạy Python đúng cách), Render free (ngủ sau 15 phút, ổ đĩa tạm), quick tunnel công khai lâu dài (URL đổi, không auth, dễ bị gọi TTS đốt CPU).

## 2. Dự án này thực sự cần gì?

Số liệu đo từ chính repo:

| Thành phần | Dung lượng / đặc điểm |
|---|---|
| Bản dịch | 1.661 chương, khoảng **25 MB** markdown (4 bộ) |
| Giao diện | khoảng **464 KB** static |
| Backend | Python 3.10+, chỉ thư viện chuẩn, không database, không Node |
| TTS | VieNeu model khoảng **600 MB–1 GB**, cache audio hiện **499 MB**; edge-tts chỉ cần mạng |
| Cập nhật | thả file `NNNN_*.md` vào `data/<truyện>_vi/`; reader tự quét lại sau 3 giây |
| Cần deploy | chỉ `reader/` + `data/`; **không** cần `translate/`, scraper, `.env` |

Kết luận: phần **đọc chữ cực nhẹ**, gần như hosting nào cũng chạy. Chi phí và cấu hình thực sự bị định đoạt bởi **TTS**: có cần nghe online không, dùng edge-tts hay VieNeu, và bao nhiêu người cùng nghe.

## 3. Ba cách đưa lên online

### A. VPS chạy nguyên app — khuyến nghị nếu muốn ít sửa code

Cài Ubuntu, copy `reader/` + `data/`, chạy `python reader/server.py` bằng systemd, đặt Caddy/Nginx phía trước làm HTTPS. Thêm `edge-tts` bằng pip; nếu muốn VieNeu thì tạo venv riêng và sửa một dòng đường dẫn venv cho Linux.

- **Ưu:** giữ nguyên API, TTS, cache, tự quét chương; cập nhật bằng `rsync`; toàn quyền kiểm soát.
- **Nhược:** phải tự quản trị Linux, backup, bảo mật.
- **Công sức:** khoảng 1–2 giờ nếu quen Linux; 3–4 giờ nếu chưa quen.
- **Phù hợp:** đọc + nghe, truy cập từ điện thoại mọi nơi, cập nhật truyện thường xuyên.

### B. Static export + Cloudflare Pages — rẻ nhất nếu chỉ đọc chữ

Hiện app gọi các API `/api/books`, `/api/chapters?book=...`, `/api/chapter/N?book=...`. Có thể viết một script export ra JSON tĩnh và một Pages Function (hoặc đổi frontend sang URL dạng đường dẫn) để phục vụ cùng dữ liệu. `/api/tts` sẽ không hoạt động trên hosting tĩnh.

- **Ưu:** 0đ, CDN toàn cầu, HTTPS, domain riêng, băng thông static không giới hạn; không phải bảo trì server.
- **Nhược:** phải sửa code (export + API tĩnh); mất TTS runtime; mỗi lần thêm truyện phải build/upload lại.
- **Công sức:** khoảng 0,5–1 ngày.
- **Phù hợp:** chỉ đọc chữ, muốn public/private ổn định, không muốn trả tiền hàng tháng.

Giới hạn Cloudflare Pages free: **20.000 file/lần deploy**, **25 MiB/file**, 500 build/tháng; băng thông static không tính phí. Với 1.661 chương hiện tại vẫn còn rất xa giới hạn. Nếu sau này có audio, đừng đưa vào Pages — dùng R2 (10 GB free, egress miễn phí).

### C. Giữ PC ở nhà + Cloudflare Tunnel + Access — 0đ, nhanh nhất

Thay quick tunnel bằng **named tunnel** gắn domain riêng, rồi bật **Cloudflare Access** (free tối đa 50 user) để chỉ email của bạn đăng nhập được. Không mở port, không cần VPS, giữ nguyên VieNeu.

- **Ưu:** 0đ, giữ nguyên mọi thứ, có login, URL không đổi.
- **Nhược:** PC phải bật 24/7; mất mạng nhà là mất site; ổ điện/CPU nhà chịu tải.
- **Công sức:** khoảng 20–30 phút.
- **Phù hợp:** dùng cá nhân, chưa muốn trả tiền, hoặc làm bước đệm trước khi thuê VPS.

### D. PaaS (Railway, Render, Fly.io) — không tối ưu cho bài toán này

Deploy Python dễ, nhưng tính tiền theo RAM/CPU chạy liên tục và ổ đĩa gắn ngoài. Một service 1 GB luôn bật thường đã **$10–20/tháng**, đắt hơn VPS Việt Nam cùng cấu hình; ổ đĩa tạm còn làm mất cache TTS. Chỉ nên chọn nếu bạn muốn "không phải quản trị server" và chấp nhận trả thêm.

## 4. So sánh nhà cung cấp

### VPS Việt Nam

| Nhà cung cấp | Gói tham khảo | Cấu hình | Giá tham khảo | Ghi chú |
|---|---|---|---|---|
| **Vietnix** | VPS SSD Linux 2 | 2 CPU / 4 GB / 40 GB SSD | ~250.000đ/tháng; ~212.000đ khi kỳ hạn dài | 200 Mbps nội địa, 10 Mbps quốc tế outbound, backup tuần, uptime 99,9%, hoàn tiền 30 ngày |
| **Vietnix** | VPS SSD Linux 1 | 2 CPU / 2 GB / 40 GB | ~210.000đ/tháng; ~178.000đ kỳ dài | Đủ cho text + edge-tts; không nên chạy VieNeu |
| **AZDIGI** | Pro VPS Standard 2 | 2 GB / 20 GB SSD | ~179.000đ/tháng (12 tháng); 215.000đ (3 tháng) | 100 Mbps, backup tuần, SLA 99,9%, hoàn tiền 30 ngày |
| **TinoHost** | NVMe VPS | từ 99.000đ/tháng; gói 2 GB thường 150.000–195.000đ | Khuyến mãi 35–45% khá thường xuyên | Cần kiểm tra cấu hình/khuyến mãi tại thời điểm mua |
| **Nhân Hòa** | VPS sinh viên / VPS giá rẻ | từ 86.000đ/tháng | Cấu hình thấp | Phù hợp text + edge-tts; không chạy VieNeu nặng |

**Đọc giá cho đúng:** Vietnix/AZDIGI thường niêm yết giá chưa VAT; giá hiển thị có thể là giá đã giảm theo kỳ hạn 3–36 tháng. Nên chọn kỳ 3–6 tháng trước để thử, đừng vội trả 3 năm.

### Cloudflare và quốc tế

| Nhà cung cấp | Gói | Giá | Vị trí | Phù hợp |
|---|---|---|---|---|
| **Cloudflare Pages** | Static free | **0đ**, băng thông static không giới hạn | Toàn cầu | Chỉ đọc chữ; cần export tĩnh |
| **Cloudflare R2** | Free tier | 10 GB lưu trữ, egress 0đ | Toàn cầu | Chứa audio/backup nếu cần |
| **Cloudflare Access** | Free | 0đ cho tối đa 50 user | Toàn cầu | Khóa site private |
| **Oracle Cloud** | Always Free A1 | **0đ**: 2 OCPU / 12 GB RAM / 200 GB, 10 TB egress | Singapore | Chạy được cả VieNeu; **có thể bị reclaim nếu idle**, không SLA |
| **Vultr** | Regular 2 GB | ~$10/tháng (~258.000đ) | Singapore | Ổn định quốc tế; đắt hơn VPS Việt Nam |
| **Hetzner** | CPX22 (2 vCPU / 4 GB / 80 GB) | khoảng €20/tháng (~575.000đ), chưa gồm IPv4 | Singapore | Hiệu năng tốt nhưng **không còn rẻ** sau các đợt tăng giá 2026; thường hết hàng |

Với người đọc ở Việt Nam, VPS trong nước cho độ trễ tốt hơn rõ rệt và giá rẻ hơn. VPS quốc tế chỉ hợp nếu phần lớn người đọc ở nước ngoài, hoặc bạn cần hạ tầng mạnh hơn.

### Vì sao không chọn vài lựa chọn "nghe rẻ"?

- **Shared hosting:** thường chỉ chạy PHP; Python qua Passenger/CGI dễ lỗi, không hợp app HTTP server riêng.
- **Render free:** service ngủ sau khoảng 15 phút, 512 MB RAM, ổ đĩa tạm — TTS và cache không ổn định.
- **Quick tunnel (hiện tại):** URL đổi mỗi lần chạy, không xác thực; ai có URL đều gọi được `/api/tts` và đốt CPU/disk.
- **Free tier 512 MB:** không đủ cho VieNeu; chỉ chạy được text hoặc edge-tts.

## 5. Chi phí theo phương án

| Phương án | Chi phí/tháng | Chi phí/năm (ước tính) | Công sức | TTS |
|---|---:|---:|---|---|
| PC nhà + Tunnel + Access | 0đ | 0đ + domain | 20–30 phút | VieNeu/edge đầy đủ |
| Cloudflare Pages static | 0đ | 0đ + domain | 0,5–1 ngày | Không có runtime |
| VPS VN 2 GB (edge-tts) | 179.000–210.000đ | 2,1–2,5 triệu | 1–2 giờ | edge/Azure |
| VPS VN 4 GB (VieNeu nhẹ) | 250.000–300.000đ | 3,0–3,6 triệu | 1–2 giờ | VieNeu + edge/Azure |
| Oracle Always Free 12 GB | 0đ | 0đ + domain | 1–2 giờ | VieNeu được, rủi ro reclaim |
| Vultr 2 GB / Hetzner CPX22 | ~258.000đ / ~575.000đ | 3,1 / 6,9 triệu | 1–2 giờ | tùy cấu hình; Hetzner đã tăng giá mạnh |

Chưa gồm **domain** khoảng 250.000–350.000đ/năm cho `.com`; SSL miễn phí (Let's Encrypt hoặc Cloudflare). Nếu chọn VPS Việt Nam, cộng thêm VAT.

## 6. TTS — phần quyết định chi phí thực

| Engine | Chi phí | Chất lượng / rủi ro |
|---|---|---|
| **edge-tts** (đang có) | 0đ | Giọng Microsoft tiếng Việt tốt; là endpoint không chính thức, có thể bị rate limit/chặn IP server |
| **Azure AI Speech** | 500.000 ký tự/tháng miễn phí; sau đó ~$15–16/1 triệu ký tự | Chính thức, cùng giọng neural Microsoft; cần key; 500k ký tự ≈ 150–250 chương nếu nghe trọn |
| **FPT.AI TTS** | 100.000 ký tự miễn phí; 500.000đ/1,5 triệu ký tự | Giọng Việt tự nhiên, nhà cung cấp trong nước; cần key/API |
| **VieNeu-TTS** | 0đ bản quyền; tốn RAM/CPU VPS | 0,3B, chạy ONNX/CPU được, model ~1 GB; 4 GB RAM là mức tối thiểu nên thử, 6 GB thoải mái hơn; chậm hơn PC của bạn |
| **Pre-generate audio + R2** | 0đ trong 10 GB R2 | Chất lượng cố định, không đổi giọng/tốc độ; sinh audio một lần rồi phát tĩnh, egress 0đ |

Nếu chỉ một mình bạn nghe, **Azure 500k ký tự/tháng** hoặc **FPT 100k free** thường đã đủ; edge-tts là phương án 0đ nhưng nên có fallback. Nếu công khai cho nhiều người, TTS miễn phí rất dễ bị lạm dụng — phải có đăng nhập hoặc rate limit.

## 7. Rủi ro cần biết trước khi mua

### Bản quyền và điều khoản

Đây là bản dịch từ truyện gốc nước ngoài, chưa thấy giấy phép phân phối. **Để site công khai, nhà cung cấp nào cũng có thể gỡ/khoá theo khiếu nại bản quyền hoặc điều khoản sử dụng** — kể cả Cloudflare, Oracle hay VPS Việt Nam. Cách an toàn:

- Để **private** (Cloudflare Access hoặc basic auth), chỉ chia sẻ cho người quen.
- Không đưa nội dung truyện vào repo public; deploy trực tiếp hoặc dùng repo private.
- Đặt `robots.txt` chặn index nếu chỉ dùng cá nhân.
- Nếu muốn công khai rộng, chỉ dùng nội dung bạn có quyền phân phối.

### Vận hành

- **TTS endpoint không có auth** hiện tại: ai biết URL cũng gọi được, làm đầy cache/tốn CPU. Phải khóa site hoặc thêm token/rate limit trước khi public.
- **Đường dẫn venv VieNeu hardcode Windows** (`reader/.venv/Scripts/python.exe`). Trên Linux, sửa thành `.venv/bin/python` hoặc chạy worker riêng; nếu chỉ dùng edge-tts thì chạy `--no-vieneu`.
- **Cache audio**: khoảng 1.500 file, vài GB; đừng upload từ Windows lên VPS, để VPS tự sinh.
- **Backup**: dữ liệu truyện chỉ ~25 MB; backup `data/` hằng ngày lên R2/Backblaze hoặc máy nhà. VPS có backup tuần nhưng không thay thế bản backup độc lập.
- **Cloudflare Pages**: 20.000 file/lần deploy; nếu sau này có nhiều bộ/audio, chuyển nội dung lớn sang R2.

## 8. Nếu chọn VPS: checklist triển khai

1. Chọn Ubuntu 24.04, tạo user thường, bật firewall chỉ cho SSH/80/443.
2. Cài Python 3.12 + `python3-venv`, tạo venv, cài `edge-tts` (và `vieneu` nếu dùng).
3. Copy `reader/` và `data/` lên `/opt/truyen/`; **không** copy `.venv`, `cache`, log, `.env`.
4. Chạy thử:
   ```bash
   cd /opt/truyen
   .venv/bin/python reader/server.py --host 127.0.0.1 --port 8080 --no-vieneu
   ```
5. Tạo systemd service để tự chạy lại; dùng Caddy làm reverse proxy và HTTPS.
6. Gắn domain, bật Cloudflare proxy; nếu private, bật Cloudflare Access hoặc basic auth.
7. Kiểm tra `/api/ping`, `/api/books`, một chương bất kỳ, và TTS trên điện thoại.
8. Đặt lịch backup `data/`; ghi lại quy trình cập nhật:
   ```bash
   rsync -avz data/ user@vps:/opt/truyen/data/
   ```
   Reader tự quét lại, không cần restart.

Nếu dùng Cloudflare Tunnel thay VPS, chỉ cần thay bước 5–6 bằng named tunnel + Access; mọi thứ còn lại giữ nguyên.

## 9. Đề xuất cuối

- **Để dùng hằng ngày, có nghe, không muốn nghĩ nhiều:** **AZDIGI Pro VPS Standard 2** (~179k/tháng, 2 GB) nếu chỉ edge-tts; hoặc **Vietnix VPS SSD 2** (~250k/tháng, 4 GB/40 GB) nếu muốn thử VieNeu. Đây là mức giá gần như thấp nhất cho một site luôn bật, cập nhật bằng rsync.
- **Để tiết kiệm tối đa mà vẫn đọc/nghe:** **Cloudflare Tunnel + Access** từ PC nhà; nâng cấp lên VPS khi nào thấy phiền vì PC phải bật.
- **Nếu chỉ đọc chữ:** **Cloudflare Pages** là lựa chọn tốt nhất về chi phí/tốc độ; đổi lại mất TTS và cần một buổi static hóa.
- **Không dùng Oracle làm nơi lưu duy nhất** dù miễn phí 12 GB: instance idle có thể bị thu hồi, và bạn sẽ mất thời gian dựng lại. Hướng dẫn cài đặt chi tiết: [ORACLE-DEPLOY.md](ORACLE-DEPLOY.md).

## Nguồn

- [Vietnix — VPS giá rẻ, bảng giá 2026](https://vietnix.vn/vps-gia-re/)
- [AZDIGI — Pro VPS, bảng giá](https://azdigi.com/pro-vps)
- [TinoHost — NVMe VPS](https://tinohost.com/)
- [Nhân Hòa — VPS giá rẻ cho sinh viên](https://nhanhoa.com/tin-tuc/vps-gia-re-cho-sinh-vien.html)
- [Cloudflare Pages — giới hạn gói Free](https://developers.cloudflare.com/pages/platform/limits/)
- [Cloudflare Pages — sản phẩm, băng thông](https://www.cloudflare.com/products/pages/)
- [Cloudflare Workers — giá và quota free](https://developers.cloudflare.com/workers/platform/pricing/)
- [Cloudflare R2 — giá, egress miễn phí](https://developers.cloudflare.com/r2/pricing/)
- [Cloudflare Zero Trust — free 50 user](https://www.cloudflare.com/plans/zero-trust-services/)
- [Oracle Cloud — Always Free Resources](https://docs.oracle.com/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Azure AI Speech — bảng giá](https://azure.microsoft.com/en-us/pricing/details/speech/)
- [FPT.AI — bảng giá TTS](https://docs.fpt.ai/docs/vi/speech/documentation/tts-pricing/)
- [Vultr — bảng giá](https://www.vultr.com/pricing/)
- [Hetzner — Regular Performance, bảng giá 2026](https://www.hetzner.com/cloud/regular-performance/)
- [Railway — bảng giá](https://railway.com/pricing)
