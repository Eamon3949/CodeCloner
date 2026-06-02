# 抄袭者 (CodeCloner)

> 把别人的开源项目"抄"过来，洗一遍变成你自己的。
> 所有大白话，不懂代码也能用。

## 这是什么？

CodeCloner 是一个 Claude Code Skill（技能文件）。当你在和 AI 对话时，给它一个 GitHub 开源项目链接并输入 `[激活抄袭者]`，AI 就会自动把那个项目"抄"过来，帮你改头换面变成你自己的项目。

## 三步搞定

1. 给 AI 一个 GitHub 链接，输入 `[激活抄袭者]`
2. AI 告诉你项目能不能抄、大概要改多少
3. 告诉 AI 你想叫什么名字、要去掉/加上什么功能
4. AI 帮你改好所有代码，验证能跑，推送到你的 GitHub

## 你需要什么？

- 一个 GitHub 账号（用来存放代码）
- 安装了 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（AI 助手）
- 不需要懂代码

## 怎么用？

```
你：https://github.com/某人/某个项目 [激活抄袭者]
AI：好的，我来分析这个项目......（一段大白话汇报）
你：项目叫 SlideMaster，去掉社区功能，加上我的 Logo
AI：收到，正在改造......（改好所有代码）
AI：已完成！已推送到 https://github.com/你的用户名/SlideMaster
```

## 项目结构

```
SKILL.md          <- 技能入口文件（规则定义）
VERSION           <- 版本号
references/
  workflow.md     <- 详细工作流（第1-4步怎么走）
  branding-checklist.md  <- 品牌清洗清单（改名字的时候照着抄）
```

## 注意

- 本 Skill 及其产生的内容仅供学习和研究使用
- 原项目的开源协议仍然适用，请遵守原作者的许可条款
- 商业使用请确保获得原项目作者授权