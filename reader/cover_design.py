#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cover_design.py — dựng bìa sách cho từng bộ truyện.

Mỗi bộ một bố cục riêng (A/A'/B/B'/C/C') nhưng dùng chung một "ngữ pháp" in ấn:
nhãn bộ TRUYỆN DỊCH + số thứ tự, gáy sách bên trái, viền chỉ mảnh, hạt phim,
tên truyện = chữ có dấu tiếng Việt (Sitka Display) nên không bị lỗi font.

Ảnh gốc (chưa chữ) nằm ở reader/static/img/art/<key>.jpg
Ảnh bìa hoàn chỉnh ghi ra reader/static/img/cover-*.jpg
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "static" / "img"
ART = IMG / "art"

W, H = 900, 1350

# ---------- font ----------
F_SERIF = ("C:/Windows/Fonts/Sitka.ttc", 5)        # Sitka Banner
F_SERIF_B = ("C:/Windows/Fonts/SitkaB.ttc", 4)     # Sitka Display Bold
F_SERIF_I = ("C:/Windows/Fonts/SitkaI.ttc", 4)     # Sitka Display Italic
F_SANS = ("C:/Windows/Fonts/Candara.ttf", 0)
F_SANS_B = ("C:/Windows/Fonts/Candarab.ttf", 0)
F_LIGHT = ("C:/Windows/Fonts/calibril.ttf", 0)
F_CJK = ("C:/Windows/Fonts/simsun.ttc", 0)

_fc: dict = {}


def F(spec, size: int) -> ImageFont.FreeTypeFont:
    key = (spec, size)
    if key not in _fc:
        path, idx = spec
        _fc[key] = ImageFont.truetype(path, size, index=idx)
    return _fc[key]


# ---------- màu ----------
def rgba(hexstr: str, a: int = 255) -> tuple:
    h = hexstr.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# ---------- chữ ----------
def tw(d: ImageDraw.ImageDraw, txt: str, f, tracking: float = 0) -> float:
    if not txt:
        return 0.0
    w = d.textlength(txt, font=f)
    return w + tracking * (len(txt) - 1)


def tracked(d, xy, txt, f, tracking=0.0, fill=(255, 255, 255, 255), anchor="ls"):
    """Vẽ chữ có giãn chữ cái. anchor: ls (trái, đường chân chữ), ms (giữa), rs (phải)."""
    total = tw(d, txt, f, tracking)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    if anchor[1] == "m":  # giữa theo chiều cao chữ hoa
        asc, desc = f.getmetrics()
        y += (asc - desc) / 2 - f.getbbox("H")[3] / 2
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + tracking
    return total


def fit(d, lines, spec, max_w, start, floor=26, tracking=0.0):
    """Thu cỡ chữ tới khi dòng dài nhất vừa bề ngang."""
    size = start
    while size > floor:
        f = F(spec, size)
        if max(tw(d, ln, f, tracking) for ln in lines) <= max_w:
            return F(spec, size)
        size -= 2
    return F(spec, floor)


# ---------- nền ----------
def cover_fit(im: Image.Image, w=W, h=H) -> Image.Image:
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def grade(im: Image.Image, accent: str, sat=0.90, contrast=1.06, tint=0.20, grain=3.0, vig=0.30):
    a = np.asarray(im, dtype=np.float32) / 255.0
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    lum3 = lum[..., None]
    a = lum3 + (a - lum3) * sat                       # giảm bão hoà nhẹ
    a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)     # đường cong tương phản
    ar = np.array(rgba(accent)[:3], dtype=np.float32) / 255.0
    shadow = np.clip(1.0 - lum, 0, 1)[..., None] ** 2
    a = a * (1 - tint * shadow) + ar * (tint * shadow)
    vy, vx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((vx - W / 2) / (W * 0.72)) ** 2 + ((vy - H * 0.46) / (H * 0.78)) ** 2)
    a *= (1 - vig * np.clip(r - 0.35, 0, 1.4))[..., None]
    a = np.clip(a, 0, 1)
    a = a * 255.0 + np.random.normal(0, grain, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def scrim(img: Image.Image, stops, softness=0) -> Image.Image:
    """stops: [(0..1 theo chiều cao, hex, alpha 0..255)] — phủ gradient dọc."""
    pos = np.array([s[0] for s in stops], dtype=np.float32)
    cols = np.array([[*rgba(s[1])[:3], s[2]] for s in stops], dtype=np.float32)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    row = np.stack([np.interp(ys, pos, cols[:, i]) for i in range(4)], axis=1)
    layer = np.repeat(row[:, None, :], W, axis=1)
    ov = Image.fromarray(layer.astype(np.uint8), "RGBA")
    if softness:
        ov = ov.filter(ImageFilter.GaussianBlur(softness))
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


def glow(img: Image.Image, xy, rx, ry, color, alpha=120) -> Image.Image:
    """quầng tối/sáng êm để chữ nổi."""
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    d.ellipse([xy[0] - rx, xy[1] - ry, xy[0] + rx, xy[1] + ry], fill=alpha)
    layer = layer.filter(ImageFilter.GaussianBlur(min(rx, ry) * 0.55))
    ov = Image.new("RGBA", (W, H), rgba(color, 0))
    ov.putalpha(layer)
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


def furniture(img: Image.Image, accent: str, light: bool) -> Image.Image:
    """gáy sách + viền chỉ + hạt phim lần cuối."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # gáy: dải 16px, tối dần vào trong
    for i in range(16):
        t = i / 15
        col = rgba(accent, int(150 * (1 - t) ** 1.6)) if not light else rgba("#101a18", int(120 * (1 - t) ** 1.6))
        d.line([(i, 0), (i, H)], fill=col)
    d.line([(16, 0), (16, H)], fill=rgba("#000000", 70 if not light else 40))
    # viền chỉ mảnh
    d.rectangle([40, 40, W - 41, H - 41], outline=rgba(accent, 60 if not light else 90), width=1)
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


# ---------- khối chữ dùng chung ----------
def imprint(d, accent, light, n, align="l", y=74):
    """nhãn bộ + số thứ tự"""
    col = rgba("#1b2a26", 190) if light else rgba("#ffffff", 200)
    acc = rgba(accent, 235)
    label = "TRUYỆN DỊCH"
    f = F(F_LIGHT, 17)
    num = f"{n:02d}"
    fn = F(F_SANS, 17)
    if align == "l":
        tracked(d, (64, y), label, f, 9.5, col)
        tracked(d, (W - 64, y), num, fn, 2, acc, anchor="rs")
    elif align == "c":
        total = tw(d, label, f, 9.5)
        tracked(d, (W / 2, y), label, f, 9.5, col, anchor="ms")
        d.line([(W / 2 - total / 2 - 46, y - 6), (W / 2 - total / 2 - 16, y - 6)], fill=acc, width=1)
        d.line([(W / 2 + total / 2 + 16, y - 6), (W / 2 + total / 2 + 46, y - 6)], fill=acc, width=1)
    elif align == "r":
        tracked(d, (W - 64, y), label, f, 9.5, col, anchor="rs")
        tracked(d, (64, y), num, fn, 2, acc)


def cjk_column(d, text, accent, x=None, y=150, size=25, gap=31, alpha=90):
    if not text:
        return
    x = W - 56 if x is None else x
    f = F(F_CJK, size)
    for i, ch in enumerate(text):
        if ch.strip():
            d.text((x, y + i * gap), ch, font=f, fill=rgba(accent, alpha), anchor="ms")


def kicker(d, x, y, text, accent, light, anchor="ls", size=15, tracking=6.4):
    col = rgba("#22322d", 175) if light else rgba("#ffffff", 175)
    tracked(d, (x, y), text, F(F_LIGHT, size), tracking, col, anchor=anchor)


def author_line(d, x, y, name, light, anchor="ls", size=25, tracking=2.4, accent=None):
    col = rgba("#17251f", 225) if light else rgba("#f3e8d4", 225)
    tracked(d, (x, y), name.upper(), F(F_SANS_B, size), tracking, col, anchor=anchor)
    if accent:
        d.text((x, y + 20), "tác giả", font=F(F_SERIF_I, 20), fill=rgba(accent, 150), anchor="ls")


def rule(d, x1, y, x2, accent, alpha=140, w=1):
    d.line([(x1, y), (x2, y)], fill=rgba(accent, alpha), width=w)


def diamond(d, cx, cy, s, accent, alpha=200):
    d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], outline=rgba(accent, alpha))


# =======================================================================
#  BỐ CỤC
# =======================================================================
def lay_classic(img, b):
    """A — cổ điển: khối chữ giữa, dưới; tiêu đề xếp tầng, to, giãn rộng."""
    acc, light = b["accent"], b["light"]
    img = scrim(img, [(0.00, "#000000", 0), (0.40, b["ink"], 0), (0.56, b["ink"], 96),
                      (0.76, b["ink"], 208), (1.00, b["ink"], 250)], softness=0)
    img = glow(img, (W / 2, H - 330), 420, 300, b["ink"], 130)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, acc, light, b["n"], "c", 84)
    cjk_column(d, b["cjk"], acc, alpha=70, y=150)

    # tác giả dưới cùng
    author_line(d, W / 2, H - 96, b["author"], light, "ms", 22, 3.0)
    rule(d, W / 2 - 54, H - 148, W / 2 + 54, acc, 160)
    kicker(d, W / 2, H - 176, b["genre_kick"], acc, light, "ms", 13, 7.0)

    lines = b["lines"]
    track = b.get("track", 10)
    f = fit(d, lines, F_SERIF_B, W - 190, b["size"], b.get("floor", 60), track)
    lh = f.size * 1.04
    base = H - 236
    for i, ln in enumerate(reversed(lines)):
        tracked(d, (W / 2, base - i * lh), ln, f, track, rgba("#f6ecd8", 250), anchor="ms")
    diamond(d, W / 2, base - (len(lines) - 1) * lh - 62, 7, acc, 220)
    return img


def lay_quiet(img, b):
    """A' — tĩnh: chữ đậm trên nền trời sáng, giãn chữ rất rộng, không khối tối."""
    acc, light = b["accent"], True
    img = scrim(img, [(0.00, "#ffffff", 30), (0.34, "#ffffff", 12), (0.62, "#ffffff", 0),
                      (0.84, b["ink"], 40), (1.00, b["ink"], 150)], softness=0)
    img = glow(img, (W / 2, 250), 540, 210, "#ffffff", 96)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, "#8a6a3a", light, b["n"], "c", 86)
    cjk_column(d, b["cjk"], "#4c6b63", alpha=120, x=W - 60, y=190)

    ink = rgba("#0f231e", 244)
    f = fit(d, b["lines"], F_SERIF, W - 210, b["size"], 66, b.get("track", 16))
    lh = f.size * 1.20
    y = b["ty"]
    for ln in b["lines"]:
        tracked(d, (W / 2, y), ln, f, b.get("track", 16), ink, anchor="ms")
        y += lh
    last = y - lh
    ry = last + f.size * 0.80
    rule(d, W / 2 - 92, ry, W / 2 + 92, "#8a6a3a", 200)
    img = glow(img, (W / 2, ry + 62), 250, 52, "#ffffff", 120)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((W / 2, ry + 44), "Tác giả", font=F(F_SERIF_I, 20), fill=rgba("#2a3f38", 190), anchor="ms")
    tracked(d, (W / 2, ry + 84), b["author"].upper(), F(F_SANS_B, 23), 3.0,
            rgba("#13261f", 235), anchor="ms")
    kicker(d, W / 2, H - 92, b["genre_kick"], "#eadfc8", False, "ms", 12, 7.2)
    return img


def lay_modern(img, b):
    """B — hiện đại: khối chữ lệch trái, gạch nhấn dọc, tiêu đề nhiều dòng."""
    acc, light = b["accent"], b["light"]
    img = scrim(img, [(0.00, b["ink"], 120), (0.18, b["ink"], 0), (0.50, b["ink"], 0),
                      (0.68, b["ink"], 140), (0.86, b["ink"], 226), (1.00, b["ink"], 248)], softness=0)
    img = glow(img, (330, H - 300), 460, 320, b["ink"], 120)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, acc, light, b["n"], "l", 82)
    cjk_column(d, b["cjk"], acc, alpha=75, y=180)

    x = 92
    lines = b["lines"]
    track = b.get("track", 4)
    f = fit(d, lines, F_SERIF_B, W - 92 - 96, b["size"], b.get("floor", 44), track)
    lh = f.size * 1.06
    base = H - 150
    top = base - (len(lines) - 1) * lh - f.size * 0.74
    # gạch nhấn dọc
    d.rectangle([x - 26, top + 6, x - 22, base + 6], fill=rgba(acc, 220))
    for i, ln in enumerate(reversed(lines)):
        tracked(d, (x, base - i * lh), ln, f, track, rgba("#f7edda", 250), anchor="ls")

    y = top - 34
    kicker(d, x, y, b["genre_kick"], acc, light, "ls", 12, 7.0)
    y -= 40
    d.text((x, y), b["author"].upper(), font=F(F_SANS_B, 22),
           fill=rgba("#f3e8d4", 220), anchor="ls")
    return img


def lay_relic(img, b):
    """B' — hiện đại nhưng nhấn bằng đường kẻ dưới + nhãn thể loại phía trên."""
    acc, light = b["accent"], b["light"]
    img = scrim(img, [(0.00, b["ink"], 90), (0.22, b["ink"], 0), (0.52, b["ink"], 10),
                      (0.72, b["ink"], 170), (0.90, b["ink"], 232), (1.00, b["ink"], 250)], softness=0)
    img = glow(img, (430, H - 250), 470, 300, b["ink"], 110)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, acc, light, b["n"], "l", 82)
    cjk_column(d, b["cjk"], acc, alpha=70, y=430)

    x = 92
    lines = b["lines"]
    track = b.get("track", 8)
    f = fit(d, lines, F_SERIF_B, W - 92 - 110, b["size"], b.get("floor", 52), track)
    lh = f.size * 1.06
    base = H - 168
    for i, ln in enumerate(reversed(lines)):
        tracked(d, (x, base - i * lh), ln, f, track, rgba("#f5f8f2", 250), anchor="ls")
    ytop = base - (len(lines) - 1) * lh - f.size * 0.78
    rule(d, x, ytop - 30, W - 96, acc, 190, 2)
    kicker(d, x, ytop - 54, b["genre_kick"], acc, light, "ls", 12, 7.0)
    author_line(d, x, H - 96, b["author"], light, "ls", 20, 3.0)
    return img


def lay_poster(img, b):
    """C — poster: tiêu đề lớn trên đỉnh, ảnh làm nền tối phía dưới."""
    acc, light = b["accent"], b["light"]
    img = scrim(img, [(0.00, b["ink"], 196), (0.26, b["ink"], 96), (0.42, b["ink"], 0),
                      (0.72, b["ink"], 20), (0.90, b["ink"], 190), (1.00, b["ink"], 246)], softness=0)
    img = glow(img, (W / 2, 250), 480, 230, b["ink"], 120)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, acc, light, b["n"], "l", 82)
    cjk_column(d, b["cjk"], acc, alpha=95, y=300)

    lines = b["lines"]
    track = b.get("track", 3)
    f = fit(d, lines, F_SERIF_B, W - 190, b["size"], b.get("floor", 54), track)
    lh = f.size * 0.98
    y = b["ty"]
    for ln in lines:
        tracked(d, (W / 2, y), ln, f, track, rgba("#fdf1de", 252), anchor="ms")
        y += lh
    rule(d, W / 2 - 70, y + 4, W / 2 + 70, acc, 210, 2)
    if b.get("tagline"):
        img = glow(img, (W / 2, y + 34), 300, 46, b["ink"], 150)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((W / 2, y + 34), b["tagline"], font=F(F_SERIF_I, 25),
               fill=rgba("#f4e2ca", 225), anchor="ms")

    kicker(d, W / 2, H - 118, b["genre_kick"], acc, light, "ms", 12, 7.4)
    author_line(d, W / 2, H - 84, b["author"], light, "ms", 22, 3.2)
    return img


def lay_band(img, b):
    """C' — dải chữ dưới: nền đặc, đường kẻ nhấn, tiêu đề giữa."""
    acc, light = b["accent"], b["light"]
    img = scrim(img, [(0.00, b["ink"], 40), (0.30, b["ink"], 0), (0.62, b["ink"], 40),
                      (0.80, b["ink"], 150), (1.00, b["ink"], 240)], softness=0)
    d0 = ImageDraw.Draw(img, "RGBA")
    imprint(d0, acc, light, b["n"], "l", 82)
    cjk_column(d0, b["cjk"], acc, alpha=80, y=180)

    band_top = b.get("band", 962)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, band_top, W, H], fill=rgba(b["ink"], 252))
    bd.line([(0, band_top), (W, band_top)], fill=rgba(acc, 235), width=3)
    img = Image.alpha_composite(img.convert("RGBA"), band).convert("RGB")

    d = ImageDraw.Draw(img, "RGBA")
    lines = b["lines"]
    track = b.get("track", 6)
    f = fit(d, lines, F_SERIF_B, W - 200, b["size"], b.get("floor", 44), track)
    lh = f.size * 1.12
    pad_top, gap_k, gap_r, gap_a, a_h = 16, 36, 42, 34, 24
    block = pad_top + gap_k + f.size * 0.78 + (len(lines) - 1) * lh + gap_r + gap_a + a_h
    avail = (H - 44) - band_top
    top = band_top + max(20, (avail - block) / 2)

    kicker(d, W / 2, top + pad_top, b["genre_kick"], acc, False, "ms", 13, 7.2)
    y = top + pad_top + gap_k + f.size * 0.78
    for ln in lines:
        tracked(d, (W / 2, y), ln, f, track, rgba("#fbf0da", 250), anchor="ms")
        y += lh
    ry = y - lh + gap_r
    rule(d, W / 2 - 62, ry, W / 2 + 62, acc, 170)
    author_line(d, W / 2, ry + gap_a + 14, b["author"], False, "ms", 20, 3.0)
    return img


def lay_novel(img, b):
    """D — tiểu thuyết: tựa hỗn hợp hoa/thường ở góc trên trái, mực đậm trên nền sáng,
    dòng giữa nghiêng, nhấn son; năm truyện in mờ góc phải."""
    acc = b["accent"]
    img = scrim(img, [(0.00, "#ffffff", 40), (0.26, "#ffffff", 16), (0.50, "#ffffff", 0),
                      (0.80, b["ink"], 70), (0.92, b["ink"], 200), (1.00, b["ink"], 238)], softness=0)
    img = glow(img, (W * 0.40, 250), 450, 200, "#ffffff", 120)
    d = ImageDraw.Draw(img, "RGBA")
    imprint(d, acc, True, b["n"], "c", 84)
    cjk_column(d, b["cjk"], "#8a4a34", alpha=115, x=W - 58, y=170)

    x = 88
    size = b["size"]
    f_b = F(F_SERIF_B, size)
    f_i = F(F_SERIF_I, size)
    lh = size * 1.18
    ink = rgba("#26190e", 246)
    diamond(d, x + 8, 138, 7, acc, 235)
    y = 168 + size * 0.78
    for i, ln in enumerate(b["lines"]):
        f = f_i if i % 2 == 1 else f_b
        tracked(d, (x, y), ln, f, 0, ink, anchor="ls")
        y += lh
    rule(d, x, y - lh + size * 0.42, x + 128, acc, 220, 3)

    kicker(d, x, H - 152, b["genre_kick"], "#f4ddcc", False, "ls", 12, 7.0)
    author_line(d, x, H - 108, b["author"], False, "ls", 21, 2.6)
    if b.get("year"):
        d.text((W - 52, H - 240), b["year"], font=F(F_SERIF, 158),
               fill=rgba(acc, 36), anchor="rs")
    return img


LAYOUTS = {
    "classic": lay_classic,
    "quiet": lay_quiet,
    "modern": lay_modern,
    "relic": lay_relic,
    "poster": lay_poster,
    "band": lay_band,
    "novel": lay_novel,
}


# =======================================================================
BOOKS = [
    dict(
        key="baojian_vi", out="cover-bao.jpg", n=1, layout="classic",
        lines=["BẢO", "GIÁM"], size=196, track=14, floor=90,
        author="Đả Nhãn", genre_kick="CỔ VẬT · MƯU ĐỒ · TÌNH CẢM",
        accent="#c9a227", ink="#0b1018", light=False, cjk="",
    ),
    dict(
        key="can_bao_chan_long_vi", out="cover-chan.jpg", n=2, layout="poster",
        lines=["CẢNH BÁO!", "CHÂN LONG", "XUẤT NGỤC!"], size=104, track=2, floor=62,
        author="Hồng Thấu Bán Biên Thiên",
        genre_kick="HUYỀN HUYỄN · TU TIÊN · BÁO THÙ",
        tagline="Ba năm ngục tối, một lần long ngâm.",
        accent="#d98b4a", ink="#140708", light=False, cjk="警报！真龙出狱！",
        ty=248,
    ),
    dict(
        key="khai_cuc_dinh_chuc_vi", out="cover-kcdc.jpg", n=3, layout="modern",
        lines=["KHAI CỤC ĐÌNH CHỨC?", "TA CHUYỂN ĐẦU", "ỦY BAN KỶ LUẬT", "ĐIỀU TRA TỔ"],
        size=76, track=2, floor=42,
        author="Giang Môn Nhị Gia", genre_kick="QUAN TRƯỜNG · TRỌNG SINH · 2008",
        accent="#d8a35c", ink="#120d09", light=False, cjk="开局停职？我转投纪委调查组",
    ),
    dict(
        key="nhi_huu_thien_nhan_vi", out="cover-thien.jpg", n=4, layout="relic",
        lines=["THIÊN NHÃN", "ĐỔ THẠCH"], size=100, track=8, floor=58,
        author="Khuyết danh", genre_kick="ĐÔ THỊ · DỊ NĂNG · ĐỔ THẠCH",
        accent="#6fc79b", ink="#05100d", light=False, cjk="你有天眼不去赌石，又在乱看",
    ),
    dict(
        key="nien_dai_58_vi", out="cover-nien.jpg", n=5, layout="band",
        lines=["NIÊN ĐẠI:", "NĂM 58, TA CÓ", "MỘT THỬA RUỘNG"],
        size=72, track=3, floor=40,
        author="Phong Trung Chiết Yêu", genre_kick="NIÊN ĐẠI VĂN · XUYÊN KHÔNG · 1958",
        band=932,
        accent="#e3b878", ink="#150f08", light=False, cjk="年代：我在58有块田",
    ),
    dict(
        key="quan_dao_chi_dien_vi", out="cover-qdcd.jpg", n=6, layout="quiet",
        lines=["ĐỈNH CAO", "QUAN LỘ"], size=126, track=18, floor=80,
        author="Thanh Mộc Thư Sinh", genre_kick="QUAN TRƯỜNG · TRỌNG SINH · ĐÔ THỊ",
        accent="#8a6a3a", ink="#0d1f1c", light=True, cjk="官道之巅", ty=196,
    ),
    dict(
        key="cao_nhi_phan_khoa_vi", out="cover-phankhoa.jpg", n=7, layout="novel",
        lines=["Phân ban lớp 11,", "tôi chọn hoa khôi", "và cơ nghiệp trăm tỷ"],
        size=62, track=0, floor=42,
        author="Hắc Cẩu Không Thích Ăn Bánh Trôi",
        genre_kick="TRỌNG SINH · HỌC ĐƯỜNG · KINH DOANH",
        accent="#cf4f36", ink="#171009", light=False,
        cjk="高二分科，我选校花也选亿万身家", year="2011",
    ),
]


def build(b: dict, write=True) -> Path:
    src = ART / f"{b['key']}.jpg"
    im = Image.open(src).convert("RGB")
    im = cover_fit(im)
    im = grade(im, b["accent"], vig=0.26 if b["light"] else 0.34)
    im = LAYOUTS[b["layout"]](im, b)
    im = furniture(im, b["accent"], b["light"])
    out = IMG / b["out"]
    if write:
        im.save(out, "JPEG", quality=90, subsampling=1, optimize=True, progressive=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    for book in BOOKS:
        if a.only and a.only not in book["key"]:
            continue
        p = build(book)
        print(f"{p.name:16s} {p.stat().st_size/1024:7.1f} KB  {book['layout']}")
