"""Vá các chương bị thiếu nội dung trên ixdzs8 bằng bản mirror fxnzw.

Chỉ dùng cho bộ "警报！真龙出狱！": TXT của ixdzs8 có 11 chương chỉ có
tiêu đề, trang chương trả "内容还在处理中". fxnzw (飞翔鸟中文) có nội dung
các chương đó.

Script đọc _meta.json của folder, tải các chương thiếu, ghi file
{number:04d}_{title}.txt, rồi cập nhật _toc.txt / _meta.json /
_thieu-noi-dung.txt.

Chạy:
  python fxnzw_fill_gaps.py
"""

from __future__ import annotations

import html
import json
import os
import re
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "canh-bao-chan-long-xuat-nguc"
BOOK_ID = "52101"
BASE = "https://www.fxnzw.com"
CATALOG = f"{BASE}/chapternum/{BOOK_ID}/1400_1500.html"
PATH_PREFIX = f"/fxnread/{BOOK_ID}_"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
INVALID_FILENAME = re.compile(r'[\\/:*?"<>|]')

# Trang fxnzw của 2 chương này bị trộn nội dung từ truyện khác, không dùng.
BLACKLIST = {1408, 1429}


def log(msg: str) -> None:
    print(msg, flush=True)


def get(url: str, retries: int = 4) -> str:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as resp:
                raw = resp.read()
            for enc in ("utf-8", "gb18030"):
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", errors="ignore")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
            wait = 2 + attempt * 2
            log(f"  ! loi {url}: {exc}; thu lai sau {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Khong tai duoc {url}: {last}")


def safe_name(name: str, limit: int = 80) -> str:
    name = INVALID_FILENAME.sub("_", name).strip(" .")
    return name[:limit] or "untitled"


def map_chapters() -> dict[int, str]:
    soup = BeautifulSoup(get(CATALOG), "lxml")
    mapping: dict[int, str] = {}
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        m = re.search(r"第(\d+)章", text)
        if not m or not a["href"].startswith(PATH_PREFIX):
            continue
        mapping[int(m.group(1))] = BASE + a["href"]
    return mapping


def extract_chapter(url: str) -> str:
    soup = BeautifulSoup(get(url), "lxml")
    box = soup.find("div", id="Lab_Contents")
    if box is None:
        return ""
    paras: list[str] = []
    for p in box.find_all("p"):
        text = html.unescape(p.get_text(" ", strip=True)).strip()
        if not text:
            continue
        if "←→" in text or "_警报！真龙出狱！" in text:
            continue
        if text.startswith("新书推荐"):
            break
        if text.startswith("第一卷第") and "警报" in text:
            continue
        paras.append(text)
    return "\n\n".join(paras).strip()


def write_toc(out_dir: str, chapters: list[dict], missing: set[int]) -> None:
    lines = []
    for ch in chapters:
        n = ch["number"]
        marker = "\t[nguồn thiếu nội dung]" if n in missing else ""
        lines.append(f"{n:04d}\t第{n}章 {ch['title']}{marker}")
    with open(os.path.join(out_dir, "_toc.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def write_missing_note(out_dir: str, chapters: list[dict], missing: set[int]) -> None:
    path = os.path.join(out_dir, "_thieu-noi-dung.txt")
    if not missing:
        if os.path.exists(path):
            os.remove(path)
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("Các chương sau vẫn không có nội dung sau khi vá từ fxnzw:\n\n")
        for ch in chapters:
            if ch["number"] in missing:
                f.write(f"{ch['number']:04d}\t第{ch['number']}章 {ch['title']}\n")


def main() -> None:
    out_dir = os.path.join(ROOT, SLUG)
    meta_path = os.path.join(out_dir, "_meta.json")
    meta = json.load(open(meta_path, encoding="utf-8"))
    missing = [int(n) for n in meta.get("empty_chapters", [])]
    if not missing:
        log("Khong co chuong nao thieu noi dung.")
        return

    toc_text = open(os.path.join(out_dir, "_toc.txt"), encoding="utf-8").read()
    chapters = []
    for line in toc_text.splitlines():
        parts = line.split("\t")
        m = re.match(r"第(\d+)章\s*(.*)", parts[1])
        if m:
            chapters.append({"number": int(m.group(1)), "title": m.group(2)})
    by_num = {c["number"]: c for c in chapters}

    log(f"Can va {len(missing)} chuong: {missing}")
    url_map = map_chapters()
    log(f"Catalog co {len(url_map)} chuong")

    filled: dict[int, dict] = {}
    for n in missing:
        if n in BLACKLIST:
            log(f"  ! bo qua {n}: trang fxnzw bi tron noi dung truyen khac")
            continue
        url = url_map.get(n)
        if not url:
            log(f"  ! khong tim thay URL chuong {n}")
            continue
        text = extract_chapter(url)
        if len(text) < 500:
            log(f"  ! chuong {n} van rong/ngan ({len(text)} ky tu): {url}")
            continue
        ch = by_num[n]
        fname = f"{n:04d}_{safe_name(ch['title'])}.txt"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8", newline="\n") as f:
            f.write(f"第{n}章 {ch['title']}\n\n{text}\n")
        filled[n] = {"number": n, "title": ch["title"], "url": url, "chars": len(text)}
        log(f"  + {n:04d} {ch['title']} ({len(text)} ky tu)")
        time.sleep(0.7)

    remaining = sorted(set(missing) - set(filled))
    write_toc(out_dir, chapters, set(remaining))
    write_missing_note(out_dir, chapters, set(remaining))

    meta["chapters_written"] = int(meta.get("chapters_written", 0)) + len(filled)
    meta["empty_chapters"] = remaining
    meta["supplemented_chapters"] = list(filled.values())
    meta["total_chars"] = int(meta.get("total_chars", 0)) + sum(v["chars"] for v in filled.values())
    meta["notes"] = (
        "11 chương thiếu nội dung trên ixdzs8 đã được vá từ fxnzw; "
        "các chương còn lại trong empty_chapters là chưa vá được."
    )
    with open(meta_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

    log(
        f"\nDa va {len(filled)}/{len(missing)} chuong. "
        f"Con thieu: {remaining if remaining else 'khong'}"
    )


if __name__ == "__main__":
    main()
