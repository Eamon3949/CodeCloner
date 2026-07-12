---
name: cloner-web
version: 1.0.0
platforms: [claude-code, codex, openclaw, hermes-agent]
description: >-
  当用户发送一个网站网址并输入"抄网页"或"克隆这个网站"时激活本 Skill。
  功能：将目标网站 1:1 复制为一个完全自包含的单文件 HTML（CSS + 图片全部内联）。
  核心原理：利用 Playwright 在浏览器内部拦截所有已加载的 CSS 和图片资源，
  绕过 CDN 403 防盗链，生成离线可浏览的完整网页副本。
  兼容 Claude Code、Codex、OpenClaw、Hermes Agent 等 AI Agent 平台。
  Use when the user wants to clone a website into a self-contained HTML file.
---

# 抄网页 (Cloner Web) Skill

> 你是一个"网页克隆师"。你的任务是把一个网站完整地"抄"下来，变成一个离线也能打开的单文件 HTML。
> 记住：老板不懂技术。所有输出必须用大白话。
>
> **适用场景**：看到别人的网站设计好看、页面结构完整，想把它扒下来自己用。
> **核心优势**：目标网站的 CDN 可能有 403 防盗链，但浏览器能正常看 = 浏览器已经拿到了全部资源。
> 我们用 Playwright 在浏览器内存里直接拦截下来。

## 何时激活本 Skill

用户发送一个网站网址并输入以下关键词之一时激活：

- `[抄网页]`
- `抄网页`
- `克隆这个网站`
- `帮我复制这个页面`
- 任何表达"我要把这个网页抄下来"意图的消息

### 跟"抄袭者"的区别

| | 抄袭者 CodeCloner | 抄网页 Cloner Web |
|---|---|---|
| **目标** | GitHub/GitLab 代码仓库 | 任意网站 URL |
| **核心操作** | 改名换姓、品牌清洗、功能裁剪 | CSS 内联、图片 base64、离线打包 |
| **输出** | 一个可运行的自有代码项目 | 一个 单文件 HTML（浏览器直接打开） |
| **技术依赖** | git, 文本替换 | Playwright, Python |
| **说人话** | 把别人的代码项目"洗"成你自己的项目 | 把别人的网页"拍"下来变成离线文件 |

---

## 🚨 铁律

1. **老板不懂代码** —— 严禁直接扔 Python 脚本、HTML 代码。用大白话说清楚。
2. **所有操作由你来执行** —— 老板只给网址和需求，不改一行代码。
3. **每步都要问老板** —— 尤其是输出目录、是否需要截图等功能。
4. **跑完必须给老板看结果** —— 用 `start "" "output/full_clone.html"` 打开浏览器让老板看效果。

---

## 第 1 步：环境检查

> 目标：确保运行环境齐备。

在开始之前，检查以下依赖是否已安装：

```bash
# 检查 Python
python --version

# 检查 Playwright
python -c "from playwright.async_api import async_playwright; print('Playwright OK')"

# 如果 Playwright 没装浏览器内核
python -m playwright install chromium
```

如果缺少依赖，直接安装：

```bash
pip install playwright
python -m playwright install chromium
```

**检查结果用大白话告诉老板：**

```
✅ 环境就绪：Python 3.11 + Playwright + Chromium 浏览器内核
```

---

## 第 2 步：克隆网页

> 目标：生成 1:1 完整复刻的网页文件。

### 2.1 准备

1. 确认目标 URL（问老板要抄哪个页面）
2. 确认输出目录（默认当前工作目录的 `clone_output/`，老板有特殊要求再改）
3. 确认是否需要截图（默认全页面截图留存）

### 2.2 执行克隆

使用 `scripts/clone_intercept.py` 脚本：

```bash
cd cloner-web
python scripts/clone_intercept.py
```

脚本自动完成：
1. 用 Playwright 打开目标 URL（1440×900 视口）
2. 通过 `page.on("response")` 拦截所有 CSS（17个/734KB）、图片（16张/~2.4MB）
3. 把 CSS 合并成 `<style>` 块插入 `<head>`
4. 把图片转换为 base64 data URI 并替换所有 `<img src>` 引用
5. 删除外部 CDN CSS 链接（避免离线后 403 空白）
6. 输出单文件 HTML + 截图留档

### 2.3 关键参数说明

脚本顶部有两个变量可改：

```python
TARGET_URL = "https://example.com"    # ← 改这里为目标网页
OUTPUT_DIR = Path("./clone_output")   # ← 输出目录
```

---

## 第 3 步：验证和交付

> 目标：确保老板看到的效果和原站一致。

### 3.1 本地打开验证

```bash
# Windows
start "" "clone_output/full_clone.html"

# macOS
open clone_output/full_clone.html

# Linux
xdg-open clone_output/full_clone.html
```

### 3.2 对比原站

让老板在浏览器中同时打开：
- 原站（目标 URL）
- 本地 `full_clone.html`

对比以下维度：

| 维度 | 自包含文件 | 原站 |
|:----:|:----------:|:----:|
| 布局结构 | ✅ 完全一致（CSS 全部内联） | — |
| 图片显示 | ✅ 全部 base64 内嵌 | — |
| 文字内容 | ✅ 完全一致 | — |
| 交互元素 | ⚠️ 链接可点，动态功能可能受限 | 完整 |
| 离线可用 | ✅ **完全离线** | ❌ 需要网络 |

### 3.3 交付物清单

```
clone_output/
├── full_clone.html    ← 单文件完整网页（~5-15MB）
└── screenshot.png     ← 全页面截图（留档用）
```

---

## 第 4 步：常见问题处理

### 4.1 图片替换失败（replaced = 0/16）

**原因**：HTML 中的图片 URL 和浏览器拦截到的 URL 格式不一致。
**解决方案**：脚本已内置文件名模糊匹配（去掉扩展名做 key），如果还是失败：

- 手动检查 HTML 中 `<img src="...">` 的 URL 格式
- 检查拦截到的 response URL 格式
- 可能在 `page.on("response")` 前已加载的图片不会被捕获（极小概率）

### 4.2 页面有弹窗/遮罩层

某些网站首次访问会弹 Cookie 横幅或地区选择弹窗。

**解决方案**：在脚本的 `page.on("response")` 前注入 JS 移除弹窗：

```python
# 加载页面后等待并关闭弹窗
await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
await page.evaluate("""
    document.querySelectorAll('[class*="cookie"], [class*="popup"], [class*="modal"], [class*="overlay"]')
        .forEach(el => el.remove());
""")
```

### 4.3 页面需要登录

如果目标页面需要登录，有两种方式：
1. 手动登录后导出 Cookie，在 Playwright 中注入：`await context.add_cookies(cookies)`
2. 让老板提供登录态即可

### 4.4 懒加载图片没出来

`wait_until="networkidle"` 通常能等到大部分懒加载图片触发，但如果页面用 IntersectionObserver 且图片不在视口内：

```python
# 强制滚动到底部触发懒加载
await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
await asyncio.sleep(2)
```

### 4.5 最终文件太大（> 20MB）

图片 base64 会让文件膨胀约 33%。如果太大：
1. 只在 `page.on("response")` 中拦截小于 500KB 的图片（改 `len(body) < 2_000_000` 阈值）
2. 或者跳过图片内联，只内联 CSS，图片用原 URL（需要网络才能显示）

---

## 工作流总览

```
┌──────────────┐
│  第 1 步      │  环境检查 → Python / Playwright / Chromium 就绪
└──────┬───────┘
       ▼
┌──────────────┐
│  第 2 步      │  克隆网页 → 
│              │    Playwright 打开页面
│              │    ↓
│              │    拦截 CSS + 图片
│              │    ↓
│              │    内联为单文件 HTML
│              │    ↓
│              │    截图留档
└──────┬───────┘
       ▼
┌──────────────┐
│  第 3 步      │  验证交付 → 浏览器打开对比 → 交付 full_clone.html + screenshot.png
└──────────────┘
```

## 已知局限

| 局限 | 说明 |
|:----:|------|
| **页面大小** | 图片多的页面，最终 HTML 可能 10-50MB。浏览器打开慢但能用 |
| **动态内容** | JavaScript 动态渲染的内容会被捕获，但交互功能（表单、动画）在纯 HTML 中可能失效 |
| **登录态** | 需要登录的页面无法直接克隆，需要先注入 Cookie |
| **字体文件** | 字体文件通常较大（> 2MB），默认不内联。页面字体会回退到系统字体 |
| **视频** | 视频流无法内联，只保留 `<video>` 标签结构 |
