"""Read novel index metadata (that endpoint returns 200)."""
import asyncio, sys, re, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from truyendich_scraper.http_client import HttpClient
from bs4 import BeautifulSoup

SLUG = "bao-giam"

async def main():
    async with HttpClient() as http:
        html = await http.fetch(f"https://truyendich.space/doc-truyen/{SLUG}")
    Path(f"_{SLUG}_index.html").write_text(html, encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    print("=== META ===")
    for m in soup.find_all("meta"):
        p = m.get("property") or m.get("name")
        if p and p in ("og:title","og:description","og:site_name","description","author","keywords"):
            print(f"  {p}: {(m.get('content') or '')[:300]}")

    print("\n=== JSON-LD ===")
    for s in soup.find_all("script", type="application/ld+json"):
        print((s.string or "")[:1500])

    print("\n=== H1 / title ===")
    print("  title:", soup.title.get_text(strip=True) if soup.title else None)
    for h in soup.find_all(["h1","h2"])[:8]:
        t = h.get_text(" ", strip=True)
        if t: print(f"  <{h.name}> {t[:120]}")

    print("\n=== author / status hints ===")
    for pat in ["Tác giả", "Tác Giả", "Hoàn", "Đang", "Tình trạng", "Thể loại"]:
        for m in re.finditer(pat, html):
            seg = re.sub(r"<[^>]+>", " ", html[m.start()-100:m.start()+250])
            seg = re.sub(r"\s+", " ", seg).strip()
            print(f"  [{pat}] {seg[:220]}")
            break

asyncio.run(main())