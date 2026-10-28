# -*- coding: utf-8 -*-
"""Trich ten rieng sach hon: ten + cum dong tu/dan tu ngay sau."""
import pathlib, re, collections

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
AFTER = (r"(?:说道|笑道|喝道|问道|答道|冷声道|沉声道|淡淡道|点了点头|摇了摇头|皱起眉头|"
         r"深吸一口气|脸色一变|眼中|目光|嘴角|心中|闻言|苦笑|冷笑|淡淡的|微微|突然|"
         r"立刻|瞬间|转身|抬手|盯着|看着|望着|脸色|心头|身上|手中|脚下|房间|出手|"
         r"眼眸|瞳孔|抱着|走了过来|身体|气息|脚步|手臂|肩膀|抬头|回头|闪身|负手|"
         r"站在|坐在|躺在|开口道|解释道|反问|疑问|点头|摇头|叹气|轻笑|大笑|怒吼|"
         r"开口|走来|一旁|身边|身形|说道|走向|直奔|开口|伸手|抬手)")
STOP = set("的 了 是 在 和 有 我 你 他 她 们 这 那 不 就 也 都 而 及 与 或 一个 什么 没有 "
           "我们 你们 他们 这个 那个 因为 所以 但是 如果 虽然 已经 还是 可以 这样 那样 "
           "时候 知道 看到 听到 起来 出来 下来 进去 过去 自己 一些 现在 刚才 于是 然后 "
           "因此 并且 或者 忽然 突然 顿时 立刻 马上 直接 简单 一起 而是 不是 就是 一样 "
           "非常 十分 比较 有些 这些 那些 除了 由于 按照 对于 关于 通过 根据 东西 "
           "事情 地方 样子 问题 感觉 心里 身上 眼中 手中 脸上 头顶 一边 一面 怎么 随即 "
           "旋即 再度 再次 缓缓 淡淡 一声 众人 两人 三人 几人 一人 一名 一位 一只 一张 一道 "
           "一片 一股 一阵 老者 男子 女子 少年 青年 中年 有人 对面 身后 面前 上方 下方 "
           "里面 外面 房间 大厅 空气 地面 天空 四周 一瞬 一刻 不少 许多 很多 几个 数十 "
           "上百 上千 数百 万千 不下 上下 左右 前后 略微 几分 口中 心中 眼中 身上 "
           "冷冷 连忙 齐齐 强大 满意 强横 双方 强者 威严的 口中 包在 里的 那人 那股 "
           "那小子 余人也都 都从各自".split())

files = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
c = collections.Counter()
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"([\u4e00-\u9fff]{2,4})(?=" + AFTER + ")", t):
        for L in (3, 2):                     # thu do dai 3 truoc, 2 lai
            s = m.group(1)[-L:]
            if s not in STOP and not re.search(r"[的了是在和有我你他她这那不就也都]", s):
                c[s] += 1
                break

items = sorted(((v, k) for k, v in c.items() if v >= 12), reverse=True)
out = pathlib.Path(r"f:/taitruyen/translate/_names_new2.txt")
out.write_text("\n".join(f"{v}\t{k}" for v, k in items), encoding="utf-8")
print("ung vien >=12:", len(items))
for v, k in items:
    print(v, k)
