#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-translate with glossary refinement every 10 chapters.
Dịch tự động với cập nhật glossary mỗi 10 chương.
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRANSLATE = ROOT / "translate"
DATA_OUT = ROOT / "data" / "can_bao_chan_long_vi"
GLOSSARY_FILE = TRANSLATE / "glossary_can_bao_chan_long.txt"
STATE_FILE = TRANSLATE / "state_can_bao_chan_long.json"
LOG_FILE = TRANSLATE / "_auto_batch_log.txt"

# Cấu hình batch
BATCH_SIZE = 10  # Dịch 10 chương một lô
MAX_CHAPTERS = 1897
START_FROM = 6  # Bắt đầu từ chương 6 (đã dịch 1-5)

def log(msg):
    """Ghi log ra file và console."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_glossary():
    """Đọc glossary hiện tại."""
    if GLOSSARY_FILE.exists():
        return GLOSSARY_FILE.read_text(encoding="utf-8")
    return ""

def save_glossary(content):
    """Lưu glossary mới."""
    GLOSSARY_FILE.write_text(content, encoding="utf-8")
    log(f"Da cap nhat glossary: {GLOSSARY_FILE}")

def run_translate(from_ch, to_ch):
    """Chạy dịch từ chương from_ch đến to_ch."""
    cmd = [
        sys.executable,
        str(TRANSLATE / "dich.py"),
        "--book", "can_bao_chan_long",
        "--from", str(from_ch),
        "--to", str(to_ch),
        "--backend", "openai",
        "--workers", "1"
    ]
    log(f"Dich chuong {from_ch}..{to_ch}: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    
    if result.returncode == 0:
        log(f"✓ Dich thanh cong chuong {from_ch}..{to_ch}")
        return True
    else:
        log(f"✗ Dich THAT BAI chuong {from_ch}..{to_ch}")
        log(f"stdout: {result.stdout[:500]}")
        log(f"stderr: {result.stderr[:500]}")
        return False

def extract_new_terms_from_batch(from_ch, to_ch):
    """
    Trích xuất thuật ngữ mới từ batch chương vừa dịch.
    Đọc các file .md đã dịch, tìm mục "THUẬT NGỮ MỚI" nếu có.
    """
    new_terms = []
    for ch_no in range(from_ch, to_ch + 1):
        md_files = list(DATA_OUT.glob(f"{ch_no:04d}_*.md"))
        if not md_files:
            continue
        
        content = md_files[0].read_text(encoding="utf-8")
        if "=== THUẬT NGỮ MỚI ===" in content:
            lines = content.split("=== THUẬT NGỮ MỚI ===")[1].strip().split("\n")
            for line in lines:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    new_terms.append(line)
    
    return new_terms

def update_glossary_with_new_terms(new_terms):
    """Cập nhật glossary với thuật ngữ mới."""
    if not new_terms:
        log("Khong co thuat ngu moi, giu nguyen glossary")
        return
    
    glossary = load_glossary()
    
    # Thêm vào cuối mục "THUẬT NGỮ CHUNG"
    insert_marker = "## ══════ CẤM TỪ"
    if insert_marker in glossary:
        parts = glossary.split(insert_marker)
        new_section = "\n### Thuật ngữ bổ sung (tự động):\n" + "\n".join(new_terms) + "\n\n"
        glossary = parts[0] + new_section + insert_marker + parts[1]
    else:
        glossary += "\n\n### Thuật ngữ bổ sung (tự động):\n" + "\n".join(new_terms)
    
    save_glossary(glossary)
    log(f"Da them {len(new_terms)} thuat ngu moi vao glossary")

def main():
    log("=" * 60)
    log("BAT DAU DICH TU DONG - Canh Bao Chan Long Xuat Nguc")
    log("=" * 60)
    
    current = START_FROM
    
    while current <= MAX_CHAPTERS:
        batch_end = min(current + BATCH_SIZE - 1, MAX_CHAPTERS)
        
        log("")
        log(f">>> BATCH: Chuong {current}..{batch_end}")
        
        # Bước 1: Dịch batch
        success = run_translate(current, batch_end)
        if not success:
            log(f"!!! Dich that bai tai chuong {current}, DUNG LAI")
            break
        
        # Bước 2: Trích xuất thuật ngữ mới
        log("Trich xuat thuat ngu moi...")
        new_terms = extract_new_terms_from_batch(current, batch_end)
        
        # Bước 3: Cập nhật glossary
        if new_terms:
            log(f"Tim thay {len(new_terms)} thuat ngu moi:")
            for term in new_terms[:10]:  # Chỉ log 10 thuật ngữ đầu
                log(f"  - {term}")
            update_glossary_with_new_terms(new_terms)
        
        # Chuyển sang batch tiếp theo
        current = batch_end + 1
        
        # Nghỉ 5 giây giữa các batch để tránh rate limit
        if current <= MAX_CHAPTERS:
            log("Nghi 5s truoc batch tiep...")
            time.sleep(5)
    
    log("")
    log("=" * 60)
    log("HOAN THANH DICH TU DONG")
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n!!! Nguoi dung dung lai (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        log(f"\n!!! LOI: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
