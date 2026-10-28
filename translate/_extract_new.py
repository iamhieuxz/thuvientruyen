# -*- coding: utf-8 -*-
"""Trich ten rieng + thuat ngu tu truyen moi, de dung glossary."""
import re
import pathlib
import collections

D = pathlib.Path(r"f:\taitruyen\truyendich_scraper\canh-bao-chan-long-xuat-nguc")
SUR = set("赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯管卢莫房干解应宗丁宣邓郁单杭洪包诸左石崔吉龚程嵇邢裴陆荣翁荀羊惠甄曲家封储靳汲糜松井段富巫乌焦巴牧山谷车侯班秋仲伊宁仇暴甘厉祖武符刘景詹束龙叶幸司韶郜黎印宿白怀蒲鄂索赖卓蔺屠蒙池乔胥苍双闻莘翟谭贡姬申冉雍桑桂牛通边燕浦尚农温庄晏柴瞿阎充慕连茹艾鱼容向古易慎戈廖终居衡步都耿满弘匡国文广东欧利越隆师巩聂晁敖冷辛阚那简饶空曾沙鞠丰巢关相查荆红游权盖桓元明永文武秋林石李王方汪左邹叶白苏陆崔钟谭陆韩曾杨徐朱胡郭何高罗郑梁谢宋唐许邓冯韩曹彭曾肖田董袁潘蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏韦付方白邹孟熊秦邱江尹薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔向汤")

STOP = set("的 了 是 在 和 有 我 你 他 她 们 这 那 不 就 也 都 而 及 与 或 一个 什么 没有 我们 你们 他们 这个 那个 因为 所以 但是 如果 虽然 已经 还是 可以 这样 那样 时候 知道 看到 听到 起来 出来 下来 进去 过去 自己 一些 现在 刚才 于是 然后 因此 并且 或者 忽然 突然 顿时 立刻 马上 直接 简单 一起 而是 不是 就是 一样 非常 十分 比较 有些 这些 那些 除了 由于 按照 对于 关于 通过 根据 东西 事情 地方 样子 问题 感觉 心里 身上 眼中 手中 脸上 头顶 一边 一面 怎么 随即 旋即 直接 再度 再次 顿时 缓缓 微微 淡淡 冷笑 淡笑 摇头 点头 皱眉 眼中 心中 嘴角 脸色 闻言 身形 目光 眼眸 瞳孔 手臂 肩膀 体内 体内 一声 众人 两人 三人 几人 一人 一名 一位 一只 一张 一道 一片 一股 一阵 一声 老者 男子 女子 少年 青年 中年 有人 众人 对面 身后 面前 上方 下方 里面 外面 房间 大厅 空气 地面 天空 四周 一瞬 一刻 一声 不少 许多 很多 一些 几个 数十 上百 上千 数百 万千 不下 上下 左右 前后 略微 几分 一些".split())

files = [f for f in sorted(D.glob("*.txt")) if not f.name.startswith("_")]
T = []
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"^第\d+章.*$", "", t, flags=re.M)
    T.append(t)
full = "\n".join(T)

# ── tên riêng: 2-4 chữ Hán, đứng trước động từ / danh từ chỉ người
c = collections.Counter()
pat = (r"([\u4e00-\u9fff]{2,4})(?=[\u4e00-\u9fff]{0,2}(?:说道|笑道|喝道|问道|答道|冷声道|沉声道|淡淡道|点了点头|摇了摇头|皱起眉头|深吸一口气|脸色一变|眼中|目光|嘴角|心中|闻言|苦笑|冷笑|淡淡的|微微|突然|立刻|瞬间|转身|抬手|盯着|看着|望着|脸色|心头|身上|手中|脚下|房间|出手|眼眸|瞳孔|抱着|走了过来|身体|气息|脚步|手臂|肩膀|抬头|回头|闪身|负手|站在|坐在|躺在|开口道|解释道|反问|疑问|点头|摇头|叹气|轻笑|大笑|怒吼|开口))")
for m in re.finditer(pat, full):
    s = m.group(1)
    if s[0] in SUR and len(s) >= 2 and s not in STOP:
        c[s] += 1

items = sorted(((v, k) for k, v in c.items() if v >= 8), reverse=True)
out = pathlib.Path(r"f:\taitruyen\translate\_names_new.txt")
out.write_text("\n".join(f"{v}\t{k}" for v, k in items), encoding="utf-8")
print("ung vien >=8:", len(items))
for v, k in items[:80]:
    print(v, k)

# ── thuật ngữ võ đạo / địa danh / tổ chức
t2 = collections.Counter()
for p in [r"([\u4e00-\u9fff]{2,6}?)(?:境|宗|派|阁|殿|宫|府|城|山|海|星域|皇朝|王朝|宗门|家族|协会|联盟|会|教|谷|域|星|界|州|郡|县)"]:
    for m in re.finditer(p, full):
        t2[m.group(0)] += 1
items2 = sorted(((v, k) for k, v in t2.items() if v >= 40), reverse=True)
out2 = pathlib.Path(r"f:\taitruyen\translate\_terms_new.txt")
out2.write_text("\n".join(f"{v}\t{k}" for v, k in items2), encoding="utf-8")
print("\nthuat ngu >=40:", len(items2))
for v, k in items2[:70]:
    print(v, k)
