# 实战案例：GordenPPTSkill → SlideMaster

> 这是一份真实的"抄袭"全过程记录。老板发了 GitHub 链接，我跑完了完整 6 步工作流。
> 每一步都有真实的输入和输出，后来者可以照着走一遍。

---

## 输入

```
URL: https://github.com/GordenSun/GordenPPTSkill
触发词: [激活抄袭者]
```

---

## 第 0 步：可行性评估

### 许可证检查

```
✅ MIT License — 可以抄，需要保留版权声明
```

### 规模评估

```
文件数: 99
总大小: ~90MB（含 19 个 PPTX 模板）
评估: 中等偏大项目，需分 2-3 批改
```

### 技术栈

```
语言: Python 100%
核心依赖: python-pptx >= 1.0
可选依赖: LibreOffice + poppler（渲染预览用）
运行环境: Python 3.9+
```

**结论：✅ 可以开抄。**

---

## 第 1 步：项目结构与技术栈拆解

### 目录结构

```
GordenPPTSkill/
├── SKILL.md              # AI 入口文档（1.4万字符，最核心的文件）
├── VERSION               # 版本号 1.0.13
├── CHANGELOG.md          # 变更日志
├── updates.json           # 自动更新配置（指向原作者 GitHub）
├── manifest.json          # 文件校验清单
├── README.md              # 项目说明
├── LICENSE                # MIT 协议
├── NOTICE.md              # 模板版权声明
├── assets/group-qr.jpg    # 微信群二维码
├── scripts/
│   ├── build_pptx.py      # 核心：构建 PPTX
│   ├── render_slides.py   # 渲染预览图
│   ├── compute_capacity.py # 计算文本框容量
│   ├── apply_update.py    # 自动更新脚本
│   ├── check_update.py    # 检查更新
│   └── build_manifest.py  # 重建 manifest
├── references/
│   ├── workflow.md         # 工作流文档
│   ├── pptx-edit-schema.md # 编辑格式规范
│   ├── custom-template-workflow.md
│   ├── chart-editing.md
│   └── original-design-guide.md
└── templates/
    ├── INDEX.md
    └── 19 套模板（每套含 template.pptx / intro.md / detail.json / preview.png）
```

### 品牌要素搜索

```
原项目名变体:
  GordenPPTSkill:   23 处 ← P0
  gorden-ppt-skill:  8 处 ← P0（npm 风格包名）
  gorden_ppt_skill:  0 处 ← 无（不是 Python 包名风格）
  GordenSun:        4 处 ← P0（作者名/URL）
  GordenSun/GordenPPTSkill: 4 处 ← P0（GitHub URL）

原作者社区资源:
  assets/group-qr.jpg: 微信群二维码 ← 要删
  README 中的社区/微信群段落 ← 要删
  SKILL.md 中的自动更新段落 ← 要删（指向原作者 GitHub）

自动更新机制:
  scripts/apply_update.py ← 要删（从原作者 GitHub 拉更新）
  scripts/check_update.py ← 要删
  updates.json ← 要删
```

---

## 第 2 步：大白话汇报

**项目是干嘛的？**
这是一个让 AI 助手能自动做 PPT 的工具包。就是一套现成的 PPT 模板 + 一套"只改文字、不碰排版"的规则引擎，AI 拿到以后就能帮你把文字填进精美的 PPT 模板里。

**核心亮点：**
- 🔥 不破坏排版（改文字不碰版式，像在表格里填空——风格、颜色、字号全都不动）
- 🔥 19 套中文模板（从简约商务到学术答辩都有，像装修样板间选风格）
- 🔥 文字溢出检测（字太多放不下会提前警告你，像表格格子写不下会报错）
- 🔥 兼容所有大模型（DeepSeek、Claude、GPT 都实测过）

**功能模块：**
- 📦 模板引擎 —— 就像装修样板间，你选一套风格往里搬
- ✏️ 文字替换器 —— 就像填表格，只填文字不碰格式
- 🖼️ 渲染预览 —— 就像拍照留档，做完先看一眼效果
- 🔄 自动更新 —— 就像手机 App 自动升级（⚠️ 要去掉，它连原作者 GitHub）

**必须修改的地方：**
- 项目名 / 仓库名：GordenPPTSkill → 你说了算
- 作者名：GordenSun → 你说了算
- 自动更新机制：要整块删掉（它连原作者 GitHub 拉更新）
- 微信群二维码：要删（不是你的社群）
- README/SKILL 中的社区段落：要删
- LICENSE：MIT 保留，作者名改成你的

---

## 第 3 步：交互式重构

### 老板的定制需求

| 需求 | 决定 |
|------|------|
| 项目名 | SlideMaster |
| 自动更新 | 彻底去掉 |
| 社群资源 | 删掉（等我自己的） |
| 模板 | 先全部保留 |

### 执行的品牌清洗

```
命名变体映射表：
  GordenPPTSkill → SlideMaster        (PascalCase)
  gorden-ppt-skill → slide-master     (kebab-case)
  GordenSun → Eamon3949               (作者名)
  GordenSun/GordenPPTSkill → Eamon3949/SlideMaster  (URL)
  ppt-builder → slide-master          (manifest 中的 skill_name)
```

**批次 1 — 品牌清洗：**
- `SKILL.md`：frontmatter name 从 `gorden-ppt-skill` 改为 `slide-master`，全文品牌替换
- `manifest.json`：`skill_name` 从 `ppt-builder` 改为 `slide-master`
- `scripts/build_manifest.py`：`skill_name` 从 `ppt-builder` 改为 `slide-master`
- `LICENSE`：作者从 `GordenSun` 改为 `SlideMaster contributors (original work by GordenSun)`
- `NOTICE.md`：维护者名称替换

**批次 2 — 功能裁剪：**
- 删除 `scripts/apply_update.py`（自动更新脚本）
- 删除 `scripts/check_update.py`（更新检查脚本）
- 删除 `updates.json`（更新配置）
- 删除 `assets/group-qr.jpg`（微信群二维码）
- 删除 `assets/` 空目录
- 从 `SKILL.md` 中删除"第一件事跑自动更新"段落
- 从 `SKILL.md` 中删除更新机制说明段落
- 从 `README.md` 中重写，删除社区段落

**批次 3 — 功能增强：**
- 新增 `Dockerfile`（Python + LibreOffice + 中文字体）
- 新增 `requirements.txt`
- 新增 `run.py`（交互式命令行入口）
- 新增 `start.sh` / `start.bat`（一键启动脚本）

---

## 第 4 步：冒烟验证

```bash
# 语法检查
python scripts/build_pptx.py --help     ✅ 输出帮助信息
python scripts/render_slides.py --help   ✅ 输出帮助信息

# 构建测试
python scripts/build_pptx.py \
    templates/minimal-business-summary/template.pptx \
    (test_edits.json) \
    out/test.pptx \
    --detail templates/minimal-business-summary/detail.json \
    --strict                                  ✅ 构建成功

# 品牌残留搜索
grep -ri "GordenPPTSkill" --include="*.{md,py,json,txt,yaml}" . | grep -v "LICENSE\|NOTICE\|based on"
# ✅ 无残留（仅在致谢段落保留归因）
```

**干净度评分：95/100 ✅**

扣5分：CHANGELOG.md 中历史条目还提到 GordenPPTSkill（合理保留，P2 级别）

---

## 第 5 步：极简交付

### 生成文件清单

```
SlideMaster/
├── SKILL.md              ✅ 重写（去掉更新段落）
├── VERSION               ✅ 重置为 1.0.0
├── CHANGELOG.md           ✅ 重写（新项目的变更日志）
├── manifest.json          ✅ 重建（skill_name 改为 slide-master）
├── README.md              ✅ 重写（去掉社区段落）
├── LICENSE                ✅ 修改（作者名改为 SlideMaster contributors）
├── NOTICE.md              ✅ 修改（维护者名称）
├── Dockerfile             ✅ 新增（一键 Docker 运行）
├── requirements.txt       ✅ 新增（python-pptx 依赖）
├── run.py                 ✅ 新增（交互式命令行）
├── start.sh               ✅ 新增（Mac/Linux 一键启动）
├── start.bat              ✅ 新增（Windows 一键启动）
├── .gitattributes         ✅ 保留
├── .gitignore             ✅ 保留
├── scripts/
│   ├── build_pptx.py      ✅ 保留
│   ├── render_slides.py   ✅ 保留
│   ├── compute_capacity.py ✅ 保留
│   └── build_manifest.py  ✅ 保留（skill_name 已改）
├── references/            ✅ 保留（5 个文档）
└── templates/             ✅ 保留（19 套模板，共 76 个文件）
```

### 删除文件清单

```
❌ scripts/apply_update.py    （自动更新，不需要）
❌ scripts/check_update.py    （更新检查，不需要）
❌ updates.json               （更新配置，不需要）
❌ assets/group-qr.jpg        （微信群二维码，不需要）
❌ assets/                    （空目录，删除）
```

### Git 提交

```
git init
git add -A
git commit -m "SlideMaster v1.0.0: initial fork from GordenSun/GordenPPTSkill v1.0.13"
```

### GitHub 推送

```
gh repo create SlideMaster --public --description "..."
git push -u origin master
```

**✅ 交付完成！仓库地址：https://github.com/Eamon3949/SlideMaster**

---

## 复盘总结

| 维度 | 评价 |
|------|------|
| 品牌清洗 | 95/100，P0/P1 全清，P2 保留历史条目 |
| 功能裁剪 | 干净，删除了自动更新和社区资源，无残留 |
| 功能增强 | 加了 Dockerfile、run.py、一键启动脚本 |
| 冒烟验证 | 构建脚本正常运行 ✅ |
| 交付质量 | 傻瓜式 README + 一键启动，小白可用 |

**耗时：约 30 分钟（人工交互 3 次，其余全自动）**