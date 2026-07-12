"""
Playwright 响应拦截方案：1:1 网页复刻（CSS + 图片全部内联）
============================================================
适用场景：目标网站 CDN 有 403 保护，无法直接下载静态资源
原理：浏览器能渲染页面 = 浏览器已拿到所有 CSS/图片。
      Playwright page.on("response") 在浏览器内存中直接拦截 body，不对外发新请求。

使用方法：
  1. 修改 TARGET_URL 为目标网页地址
  2. python scripts/clone_intercept.py
  3. start "" "clone_output/full_clone.html"
"""

import asyncio, base64, re
from pathlib import Path
from playwright.async_api import async_playwright

# ====== 用户配置 ======
TARGET_URL = "https://example.com"
OUTPUT_DIR = Path("./clone_output")
# =====================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    css_map = {}  # url -> css_text
    img_map = {}  # url -> (content_type, base64_data)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # 🔑 核心：拦截浏览器内部所有 response
        async def on_response(response):
            url = response.url
            ct = response.headers.get("content-type", "")
            if response.status != 200:
                return
            try:
                body = await response.body()
            except:
                return
            if not body:
                return
            if "css" in ct or url.endswith(".css"):
                css_map[url] = body.decode("utf-8", errors="replace")
                print(f"  CSS: {len(css_map[url])} chars <- {url[-60:]}")
            elif any(t in ct for t in ["image/", "font/"]):
                if len(body) < 2_000_000:
                    img_map[url] = (ct, base64.b64encode(body).decode())
                    print(f"  IMG: {len(body)} bytes <- {url[-60:]}")

        page.on("response", on_response)

        # 加载页面，等完全渲染
        print(f"🌐 加载: {TARGET_URL}")
        await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)

        # 截图留档
        screenshot = await page.screenshot(full_page=False, type="png")
        (OUTPUT_DIR / "screenshot.png").write_bytes(screenshot)

        html = await page.content()

        # === 清理：删除外部 CSS link 和无关脚本 ===
        html = re.sub(r'<link[^>]*rel=["\']?stylesheet["\']?[^>]*/?>', '', html, re.I)
        html = re.sub(r'<script[^>]*vercel[^>]*></script>', '', html, re.I)

        # === 合并所有 CSS 内联 ===
        if css_map:
            mega_css = "\n".join(css_map.values())
            html = html.replace("</head>", f"<style>\n{mega_css}\n</style>\n</head>")
            css_total = sum(len(v) for v in css_map.values())
            print(f"📄 CSS: {len(css_map)} 个文件, {css_total:,} chars")

        # === 图片替换（文件名模糊匹配）===
        replaced = 0
        if img_map:
            # 构建 文件名 → data URI 映射
            file_map = {}
            for url, (ct, b64) in img_map.items():
                filename = url.split("/")[-1].split("?")[0]
                short = re.sub(r'\.[a-z]+$', '', filename)
                data_uri = f"data:{ct};base64,{b64}"
                file_map[filename] = data_uri
                if short != filename:
                    file_map[short] = data_uri

            # 收集 HTML 中所有引用
            all_refs = set(re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html))
            all_refs |= set(re.findall(r'url\(["\']?([^"\'()]+)["\']?\)', html))

            # 按长度排序，先匹配长 URL（避免短名误配）
            for ref in sorted(all_refs, key=len, reverse=True):
                if ref.startswith("data:"):
                    continue
                ref_filename = ref.split("/")[-1].split("?")[0]
                ref_short = re.sub(r'\.[a-z]+$', '', ref_filename)
                if ref_filename in file_map:
                    html = html.replace(ref, file_map[ref_filename])
                    replaced += 1
                elif ref_short in file_map:
                    html = html.replace(ref, file_map[ref_short])
                    replaced += 1

            print(f"🖼️  图片: {replaced}/{len(img_map)} 个替换")

        # === 最终写入 ===
        final = OUTPUT_DIR / "full_clone.html"
        final.write_text(html, encoding="utf-8")
        size_mb = len(html.encode()) / (1024 * 1024)
        print(f"\n✅ {final}")
        print(f"   大小: {size_mb:.1f} MB")
        print(f"   含 {len(css_map)} CSS + {replaced} 图片")

        await browser.close()

asyncio.run(main())
