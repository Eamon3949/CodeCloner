<div align="center">

# 🔥 抄袭者 CodeCloner

**把别人的开源项目"抄"过来，洗一遍变成你自己的。**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/Eamon3949/CodeCloner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/type-Claude%20Code%20Skill-purple.svg)](https://docs.anthropic.com/en/docs/claude-code)

</div>

---

## 🤔 这是什么？

你看到一个开源项目，心想：**"这东西真好，要是叫我的名字就好了。"**

抄袭者就是一个 Claude Code 技能文件。你给它一个 GitHub 开源项目链接，说一声 **`[激活抄袭者]`**，AI 就会自动帮你：

1. 🔍 查清项目能不能抄、怎么抄（许可证检查）
2. 📋 大白话告诉你项目是什么、有什么、要改哪里
3. ✏️ 按你的要求改名字、换品牌、删功能、加功能
4. ✅ 验证改完的东西能跑
5. 📦 打包交付，推到你的 GitHub

**全程不用写一行代码。你只管提需求，AI 帮你干活。**

---

## ✨ 核心特点

| 特点 | 说明 |
|:----:|------|
| 🛡️ **许可证把关** | 自动检查 MIT / Apache / GPL 等许可证，告诉你能不能抄、要遵守什么 |
| 🔤 **命名全覆盖** | 不只是换个名字——PascalCase、camelCase、kebab-case、snake_case、常量、URL 全部替换，一个不漏 |
| 🧹 **品牌清洗** | 按 P0 / P1 / P2 优先级逐项清洗，内置 0-100 分干净度评分系统 |
| 💬 **大白话汇报** | 全程用你听得懂的话解释，不懂代码也能做决策 |
| 🔇 **静音模式** | 加上 `--auto` 全自动跑，只在你需要的时候才打断你 |
| 📖 **实战案例** | 附带完整案例（GordenPPTSkill → SlideMaster），照着走一遍就会 |

---

## 🚀 怎么用？

### 你需要什么？

- 一个 GitHub 账号
- 安装了 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- **不需要懂代码**

### 三步搞定

```
第 1 步 ── 发送项目链接
你：https://github.com/某人/某个项目 [激活抄袭者]

第 2 步 ── 看报告，提需求
AI：📋 可行性报告：MIT 协议 ✅ 可以抄，约 120 个文件，预计分 2-3 批改完
你：项目叫 SlideMaster，去掉社区功能

第 3 步 ── 等交付
AI：✅ 改完了！已推送到 https://github.com/你的用户名/SlideMaster
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
│  一句话说清楚  │  → "这是一个让 AI 自动做 PPT 的工具"
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
├── README.md                       ← 你正在看的这个文件
├── .gitignore
└── references/
    ├── workflow.md                  ← 详细工作流（含技术栈决策树）
    ├── branding-checklist.md       ← 品牌清洗清单（P0/P1/P2 优先级 + grep 模板）
    ├── naming-variants.md          ← 命名变体映射规则（8 种变体全覆盖）
    ├── cleanliness-score.md        ← 干净度评分系统（0-100 分）
    └── case-study-slidemaster.md   ← 实战案例：GordenPPTSkill → SlideMaster
```

---

## 📖 参考文档速览

| 文档 | 一句话说明 |
|------|-----------|
| [workflow.md](./references/workflow.md) | 每一步具体干什么、怎么干、遇到问题怎么办 |
| [branding-checklist.md](./references/branding-checklist.md) | 改名字时照着这个清单走，P0 是必须改的 |
| [naming-variants.md](./references/naming-variants.md) | 项目名的 8 种变体形式，替换时一个不漏 |
| [cleanliness-score.md](./references/cleanliness-score.md) | 0-100 分评分系统，90 分以上才允许交付 |
| [case-study-slidemaster.md](./references/case-study-slidemaster.md) | 真实案例全记录，照着走一遍就会 |

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

## 🎯 实战案例

**GordenPPTSkill → SlideMaster** 全过程记录在 [`references/case-study-slidemaster.md`](./references/case-study-slidemaster.md)。

关键数据：
- 原项目：99 个文件，约 90MB
- 许可证：MIT ✅
- 品牌清洗得分：**95 / 100 🟢 A 级**
- 耗时：约 30 分钟（人工交互 3 次，其余全自动）

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

<div align="center">

**Made with 🔥 by [Eamon3949](https://github.com/Eamon3949)**

</div>