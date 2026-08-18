---
description: "Git 常用命令速查手册：覆盖分支管理、拉取与推送、合并与变基、提交管理、状态查看、撤销操作、标签管理与远程仓库等常用操作。"
title: Git常用命令速查手册
date: 2025-12-04 20:20:00
categories: [开发工具]
tags: ['Git', '版本控制', '开发工具', '命令行']
---

> 以 `feature/0.26` 和 `develop` 分支为例

## 📋 目录

- [分支管理](#%E5%88%86%E6%94%AF%E7%AE%A1%E7%90%86)
- [拉取与推送](#%E6%8B%89%E5%8F%96%E4%B8%8E%E6%8E%A8%E9%80%81)
- [合并与变基](#%E5%90%88%E5%B9%B6%E4%B8%8E%E5%8F%98%E5%9F%BA)
- [提交管理](#%E6%8F%90%E4%BA%A4%E7%AE%A1%E7%90%86)
- [状态查看](#%E7%8A%B6%E6%80%81%E6%9F%A5%E7%9C%8B)
- [撤销操作](#%E6%92%A4%E9%94%80%E6%93%8D%E4%BD%9C)
- [标签管理](#%E6%A0%87%E7%AD%BE%E7%AE%A1%E7%90%86)
- [远程仓库](#%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93)

---

## 分支管理

### 查看分支

```bash
# 查看本地分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 查看远程分支
git branch -r
```

### 创建分支

```bash
# 从当前分支创建新分支
git branch feature/0.26

# 创建并切换到新分支
git checkout -b feature/0.26

# 从 develop 分支创建新分支
git checkout -b feature/0.26 develop

# 从远程分支创建本地分支
git checkout -b feature/0.26 origin/feature/0.26
```

### 切换分支

```bash
# 切换到 develop 分支
git checkout develop

# 切换到 feature/0.26 分支
git checkout feature/0.26

# 新版本 Git 使用 switch（推荐）
git switch develop
git switch feature/0.26
```

### 删除分支

```bash
# 删除本地分支（已合并）
git branch -d feature/0.26

# 强制删除本地分支（未合并）
git branch -D feature/0.26

# 删除远程分支
git push origin --delete feature/0.26
```

---

## 拉取与推送

### 拉取代码

```bash
# 拉取远程 develop 分支最新代码
git pull origin develop

# 拉取远程 feature/0.26 分支
git pull origin feature/0.26

# 拉取所有远程分支信息（不合并）
git fetch origin

# 拉取特定远程分支
git fetch origin feature/0.26
```

### 推送代码

```bash
# 推送 feature/0.26 到远程
git push origin feature/0.26

# 首次推送并设置上游分支
git push -u origin feature/0.26

# 推送 develop 分支
git push origin develop

# 强制推送（谨慎使用）
git push -f origin feature/0.26
```

---

## 合并与变基

### 合并分支

```bash
# 将 feature/0.26 合并到 develop
git checkout develop
git merge feature/0.26

# 不使用快进合并（保留合并记录）
git merge --no-ff feature/0.26

# 合并时添加提交信息
git merge feature/0.26 -m "Merge feature/0.26 into develop"
```

### 变基操作

```bash
# 将 feature/0.26 变基到 develop
git checkout feature/0.26
git rebase develop

# 交互式变基（整理提交历史）
git rebase -i develop

# 继续变基
git rebase --continue

# 中止变基
git rebase --abort
```

### 解决冲突

```bash
# 查看冲突文件
git status

# 编辑冲突文件后，标记为已解决
git add <冲突文件>

# 完成合并
git commit

# 完成变基
git rebase --continue
```

---

## 提交管理

### 提交代码

```bash
# 添加所有更改
git add .

# 添加特定文件
git add src/index.js

# 提交更改
git commit -m "feat: 完成 feature/0.26 功能开发"

# 添加并提交（跳过 add）
git commit -am "fix: 修复 develop 分支的 bug"

# 修改最后一次提交
git commit --amend
```

### 查看提交历史

```bash
# 查看提交日志
git log

# 简洁查看日志
git log --oneline

# 查看图形化分支历史
git log --graph --oneline --all

# 查看 feature/0.26 和 develop 的差异
git log develop..feature/0.26

# 查看某个文件的提交历史
git log -- src/index.js
```

### Cherry-pick

```bash
# 将特定提交应用到当前分支
git cherry-pick <commit-hash>

# 从 feature/0.26 挑选提交到 develop
git checkout develop
git cherry-pick abc123
```

---

## 状态查看

### 查看状态

```bash
# 查看工作区状态
git status

# 简洁模式
git status -s

# 查看差异
git diff

# 查看已暂存的差异
git diff --staged

# 查看两个分支的差异
git diff develop feature/0.26
```

### 查看远程信息

```bash
# 查看远程仓库信息
git remote -v

# 查看远程分支详情
git remote show origin

# 查看 feature/0.26 的追踪关系
git branch -vv
```

---

## 撤销操作

### 撤销工作区更改

```bash
# 撤销单个文件的更改
git checkout -- src/index.js

# 撤销所有工作区更改
git checkout -- .

# 新版 Git 使用 restore（推荐）
git restore src/index.js
git restore .
```

### 撤销暂存区

```bash
# 取消暂存特定文件
git reset HEAD src/index.js

# 取消所有暂存
git reset HEAD

# 新版 Git 使用 restore（推荐）
git restore --staged src/index.js
```

### 撤销提交

```bash
# 撤销最后一次提交（保留更改）
git reset --soft HEAD~1

# 撤销最后一次提交（不保留更改）
git reset --hard HEAD~1

# 撤销到特定提交
git reset --hard abc123

# 创建新提交来撤销（推荐用于已推送的提交）
git revert HEAD
```

---

## 标签管理

### 创建标签

```bash
# 在当前提交创建轻量标签
git tag v0.26

# 创建附注标签
git tag -a v0.26 -m "Release version 0.26"

# 在特定提交创建标签
git tag -a v0.26 abc123 -m "Release version 0.26"
```

### 查看和推送标签

```bash
# 查看所有标签
git tag

# 查看标签详情
git show v0.26

# 推送标签到远程
git push origin v0.26

# 推送所有标签
git push origin --tags

# 删除本地标签
git tag -d v0.26

# 删除远程标签
git push origin --delete v0.26
```

---

## 远程仓库

### 同步远程分支

```bash
# 更新远程分支列表
git fetch origin

# 更新所有远程仓库
git fetch --all

# 查看远程分支
git branch -r

# 清理已删除的远程分支引用
git fetch --prune
```

### 跟踪远程分支

```bash
# 设置 feature/0.26 跟踪远程分支
git branch --set-upstream-to=origin/feature/0.26 feature/0.26

# 简写
git branch -u origin/feature/0.26

# 推送并设置跟踪
git push -u origin feature/0.26
```

---

## 💡 常用工作流示例

### 场景1：开始新功能开发

```bash
# 1. 切换到 develop 分支
git checkout develop

# 2. 拉取最新代码
git pull origin develop

# 3. 创建功能分支
git checkout -b feature/0.26

# 4. 开发并提交
git add .
git commit -m "feat: 实现 0.26 新功能"

# 5. 推送到远程
git push -u origin feature/0.26
```

### 场景2：合并功能到 develop

```bash
# 1. 确保 feature/0.26 是最新的
git checkout feature/0.26
git pull origin feature/0.26

# 2. 切换到 develop 并更新
git checkout develop
git pull origin develop

# 3. 合并 feature/0.26
git merge --no-ff feature/0.26

# 4. 推送到远程
git push origin develop

# 5. 删除功能分支（可选）
git branch -d feature/0.26
git push origin --delete feature/0.26
```

### 场景3：同步 develop 的更新到 feature 分支

```bash
# 1. 切换到 feature/0.26
git checkout feature/0.26

# 2. 拉取 develop 最新代码
git fetch origin develop

# 3. 变基到 develop（推荐）
git rebase origin/develop

# 或者使用合并
git merge origin/develop

# 4. 推送更新（如果使用了 rebase，需要强制推送）
git push -f origin feature/0.26
```

### 场景4：紧急修复

```bash
# 1. 从 develop 创建热修复分支
git checkout develop
git checkout -b hotfix/urgent-fix

# 2. 修复并提交
git add .
git commit -m "fix: 紧急修复关键问题"

# 3. 合并到 develop
git checkout develop
git merge hotfix/urgent-fix
git push origin develop

# 4. 同时合并到 feature/0.26
git checkout feature/0.26
git merge hotfix/urgent-fix
git push origin feature/0.26
```

---

## ⚠️ 注意事项

1. **强制推送要谨慎**：使用 `git push -f` 前确保不会影响其他人
2. **合并前先更新**：合并分支前确保两个分支都是最新的
3. **提交信息要规范**：使用清晰的提交信息，建议遵循约定式提交
4. **定期同步 develop**：在功能分支开发时定期同步 develop 的更新
5. **避免直接在 develop 开发**：始终通过功能分支进行开发

---

## 📚 Git 提交信息规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建或辅助工具的变动
```

**示例**：

```bash
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复 feature/0.26 的空指针异常"
git commit -m "docs: 更新 develop 分支的 README"
```

