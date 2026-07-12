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

特性：
  ✅ CSSOM 捕获（styled-components/emotion 等 CSS-in-JS）
  ✅ 滚动触发懒加载图片
  ✅ DOM 级图片替换（不丢 <source srcset>、CSS background-image、favicon）
  ✅ httpx 替补下载（on_response 没拦截到的图片）
"""
import asyncio, base64, re
from pathlib import Path
import httpx
from playwright.async_api import async_playwright

# ====== 用户配置 ======
TARGET_URL = "https://www.coinbase.com/zh-cn"
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
            elif any(t in ct for t in ["image/", "font/"]):
                if len(body) < 2_000_000:
                    img_map[url] = (ct, base64.b64encode(body).decode())

        page.on("response", on_response)

        # 加载页面，等完全渲染
        print(f"🌐 加载: {TARGET_URL}")
        await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)

        # 额外等 React / styled-components 完成水合
        print("⏳ 等待渲染完成...")
        await asyncio.sleep(3)
        print(f"  初始捕获: {len(img_map)} 图片")

        # ============================================================
        # 第一步：滚动触发懒加载图片
        # ============================================================
        print("⬇️ 滚动触发懒加载...")
        for i in range(5):
            await page.evaluate("window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(1)
        # 滚回顶部
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(2)

        # ============================================================
        # 第二步：CSSOM 捕获（styled-components v6 等 CSS-in-JS 用 insertRule 注入样式）
        # ============================================================
        runtime_css = await page.evaluate("""
            () => {
                let chunks = [];
                for (let i = 0; i < document.styleSheets.length; i++) {
                    const ss = document.styleSheets[i];
                    if (ss.href) continue;  // 跳过外部样式表
                    try {
                        const rules = ss.cssRules || ss.rules || [];
                        for (let j = 0; j < rules.length; j++)
                            chunks.push(rules[j].cssText);
                    } catch(e) {}  // 跨域 sheet 无法访问，跳过
                }
                return chunks.join('\\n');
            }
        """)
        if runtime_css:
            css_map["__cssom__"] = runtime_css
            print(f"  🎯 CSSOM: {len(runtime_css):,} chars")

        # ============================================================
        # 第三步：从滚动后的 DOM 找出浏览器已加载但 on_response 没拿到的图片
        # ============================================================
        loaded_urls = await page.evaluate("""
            () => {
                const urls = new Set();
                // <img> 标签
                document.querySelectorAll('img').forEach(img => {
                    if (img.src && img.src.startsWith('http')) urls.add(img.src);
                });
                // <source srcset>（<picture> 内的 responsive 图片）
                document.querySelectorAll('source').forEach(s => {
                    if (s.srcset && s.srcset.startsWith('http')) urls.add(s.srcset);
                });
                // CSS background-image
                document.querySelectorAll('[style*="background-image"]').forEach(el => {
                    const m = el.getAttribute('style').match(/url\\(["']?([^"'()]+)["']?\\)/);
                    if (m && m[1].startsWith('http')) urls.add(m[1]);
                });
                // favicon / apple-touch-icon
                document.querySelectorAll('link[rel*="icon"]').forEach(link => {
                    if (link.href && link.href.startsWith('http')) urls.add(link.href);
                });
                return Array.from(urls);
            }
        """)

        to_download = [u for u in loaded_urls if u not in img_map]
        print(f"📸 需要 httpx 补抓: {len(to_download)}/{len(loaded_urls)}")

        if to_download:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                for url in to_download:
                    try:
                        resp = await client.get(url, headers={
                            'Referer': TARGET_URL,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131'
                        })
                        if resp.status_code == 200 and len(resp.content) > 100:
                            ct = resp.headers.get('content-type', 'image/png')
                            b64 = base64.b64encode(resp.content).decode()
                            img_map[url] = (ct, b64)
                            print(f"  ✅ {url[-60:]} ({len(resp.content)} bytes)")
                        else:
                            print(f"  ❌ {resp.status_code}: {url[-60:]}")
                    except Exception as e:
                        print(f"  ❌ 失败: {url[-50:]}: {str(e)[:40]}")

        print(f"\n📊 总计: CSS={len(css_map)}, 图片={len(img_map)}")

        # ============================================================
        # 第四步：在浏览器 DOM 里直接替换所有外部引用为 data URI
        # ============================================================
        if img_map:
            url_to_data = {url: f"data:{ct};base64,{b64}" for url, (ct, b64) in img_map.items()}
            print("🔄 浏览器 DOM 替换图片引用...")
            replaced = await page.evaluate("""(mapping) => {
                let count = 0;
                // <img src>
                document.querySelectorAll('img').forEach(img => {
                    if (img.src && mapping[img.src]) {
                        img.src = mapping[img.src]; count++;
                    }
                });
                // <source srcset>
                document.querySelectorAll('source').forEach(s => {
                    if (s.srcset && mapping[s.srcset]) {
                        s.srcset = mapping[s.srcset]; count++;
                    }
                });
                // CSS background-image
                document.querySelectorAll('[style*="background-image"]').forEach(el => {
                    const style = el.getAttribute('style');
                    const m = style.match(/url\\(["']?([^"'()]+)["']?\\)/);
                    if (m && mapping[m[1]]) {
                        el.setAttribute('style', style.replace(m[1], mapping[m[1]]));
                        count++;
                    }
                });
                // link favicon / apple-touch-icon
                document.querySelectorAll('link[rel*="icon"]').forEach(link => {
                    if (link.href && mapping[link.href]) {
                        link.href = mapping[link.href]; count++;
                    }
                });
                return count;
            }""", url_to_data)
            print(f"  DOM 替换: {replaced} 处")

        # 截图留档
        screenshot = await page.screenshot(full_page=False, type="png")
        (OUTPUT_DIR / "screenshot.png").write_bytes(screenshot)

        html = await page.content()

        # === 清理 ===
        html = re.sub(r'<link[^>]*rel=["\']?stylesheet["\']?[^>]*/?>', '', html, re.I)
        html = re.sub(r'<script[^>]*vercel[^>]*></script>', '', html, re.I)

        # === 合并 CSS 内联 ===
        if css_map:
            mega_css = "\n".join(css_map.values())
            html = html.replace("</head>", f"<style>\n{mega_css}\n</style>\n</head>")
            css_total = sum(len(v) for v in css_map.values())
            print(f"📄 CSS: {len(css_map)} 个源, {css_total:,} chars")

        # === 额外处理：CSS 文本中的 url() 引用（在 <style> 内部） ===
        if img_map:
            url_to_data = {url: f"data:{ct};base64,{b64}" for url, (ct, b64) in img_map.items()}
            for url, data_uri in url_to_data.items():
                html = html.replace(f'url("{url}")', f'url("{data_uri}")')
                html = html.replace(f"url('{url}')", f"url('{data_uri}')")
                html = html.replace(f'url({url})', f'url({data_uri})')

        # === 最终写入 ===
        final = OUTPUT_DIR / "full_clone.html"
        final.write_text(html, encoding="utf-8")
        size_mb = len(html.encode()) / (1024 * 1024)

        # === 验证 ===
        remaining_imgs = []
        for m in re.finditer(r'<img[^>]*src=[\"\']([^\"\']+)[\"\']', html):
            u = m.group(1)
            if not u.startswith('data:') and not u.startswith('file:'):
                remaining_imgs.append(u)

        print(f"\n✅ {final}")
        print(f"   大小: {size_mb:.1f} MB")
        print(f"   CSS: {css_total:,} chars" if css_map else "")
        print(f"   图片: {len(img_map)} 张, 剩余未内联 <img>: {len(remaining_imgs)}")

        await browser.close()

asyncio.run(main())
