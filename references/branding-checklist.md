# 品牌清洗检查清单

> 当你"抄"一个项目过来时，必须把原作者的所有品牌痕迹替换掉。
> 下面这份清单帮你逐项检查，确保没有遗漏。

---

## ✅ 清洗步骤

每完成一步，打一个 ✅。全部打完才算清洗完成。

### 1. 项目名 / 仓库名

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

### 2. 包名 / 模块名 / import 路径

- [ ] Python: `import 原项目名` → `import 新项目名`
- [ ] JavaScript/TypeScript: `from '原项目名'` / `require('原项目名')` → 新项目名
- [ ] Go: `module github.com/原作者/原项目` → 新路径
- [ ] Rust: `[原项目名]` crate 名 → 新 crate 名
- [ ] Java: `com.原作者.原项目` 包路径 → 新包路径

### 3. README.md

- [ ] 标题（`# 原项目名`）
- [ ] 描述段落
- [ ] 安装命令中的项目名
- [ ].Badge/图标中的链接
- [ ] 截图/示例代码中的项目名
- [ ] 贡献指南链接
- [ ] 许可证链接

### 4. LICENSE

- [ ] 版权行中的作者名（`Copyright (c) YEAR 原作者` → `Copyright (c) YEAR 新作者`）
- [ ] 版权行中的项目名（如有）
- [ ] 保留原始开源协议类型（MIT/Apache/GPL），只改作者名

### 5. 配置文件

- [ ] `.env.example` 中的项目相关变量
- [ ] `config/` 目录下的项目名和 URL
- [ ] `docker-compose.yml` 中的容器名、镜像名
- [ ] `Dockerfile` 中的项目名引用
- [ ] CI/CD 配置（`.github/workflows/`）中的仓库名
- [ ] `Makefile` 中的项目名

### 6. HTML / 前端模板

- [ ] `<title>` 标签中的项目名
- [ ] `<meta name="description">` 中的描述
- [ ] `<link rel="icon">` favicon 引用
- [ ] `<meta property="og:*">` 社交分享标签
- [ ] 页面中的 Logo 图片引用
- [ ] 页面头部的导航品牌名

### 7. Logo / 图标文件

- [ ] `logo.png` / `logo.svg` / `favicon.ico` 等
- [ ] 通常需要老板提供新图片直接替换文件
- [ ] 如果没有新图片，保留原有图片但确认是否可以继续使用

### 8. 隐藏文件和特殊位置

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

### 10. 最终全局搜索确认

- [ ] 全局搜索原项目名（大小写不敏感）—— 应该只剩注释里的归因说明
- [ ] 全局搜索原作者名 —— 应该只剩 LICENSE 中的归因行
- [ ] 全局搜索原项目 URL —— 应该只剩 README 中的致谢/归因链接
- [ ] `git diff --stat` 确认改动范围合理

---

## 🚫 不要做的事

1. **不要删除原作者的 LICENSE** —— 只改版权行的作者名，保留协议类型
2. **不要手动改锁定文件** —— 运行对应的包管理器重新生成
3. **不要改二进制文件里的文字** —— 直接替换整个文件
4. **不要遗漏 import 路径** —— 改了包名必须同步改所有 import
5. **不要忘记测试** —— 改完后跑一遍项目测试确认没有改坏

---

## 📋 清洗报告模板

清洗完成后，向老板汇报：

```
品牌清洗完成，共替换以下内容：

1. 项目名：OldName → NewName（共 XX 处）
2. 包名/模块名：old.name → new.name（共 XX 处）
3. URL：github.com/old/repo → github.com/new/repo（共 XX 处）
4. 版权声明：Old Author → New Author（共 XX 处）
5. Logo/图标：已替换 / 未替换（老板未提供）
6. 配置文件：已更新 XX 个文件

未替换（有意保留）：
- README.md 末尾致谢原项目
- LICENSE 中的原作者归因（开源协议要求）

请确认以上改动是否符合预期。
```