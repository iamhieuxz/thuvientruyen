"""Exporters: gộp cached chapters thành JSON/TXT thân thiện."""
from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ..models import Chapter, Novel
from .cache import Cache


@dataclass
class Exporter:
    cache: Cache

    # === JSON gộp ===
    def export_json(self, slug: str, output: Path) -> Path:
        novel = self.cache.load_meta(slug) or Novel(slug=slug)
        chapters: list[Chapter] = []
        for n in self.cache.list_cached_chapters(slug):
            ch = self.cache.load_chapter(slug, n)
            if ch:
                chapters.append(ch)
        novel.chapters = sorted(chapters, key=lambda c: c.chapter_number)

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(novel.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return output

    # === TXT thuần (1 file / novel) ===
    def export_txt(
        self,
        slug: str,
        output: Path,
        novel_title: str | None = None,
        author: str | None = None,
    ) -> Path:
        title = novel_title or slug
        lines: list[str] = []
        for n in self.cache.list_cached_chapters(slug):
            ch = self.cache.load_chapter(slug, n)
            if not ch or not ch.content:
                continue
            lines.append("=" * 70)
            lines.append(f"Chương {ch.chapter_number}: {ch.title}")
            lines.append("=" * 70)
            lines.append("")
            lines.append(ch.content)
            lines.append("")

        output.parent.mkdir(parents=True, exist_ok=True)
        header = f"{title}\nTác giả: {author or 'N/A'}\n{'='*70}\n\n"
        output.write_text(header + "\n".join(lines), encoding="utf-8")
        return output
