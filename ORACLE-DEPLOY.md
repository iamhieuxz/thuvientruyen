# Chạy thư viện truyện trên Oracle Cloud Always Free

*Hướng dẫn theo thực tế repo này, cập nhật 28/10/2026. Giá và hạn mức Always Free có thể thay đổi; luôn kiểm tra lại trang chính thức trước khi làm.*

## 1. Oracle Cloud là gì?

**Oracle Cloud Infrastructure (OCI)** là dịch vụ cloud công cộng của Oracle, cùng loại với AWS, Google Cloud hay Azure. Bạn thuê một **máy ảo (compute instance)** đặt trong datacenter của Oracle, có IP công cộng, ổ đĩa, mạng, rồi tự SSH vào cài phần mềm. Oracle không quản lý application của bạn; họ chỉ quản lý hạ tầng.

**Always Free** là gói miễn phí *trong hạn mức*, không phải bản dùng thử 30 ngày. Nếu bạn ở trong hạn mức và không bật tài nguyên trả tiền, hóa đơn bằng 0. Tuy nhiên:

- Cần **thẻ tín dụng/ghi nợ** để xác minh danh tính (thường giữ $1 tạm thời, không phải phí dịch vụ).
- Phải chọn **home region** khi tạo tài khoản; tài nguyên Always Free phải nằm ở region đó. Với Việt Nam, chọn **Singapore** để độ trễ thấp.
- Oracle có thể **thay đổi hạn mức**; tháng 6/2026 họ đã giảm Ampere A1 từ 4 OCPU/24 GB xuống **2 OCPU/12 GB**. Các bài hướng dẫn cũ vẫn ghi 4/24 — đừng làm theo con số đó.
- Không có SLA hay hỗ trợ như gói trả tiền. Đây là môi trường để học/thử, không phải nơi đặt thứ duy nhất bạn có.

### Bạn nhận được gì trong Always Free?

| Tài nguyên | Hạn mức (10/2026) | Ý nghĩa với dự án này |
|---|---|---|
| Ampere A1 (ARM) | **2 OCPU / 12 GB RAM**, 1 hoặc 2 VM | Quá đủ cho reader; đủ chạy VieNeu |
| Block storage | **200 GB** tổng (boot + volume), 5 bản backup | Chứa code, model ~1 GB, cache vài GB |
| Egress | **10 TB/tháng** | Thừa cho text/audio cá nhân |
| AMD micro | 2 VM nhỏ 1 GB (tuỳ chọn) | Không cần cho dự án này |
| Public IPv4 | Có thể gắn cho instance | Dùng để SSH/truy cập; kiểm tra Billing nếu Oracle đổi chính sách |

**Điểm quan trọng:** đây là máy **ARM64**, không phải x86. Python thuần và edge-tts chạy bình thường; VieNeu cần kiểm tra wheel ARM/ONNX trước khi dựa vào nó.

## 2. Có nên chạy dự án này trên Oracle không?

### Nên chọn nếu

- Bạn muốn **0đ** nhưng vẫn có 12 GB RAM, đủ chạy VieNeu.
- Bạn chấp nhận **tự quản trị Linux**, tự backup, tự dựng lại nếu instance bị thu hồi.
- Bạn thích thử nghiệm, không đặt nặng uptime.
- Bạn chỉ dùng cá nhân/nhóm nhỏ, không cần SLA.

### Không nên chọn nếu

- Bạn muốn "bật lên rồi quên", cần site luôn sống.
- Bạn không muốn săn capacity hoặc xử lý sự cố ARM.
- Đây là nơi lưu **bản duy nhất** của truyện.
- Bạn cần hỗ trợ kỹ thuật khi app lỗi.

### Ba rủi ro lớn nhất

1. **Idle reclamation:** Oracle có thể thu hồi instance Always Free nếu trong 7 ngày: CPU percentile 95 < 20%, network < 20%, và RAM < 20%. Một site đọc truyện cá nhân rất dễ rơi vào trạng thái idle. Đừng tạo tải giả để lách; hãy coi instance là **có thể mất bất cứ lúc nào** và giữ backup.
2. **Out of host capacity:** khi tạo A1, Oracle có thể báo "Out of host capacity". Cách xử lý thực tế là thử lại nhiều lần/khác Availability Domain; không có gì đảm bảo. Có người phải chờ nhiều ngày.
3. **Tài khoản có thể bị đóng:** dùng thẻ không hợp lệ, nhiều tài khoản, hoặc vi phạm điều khoản đều có thể dẫn đến khóa. Đừng coi đây là hạ tầng production.

### So với VPS Việt Nam

| | Oracle Always Free | VPS Việt Nam 2–4 GB |
|---|---|---|
| Chi phí | 0đ | 179.000–250.000đ/tháng |
| RAM | 12 GB | 2–4 GB |
| Độ ổn định | Không SLA, có thể reclaim | SLA 99,9%, backup tuần |
| Công sức | Tự dựng, săn capacity | Tự dựng nhưng ổn định hơn |
| Hỗ trợ | Gần như không | Có hỗ trợ hạ tầng |
| Phù hợp | Thử nghiệm, cá nhân | Dùng hằng ngày |

**Kết luận:** Oracle đáng thử nếu bạn thích tinkering và chấp nhận rủi ro; nếu chỉ muốn đọc truyện ổn định, VPS 179–250k/tháng là lựa chọn hợp lý hơn về thời gian và độ an tâm.

## 3. Chuẩn bị trước khi tạo máy

Bạn cần:

- Tài khoản Oracle Cloud đã xác minh, home region **Singapore**.
- Domain (nếu muốn HTTPS đẹp) và tài khoản Cloudflare (miễn phí).
- Bản `data/` trên máy Windows (khoảng 25 MB) và repo `reader/`.
- SSH key (Oracle bắt buộc khi tạo instance). Trên Windows có thể dùng `ssh-keygen` trong PowerShell.

Nên đặt **budget alert** trong Oracle Billing để biết nếu có tài nguyên phát sinh ngoài ý muốn. Không nâng cấp lên tài khoản trả tiền nếu không cần.

## 4. Tạo instance A1

1. Vào **Compute → Instances → Create instance**.
2. Chọn **Image: Ubuntu 24.04** (hoặc 22.04), shape **VM.Standard.A1.Flex**.
3. Đặt **2 OCPU, 12 GB RAM**, boot volume **50 GB** (tối thiểu 47 GB; 50 GB để thoải mái).
4. Chọn **public subnet**, gán **public IPv4**.
5. Tải/khai báo SSH public key.
6. Nếu gặp "Out of host capacity": thử Availability Domain khác, thử lại sau; kiên nhẫn. Đừng tạo nhiều instance vượt hạn mức.

Sau khi tạo, ghi lại **public IP** và SSH bằng:

```bash
ssh ubuntu@<PUBLIC_IP>
```

Ubuntu image mặc định dùng user `ubuntu`; Oracle Linux dùng `opc`. Đừng nhầm.

### Mở firewall đúng cách

Có **hai lớp** firewall:

1. **Oracle Security List / NSG** (trong console): mở ingress TCP 22 từ IP nhà bạn. Nếu dùng Cloudflare Tunnel, **không cần mở 80/443**. Nếu truy cập trực tiếp, mở 80/443.
2. **Firewall trong Ubuntu** (`ufw` hoặc iptables): mở đúng port tương ứng.

Nếu dùng Tunnel, chỉ cần SSH. Đây là cách ít lỗi và an toàn nhất.

## 5. Cài app

### 5.1. Gói cơ bản

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip rsync git curl ufw
```

Nếu dùng Caddy trực tiếp, cài thêm Caddy; nếu dùng Cloudflare Tunnel thì không cần Caddy.

### 5.2. Copy code và dữ liệu

Cách gọn nhất là clone repo trên server rồi đẩy `data/` từ máy Windows lên:

```bash
sudo mkdir -p /opt/truyen
sudo chown ubuntu:ubuntu /opt/truyen
git clone --depth 1 https://github.com/iamhieuxz/thuvientruyen.git /opt/truyen
```

Trên máy Windows (Git Bash/WSL có `rsync`):

```bash
rsync -avz --exclude '.venv' --exclude 'cache' --exclude '__pycache__' --exclude '*.log' \
  reader data ubuntu@<PUBLIC_IP>:/opt/truyen/
```

Nếu không có `rsync`, dùng WinSCP/`scp` để chép hai thư mục `reader` và `data`. **Không** chép `.env`, `translate/`, scraper, `reader/cache`, `.venv`; chúng không cần cho site và chỉ làm nặng máy.

Kiểm tra quyền:

```bash
sudo chown -R ubuntu:ubuntu /opt/truyen
```

### 5.3. Tạo venv và chạy thử

```bash
cd /opt/truyen
python3 -m venv .venv
.venv/bin/pip install -U pip edge-tts
.venv/bin/python reader/server.py --host 127.0.0.1 --port 8080 --no-vieneu
```

Mở terminal khác, tạo SSH tunnel từ máy bạn:

```bash
ssh -L 8080:127.0.0.1:8080 ubuntu@<PUBLIC_IP>
```

Rồi mở `http://localhost:8080`. Nếu thấy kệ sách và đọc được chương, phần khó nhất đã xong.

> Nếu server báo thiếu dữ liệu: kiểm tra `/opt/truyen/data/<truyện>_vi/NNNN_*.md`. Reader lấy `data/` cạnh thư mục `reader/`.

### 5.4. Chạy nền bằng systemd

Tạo file `/etc/systemd/system/truyen-reader.service`:

```ini
[Unit]
Description=Truyen reader
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/truyen
ExecStart=/opt/truyen/.venv/bin/python /opt/truyen/reader/server.py --host 127.0.0.1 --port 8080 --no-vieneu
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Kích hoạt:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now truyen-reader
sudo systemctl status truyen-reader
journalctl -u truyen-reader -f
```

### 5.5. Nếu muốn dùng VieNeu trên ARM

Trước hết chạy thử riêng worker để biết wheel ARM có hoạt động không:

```bash
sudo apt install -y libsndfile1
cd /opt/truyen
python3 -m venv reader/.venv
reader/.venv/bin/pip install -U pip vieneu
reader/.venv/bin/python reader/tts_worker.py --port 8123
```

Mở terminal khác:

```bash
curl http://127.0.0.1:8123/health
```

Lần đầu sẽ tải model (~600 MB–1 GB), có thể mất vài phút. Khi `ready: true`, thử:

```bash
curl -G 'http://127.0.0.1:8123/say' --data-urlencode 'text=Xin chào, đây là thử nghiệm.' --data-urlencode 'voice=<id>' -o test.wav
```

Nếu lỗi wheel/ONNX trên ARM, dừng ở đây và dùng **edge-tts** hoặc Azure/FPT; đừng cố sửa hàng giờ nếu mục tiêu chỉ là đọc truyện.

`server.py` đang hardcode đường dẫn venv Windows:

```python
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
```

Trên Linux, sửa thành:

```python
VENV_PY = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
```

Sau đó bỏ `--no-vieneu` trong service và restart. Nếu muốn giữ nguyên file gốc, có thể chạy worker thủ công bằng systemd riêng và trỏ server qua `--worker-port`; nhưng cách sửa một dòng là gọn nhất.

**Kỳ vọng hiệu năng:** 2 OCPU ARM + 12 GB đủ chạy, nhưng CPU inference có thể chậm hơn PC Windows của bạn. Nếu nghe nhiều, dùng edge-tts/Azure cho nhanh; giữ VieNeu cho lúc cần chất lượng/offline.

### 5.6. Đưa ra Internet: Cloudflare Tunnel (khuyến nghị)

Cách này không cần mở 80/443, không cần Caddy, không lộ IP Oracle:

```bash
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install -y cloudflared
```

Trong **Cloudflare Zero Trust → Networks → Tunnels**, tạo tunnel, copy token, rồi:

```bash
sudo cloudflared service install <TOKEN>
```

Thêm **Public Hostname**:

- Subdomain: `truyen`
- Domain: domain của bạn
- Service: `http://localhost:8080`

Sau đó bật **Access** cho hostname này (Zero Trust → Access → Applications), policy chỉ cho email của bạn. Đây là lớp khóa site private, tránh người lạ gọi TTS.

Nếu không dùng Tunnel, có thể mở 80/443, cài Caddy và trỏ domain; nhưng phải xử lý SSL gốc (Cloudflare Origin Certificate) và mở firewall. Tunnel ít bước hơn cho người mới.

### 5.7. Kiểm tra sau khi lên

```bash
curl http://127.0.0.1:8080/api/ping
curl http://127.0.0.1:8080/api/books
```

Trên điện thoại: mở domain, đọc một chương, bấm nghe thử. Kiểm tra log nếu TTS lỗi.

## 6. Backup, cập nhật, bảo trì

### Backup

Dữ liệu truyện chỉ ~25 MB; đừng chỉ để trên Oracle:

```bash
tar czf ~/truyen-$(date +%F).tgz -C /opt/truyen data
```

Tải về máy hoặc đẩy lên R2/Backblaze B2. Có thể dùng `rclone`:

```bash
rclone copy ~/truyen-$(date +%F).tgz r2:truyen-backup/
```

Thêm cron/systemd timer chạy hằng ngày. Oracle có backup block volume, nhưng không thay thế bản backup độc lập.

### Cập nhật truyện

Từ Windows:

```bash
rsync -avz data/ ubuntu@<PUBLIC_IP>:/opt/truyen/data/
```

Reader tự quét lại sau 3 giây; không cần restart. Nếu sửa code (`server.py`, static), restart service:

```bash
sudo systemctl restart truyen-reader
```

### Theo dõi

```bash
systemctl status truyen-reader
journalctl -u truyen-reader -n 100 --no-pager
df -h
free -h
```

Nếu dùng Tunnel, xem `systemctl status cloudflared`. Nếu instance bị reclaim, tạo lại từ backup; đây là lý do phải giữ `data/` ở nơi khác.

## 7. Chi phí thực tế

| Khoản | Chi phí |
|---|---|
| Compute A1 2 OCPU/12 GB | 0đ trong Always Free |
| 200 GB block storage | 0đ trong hạn mức |
| 10 TB egress | 0đ trong hạn mức |
| Domain `.com` | ~250.000–350.000đ/năm |
| Cloudflare DNS/Tunnel/Access | 0đ (Access tối đa 50 user) |
| Thời gian dựng + săn capacity | 1–3 giờ, có thể lâu hơn nếu hết capacity |

Nếu vượt hạn mức hoặc bật tài nguyên trả tiền, Oracle sẽ tính phí. Đặt budget alert và kiểm tra Billing thường xuyên.

## 8. Checklist ngắn

- [ ] Tài khoản Oracle đã xác minh, home region Singapore.
- [ ] Budget alert đã bật; không nâng cấp trả tiền.
- [ ] A1.Flex 2 OCPU/12 GB, Ubuntu 24.04, boot 50 GB.
- [ ] Security List chỉ mở SSH từ IP nhà; không mở 8080.
- [ ] Copy `reader/` + `data/`; không copy `.env`/cache/venv.
- [ ] `--no-vieneu` chạy được trước.
- [ ] systemd tự restart; `journalctl` xem log.
- [ ] Cloudflare Tunnel + Access (hoặc Caddy + HTTPS).
- [ ] Backup `data/` ra ngoài Oracle.
- [ ] Thử VieNeu; nếu wheel ARM lỗi, dùng edge-tts/Azure.
- [ ] Chấp nhận khả năng instance bị reclaim.

## 9. Kết luận

Oracle Cloud Always Free là một **máy ARM 12 GB miễn phí** đủ mạnh cho dự án này, đặc biệt nếu muốn chạy VieNeu. Nhưng nó không phải VPS "bật là quên": bạn phải tự dựng, săn capacity, đối mặt idle reclamation và không có SLA. Nếu chỉ muốn đọc truyện ổn định mỗi ngày, VPS Việt Nam 179–250k/tháng vẫn là lựa chọn đáng tiền hơn. Nếu muốn học, thử nghiệm, hoặc tận dụng 12 GB RAM để chạy TTS offline, Oracle là lựa chọn rất đáng thử — với điều kiện giữ backup ở nơi khác.

## Nguồn

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Always Free Resources — hạn mức và idle reclamation](https://docs.oracle.com/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Oracle giảm A1 từ 4 OCPU/24 GB xuống 2 OCPU/12 GB (6/2026)](https://www.infoq.com/news/2026/07/oracle-cloud-free-tier-limits/)
- [Cloudflare Tunnel — tài liệu](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Cloudflare Access — Zero Trust](https://www.cloudflare.com/plans/zero-trust-services/)
- [VieNeu-TTS — model card](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v2)
- [VieNeu-TTS — README PyPI](https://github.com/pnnbao97/VieNeu-TTS/blob/main/README_PYPI.md)
