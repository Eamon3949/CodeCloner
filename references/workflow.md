# CodeCloner 详细工作流

本文档是 [`SKILL.md`](../SKILL.md) 的展开版本，详细说明每一步的具体操作。

---

## 第 0 步：可行性评估

详见 SKILL.md 第 0 步。重点检查许可证、技术栈可行性、项目规模。

---

## 第 1 步：项目结构与技术栈拆解

### 1.1 克隆目标仓库

```bash
# 克隆到临时目录，不污染工作区
# Linux/Mac:
git clone <目标仓库URL> /tmp/codecloner-clone
# Windows:
git clone <目标仓库URL> %TEMP%\codecloner-clone
```

如果目标仓库使用了 Git LFS，加上 `--no-tags` 避免拉取大文件。

### 1.2 扫描项目结构

检查以下文件（按优先级排序）：

| 文件 | 说明 | 关注点 |
|------|------|--------|
| `package.json` | Node.js 项目元数据 | 项目名(name)、描述(description)、作者(author)、仓库URL(repository)、依赖(dependencies) |
| `requirements.txt` / `pyproject.toml` | Python 依赖 | 项目名、版本、作者 |
| `Cargo.toml` | Rust 项目 | 包名(name)、作者(authors)、描述(description) |
| `go.mod` | Go 项目 | 模块路径(module) |
| `pom.xml` / `build.gradle` | Java 项目 | groupId、artifactId |
| `composer.json` | PHP 项目 | 包名(name)、描述 |
| `README.md` | 项目说明 | 项目名、描述、安装说明、链接 |
| `LICENSE` | 许可证 | 版权声明中的作者名、年份 |
| `CONTRIBUTING.md` | 贡献指南 | 项目名引用 |
| `CHANGELOG.md` | 变更日志 | 项目名引用 |
| `.github/` | GitHub 配置 | CI/CD 中的仓库名、issue 模板中的项目名 |
| `docker-compose.yml` / `Dockerfile` | 容器配置 | 镜像名、项目名引用 |
| `.env.example` | 环境变量示例 | 项目相关的变量名和默认值 |
| `config/` | 配置文件 | 项目名、URL、密钥占位符 |
| `src/` | 源代码 | 包名、模块名、import 路径 |

### 1.3 识别技术栈

用以下方式自动识别：

- **语言**: 文件扩展名统计（`.py` → Python，`.ts/.tsx` → TypeScript，等等）
- **框架**: 依赖文件中的关键词（`react`/`django`/`flask`/`fastapi`/`spring` 等）
- **运行环境**: `Dockerfile` / `.python-version` / `.nvmrc` / `.tool-versions`
- **包管理器**: `package.json` → npm/yarn/pnpm，`requirements.txt` → pip，`poetry.lock` → poetry

### 1.4 识别品牌要素

全局搜索以下关键词：

- 原项目名（大小写不敏感）
- 原作者名
- 原项目 URL
- Logo/图标文件名

输出一份"品牌要素清单"给老板确认。

---

## 技术栈决策树

识别完技术栈后，用下面的决策树决定交付方案和验证策略：

```
项目类型？
├── Web 应用（有 HTTP 服务器）
│   ├── Python (Django/Flask/FastAPI)
│   │   ├── 交付: Dockerfile + requirements.txt + start.bat
│   │   ├── 验证: python -c "import app" → 启动服务器 → curl localhost
│   │   └── 依赖重生成: pip freeze > requirements.txt
│   ├── Node.js (Express/Next/Nuxt)
│   │   ├── 交付: Dockerfile + package.json + start.bat
│   │   ├── 验证: npm ls → npm test → npm start → curl localhost
│   │   └── 依赖重生成: rm package-lock.json && npm install
│   ├── Go (Gin/Echo/Fiber)
│   │   ├── 交付: Dockerfile + Makefile
│   │   ├── 验证: go build ./... → go test ./... → ./app
│   │   └── 依赖: go mod tidy
│   └── Rust (Actix/Axum)
│       ├── 交付: Dockerfile + Cargo.toml
│       ├── 验证: cargo check → cargo test → cargo run
│       └── 依赖: cargo update
│
├── CLI 工具（命令行程序）
│   ├── Python
│   │   ├── 交付: pyproject.toml + start.bat
│   │   └── 验证: python -m <新包名> --help
│   ├── Node.js
│   │   ├── 交付: package.json (bin 字段) + start.bat
│   │   └── 验证: node dist/index.js --help / npx <新包名> --help
│   ├── Go
│   │   ├── 交付: Makefile + 二进制
│   │   └── 验证: go build -o <新名> . && ./<新名> --help
│   └── Rust
│       ├── 交付: Cargo.toml
│       └── 验证: cargo build --release && ./target/release/<新名> --help
│
├── 库 / SDK（给其他项目用的工具包）
│   ├── Python
│   │   ├── 交付: pyproject.toml / setup.py
│   │   └── 验证: python -c "import <新包名>; print(<新包名>.__version__)"
│   ├── Node.js
│   │   ├── 交付: package.json (name 字段)
│   │   └── 验证: node -e "const lib = require('./'); console.log(lib)"
│   ├── Go
│   │   ├── 交付: go.mod
│   │   └── 验证: go build ./...
│   └── Rust
│       ├── 交付: Cargo.toml (name 字段)
│       └── 验证: cargo check
│
└── 其他 / 混合
    ├── 交付: Dockerfile（最保险）
    ├── 验证: docker build -t <新名> . && docker run <新名> --help
    └── 依赖: 按主语言处理
```

---

## 第 2 步：大白话汇报

### 2.1 项目一句话概括

**模板**：这是一个让 [谁] 能够 [做什么] 的 [类型]。

**示例**：这是一个让开发者能够一键生成 API 文档的工具包，就像一个自动化说明书工厂。

### 2.2 核心亮点（3-5 条）

每条格式：🔥 [大白话描述] （[括号里的通俗注解]）

### 2.3 功能模块

每条格式：📦 [模块名] — [大白话描述] （[通俗比喻]）

### 2.4 必须修改的地方

分两类：
- **必须改的**：项目名、版权、URL、Logo 等
- **建议改的**：去掉不需要的功能模块、调整配置

---

## 第 3 步：交互式重构

### 3.1 收集需求

**分批询问**，不要一次问太多：

第 1 轮（品牌相关）：
- 项目叫什么名字？
- 版权/作者写什么？
- GitHub 用户名和仓库名？
- Logo/图标需要换吗？

第 2 轮（功能相关）：
- 哪些功能要去掉？
- 哪些功能要加上？

第 3 轮（细节确认）：
- 还有其他特殊要求吗？

### 3.2 执行品牌清洗

严格按照 [`branding-checklist.md`](./branding-checklist.md) 逐项执行，优先完成 P0 项。

**替换策略**：
- 文本文件：全局搜索替换（大小写敏感 + 不敏感各跑一遍）
- 配置文件：精确替换（不要误改值里的其他内容）
- 二进制文件：直接替换整个文件（需要老板提供新文件）
- 锁定文件：不手动改，改完依赖后重新生成

**每次替换后**：
- `git diff --stat` 确认改动范围
- 检查是否有遗漏（再搜一遍原项目名）

### 3.3 每批改动的大白话汇报

**格式**：
```
✅ 第 X 批改动完成：
- 把所有 "OldName" 改成了 "NewName"（共 23 处）
- 把 LICENSE 里的作者从 "Author" 改成了 "YourName"
- 更新了 README.md 的项目描述

下一步计划：删除不需要的功能模块 Y 和 Z
```

---

## 第 4 步：冒烟验证

详见 SKILL.md 第 4 步。核心原则：**改完必须验，没验不算完。**

验证优先级：
1. 语法级（必做）—— import/require 能通
2. 编译级（如有编译步骤）—— build 能过
3. 测试级（如有测试）—— test 能过
4. 运行级（交付前必做）—— 能启动

---

## 第 5 步：极简交付

### 5.1 运行环境生成

根据技术栈决策树自动选择交付方案。

### 5.2 README.md 模板

必须包含的章节：
1. **一句话介绍** —— 这是什么，给谁用
2. **系统要求** —— 最少需要什么（操作系统、语言版本）
3. **三步安装** —— 1. 下载 2. 安装依赖 3. 运行
4. **一键启动** —— 双击 `start.bat`（Windows）或 `./start.sh`（Mac/Linux）
5. **常见问题** —— 环境出问题怎么办
6. **致谢** —— 归因原项目（开源协议要求）

### 5.3 Git 初始化

```bash
git init
git add -A
git commit -m "Initial commit: <新项目名> forked and customized from <原项目名>"
```

### 5.4 推送到 GitHub

```bash
# 检测默认分支名（GitHub 默认 main，旧仓库可能是 master）
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
DEFAULT_BRANCH=${DEFAULT_BRANCH:-main}

gh repo create <仓库名> --public --description "<项目描述>"
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin $DEFAULT_BRANCH
```

---

## 异常处理

### 克隆失败
- 检查 URL 是否正确
- 检查网络连接
- 尝试 HTTPS 而不是 SSH
- 仓库可能是私有的，需要老板提供访问权限

### 替换出错
- 用 `git diff` 检查改动
- 如果误改了不该改的文件，用 `git checkout -- <文件>` 恢复
- 重新运行替换

### 推送失败
- 检查 GitHub 认证（`gh auth status`）
- 检查仓库名是否已存在
- 检查网络连接

### 冒烟验证失败
- 读报错信息，区分品牌替换导致 vs 项目本身问题
- 品牌替换导致 → 修好后重新验证
- 项目本身问题 → 告诉老板原因和大白话修复方案
- 修好后重新跑验证，直到通过