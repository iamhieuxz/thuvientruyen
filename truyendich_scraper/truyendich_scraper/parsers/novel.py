"""Parser trích metadata truyện + danh sách chương từ novel index page.

Selectors:
  - Slug: lấy từ URL path /doc-truyen/{slug} (xác minh)
  - Chapters: <a href="/doc-truyen/{slug}/chuong-X">X</a>
  - Đã xác minh: tìm được 56 chương trong 1 lần load (đầu/cuối)
  - Danh sách ở giữa bị phân trang (cần đào sâu hơn nếu cần)
  - Title / Author: từ itemprop="name" trên <h1>
"""
from __future__ import annotations

import re
from typing import Optional

from bs4 import BeautifulSoup

from ..models import Novel


_CHAPTER_LINK_RE = re.compile(
    r"^/doc-truyen/(?:ai/|cv/)?(?P<slug>[a-z0-9\-]+)/chuong-(?P<num>\d+)$"
)


class NovelIndexParser:
    def parse(self, html: str, slug: str, fallback_title: Optional[str] = None) -> Novel:
        soup = BeautifulSoup(html, "lxml")

        # Title
        title = None
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
        if not title:
            og = soup.find("meta", attrs={"property": "og:title"})
            if og and og.get("content"):
                title = og["content"].replace(" | TruyenDichAI", "").strip()
        if not title and fallback_title:
            title = fallback_title

        # Description
        description = None
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()

        # Author
        author = None
        jsonld_text = soup.find("script", type="application/ld+json")
        if jsonld_text:
            import json
            try:
                data = json.loads(jsonld_text.string or "{}")
                if isinstance(data.get("author"), dict):
                    author = data["author"].get("name")
                elif isinstance(data.get("author"), str):
                    author = data["author"]
            except (json.JSONDecodeError, AttributeError):
                pass

        novel = Novel(
            slug=slug,
            title=title,
            description=description,
            author=author,
        )

        # Danh sách chapter (chỉ lấy những link hiển thị trong DOM)
        chapter_links: set[int] = set()
        for a in soup.find_all("a", href=True):
            m = _CHAPTER_LINK_RE.match(a["href"])
            if not m or m.group("slug") != slug:
                continue
            try:
                chapter_links.add(int(m.group("num")))
            except ValueError:
                continue

        # Không lưu chapter object ở index (cần body); chỉ save số
        for n in sorted(chapter_links):
            # Mỗi entry stub; chapter_scraper sẽ thay thế
            from ..models import Chapter
            novel.chapters.append(
                Chapter(
                    novel_slug=slug,
                    chapter_number=n,
                    title=f"Chương {n}",
                    content="",
                    url=f"https://truyendich.space/doc-truyen/{slug}/chuong-{n}",
                )
            )
        novel.total_chapters = len(novel.chapters)
        return novel

    def extract_chapter_numbers(self, html: str, slug: str) -> list[int]:
        """Trả về list các số chương có trong DOM."""
        soup = BeautifulSoup(html, "lxml")
        nums: set[int] = set()
        for a in soup.find_all("a", href=True):
            m = _CHAPTER_LINK_RE.match(a["href"])
            if not m or m.group("slug") != slug:
                continue
            try:
                nums.add(int(m.group("num")))
            except ValueError:
                continue
        return sorted(nums)
