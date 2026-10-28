# -*- coding: utf-8 -*-
"""Dich thu chuong 2 bang nhieu model, so sanh chat luong + do day."""
import sys, os, json, urllib.request, urllib.error, time
sys.path.insert(0, r"f:\taitruyen\translate")
import dich
dich.load_env()

key = os.environ["GEMINI_API_KEY"]
base = "https://generativelanguage.googleapis.com/v1beta"

src_file = dich.SRC / dich.all_chapters()[2]
text = dich.clean(src_file.read_text(encoding="utf-8", errors="replace"))
title = dich.all_chapters()[2].split("_", 1)[1].rsplit(".", 1)[0]
glossary = dich.GLOSSARY.read_text(encoding="utf-8")
prompt = dich.build_prompt(2, title, text, glossary)

sp, sq = dich.count_units(text)
print(f"goc: {len(text):,} ky tu, {sp} doan, {sq} dau cau")
print()

for model in ["gemini-3.1-flash-lite", "gemini-3-flash-preview",
              "gemini-3.5-flash-lite"]:
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 65536}}
    t0 = time.time()
    try:
        req = urllib.request.Request(
            f"{base}/models/{model}:generateContent",
            data=json.dumps(body).encode(),
            headers={"x-goog-api-key": key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            d = json.loads(r.read().decode())
        cand = d["candidates"][0]
        fr = cand.get("finishReason")
        parts = cand.get("content", {}).get("parts", [])
        raw = "".join(p.get("text", "") for p in parts)
        vi, terms = dich.parse_extra(raw)
        dp, dq = dich.count_units_vi(vi)
        ok, why = dich.check_complete(text, vi)
        um = d.get("usageMetadata", {})

        print(f"{model}")
        print(f"   finish={fr}  {time.time()-t0:.1f}s  out={len(vi):,} ky tu  "
              f"doan {dp}/{sp}  dau cau {dq}/{sq}")
        print(f"   usage: {um}")
        print(f"   check_complete: {'OK' if ok else 'FAIL - ' + why}")
        print(f"   thuat ngu moi: {len(terms)}")
        print(f"   cuoi: ...{vi.strip()[-100:]!r}")
        print()
    except urllib.error.HTTPError as e:
        print(f"{model}: HTTP {e.code} {e.read().decode()[:120]}")
    except Exception as e:
        print(f"{model}: LOI {e}")
    time.sleep(2)