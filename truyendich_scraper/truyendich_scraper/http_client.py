"""Async HTTP client với rate-limit, retry, UA rotation."""
from __future__ import annotations

import asyncio
import logging
import random
from typing import Awaitable, Callable, Optional

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

try:
    from fake_useragent import UserAgent
    _HAS_FAKE_UA = True
except ImportError:
    _HAS_FAKE_UA = False

from .config import get_settings
from .logging_config import get_logger


log = get_logger(__name__)


# === User-Agent pool tĩnh ===
# Lưu ý: fake_useragent cần network để tải dataset và rất chậm (hoặc fail)
# với site không cho phép. Vì vậy ưu tiên pool tĩnh, chỉ dùng fake_useragent
# nếu người dùng BẬT tường minh qua .env.
_DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_FALLBACK_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
]


def _init_user_agents() -> list[str]:
    """Lấy pool UA.

    - Nếu tắt rotation -> 1 UA duy nhất.
    - Nếu bật -> thử fake_useragent, nhưng chỉ 1 lần và fallback ngay
      nếu lỗi/không có mạng (tránh spam & độ trễ).
    """
    settings = get_settings()
    if not settings.enable_ua_rotation:
        return [_DEFAULT_UA]

    if _HAS_FAKE_UA:
        try:
            ua = UserAgent(min_percentage=1.5)
            agents: set[str] = set()
            # Giới hạn số lần thử để không bị treo
            for _ in range(12):
                try:
                    agents.add(ua.random)
                except Exception:
                    break
            if agents:
                log.debug("fake_useragent: lấy %d UA", len(agents))
                return list(agents)
        except Exception as e:
            log.warning("fake_useragent lỗi (%s) -> dùng pool tĩnh", e)

    return list(_FALLBACK_UAS)


class RateLimiter:
    """Token-bucket đơn giản để giới hạn requests/giây."""

    def __init__(self, rate_per_second: float, max_concurrent: int = 3):
        self._interval = 1.0 / max(rate_per_second, 0.1)
        self._sem = asyncio.Semaphore(max_concurrent)
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        await self._sem.acquire()
        async with self._lock:
            now = asyncio.get_event_loop().time()
            wait_for = self._interval - (now - self._last)
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            self._last = asyncio.get_event_loop().time()

    def release(self) -> None:
        self._sem.release()


class HttpClient:
    """Async HTTP client wrapper.

    Sử dụng:
        async with HttpClient() as http:
            html = await http.fetch(url)
    """

    def __init__(self):
        s = get_settings()
        self._rate_limiter = RateLimiter(s.requests_per_second, s.max_concurrent)
        self._timeout = aiohttp.ClientTimeout(total=s.request_timeout)
        self._proxy: Optional[str] = s.proxy_url
        self._headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache",
        }
        self._ua_pool = _init_user_agents()
        self._session: Optional[aiohttp.ClientSession] = None
        self._connector: Optional[aiohttp.TCPConnector] = None

    async def __aenter__(self) -> "HttpClient":
        await self.start()
        return self

    async def __aexit__(self, *_exc) -> None:
        await self.close()

    async def start(self) -> None:
        if self._session is not None:
            return
        # Limit connections cứng ở tầng connector để tránh flood
        s = get_settings()
        self._connector = aiohttp.TCPConnector(
            limit=s.max_concurrent * 2,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
            ssl=False,           # tránh một số vấn đề về SSL handshake
        )
        self._session = aiohttp.ClientSession(
            timeout=self._timeout,
            connector=self._connector,
            headers=self._headers,
        )

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
        if self._connector is not None:
            await self._connector.close()
            self._connector = None

    def _pick_ua(self) -> str:
        return random.choice(self._ua_pool)

    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        stop=stop_after_attempt(4),   # KHÔNG dùng setting để tránh lỗi đóng băng
        wait=wait_exponential(multiplier=1.5, min=1, max=20),
        before_sleep=before_sleep_log(log, logging.WARNING),
        reraise=True,
    )
    async def fetch(self, url: str, *, max_retries: int | None = None) -> str:
        """Fetch HTML với retry + rate-limit.

        Raises:
            aiohttp.ClientResponseError: nếu 4xx/5xx
        """
        if self._session is None:
            await self.start()

        await self._rate_limiter.acquire()
        try:
            headers = {"User-Agent": self._pick_ua()}
            log.debug("GET %s", url)
            async with self._session.get(
                url, headers=headers, proxy=self._proxy
            ) as resp:
                if resp.status == 403:
                    log.warning("403 Forbidden: %s", url)
                resp.raise_for_status()
                return await resp.text(encoding="utf-8")
        finally:
            self._rate_limiter.release()
