"""Cào danh sách truyện từ sitemap + lưu index.json."""
from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Optional

import aiohttp

from ..config import get_settings
from ..http_client import HttpClient
from ..logging_config import get_logger


log = get_logger(__name__)

_SITEMAP_INDEX_RE = re.compile(r"<loc>(?P<url>[^<]+sitemap[^<]+)</loc>", re.IGNORECASE)
_NOVEL_LOC_RE = re.compile(
    r"<loc>(?P<url>https?://[^<]+/doc-truyen/[a-z0-9\-]+)</loc>"
)


async def fetch_sitemap_urls(sitemap_url: str, http: HttpClient) -> list[str]:
    """Trả về tất cả <loc> trong một sitemap xml.

    Nếu sitemap_url là sitemapindex -> trích các sitemap con trước.
    """
    html = await http.fetch(sitemap_url)
    # Nếu là sitemapindex -> recurse vào các sitemap con
    if "<sitemapindex" in html or "<sitemap>" in html:
        sub = _SITEMAP_INDEX_RE.findall(html)
        all_urls: list[str] = []
        for s in sub:
            log.info("Sub-sitemap: %s", s)
            all_urls.extend(await fetch_sitemap_urls(s, http))
        return all_urls
    return _NOVEL_LOC_RE.findall(html)


async def list_novels_from_sitemap(output: Path) -> int:
    """Lưu tất cả URL novel theo sitemap. Trả về số lượng."""
    s = get_settings()
    async with HttpClient() as http:
        urls = await fetch_sitemap_urls(s.sitemap_url, http)
    output.parent.mkdir(parents=True, exist_ok=True)
    slugs = []
    for u in urls:
        # Lấy slug cuối URL
        slug = u.rstrip("/").split("/")[-1]
        slugs.append({"slug": slug, "url": u})
    output.write_text(
        json.dumps(slugs, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log.info("Saved %d novels to %s", len(slugs), output)
    return len(slugs)
