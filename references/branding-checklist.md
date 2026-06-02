# 品牌清洗检查清单

> 当你"抄"一个项目过来时，必须把原作者的所有品牌痕迹替换掉。
> 下面这份清单帮你逐项检查，确保没有遗漏。

---

## 优先级说明

| 优先级 | 含义 | 不做的后果 |
|--------|------|-----------|
| **P0** | 必须改，不改项目跑不起来或严重违规 | import 失败 / 版权侵权 / 功能报错 |
| **P1** | 应该改，不改会有明显的原作者痕迹 | README 还是别人的名字 / URL 指向别人的仓库 |
| **P2** | 建议改，不改不影响功能但有残留 | CHANGELOG 里提到原作者 / 注释里还有旧名 |

**清洗顺序：先 P0 → 再 P1 → 最后 P2。P0 全部完成后才能进入冒烟验证。**

---

## Grep 命令模板

替换前先用 grep 确认影响范围，替换后再 grep 确认无残留。

```bash
# 搜索原项目名（大小写不敏感，排除 .git 和二进制）
grep -ri "OldProjectName" --include="*.{py,js,ts,jsx,tsx,go,rs,java,rb,php,md,txt,json,yaml,yml,toml,cfg,ini,sh,bat,html,css,xml,env,conf}" .

# 搜索原项目名（大小写敏感，精确匹配）
grep -rw "OldProjectName" --include="*.{py,js,ts,json,yaml,yml,toml,md}" .

# 搜索原作者名
grep -ri "OriginalAuthor" --include="*.{md,txt,json,yaml,yml,toml,py,js,ts}" .

# 搜索原项目 URL
grep -r "github.com/OldAuthor/OldProject" --include="*.{md,json,yaml,yml,toml,py,js,ts,html}" .

# 搜索原项目名的变体形式
grep -r "old-project-name\|old_project_name\|OLD_PROJECT_NAME\|OldProjectName\|oldprojectname" --include="*.{py,js,ts,json,yaml,yml,toml,md,sh,bat,env}" .

# 替换后验证无残留
grep -ri "OldProjectName" --include="*.{py,js,ts,jsx,tsx,go,rs,java,rb,php,md,txt,json,yaml,yml,toml,cfg,ini,sh,bat,html,css,xml,env,conf}" . | grep -v "attribution\|based on\|forked from\|inspired by\|upstream"
```

---

## ✅ 清洗步骤

每完成一步，打一个 ✅。全部打完才算清洗完成。

### 1. 项目名 / 仓库名 [P0]

- [ ] 全局搜索原项目名（大小写敏感 + 不敏感）
  - 常见位置：README.md, package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml, setup.py, setup.cfg, composer.json
  - 替换成老板指定的新项目名
- [ ] 搜索原项目名的连字符/下划线/驼峰变体
  - 例如原来叫 `MyProject`，也要搜 `my-project`、`my_project`、`MYPROJECT`
- [ ] 搜索原项目的 URL
  - GitHub URL: `github.com/原作者/原项目`
  - 替换成 `github.com/老板/新项目`
- [ ] 检查目录名是否包含原项目名
  - `src/原项目名/` → 改成 `src/新项目名/`

### 2. 包名 / 模块名 / import 路径 [P0]

- [ ] Python: `import 原项目名` → `import 新项目名`
- [ ] JavaScript/TypeScript: `from '原项目名'` / `require('原项目名')` → 新项目名
- [ ] Go: `module github.com/原作者/原项目` → 新路径
- [ ] Rust: `[原项目名]` crate 名 → 新 crate 名
- [ ] Java: `com.原作者.原项目` 包路径 → 新包路径

### 3. README.md [P1]

- [ ] 标题（`# 原项目名`）
- [ ] 描述段落
- [ ] 安装命令中的项目名
- [ ] Badge/图标中的链接
- [ ] 截图/示例代码中的项目名
- [ ] 贡献指南链接
- [ ] 许可证链接

### 4. LICENSE [P0]

- [ ] 版权行中的作者名（`Copyright (c) YEAR 原作者` → `Copyright (c) YEAR 新作者`）
- [ ] 版权行中的项目名（如有）
- [ ] 保留原始开源协议类型（MIT/Apache/GPL），只改作者名

#### 不同协议的归因策略

| 协议 | 归因要求 | 建议做法 |
|------|---------|---------|
| MIT | 保留版权声明 | LICENSE 文件顶部加一行 `Based on <原项目> by <原作者>, licensed under MIT.` |
| Apache-2.0 | 保留版权 + NOTICE + 标注修改 | 保留原始 NOTICE，新建 `NOTICE.md` 列出修改的文件 |
| GPL-2.0/3.0 | 保留版权 + 衍生作品同协议 | LICENSE 中保留原版权行，加上你的版权行 |
| BSD | 保留版权声明 | 同 MIT 做法 |

### 5. 配置文件 [P1]

- [ ] `.env.example` 中的项目相关变量
- [ ] `config/` 目录下的项目名和 URL
- [ ] `docker-compose.yml` 中的容器名、镜像名
- [ ] `Dockerfile` 中的项目名引用
- [ ] CI/CD 配置（`.github/workflows/`）中的仓库名
- [ ] `Makefile` 中的项目名

### 6. HTML / 前端模板 [P1]

- [ ] `<title>` 标签中的项目名
- [ ] `<meta name="description">` 中的描述
- [ ] `<link rel="icon">` favicon 引用
- [ ] `<meta property="og:*">` 社交分享标签
- [ ] 页面中的 Logo 图片引用
- [ ] 页面头部的导航品牌名

### 7. Logo / 图标文件 [P1]

- [ ] `logo.png` / `logo.svg` / `favicon.ico` 等
- [ ] 通常需要老板提供新图片直接替换文件
- [ ] 如果没有新图片，保留原有图片但确认是否可以继续使用

### 8. 隐藏文件和特殊位置 [P2]

- [ ] `.github/ISSUE_TEMPLATE/` 中的项目名
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` 中的项目名
- [ ] `.gitignore` 中可能引用的项目名（通常不需要改）
- [ ] `.editorconfig` / `.eslintrc` / `.prettierrc` 中的项目级设置
- [ ] `CHANGELOG.md` / `HISTORY.md` 中的项目名和历史记录

### 9. 锁定文件（⚠️ 不要手动改）

以下文件不要手动编辑，改完依赖后重新生成：

- [ ] `package-lock.json` → `rm package-lock.json && npm install`
- [ ] `yarn.lock` → `rm yarn.lock && yarn install`
- [ ] `poetry.lock` → `rm poetry.lock && poetry install`
- [ ] `Pipfile.lock` → `rm Pipfile.lock && pipenv install`

### 10. 最终全局搜索确认 [P0]

- [ ] 全局搜索原项目名（大小写不敏感）—— 应该只剩归因说明
- [ ] 全局搜索原作者名 —— 应该只剩 LICENSE / 归因行
- [ ] 全局搜索原项目 URL —— 应该只剩 README 中的致谢/归因链接
- [ ] `git diff --stat` 确认改动范围合理
- [ ] 排除归因行后的残留检查：
  ```bash
  grep -ri "OldProjectName" --include="*.{py,js,ts,json,md,yaml,yml,toml}" . | grep -v "attribution\|based on\|forked from\|inspired by\|upstream\|LICENSE"
  ```
  以上命令输出应为空

---

## 🚫 不要做的事

1. **不要删除原作者的 LICENSE** —— 只改版权行的作者名，保留协议类型
2. **不要手动改锁定文件** —— 运行对应的包管理器重新生成
3. **不要改二进制文件里的文字** —— 直接替换整个文件
4. **不要遗漏 import 路径** —— 改了包名必须同步改所有 import（这是最常见的 P0 遗漏）
5. **不要忘记测试** —— 改完后跑一遍冒烟验证确认没有改坏

---

## 📋 清洗报告模板

清洗完成后，向老板汇报：

```
品牌清洗完成，共替换以下内容：

P0 项（必须改）：
1. 项目名：OldName → NewName（共 XX 处）✅
2. 包名/模块名：old.name → new.name（共 XX 处）✅
3. import 路径：XX 个文件 ✅
4. URL：github.com/old/repo → github.com/new/repo（共 XX 处）✅
5. 版权声明：Old Author → New Author（共 XX 处）✅

P1 项（应该改）：
6. README.md 重写 ✅
7. 配置文件：已更新 XX 个文件 ✅
8. Logo/图标：已替换 / 未替换（老板未提供）
9. HTML 模板：已更新 XX 个文件 ✅

P2 项（建议改）：
10. CHANGELOG.md：已更新 ✅ / 保留原样 ⏭️
11. GitHub 模板：已更新 ✅ / 不需要 ⏭️

未替换（有意保留，符合开源协议归因要求）：
- LICENSE 中的原作者归因行（MIT 协议要求保留）
- README.md 末尾致谢原项目

冒烟验证：✅ 通过 / ❌ 未通过（原因：XXX）

请确认以上改动是否符合预期。
```