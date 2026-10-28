# -*- coding: utf-8 -*-
"""Sinh tieu de tieng Viet hang loat cho cac chuong chua co trong titles_vi.json."""
import argparse
import json
import re
import sys
import time
import pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import dich  # noqa: E402

PROMPT = """Dịch tiêu đề chương tiểu thuyết Trung Quốc sang tiếng Việt.
Mỗi dòng: "số chương|tên Hán". Trả về mỗi dòng: "số chương: Tên Việt".
Quy tắc: ngắn (2-6 chữ), Hán Việt cho từ cổ trang, thoát ý tự nhiên,
không giữ chữ Hán, không thêm số thứ tự, không giải thích.

{items}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="lo", type=int, help="story so bat dau")
    ap.add_argument("--to", dest="hi", type=int, help="story so ket thuc")
    ap.add_argument("--chunk", type=int, default=50)
    ap.add_argument("--backend", default=None)
    a = ap.parse_args()

    dich.load_env()
    api = dich.BACKENDS[a.backend or __import__("os").environ.get("BACKEND", "openai")]
    cm = dich.load_chapter_map()
    titles = dich.load_titles()

    todo = sorted(s for v in cm.values()
                  if (s := v["story"]) and s not in titles
                  and (a.lo is None or s >= a.lo) and (a.hi is None or s <= a.hi))
    if not todo:
        print("Da co du tieu de.", flush=True)
        return
    print(f"{len(todo)} tieu de con thieu: {todo[0]}..{todo[-1]}", flush=True)

    path = HERE / "titles_vi.json"
    raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for i in range(0, len(todo), a.chunk):
        grp = todo[i:i + a.chunk]
        han = {v["story"]: v["title"] for v in cm.values() if v["story"]}
        items = "\n".join(f"{s}|{re.sub(r'^第.+?章[ 　]*', '', han[s])}" for s in grp)
        out = api(PROMPT.format(items=items))
        got = dict(re.findall(r"(?m)^\s*(\d{1,4})\s*[:：]\s*(.+?)\s*$", out))
        n = 0
        for s in grp:
            v = got.get(str(s))
            if not v or re.search(r"[\u4e00-\u9fff]", v):
                continue
            raw[str(s)] = f"Chương {s}: {v.strip().rstrip('。，,')}"
            n += 1
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"  +{n}/{len(grp)} (tong {len(raw)})", flush=True)
        time.sleep(0.5)
    missing = [s for s in todo if str(s) not in raw]
    if missing:
        print("THIEU:", missing[:20], flush=True)


if __name__ == "__main__":
    main()
