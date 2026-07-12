# Cloner Web — 页面克隆参考笔记

## Playwright 响应拦截原理

```
浏览器访问目标页面
        │
        ▼
Playwright 内部请求 → 浏览器发起 HTTP 请求
        │
        ▼
服务器返回响应（CSS/图片） ← 浏览器带 Cookie/Referer，CDN 放行
        │
        ▼
page.on("response") 拦截     ← 在浏览器内存中，不对外发新请求
        │
        ├── CSS → 合并为 <style> 块
        └── 图片 → base64 编码 → data URI
        │
        ▼
        HTML 所有外链 → 替换为内联
        │
        ▼
        ✅ 生成单文件 HTML，完全离线可用
```

## 为什么 MHTML 不行

| 方案 | 问题 |
|:----:|------|
| `requests.get(css_url)` | CDN 返回 403（Referer/Origin 校验） |
| `requests.get(img_url)` | 同上，图片被 CDN 保护 |
| MHTML via CDP (Crawl4AI) | 浏览器渲染后用 `Page.captureSnapshot` 生成 MHTML，但 Windows Edge/Chrome 打开兼容性差，可能显示空白 |
| **Playwright 拦截** | 在浏览器渲染过程中实时捕获 → CDN 放行 → 100% 成功 |

## 实战数据：OpenAI 中文首页

| 指标 | 数据 |
|:----:|:----:|
| 页面 URL | openai.com/zh-Hans-CN/ |
| 拦截 CSS 文件数 | 17 个 |
| CSS 总大小 | 734,283 chars（含 Next.js chunk CSS + 字体声明） |
| 拦截图片数 | 16 张 |
| 图片总大小 | ~2.4 MB（webp 格式） |
| 最终 HTML 大小 | 9.2 MB |
| 截图 | 1440×900 PNG |
| 处理时间 | ~15 秒 |

## 文件名匹配规则

HTML 中的图片 URL 和 Playwright 拦截到的 URL 往往不完全相同：
- HTML 中可能是 `/next/image?url=xxx&w=1920&q=80`
- 拦截到的可能是 `cdn.openai.com/xxx/Art_Card_1_1.png?w=1920&q=90&fm=webp`

匹配策略：提取 URL 最后一段的文件名（去掉 query），再尝试去掉扩展名做第二次匹配。

## 已知陷坑

1. **重复替换**：如果多个图片文件名相同但路径不同（如不同目录下的 `logo.svg`），`str.replace()` 会全部替换。先按 URL 长度排序可缓解。
2. **CSS 中的 `url()` 引用**：CSS 中的图片引用用 `url(...)` 语法，需要分别匹配。
3. **srcset 属性**：响应式图片的 `srcset` 属性可能包含多个候选 URL，目前通过 `src` 匹配处理，遗漏概率低。
4. **字体文件**：字体通常 > 2MB，默认不内联，所以页面会回退到系统字体。

## 环境要求

- Python 3.8+
- `playwright` 包
- Chromium 浏览器内核（`python -m playwright install chromium`）
- 不需要额外安装包
