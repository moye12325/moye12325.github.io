# 文章作者信息配置指南

## 问题描述

每篇文章的作者信息显示为 "The Redefine Team"，这是主题的默认值。你需要将其改为你自己的身份。

---

## 解决方案

### 方案 1：修改主题配置文件（推荐）

编辑 `_config.redefine.yml` 文件中的作者信息：

**文件位置**：`_config.redefine.yml`

**修改内容**（第 10-21 行）：

```yaml
# BASIC INFORMATION
info:
  # Site title
  title: 码农修行手册
  # Site subtitle
  subtitle: Python与量子计算之路上的心得与实践
  # Author name
  author: moye  # ← 改为你的名字
  # Site URL
  url: https://moye12325.github.io
```

**修改步骤**：

1. 打开 `_config.redefine.yml` 文件
2. 找到第 18 行的 `author: The Redefine Team`
3. 改为 `author: moye`（或你喜欢的名字）
4. 保存文件
5. 重启本地服务器：`npm run server`
6. 访问 http://localhost:4000 查看效果

---

### 方案 2：修改全局配置文件

编辑 `_config.yml` 文件中的作者信息：

**文件位置**：`_config.yml`

**修改内容**（第 10 行）：

```yaml
author: moye12325  # ← 改为你的名字
```

**说明**：
- 这是 Hexo 的全局配置
- 如果主题配置中没有指定作者，会使用这个全局作者
- 建议同时修改两个文件保持一致

---

### 方案 3：在文章 Front Matter 中指定作者

如果你想为不同的文章指定不同的作者，可以在每篇文章的 Front Matter 中指定：

**文件位置**：`source/_posts/your-article.md`

**修改内容**（文章开头）：

```yaml
---
title: 文章标题
date: 2024-11-08 10:00:00
author: moye  # ← 指定这篇文章的作者
categories:
  - 技术
tags:
  - Python
---

文章内容...
```

**说明**：
- 这会覆盖全局和主题配置中的作者
- 每篇文章可以有不同的作者
- 如果不指定，会使用全局配置中的作者

---

## 身份建议

根据你的信息，以下是几个身份选择：

### 选项 1：使用昵称（推荐）
```yaml
author: moye
```
- 简洁、易记
- 与 GitHub 用户名一致
- 适合技术博客

### 选项 2：使用全名
```yaml
author: moye12325
```
- 更正式
- 与 GitHub 用户名完全一致
- 适合专业博客

### 选项 3：使用中文名
```yaml
author: 码农修行者
```
- 更有个性
- 与博客主题相符
- 适合中文技术博客

### 选项 4：使用英文名
```yaml
author: Kane
```
- 国际化
- 简洁
- 适合国际受众

---

## 验证修改

修改后，你可以通过以下方式验证：

### 1. 本地预览
```bash
npm run server
```
访问 http://localhost:4000，查看文章页面的作者信息

### 2. 检查生成的 HTML
修改后运行：
```bash
npm run build
```
查看 `public/` 目录中生成的 HTML 文件，搜索作者名字

### 3. 检查 Front Matter
打开任意文章文件，查看是否有 `author` 字段

---

## 常见问题

### Q: 修改后作者信息仍未更新？

**A**: 尝试以下步骤：
1. 清理缓存：`npm run clean`
2. 重新生成：`npm run build`
3. 重启服务器：`npm run server`
4. 清除浏览器缓存（Ctrl+Shift+Delete）

### Q: 可以为不同的文章设置不同的作者吗？

**A**: 可以。在每篇文章的 Front Matter 中添加 `author` 字段即可。

### Q: 作者信息在哪里显示？

**A**: 通常显示在：
- 文章页面的顶部或底部
- 文章列表中
- 侧边栏的作者信息区域

具体位置取决于主题的设计。

### Q: 如何同时修改多篇文章的作者？

**A**: 
1. 使用全局配置（推荐）：修改 `_config.yml` 中的 `author` 字段
2. 使用脚本批量修改：编写 Node.js 脚本遍历所有文章文件
3. 使用编辑器的查找替换功能

---

## 相关配置文件

- **`_config.yml`** - Hexo 全局配置
- **`_config.redefine.yml`** - Redefine 主题配置
- **`source/_posts/*.md`** - 文章文件

---

## 下一步

1. 选择你喜欢的身份
2. 修改 `_config.redefine.yml` 中的 `author` 字段
3. 重启服务器验证效果
4. 如果满意，提交到 Git

---

**最后更新**: 2025-11-08
**Hexo 版本**: 8.1.0
**主题**: Redefine v2.8.5

