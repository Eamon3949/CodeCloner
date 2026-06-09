# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-06-09

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
