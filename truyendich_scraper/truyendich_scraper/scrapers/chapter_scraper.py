"""Cào một chương / danh sách chương với concurrency + resume."""
from __future__ import annotations

import asyncio
from typing import Iterable, Optional

from tqdm.asyncio import tqdm_asyncio

from ..config import CHAPTER_URL_PATTERN, get_settings
from ..http_client import HttpClient
from ..logging_config import get_logger
from ..models import Chapter
from ..parsers.chapter import ChapterParser
from ..storage.cache import Cache


log = get_logger(__name__)


class ChapterScraper:
    def __init__(
        self,
        http: HttpClient,
        cache: Cache,
        parser: Optional[ChapterParser] = None,
    ):
        self.http = http
        self.cache = cache
        self.parser = parser or ChapterParser()

    async def scrape_one(
        self,
        slug: str,
        chapter_number: int,
        *,
        force: bool = False,
        edition: str = "default",
    ) -> Optional[Chapter]:
        """Cào 1 chương; cache-first."""
        if not force and self.cache.has_chapter(slug, chapter_number):
            ch = self.cache.load_chapter(slug, chapter_number)
            log.debug("Cache hit: %s ch.%s", slug, chapter_number)
            return ch

        path = CHAPTER_URL_PATTERN.format(slug=slug, n=chapter_number)
        url = f"{get_settings().base_url}{path}"

        try:
            html = await self.http.fetch(url)
        except Exception as e:
            log.error("Lỗi fetch ch.%s của %s: %s", chapter_number, slug, e)
            return None

        ch = self.parser.parse(html, slug, chapter_number, url, edition=edition)
        if ch is None:
            log.warning("Parse rỗng: %s", url)
            return None

        self.cache.save_chapter(ch)
        log.debug("Saved ch.%s (%d words)", chapter_number, ch.word_count)
        return ch

    async def scrape_range(
        self,
        slug: str,
        start: int,
        end: int,
        *,
        force: bool = False,
        show_progress: bool = True,
    ) -> list[Chapter]:
        """Cào nhiều chương liên tục, tự dừng khi gặp 403 (truyện kết thúc)."""
        results: list[Chapter] = []
        semaphore = asyncio.Semaphore(get_settings().max_concurrent)

        async def _task(n: int) -> Chapter | None:
            async with semaphore:
                # Dùng client của self (đã được init)
                return await self.scrape_one(slug, n, force=force)

        tasks = [_task(n) for n in range(start, end + 1)]

        if show_progress:
            results_iter = await tqdm_asyncio.gather(
                *tasks, total=len(tasks), desc=f"Scraping {slug}"
            )
        else:
            results_iter = await asyncio.gather(*tasks)

        results = [ch for ch in results_iter if ch is not None]
        log.info("Scrape xong %s: %d/%d chương", slug, len(results), end - start + 1)
        return results
