# -*- coding: utf-8 -*-
"""Trich xuat tu vong danh bao/nhan vat tu cac chuong da tai, de xay dung glossary."""
import re, os, json
from collections import Counter

SRC = r"f:\taitruyen\truyendich_scraper\baojian"
OUTDIR = r"f:\taitruyen\translate"
os.makedirs(OUTDIR, exist_ok=True)

MARKER = re.compile(r'^[ \t]*\d+\|[ \t]*$', re.M)

STOP = set(
    "的 了 是 在 和 有 我 你 他 她 们 这 那 不 就 也 都 而 及 与 或 一个 什么 没有 我们 你们 他们 这个 那个 "
    "因为 所以 但是 如果 虽然 已经 还是 可以 这样 那样 时候 知道 看到 听到 起来 出来 下来 进去 过去 自己 "
    "一些 现在 刚才 于是 然后 因此 并且 或者 忽然 突然 顿时 立刻 马上 直接 简单 一起 而是 不是 就是 一样 "
    "非常 十分 比较 有些 这些 那些 除了 由于 按照 对于 关于 通过 根据 一二三四五六七八九十 我们 东西 事情 "
    "地方 样子 问题 感觉 心里 身上 眼中 手中 脸上 身上 身上 头顶 一边 一面 这个 那个 什么 怎么 这样 那样"
    .split()
)


def clean(t):
    t = MARKER.sub("", t)
    t = t.replace("\ufffd", "")
    t = t.replace("\ufffd", "")
    t = t.replace("\ufffd", "")
    # OCR: 曰 thay cho 日
    t = t.replace("\u66f0", "\u65e5")
    return t


def main():
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".txt"))
    chunks = []
    for f in files:
        with open(os.path.join(SRC, f), encoding="utf-8", errors="replace") as fh:
            chunks.append(clean(fh.read()))
    full = "\n".join(chunks)

    name_ctr = Counter()
    item_ctr = Counter()

    name_pats = [
        r"([\u4e00-\u9fff]{2,4})(?:\u8bf4\u9053|\u8bf4|\u9053|\u95ee\u9053|\u95ee|\u7b54\u9053|\u7b11\u9053|\u558a\u9053|\u53eb\u9053)",
        r"([\u4e00-\u9fff]{2,4})(?:\u70b9\u4e86\u70b9\u5934|\u6447\u4e86\u6447\u5934|\u53f9\u4e86\u53e3\u6c14|\u76b1\u8d77\u7709\u82e6|\u770b\u4e86\u770b|\u671b\u5411|\u76ef\u7740|\u56de\u8fc7\u5934)",
        r"(?:\u540d\u53eb|\u53eb\u505a|\u59d3|\u5524\u4f5c)([\u4e00-\u9fff]{1,4})",
        r"([\u4e00-\u9fff]{2,3})(?:\u7684(?:\u7236\u4eb2|\u6bcd\u4eb2|\u5e08\u7236|\u7237\u7237|\u5976\u5976|\u54e5\u54e5|\u59d0\u59d0|\u5f1f\u5f1f|\u59b9\u59b9))",
    ]
    for p in name_pats:
        for m in re.finditer(p, full):
            w = m.group(1)
            if w not in STOP and len(w) >= 2:
                name_ctr[w] += 1

    item_pats = [
        r"([\u4e00-\u9fff]{2,5}?)(?:\u5b9d\u5251|\u957f\u5251|\u77ed\u5251|\u5200|\u5251|\u73e0|\u4e39|\u9f0e|\u949f|\u955c|\u5e61|\u65d7|\u7b26|\u5370|\u7532|\u888d)",
        r"([\u4e00-\u9fff]{2,6}?)(?:\u529f\u6cd5|\u5fc3\u6cd5|\u79d8\u7c4d|\u6b66\u6280|\u62db\u5f0f|\u79d8\u672f|\u6cd5\u672f|\u9635\u6cd5)",
        r"([\u4e00-\u9fff]{2,5}?)(?:\u836f\u6750|\u7075\u836f|\u4e39\u836f|\u7075\u77f3|\u7075\u6676|\u6676\u77f3)",
    ]
    for p in item_pats:
        for m in re.finditer(p, full):
            item_ctr[m.group(0)] += 1

    res = {
        "files": len(files),
        "chars": len(full),
        "names": name_ctr.most_common(150),
        "items": item_ctr.most_common(100),
    }
    with open(os.path.join(OUTDIR, "analysis.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)

    lines = ["=== NAMES ==="] + [f"{w}\t{c}" for w, c in name_ctr.most_common(150)]
    lines += ["", "=== ITEMS ==="] + [f"{w}\t{c}" for w, c in item_ctr.most_common(100)]
    with open(os.path.join(OUTDIR, "analysis.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("files=%d chars=%d -> analysis.txt" % (len(files), len(full)))


main()