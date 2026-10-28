# Review TTS — vì sao nghe trên điện thoại chưa tốt

Đo trên máy thật (2026-10-26), engine VieNeu v3turbo / ONNX CPU, 25 giọng Việt.

## Số đo

| Hạng mục | Kết quả |
|---|---|
| VieNeu RTF | 0.26 – 0.33 (10s audio ≈ 3s máy) |
| VieNeu 1 đoạn 158 ký tự | 2.7s sinh, 9.1s audio |
| VieNeu đoạn 964 ký tự | 13.8s sinh, 49.2s audio |
| VieNeu 48kHz MP3 | 76 kbps, ~75KB/đoạn |
| edge-tts cùng câu | 5.4 – 10.5s, RTF 0.73–1.0, đã crash `NoAudioReceived` |
| Cache hit | 14 ms |
| Đoạn văn | median 170, p90 246, max 2210 ký tự; 60 đoạn/chương ≈ 13 phút |
| `Accept-Ranges` trên `/api/tts` | không có |
| `/api/chapters` | 239 KB JSON, không gzip, gửi lại mỗi lần mở chương |
| Cache đĩa | 86 MB / 1171 file |

Kết luận: engine không phải nút cổ chai. Vấn đề nằm ở tầng phát (`app.js`) và vòng đời audio.

## Đã sửa và đo lại (2026-10-26, server 8099)

| Kiểm chứng | Kết quả |
|---|---|
| `Range: bytes=100-199` trên đoạn 11232 B | `206` + `Content-Range: bytes 100-199/11232`, đúng 100 B |
| `Range: bytes=-10` | `206`, 10 B cuối |
| `Range` ngoài file | `416` |
| Seek giữa đoạn sau đó | `seeked`, `currentTime` đặt đúng |
| `/api/chapters` (239 599 B) | gzip còn **40 535 B** (5.9×) |
| `ETag` + `If-None-Match` | `304` |
| `scan(force)` lần 1 / lần 2 | 0.217s → **0.016s** (13×) |
| Một `<audio>` chạy 2 đoạn liên tiếp | tự sang đoạn 2, không cần user gesture |
| Pause do hệ thống ngắt | tự `play()` lại sau 500 ms |
| `NGHE TIẾP` sau khi dừng | resume đúng đoạn + giây (`i:2, t:2.88`) |
| Hết chương → chương sau | sang chương 2, vẫn phát, label `ĐANG DỰNG…` |
| `mediaSession.metadata` | có tiêu đề chương |

### Sự cố "VieNeu chưa hoạt động" (2026-10-26 16:30)

Không phải engine hỏng. Ba nguyên nhân xếp chồng:

1. **Server 8080 còn chạy code cũ** — tiến trình bật từ 13:15, trước khi sửa. Log còn traceback
   `NoAudioReceived` không có `try` nghĩa là bản `edge_say` chưa được nạp. Đã khởi động lại.
2. **`play()` bị từ chối vì `AbortError` bị hiểu nhầm là autoplay bị chặn** — ô prefetch đổi
   `src` khi lần `play()` trước chưa xong, trình duyệt ném `AbortError`, code cũ gọi
   `stopSpeak()` ⇒ phiên tự chết giữa đoạn. Đã bỏ qua `AbortError`, chỉ báo khi thật sự bị chặn.
3. **Prefetch 2 đoạn bắn trùng** — VieNeu sinh tuần tự qua một `LOCK`, mỗi đoạn 2.7–3s, nên
   đoạn kế bị đẩy hai lần ⇒ tốn gấp đôi CPU và làm dài thời gian chờ. Đã khử trùng bằng `warm`.

Đo sau khi sửa: chạy 60 giây trên một `<audio>`, 4 đoạn nối tiếp (`#0→#4`),
`idleMs = 0`, không lần nào tự dừng.



## Điểm mạnh

- Chọn engine đúng: VieNeu offline, nhanh hơn realtime 3×, chất lượng hơn edge-tts.
- Cache theo `sha1(engine|voice|text)`, hit 14 ms.
- `apply_watermark=False` hợp lý cho dùng cá nhân.
- `_probe_format()` tự dò MP3, giảm 5× băng thông.
- Worker tách process riêng, bind `127.0.0.1`, model load 1 lần.
- `trim_cache`, `already_running`, `_INDEX` TTL — đã nghĩ tới vận hành.

## Điểm yếu

**Critical**

1. Mỗi đoạn một `new Audio()` mới ⇒ khoá màn hình mất tiếng, không có lock-screen control, mất audio focus khi có thông báo/cuộc gọi thì im lặng vĩnh viễn, khoảng lặng 100–400ms giữa các đoạn.
2. 3–6 giây im lặng sau khi bấm NGHE, UI không phản hồi ⇒ người dùng bấm lại và tự huỷ phiên. Prefetch chỉ sâu 1 đoạn.

**High**

3. Tự chuyển chương gọi `new Audio().play()` ngoài user gesture ⇒ iOS/Safari chặn autoplay, "Tự đọc sang chương sau" gần như không chạy trên điện thoại.
4. "NGHE TIẾP" resume giữa đoạn không đáng tin: server trả `200` toàn file, không `Accept-Ranges` ⇒ seek tại `loadedmetadata` im lặng thất bại.

**Medium**

5. `edge_say` để `NoAudioReceived` thoát ra, handler chết giữa chừng, không retry.
6. `scan()` parse lại 1205 file markdown mỗi 3 giây (đo 0.21s), chạy ở mọi request chương.
7. `tts_worker.synth` không expose `temperature` / `repetition_penalty` / `silence_ps`; client chia đoạn nên mất hơi thở giữa đoạn, không dùng `infer_stream`.
8. `playbackRate` thô 0.60–1.60×, không set `preservesPitch` ⇒ méo giọng.

**Low**

9. Ghi `localStorage` mỗi 1.5s vô điều kiện, kể cả khi đang ngủ.
10. `trim_cache` xoá theo `mtime` = lúc tạo ⇒ xoá nhầm đoạn hay nghe (cache_get không touch).
11. Tunnel công khai không auth: ai có URL đều đọc được truyện và đốt CPU máy chủ.

## Kế hoạch

### P0 — tầng phát (≈80% vấn đề)
- [x] Một `<audio id="player">` duy nhất cho cả phiên, đổi `src` thay vì `new Audio()`.
- [x] `navigator.mediaSession` (metadata + play/pause/next/prev).
- [x] `navigator.wakeLock` giữ màn hình khi đang nghe, re-request khi quay lại tab.
- [x] Resume sau khi bị thông báo/cuộc gọi ngắt (qua `onpause`, có guard `speaking`).
- [x] `onended` tự set `src` đoạn kế + `play()` ngay trong handler ⇒ tự chuyển chương vẫn nằm trong quyền autoplay của element.
- [x] Prefetch 3 đoạn (dùng `fetch` làm nóng cache server, rẻ hơn mở media element).
- [x] Phản hồi tức thì: label "ĐANG DỰNG…" trong lúc chờ, đổi "DỪNG" ở `onplaying`.

### P1 — chất lượng và độ tin cậy
- [x] `/api/tts` hỗ trợ `Range` → trả `206` + `Content-Range`, resume giữa đoạn hoạt động thật.
- [x] Nghỉ 320 ms giữa hai đoạn (`PAD`) cho giọng có hơi thở.
- [x] `player.preservesPitch = true`, kẹp tốc độ về 0.85–1.35× (ngoài khoảng này VieNeu méo).
- [x] Bắt exception của `edge_say`, trả `502` JSON sạch thay vì chết giữa response.

### P2 — hiệu năng
- [x] `scan()` tái dùng chương đã parse theo `(mtime, size)` từng file.
- [x] gzip cho JSON > 512 byte khi client nhận `gzip` (239 KB → ~40 KB).
- [x] `ETag` + `304` cho `static/`.

### P3 — dọn nhỏ
- [x] `save()` chỉ chạy khi có thay đổi thật (`dirty`).
- [x] `cache_get` touch file khi hit ⇒ `trim_cache` thành LRU thật.
- [x] `_send` bỏ qua `BrokenPipeError` / `ConnectionResetError` (log đang ngập vì điện thoại huỷ request).
- [x] `#listen` có `aria-pressed`.

## Còn lại (chưa làm)

- Tunnel công khai không auth (P3-#11) — chấp nhận cho dùng cá nhân, cần biết rủi ro.
- `infer_stream` của VieNeu (giảm độ trễ đoạn dài 2210 ký tự từ ~30s chờ xuống còn ~0.3s) — cần đổi sang streaming response, ngoài phạm vi đợt này.
- Khoảng lặng gapless giữa các đoạn: một `<audio>` duy nhất vẫn có ~50–150ms hụt mỗi lần đổi `src`. Nếu cần liền mạch tuyệt đối phải đi đường `AudioContext` + `decodeAudioData`, đổi lại dễ mất background playback trên iOS.
