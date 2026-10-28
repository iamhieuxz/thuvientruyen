"""JSON cache theo từng novel - hỗ trợ resume & incremental save."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from ..config import get_settings
from ..logging_config import get_logger
from ..models import Chapter, Novel


log = get_logger(__name__)


class Cache:
    """Cache dạng JSON - 1 file / novel.

    File layout:
        data/novels/{slug}/meta.json     -> Novel metadata
        data/novels/{slug}/chapters/{n}.json  -> Chapter data
    """

    def __init__(self, root: Optional[Path] = None):
        s = get_settings()
        self.root: Path = (root or s.novel_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def novel_dir(self, slug: str) -> Path:
        p = self.root / slug
        (p / "chapters").mkdir(parents=True, exist_ok=True)
        return p

    # === Meta ===
    def save_meta(self, novel: Novel) -> Path:
        path = self.novel_dir(novel.slug) / "meta.json"
        path.write_text(
            json.dumps(novel.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        log.info("Saved meta: %s", path)
        return path

    def load_meta(self, slug: str) -> Optional[Novel]:
        path = self.novel_dir(slug) / "meta.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return Novel(**data)
        except (json.JSONDecodeError, ValueError) as e:
            log.warning("meta.json lỗi (%s): %s", slug, e)
            return None

    # === Chapter ===
    def chapter_path(self, slug: str, n: int) -> Path:
        return self.novel_dir(slug) / "chapters" / f"{n:05d}.json"

    def has_chapter(self, slug: str, n: int) -> bool:
        return self.chapter_path(slug, n).exists()

    def save_chapter(self, chapter: Chapter) -> Path:
        path = self.chapter_path(chapter.novel_slug, chapter.chapter_number)
        path.write_text(
            json.dumps(chapter.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def load_chapter(self, slug: str, n: int) -> Optional[Chapter]:
        path = self.chapter_path(slug, n)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return Chapter(**data)
        except (json.JSONDecodeError, ValueError):
            return None

    def list_cached_chapters(self, slug: str) -> list[int]:
        d = self.novel_dir(slug) / "chapters"
        if not d.exists():
            return []
        nums: list[int] = []
        for f in d.glob("*.json"):
            try:
                nums.append(int(f.stem))
            except ValueError:
                continue
        return sorted(nums)
