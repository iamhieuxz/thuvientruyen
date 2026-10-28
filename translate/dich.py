# -*- coding: utf-8 -*-
"""
Dich truyen Trung -> Viet, dung GLOSSARY lam chuan.
Ho tro nhieu backend: gemini (Google AI Studio) hoac openai-compatible.
Tu dung khi het ha muc (rat dau het request -> luu -> thoat).

Dung:
  python dich.py --from 1 --to 20
  python dich.py --from 1 --to 20 --limit 10      # chi dich 10 chuong
  python dich.py --from 1 --to 1282 --reset      # lam lai tu dau
  python dich.py --status
"""
import argparse, os, re, sys, time, json, glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import urllib.request
import urllib.error

# Console Windows mac dinh cp1252: in chu bao loi tieng Viet (a ring 'ư') lam
# crash ca lot dich giua chung -> ep stdout/stderr la UTF-8.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(r"f:\taitruyen")

# ── Cấu hình từng truyện ──────────────────────────────────────────────
# Mỗi truyện = 1 thư mục nguồn .txt + 1 thư mục output .md + file trạng thái riêng.
# Thêm truyện mới: thêm 1 khối vào BOOKS, không cần sửa code khác.
BOOKS = {
    "baojian": {
        "src": "baojian",
        "out": "baojian_vi",
        "glossary": "glossary.md",
        "notes": "notes.txt",
        "state": "state.json",
        "titles": "titles_vi.json",
        "chapter_map": "chapter_map.json",
    },
    "can_bao_chan_long": {
        "src": "canh-bao-chan-long-xuat-nguc",
        "out": "can_bao_chan_long_vi",
        "glossary": "glossary_can_bao_chan_long.txt",
        "notes": "notes_can_bao_chan_long.txt",
        "state": "state_can_bao_chan_long.json",
        "titles": "titles_can_bao_chan_long.json",
        "chapter_map": "",           # số chương trùng số file → không cần map
    },
    "nhi_huu_thien_nhan": {
        "src": "nhi-huu-thien-nhan-bat-khu-do-thach-huu-tai-loan-khan",
        "out": "nhi_huu_thien_nhan_vi",
        "glossary": "glossary_nhi_huu_thien_nhan.txt",
        "notes": "notes_nhi_huu_thien_nhan.txt",
        "state": "state_nhi_huu_thien_nhan.json",
        "titles": "titles_nhi_huu_thien_nhan.json",
        "chapter_map": "",
    },
    "nien_dai_58": {
        "src": "nien-dai-nga-tai-58-huu-khoi-dien",
        "out": "nien_dai_58_vi",
        "glossary": "glossary_nien_dai_58.txt",
        "notes": "notes_nien_dai_58.txt",
        "state": "state_nien_dai_58.json",
        "titles": "titles_nien_dai_58.json",
        "chapter_map": "",
    },
}

# Biến toàn cục trỏ vào truyện đang chạy (set_book() gán lại).
BOOK = "baojian"
SRC = ROOT / "truyendich_scraper" / BOOKS[BOOK]["src"]
OUT = ROOT / "data" / BOOKS[BOOK]["out"]
NOTES = ROOT / "translate" / BOOKS[BOOK]["notes"]
GLOSSARY = ROOT / "translate" / BOOKS[BOOK]["glossary"]
STATE = ROOT / "translate" / BOOKS[BOOK]["state"]
TITLES = ROOT / "translate" / BOOKS[BOOK]["titles"]
CHAPTER_MAP = ROOT / "translate" / BOOKS[BOOK]["chapter_map"] if BOOKS[BOOK]["chapter_map"] else None


def set_book(name):
    """Trỏ các đường dẫn toàn cục sang truyện `name`."""
    global BOOK, SRC, OUT, NOTES, GLOSSARY, STATE, TITLES, CHAPTER_MAP
    if name not in BOOKS:
        sys.exit("Khong co truyen '%s'. Co: %s" % (name, ", ".join(BOOKS)))
    cfg = BOOKS[name]
    BOOK = name
    SRC = ROOT / "truyendich_scraper" / cfg["src"]
    OUT = ROOT / "data" / cfg["out"]
    NOTES = ROOT / "translate" / cfg["notes"]
    GLOSSARY = ROOT / "translate" / cfg["glossary"]
    STATE = ROOT / "translate" / cfg["state"]
    TITLES = ROOT / "translate" / cfg["titles"]
    CHAPTER_MAP = ROOT / "translate" / cfg["chapter_map"] if cfg["chapter_map"] else None

MARKER = re.compile(r'^[ \t]*\d+\|[ \t]*$', re.M)
REPL = [("\ufffd", ""), ("\ufffd", ""), ("\u66f0", "\u65e5")]


# ─────────────────────────── hàm phụ ───────────────────────────

def load_env():
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def clean(t):
    t = MARKER.sub("", t)
    for a, b in REPL:
        t = t.replace(a, b)
    return t.strip()


PS_HEAD = re.compile(r"(?i)^\s*[-–—*·]*\s*(?:p\.?s)\s*[:：]")
NOISE = re.compile(r"飘天|getmode|selectcolors|gundong|getfont|宝鉴最新章节|选择背景颜|"
                   r"选择字体大小|注册会员|私人书架|bixia\.org")
PAREN_JUNK = re.compile(
    r"[（(][^（()）]{0,400}?(?:未完待续|微信|公众号|qdread|月票|推荐票|百度搜索|抽奖|"
    r"注册会员|私人书架|飘天)[^（()）]{0,400}?[)）]")
INLINE_JUNK = re.compile(r"宝鉴\d+|百度搜索[“”\"']{0,2}|【[^】]{0,60}bixia[^】]{0,60}】")
PROMO_KW = ("月票", "推荐票", "订阅", "加入收藏", "更多支持", "书友群", "样书",
            "更多精彩", "独家故事", "打赏", "微信", "威信", "新榜", "推荐位")


def strip_src_junk(text):
    """Gỡ ghi chú tác giả (PS), quảng cáo và rác scraper chèn giữa chương."""
    # "(未完待续..." luôn là dấu hiệu kết thúc chương -> cắt sạch phần đuôi
    text = re.sub(r"[（(]?\s*未完待续.*$", "", text, flags=re.S)
    text = PAREN_JUNK.sub("", text)
    text = INLINE_JUNK.sub("", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    cut = None
    for i, p in enumerate(paras):
        if PS_HEAD.match(p) and i >= len(paras) * 0.5:
            cut = i
            break
    kept = paras if cut is None else paras[:cut]
    out = []
    for p in kept:
        if NOISE.search(p) or (PS_HEAD.match(p) and len(p) < 600):
            continue
        if len(p) < 400 and sum(k in p for k in PROMO_KW) >= 2:
            continue
        out.append(p.strip())
    return "\n\n".join(x for x in out if x).strip()


def dedup_repeats(text):
    """Nguồn lỗi scraper: cùng một chương bị lặp 2-4 lần liên tiếp (file 0818 =
    truyện 777 lặp 3 lần). Dịch một lần là đủ; giữ lại khối đầu tiên."""
    sents = [x.strip() for x in re.split(r"(?<=[。！？])", text) if x.strip()]
    if len(sents) < 20:
        return text
    for n in (4, 3, 2):
        k = len(sents) // n
        if k < 8:
            continue
        first = set(sents[:k])
        ok = all(len(first & set(sents[i * k:(i + 1) * k])) / len(first) >= 0.8
                 for i in range(1, n))
        if ok:
            return "".join(sents[:k]).strip()
    return text


SEG = re.compile(r".+?(?:[。！？…]+”|”|$)", flags=re.S)


def break_long_lines(text):
    """Nguồn lỗi (file 0818...) nén cả chương thành MỘT dòng dài -> model dịch
    ra một khối đặc, không còn đoạn văn. Tách lại theo câu: xuống dòng trước mỗi
    lời thoại và sau khi tích lũy đủ ~150 ký tự. Không được làm mất ký tự nào."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        if len(para) < 500:
            out.append(para)
            continue
        segs = [s.strip() for s in SEG.findall(para) if s.strip()]
        assert sum(len(s) for s in segs) >= len(re.sub(r"\s", "", para)) - 5, \
            "break_long_lines làm mất nội dung"
        chunks, buf = [], ""
        for seg in segs:
            if buf and (seg.startswith("“") or len(buf) > 150):
                chunks.append(buf)
                buf = seg
            else:
                buf = (buf + " " + seg).strip()
        if buf:
            chunks.append(buf)
        out.append("\n\n".join(chunks))
    return "\n\n".join(out).strip()


def fix_quotes(t):
    """Đổi ngoặc kép ASCII thành ngoặc kép cong, xen kẽ mở/đóng toàn văn bản.
    Cách này xử lý được cả đoạn thoại dài nhiều đoạn chỉ có một cặp ngoặc."""
    if t.count('"') % 2:
        return t
    out = []
    opening = True
    for ch in t:
        if ch == '"':
            out.append("“" if opening else "”")
            opening = not opening
        else:
            out.append(ch)
    return "".join(out)


EXCL_TA = {"chúng", "người", "anh", "cô", "ông", "bà", "hắn", "nó",
           "thằng", "con", "vợ", "chồng", "em", "chú", "bác", "cậu",
           "mợ", "thím", "chị", "một", "hai"}


def _fix_pronouns(t):
    """Thay đại từ cổ 'ngươi/ta/lão tử' — glossary cấm dùng."""
    t = re.sub(r"(?i)lão tử|lão phu", "tôi", t)
    out, prev = [], ""
    for tok in re.split(r"(\s+)", t):
        if tok.isspace():
            out.append(tok)
            continue
        core = re.sub(r"^[^\wÀ-ỹ]+|[^\wÀ-ỹ]+$", "", tok)
        low = core.lower()
        if low == "ngươi":
            out.append(tok.replace("ngươi", "cậu").replace("Ngươi", "Cậu"))
        elif low == "ta" and prev.lower() not in EXCL_TA:
            out.append(tok.replace("ta", "tôi").replace("Ta", "Tôi"))
        else:
            out.append(tok)
        prev = core if core else prev
    return "".join(out)


def normalize_address(t):
    """Chuẩn hóa xưng hô theo glossary: bỏ 'ngài', sửa cách gọi Tần Phong."""
    t = t.replace("ngài", "ông").replace("Ngài", "Ông")
    t = re.sub(r"(?i)Cựu Kim Sơn", "San Francisco", t)
    # địa danh hồi Hồng Kông: luôn dùng Hán Việt, không viết ngược/romaji
    t = re.sub(r"(?i)đảo Cảng|Cảng đảo", "Cảng Đảo", t)
    t = re.sub(r"(?i)Thâm Thủy Phụ", "Thâm Thủy Bộ", t)
    t = re.sub(r"(?i)\bNakashima\b", "Trung Đảo", t)
    t = re.sub(r"(?i)\bHashimoto\b", "Kiều Bản", t)
    t = re.sub(r"(?i)Yamamoto (?:Yuken|Kensuke)", "Yamamoto Chi Kiện", t)
    t = re.sub(r"(?i)Tần tiên sinh", "anh Tần", t)
    t = re.sub(r"(^|[“”\"'\.\!\?]\s*)anh Tần", r"\1Anh Tần", t, flags=re.M)
    t = _fix_pronouns(t)
    if t.count("“") > t.count("”"):
        # dấu đóng thoại bị model gõ thành apostrophe: "……’" -> "……”"
        t = re.sub(r"(?<=…)’", "”", t)
    return t


def chap_num(fn):
    m = re.match(r"^(\d+)_", fn)
    return int(m.group(1)) if m else None


def all_chapters():
    out = {}
    for f in os.listdir(SRC):
        if f.endswith(".txt"):
            n = chap_num(f)
            if n:
                out[n] = f
    return out


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": [], "failed": [], "new_terms": [], "quota_hits": 0}


def save_state(s):
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")


def load_titles():
    if TITLES.exists():
        return {int(k): v for k, v in
                json.loads(TITLES.read_text(encoding="utf-8")).items()}
    return {}


def load_chapter_map():
    if CHAPTER_MAP and CHAPTER_MAP.exists():
        return json.loads(CHAPTER_MAP.read_text(encoding="utf-8"))
    return {}


def ensure_titles(todo, chs, api, cmap):
    """Dich tieu de cua lo chuong sap dich (1 lan goi API cho ca lo).
    todo: danh sach (file_index, story_number)."""
    titles = load_titles()
    missing = []
    generic = []
    for n, s in todo:
        if s in titles:
            continue
        raw = chs[n].split("_", 1)[1].rsplit(".", 1)[0]
        if re.fullmatch(r"第\d+章", raw):
            generic.append(s)
        else:
            missing.append((s, raw))
    for s in generic:
        titles[s] = f"Chương {s}"
    if generic:
        TITLES.write_text(
            json.dumps({str(k): v for k, v in titles.items()},
                       ensure_ascii=False, indent=0, sort_keys=True),
            encoding="utf-8")
    if not missing:
        return titles

    print(f"Dich {len(missing)} tieu de chuong...", flush=True)
    got = {}
    for i in range(0, len(missing), 60):
        batch = missing[i:i + 60]
        lines = "\n".join(f"{s}|{t}" for s, t in batch)
        prompt = f"""Bạn là dịch giả Trung -> Việt. Dịch TIÊU ĐỀ chương truyện sau sang tiếng Việt tự nhiên.

QUY TẮC:
- Số đầu dòng là số chương THẬT trong bản dịch. Luôn dùng đúng số đó, KHÔNG lấy số ghi trong tiêu đề Hán.
- Định dạng mỗi dòng: <số đầu dòng tôi đưa>|<Chương N: tên chương tiếng Việt> với N đúng bằng số đầu dòng.
- (上)/(中)/(下) → (Thượng)/(Trung)/(Hạ).
- Chỉ xuất đúng các dòng kết quả, không thêm lời giải thích.

{lines}"""
        try:
            raw = api(prompt + f"\n\n(Mã tác vụ: {time.time_ns()})")
        except (RateLimit, ServerBusy, Truncated) as e:
            print(f"  khong dich duoc tieu de: {e}", flush=True)
            break
        for ln in raw.splitlines():
            m = re.match(r"^\s*(\d+)\s*[|｜]\s*(.+?)\s*$", ln)
            if not m:
                continue
            n = int(m.group(1))
            if n not in dict(batch):
                continue
            val = m.group(2)
            val = re.sub(r"^Chương\s*\d+\s*[:：-]?\s*", "", val).strip()
            if not val:
                val = f"Chương {n}"
            else:
                val = f"Chương {n}: {val}"
            got[n] = val

    if got:
        titles.update(got)
        TITLES.write_text(
            json.dumps({str(k): v for k, v in titles.items()},
                       ensure_ascii=False, indent=0, sort_keys=True),
            encoding="utf-8")
        print(f"  da co {len(got)}/{len(missing)} tieu de tieng Viet", flush=True)
    return titles


def strip_heading(t, raw_title=""):
    """Bo dong tieu de model tu sinh (ca ban Han lan ban Viet)."""
    def norm(s):
        return re.sub(r"\s+", "", s).replace("（", "(").replace("）", ")")

    lines = t.lstrip().splitlines()
    while lines:
        line = lines[0].strip().lstrip("#*").strip()
        if not line:
            lines.pop(0)
            continue
        is_vi_title = re.match(r"^Chương\s*\d+", line)
        is_han_title = (re.search(r"[\u4e00-\u9fff]", line)
                        and len(line) < 60)
        if is_vi_title or is_han_title or norm(line) == norm(raw_title):
            lines.pop(0)
            continue
        break
    return "\n".join(lines).strip()


def mark_failed(st, n):
    if n not in st["failed"]:
        st["failed"].append(n)


# ─────────────────────────── gọi API ───────────────────────────

class RateLimit(Exception):
    pass


class ServerBusy(Exception):
    """503 UNAVAILABLE — server quá tải, nên thử lại chứ KHÔNG phải hết hạn mức."""
    pass


class Truncated(Exception):
    """Model trả về nhưng bị cắt giữa chừng (finishReason != STOP)."""
    pass


DEFAULT_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def post_json(url, headers, body, timeout=300, retry_503=0):
    """Gọi API. retry_503 = số lần thử lại khi gặp 503 (quá tải tạm thời)."""
    last = None
    for attempt in range(retry_503 + 1):
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"),
            headers={**headers,
                     "User-Agent": DEFAULT_UA,
                     "Accept": "application/json, text/plain, */*",
                     "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            t = e.read().decode("utf-8", "replace")
            if e.code == 503:
                last = f"HTTP 503: {t[:200]}"
                if attempt < retry_503:
                    wait = min(60, 5 * (attempt + 1))
                    print(f"    [503 qua tai] thu lai sau {wait}s "
                          f"({attempt+1}/{retry_503})", flush=True)
                    time.sleep(wait)
                    continue
                raise ServerBusy(last)
            if e.code in (429, 403):
                raise RateLimit(f"HTTP {e.code}: {t[:2000]}")
            raise RuntimeError(f"HTTP {e.code}: {t[:400]}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = str(e)
            if attempt < retry_503:
                wait = min(60, 5 * (attempt + 1))
                print(f"    [mang loi] thu lai sau {wait}s "
                      f"({attempt+1}/{retry_503})", flush=True)
                time.sleep(wait)
                continue
            raise RuntimeError(f"lỗi mạng: {last}")
    raise RuntimeError(last or "unknown")


MODEL_FALLBACK = [
    "gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.5-flash",
    "gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
    "gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite",
]
QUOTA = ROOT / "translate" / "models_quota.json"


def models():
    raw = os.environ.get("GEMINI_MODELS")
    if raw:
        return [m.strip() for m in raw.split(",") if m.strip()]
    one = os.environ.get("GEMINI_MODEL")
    return [one] if one else MODEL_FALLBACK


def load_quota():
    if QUOTA.exists():
        try:
            q = json.loads(QUOTA.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        now = time.time()
        return {m: t for m, t in q.items() if t > now}
    return {}


def save_quota(q):
    QUOTA.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")


def reset_seconds(msg, default=3600):
    m = re.search(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"', msg)
    if m:
        return float(m.group(1))
    m = re.search(r"retry in (?:(\d+)h)?(?:(\d+)m)?([\d.]+)s", msg)
    if m:
        return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + float(m.group(3))
    return default


def _call_model(model, prompt, key, max_tok):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    d = post_json(url, {"x-goog-api-key": key},
                  {"contents": [{"parts": [{"text": prompt}]}],
                   "generationConfig": {"temperature": 0.2,
                                        "maxOutputTokens": max_tok}},
                  retry_503=int(os.environ.get("GEMINI_RETRY", "2")))
    cand = d.get("candidates", [{}])[0]
    fr = cand.get("finishReason")
    parts = cand.get("content", {}).get("parts", [])
    out = "".join(p.get("text", "") for p in parts)

    # ── KIỂM TRA BỊ CẮT ──
    # finishReason=MAX_TOKENS nghĩa là model bị ngắt giữa chừng.
    # Nếu không kiểm tra, bản dịch cắt cụt vẫn được ghi ra như hợp lệ.
    if fr and fr != "STOP":
        raise Truncated(f"finishReason={fr}, nhận {len(out)} ký tự "
                        f"(bị cắt, maxOutputTokens={max_tok})")
    if not out.strip():
        raise Truncated(f"finishReason={fr}, phản hồi rỗng")
    return out


def call_gemini(prompt):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("Thieu GEMINI_API_KEY. Tao file .env o f:\\taitruyen voi dong GEMINI_API_KEY=...")
    max_tok = int(os.environ.get("GEMINI_MAX_TOKENS", "65536"))

    quota = load_quota()
    now = time.time()
    cands = models()
    usable = [m for m in cands if quota.get(m, 0) <= now]
    if not usable:
        soon = min((quota.get(m, 0) for m in cands), default=0)
        raise RateLimit(
            f"tất cả model đã hết hạn mức (sớm nhất còn {max(0, soon - now) / 3600:.1f} giờ)")

    last = None
    for model in usable:
        try:
            return _call_model(model, prompt, key, max_tok)
        except RateLimit as e:
            secs = reset_seconds(str(e))
            quota[model] = time.time() + secs
            save_quota(quota)
            print(f"    [{model} het han muc, reset sau {secs / 3600:.1f} gio] "
                  f"chuyen model khac", flush=True)
            last = e
        except ServerBusy as e:
            print(f"    [{model} qua tai] chuyen model khac", flush=True)
            last = e
        except RuntimeError as e:
            print(f"    [{model}: {str(e)[:70]}] chuyen model khac", flush=True)
            last = e
    raise last or RuntimeError("không gọi được model nào")


def call_openai(prompt):
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    if not key:
        sys.exit("Thieu OPENAI_API_KEY trong .env")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    max_tok = int(os.environ.get("OPENAI_MAX_TOKENS", "16384"))
    d = post_json(f"{base}/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": model,
                   "messages": [{"role": "user", "content": prompt}],
                   "temperature": 0.2, "max_tokens": max_tok},
                  retry_503=int(os.environ.get("OPENAI_RETRY", "3")))
    ch = d["choices"][0]
    if ch.get("finish_reason") == "length":
        raise Truncated(f"finish_reason=length (bị cắt, max_tokens={max_tok})")
    out = ch["message"]["content"]
    if not out.strip():
        raise Truncated("phản hồi rỗng")
    return out


BACKENDS = {"gemini": call_gemini, "openai": call_openai}


# ─────────────────────────── prompt ───────────────────────────

SYSTEM = """Bạn là dịch giả văn học Trung Quốc -> Tiếng Việt, chuyên dịch tiểu thuyết hiện đại và cổ trang.

BẤT BIẾN KHÔNG ĐƯỢC PHÁ VỠ:

1. TÊN RIÊNG & XƯNG HÔ: tuân thủ tuyệt đối mục GLOSSARY bên dưới (tên nhân vật, địa danh, cách xưng hô giữa từng cặp). Không tự đặt tên, không đổi tên.
2. GIỮ NGUYÊN HÁN VIỆT cho tên nhân vật chưa có trong glossary — không bịa, không tự đặt.
3. KHÔNG tóm tắt, KHÔNG bịa thêm, KHÔNG bỏ chi tiết. Dịch đủ từng câu.
5. Giữ nguyên số, đơn vị tiền (1元 = 1 tệ), đơn vị đo. Số đếm luôn viết "nghìn" (hai nghìn cân, mười nghìn người); chỉ giữ "ngàn" trong các thành ngữ văn ngôn quen dùng: "ngàn dặm", "ngàn năm", "ngàn vàng".
6. Giữ giọng văn gốc: cổ trang dùng từ cổ ("kẻ tiểu nhân", "công tử"), hiện đại dùng từ đời thường. KHÔNG trẻ hóa, KHÔNG làm mềm, KHÔNG thêm cảm xúc.
7. ĐẠI TỪ THOẠI: dùng "mày/tao/tôi/cậu/anh/chị" theo quan hệ trong glossary. TUYỆT ĐỐI KHÔNG dùng "ngươi", "ta", "lão tử", "lão phu" trong lời thoại (trừ ca từ cổ/kinh kịch trích dẫn). KHÔNG dùng "ngài" trong thoại (trừ khi nói với giới thượng lưu thần tiên).
   (Quy ước xưng hô cụ thể cho từng cặp nhân vật nằm trong GLOSSARY — tuân thủ tuyệt đối.)

8. KIỂM DUYỆT: bản gốc bị website chặn chữ, in ra dấu "*" hoặc "[***]" thay cho một từ (VD: sát thủ cấp **, **[***] luật, một đêm **). TUYỆT ĐỐI không giữ dấu * trong bản dịch — phải đoán từ ngữ cảnh mà viết trọn nghĩa tiếng Việt, tự nhiên, không thêm ghi chú.
9. ĐỊNH DẠNG: thân bài là văn thuần, KHÔNG dùng cú pháp markdown (không #, không **, không in đậm), KHÔNG viết lại tiêu đề chương ở đầu hay giữa thân bài.

VĂN PHONG: câu văn tự nhiên, đúng tiếng Việt, không dịch máy từ chữ. Ví dụ:
- 说 → nói (tuỳ ngữ cảnh, có thể "bảo")
- 看着 → nhìn
- 苦笑 → cười khổ
- 连忙 → vội vàng
- 心里 → trong lòng

Nếu gặp tên riêng hoặc thuật ngữ CHƯA có trong glossary, dịch bằng Hán Việt và ghi thêm vào mục "THUẬT NGỮ MỚI" ở cuối bản dịch.

ĐỊNH DẠNG ĐẦU RA:
- Dịch nguyên văn.
- Nếu có thuật ngữ mới, thêm sau bản dịch, phân cách bằng dòng "=== THUẬT NGỮ MỚI ===" rồi liệt kê "Hán = Việt" mỗi dòng."""


def build_prompt(ch_no, title, text, glossary):
    return f"""{SYSTEM}

════════ GLOSSARY (tuân thủ tuyệt đối) ════════
{glossary}

════════════════════════════════════════
DỊCH CHƯƠNG {ch_no}: {title}
(Lưu ý: số chương phải là {ch_no}, không lấy số ghi trong tiêu đề Hán nếu khác.)
Văn bản gốc:
<<<{text}>>>
"""


def parse_extra(out):
    """Lấy phần thuật ngữ mới nếu có."""
    # model đôi khi viết biến thể: "=== THUẬT NGỮ MỚI ===",
    # "=== KHÔNG CÓ THUẬT NGỮ MỚI ===" -> tách bằng regex, không so chuỗi cứng
    m = re.search(r"={2,}[^\n]*THUẬT NGỮ[^\n]*={2,}", out, flags=re.I)
    if m:
        body, extra = out[:m.start()], out[m.end():]
        pairs = []
        for line in extra.strip().splitlines():
            line = line.strip().strip("-*").strip()
            if "=" in line:
                pairs.append(line)
        return body.strip(), pairs
    return out.strip(), []


# ─────────────────────────── tự kiểm ───────────────────────────

AUTO_FIX = [
    # (mẫu, thay thế) — sửa an toàn, không đổi nghĩa
    (r"\bVariation---?\s*", ""),
    (r"^\s*\d+\|\s*$\n?", ""),
    (r"\ufffd", ""),
    (r"\(\s*\*+\s*\)", ""),
    # model chép lại phân cách "=== THUẬT NGỮ ===" của prompt vào cuối bài
    (r"(?m)^={2,}[^=\n]*={2,}[^\n]*$[^\S\n]*\n?", ""),
]

# in đậm markdown model tự thêm, và dòng tiêu đề chương bị lặp lại giữa thân bài
MD_BOLD = re.compile(r"\*\*([^*\n]+)\*\*")
DUP_HEAD = re.compile(
    r"(?m)^[ \t]*\*{0,2}[ \t]*(?:CHƯƠNG|Chương)[ \t]+\d+[ \t]*[:：][^\n]*?\*{0,2}[ \t]*$")


def strip_markdown(t):
    t = DUP_HEAD.sub("", t)
    t = MD_BOLD.sub(r"\1", t)
    return re.sub(r"\n{3,}", "\n\n", t)

# bảng ràng buộc: trong bản dịch KHÔNG được xuất hiện (riêng từng truyện)
FORBID = {
    "baojian": ["秦风", "秦葭", "胡保国", "谢轩", "秦老板", "粮票", "烧饼", "废品",
                "户口", "哥哥", "妹妹", "咱们", "什么", "没有", "就是", "所以",
                "但是", "如果", "已经", "还是", "这样", "时候", "一个", "他们"],
    # tên riêng + thuật ngữ chính của truyện mới (đều phải dịch sang Hán Việt)
    "can_bao_chan_long": ["叶楚", "姜君瑶", "叶天成", "谢雨珊", "韩梦娟", "姜海云",
                           "皇甫诗月", "诸葛哲雅", "叶倾颜", "叶倾城", "敖颖", "敖光",
                           "龙镇山", "红莲", "李玄德", "白鹤真人", "姬德", "司徒弘远",
                           "楚九歌", "嬴惊鸿", "真凰体", "怨龙气", "入赘", "赘婿",
                           "药皇", "祖龙墓", "药神宫", "什么", "没有", "就是", "所以",
                           "但是", "如果", "已经", "还是", "这样", "时候", "一个", "他们"],
}


def forbid_list():
    return FORBID.get(BOOK, FORBID["baojian"])


def validate(vi, glossary):
    """Trả về danh sách lỗi. Lỗi tự sửa được → đã sửa trong chính `vi` (bytearray)."""
    errs = []
    for pat, rep in AUTO_FIX:
        vi, n = re.subn(pat, rep, vi, flags=re.M)
        if n:
            errs.append(f"sửa tự động: bỏ {n} marker thừa")

    ctrl = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", vi)
    if ctrl:
        errs.append(f"ký tự điều khiển hỏng: {len(ctrl)} chỗ")

    han = re.findall(r"[\u4e00-\u9fff]+", vi)
    for h in han:
        # so khop chuoi con, vi "秦风说" la mot token lien mach
        for f in forbid_list():
            if f in h:
                errs.append(f"Hán sót: {f} (trong '{h}', sai quy tắc glossary)")
                break
    if han:
        errs.append("Hán sót: " + " ".join(dict.fromkeys(han)))

    # xưng hô sai: "Anh ơi, con ..." / "Chú ơi, con ..."
    # KHONG dung \b truoc "anh": tieng Viet co dau (ơ, ạ) la ky tu khong phai
    # chu cai, nen Python coi "ơi," la mot "tu" va \b se khong khop.
    # "con" + danh tu (con ranh, con be, con cho...) la danh tu, khong phai xung ho
    DANH_TU_SAU_CON = re.compile(
        r"(?i)^\s+(?:ranh|be|nhỏ|trai|gái|người|vật|chó|mèo|chim|cá|rắn|dao|"
        r"đường|sông|thuyền|trâu|bò|ngựa|gà|vịt|kiến|sâu|mắt|tim|số|phần|dâu|rể|nuôi|"
        r"gấu|độc|của|út|trưởng|thứ|riêng|thơ|búp|"
        # tuc tu xuc danh: "trói con tiện nhân này lại" la loai tu, khong phai xung ho
        r"tiện|đĩ|dâm|khốn|khứ|"
        # dong vat: "con sói đầu đàn" la loai danh tu, khong phai xung ho
        r"sói|cáo|hoẵng|hươu|chồn|beo|báo|trăn|kỳ đà|khỉ|voi|sóc|nhím|"
        r"cừu|dê|nai|hoẵng|chồn|diều hâu|đại bàng|ưng|cắt|sáo|quạ|bồ câu|"
        r"tằm|ong|bướm|chuồn chuồn|tắc kè|rùa|ba ba|cá sấu)")
    for m in re.finditer(
            r"(?i)(?<![^\W\d_])(?:toi|anh|chu|bo|me|chau)\b[^.!?\n]{0,14}?\bcon\b(?![\wàáảãạăâêôơưý])",
            vi):
        if DANH_TU_SAU_CON.match(vi[m.end():]):
            continue
        # "bọn con"/"chúng con" là cách trẻ em xưng với người lớn, hợp lệ
        if re.search(r"(?i)(?:bọn|chúng)\s+con$", vi[:m.end()]):
            continue
        # "anh Hà Phong của con" / "anh hai con" / "anh con dẫn đầu":
        # trẻ con nói với người lớn về anh chị mình — sở hữu cách, không sai.
        if re.search(r"(?:\bcủa|\s(?:hai|ba|bốn|năm|lớn|cả|út|trưởng))\s+con$",
                     vi[:m.end()]):
            continue
        if re.search(r"(?i)(?:anh|chị|em|ông|bà|cô|dì|thầy|mợ)\s+con$", vi[:m.end()]):
            continue
        # quantifier đứng trước ("mấy con sói") -> classifier
        if re.search(r"(?i)(?:mấy|những|các|hai|ba|bốn|năm|sáu|bảy|tám|chín|một|hai|"
                     r"bao nhiêu|vài)\s+con\b", vi[max(0, m.start() - 12):m.end()]):
            continue
        errs.append(f"xưng 'con' sai: ...{m.group(0)}...")
        break

    if len(vi.strip()) < 300:
        errs.append("bản dịch quá ngắn — có thể bị cắt")

    if vi.count("“") != vi.count("”"):
        errs.append(f"ngoặc kép lệch: {vi.count('“')} mở / {vi.count('”')} đóng")

    if "*" in vi:
        m = re.search(r"[^\n]{0,60}\*[^\n]{0,60}", vi)
        errs.append(f"còn dấu kiểm duyệt/markdown '*': ...{m.group(0)}...")

    return errs


# ─────────────────── kiểm tra độ đầy đủ so với bản gốc ───────────────────

def count_units(t):
    """Đếm 'đơn vị nội dung': số đoạn + số dấu câu kết thúc.
    Dùng để so bản dịch với bản gốc mà không phụ thuộc độ dài chữ."""
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    return len(paras), len(re.findall(r"[。！？…”]", t))


def count_units_vi(t):
    """Đoạn + dấu câu theo chuẩn tiếng Việt (., ! ?, ", …)."""
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    marks = len(re.findall(r"[.!?…]|\"", t))
    return len(paras), marks


def _strip_cont(t):
    return re.sub(r"[\(（]\s*Còn tiếp[^\)）]*[\)）]\s*$", "", t, flags=re.I).strip()


def check_complete(src_text, vi_text):
    """Bản dịch có bị cắt cụt không? Trả về (ok, lý do).

    Nguyên lý: tiếng Việt cần NỘI DUNG tương đương bản gốc. Đoạn văn Hán
    thường dài hơn tiếng Việt ~1,5-2,2 lần, nhưng SỐ ĐOẠN và SỐ DẤU CÂU
    phải tương đương. Nếu bản dịch mất 40% đoạn -> chắc chắn bị cắt.
    """
    src_text = re.sub(r"[（(]\s*未完待续[。.]?\s*[）)]\s*$", "", src_text).strip()
    vi_text = _strip_cont(vi_text)
    sp, sq = count_units(src_text)
    dp, dq = count_units_vi(vi_text)
    if sp == 0:
        return True, ""

    # thiếu đoạn (nới ngưỡng: tiếng Việt hay gộp đoạn thoại)
    if dp < sp * 0.60:
        return False, f"thiếu đoạn ({dp}/{sp})"
    # thiếu dấu câu (mỗi đoạn Hán có ~1 dấu 。！？ hoặc ”)
    if sq and dq < sq * 0.45:
        return False, f"thiếu dấu câu ({dq}/{sq}) — có thể bị cắt"
    # đoạn cuối không kết thúc câu (chỉ xét khi bản gốc kết thúc bằng dấu câu)
    last = vi_text.strip().split("\n\n")[-1].strip()
    src_last = src_text.strip().split("\n\n")[-1].strip()
    src_closed = bool(re.search(r"[。！？…”』」）.!?]\s*$", src_last))
    if src_closed and last and last[-1] not in ".”\"!?！？…』」）)'":
        return False, "câu cuối không đóng dấu — bản dịch bị cắt giữa chừng"
    return True, ""


# ─────────────────────────── chính ───────────────────────────

def translate_chapter(n, s, chs, api, glossary):
    """Dich 1 chuong, tra ve dict ket qua. Chay duoc trong thread."""
    raw_title = chs[n].split("_", 1)[1].rsplit(".", 1)[0]
    text = clean((SRC / chs[n]).read_text(encoding="utf-8", errors="replace"))
    # nguồn chen "宝鉴612", "飘天文学getmode;...", "(未完待续)ps：..." -> gỡ rác
    src_ref = dedup_repeats(strip_src_junk(text))
    # prompt cần đoạn văn rõ: nguồn nén cả chương thành một dòng thì tách lại
    text = break_long_lines(src_ref)
    if not text.strip():
        return {"status": "skip", "n": n, "s": s, "title": raw_title}

    raw = api(build_prompt(s, raw_title, text, glossary)
              + f"\n\n(Mã tác vụ: {time.time_ns()})")
    vi, terms = parse_extra(raw)
    vi = strip_heading(vi, raw_title)
    vi = fix_quotes(vi)
    vi = normalize_address(vi)
    vi = _strip_cont(vi)
    vi = strip_markdown(vi)

    complete, why = check_complete(src_ref, vi)
    if not complete:
        return {"status": "cut", "n": n, "s": s, "title": raw_title,
                "vi": vi, "why": why, "terms": terms}

    errs = validate(vi, glossary)
    if errs:
        return {"status": "invalid", "n": n, "s": s, "title": raw_title,
                "vi": vi, "errs": errs, "terms": terms}

    return {"status": "ok", "n": n, "s": s, "title": raw_title,
            "vi": vi, "terms": terms}


def main():
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=os.environ.get("BOOK", "baojian"),
                    choices=sorted(BOOKS), help="truyen can dich")
    ap.add_argument("--from", dest="lo", type=int, default=1)
    ap.add_argument("--to", dest="hi", type=int, default=0,
                    help="0 = den chuong cuoi cung")
    ap.add_argument("--limit", type=int, default=0, help="so chuong toi da trong lan chay nay")
    ap.add_argument("--backend", default=os.environ.get("BACKEND", "gemini"))
    ap.add_argument("--reset", action="store_true", help="dich lai ca nhung chuong da co")
    ap.add_argument("--retry", action="store_true", help="dich lai nhung chuong bi loi")
    ap.add_argument("--workers", type=int, default=int(os.environ.get("WORKERS", "4")),
                    help="so chuong dich song song")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    set_book(a.book)

    OUT.mkdir(parents=True, exist_ok=True)
    st = load_state()
    chs = all_chapters()
    if a.hi <= 0:
        a.hi = max(chs) if chs else a.lo

    if a.status:
        have = len(list(OUT.glob("*.md")))
        print(f"Da dich: {have} chuong  | con lai: {max(0, a.hi - have)}")
        if st["new_terms"]:
            print("Thuật ngữ mới:", len(st["new_terms"]))
        if st["failed"]:
            print("Lỗi:", len(st["failed"]), st["failed"][:10])
        return

    if a.reset:
        for f in OUT.glob("*.md"):
            f.unlink()
        st = {"done": [], "failed": [], "new_terms": [], "quota_hits": 0}
        print("Đã xoá toàn bộ bản dịch cũ.")

    cmap = load_chapter_map()
    todo = []
    notes_skipped = 0
    for n in range(a.lo, a.hi + 1):
        if n not in chs:
            continue
        row = cmap.get(str(n))
        if row is not None and (row.get("note") or not row.get("story")):
            notes_skipped += 1
            continue
        s = row["story"] if row else n
        if a.retry:
            if s not in st["failed"] and list(OUT.glob(f"{s:04d}_*.md")):
                continue
        else:
            if s in st["failed"] or list(OUT.glob(f"{s:04d}_*.md")):
                continue
        todo.append((n, s))
    if a.limit:
        todo = todo[:a.limit]

    api = BACKENDS[a.backend]
    glossary = GLOSSARY.read_text(encoding="utf-8")

    if not todo:
        print("Khong co gi de dich.")
        return

    titles = ensure_titles(todo, chs, api, cmap)

    workers = max(1, a.workers)
    print(f"Backend: {a.backend} | dich {len(todo)} chuong "
          f"(file {todo[0][0]}..{todo[-1][0]}, truyen {todo[0][1]}..{todo[-1][1]}), "
          f"bo qua {notes_skipped} file ghi chu | {workers} luong", flush=True)
    ok = fail = skip = 0
    t0 = time.time()
    finished = 0

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(translate_chapter, n, s, chs, api, glossary): (n, s)
                for n, s in todo}
        for fut in as_completed(futs):
            n, s = futs[fut]
            finished += 1
            try:
                r = fut.result()
            except RateLimit as e:
                st["quota_hits"] += 1
                save_state(st)
                print(f"\nHET HAN MUC tai chuong {s:04d} (file {n}): {e}", flush=True)
                print(f"Da dich {ok} chuong trong lan nay. State da luu.", flush=True)
                for f in futs:
                    f.cancel()
                break
            except ServerBusy as e:
                print(f"[{finished}/{len(todo)}] SERVER QUA TAI {s:04d} (file {n})", flush=True)
                mark_failed(st, s)
                fail += 1
                continue
            except Truncated as e:
                print(f"[{finished}/{len(todo)}] BI CAT {s:04d} (file {n}): {e}", flush=True)
                mark_failed(st, s)
                fail += 1
                (OUT / f"_{s:04d}_cat.md").write_text(
                    f"<!-- chuong {s:04d} | BI CAT: {e} -->\n", encoding="utf-8")
                continue
            except Exception as e:
                mark_failed(st, s)
                fail += 1
                print(f"[{finished}/{len(todo)}] LOI {s:04d} (file {n}): {str(e)[:120]}", flush=True)
                continue

            status = r["status"]
            raw_title = r["title"]
            dst = OUT / f"{s:04d}_{raw_title}.md"

            if status == "skip":
                skip += 1
                continue

            if status == "cut":
                mark_failed(st, s)
                fail += 1
                print(f"[{finished}/{len(todo)}] BI CAT {s:04d} (file {n}): {r['why']}", flush=True)
                (OUT / f"_{s:04d}_cat.md").write_text(
                    f"<!-- chuong {s:04d} | BI CAT: {r['why']} -->\n\n{r['vi']}\n",
                    encoding="utf-8")
                save_state(st)
                continue

            if status == "invalid":
                mark_failed(st, s)
                fail += 1
                print(f"[{finished}/{len(todo)}] KIEM THU FAIL {s:04d} (file {n}): {r['errs'][0]}", flush=True)
                if not r["errs"][0].startswith("sửa tự động"):
                    (OUT / f"_{s:04d}_nhap.md").write_text(
                        f"<!-- chuong {s:04d} | LOI: {'; '.join(r['errs'][:5])} -->\n\n{r['vi']}\n",
                        encoding="utf-8")
                save_state(st)
                continue

            hdr = f"<!-- chuong {s:04d} | {raw_title} | dich boi AI + glossary -->\n\n"
            body = r["vi"].rstrip()
            if not body.endswith("(Còn tiếp)"):
                body += "\n\n(Còn tiếp)"
            if s in titles:
                content = hdr + f"# {titles[s]}\n\n" + body + "\n"
            else:
                content = hdr + body + "\n"
            dst.write_text(content, encoding="utf-8")
            for d in OUT.glob(f"_{s:04d}_*.md"):
                d.unlink()
            if r["terms"]:
                for t in r["terms"]:
                    if t not in st["new_terms"]:
                        st["new_terms"].append(t)
                NOTES.write_text("\n".join(st["new_terms"]), encoding="utf-8")
            if s in st["failed"]:
                st["failed"].remove(s)
            if s not in st["done"]:
                st["done"].append(s)
            ok += 1
            save_state(st)
            el = time.time() - t0
            safe_title = raw_title[:22].encode('utf-8', errors='replace').decode('utf-8')
            print(f"[{finished}/{len(todo)}] OK  {s:04d} (file {n})  "
                  f"({el/finished:.1f}s/chuong, total {el/60:.1f} phut)", flush=True)

    save_state(st)
    print(f"\n=== Xong: OK={ok}  Loi={fail}  Bo qua={skip} ===")
    if st["failed"]:
        print("Danh sách lỗi:", sorted(set(st["failed"])))


if __name__ == "__main__":
    main()