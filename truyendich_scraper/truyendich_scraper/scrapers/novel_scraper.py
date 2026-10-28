"""Cào metadata + danh sách chương từ trang index novel."""
from __future__ import annotations

from typing import Optional

import aiohttp

from ..config import NOVEL_URL_PATTERN, get_settings
from ..http_client import HttpClient
from ..logging_config import get_logger
from ..models import Novel
from ..parsers.novel import NovelIndexParser
from ..storage.cache import Cache


log = get_logger(__name__)


class NovelScraper:
    def __init__(
        self,
        http: HttpClient,
        cache: Cache,
        parser: Optional[NovelIndexParser] = None,
    ):
        self.http = http
        self.cache = cache
        self.parser = parser or NovelIndexParser()

    async def scrape_index(self, slug: str) -> Novel:
        """Fetch novel index page, parse metadata + chapter list."""
        url = f"{get_settings().base_url}{NOVEL_URL_PATTERN.format(slug=slug)}"
        html = await self.http.fetch(url)
        novel = self.parser.parse(html, slug=slug)
        # Merge với cache meta cũ nếu có (để không mất chapters đã scrape)
        existing = self.cache.load_meta(slug)
        if existing and existing.chapters and len(existing.chapters) > len(novel.chapters):
            novel.chapters = existing.chapters
        self.cache.save_meta(novel)
        log.info(
            "Novel %s: title=%s | chapters=%d", slug, novel.title, novel.total_chapters
        )
        return novel
