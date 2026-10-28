# -*- coding: utf-8 -*-
"""QA ban dich Trung -> Viet. Chi DOI, khong sua. Exit code 1 neu co loi E.

Da lam moi cho bo "Canh Bao! Chan Long Xuat Nguc" (can_bao_chan_long),
van dung duoc cho baojian qua --book. Duong dan/glossary/state lay tu dich.py
BOOKS nen khoi trung cau hinh.

Dung:
  python check.py --from 6 --to 15            # QA mot lo
  python check.py                             # QA toan bo so chuong da dich
  python check.py --names                     # dong nhat ten rieng toan cuc
  python check.py --from 6 --to 15 --json     # xuat may doc duoc
  python check.py --book baojian --from 1 --to 30
  python check.py --quiet                     # chi in tong ket + loi E

Nhom kiem
  E1  Han con sot trong than bai (moi chuoi CJK; gan nhan FORBID/glossary/la)
  E2  Ten rieng lech dang chuan cua glossary
  E3  Dau kiem duyet con sot: "*" / "[***]"
  E4  Dai cam cam: nguoi / lao tu / lao phu (+ "ngai" = W)
  E5  Xung ho "con" sai (anh chi / nguoi lon goi nhau la "con")
  E6  Cau truc bai: thieu "# Chuong N", so lech filename, thieu "(Con tiep)",
      ngoac kep lech, markdown, ten chuong bi chep lai giua bai
  E7  Ban dich bi cat so voi nguon (so doan + so dau cau, dung dich.check_complete)
  E8  Rac scraper lot vao ban dich
  E9  File nhap sot (_NNNN_nhap.md / _NNNN_cat.md), trung so chuong, chuong trong state.failed
  W   Chua hop le hoa: nhac check (khong cat mau)
"""
import argparse, collections, difflib, json, os, re, statistics, sys

try:  # console Windows mac dinh khong in duoc tieng Viet co dau + chu Han
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import dich

DEFAULT_BOOK = os.environ.get("BOOK", "can_bao_chan_long")

CJK = re.compile(r"[\u4e00-\u9fff]+")
# day 2-3 tu lien nhau; dung .upper() de xac dinh chu in hoa (khong dung
# [A-ZDa-y] vi dai Unicode A-Z chua ca tu in thuong co dau)
WORD_SEQ = re.compile(r"(?:[^\W\d_]+[ \t]+){1,2}[^\W\d_]+")
DUP_HEAD = re.compile(r"(?m)^[ \t]*\*{0,2}[ \t]*(?:CHƯƠNG|Chương)[ \t]+\d+[ \t]*[:：]")
MD_BOLD = re.compile(r"\*\*")
MD_HEAD = re.compile(r"(?m)^\s*#{1,6}\s")
STRAIGHT_Q = re.compile(r'"')
NGAN_BAD = re.compile(r"\bngàn\b")
# Quy ước trong SYSTEM: số đếm dùng "nghìn", chỉ giữ "ngàn" trong thành ngữ văn ngôn
NGAN_WORD = {"dặm", "năm", "vàng", "cân"}
BANNED_PRONOUN = re.compile(r"(?i)\b(?:ngươi|lão tử|lão phu)(?! nhân)\b")
SERVE = re.compile(r"(?i)\bngài\b")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd]")
HAN_PUNCT = re.compile(r"[（）【】]")

SRC_JUNK = ("飘天", "getmode", "selectcolors", "bixia", "注册会员", "私人书架",
            "未完待续", "月票", "推荐票", "加入书签", "扫码关注", "微信公众号",
            "百度搜索", "本章完", "txt下载", "章节错误", "作者自定义标签")

SURNAME = set(
    "叶姜谢韩敖诸葛皇甫司徒姬龙颜李王朱孙白魏秦东皇沈周杨金苏陆萧张马林赵罗梁宋"
    "唐许冯曹袁钟柳温常刘高方侯邱孔顾尹汤戴莫向金石廖贾夏韦付邹孟熊江薛闫段雷"
    "史陶黎贺毛郝龚邵钱严覃程余杜潘蒋蔡卢姚崔谭汪范吴周田任袁宁")
STOP_BLOB = ("的了是在有我你他她们这那不就也都而及与或一个什么没有我们你们他们这个那个"
             "因为所以但是如果虽然已经还是可以这样那样时候知道看到听到起来出来下来进去过去自己"
             "一些现在刚才于是然后因此并且或者忽然突然顿时立刻马上直接简单一起而是不是一样非常"
             "十分比较有些这些那些除了由于按照对于关于通过根据东西事情地方样子问题感觉心里身上"
             "眼中手中脸上头顶一边一面怎么随即声音冷淡连忙齐齐众人一位一名一群女子男子少年青年"
             "中年老者家人夫人大人小子身份先生小姐说道笑喝问答看着想过来去点头上前出手离开回头"
             "开口摇头皱眉冷哼谢谢大房二房三房家主老爷子")
# CJK khong tach bang khoang trang -> sinh tru chu 2..4 tu khoi blob
STOP = {STOP_BLOB[i:j] for i in range(len(STOP_BLOB))
        for j in range(i + 2, min(i + 5, len(STOP_BLOB)) + 1)}

# ho + chuoi nay la dong tu/cum thong thuong, khong phai ten rieng moi
NOISE_TAIL = set("""养家 出来 进去 过去 现在 明白 起身 向前 后方 上面 下去 上来 说道
张嘴 苦笑 微蹙 要害 总是 有钱 生气 好看 无法 无天 日 月 年 时 八蛋 混混 小子 娘的 妈的 大爷 东西
家伙 同志 老师 老板 兄弟 姐妹 小姐 太太 夫人 先生 小三 强者 嘴巴 代价 贵手 之怒 几人 谢谢 高兴""".split())

# chu khong bao gio xuat hien trong ten nguoi that -> candidate chua no la cum tu thong thuong
FUNC_CHAR = set("的了着过呢吗吧就都很又只被让而你他她它")


# ─────────────────────── cấu hình theo truyện ───────────────────────

def load_glossary(path):
    """glossary: moi dong `Hán = Việt (chú thích)` -> (zh2vi, vi2zh)."""
    zh2vi, vi2zh = {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k, v = k.strip(), v.split("(")[0].strip()
        if not k or not v or not CJK.search(k):
            continue
        zh2vi[k] = v
        if v[0].isupper():
            vi2zh[v] = k
    return zh2vi, vi2zh


class Ctx:
    def __init__(self, book):
        dich.set_book(book)
        self.book, self.src, self.out = book, dich.SRC, dich.OUT
        self.forbid = [f for f in dich.forbid_list() if CJK.search(f)]
        self.zh2vi, self.vi2zh = load_glossary(dich.GLOSSARY)
        self.titles = dich.load_titles()
        self.state = dich.load_state()
        self.failed = set(self.state.get("failed", []))
        self.chs = dich.all_chapters()
        # dang goi tat duoc chap nhan: "Khương Quân Dao" -> "Quân Dao", "Dao"
        self.accepted = set()
        self.trailer = None   # lazy: truyen nay dung '(Còn tiếp)' khong?
        for vi in self.vi2zh:
            w = vi.split()
            self.accepted.add(vi)
            # cac dang goi tat hop le: "Khương Quân Dao" -> "Quân Dao";
            # "Chân Long Cốt" -> "Chân Long". Chi chap nhan do lien tuc >=2 tu
            # hoac tu cuoi, khong chap nhan cach viet lech chinh ta.
            for i in range(len(w)):
                for j in range(i + 1, len(w) + 1):
                    if j - i >= 2 or i == len(w) - 1:
                        self.accepted.add(" ".join(w[i:j]))

    def src_text(self, n):
        """Ban goc da chuan hoa giong luc goi dich (de so doan/dau cau)."""
        if n not in self.chs:
            return ""
        t = dich.clean((self.src / self.chs[n]).read_text(
            encoding="utf-8", errors="replace"))
        return dich.dedup_repeats(dich.strip_src_junk(t))

    def wants_trailer(self):
        """Quy uoc '(Còn tiếp)' khac nhau giua cac truyen -> lay theo 20 bai gan nhat."""
        by_num = index_files(self)[0]
        nums = sorted(by_num)[-20:]
        if not nums:
            return False
        ok = sum(1 for n in nums
                 if body_of(by_num[n][0].read_text(encoding="utf-8"))
                 .rstrip().endswith("(Còn tiếp)"))
        return ok >= len(nums) * 0.8


def body_of(t):
    lines = [l for l in t.splitlines() if not l.strip().startswith("<!--")]
    while lines and (not lines[0].strip() or lines[0].lstrip().startswith("#")):
        lines.pop(0)
    return "\n".join(lines).strip()


def snip(t, i, w=35):
    return re.sub(r"\s+", " ", t[max(0, i - w):i + w])


def cap_seqs(text):
    """Các dãy 2-3 từ in hoa liền nhau = ứng viên tên riêng."""
    out = []
    for m in WORD_SEQ.finditer(text):
        ws = m.group(0).split()
        if all(w[0].upper() == w[0] for w in ws):
            out.append(" ".join(ws))
    return out


# Tit goi dung truoc ten rieng ("Chị Tĩnh Huyên", "cô Hoàng Phủ"...), khong phai ten lech
HONORIFIC = {
    "anh", "chị", "em", "cô", "cậu", "chú", "bác", "bà", "ông", "mụ", "mợ",
    "thằng", "con", "lão", "gã", "hắn", "tao", "mày", "vị", "nhà", "thầy",
    # tu chi noi/dich chuyen, dung dau cum "Ở Giang Đô", "Tại Kim Lăng"...
    "ở", "tại", "từ", "đến", "tới", "sang", "về", "trong", "ngoài", "trên",
    "dưới", "giữa", "gần", "cách", "khu", "nơi", "hướng", "phía",
}


def strip_honorific(name):
    """Bỏ từ xưng hô/nơi đứng trước tên: 'Chị Tĩnh Huyên' -> 'Tĩnh Huyên'."""
    w = name.split()
    while w and w[0].lower() in HONORIFIC:
        w = w[1:]
    return " ".join(w)


# ─────────────────────────── tung bai ───────────────────────────

def check_cjk(ctx, body):
    errs = []
    for h, n in collections.Counter(CJK.findall(body)).items():
        tag = ("FORBID" if any(f in h for f in ctx.forbid)
               else "glossary" if any(k in h or h in k for k in ctx.zh2vi) else "lạ")
        errs.append(("E", f"Hán sót ({tag}) x{n}: {h}"))
    return errs


def check_censor(body):
    errs = []
    hits = list(re.finditer(r"\*+", body))
    if hits:
        errs.append(("E", f"còn dấu kiểm duyệt '*' x{len(hits)}: "
                          f"…{snip(body, hits[0].start())}…"))
    for pat in ("[***]", "… … …"):
        if pat in body:
            errs.append(("E", f"ký tự kiểm duyệt lạ: {pat}"))
    return errs


def check_pronouns(body):
    errs = []
    ms = list(BANNED_PRONOUN.finditer(body))
    for m in ms[:3]:
        errs.append(("E", f"đại từ cấm '{m.group(0)}' → …{snip(body, m.start())}…"))
    if len(ms) > 3:
        errs.append(("E", f"…+{len(ms) - 3} đại từ cấm nữa"))
    ms = list(SERVE.finditer(body))
    if ms:
        errs.append(("W", f"'ngài' x{len(ms)} (glossary: dùng 'ông') → "
                          f"…{snip(body, ms[0].start())}…"))
    return errs


def check_con(body):
    """E5: 'con' dung lam xuong minh TRUOC nguoi lon, cach goi co xuc ho
    (dau phay/loi ken truoc 'con'). Chuoi 'me con', 'bo con', 'anh con'...
    la cum chi quan he gia dinh -> hop le, khong phan."""
    errs = []
    VOC = (r"(?:anh|chị|em|ông|bà|cô|dì|thím|mợ|chú|bác|ba|má|mẹ|bố|cha|thầy)"
           r"\s*(?:ơi|ạ|à|nhỉ|nhen)?\s*[,.!:]\s*(?:thì\s+)?con\b"
           r"(?![\wàáảãạăâêôơưý])")
    for i, line in enumerate(body.splitlines(), 1):
        if "con" not in line.lower():
            continue
        m = re.search(VOC, line, re.I)
        if m:
            errs.append(("W", f"dòng {i}: xưng 'con' với người lớn → …"
                              f"{snip(line, m.start(), 30)}…"))
    return errs


def check_structure(ctx, num, body, raw):
    errs = []
    first = next((l.strip() for l in raw.splitlines()
                  if l.strip() and not l.strip().startswith("<!--")), "")
    m = re.match(r"^#\s*Chương\s*(\d+)\s*[:：]\s*(.+)$", first)
    if not m:
        errs.append(("E", f"thiếu dòng '# Chương N: …' (dấu bài: {first[:50]!r})"))
    else:
        if int(m.group(1)) != num:
            errs.append(("E", f"số chương ở heading {m.group(1)} != filename {num}"))
        exp = ctx.titles.get(num, "")
        got = m.group(2).strip()
        if BANNED_PRONOUN.search(got):
            errs.append(("E", f"tiêu đề chứa từ cấm: {got!r} — sửa cả titles json"))
        if exp and got != re.sub(r"^Chương\s*\d+\s*[:：]\s*", "", exp).strip():
            errs.append(("W", f"tiêu đề lệch titles json: '{got}' != '{exp}'"))
    if ctx.trailer is None:
        ctx.trailer = ctx.wants_trailer()
    if ctx.trailer and not body.rstrip().endswith("(Còn tiếp)"):
        errs.append(("W", "thiếu '(Còn tiếp)' cuối bài"))
    if DUP_HEAD.search(body):
        m2 = DUP_HEAD.search(body)
        errs.append(("E", f"tiêu đề chương bị chép giữa thân bài: …{snip(body, m2.start(), 20)}…"))
    if MD_BOLD.search(body):
        errs.append(("E", "còn markdown ** ** trong thân bài"))
    if MD_HEAD.search(body):
        errs.append(("E", "còn dấu # (markdown heading) trong thân bài"))
    if body.count("“") != body.count("”"):
        errs.append(("E", f"ngoặc kép lệch: {body.count('“')} mở / {body.count('”')} đóng"))
    if STRAIGHT_Q.search(body):
        errs.append(("W", 'còn ngoặc kép ASCII "'))
    if CTRL.search(body):
        errs.append(("E", "ký tự điều khiển/hỏng trong bài"))
    if HAN_PUNCT.search(body):
        errs.append(("W", "còn dấu câu Hán （）【】"))
    return errs


def check_junk(body):
    errs = []
    for j in SRC_JUNK:
        if j in body:
            errs.append(("E", f"rác scraper: {j} → …{snip(body, body.index(j), 25)}…"))
    return errs


def check_style(ctx, body):
    errs = []
    bad = []
    for m in NGAN_BAD.finditer(body):
        nxt = re.match(r"\s*([A-Za-zà-ỹ]+)", body[m.end():])
        word = nxt.group(1).lower() if nxt else ""
        if word in NGAN_WORD or body[max(0, m.start() - 6):m.start()].lower() == "bạc ":
            continue
        bad.append(m.start())
    if bad:
        errs.append(("W", f"'ngàn' ngoài thành ngữ x{len(bad)} "
                          f"(quy ước: 'nghìn') → …{snip(body, bad[0])}…"))
    return errs


def check_names(ctx, num, src_text, body):
    """E2: dang viet ten rieng lech dang chuan trong glossary."""
    errs = []
    found = collections.Counter(cap_seqs(body))
    canon = sorted(ctx.vi2zh)
    for name, n in found.items():
        if name in ctx.accepted or n < 2:
            continue
        if strip_honorific(name) in ctx.accepted:
            continue
        best = difflib.get_close_matches(name, canon, n=1, cutoff=0.80)
        if best:
            errs.append(("E", f"biến thể tên '{name}' (x{n}) → chuẩn '{best[0]}'"))
    # nguon goi >=3 lan nhung bai khong co dang nao (dua hay tat) cua ten ay
    for zh, vi in ctx.zh2vi.items():
        c = src_text.count(zh)
        if c < 3:
            continue
        w = vi.split()
        forms = {vi, " ".join(w[-2:]) if len(w) >= 2 else vi,
                 w[-1] if len(w) >= 2 else vi}
        if forms & set(found) or any(f in body for f in forms):
            continue
        near = difflib.get_close_matches(vi, list(found), n=1, cutoff=0.72)
        if near:
            errs.append(("E", f"'{zh}' (nguồn x{c}) dịch thành '{near[0]}', "
                              f"chuẩn glossary '{vi}'"))
        else:
            errs.append(("W", f"'{zh}' (nguồn x{c}) nhưng bài không dùng tên '{vi}' "
                              f"— kiểm tra có bị đổi vai/không dịch"))
    return errs


# ─────────────────────────── khoi: file thieu/sot/trung ───────────────────────────

def index_files(ctx):
    by_num = collections.defaultdict(list)
    for p in sorted(ctx.out.glob("*.md")):
        m = re.match(r"^(\d{4,})_", p.name)
        if m:
            by_num[int(m.group(1))].append(p)
    drafts = sorted(ctx.out.glob("_*.md"))
    return by_num, drafts


def bulk_errors(ctx, by_num, drafts, nums):
    errs = []
    for d in drafts:
        num = int(re.match(r"_(\d{4,})_", d.name).group(1))
        if num in by_num:
            errs.append(("W", f"{d.name}: bài đã hợp thức nhưng còn file nháp → xoá"))
        else:
            kind = "bị cắt" if d.name.endswith("_cat.md") else "lỗi validate"
            errs.append(("E", f"{d.name}: bản nháp chưa duyệt ({kind})"))
    for n, fs in by_num.items():
        if len(fs) > 1:
            errs.append(("E", f"chương {n}: trùng {len(fs)} file: "
                              f"{', '.join(f.name for f in fs)}"))
    bad = [n for n in nums if n in ctx.failed]
    if bad:
        errs.append(("E", f"state.failed trong khoảng: {bad} (chạy dich.py --retry)"))
    miss = [n for n in nums if n not in by_num]
    if miss:
        errs.append(("W", f"chưa dịch {len(miss)} chương: {ranges(miss)}"))
    return errs


def ranges(nums):
    """[1,2,3,7] -> '1-3, 7' (gon bao cao)."""
    out, lo, prev = [], None, None
    for n in sorted(nums):
        if lo is None:
            lo = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append(f"{lo}-{prev}" if prev > lo else str(lo))
            lo = prev = n
    if lo is not None:
        out.append(f"{lo}-{prev}" if prev > lo else str(lo))
    return ", ".join(out)


# ─────────────────────────── glossary / ngu canh ───────────────────────────

def glossary_report(ctx, nums):
    lines = []
    pending = []
    for pair in ctx.state.get("new_terms", []):
        zh = pair.split("=")[0].strip()
        if zh and zh not in ctx.zh2vi and pair not in pending:
            pending.append(pair)
    if pending:
        lines.append(f"W1 {len(pending)} thuật ngữ mới chưa vào glossary (dòng paste được):")
        lines += [f"    {p}" for p in pending[:30]]
        if len(pending) > 30:
            lines.append(f"    … +{len(pending) - 30} nữa")

    cnt, ctxs = collections.Counter(), {}
    known = list(ctx.zh2vi)
    for n in nums:
        t = ctx.src_text(n)
        for m in re.finditer(r"([\u4e00-\u9fff]{2,4})(?=[说道笑喝问答喊、，。：“”）\s])", t):
            s = m.group(1)
            if s in ctx.zh2vi or s[0] not in SURNAME or s in STOP:
                continue
            if set(s) & FUNC_CHAR:
                continue          # "高兴的事", "方握了握" -> cum tu, khong phai ten
            if any(k in s or s in k for k in known):
                continue          # "向叶楚", "龙血脉" -> chuoi cat tu ten da co
            if s[1:] in NOISE_TAIL or s[-2:] in NOISE_TAIL:
                continue
            if len(s) >= 3 and s[1] == s[2]:
                continue          # "李哈哈大笑" -> lap lai am diau, khong phai ten
            cnt[s] += 1
            ctxs.setdefault(s, (n, snip(t, m.start(), 20)))
    # "甫诗月" la duoi cua "皇甫诗月" -> giu dang dai nhat
    drop = {s for s in cnt
            if any(t != s and s in t[1:] and cnt[t] >= cnt[s] for t in cnt)}
    fresh = sorted(((v, k) for k, v in cnt.items()
                    if v >= 2 and k not in drop), reverse=True)
    if fresh:
        lines.append(f"W2 {len(fresh)} tên Hán trong lô chưa có glossary:")
        lines += [f"    {k} (x{v}, ch{ctxs[k][0]}) …{ctxs[k][1]}…"
                  for v, k in fresh[:25]]
    return lines


def name_alignment_report(ctx):
    """--names: gom moi dang ten rieng trong toan ban dich, tim nhom gan trung."""
    cnt = collections.Counter()
    where = collections.defaultdict(set)
    for n, fs in sorted(index_files(ctx)[0].items()):
        body = body_of(fs[0].read_text(encoding="utf-8"))
        for name in cap_seqs(body):
            cnt[name] += 1
            where[name].add(n)
    names = sorted(k for k, v in cnt.items() if v >= 2
                   and not (strip_honorific(k) != k
                            and (strip_honorific(k) in ctx.accepted
                                 or strip_honorific(k) in cnt)))
    used, groups = set(), []
    for a in names:
        if a in used:
            continue
        grp = [a]
        for b in names:
            if b in used or b == a:
                continue
            r = difflib.SequenceMatcher(None, a.replace(" ", ""),
                                        b.replace(" ", "")).ratio()
            if r >= 0.85:
                grp.append(b)
                used.add(b)
        if len(grp) > 1:
            used.add(a)
            groups.append(grp)
    lines = [f"Tên gần trùng: {len(groups)} nhóm"]
    for grp in groups:
        std = [g for g in grp if g in ctx.vi2zh]
        if std:
            mark = "✓ chuẩn: " + std[0]
        elif all(g in ctx.accepted for g in grp):
            mark = "✓ chỉ các dạng gọi tắt hợp lệ của cùng một tên"
        else:
            mark = "? chưa có trong glossary"
        detail = " | ".join(
            f"{g} x{cnt[g]} (ch {ranges(sorted(where[g]))})"
            for g in sorted(grp, key=lambda x: -cnt[x]))
        lines.append(f"    {detail} -> {mark}")
    return lines


# ─────────────────────────── main ───────────────────────────

def run(ctx, nums):
    by_num, drafts = index_files(ctx)
    results = {"(khối lượng)": bulk_errors(ctx, by_num, drafts, nums)}
    lens = {}
    for n in nums:
        fs = by_num.get(n)
        if not fs:
            continue
        raw = fs[0].read_text(encoding="utf-8")
        body = body_of(raw)
        lens[n] = len(body)
        src_text = ctx.src_text(n)
        errs = []
        errs += check_cjk(ctx, body)
        errs += check_censor(body)
        errs += check_pronouns(body)
        errs += check_con(body)
        errs += check_structure(ctx, n, body, raw)
        errs += check_names(ctx, n, src_text, body)
        errs += check_junk(body)
        errs += check_style(ctx, body)
        if src_text:
            ok, why = dich.check_complete(src_text, body)
            if not ok:
                errs.append(("E", f"cắt so với nguồn: {why}"))
        results[fs[0].name] = errs
    # do dai bat thuong so voi median ca lo
    if len(lens) >= 5:
        med = statistics.median(lens.values())
        for n, L in sorted(lens.items()):
            if L < med * 0.45:
                key = next(k for k in results if k.startswith(f"{n:04d}_"))
                results[key].append(
                    ("W", f"quá ngắn: {L} ký tự (median lô {int(med)}) — coi chừng thiếu"))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=DEFAULT_BOOK, choices=sorted(dich.BOOKS))
    ap.add_argument("--from", dest="lo", type=int, default=0)
    ap.add_argument("--to", dest="hi", type=int, default=0)
    ap.add_argument("--names", action="store_true",
                    help="đồng nhất tên riêng toàn bản dịch")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="chỉ in lỗi E + tổng kết")
    ap.add_argument("--no-glossary", action="store_true")
    a = ap.parse_args()

    ctx = Ctx(a.book)
    if not ctx.out.exists():
        sys.exit(f"Không có thư mục bản dịch: {ctx.out}")
    have = sorted(n for n in index_files(ctx)[0])
    if not have:
        sys.exit("Chưa có bản dịch nào.")
    lo, hi = (a.lo or min(have)), (a.hi or max(have))
    if hi < lo:
        sys.exit("--to nhỏ hơn --from")
    nums = list(range(lo, hi + 1))

    if a.names:
        print("\n".join(name_alignment_report(ctx)))
        results = run(ctx, nums)
    else:
        results = run(ctx, nums)

    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return 1 if any(l == "E" for v in results.values() for l, _ in v) else 0

    print(f"═══ {ctx.book} · chương {lo}-{hi} · {len([n for n in nums if n in have])} bài ═══")
    n_e = n_w = 0
    for name, errs in results.items():
        errs = [e for e in errs if e]
        if not errs:
            continue
        show = [e for e in errs if e[0] == "E"] if a.quiet else errs
        if not show:
            n_w += len(errs)
            continue
        print(f"\n✗ {name}")
        for lvl, msg in show[:15]:
            print(f"   [{lvl}] {msg}")
        if len(show) > 15:
            print(f"   … +{len(show) - 15} lỗi nữa")
        n_e += sum(1 for l, _ in errs if l == "E")
        n_w += sum(1 for l, _ in errs if l == "W")

    if not a.names and not a.no_glossary:
        extra = glossary_report(ctx, nums)
        if extra:
            print("\n─── Glossary / ngữ cảnh ───")
            print("\n".join(extra))

    clean = len([n for n in nums if n in have]) - sum(
        1 for k, v in results.items() if v and any(l == "E" for l, _ in v) and not k.startswith("("))
    print(f"\n═══ {len([n for n in nums if n in have])} bài · sạch E={clean} "
          f"· E={n_e} W={n_w} ═══")
    return 1 if n_e else 0


if __name__ == "__main__":
    sys.exit(main())
