"""CLI entrypoint: argparse dispatch các sub-lệnh.

Sử dụng:
    python -m truyendich_scraper.cli scrape --slug bao-giam --start 1 --end 1184
    python -m truyendich_scraper.cli novels --from-sitemap
    python -m truyendich_scraper.cli test --slug bao-giam --chapter 1
    python -m truyendich_scraper.cli export --slug bao-giam --format json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .http_client import HttpClient
from .logging_config import setup_logging, get_logger
from .scrapers.chapter_scraper import ChapterScraper
from .scrapers.novel_list_scraper import list_novels_from_sitemap
from .scrapers.novel_scraper import NovelScraper
from .storage.cache import Cache
from .storage.exporter import Exporter


log = get_logger(__name__)


# ============================================================================
# Subcommand: scrape (1 novel, range chapters)
# ============================================================================
async def _cmd_scrape(args: argparse.Namespace) -> int:
    cache = Cache()
    async with HttpClient() as http:
        novel_scraper = NovelScraper(http, cache)
        novel = await novel_scraper.scrape_index(args.slug)

        if args.max_chapters:
            end = min(args.max_chapters, novel.total_chapters or args.end)
        else:
            end = args.end
        start = max(1, args.start)

        ch_scraper = ChapterScraper(http, cache)
        chapters = await ch_scraper.scrape_range(
            args.slug, start, end, force=args.force
        )

        # cập nhật meta với list chapter mới
        novel.chapters = chapters
        cache.save_meta(novel)
    log.info("Done. %d chương lưu cache tại %s", len(chapters), cache.novel_dir(args.slug))
    return 0


# ============================================================================
# Subcommand: test (1 chapter)
# ============================================================================
async def _cmd_test(args: argparse.Namespace) -> int:
    cache = Cache()
    async with HttpClient() as http:
        ch_scraper = ChapterScraper(http, cache)
        ch = await ch_scraper.scrape_one(args.slug, args.chapter, force=args.force)
        if ch:
            print(json.dumps(ch.model_dump(mode="json"), ensure_ascii=False, indent=2))
            print(f"\n--- INFO ---")
            print(f"Slug: {ch.novel_slug}")
            print(f"Chapter: {ch.chapter_number} - {ch.title}")
            print(f"Word count: {ch.word_count}")
            print(f"Author: {ch.author}")
            print(f"Published: {ch.published_at}")
            return 0
        return 1


# ============================================================================
# Subcommand: novels (sitemap)
# ============================================================================
async def _cmd_novels(args: argparse.Namespace) -> int:
    if args.from_sitemap:
        out = Path(args.output)
        n = await list_novels_from_sitemap(out)
        print(f"Saved {n} novels to {out}")
        return 0
    print("Chưa implement: --from-index", file=sys.stderr)
    return 1


# ============================================================================
# Subcommand: export
# ============================================================================
def _cmd_export(args: argparse.Namespace) -> int:
    cache = Cache()
    exporter = Exporter(cache)
    if args.format == "json":
        out = Path(args.output or f"data/exports/{args.slug}.json")
        path = exporter.export_json(args.slug, out)
        print(f"Exported JSON: {path}")
    elif args.format == "txt":
        novel = cache.load_meta(args.slug)
        out = Path(args.output or f"data/exports/{args.slug}.txt")
        path = exporter.export_txt(
            args.slug, out,
            novel_title=novel.title if novel else None,
            author=novel.author if novel else None,
        )
        print(f"Exported TXT: {path}")
    else:
        print(f"Unsupported format: {args.format}", file=sys.stderr)
        return 1
    return 0


# ============================================================================
# CLI parser
# ============================================================================
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="truyendich-scraper",
        description="Cào truyện từ truyendich.space phục vụ đọc cá nhân.",
    )
    p.add_argument("--log-level", default=None)

    sub = p.add_subparsers(dest="command", required=True)

    # ---- scrape ----
    sp_scrape = sub.add_parser("scrape", help="Cào 1 truyện")
    sp_scrape.add_argument("--slug", required=True)
    sp_scrape.add_argument("--start", type=int, default=1)
    sp_scrape.add_argument("--end", type=int, default=100)
    sp_scrape.add_argument("--max-chapters", type=int, default=None,
                           help="Giới hạn số chương (override --end)")
    sp_scrape.add_argument("--force", action="store_true", help="Bỏ qua cache")
    sp_scrape.set_defaults(func=_cmd_scrape)

    # ---- test ----
    sp_test = sub.add_parser("test", help="Cào 1 chương thử nghiệm")
    sp_test.add_argument("--slug", required=True)
    sp_test.add_argument("--chapter", type=int, required=True)
    sp_test.add_argument("--force", action="store_true")
    sp_test.set_defaults(func=_cmd_test)

    # ---- novels ----
    sp_nov = sub.add_parser("novels", help="Lấy danh sách novel từ sitemap")
    nov = sp_nov.add_mutually_exclusive_group(required=True)
    nov.add_argument("--from-sitemap", action="store_true")
    sp_nov.add_argument("--output", default="data/novels/index.json")
    sp_nov.set_defaults(func=_cmd_novels)

    # ---- export ----
    sp_exp = sub.add_parser("export", help="Xuất novel đã cào thành JSON/TXT")
    sp_exp.add_argument("--slug", required=True)
    sp_exp.add_argument("--format", choices=["json", "txt"], default="json")
    sp_exp.add_argument("--output", default=None)
    sp_exp.set_defaults(func=_cmd_export)

    return p


# ============================================================================
# Entrypoint
# ============================================================================
def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.log_level:
        import logging
        logging.getLogger().setLevel(args.log_level.upper())

    func = args.func
    # Hàm có thể async hoặc sync
    if asyncio.iscoroutinefunction(func):
        result = asyncio.run(func(args))
    else:
        result = func(args)
    return result or 0


if __name__ == "__main__":
    sys.exit(main())
