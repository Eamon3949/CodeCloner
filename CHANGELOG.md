# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2026-07-12

### Fixed
- **CSSOM 捕获修复** — styled-components v6 用 `insertRule()` 注入样式，`<style>.textContent` 为空。
  改为从 `document.styleSheets[i].cssRules` 读取运行时样式
- **图片替换改为 DOM 级** — 不再用正则匹配 HTML 文本，改用 Playwright `page.evaluate()` 
  在浏览器中直接替换 `<img src>`、`<source srcset>`、CSS background-image、favicon 
  的 URL 为 data URI。彻底解决 `srcset` 漏网、裸 base64 缺前缀、favicon 不替换等问题
- **懒加载图片补抓** — 滚动 5 次触发 IntersectionObserver，未拦截的图片用 httpx 替补下载
- 已验证：Coinbase 中文首页（62 图片 → 6.7MB 单文件，0 未内联 `<img>`）

## [2.0.0] - 2026-07-10

### Added
- **新模块: cloner-web（抄网页）** — 把任意网页克隆为完全自包含的单文件 HTML
  - Playwright 响应拦截技术：在浏览器内存中直接捕获 CSS 和图片，绕过 CDN 403 防盗链
  - CSS 全部内联 + 图片 base64，无需网络即可离线浏览
  - 截图留档 + 一键浏览器打开验证
  - 已验证：OpenAI 中文首页（17 CSS + 16 图片 → 9.2MB 单文件）
- **路由系统** — 根 SKILL.md 自动判断用户链接类型，路由到对应模块
  - GitHub/GitLab/Bitbucket 链接 → cloner-code（原抄袭者）
  - 其他网址 → cloner-web（抄网页）
  - 支持 `[激活抄袭者]` / `[抄网页]` / 直接丢链接三种激活方式
- 新增参考文档：
  - `cloner-web/SKILL.md` — 网页克隆完整工作流
  - `cloner-web/scripts/clone_intercept.py` — Playwright 拦截脚本模板
  - `cloner-web/references/page-cloning-notes.md` — 技术原理和已知陷坑

### Changed
- 根 SKILL.md 从单一流程改为路由入口 + 双模块架构
- README.md 重写：体现双模块设计，中英文同步更新
- VERSION → 2.0.0

### Removed
- 无

### Added
- **logo.svg** — Project logo (two overlapping cards with clone badge)
- **Bilingual README** — Full English translation alongside Chinese
- Language switcher at top of README

### Changed
- README structure: merged Chinese and English into single document with clear sections
- Project structure now includes logo.svg

## [1.3.0] - 2026-06-09

### Added
- Multi-platform source support: GitHub, GitLab, Bitbucket (not just GitHub)
- Security scan step (Step 4.4): npm audit, pip-audit, govulncheck, cargo audit
- Rollback mechanism: git stash / git checkout / re-clone instructions
- `--auto` mode edge case handling table (6 conditions that still interrupt)
- Contributing section in README
- Default branch auto-detection (main vs master)
- Cross-platform clone paths (Linux/Mac + Windows)

### Changed
- All PPT-specific examples replaced with generic ones (SKILL.md, README, workflow.md)
- Frontmatter: "GitHub 开源项目" → "开源项目" (platform-agnostic)
- README: added Git/gh CLI to prerequisites
- README: Codex install uses AGENTS.md instead of CODEX.md
- README: badge anchor links fixed for GitHub rendering
- LICENSE year: 2024 → 2026
- All CHANGELOG dates: 2025 → 2026

## [1.2.0] - 2026-06-09

### Added
- Multi-platform support: Claude Code, Codex, OpenClaw, Hermes Agent
- Installation guide for each supported platform
- MIT LICENSE file
- GitHub topics for discoverability
- This CHANGELOG

### Changed
- README.md: rewrote for professional presentation
- README.md: fixed duplicate tree entries and stale count
- SKILL.md: fixed broken directory tree after case study removal

### Removed
- Case study file `references/case-study-slidemaster.md`

## [1.1.0] - 2026-06-03

### Added
- `references/naming-variants.md` — intelligent naming variant mapping rules (8 variants)
- `references/cleanliness-score.md` — 0-100 cleanliness scoring system with P0/P1/P2 tiers
- `references/case-study-slidemaster.md` — real-world full walkthrough case study
- Auto/quiet mode (`--auto` flag) for hands-off operation
- Step 0 feasibility gate (license + scale + tech stack check)
- Step 4 smoke test verification
- Step 5.4 cleanliness score gate before delivery

### Changed
- `SKILL.md`: expanded from 4-step to 6-step workflow
- `references/branding-checklist.md`: added P0/P1/P2 priorities and grep command templates
- `references/workflow.md`: added tech stack decision tree

## [1.0.1] - 2026-06-01

### Added
- Feasibility assessment gate (license compatibility matrix)
- Smoke test step (syntax + runtime verification)
- Tech stack decision tree in workflow.md
- Grep command templates in branding-checklist.md

### Changed
- `SKILL.md`: major rule upgrade, added license check table and verification steps

## [1.0.0] - 2026-06-01

### Added
- Initial release
- `SKILL.md` with frontmatter and 4-step workflow
- `VERSION`, `README.md`, `.gitignore`
- `references/workflow.md` — detailed workflow document
- `references/branding-checklist.md` — brand cleanup checklist
