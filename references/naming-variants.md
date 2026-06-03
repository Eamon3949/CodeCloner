# 命名变体映射规则

> "把 SlideMaster 改成 MyPPT" 不是简单的文本替换——如果你只替换了 `SlideMaster`，
> 那 `slide-master`、`slide_master`、`SLIDE_MASTER`、`slideMaster` 全都还留在代码里。
> 这份规则确保所有变体形式都被替换，一个不漏。

---

## 第 1 步：生成变体表

收到老板给的新项目名后，**立即生成以下变体表**，替换时每个变体都要搜一遍。

### 变体生成规则

假设原项目名（从仓库/包名/目录名识别）和老板给的新名字如下：

| 原名 | 新名 |
|------|------|
| `GordenPPTSkill`（从仓库名识别） | `SlideMaster`（老板指定） |

自动生成所有变体：

| 变体形式 | 原名变体 | 新名变体 | 说明 |
|---------|---------|---------|------|
| **PascalCase** | `GordenPPTSkill` | `SlideMaster` | 类名、组件名 |
| **camelCase** | `gordenPPTSkill` | `slideMaster` | JS 变量、函数名 |
| **kebab-case** | `gorden-ppt-skill` | `slide-master` | npm 包名、URL 路径、CSS class |
| **snake_case** | `gorden_ppt_skill` | `slide_master` | Python 模块名、文件名 |
| **SCREAMING_SNAKE** | `GORDEN_PPT_SKILL` | `SLIDE_MASTER` | 常量名、环境变量 |
| **全小写** | `gordenpptskill` | `slidemaster` | Docker 镜像名、配置值 |
| **点分** | `gorden.ppt.skill` | `slide.master` | Java 包路径、某些配置 |
| **URL 路径** | `GordenSun/GordenPPTSkill` | `Eamon3949/SlideMaster` | GitHub URL |

### 特殊情况处理

- 如果原名包含作者前缀（如 `GordenSun/GordenPPTSkill`），**也要单独替换作者前缀**
- 如果原名里有缩写（如 `PPT`），生成变体时要考虑**缩写展开**和**缩写折叠**：
  - `GordenPPTSkill` ↔ `GordenPptSkill` ↔ `gorden-ppt-skill` ↔ `gorden_ppt_skill`
- 如果新名包含数字（如 `App2`），生成变体时注意数字的分隔：
  - `App2` → `app-2` / `app_2` / `APP_2`

---

## 第 2 步：搜索确认影响范围

对每个变体形式，**先搜再替**：

```bash
# 对每个变体跑一遍 grep，记录出现次数
for variant in "GordenPPTSkill" "gordenPPTSkill" "gorden-ppt-skill" "gorden_ppt_skill" "GORDEN_PPT_SKILL" "gordenpptskill" "GordenSun/GordenPPTSkill"; do
  count=$(grep -ri "$variant" --include="*.{py,js,ts,jsx,tsx,go,rs,java,rb,php,md,txt,json,yaml,yml,toml,cfg,ini,sh,bat,html,css,xml,env,conf}" . | wc -l)
  echo "  $variant: $count 处"
done
```

输出示例：
```
品牌要素搜索结果：
  GordenPPTSkill: 23 处  ← P0 必须全改
  gorden-ppt-skill: 8 处  ← P0 npm 包名
  gorden_ppt_skill: 5 处  ← P0 Python 模块
  gordenPPTSkill:  3 处  ← P0 JS 变量
  GORDEN_PPT_SKILL: 2 处  ← P1 常量
  gordenpptskill:   1 处  ← P1 Docker
  GordenSun/GordenPPTSkill: 4 处  ← P0 URL
```

把这个表发给老板确认后，再开始替换。

---

## 第 3 步：按变体逐个替换

替换顺序：**从最长变体开始，避免短变体误匹配长变体。**

```
替换顺序（从长到短）：
1. GordenSun/GordenPPTSkill → Eamon3949/SlideMaster    （URL，最长）
2. GORDEN_PPT_SKILL → SLIDE_MASTER                      （常量）
3. gorden_ppt_skill → slide_master                      （Python 模块）
4. gorden-ppt-skill → slide-master                      （npm 包名）
5. gordenPPTSkill → slideMaster                         （JS 变量）
6. GordenPPTSkill → SlideMaster                          （类名/主名）
7. gordenpptskill → slidemaster                          （全小写）
8. GordenSun → Eamon3949                                 （作者前缀，单独替换）
```

⚠️ **每次替换后立刻验证**：
```bash
# 确认该变体无残留
grep -ri "GordenSun/GordenPPTSkill" --include="*.{py,js,ts,json,yaml,yml,toml,md}" . | grep -v "attribution\|based on\|forked from"
# 应该输出为空
```

---

## 第 4 步：包名冲突预检

替换完成后，在推送之前，**检查新名字是否和已有的公开包冲突**：

```bash
# PyPI 包名检查
curl -s "https://pypi.org/pypi/slide-master/json" | python -c "import sys; print('⚠️ PyPI 上已存在包 slide-master')" 2>/dev/null || echo "✅ PyPI 包名可用: slide-master"

# npm 包名检查
curl -s "https://registry.npmjs.org/slide-master" | python -c "import sys,json; d=json.load(sys.stdin); print('⚠️ npm 上已存在包 slide-master') if 'name' in d else print('✅ npm 包名可用: slide-master')" 2>/dev/null

# GitHub 仓库检查
curl -s "https://api.github.com/repos/Eamon3949/SlideMaster" | python -c "import sys,json; d=json.load(sys.stdin); print('⚠️ GitHub 仓库已存在') if 'full_name' in d else print('✅ GitHub 仓库名可用')"
```

如果冲突：
- PyPI/npm 冲突 → 改包名或加 scope（如 `@eamon3949/slide-master`）
- GitHub 冲突 → 改仓库名

---

## 第 5 步：文件名和目录名替换

文本替换完后，别忘了**文件名和目录名**也可能包含旧项目名：

```bash
# 查找包含旧项目名的文件/目录
find . -name "*gorden*" -o -name "*Gorden*" | grep -v ".git/"

# 重命名（示例）
mv src/gorden_ppt_skill/ src/slide_master/
mv tests/test_gorden_ppt_skill.py tests/test_slide_master.py
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
║ 原名:  GordenPPTSkill                        ║
║ 新名:  SlideMaster                           ║
║ 原作者: GordenSun                            ║
║ 新作者: Eamon3949                            ║
║ 原URL:  github.com/GordenSun/GordenPPTSkill  ║
║ 新URL:  github.com/Eamon3949/SlideMaster     ║
╠══════════════════════════════════════════════╣
║ PascalCase:     GordenPPTSkill → SlideMaster ║
║ camelCase:      gordenPPTSkill → slideMaster  ║
║ kebab-case:  gorden-ppt-skill → slide-master  ║
║ snake_case:  gorden_ppt_skill → slide_master  ║
║ SCREAMING:  GORDEN_PPT_SKILL → SLIDE_MASTER   ║
║ lowercase:     gordenpptskill → slidemaster    ║
║ dot-separated: gorden.ppt.skill → slide.master ║
╠══════════════════════════════════════════════╣
║ PyPI 冲突检查:  ✅ 可用 / ⚠️ 已存在           ║
║ npm 冲突检查:   ✅ 可用 / ⚠️ 已存在           ║
║ GitHub 冲突检查: ✅ 可用 / ⚠️ 已存在          ║
╚══════════════════════════════════════════════╝
```