"""Smoke test cho ChapterParser (không cần mạng)."""
import asyncio
import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT
sys.path.insert(0, str(SRC))

from truyendich_scraper.parsers.chapter import ChapterParser


SAMPLE = """
<!DOCTYPE html><html lang="vi">
<body>
  <section class="prose-novel font-modern" itemprop="text" style="font-size:22px">
    <div id="original-content-tab" class="transition">
      <p><content></content></p>
      <p>Chương 1: Huynh Muội</p>
      <p>"Ca, ta lượm được một tấm phiếu lương thực năm cân!"</p>
      <p>Theo một tiếng kêu ngạc nhiên, tại một đống rác ...</p>
      <p>Cuối cùng cũng kể xong.</p>
    </div>
  </section>
</body>
</html>
"""


def test_parse_minimal():
    p = ChapterParser()
    ch = p.parse(
        SAMPLE,
        slug="test",
        chapter_number=1,
        url="https://truyendich.space/doc-truyen/test/chuong-1",
    )
    assert ch is not None, "Parser trả về None"
    assert ch.novel_slug == "test"
    assert ch.chapter_number == 1
    assert "Huynh Muội" in ch.title or "Chương 1" in ch.title
    assert "phiếu lương thực" in ch.content
    assert "Cuối cùng" in ch.content
    # Bỏ <p><content> placeholder
    assert "<content>" not in ch.content
    assert ch.word_count > 0
    print("[OK] parse_minimal")


def test_parse_invalid():
    p = ChapterParser()
    ch = p.parse("<html>không có gì</html>", slug="x", chapter_number=1, url="")
    assert ch is None, "Phải trả về None cho HTML không có prose-novel"
    print("[OK] parse_invalid")


if __name__ == "__main__":
    test_parse_minimal()
    test_parse_invalid()
    print("All tests passed!")
