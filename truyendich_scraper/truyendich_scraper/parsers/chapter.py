"""Parser trích một chương từ HTML của trang chapter.

Selectors đã xác minh từ mã nguồn trang:
  - Nội dung: <section class="prose-novel ..." itemprop="text">
                <div id="original-content-tab">... <p>...</p> ...
  - Tiêu đề phụ: <h1 ... itemprop="name">
  - Số chương: <p ... uppercase ...>Chương X</p>
  - Ngày đăng: <time datetime="..." itemprop="datePublished">
  - Tác giả: nằm sau time, trong cùng <p>
  - URL: trong nav prev/next <a href=".../chuong-X">
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup, Tag

from ..models import Chapter


_CHAPTER_TITLE_RE = re.compile(r"Chương (\d+)", re.IGNORECASE)


class ChapterParser:
    """Singleton đơn giản - không stateful."""

    def parse(
        self,
        html: str,
        slug: str,
        chapter_number: int,
        url: str,
        edition: str = "default",
    ) -> Optional[Chapter]:
        """Parse HTML thành Chapter.

        Trả về None nếu trang lỗi / không tìm thấy nội dung.
        """
        if not html:
            return None
        soup = BeautifulSoup(html, "lxml")

        section = soup.find("section", class_=re.compile(r"\bprose-novel\b"))
        if section is None:
            return None

        content_div = section.find("div", id="original-content-tab") or section
        paragraphs: list[str] = []
        for p in content_div.find_all("p"):
            txt = p.get_text(" ", strip=True)
            # Bỏ đoạn title placeholder
            if txt and txt.lower() != "<content></content>":
                # Nếu chính là "Chương X: Tiêu đề" -> trích title, không cho vào content
                m = _CHAPTER_TITLE_RE.match(txt)
                if m and int(m.group(1)) == chapter_number and ":" in txt:
                    title_inline = txt.split(":", 1)[1].strip()
                    if title_inline:
                        paragraphs.append(title_inline)
                    continue
                paragraphs.append(txt)

        if not paragraphs:
            return None

        title = self._extract_title(soup, chapter_number)
        author = self._extract_author(soup)
        published_at = self._extract_published_at(soup)

        return Chapter(
            novel_slug=slug,
            chapter_number=chapter_number,
            title=title or f"Chương {chapter_number}",
            content="\n\n".join(paragraphs),
            url=url,
            author=author,
            published_at=published_at,
            edition=edition,
        )

    @staticmethod
    def _extract_title(soup: BeautifulSoup, chapter_number: int) -> Optional[str]:
        h1 = soup.find("h1", itemprop="name")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        # Fallback: tìm trong <header> <p> trên cùng với "Chương X"
        header = soup.find("header")
        if header:
            for tag in header.find_all(["p", "h1", "h2"]):
                t = tag.get_text(" ", strip=True)
                if t.startswith(f"Chương {chapter_number}") and ":" in t:
                    return t.split(":", 1)[1].strip()
        return None

    @staticmethod
    def _extract_author(soup: BeautifulSoup) -> Optional[str]:
        # Format thường gặp:
        # <header>...<time>...</time><span>|</span>Tác Giả</p>
        header = soup.find("header")
        if header:
            time_tag = header.find("time")
            if time_tag:
                # Lấy chữ đứng sau <span>|</span>
                parent_p = time_tag.parent
                if parent_p:
                    raw = parent_p.get_text(" ", strip=True)
                    parts = [x.strip() for x in raw.split("|") if x.strip()]
                    for p in parts:
                        if not p.endswith(":") and not p.startswith("Chương"):
                            # Loại mọi token thời gian
                            if re.search(r"\d{4}|\d+:\d+", p) and not any(
                                v in p.lower() for v in ("tác giả", "author")
                            ):
                                continue
                            return p
        return None

    @staticmethod
    def _extract_published_at(soup: BeautifulSoup) -> Optional[datetime]:
        time_tag = soup.find("time", itemprop="datePublished")
        if not time_tag or not time_tag.get("datetime"):
            return None
        try:
            raw = time_tag["datetime"]
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None
