# -*- coding: utf-8 -*-
"""Ten rieng: theo ho + 1-2 chu, dem theo cap do sau, loai bo danh tu/phien tu."""
import pathlib, re, collections

D = pathlib.Path(r"f:/taitruyen/truyendich_scraper/canh-bao-chan-long-xuat-nguc")
SURNAME = set("叶姜谢韩敖云诸葛皇甫司徒姬敖龙颜李王朱孙白魏秦东皇沈周杨金苏陆萧张马林"
              "赵罗梁宋唐许冯曹袁钟柳温常刘高方侯邱孔顾尹汤戴莫向秦"
              "金石廖贾夏韦付邹孟熊邱江薛闫段雷侯史陶黎贺毛郝龚邵钱严覃"
              "程余杜潘蒋蔡卢姚崔谭陆汪范白沈李罗吴周田任袁孟宁顾")
STOP = set("的了是在有我你他她们这那不就也都而及与或一个什么没有我们你们他们这个那个"
           "因为所以但是如果虽然已经还是可以这样那样时候知道看到听到起来出来下来进去"
           "过去自己一些现在刚才于是然后因此并且或者忽然突然顿时立刻马上直接简单一起"
           "而是不是一样非常十分比较有些这些那些除了由于按照对于关于通过根据东西事情"
           "地方样子问题感觉心里身上眼中手中脸上头顶一边一面怎么随即声音冷淡连忙齐齐"
           "强大满意强横双方强者立刻心中目光嘴角眼眸闻言苦笑冷笑微微淡淡身形脚步房间"
           "众人一位一名一群女子男子少年青年中年老者家人夫人大人小子身份金仙圆满中期"
           "叶楚点头叶楚诧异叶楚摇头叶楚冷哼叶楚摆手叶楚淡淡叶楚恍然叶楚一眼叶楚体内"
           "叶楚一愣叶楚皱眉叶楚愕然叶楚淡笑叶楚大哥叶楚冷笑叶楚身前叶楚离开叶楚拱手"
           "叶楚两人叶楚身边叶楚好奇叶楚知叶楚冷叶楚无语叶楚沉声叶楚冲去叶楚出手"
           "叶楚上前叶楚颔首叶楚逼近叶楚阻止叶楚无奈叶楚回神叶楚撇嘴叶楚开口叶楚含"
           "叶楚询问叶楚挥手叶楚手中叶楚身后叶楚解释叶楚淡叶楚眉心叶楚疑惑叶楚爽快"
           "叶楚大喝叶楚杀去叶楚杀来叶楚回头叶楚四周叶楚继续叶楚一愣叶楚摇头叶楚问"
           "叶楚家人叶楚一眼叶楚闻言叶楚笑道叶楚众人叶楚安慰叶楚挑眉叶楚面前叶楚身上"
           "叶楚身后叶楚其他叶楚一眼叶楚心中叶楚手中叶楚脚下叶楚身边叶楚面前"
           "叶神医叶兄弟叶大师叶大哥叶兄叶小友叶姑娘叶家众人叶楚闻言叶楚见此叶楚深处"
           "白什么叶楚颔首叶楚深吸叶楚体叶楚微微叶楚暗暗叶楚嘴角叶楚迅速叶楚淡淡"
           "叶楚满意叶楚郑重叶楚含笑叶楚压下叶楚重重叶楚心中叶楚轻轻叶楚在叶楚听后"
           "叶楚肯定叶楚没有叶楚连忙叶楚立刻叶楚见此叶楚嘴角叶楚一愣叶楚淡淡"
           "叶楚人士叶楚小姐叶楚夫人叶楚先生叶楚朋友叶楚大哥叶楚小叶楚叶楚"
           .split())

files = [f for f in sorted(D.glob("*.txt")) if f.name[0].isdigit()]
c = collections.Counter()
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"([\u4e00-\u9fff]{2,3})(?=[说道笑喝问答地、，。：“）\s])", t):
        s = m.group(1)
        if s[0] in SURNAME and s not in STOP:
            c[s] += 1

gl = pathlib.Path(r"f:/taitruyen/translate/glossary_can_bao_chan_long.txt").read_text(
    encoding="utf-8")
have = set(re.findall(r"[\u4e00-\u9fff]{2,4}", gl))
items = sorted(((v, k) for k, v in c.items() if v >= 12 and k not in have), reverse=True)
print("ung vien >=12:", len(items))
for v, k in items:
    print(v, k)
