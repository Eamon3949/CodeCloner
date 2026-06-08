# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-06-08

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

## [1.1.0] - 2025-06-03

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

## [1.0.1] - 2025-06-01

### Added
- Feasibility assessment gate (license compatibility matrix)
- Smoke test step (syntax + runtime verification)
- Tech stack decision tree in workflow.md
- Grep command templates in branding-checklist.md

### Changed
- `SKILL.md`: major rule upgrade, added license check table and verification steps

## [1.0.0] - 2025-06-01

### Added
- Initial release
- `SKILL.md` with frontmatter and 4-step workflow
- `VERSION`, `README.md`, `.gitignore`
- `references/workflow.md` — detailed workflow document
- `references/branding-checklist.md` — brand cleanup checklist
