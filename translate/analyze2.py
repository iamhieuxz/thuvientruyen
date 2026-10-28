# -*- coding: utf-8 -*-
"""Trich xuat danh bao sach hon: loc bo cac to hop dong ngai (khong phai ten nguoi)."""
import re, os, json
from collections import Counter

SRC = r"f:\taitruyen\truyendich_scraper\baojian"
OUTDIR = r"f:\taitruyen\translate"
MARKER = re.compile(r'^[ \t]*\d+\|[ \t]*$', re.M)

# cac tu/to hop chung, KHONG phai ten rieng
BAD_SUB = set(
    "开口 不知 俗话 他知 要知 我知 谁知 按理 且不 也就是 接着 没好 没好气 当下 闻言 笑着 闻言 摇头 "
    "摆了 摆了摆手 低声 连忙 以为 以为然 低的 降低 声音 虽然 自然 你也 你知 我听 听到 听到秦风 看向 看向秦风 "
    "我很 也很 真的 好好的 早知 我听 苦笑 微微 喃喃 继续 轻声 倒不 门见 恶狠 回头 都知 淡淡 的这 仔细 "
    "不多 不了 什么的 可以 刚才 然后 忽然 突然 顿时 立刻 马上 直接 简单 一起 而是 不是 就是 一样 非常 "
    "十分 比较 有些 排除 由于 按照 对于 关于 通过 根据 现在 刚才 于是 因此 并且 或者 以为 知道 看到 "
    "听到 起来 出来 下来 进去 过去 自己 一些 这个 那个 什么 没有 我们 你们 他们 因为 所以 但是 如果 "
    "虽然 已经 还是 这样 那样 时候 东西 事情 地方 样子 问题 感觉 心里 身上 眼中 手中 脸上 头顶 一边 一面"
    .split()
)

# danh tu / phong hoa, thuong di kem ten rieng -> loai
NUANCE = ("的", "了", "着", "过", "地", "得")
VERBISH = ("说", "道", "问", "喊", "叫", "笑", "摇", "看", "听", "想", "走", "点", "望", "盯", "皱", "叹")


def clean(t):
    t = MARKER.sub("", t)
    t = t.replace("\ufffd", "")
    t = t.replace("\ufffd", "")
    t = t.replace("\ufffd", "")
    t = t.replace("\u66f0", "\u65e5")
    return t


def plausible(w):
    if len(w) < 2 or len(w) > 4:
        return False
    if w in BAD_SUB:
        return False
    # to hop ngai: chi ton tai neu "X + verb" ngay sau
    for c in w:
        if c in "\uff0c\u3002\u3001\uff01\uff1f\uff1b\uff1a\u201c\u201d":
            return False
    return True


def main():
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".txt"))
    full = "\n".join(clean(open(os.path.join(SRC, f), encoding="utf-8", errors="replace").read()) for f in files)

    ctr = Counter()
    # X + verb/dialogue marker : nhieu hon -> kha nang la ten nguoi
    for m in re.finditer(r"([\u4e00-\u9fff]{2,4})(?=\u8bf4|\u9053|\u95ee|\u7b54|\u558a|\u53eb)", full):
        w = m.group(1)
        if plausible(w):
            ctr[w] += 1
    # X + quan he hoa thu: "Lao Hu", "beo Hu"
    for m in re.finditer(r"(?:\u8001|\u5c0f|\u5927|\u963f)\s?([\u4e00-\u9fff]{1,3})", full):
        w = m.group(1)
        if plausible(w):
            ctr[w] += 1
    # "X说" tai dau cau, hoac sau dau cham
    for m in re.finditer(r"[\uff0c\u3002\u201c]([\u4e00-\u9fff]{2,4})(?=\u8bf4|\u9053|\u95ee|\u7b54|\u558a)", full):
        w = m.group(1)
        if plausible(w):
            ctr[w] += 2  # trong thoai -> manh tinh ten nguoi

    # loc them: bo tu dang sau
    res = [(w, c) for w, c in ctr.most_common(400) if c >= 3]
    with open(os.path.join(OUTDIR, "names.txt"), "w", encoding="utf-8") as fh:
        fh.write("files=%d chars=%d\n\n" % (len(files), len(full)))
        for w, c in res:
            fh.write(f"{w}\t{c}\n")
    print("files=%d chars=%d  candidates=%d" % (len(files), len(full), len(res)))


main()