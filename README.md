<div align="center">

# 🔥 抄袭者 CodeCloner

**把别人的开源项目"抄"过来，洗一遍变成你自己的。**

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/Eamon3949/CodeCloner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/type-AI%20Agent%20Skill-purple.svg)](#-怎么安装)
[![Platforms](https://img.shields.io/badge/platforms-Claude%20Code%20|%20Codex%20|%20OpenClaw%20|%20Hermes-orange.svg)](#-支持的平台)

</div>

---

## 🤔 这是什么？

你看到一个开源项目，心想：**"这东西真好，要是叫我的名字就好了。"**

CodeCloner 就是一个 AI Agent 技能文件。你给它一个开源项目链接，说一声 **`[激活抄袭者]`**，AI 就会自动帮你：

1. 🔍 查清项目能不能抄、怎么抄（许可证检查）
2. 📋 大白话告诉你项目是什么、有什么、要改哪里
3. ✏️ 按你的要求改名字、换品牌、删功能、加功能
4. ✅ 验证改完的东西能跑
5. 📦 打包交付，推到你的 GitHub

**全程不用写一行代码。你只管提需求，AI 帮你干活。**

---

## 🌐 支持的平台

CodeCloner 不绑定任何平台——任何能读 markdown 指令的 AI Agent 都能用：

| 平台 | 怎么用 |
|:----:|--------|
| 🟣 **Claude Code** | 原生 Skill 格式，直接放到 `~/.claude/skills/` 或项目 `.claude/skills/` |
| 🟢 **OpenAI Codex** | 把 SKILL.md 内容贴进项目根目录的 `AGENTS.md` 或作为 system prompt |
| 🟡 **OpenClaw** | 作为 Agent 指令文件导入，或贴进对话开头 |
| 🔵 **Hermes Agent** | 作为 skill/instruction 文件加载，或贴进 system prompt |
| 🔘 **其他 AI Agent** | 只要能读 markdown 规则，就能用 |

---

## 📦 怎么安装？

### Claude Code

```bash
# 方式 1：全局安装（所有项目都能用）
git clone https://github.com/Eamon3949/CodeCloner.git ~/.claude/skills/CodeCloner

# 方式 2：项目级安装（只在当前项目能用）
git clone https://github.com/Eamon3949/CodeCloner.git .claude/skills/CodeCloner
```

装完后在任何对话里输入 `[激活抄袭者]` + 项目链接即可触发。

### OpenAI Codex

```bash
# 把 SKILL.md 内容复制进项目根目录
cp SKILL.md /your/project/AGENTS.md
```

### OpenClaw / Hermes Agent / 其他平台

把 `SKILL.md` 的内容复制粘贴到对话开头，或作为 system prompt / instruction 文件导入。格式是通用 markdown，不需要特殊适配。

---

## ✨ 核心特点

| 特点 | 说明 |
|:----:|------|
| 🛡️ **许可证把关** | 自动检查 MIT / Apache / GPL 等许可证，告诉你能不能抄、要遵守什么 |
| 🔤 **命名全覆盖** | 不只是换个名字——PascalCase、camelCase、kebab-case、snake_case、常量、URL 全部替换，一个不漏 |
| 🧹 **品牌清洗** | 按 P0 / P1 / P2 优先级逐项清洗，内置 0-100 分干净度评分系统 |
| 💬 **大白话汇报** | 全程用你听得懂的话解释，不懂代码也能做决策 |
| 🔇 **静音模式** | 加上 `--auto` 全自动跑，只在你需要的时候才打断你 |
| 📖 **参考文档** | 附带 4 份详细参考（工作流、品牌清单、命名变体、评分系统） |

---

## 🚀 怎么用？

### 你需要什么？

- 一个 GitHub / GitLab / Bitbucket 账号
- 安装了 [Git](https://git-scm.com/)
- 安装了 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 或 [Codex](https://openai.com/codex/) 或其他 AI Agent 工具
- 如果要自动推送仓库：安装 [GitHub CLI (gh)](https://cli.github.com/)
- **不需要懂代码**

### 三步搞定

```
第 1 步 ── 发送项目链接
你：https://github.com/某人/某个项目 [激活抄袭者]
（也支持 GitLab、Bitbucket 等平台的链接）

第 2 步 ── 看报告，提需求
AI：📋 可行性报告：MIT 协议 ✅ 可以抄，约 120 个文件，预计分 2-3 批改完
你：项目叫 MyApp，去掉社区功能

第 3 步 ── 等交付
AI：✅ 改完了！已推送到 https://github.com/你的用户名/MyApp
```

### 静音模式

不想一步步问答？加上 `--auto`，AI 按默认值全自动跑，只在评估不通过时才问你：

```
你：https://github.com/某人/某个项目 [激活抄袭者] --auto
AI：（安静地干活，只在出问题时才问你）
```

---

## 🔄 工作流一览

```
┌─────────────┐
│  第 0 步     │  🛡️ 可行性评估
│  许可证检查   │  → 能不能抄？规模多大？技术栈兼容？
│  规模评估     │  → 不能抄就直接告诉你，不浪费时间
└──────┬──────┘
       │ ✅ 可行
       ▼
┌─────────────┐
│  第 1 步     │  🔍 项目拆解
│  克隆仓库     │  → git clone 到临时目录
│  分析结构     │  → 语言、框架、依赖、运行环境
│  识别品牌要素  │  → 项目名、作者名、URL、Logo……
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  第 2 步     │  📋 大白话汇报
│  一句话说清楚  │  → "这是一个让开发者自动生 API 文档的工具"
│  核心亮点     │  → 3-5 条，每条有比喻
│  问你想改什么  │  → 叫什么名？删什么功能？加什么？
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  第 3 步     │  ✏️ 交互式重构
│  品牌清洗     │  → 批次 1：名字、Logo、版权全换
│  功能裁剪     │  → 批次 2：删你不要的
│  功能增强     │  → 批次 3：加你想要的
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  第 4 步     │  ✅ 冒烟验证
│  语法级验证    │  → 编译检查 / import 检查
│  安全扫描      │  → npm audit / pip-audit 等
│  运行级验证    │  → 项目能启动
│  干净度评分    │  → 搜索残留的原项目名
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  第 5 步     │  📦 极简交付
│  生成运行环境  │  → Dockerfile / 一键启动脚本
│  傻瓜式 README│  → 三步安装法，小白也能跑
│  推送 GitHub │  → 一键推到你的仓库
└─────────────┘
```

---

## 📏 干净度评分系统

洗完稿到底干净不干净？不能光说"替换完了"，得有分数：

| 维度 | 满分 | 扣分规则 | 说明 |
|:----:|:----:|:--------|:-----|
| **P0 核心替换** | 40 | 每处残留扣 5 分 | 项目名、仓库名没换完 = 侵权风险 |
| **P0 包名/import** | 30 | 每处残留扣 10 分 | import 路径没改 = 项目跑不起来 |
| **P1 文档配置** | 15 | 每处残留扣 3 分 | README、package.json 里的旧名 |
| **P2 辅助信息** | 15 | 每处残留扣 1 分 | CHANGELOG、模板中的历史记录 |

| 分数 | 等级 | 结论 |
|:----:|:----:|:-----|
| **95-100** | 🟢 A | 可以放心推送 |
| **80-94** | 🟡 B | 可以交付，P2 有合理残留 |
| **60-79** | 🟠 C | 不建议交付，继续洗 |
| **< 60** | 🔴 D | **禁止交付**，项目跑不起来或严重侵权 |

---

## 📁 项目结构

```
CodeCloner/
├── SKILL.md                        ← 技能入口（6 步工作流规则）
├── VERSION                         ← 版本号
├── LICENSE                         ← MIT 许可证
├── CHANGELOG.md                    ← 变更日志
├── README.md                       ← 你正在看的这个文件
├── .gitignore
└── references/
    ├── workflow.md                  ← 详细工作流（含技术栈决策树）
    ├── branding-checklist.md       ← 品牌清洗清单（P0/P1/P2 优先级 + grep 模板）
    ├── naming-variants.md          ← 命名变体映射规则（8 种变体全覆盖）
    └── cleanliness-score.md        ← 干净度评分系统（0-100 分）
```

---

## 📖 参考文档速览

| 文档 | 一句话说明 |
|------|-----------|
| [workflow.md](./references/workflow.md) | 每一步具体干什么、怎么干、遇到问题怎么办 |
| [branding-checklist.md](./references/branding-checklist.md) | 改名字时照着这个清单走，P0 是必须改的 |
| [naming-variants.md](./references/naming-variants.md) | 项目名的 8 种变体形式，替换时一个不漏 |
| [cleanliness-score.md](./references/cleanliness-score.md) | 0-100 分评分系统，90 分以上才允许交付 |

---

## ⚖️ 许可证支持

| 许可证 | 能不能抄 | 归因要求 |
|:------:|:--------:|---------|
| MIT | ✅ 能 | 保留版权声明 |
| Apache-2.0 | ✅ 能 | 保留版权 + NOTICE |
| BSD | ✅ 能 | 保留版权声明 |
| GPL | ⚠️ 能 | 你的项目也必须开源 |
| AGPL | ⚠️ 能 | 网络服务也要开源 |
| Unlicense | ✅ 能 | 无要求 |
| 无许可证 | 🚫 不能 | 法律上 = 保留所有权利 |

---

## ⚠️ 注意事项

- 本 Skill 产生的项目基于原项目的开源许可证，请遵守原作者的许可条款
- GPL / AGPL 项目抄完后**必须同样开源**，这是法律要求，不是建议
- 不要删除原作者的 LICENSE 文件，而是替换版权声明中的作者名和项目名
- 商业使用请确保获得原项目作者授权

---

## 📜 许可证

本项目采用 [MIT License](./LICENSE) 开源。

---

## 🤝 参与贡献

欢迎贡献！你可以：

- **提 Bug** — 在 [Issues](https://github.com/Eamon3949/CodeCloner/issues) 里描述问题
- **提建议** — 在 Issues 里标记为 `enhancement`
- **提 PR** — Fork 仓库，改完后提 Pull Request
- **加平台** — 如果你用过的 AI Agent 平台不在列表里，告诉我们怎么适配

贡献前请确保：
- 改动不影响 SKILL.md 的通用性（不要加平台特定的硬编码）
- 新加的参考文档放在 `references/` 下
- 更新 CHANGELOG.md

---

<div align="center">

**Made with 🔥 by [Eamon3949](https://github.com/Eamon3949)**

</div>
