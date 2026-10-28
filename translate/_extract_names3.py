# -*- coding: utf-8 -*-
"""Ten rieng that su: 2-4 chu, bat dau bang ho Hoa, >=8 lan, chua co trong glossary."""
import pathlib, re, collections

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
SURNAME = set("叶姜谢韩敖云诸葛皇甫诸葛司徒姬敖龙颜李王朱孙白魏秦东皇沈周杨金苏陆萧张马林"
              "赵罗梁宋唐许冯曹袁钟柳马温常刘罗高梁方侯邱孔白罗谢顾尹"
              "宋唐许邓冯韩曹彭曾肖田董袁潘蒋蔡余杜程苏魏吕丁任沈姚卢崔钟谭陆汪范金"
              "石廖贾夏韦付邹孟熊秦邱江薛闫段雷侯史陶黎贺毛郝龚邵钱严覃戴莫孔向汤")
STOP = set("的 了 是 在 和 有 我 你 他 她 们 这 那 不 就 也 都 而 及 与 或 一个 什么 没有 "
           "我们 你们 他们 这个 那个 因为 所以 但是 如果 虽然 已经 还是 可以 这样 那样 "
           "时候 知道 看到 听到 起来 出来 下来 进去 过去 自己 一些 现在 刚才 于是 然后 "
           "因此 并且 或者 忽然 突然 顿时 立刻 马上 直接 简单 一起 而是 不是 就是 一样 "
           "非常 十分 比较 有些 这些 那些 除了 由于 按照 对于 关于 通过 根据 东西 "
           "事情 地方 样子 问题 感觉 心里 身上 眼中 手中 脸上 头顶 一边 一面 怎么 随即 "
           "声音 冷淡 连忙 齐齐 强大 满意 强横 双方 强者 立刻 样子 心中 目光 嘴角 眼眸 "
           "闻言 苦笑 冷笑 微微 淡淡 身形 脚步 房间 身上 手中 众人 一声 一位 一名 一群 "
           "女子 男子 少年 青年 中年 老者 家人 夫人 大人 小子 时候 地方 东西 时候 身份"
           .split())

files = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
c = collections.Counter()
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"([\u4e00-\u9fff]{2,4})(?=[说道笑喝问答的、，。！：“）\s])", t):
        s = m.group(1)
        if s[0] in SURNAME and s not in STOP and len(s) >= 2:
            c[s] += 1

gl = pathlib.Path(r"f:/taitruyen/translate/glossary_can_bao_chan_long.txt").read_text(
    encoding="utf-8")
have = set(re.findall(r"[\u4e00-\u9fff]{2,4}", gl))

items = sorted(((v, k) for k, v in c.items() if v >= 10 and k not in have), reverse=True)
out = pathlib.Path(r"f:/taitruyen/translate/_names_new3.txt")
out.write_text("\n".join(f"{v}\t{k}" for v, k in items), encoding="utf-8")
print("ung vien >=10:", len(items))
for v, k in items:
    print(v, k)
