"""VieNeu-TTS worker — chay bang python cua reader/.venv, khong phai python cua may.

  reader/.venv/Scripts/python.exe reader/tts_worker.py --port 8123

Server doc truyen (reader/server.py) tu khoi dong file nay va goi qua HTTP:
  GET /health            -> {"ready","error","voices","mode","sample_rate"}
  GET /say?text=&voice=  -> audio (wav hoac mp3 neu libsndfile ho tro)

Lan chay dau tien tai model tu HuggingFace (~600MB-1GB) ve cache cua user,
sau do chay hoan toan offline.
"""

import argparse
import io
import json
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

STATE = {"ready": False, "error": None, "voices": [], "tts": None, "mode": "v3turbo",
         "sample_rate": 0, "ctype": "audio/wav"}
LOCK = threading.Lock()


def load_model(mode):
    try:
        from vieneu import Vieneu

        tts = Vieneu(mode=mode)
        STATE["tts"] = tts
        STATE["mode"] = mode
        STATE["sample_rate"] = int(getattr(tts, "sample_rate", 48000))
        STATE["voices"] = [{"id": vid, "name": desc or vid}
                           for desc, vid in sorted(tts.list_preset_voices(), key=lambda x: str(x[1]))]
        STATE["ctype"] = _probe_format()
        STATE["ready"] = True
    except Exception as exc:  # noqa: BLE001
        STATE["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:300])
        traceback.print_exc()


def _probe_format():
    """Chap nhan MP3 (nhe hon ~5 lan) neu libsndfile build kem voi mp3."""
    try:
        import numpy as np
        import soundfile as sf

        buf = io.BytesIO()
        sf.write(buf, np.zeros(480, dtype="float32"), 24000, format="MP3")
        return "audio/mpeg" if buf.tell() > 100 else "audio/wav"
    except Exception:  # noqa: BLE001
        return "audio/wav"


def synth(text, voice):
    tts = STATE["tts"]
    with LOCK:
        audio = tts.infer(text, voice=voice, apply_watermark=False)
    import numpy as np
    import soundfile as sf

    data = np.asarray(audio, dtype="float32").reshape(-1)
    fmt = "MP3" if STATE["ctype"] == "audio/mpeg" else "WAV"
    sr = STATE["sample_rate"]
    if fmt == "MP3" and sr > 48000:
        sr = 48000
    buf = io.BytesIO()
    kw = {"format": fmt, "subtype": "PCM_16"} if fmt == "WAV" else {"format": fmt}
    sf.write(buf, data, sr, **kw)
    return buf.getvalue()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            return self._json({k: STATE[k] for k in ("ready", "error", "voices", "mode",
                                                     "sample_rate", "ctype")})
        if u.path == "/say":
            q = parse_qs(u.query)
            text = (q.get("text", [""])[0] or "")[:3000].strip()
            voice = q.get("voice", [""])[0]
            known = {v["id"] for v in STATE["voices"]}
            if not text or voice not in known:
                return self._json({"error": "thieu text hoac voice khong hop le"}, 400)
            if not STATE["ready"]:
                return self._json({"error": STATE["error"] or "model dang khoi dong"}, 503)
            try:
                audio = synth(text, voice)
            except Exception as exc:  # noqa: BLE001
                traceback.print_exc()
                return self._json({"error": str(exc)[:200]}, 500)
            self.send_response(200)
            self.send_header("Content-Type", STATE["ctype"])
            self.send_header("Content-Length", str(len(audio)))
            self.send_header("Cache-Control", "public, max-age=604800, immutable")
            self.end_headers()
            self.wfile.write(audio)
            return
        self._json({"error": "khong tim thay"}, 404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8123)
    ap.add_argument("--mode", default="v3turbo", help="v3turbo | v3nano | standard")
    args = ap.parse_args()
    threading.Thread(target=load_model, args=(args.mode,), daemon=True).start()

    class Server(ThreadingHTTPServer):
        # Khong cho "tranh" port: worker nao den sau thi chap nhan thua va de duoc go.
        allow_reuse_address = 0

    try:
        srv = Server((args.host, args.port), Handler)
    except OSError:
        print("Da co worker khong dang chay o %s:%d, thoat." % (args.host, args.port), flush=True)
        return
    print("VieNeu worker: http://%s:%d (mode %s)" % (args.host, args.port, args.mode), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
