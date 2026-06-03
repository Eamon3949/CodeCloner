# 干净度评分系统

> 洗完稿到底干净不干净？光说"替换完了"不行，得有个分数。
> 这份评分系统让你把残留痕迹量化成 0-100 分，90 分以上才允许交付。

---

## 评分维度

| 维度 | 权重 | 满分 | 扣分规则 |
|------|------|------|---------|
| **P0 核心替换** | 最重要 | 40 | 每处残留扣 5 分，扣完为止 |
| **P0 import/包名** | 最重要 | 30 | 每处残留扣 10 分，扣完为止 |
| **P1 文档/配置** | 重要 | 15 | 每处残留扣 3 分，扣完为止 |
| **P2 辅助信息** | 可选 | 15 | 每处残留扣 1 分，最低 0 分 |

---

## 扫描命令

品牌清洗完成后，运行以下命令计算分数：

```bash
#!/bin/bash
# 干净度扫描脚本
# 用法: bash cleanliness_scan.sh <原项目名> <原作者名> <原URL路径>

OLD_NAME="$1"        # 例: OriginalApp
OLD_AUTHOR="$2"      # 例: OriginalAuthor
OLD_URL="$3"         # 例: OriginalAuthor/OriginalApp

EXCLUDE="--include="*.{py,js,ts,jsx,tsx,go,rs,java,rb,php,md,txt,json,yaml,yml,toml,cfg,ini,sh,bat,html,css,xml,env,conf}""

# 归因排除词（这些上下文中的残留是合理的）
ATTRIBUTION="attribution\|based on\|forked from\|inspired by\|upstream\|LICENSE\|original.*by"

echo "========================================="
echo "  干净度扫描报告"
echo "========================================="
echo ""

# P0 核心替换：项目名变体
echo "--- P0 核心替换（满分 40）---"
for variant in "$OLD_NAME" "$(echo $OLD_NAME | sed 's/\([A-Z]\)/-\L\1/g;s/^-//')"; do
    count=$(grep -ri "$variant" $EXCLUDE . 2>/dev/null | grep -v "$ATTRIBUTION" | wc -l)
    if [ $count -gt 0 ]; then
        echo "  ⚠️  $variant: ${count} 处残留"
    else
        echo "  ✅  $variant: 0 处残留"
    fi
done

# P0 import/包名
echo ""
echo "--- P0 import/包名路径（满分 30）---"
IMPORT_PATTERNS="import $OLD_NAME\|from $OLD_NAME\|require('$OLD_NAME')\|require(\"$OLD_NAME\")"
count=$(grep -ri "$IMPORT_PATTERNS" $EXCLUDE . 2>/dev/null | wc -l)
if [ $count -gt 0 ]; then
    echo "  ⚠️  import/require 路径: ${count} 处残留"
else
    echo "  ✅  import/require 路径: 0 处残留"
fi

# P1 文档/配置
echo ""
echo "--- P1 文档配置（满分 15）---"
for file in "README.md" "package.json" "pyproject.toml" "docker-compose.yml" "Dockerfile" ".github" ".env.example"; do
    count=$(grep -ri "$OLD_NAME" "$file" 2>/dev/null | grep -v "$ATTRIBUTION" | wc -l)
    if [ $count -gt 0 ]; then
        echo "  ⚠️  $file: ${count} 处残留"
    fi
done

# P2 辅助信息
echo ""
echo "--- P2 辅助信息（满分 15）---"
p2_total=0
for file in "CHANGELOG.md" "HISTORY.md" ".github/ISSUE_TEMPLATE" ".github/PULL_REQUEST_TEMPLATE.md"; do
    if [ -f "$file" ]; then
        count=$(grep -ri "$OLD_NAME" "$file" 2>/dev/null | wc -l)
        p2_total=$((p2_total + count))
    fi
done
echo "  ℹ️  CHANGELOG/模板中残留: ${p2_total} 处（可接受，建议保留归因）"

echo ""
echo "========================================="
```

---

## 计算规则

### P0 核心替换（满分 40 分）

```
P0_core = 40 - (残留处数 × 5)
P0_core = max(P0_core, 0)
```

扫描范围：项目名所有变体形式（PascalCase、kebab-case、snake_case、SCREAMING_SNAKE、全小写），排除归因上下文。

**0 处残留 = 40 分**

### P0 import/包名路径（满分 30 分）

```
P0_import = 30 - (残留处数 × 10)
P0_import = max(P0_import, 0)
```

扫描范围：`import` / `from` / `require` / `use` 语句中的旧包名。

**0 处残留 = 30 分。哪怕 1 处残留项目就跑不起来，所以每处扣 10 分。**

### P1 文档/配置（满分 15 分）

```
P1_doc = 15 - (残留处数 × 3)
P1_doc = max(P1_doc, 0)
```

扫描范围：README.md、package.json、pyproject.toml、Dockerfile、docker-compose.yml、.env.example、.github/。

### P2 辅助信息（满分 15 分）

```
P2_misc = max(15 - (残留处数 × 1), 0)
```

扫描范围：CHANGELOG.md、GitHub issue/PR 模板。

**P2 残留通常合理（保留历史记录和归因），所以每处只扣 1 分。**

---

## 评分等级

| 分数 | 等级 | 说明 |
|------|------|------|
| **95-100** | 🟢 A 级 | 可以交付，几乎无残留 |
| **80-94** | 🟡 B 级 | 可以交付，P2 有合理残留（如 CHANGELOG 归因） |
| **60-79** | 🟠 C 级 | 不建议交付，P1 有残留，需继续清洗 |
| **0-59** | 🔴 D 级 | **禁止交付**，P0 有残留，项目跑不起来或严重侵权 |

### 交付门槛

- **≥ 80 分**：允许交付
- **≥ 90 分**：可以直接推送 GitHub
- **< 80 分**：必须继续清洗，直到达到 80 分

---

## 评分报告模板

清洗完成后，向老板汇报：

```
📊 干净度评分报告

P0 核心替换（满分 40）：
  ✅ OriginalApp → YourApp: 0 处残留
  ✅ original-app → your-app: 0 处残留
  ✅ OriginalAuthor/OriginalApp → YourName/YourApp: 0 处残留
  P0 核心得分: 40/40

P0 import/包名路径（满分 30）：
  ✅ import/require 路径: 0 处残留（该项目无 import 路径引用）
  P0 import 得分: 30/30

P1 文档配置（满分 15）：
  ✅ README.md: 0 处残留
  ✅ manifest.json: 0 处残留
  P1 文档得分: 15/15

P2 辅助信息（满分 15）：
  ℹ️  CHANGELOG.md: 3 处残留（历史条目中的旧名，合理保留）
  P2 辅助得分: 12/15

━━━━━━━━━━━━━━━━━
总分: 97/100 🟢 A 级
✅ 满足交付门槛（≥ 80），可以推送 GitHub
```

---

## 自动降级规则

以下情况**自动降为 D 级（禁止交付）**，不管总分多少：

1. **import 路径有残留** → 项目跑不起来（`ModuleNotFoundError` / `Cannot find module`）
2. **LICENSE 中原作者版权声明被删除** → 违反开源协议
3. **项目名的 PascalCase 形式有残留** → `class OldName` 或 `def OldName` 会导致理解混乱