"""Cấu hình cho scraper - load từ .env hoặc defaults."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_env() -> None:
    """Load .env nếu có, fallback defaults."""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        load_dotenv(env_file)


def _get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def _get_float(key: str, default: float) -> float:
    try:
        return float(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def _get_bool(key: str, default: bool) -> bool:
    val = os.getenv(key, "").strip().lower()
    if val in ("true", "1", "yes", "on"):
        return True
    if val in ("false", "0", "no", "off"):
        return False
    return default


_load_env()


@dataclass(frozen=True)
class Settings:
    """Application settings, frozen để chống mutation."""

    # === HTTP ===
    base_url: str = "https://truyendich.space"
    request_timeout: int = field(default_factory=lambda: _get_int("REQUEST_TIMEOUT", 30))
    max_concurrent: int = field(default_factory=lambda: _get_int("MAX_CONCURRENT", 3))
    requests_per_second: float = field(default_factory=lambda: _get_float("REQUESTS_PER_SECOND", 0.7))
    max_retries: int = field(default_factory=lambda: _get_int("MAX_RETRIES", 4))
    backoff_factor: float = field(default_factory=lambda: _get_float("BACKOFF_FACTOR", 1.5))
    proxy_url: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_URL", "").strip() or None)
    enable_ua_rotation: bool = field(default_factory=lambda: _get_bool("ENABLE_UA_ROTATION", False))

    # === URLs ===
    sitemap_index_url: str = "https://truyendich.space/sitemap-index.xml"
    sitemap_url: str = "https://truyendich.space/sitemap-novels-1.xml"

    # === Storage ===
    raw_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("RAW_DIR", "data/raw")
    )
    novel_dir: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("NOVEL_DIR", "data/novels")
    )

    # === Logging ===
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper())
    log_file: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("LOG_FILE", "logs/scraper.log")
    )

    # === Behavior ===
    resume_from_cache: bool = field(default_factory=lambda: _get_bool("RESUME_FROM_CACHE", True))
    save_raw_html: bool = field(default_factory=lambda: _get_bool("SAVE_RAW_HTML", False))


# URL patterns đã xác minh từ HTML
CHAPTER_URL_PATTERN = "/doc-truyen/{slug}/chuong-{n}"
AI_CHAPTER_URL_PATTERN = "/doc-truyen/ai/{slug}/chuong-{n}"
NOVEL_URL_PATTERN = "/doc-truyen/{slug}"


# Singleton accessor
_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        # tạo folders lazy
        _settings.raw_dir.mkdir(parents=True, exist_ok=True)
        _settings.novel_dir.mkdir(parents=True, exist_ok=True)
        _settings.log_file.parent.mkdir(parents=True, exist_ok=True)
    return _settings
