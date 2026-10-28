"""Pydantic models cho dữ liệu crawl về."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Chapter(BaseModel):
    """Một chương truyện sau khi parse."""

    novel_slug: str
    chapter_number: int = Field(ge=1)
    title: str                           # tiêu đề phụ (vd "Huynh Muội")
    content: str                         # các <p> nối bằng \n\n
    url: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    edition: str = "default"             # default | ai | cv
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    word_count: int = 0

    def model_post_init(self, *_) -> None:
        # Tính word count (đếm cả ký tự CJK)
        self.word_count = len(self.content)


class Novel(BaseModel):
    """Metadata cấp truyện."""

    slug: str                            # url-friendly id
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    status: Optional[str] = None         # ongoing/finished
    total_chapters: Optional[int] = None
    updated_at: Optional[datetime] = None
    chapters: list[Chapter] = Field(default_factory=list)
