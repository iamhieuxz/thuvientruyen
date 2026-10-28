"""Probe v2: realistic browser fingerprint."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.async_api import async_playwright

URL = "https://truyendich.space/doc-truyen/bao-giam/chuong-1"
PROBE = "phiếu lương thực"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


async def attempt(label, **launch_kw):
    ctx_kw = launch_kw.pop("ctx_kw", {})
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, **launch_kw)
        ctx = await browser.new_context(
            locale="vi-VN",
            timezone_id="Asia/Ho_Chi_Minh",
            viewport={"width": 1366, "height": 768},
            user_agent=UA,
            **ctx_kw,
        )
        # mask the most obvious automation tell
        await ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = window.chrome || {runtime: {}};
            Object.defineProperty(navigator, 'languages', {get: () => ['vi-VN','vi','en-US']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        """)
        page = await ctx.new_page()
        try:
            r = await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(7000)
            html = await page.content()
            real = PROBE in html
            print(f"[{label}] status={r.status} len={len(html)} real_text={real} cipher={html.count('mystic-cipher')}")
            if r.status == 200:
                info = await page.evaluate("""() => {
                    const sec = document.querySelector('section.prose-novel');
                    if(!sec) return {found:false};
                    const tabs=[...sec.querySelectorAll('[id*="content-tab"]')].map(d=>({
                        id:d.id, display:getComputedStyle(d).display,
                        pCount:d.querySelectorAll('p').length,
                        text:(d.innerText||'').slice(0,100)
                    }));
                    return {found:true,tabs};
                }""")
                print("   tabs:", info.get("tabs"))
            await browser.close()
            return r.status, real
        except Exception as e:
            print(f"[{label}] ERROR {e}")
            await browser.close()
            return None, False


async def main():
    # A: default headless
    await attempt("headless-default")
    # B: headless=new channel style
    await attempt("headless-new", args=["--headless=new"])
    # C: chromium channel (real installed Chrome-like build)
    try:
        await attempt("channel-chromium", channel="chromium")
    except Exception as e:
        print("channel chromium unavailable:", e)

asyncio.run(main())