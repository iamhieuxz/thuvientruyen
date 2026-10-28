"""Logging có cấu trúc cho scraper."""
from __future__ import annotations

import logging
import sys

from .config import get_settings


_FMT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def setup_logging() -> None:
    """Khởi tạo logging đồng nhất cho CLI + library."""
    settings = get_settings()
    root = logging.getLogger()
    if root.handlers:
        return  # tránh duplicate khi gọi nhiều lần

    root.setLevel(settings.log_level)

    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter(_FMT))
    root.addHandler(console)

    # File handler
    try:
        file_h = logging.FileHandler(settings.log_file, encoding="utf-8")
        file_h.setFormatter(logging.Formatter(_FMT))
        root.addHandler(file_h)
    except OSError:
        pass  # nếu không ghi file được thì bỏ qua

    # Tắt log ồn từ thư viện bên thứ ba
    for noisy in ("fake_useragent", "aiohttp.access", "asyncio", "charset_normalizer"):
        logging.getLogger(noisy).setLevel(logging.ERROR)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
