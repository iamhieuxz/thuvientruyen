# -*- coding: utf-8 -*-
"""Kho tiến độ đọc dùng chung (GĐ3): mọi trình duyệt/điện thoại cùng WiFi đều thấy.

File: reader/progress.json (tự tạo; KHÔNG đụng data/). Đồng bộ merge-only:
  - Pull (GET /api/progress): trả kho đầy đủ + mtime (giây).
  - Push (POST /api/progress): client gửi toàn kho của nó; server merge vào
    kho chung rồi trả kho đã gộp + mtime để client cập nhật.
Merge theo từng truyện: read (hợp), pos (max), marks (union), last (max),
vpos/tts (lấy phần thiếu) — cùng triết lý với mergeAll() phía client, không
bao giờ xoá dữ liệu của thiết bị nào.
"""

import json
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATH = ROOT / "progress.json"
_LOCK = threading.RLock()       # RLock: store() giữ khoá rồi gọi load() cũng lấy khoá
_mtime = 0.0
_mtime_monotonic = 0.0


def _load_raw():
    try:
        raw = json.loads(PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raw = None
    if not isinstance(raw, dict):
        return {}
    out = {}
    books = raw.get("books")
    if isinstance(books, dict):
        out["books"] = {str(k): v for k, v in books.items()
                        if isinstance(v, dict)}
    if isinstance(raw.get("settings"), dict):
        out["settings"] = dict(raw["settings"])
    return out


def _write_raw(data):
    tmp = PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(PATH)           # atomic thay vì ghi đè trực tiếp
    global _mtime, _mtime_monotonic
    _mtime = time.time()
    _mtime_monotonic = time.monotonic()


def _merge_book(dst, src):
    """Gộp một truyện: read hợp, pos max, marks union, last max, vpos/tts bổ sung."""
    read_a = set(dst.get("read") or [])
    read_a |= {int(n) for n in (src.get("read") or []) if str(n).lstrip("-").isdigit()}
    dst["read"] = sorted(read_a)
    dpos, spos = dst.get("pos") or {}, src.get("pos") or {}
    for k, v in spos.items():
        if k not in dpos or (isinstance(v, (int, float)) and v > dpos[k]):
            dpos[k] = v
    dst["pos"] = dpos
    marks = dict(dst.get("marks") or {})
    for k, v in (src.get("marks") or {}).items():
        marks.setdefault(k, v)
    dst["marks"] = marks
    try:
        if int(src.get("last") or 0) > int(dst.get("last") or 0):
            dst["last"] = src["last"]
    except (TypeError, ValueError):
        pass
    if not dst.get("vpos") and src.get("vpos"):
        dst["vpos"] = src["vpos"]
    # Giọng đọc theo truyện ({voice, rate, ts}): bản có ts mới hơn thắng; chuỗi cũ
    # (không ts) chỉ bổ sung khi thiếu — không để bản cũ đè lựa chọn mới hơn.
    stts, dtts = src.get("tts"), dst.get("tts")
    if isinstance(stts, dict) and stts:
        try:
            newer = int(stts.get("ts") or 0) >= int((dtts or {}).get("ts") or 0) if isinstance(dtts, dict) else True
        except (TypeError, ValueError):
            newer = True
        if not dtts or newer:
            dst["tts"] = stts
    elif not dtts and stts:
        dst["tts"] = stts
    return dst


def merge_kho(dst, src):
    """Gộp hai kho (giữ nguyên tính chất merge-only; không xoá gì)."""
    for bid, sbook in (src.get("books") or {}).items():
        if not isinstance(sbook, dict):
            continue
        dbook = (dst.setdefault("books", {}).setdefault(str(bid), {}))
        _merge_book(dbook, sbook)
    for k, v in (src.get("settings") or {}).items():
        dst.setdefault("settings", {}).setdefault(k, v)
    return dst


def load():
    """Kho hiện tại (load lười lần đầu; nhớ mtime cho client so thay đổi)."""
    with _LOCK:
        global _mtime, _mtime_monotonic
        if _mtime_monotonic == 0.0:
            if PATH.exists():
                data = _load_raw()
                try:
                    _mtime = PATH.stat().st_mtime
                except OSError:
                    _mtime = 0.0
            else:
                data = {}
            _mtime_monotonic = time.monotonic()
            return data
        if PATH.exists():
            m = PATH.stat().st_mtime
            if m > _mtime:                      # chỉnh tay file -> reload
                _mtime = m
                return _load_raw()
        return _load_raw()


def store(payload):
    """Gộp payload của client vào kho chung; trả (kho_đã_gộp, mtime_giây)."""
    if not isinstance(payload, dict):
        payload = {}
    with _LOCK:
        data = load()
        before = json.dumps(data, sort_keys=True)
        merge_kho(data, payload)
        after = json.dumps(data, sort_keys=True)
        if after != before:
            _write_raw(data)
        return data, _mtime
