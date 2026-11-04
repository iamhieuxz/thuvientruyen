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
    "quan_dao_chi_dien": {
        "src": "quan-dao-chi-dien",
        "out": "quan_dao_chi_dien_vi",
        "glossary": "glossary_quan_dao_chi_dien.txt",
        "notes": "notes_quan_dao_chi_dien.txt",
        "state": "state_quan_dao_chi_dien.json",
        "titles": "titles_quan_dao_chi_dien.json",
        "chapter_map": "",
    },
    "khai_cuc_dinh_chuc": {
        "src": "khai-cuc-dinh-chuc",
        "out": "khai_cuc_dinh_chuc_vi",
        "glossary": "glossary_khai_cuc_dinh_chuc.txt",
        "notes": "notes_khai_cuc_dinh_chuc.txt",
        "state": "state_khai_cuc_dinh_chuc.json",
        "titles": "titles_khai_cuc_dinh_chuc.json",
        "chapter_map": "",
    },
    "cao_nhi_phan_khoa": {
        "src": "cao-nhi-phan-khoa",
        "out": "cao_nhi_phan_khoa_vi",
        "glossary": "glossary_cao_nhi_phan_khoa.txt",
        "notes": "notes_cao_nhi_phan_khoa.txt",
        "state": "state_cao_nhi_phan_khoa.json",
        "titles": "titles_cao_nhi_phan_khoa.json",
        "chapter_map": "",
    },
    # 重生之财源滚滚 — nguon da dung lai tu 1733 trang HTML, chuong nam trong _final/
    "trong_sinh_tai_nguyen": {
        "src": "trong-sinh-tai-nguyen-cun-cun/_final",
        "out": "trong_sinh_tai_nguyen_vi",
        "glossary": "glossary_trong_sinh_tai_nguyen.txt",
        "notes": "notes_trong_sinh_tai_nguyen.txt",
        "state": "state_trong_sinh_tai_nguyen.json",
        "titles": "titles_trong_sinh_tai_nguyen.json",
        "chapter_map": "",
        "clean_tail_notes": True,   # nguon co ~164 chuong dinh ghi chu tac gia cuoi chuong
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


def strip_tail_notes(text):
    """Bỏ ghi chú tác giả ở CUỐI chương (cảm ơn打赏, 求月票, 加更, lời tác giả).

    Chỉ bật cho truyện khai báo `clean_tail_notes` trong BOOKS — đây là văn bản của
    tác giả, không phải nội dung truyện, mà máy đọc vẫn đọc thành tiếng.
    Chỉ xét 4 đoạn cuối và chỉ cắt khi đoạn đó NGẮN và mở đầu bằng từ khoá rõ ràng.
    """
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paras:
        return text
    START = ("感谢", "求月票", "求推荐", "求订阅", "求收藏", "求打赏", "PS：", "PS:",
             "ps：", "ps:", "（求", "(求", "抱歉", "码字", "加更", "新书期", "本章完")
    for _ in range(4):
        if not paras:
            break
        last = paras[-1]
        if len(last) > 260 or not last.startswith(START):
            break
        paras.pop()
    return "\n\n".join(paras).strip()


def prepare_src(text, book=None):
    """Chuẩn hoá bản gốc giống hệt nhau ở dich.py và check.py.

    Thứ tự: clean -> strip_src_junk -> strip_tail_notes (nếu truyện bật) -> dedup.
    Dùng chung để `check_complete` so cùng một bản tham chiếu.
    """
    t = dedup_repeats(strip_src_junk(clean(text)))
    if BOOKS.get(book or BOOK, {}).get("clean_tail_notes"):
        t = strip_tail_notes(t)
    return t


def dedup_repeats(text):
    """Nguồn lỗi scraper: cùng một chương bị lặp 2-4 lần liên tiếp."""
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
- TUYỆT ĐỐI không dùng "ngươi", "ta", "lão tử", "lão phu", "ngài" trong tiêu đề; đổi thành "cậu", "bạn", "anh", "ông".
- Không để ký tự Hán, không để ngoặc 《》, chỉ dùng ngoặc kép “ ” nếu cần.
- Chỉ xuất đúng các dòng kết quả, không thêm lời giải thích.

{lines}"""
        try:
            raw = api(prompt + f"\n\n(Mã tác vụ: {time.time_ns()})")
        except (RateLimit, ServerBusy, Truncated, RuntimeError) as e:
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


def post_json(url, headers, body, timeout=300, retry_503=0, retry_429=0):
    """Gọi API. retry_503 = số lần thử lại khi gặp 503 (quá tải tạm thời).
    retry_429 = số lần nghỉ-rồi-thử-lại khi gặp 429 (rate limit tạm thời, KHÔNG phải hết hạn mức)."""
    last = None
    for attempt in range(max(retry_503, retry_429) + 1):
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
                # 429 = rate limit tạm thời -> nghỉ rồi tiếp, không dừng runner
                if e.code == 429 and attempt < retry_429:
                    wait = min(60, 15 + 10 * attempt)
                    print(f"    [429 rate limit] nghi {wait}s roi thu lai "
                          f"({attempt+1}/{retry_429})", flush=True)
                    time.sleep(wait)
                    continue
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
    # Neu nguoi dung dan ca duong dan endpoint, cat phan du de khong bi noi 2 lan
    base = re.sub(r"/chat/completions/?$", "", base)
    if not key:
        sys.exit("Thieu OPENAI_API_KEY trong .env")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    max_tok = int(os.environ.get("OPENAI_MAX_TOKENS", "16384"))
    # Provider doi khi tra HTTP 200 nhung body la loi (khong co "choices").
    # Truoc day cho nay crash KeyError -> ca lan chay bi huy. Gio thu lai vai lan.
    d = None
    for attempt in range(3):
        d = post_json(f"{base}/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.2, "max_tokens": max_tok},
                      retry_503=int(os.environ.get("OPENAI_RETRY", "3")),
                      retry_429=int(os.environ.get("OPENAI_RETRY_429", "6")))
        if "choices" in d:
            break
        print(f"    [phan hoi la, thieu 'choices'] thu lai "
              f"({attempt + 1}/3): {json.dumps(d, ensure_ascii=False)[:120]}", flush=True)
        time.sleep(min(30, 5 * (attempt + 1)))
    if not d or "choices" not in d:
        raise RuntimeError(
            f"phan hoi khong co 'choices': {json.dumps(d, ensure_ascii=False)[:300]}")
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
9b. TOÀN BỘ BẢN DỊCH PHẢI LÀ TIẾNG VIỆT: TUYỆT ĐỐI không để bất kỳ ký tự Hán nào trong thân bài. Gặp từ chưa biết thì dịch nghĩa hoặc dùng Hán Việt, KHÔNG được chép nguyên chữ Hán, KHÔNG đặt chữ Hán cạnh từ tiếng Việt.
10. KHÔNG DÙNG DẤU PHÂN CÁCH GIỮA CÁC KHỐI: đây là bản đọc bằng máy (sách nói), mọi ký hiệu như ---, ***, ===, ~~~, ###, ..., •, ※, ◆, ◇, ■, ▲, ●, — sẽ bị đọc thành tiếng. Chỉ ngăn cách đoạn bằng MỘT dòng trống, không chèn dòng ký hiệu, không gạch ngang, không dấu chấm lửng trang trí.
10b. KHÔNG BAO GIỜ để một dòng riêng chỉ gồm dấu chấm lửng (… hoặc ...) hay gạch nối (—, –, -): module đọc sẽ lỗi. Dấu lửng chỉ dùng BÊN TRONG câu thoại/kể; muốn ngắt cảnh thì dùng một dòng trống.
11. ĐOẠN NGẮN (bắt buộc, vì đây là sách nói): KHÔNG viết đoạn nào dài quá ~180 ký tự (khoảng 2 câu). Đoạn dài hơn phải tách thành nhiều đoạn, mỗi đoạn ngăn bằng MỘT dòng trống. Lý do: máy đọc phải render trọn một đoạn mới phát được, đoạn dài khiến người nghe phải chờ lâu và mất mạch truyện. Ưu tiên tách ở ranh giới câu; nếu tách giữa lời thoại thì mở lại ngoặc kép “ ở đoạn sau và đóng ” ở đoạn trước. KHÔNG gộp nhiều câu thoại vào một đoạn.

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

NHẮC LẠI: đầu ra 100% chữ Quốc ngữ, không một ký tự Hán nào — kể cả từ đơn, thành ngữ, tục ngữ,
trợ từ cuối câu. Nếu bí từ: dùng Hán Việt bằng chữ Latinh, hoặc lược bỏ từ đó cho câu trôi chảy —
TUYỆT ĐỐI không chèn chữ Hán vào câu.
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


# dong chi gom ky hieu phan cach -> sach noi se doc thanh tieng (luat du an)
SEP_LINE = re.compile(
    r"^\s*(?:[-=*_~#·•※◆◇■□▲△●○—–]{2,}|…+|[.．]{2,}|[-–—])\s*$")


def sanitize_seps(t):
    """Bo dong ky hieu phan cach, giu doan cach bang mot dong trong."""
    t = "\n".join("" if SEP_LINE.match(l) else l for l in t.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", t).strip()


# dau cau Han con sot -> ASCII (check.py bao [W] neu con （）【】)
HAN_PUNCT = str.maketrans({"（": "(", "）": ")", "【": "(", "】": ")"})


def normalize_punct(t):
    t = t.translate(HAN_PUNCT)
    # khoang trang truoc dau cau (check.py bao [W])
    return re.sub(r"[ \t]+([.,!?;:…])", r"\1", t)


# ten bi go sai dau / bi model tu che bien the -> ep ve dang chuan cua glossary.
# Chi sua dung chuoi ten, khong dung regex, nen an toan.
NAMES_FIX = {
    "cao_nhi_phan_khoa": {
        "Chu Thân": "Chu Thần",
        "Trương Kha": "Trương Nhã",
        "Lưu Khải": "Lý Khải",
    },
}


def fix_names(t):
    for a, b in NAMES_FIX.get(BOOK, {}).items():
        t = t.replace(a, b)
    return t


# ─────────── chia doan dai cho TTS (luat du an: khong doan nao qua dai) ───────────
# Model TTS render tron mot doan thanh mot file am thanh; doan cang dai thi nguoi
# nghe cang phai cho lau moi nghe duoc, mat mach truyen. Vi vay cat doan dai
# thanh nhieu doan ngan theo ranh gioi cau.
MAX_PARA = int(os.environ.get("MAX_PARA", "180"))   # ky tu toi da moi doan
MIN_PARA = 40                                        # tranh manh vun qua ngan

SENT = re.compile(r"[^.!?…]*[.!?…]+[”]?|[^.!?…]+$")


def _atomic(s, max_chars):
    """Tach 1 cau qua dai thanh cac manh <= max_chars.

    Ba muc: cat tai dau phay -> cat tai khoang trang -> cat cung (rat hiem).
    Thieu muc 2/3 thi cau dai khong co dau phay se khong bao gio duoc cat,
    sinh doan > nguong va lam hong nhip doc sach noi.
    """
    if len(s) <= max_chars:
        return [s]

    def pack(words, seps):
        out, buf = [], ""
        for i, w in enumerate(words):
            cand = (buf + " " + w).strip() if buf else w
            if buf and len(cand) > max_chars:
                out.append(buf + (seps[i - 1] if i - 1 < len(seps) else ""))
                buf = w
            else:
                buf = cand
        if buf:
            out.append(buf)
        return out

    # muc 1: theo dau phay
    parts = re.split(r"(?<=,)\s+", s)
    pieces, buf = [], ""
    for p in parts:
        cand = (buf + " " + p).strip() if buf else p
        if buf and len(cand) > max_chars:
            pieces.append(buf)
            buf = p
        else:
            buf = cand
    if buf:
        pieces.append(buf)

    # muc 2: manh nao van qua dai -> cat theo khoang trang
    final = []
    for pc in pieces:
        if len(pc) <= max_chars:
            final.append(pc)
            continue
        words = pc.split(" ")
        sub, buf = [], ""
        for w in words:
            cand = (buf + " " + w) if buf else w
            if buf and len(cand) > max_chars:
                sub.append(buf)
                buf = w
            else:
                buf = cand
        if buf:
            sub.append(buf)
        final.extend(x for x in sub if x)

    # muc 3: tu don le dai hon nguong (ten URL...) -> cat cung
    out = []
    for pc in final:
        while len(pc) > max_chars:
            out.append(pc[:max_chars])
            pc = pc[max_chars:]
        if pc:
            out.append(pc)
    return out or [s]


def _split_one(src, max_chars, min_chars):
    """Cat 1 doan dai thanh cac doan <= max_chars tai ranh gioi cau."""
    units = []
    for s in SENT.findall(src):
        s = s.strip()
        if s:
            units.extend(_atomic(s, max_chars))
    if not units:
        return [src]

    chunks, buf = [], ""
    for s in units:
        cand = (buf + " " + s).strip() if buf else s
        if buf and len(cand) > max_chars:
            chunks.append(buf)
            buf = s
        else:
            buf = cand
    if buf:
        chunks.append(buf)

    # gop manh cuoi qua ngan vao doan truoc — nhung KHONG duoc vuot max_chars;
    # vuot thi de nguyen (doan ngan con hon doan dai lam hong nhip doc sach noi)
    if len(chunks) > 1 and len(chunks[-1]) < min_chars:
        merged = (chunks[-2] + " " + chunks[-1]).strip()
        if len(merged) <= max_chars:
            chunks[-2] = merged
            chunks.pop()

    # cat giua loi thoai -> dong ngoac kep cho tung doan, giu can bang toan bai
    res, open_q = [], False
    for i, c in enumerate(chunks):
        if open_q:
            c = "“" + c
        bal = c.count("“") - c.count("”")
        if bal > 0 and i < len(chunks) - 1:
            c = c.rstrip() + "”"
            open_q = True
        else:
            open_q = False
        res.append(c)

    # sau khi them ngoac kep co the vuot vai ky tu -> cat lai tai dau phay
    final = []
    for c in res:
        if len(c) <= max_chars:
            final.append(c)
            continue
        room = max_chars - 2          # chua cho 1 cap ngoac kep neu phai mo lai
        pieces = _atomic(c, room)
        if len(pieces) <= 1:
            final.append(c)
            continue
        for j, pc in enumerate(pieces):
            if j:
                pc = "“" + pc
            if j < len(pieces) - 1:
                pc = pc.rstrip() + "”"
            final.append(pc)
    return final


def split_long_paras(t, max_chars=None, min_chars=MIN_PARA):
    """Khong de doan nao dai qua max_chars (sach noi: render lau, mat mach)."""
    max_chars = max_chars or MAX_PARA
    out = []
    for par in re.split(r"\n\s*\n", t):
        s = par.strip()
        if not s:
            continue
        if len(s) <= max_chars or s.startswith("<!--") or s.startswith("#"):
            out.append(s)
            continue
        out.extend(_split_one(s, max_chars, min_chars))
    return "\n\n".join(out)


def join_dialogue_verses(t, max_chars=None):
    """Gop lai 2 kieu doan bi cat vun (sach noi doc bi ngat):

    1. Cau dan ket thuc bang ':' roi doan thoai ngay sau -> gop neu vua.
    2. Kho tho / loi bai hat dang trong ngoac kep chua dong -> gop cac doan
       lien tiep thanh kho <= max_chars cho den khi dong ngoac.

    Bat buoc chay TRUOC split_long_paras: gop xong moi cat lai theo gioi han,
    nho vay khong bao gio sinh doan dai hon gioi han.
    """
    max_chars = max_chars or MAX_PARA
    pars = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]

    # 1) cau dan + thoai
    step1, i = [], 0
    while i < len(pars):
        p = pars[i]
        if (p.endswith(":") and i + 1 < len(pars)
                and pars[i + 1].startswith("“")
                and len(p + " " + pars[i + 1]) <= max_chars):
            step1.append(p + " " + pars[i + 1])
            i += 2
            continue
        step1.append(p)
        i += 1

    # 2) kho tho: doan mo ngoac kep ma chua dong
    step2, buf = [], []
    for s in step1:
        if buf:
            buf.append(s)
            if " ".join(buf).count("”") > " ".join(buf).count("“"):
                step2.append(" ".join(buf))
                buf = []
            continue
        opened = s.count("“") > s.count("”")
        if opened and len(s) <= 100:
            buf = [s]
            continue
        step2.append(s)
    if buf:
        step2.append(" ".join(buf))

    return "\n\n".join(step2)


HAN_CH = re.compile(r"[\u4e00-\u9fff]")
VI_CH = re.compile(r"[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]")


def drop_source_echo(t):
    """Bỏ đoạn model chép nguyên bản Hán (thường nằm ngay trước bản dịch của nó)."""
    out = []
    for par in re.split(r"\n\s*\n", t):
        s = par.strip()
        if not s:
            continue
        han = len(HAN_CH.findall(s))
        letters = len(re.findall(r"[^\W\d_]", s))
        if han >= 4 and han >= letters * 0.6 and not VI_CH.search(s):
            continue
        out.append(s)
    return "\n\n".join(out)

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
    "khai_cuc_dinh_chuc": ["杨东", "尹铁军", "苏沐芸", "林耀东", "韩雯", "田光汉",
                            "关九九", "周慧", "吴建材", "林良铭", "关木山", "孙秀芬",
                            "卫崇虎", "侯东来", "徐允才", "孙进明", "肖建国", "李正义",
                            "李富海", "苏玉良", "陈国民", "赵达功", "巩红", "燕实忠",
                            "蒋震", "郑广成", "童长河", "李臣", "楚利", "武新开",
                            "侯勇", "魏立明", "马树立", "姜红阳", "顾晨", "邹晨",
                            "杜玉香", "吴慧", "灵云", "吉江", "龙城", "市委", "省委", "纪委",
                            "双规", "借调", "停职",
                            "市政办", "市纪委", "综合科", "秘书长", "副秘书长", "副市长",
                            "什么", "没有", "就是", "所以", "但是", "如果", "已经",
                            "还是", "这样", "时候", "一个", "他们"],
    "cao_nhi_phan_khoa": ["顾屿", "苏念", "李凯", "李猴子", "张慧", "顾建国", "赵文博",
                          "阎王", "陈浩", "王雅", "李静", "张伟", "莉莉", "凯文",
                          "锦城", "七中", "长顺街", "望江路", "惠民", "极速空间",
                          "知乎", "邀请码", "文科", "理科", "分科", "降维打击",
                          "内容变现", "阿拉伯之春", "颜色革命", "分封制", "连锁加盟",
                          "念语", "第一桶金", "学霸", "校花", "教务处", "文理分科",
                          "张卫东", "陈律师", "观海听涛", "天涯", "鹤鸣", "青羊",
                          "林溪", "王哲", "王梓萌", "刘雨菲", "储晨", "王金龙",
                          "灯塔", "金牛万达", "太升南路", "浣花溪", "双流", "别踩白块儿",
                          "苏弘道", "苏半城", "星火", "罗文", "顾超", "香格里拉",
                          "余大嘴", "刘强", "柳云", "鼎食人家", "今日热点", "张雅",
                          "王莉莉", "西红柿", "极光", "九章", "嘉陵江",
                          "徐静", "斗鱼", "海思", "不言", "安倍",
                          "什么", "没有", "就是", "所以", "但是", "如果", "已经",
                          "还是", "这样", "时候", "一个", "他们"],
    "trong_sinh_tai_nguyen": ["李东", "沈茜", "秦雨涵", "袁雪", "许圣哲", "胡小蕊",
                              "孙涛", "袁成道", "陈瑞", "张岚玉", "杜安民", "沈雪华",
                              "李程远", "曹芳", "李程辉", "陈国华", "方青菲", "王杰",
                              "陈悦", "魏源", "孟启平", "白素", "李铁", "冯劲松",
                              "远方", "东宇", "马昀", "马华腾", "李彦红", "柳强东",
                              "张进东", "滕迅", "掏宝", "阿里", "百度", "国梅", "苏果",
                              "华闰", "大润发", "家乐福", "沃尔玛", "东平", "平川",
                              "江北", "青阳", "临安", "京城", "香江", "羊城", "蜀都",
                              "京大", "江大", "东子", "东哥", "炮哥", "李大炮",
                              "什么", "没有", "就是", "所以", "但是", "如果", "已经",
                              "还是", "这样", "时候", "一个", "他们"],
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
        r"(?i)^\s*[“\"'‘]*\s*(?:ranh|be|bé|nhỏ|trai|gái|người|vật|chó|mèo|chim|cá|rắn|dao|"
        r"đường|sông|thuyền|trâu|bò|ngựa|gà|vịt|kiến|sâu|mắt|tim|số|phần|dâu|rể|nuôi|"
        r"gấu|độc|của|út|trưởng|thứ|riêng|thơ|búp|"
        # tuc tu xuc danh: "trói con tiện nhân này lại" la loai tu, khong phai xung ho
        r"tiện|đĩ|dâm|khốn|khứ|"
        # dong vat: "con sói đầu đàn" la loai danh tu, khong phai xung ho
        r"sói|cáo|hoẵng|hươu|chồn|beo|báo|trăn|kỳ đà|khỉ|voi|sóc|nhím|"
        r"cừu|dê|nai|hoẵng|chồn|diều hâu|đại bàng|ưng|cắt|sáo|quạ|bồ câu|"
        r"tằm|ong|bướm|chuồn chuồn|tắc kè|rùa|ba ba|cá sấu|"
        r"quái vật|"
        # do vat co danh tu loai "con": con tro (cursor), con chip, con quay...
        # cao_nhi_phan_khoa noi ve may tinh/choi game -> "con trỏ" bi bao sai
        r"trỏ|chip|lăn|quay|lắc|xúc xắc|rối|thoi|tem|bài|dấu|ốc|vít|"
        r"chuột|bàn|phím|ống|cuộn|sạc|pin|"
        r"phố|ngõ|hẻm|suối|kênh|đò|rạch|lạch|mương|bạc|nợ|tàu|xe|thuyền)")
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
        # giới từ / copula đứng trước ("về con", "là con") -> "con" là con cái, không phải tự xưng
        if re.search(r"(?i)(?:về|cho|với|của|vì|đến|ở|lo|làm|thương|nhớ|là|vốn|thành|như)\s+con$",
                     vi[:m.end()]):
            continue
        # động từ nhận "con" làm tân ngữ ("ép con", "bắt con", "dạy con"):
        # người lớn nói với nhau về ĐỨA CON, không phải tự xưng.
        if re.search(r"(?i)(?:ép|bắt|mắng|chửi|dạy|nuôi|chiều|đánh|giúp|khen|dỗ|"
                     r"thấy|gọi|đón|đưa|giữ|để|thả|theo|kệ|đãi|bế)\s+con$", vi[:m.end()]):
            continue
        # cụm danh từ cố định: "công ty con" (công ty con = subsidiary), "con cưng"...
        if re.search(r"(?i)(?:công ty|cửa hàng|chi nhánh|thương hiệu|nhãn hàng)\s+con$",
                     vi[:m.end()]):
            continue
        # trẻ con nói với cha mẹ: "Mẹ nói xem, con nên..." là đúng
        if re.search(r"(?i)\b(?:mẹ|bố|ba|má|u|bầm|thầy|cô|ông|bà)\b[^.!?\n]{0,20}$",
                     vi[:m.start()]):
            continue
        # quantifier đứng trước ("mấy con sói") -> classifier
        if re.search(r"(?i)(?:mấy|những|các|hai|ba|bốn|năm|sáu|bảy|tám|chín|một|hai|"
                     r"bao nhiêu|vài|đứa)\s+con\b", vi[max(0, m.start() - 12):m.end()]):
            continue
        # "trẻ con" / "trò trẻ con" / "con nít" -> danh từ, không phải tự xưng
        if re.search(r"(?i)(?:trẻ|nhỏ|nít|dại|nhóc|to)\s+con$", vi[:m.end()]):
            continue
        errs.append(f"xưng 'con' sai: ...{m.group(0)}...")
        break

    if len(vi.strip()) < 300:
        errs.append("bản dịch quá ngắn — có thể bị cắt")

    if vi.count("“") != vi.count("”"):
        errs.append(f"ngoặc kép lệch: {vi.count('“')} mở / {vi.count('”')} đóng")

    if "*" in vi:
        # cho phep cac ky hieu ky thuat hop le: "A*" (A-star pathfinding),
        # "C++ /*...*/" khong xuat hien trong the loai nay. Ngoai ra giu lenh loi.
        vi_no_tech = re.sub(r"\b[A-Z]\*(?![a-zA-Z])", "", vi)  # A* / C* ...
        if "*" in vi_no_tech:
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

def translate_text(s, raw_title, text, glossary, api, parts=1):
    """Dịch 1 chương; parts>1 thì chia phần — model bám glossary tốt hơn, ít sót Hán."""
    if parts <= 1:
        out, terms = parse_extra(api(build_prompt(s, raw_title, text, glossary)
                                     + f"\n\n(Mã tác vụ: {time.time_ns()})"))
        return strip_heading(out, raw_title), terms
    paras = [p for p in text.split("\n") if p.strip()]
    size = max(1, (len(paras) + parts - 1) // parts)
    groups = [paras[i:i + size] for i in range(0, len(paras), size)]
    outs, terms = [], []
    for i, g in enumerate(groups, 1):
        out, t = parse_extra(api(build_prompt(
            s, "%s (phần %d/%d)" % (raw_title, i, len(groups)), "\n".join(g), glossary)
            + f"\n\n(Mã tác vụ: {time.time_ns()})"))
        outs.append(strip_heading(out, raw_title))
        terms += t
    return "\n\n".join(x for x in outs if x.strip()), terms


def translate_chapter(n, s, chs, api, glossary, parts=1):
    """Dich 1 chuong, tra ve dict ket qua. Chay duoc trong thread."""
    raw_title = chs[n].split("_", 1)[1].rsplit(".", 1)[0]
    text = clean((SRC / chs[n]).read_text(encoding="utf-8", errors="replace"))
    # nguồn chen "宝鉴612", "飘天文学getmode;...", "(未完待续)ps：..." -> gỡ rác
    src_ref = prepare_src(text)
    # prompt cần đoạn văn rõ: nguồn nén cả chương thành một dòng thì tách lại
    text = break_long_lines(src_ref)
    if not text.strip():
        return {"status": "skip", "n": n, "s": s, "title": raw_title}

    # glossary theo CHUONG: luat luon co, muc tu loc theo noi dung chuong
    gl = load_glossary_for_chapter(s, src_ref)
    vi, terms = translate_text(s, raw_title, text, gl, api, parts)
    vi = fix_quotes(vi)
    vi = normalize_address(vi)
    vi = _strip_cont(vi)
    vi = strip_markdown(vi)
    vi = drop_source_echo(vi)
    vi = normalize_punct(vi)
    vi = fix_names(vi)
    vi = sanitize_seps(vi)
    vi = join_dialogue_verses(vi)
    vi = split_long_paras(vi)

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


def _gloss_entry_lines(text):
    """Tach glossary thanh (header_lines, [(khoa_han, dong_nguyen_van)]).

    Dòng không phải cặp 'Hán = Việt' (tiêu đề mục, ghi chú, quy tắc) luôn được
    giữ — chúng là luật chứ không phải mục từ.
    """
    lines = text.splitlines()
    fixed, entries = [], []
    for line in lines:
        m = re.match(r"^([\u4e00-\u9fff]{1,8}) = ", line)
        if m:
            entries.append((m.group(1), line))
        else:
            fixed.append(line)
    return fixed, entries


def load_glossary_for_chapter(ch_no, src_text="", back=60, ahead=20):
    """Glossary theo CHƯƠNG: luật luôn có, mục từ chỉ nhét khi cần.

    Nguồn: FILE GỐC (GLOSSARY) — chứa cả mục lõi lẫn các mục theo lô. Mỗi mục từ
    được giữ nếu thỏa MỘT trong ba điều kiện:
      1. Khóa Hán xuất hiện trong chương đang dịch -> chắc chắn cần.
      2. Khóa nằm trong glossary lõi (nhân vật chính, quy ước, quy tắc) -> luôn nhét.
      3. Khóa thuộc lô gần chương này (ch_no-back .. ch_no+ahead).

    Điều kiện 1 tự phủ mọi tên/thuật ngữ khi chúng thực sự xuất hiện nên không
    sợ mất từ; điều kiện 3 chỉ giữ mạch thuật ngữ của arc đang dịch. Nhờ vậy
    glossary phình bao nhiêu thì prompt vẫn ổn định ~30-40k ký tự.
    """
    here = Path(__file__).parent
    core = here / "_ts_gloss_core.txt"
    raw = GLOSSARY.read_text(encoding="utf-8")
    fixed, entries = _gloss_entry_lines(raw)

    core_keys = set()
    if core.is_file():
        _, core_entries = _gloss_entry_lines(core.read_text(encoding="utf-8"))
        core_keys = {k for k, _ in core_entries}

    # khoảng lô của từng mục mở rộng
    range_of = {}
    for m in re.finditer(
            r"(?ms)^## .*?THUẬT NGỮ.*?(\d+)[–-](\d+).*?═[ \t]*$(.*?)(?=^## |\Z)",
            raw):
        lo, hi = int(m.group(1)), int(m.group(2))
        for line in m.group(3).splitlines():
            mm = re.match(r"^([\u4e00-\u9fff]{1,8}) = ", line)
            if mm:
                range_of[mm.group(1)] = (lo, hi)

    keep = []
    for zh, line in entries:
        if zh in core_keys:
            keep.append(line)
        elif src_text and zh in src_text:
            keep.append(line)
        else:
            lo_hi = range_of.get(zh)
            if lo_hi and lo_hi[0] - back <= ch_no <= lo_hi[1] + ahead:
                keep.append(line)
    return "\n".join(fixed + keep).strip() + "\n"


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
    ap.add_argument("--confirm-delete", action="store_true",
                    help="bat buoc khi dung --reset: xac nhan xoa TOAN BO ban dich cua truyen")
    ap.add_argument("--retry", action="store_true", help="dich lai nhung chuong bi loi")
    ap.add_argument("--workers", type=int, default=int(os.environ.get("WORKERS", "4")),
                    help="so chuong dich song song")
    ap.add_argument("--parts", type=int, default=int(os.environ.get("PARTS", "1")),
                    help="chia moi chuong thanh N phan (model bam glossary tot hon, it sot Han)")
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
        if not getattr(a, "confirm_delete", False):
            sys.exit(
                "TU CHOI --reset: lenh nay se XOA TOAN BO ban dich da co trong "
                f"{OUT} va reset state. Neu thuc su muon lam lai tu dau, chay lai "
                "voi --reset --confirm-delete. Muon dich lai mot vai chuong thi "
                "xoa dung file do (hoac them vao failed), KHONG dung --reset."
            )
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
    # Glossary theo từng chương: lop loi + lop mo rong đúng khoảng chương.
    # Dịch lô thì cache theo từng chương (ch_no khác nhau) — tính trong thread con.
    glossary_core = load_glossary_for_chapter(a.lo)

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
        futs = {ex.submit(translate_chapter, n, s, chs, api, glossary_core, a.parts): (n, s)
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