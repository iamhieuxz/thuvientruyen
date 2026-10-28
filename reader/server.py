"""Trang doc truyen local (mobile-first, dark) phuc vu cac chuong da dich.

 Dung:  python reader/server.py [--port 8000] [--host 0.0.0.0]
"""

import argparse
import asyncio
import gzip
import hashlib
import html
import json
import os
import re
import socket
import subprocess
import time
import urllib.parse
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
LIB = ROOT.parent / "data"          # moi truyen = mot thu muc con trong day
STATIC = ROOT / "static"
CACHE = ROOT / "cache"

DEFAULT_BOOK = "baojian_vi"
DEFAULT_VOICE = "Ngọc Huyền"

HEAD_RE = re.compile(r"^<!--\s*chuong\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*-->\s*", re.S)
TITLE_RE = re.compile(r"^#\s*Chương\s*(\d+)\s*[:\u2013\-]\s*(.+?)\s*$", re.M)
SEP_RE = re.compile(r"^[－—–\-_=\*\s]{3,}$")
TAIL_RE = re.compile(r"^\((?:Còn tiếp|Hết|Kết)\)$", re.I)

_INDEX = {}                          # bid -> {"built", "chapters", "by_num"}
_PARSED = {}                         # path -> (mtime, size, chapter), tránh parse lại 1205 file


def parse_chapter(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = HEAD_RE.match(raw)
    han = extra = ""
    if m:
        num_src, han, extra = m.group(1), m.group(2), m.group(3)
        raw = raw[m.end():]
    t = TITLE_RE.search(raw)
    if t:
        num, title = int(t.group(1)), t.group(2).strip()
        raw = raw[: t.start()] + raw[t.end():]
    else:
        num = int(path.name[:4])
        title = "Chương %d" % num

    tags = " · ".join(re.findall(r"【(.+?)】", title))
    title = re.sub(r"\s*【.+?】", "", title).strip()

    blocks = []
    for para in re.split(r"\n\s*\n", raw.strip()):
        p = " ".join(para.split("\n")).strip()
        if not p or p.startswith("<!--"):
            continue
        if SEP_RE.match(p):
            blocks.append({"type": "sep"})
        elif TAIL_RE.match(p):
            blocks.append({"type": "tail", "text": p})
        else:
            blocks.append({"type": "p", "text": p})

    chars = sum(len(b.get("text", "")) for b in blocks)
    return {
        "n": num,
        "title": title,
        "tag": tags,
        "han": han,
        "file": path.name,
        "blocks": blocks,
        "chars": chars,
        "minutes": max(1, round(chars / 700)),
        "mtime": int(path.stat().st_mtime),
    }


def scan(bid, force=False):
    """Duyet thu muc data/<bid>, dung cache 3 giay de chuong moi tu dong xuat hien."""
    now = time.time()
    idx = _INDEX.get(bid)
    if idx and not force and now - idx["built"] < 3:
        return idx
    d = LIB / bid
    idx = {"built": now, "chapters": [], "by_num": {}}
    _INDEX[bid] = idx
    if not d.is_dir():
        return idx
    items = []
    for p in d.glob("*.md"):
        if not p.name[:4].isdigit():
            continue
        try:
            st = p.stat()
            key = (st.st_mtime, st.st_size)
            hit = _PARSED.get(str(p))
            if hit and hit[0] == key:
                items.append(hit[1])
                continue
            c = parse_chapter(p)
            _PARSED[str(p)] = (key, c)
            items.append(c)
        except Exception as exc:  # noqa: BLE001
            print("bo qua", p.name, exc)
    items.sort(key=lambda c: c["n"])
    idx.update(chapters=items, by_num={c["n"]: c for c in items})
    return idx


def pretty(bid):
    return " ".join(w.capitalize() for w in re.split(r"[-_\s]+", bid) if w)


def book_info(bid):
    """Doc data/<bid>/book.json (tuy chon), thieu thi suy tu ten thu muc."""
    d = LIB / bid
    meta = {}
    f = d / "book.json"
    if f.is_file():
        try:
            meta = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            meta = {}
    names = ([meta.get("cover")] if meta.get("cover") else []) + \
            ["cover.jpg", "cover.jpeg", "cover.png", "cover.webp"]
    cover = next((n for n in names if n and (d / n).is_file()), None)
    return {
        "id": bid,
        "title": meta.get("title") or pretty(bid),
        "author": meta.get("author", ""),
        "desc": meta.get("desc", ""),
        "source": meta.get("source", ""),
        "cover": cover,
    }


def book_ids():
    """Thu muc nao trong data/ co chuong dich (NNNN_*.md) deu la mot truyen."""
    out = []
    if not LIB.exists():
        return out
    for d in sorted(LIB.iterdir()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        if any(p.name[:4].isdigit() for p in d.glob("*.md")):
            out.append(d.name)
    return out


def pick(bid):
    return bid if bid in book_ids() else None


def books_payload():
    out = []
    for bid in book_ids():
        info = book_info(bid)
        chs = scan(bid)["chapters"]
        if not chs:
            continue
        info.update(
            chapters=len(chs),
            chars=sum(c["chars"] for c in chs),
            minutes=sum(c["minutes"] for c in chs),
            first=chs[0]["n"],
            last=chs[-1]["n"],
            updated=max(c["mtime"] for c in chs),
        )
        out.append(info)
    return out


def meta_list(bid):
    out = []
    for c in scan(bid)["chapters"]:
        out.append({k: c[k] for k in ("n", "title", "tag", "han", "chars", "minutes", "mtime")})
    return out


def hint(bid, num):
    """Vi tri + tieu de cua mot chương, lay ngan gon cho the ke sach."""
    chs = scan(bid)["chapters"]
    if not chs:
        return {"n": None, "title": "", "i": 0, "total": 0}
    nums = [c["n"] for c in chs]
    n = min(max(num, nums[0]), nums[-1])
    if n not in nums:
        n = min(nums, key=lambda x: abs(x - n))
    i = nums.index(n)
    return {"n": n, "title": chs[i]["title"], "i": i + 1, "total": len(chs)}


def chapter_payload(bid, num):
    idx = scan(bid)
    chs = idx["chapters"]
    if not chs:
        return None
    num = min(max(num, chs[0]["n"]), chs[-1]["n"])
    c = idx["by_num"].get(num)
    if c is None:
        nearest = min((x["n"] for x in chs), key=lambda n: abs(n - num))
        c = idx["by_num"][nearest]
    nums = [x["n"] for x in chs]
    i = nums.index(c["n"])
    body = []
    for b in c["blocks"]:
        if b["type"] == "sep":
            body.append("<hr class='sep'>")
        elif b["type"] == "tail":
            body.append("<p class='tail'>%s</p>" % html.escape(b["text"]))
        else:
            body.append("<p>%s</p>" % html.escape(b["text"]))
    return {
        "book": bid,
        "n": c["n"],
        "title": c["title"],
        "tag": c.get("tag", ""),
        "han": c["han"],
        "file": c["file"],
        "chars": c["chars"],
        "minutes": c["minutes"],
        "mtime": c["mtime"],
        "html": "".join(body),
        "prev": nums[i - 1] if i > 0 else None,
        "next": nums[i + 1] if i + 1 < len(nums) else None,
        "first": nums[0],
        "last": nums[-1],
        "total": len(nums),
        "index": i + 1,
    }


def lan_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info[4][0])
    except OSError:
        pass
    return sorted(ip for ip in ips if not ip.startswith("127."))


_VOICES = {"at": 0.0, "ok": False, "data": []}


def neural_voices():
    """Liec gioi noi tieng Viet cua Microsoft (can mang); loi thi tra rong."""
    if _VOICES["ok"] and time.time() - _VOICES["at"] < 86400:
        return _VOICES["data"]
    if not _VOICES["ok"] and time.time() - _VOICES["at"] < 300:
        return _VOICES["data"]
    _VOICES["at"] = time.time()
    try:
        import edge_tts

        vs = asyncio.run(edge_tts.list_voices())
        _VOICES["data"] = [
            {"id": v["ShortName"],
             "name": re.sub(r"^\d+\s+", "", v.get("FriendlyName") or v["ShortName"]),
             "gender": v.get("Gender", "")}
            for v in vs if v["Locale"].startswith("vi")
        ]
        _VOICES["ok"] = True
    except Exception as exc:  # noqa: BLE001
        print("liet ke voice that bai:", exc)
        _VOICES["data"] = []
    return _VOICES["data"]


def cache_key(engine, voice, text):
    return hashlib.sha1(("%s|%s|%s" % (engine, voice, text)).encode("utf-8")).hexdigest()[:28]


def cache_get(engine, voice, text):
    """Tra ve (audio, content-type) neu da co trong cache, nguoc lai (None, None)."""
    base = cache_key(engine, voice, text)
    for ext, ctype in ((".mp3", "audio/mpeg"), (".wav", "audio/wav")):
        p = CACHE / (base + ext)
        try:
            if p.stat().st_size:
                os.utime(p)          # touch: trim_cache xoa theo mtime = lan dung gan nhat
                return p.read_bytes(), ctype
        except OSError:
            pass
    return None, None


def cache_put(engine, voice, text, audio, ctype):
    ext = ".mp3" if ctype == "audio/mpeg" else ".wav"
    p = CACHE / (cache_key(engine, voice, text) + ext)
    try:
        p.write_bytes(audio)
    except OSError:
        pass


def cache_path(engine, voice, text):
    return CACHE / (cache_key(engine, voice, text) + ".mp3")


def edge_say(text, voice):
    """Sinh MP3 qua edge-tts (can mang), luu vao reader/cache."""
    import edge_tts

    out = cache_path("edge", voice, text)
    tmp = out.with_name(out.stem + "." + uuid.uuid4().hex[:6] + ".part")
    try:
        asyncio.run(edge_tts.Communicate(text, voice).save(str(tmp)))
        tmp.replace(out)
        return out.read_bytes()
    finally:
        tmp.unlink(missing_ok=True)


def trim_cache(keep=1500):
    """Gioi bo file am thanh cu nhat, tranh de cache phinh dai."""
    if not CACHE.exists():
        return 0
    files = sorted(list(CACHE.glob("*.mp3")) + list(CACHE.glob("*.wav")),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    gone = 0
    for p in files[keep:]:
        try:
            p.unlink()
            gone += 1
        except OSError:
            pass
    return gone


VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
WORKER_LOG = ROOT / "vieneu.log"
W = {"port": 8123, "proc": None, "state": "missing", "voices": [], "error": None,
     "at": 0.0, "off": False}


def worker_health(timeout=1.2):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/health" % W["port"], timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8"))
    except (OSError, ValueError):
        return None
    W["voices"] = d.get("voices") or []
    W["error"] = d.get("error")
    W["state"] = "ready" if d.get("ready") else ("error" if d.get("error") else "loading")
    return d


def worker_start():
    """Nhan worker VieNeu (venv rieng) neu chua chay."""
    if W["off"]:
        W["state"] = "off"
        W["voices"] = []
        return
    if not VENV_PY.exists():
        W["state"] = "missing"
        return
    if worker_health(4.0) is not None:
        return
    if W["proc"] is not None and W["proc"].poll() is None:
        W["state"] = "loading"
        return
    if time.time() - W["at"] < 20:
        return
    W["at"] = time.time()
    try:
        log = open(WORKER_LOG, "ab")
        W["proc"] = subprocess.Popen(
            [str(VENV_PY), str(ROOT / "tts_worker.py"), "--port", str(W["port"])],
            stdout=log, stderr=log, cwd=str(ROOT.parent))
        W["state"] = "loading"
    except OSError as exc:
        W["state"] = "error"
        W["error"] = str(exc)


def worker_say(text, voice, timeout=600):
    url = "http://127.0.0.1:%d/say?%s" % (
        W["port"], urllib.parse.urlencode({"text": text, "voice": voice}))
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.read(), r.headers.get("Content-Type", "audio/wav")
    except OSError:
        return None, None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, fmt, *args):  # im lặng trên console
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        extra = extra or {}
        try:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            # JSON 239 KB cua /api/chapters gui lai moi lan mo chuong: nen lai khi client nhan
            if len(body) > 512 and "gzip" in (self.headers.get("Accept-Encoding") or "") \
                    and ctype.split("/")[0] in ("text", "application"):
                body = gzip.compress(body, 6)
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(body)))
            if "Cache-Control" not in extra:
                self.send_header("Cache-Control", "no-cache")
            for k, v in extra.items():
                self.send_header(k, v)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass                # dien thoai huy request, khong phai loi

    def _audio(self, audio, ctype):
        """Tra audio, ho tro Range de 'NGHE TIEP' seek duoc giua doan."""
        total = len(audio)
        rng = self.headers.get("Range") or ""
        m = re.match(r"^bytes=(\d*)-(\d*)$", rng.strip())
        if not m or (not m.group(1) and not m.group(2)):
            return self._send(200, audio, ctype,
                              {"Accept-Ranges": "bytes",
                               "Cache-Control": "public, max-age=604800, immutable"})
        if m.group(1):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else total - 1
        else:                   # bytes=-N : N byte cuoi
            start = max(0, total - int(m.group(2)))
            end = total - 1
        end = min(end, total - 1)
        if start > end or start >= total:
            return self._send(416, b"", ctype, {"Content-Range": "bytes */%d" % total})
        return self._send(206, audio[start:end + 1], ctype,
                          {"Accept-Ranges": "bytes",
                           "Content-Range": "bytes %d-%d/%d" % (start, end, total),
                           "Cache-Control": "public, max-age=604800, immutable"})

    def _static(self, name):
        p = (STATIC / name).resolve()
        if not p.is_file() or STATIC not in p.parents:
            return self._send(404, "not found", "text/plain; charset=utf-8")
        types = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
                 ".js": "application/javascript; charset=utf-8", ".svg": "image/svg+xml",
                 ".woff2": "font/woff2",
                 ".webmanifest": "application/manifest+json"}
        body = p.read_bytes()
        etag = '"%s"' % hashlib.sha1(body).hexdigest()[:16]
        if etag in (self.headers.get("If-None-Match") or ""):
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self._send(200, body, types.get(p.suffix, "application/octet-stream"),
                   {"ETag": etag, "Cache-Control": "no-cache"})

    def _redirect(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _cover(self, bid):
        info = book_info(bid)
        p = (LIB / bid / info["cover"]).resolve() if info["cover"] else None
        if not p or not p.is_file() or LIB not in p.parents:
            return self._send(404, "khong co anh bia", "text/plain; charset=utf-8")
        types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                 ".webp": "image/webp", ".gif": "image/gif"}
        self._send(200, p.read_bytes(), types.get(p.suffix.lower(), "application/octet-stream"),
                   {"Cache-Control": "public, max-age=300"})

    def do_GET(self):
        path = urlparse(self.path).path
        q = parse_qs(urlparse(self.path).query)
        bid = pick(q.get("book", [""])[0]) or DEFAULT_BOOK
        if path == "/":
            return self._static("shelf.html")
        m = re.match(r"^/sach/([A-Za-z0-9._-]{1,64})(?:/chuong/(\d+))?/?$", path)
        if m:
            if not pick(m.group(1)):
                return self._send(404, "khong co truyen nay", "text/plain; charset=utf-8")
            return self._static("index.html")
        m = re.match(r"^/read/(\d+)$", path)
        if m:
            return self._redirect("/sach/%s/chuong/%s" % (DEFAULT_BOOK, m.group(1)))
        if path.startswith("/static/"):
            return self._static(path[len("/static/"):])
        if path == "/api/books":
            return self._send(200, json.dumps({"books": books_payload()}))
        if path == "/api/book":
            return self._send(200, json.dumps(book_info(bid)))
        if path == "/api/cover":
            return self._cover(bid)
        if path == "/api/chapters":
            return self._send(200, json.dumps({"book": bid, "chapters": meta_list(bid)}))
        if path == "/api/hint":
            try:
                n = int(q.get("n", ["0"])[0])
            except ValueError:
                n = 0
            return self._send(200, json.dumps(hint(bid, n)))
        if path == "/api/reload":
            scan(bid, force=True)
            return self._send(200, json.dumps({"total": len(scan(bid)["chapters"])}))
        if path == "/api/ping":
            return self._send(200, json.dumps({"app": "baogiam-reader"}))
        if path == "/api/voices":
            worker_start()
            return self._send(200, json.dumps({
                "neural": neural_voices(),
                "vieneu": W["voices"],
                "vieneu_state": W["state"],
                "vieneu_error": W["error"],
                "default": DEFAULT_VOICE,
            }))
        if path == "/api/tts":
            q = parse_qs(urlparse(self.path).query)
            eng = "vieneu" if q.get("engine", [""])[0] == "vieneu" else "edge"
            voice = q.get("voice", [""])[0]
            text = (q.get("text", [""])[0] or "")[:3000].strip()
            if not text or not voice:
                return self._send(400, json.dumps({"error": "thieu text hoac voice"}))
            CACHE.mkdir(exist_ok=True)
            audio, ctype = cache_get(eng, voice, text)
            if audio is None and eng == "vieneu":
                ids = {v["id"] for v in W["voices"]} or {v["id"] for v in (worker_health() or {}).get("voices", [])}
                if voice not in ids:
                    return self._send(503, json.dumps({"error": "vieNeu chua san sang",
                                                       "state": W["state"]}))
                audio, ctype = worker_say(text, voice)
                if audio:
                    cache_put(eng, voice, text, audio, ctype)
            elif audio is None:
                if voice not in {v["id"] for v in neural_voices()}:
                    return self._send(400, json.dumps({"error": "voice khong hop le"}))
                try:
                    audio, ctype = edge_say(text, voice), "audio/mpeg"
                except Exception as exc:  # noqa: BLE001
                    print("edge-tts loi:", exc)
                    return self._send(502, json.dumps({"error": "edge-tts khong tra audio",
                                                       "detail": str(exc)[:200]}))
            if not audio:
                return self._send(502, json.dumps({"error": "khong sinh duoc audio", "state": W["state"]}))
            return self._audio(audio, ctype)
        m = re.match(r"^/api/chapter/(\d+)$", path)
        if m:
            data = chapter_payload(bid, int(m.group(1)))
            if data is None:
                return self._send(404, json.dumps({"error": "chua co chuong nao"}))
            return self._send(200, json.dumps(data))
        return self._send(404, "not found", "text/plain; charset=utf-8")


def already_running(host, port):
    """True nếu port này đang có một reader khác phục vụ (tránh mở hai cửa cùng vào)."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/api/ping" % port, timeout=2.5) as r:
            return b"baogiam-reader" in r.read()
    except OSError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--worker-port", type=int, default=8123)
    ap.add_argument("--no-vieneu", action="store_true",
                    help="khong khoi dong engine VieNeu-TTS (venv rieng)")
    args = ap.parse_args()
    W["port"] = args.worker_port
    W["off"] = args.no_vieneu

    if already_running(args.host, args.port):
        print("Port %d da co mot reader dang chay. Dung cua do hoac mo cua khac:" % args.port,
              flush=True)
        print("  python reader/server.py --port 8888", flush=True)
        return

    for bid in book_ids():
        scan(bid, force=True)
    books = books_payload()
    if not books:
        print("Khong tim thay truyen nao trong %s (can thu muc chua file NNNN_*.md)" % LIB)
        return

    try:
        srv = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as exc:
        print("Khong mo duoc port %d (%s). Chay lai voi: python reader/server.py --port 8888"
              % (args.port, exc), flush=True)
        return

    host = "localhost" if args.host in ("0.0.0.0", "") else args.host
    print("=" * 58)
    print("  Ke sach     : %d truyen — http://%s:%d" % (len(books), host, args.port), flush=True)
    for b in books:
        print("    %-12s %s (%s) — %d chuong (%d-%d), %d tu" % (
            b["id"] + ":", b["title"], b["author"] or "?", b["chapters"],
            b["first"], b["last"], b["chars"]), flush=True)
        print("    %-12s http://%s:%d/sach/%s" % ("", host, args.port, b["id"]), flush=True)
    for ip in lan_ips():
        print("  Dien thoai  : http://%s:%d  ( cung WiFi )" % (ip, args.port), flush=True)
    print("  Thu muc     : %s" % LIB, flush=True)
    nv = neural_voices()
    print("  Doc giong   : edge-tts %s" % ("%d tieng Viet" % len(nv) if nv else "khong ket noi duoc mang"), flush=True)
    if args.no_vieneu:
        print("  VieNeu-TTS  : tat (--no-vieneu)", flush=True)
    elif not VENV_PY.exists():
        print("  VieNeu-TTS  : chua cai — %s" % str(VENV_PY.relative_to(ROOT.parent)), flush=True)
    else:
        worker_start()
        msg = {"ready": "san sang — %d giong Viet" % len(W["voices"]),
               "loading": "worker %d dang khoi dong (lan dau tai model, xem reader/vieneu.log)"
                          % W["port"],
               "error": "worker loi — xem reader/vieneu.log"}.get(W["state"], W["state"])
        print("  VieNeu-TTS  : %s" % msg, flush=True)
    cut = trim_cache()
    if cut:
        print("  Cache TTS   : da don %d file cu" % cut, flush=True)
    print("  Ctrl+C de dung", flush=True)
    print("=" * 58, flush=True)

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung.")


if __name__ == "__main__":
    main()
