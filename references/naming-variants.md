# 命名变体映射规则

> "把 OriginalApp 改成 MyApp" 不是简单的文本替换——如果你只替换了 `OriginalApp`，
> 那 `original-app`、`original_app`、`ORIGINAL_APP`、`originalApp` 全都还留在代码里。
> 这份规则确保所有变体形式都被替换，一个不漏。

---

## 第 1 步：生成变体表

收到老板给的新项目名后，**立即生成以下变体表**，替换时每个变体都要搜一遍。

### 变体生成规则

假设原项目名（从仓库/包名/目录名识别）和老板给的新名字如下：

| 原名 | 新名 |
|------|------|
| `OriginalApp`（从仓库名识别） | `YourApp`（老板指定） |

自动生成所有变体：

| 变体形式 | 原名变体 | 新名变体 | 说明 |
|---------|---------|---------|------|
| **PascalCase** | `OriginalApp` | `YourApp` | 类名、组件名 |
| **camelCase** | `originalApp` | `yourApp` | JS 变量、函数名 |
| **kebab-case** | `original-app` | `your-app` | npm 包名、URL 路径、CSS class |
| **snake_case** | `original_app` | `your_app` | Python 模块名、文件名 |
| **SCREAMING_SNAKE** | `ORIGINAL_APP` | `YOUR_APP` | 常量名、环境变量 |
| **全小写** | `originalapp` | `yourapp` | Docker 镜像名、配置值 |
| **点分** | `original.app` | `your.app` | Java 包路径、某些配置 |
| **URL 路径** | `OriginalAuthor/OriginalApp` | `YourName/YourApp` | GitHub URL |

### 特殊情况处理

- 如果原名包含作者前缀（如 `AuthorName/AuthorApp`），**也要单独替换作者前缀**
- 如果原名里有缩写（如 `PPT`），生成变体时要考虑**缩写展开**和**缩写折叠**：
  - `PPTApp` ↔ `PptApp` ↔ `ppt-app` ↔ `ppt_app`
- 如果新名包含数字（如 `App2`），生成变体时注意数字的分隔：
  - `App2` → `app-2` / `app_2` / `APP_2`

---

## 第 2 步：搜索确认影响范围

对每个变体形式，**先搜再替**：

```bash
# 对每个变体跑一遍 grep，记录出现次数
for variant in "OriginalApp" "originalApp" "original-app" "original_app" "ORIGINAL_APP" "originalapp" "OriginalAuthor/OriginalApp"; do
  count=$(grep -ri "$variant" --include="*.{py,js,ts,jsx,tsx,go,rs,java,rb,php,md,txt,json,yaml,yml,toml,cfg,ini,sh,bat,html,css,xml,env,conf}" . | wc -l)
  echo "  $variant: $count 处"
done
```

输出示例：
```
品牌要素搜索结果：
  OriginalApp: 23 处  ← P0 必须全改
  original-app: 8 处  ← P0 npm 包名
  original_app: 5 处  ← P0 Python 模块
  originalApp:  3 处  ← P0 JS 变量
  ORIGINAL_APP: 2 处  ← P1 常量
  originalapp:  1 处  ← P1 Docker
  OriginalAuthor/OriginalApp: 4 处  ← P0 URL
```

把这个表发给老板确认后，再开始替换。

---

## 第 3 步：按变体逐个替换

替换顺序：**从最长变体开始，避免短变体误匹配长变体。**

```
替换顺序（从长到短）：
1. OriginalAuthor/OriginalApp → YourName/YourApp      （URL，最长）
2. ORIGINAL_APP → YOUR_APP                              （常量）
3. original_app → your_app                              （Python 模块）
4. original-app → your-app                              （npm 包名）
5. originalApp → yourApp                                （JS 变量）
6. OriginalApp → YourApp                                （类名/主名）
7. originalapp → yourapp                                （全小写）
8. OriginalAuthor → YourName                             （作者前缀，单独替换）
```

⚠️ **每次替换后立刻验证**：
```bash
# 确认该变体无残留
grep -ri "OriginalAuthor/OriginalApp" --include="*.{py,js,ts,json,yaml,yml,toml,md}" . | grep -v "attribution\|based on\|forked from"
# 应该输出为空
```

---

## 第 4 步：包名冲突预检

替换完成后，在推送之前，**检查新名字是否和已有的公开包冲突**：

```bash
# PyPI 包名检查
curl -s "https://pypi.org/pypi/your-app/json" | python -c "import sys; print('⚠️ PyPI 上已存在包 your-app')" 2>/dev/null || echo "✅ PyPI 包名可用: your-app"

# npm 包名检查
curl -s "https://registry.npmjs.org/your-app" | python -c "import sys,json; d=json.load(sys.stdin); print('⚠️ npm 上已存在包 your-app') if 'name' in d else print('✅ npm 包名可用: your-app')" 2>/dev/null

# GitHub 仓库检查
curl -s "https://api.github.com/repos/YourName/YourApp" | python -c "import sys,json; d=json.load(sys.stdin); print('⚠️ GitHub 仓库已存在') if 'full_name' in d else print('✅ GitHub 仓库名可用')"
```

如果冲突：
- PyPI/npm 冲突 → 改包名或加 scope（如 `@yourname/your-app`）
- GitHub 冲突 → 改仓库名

---

## 第 5 步：文件名和目录名替换

文本替换完后，别忘了**文件名和目录名**也可能包含旧项目名：

```bash
# 查找包含旧项目名的文件/目录
find . -name "*original*" -o -name "*Original*" | grep -v ".git/"

# 重命名（示例）
mv src/original_app/ src/your_app/
mv tests/test_original_app.py tests/test_your_app.py
```

⚠️ 重命名后必须：
1. 更新所有 `import` 和 `require` 路径
2. 更新 `setup.py` / `pyproject.toml` / `package.json` 中的模块名
3. 重新跑冒烟验证

---

## 快速参考卡片

收到项目名后，**第一时间填这张表**，替换时照着表走：

```
╔══════════════════════════════════════════════╗
║          命名变体映射表                       ║
╠══════════════════════════════════════════════╣
║ 原名:  OriginalApp                            ║
║ 新名:  YourApp                               ║
║ 原作者: OriginalAuthor                       ║
║ 新作者: YourName                             ║
║ 原URL:  github.com/OriginalAuthor/OriginalApp║
║ 新URL:  github.com/YourName/YourApp           ║
╠══════════════════════════════════════════════╣
║ PascalCase:     OriginalApp → YourApp         ║
║ camelCase:      originalApp → yourApp          ║
║ kebab-case:  original-app → your-app            ║
║ snake_case:  original_app → your_app            ║
║ SCREAMING:  ORIGINAL_APP → YOUR_APP             ║
║ lowercase:     originalapp → yourapp             ║
║ dot-separated: original.app → your.app          ║
╠══════════════════════════════════════════════╣
║ PyPI 冲突检查:  ✅ 可用 / ⚠️ 已存在           ║
║ npm 冲突检查:   ✅ 可用 / ⚠️ 已存在           ║
║ GitHub 冲突检查: ✅ 可用 / ⚠️ 已存在          ║
╚══════════════════════════════════════════════╝
```