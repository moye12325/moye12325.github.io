# 码农修行手册 - Hexo Blog

> Python与量子计算之路上的心得与实践

[![Hexo](https://img.shields.io/badge/Hexo-8.1.0-blue)](https://hexo.io/)
[![Theme](https://img.shields.io/badge/Theme-Redefine%20v2.8.5-brightgreen)](https://github.com/EvanNotFound/hexo-theme-redefine)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green)](https://nodejs.org/)
[![Deploy](https://img.shields.io/badge/Deploy-GitHub%20Pages-orange)](https://moye12325.github.io)

## 📖 简介

这是 moye12325 的个人技术博客，专注于 Python、全栈开发实战经验、编程技巧分享与深入的技术解析。

**博客地址**：[https://moye12325.github.io](https://moye12325.github.io)

## 📚 内容分类

- **Java**: Java 基础、集合、并发、JVM 等
- **数据结构与算法**: 各种数据结构实现与算法解析
- **深度学习**: 李沐、李宏毅深度学习课程笔记
- **人工智能**: AI 相关技术研究与实践
- **软件测试**: 软件测试理论与实践
- **项目测试**: 实际项目测试经验分享
- **项目部署**: 项目部署相关技术
- **LeetCode**: LeetCode 刷题记录与解析
- **笔试记录**: 各公司笔试题目与解答
- **随笔**: 个人思考与生活记录

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Git

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
# 启动本地服务器（默认端口 4000）
npm run server

# 或指定端口
npx hexo server -p 4001
```

### 构建网站

```bash
# 清理生成文件
npm run clean

# 生成静态文件
npm run build
```

### 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

```bash
git add .
git commit -m "your commit message"
git push origin main
```

## 📝 文章管理

### 创建新文章

```bash
# 创建博客文章
npx hexo new "文章标题"

# 创建随笔
npx hexo new "文章标题" --path notes/文章标题
```

### Front Matter 格式

```yaml
---
title: 文章标题
date: 2024-11-03 10:00:00
updated: 2024-11-03 12:00:00
categories:
  - 分类名
tags:
  - 标签1
  - 标签2
summary: 文章摘要
---
```

## 🎨 主题配置

本博客使用 [Redefine](https://github.com/EvanNotFound/hexo-theme-redefine) 主题。

主要配置文件：
- `_config.yml` - Hexo 主配置
- `_config.redefine.yml` - Redefine 主题配置

## 📂 项目结构

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions 部署配置
├── scripts/
│   └── migrate-drafts.js     # 文章迁移脚本
├── source/
│   ├── _posts/              # 博客文章
│   │   └── notes/           # 随笔文章
│   ├── about/               # 关于页面
│   ├── projects/            # 项目页面
│   ├── links/               # 友链页面
│   ├── categories/          # 分类页面
│   ├── tags/                # 标签页面
│   └── archives/            # 归档页面
├── themes/                  # 主题目录
├── _config.yml             # Hexo 配置
├── _config.redefine.yml    # 主题配置
└── package.json            # 依赖和脚本
```

## 🔧 可用脚本

```bash
# 清理生成文件
npm run clean

# 生成静态文件
npm run build

# 启动本地服务器
npm run server

# 部署到 GitHub Pages
npm run deploy

# 迁移草稿文章（已执行）
npm run migrate
```

## 🌐 导航结构

- **首页** `/` - 博客首页
- **博客** - 下拉菜单
  - 全部文章 `/archives/`
  - 分类 `/categories/`
  - 标签 `/tags/`
  - 归档 `/archives/`
- **随笔** `/categories/随笔/` - 个人随笔
- **项目** `/projects/` - 项目展示
- **关于** `/about/` - 关于作者
- **友链** `/links/` - 友情链接

## 📊 统计信息

- 博客文章: 163+ 篇
- 随笔文章: 15+ 篇
- 总计: 178+ 篇

## 🔄 自动部署

本项目已配置 GitHub Actions 自动部署：

1. 推送到 `main` 分支
2. 自动触发 GitHub Actions
3. 构建 Hexo 静态网站
4. 部署到 `gh-pages` 分支
5. GitHub Pages 自动发布

查看部署状态: [Actions](../../actions)

## 📜 许可证

本博客内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。

## 🤝 友链交换

欢迎交换友链！请在 [友链页面](https://moye12325.github.io/links/) 留言。

### 本站信息

```
站点名称：码农修行手册
站点链接：https://moye12325.github.io
站点描述：Python与量子计算之路上的心得与实践
```

## 📧 联系方式

- GitHub: [@moye12325](https://github.com/moye12325)
- 博客: [moye12325.github.io](https://moye12325.github.io)

## 🙏 致谢

- [Hexo](https://hexo.io/) - 快速、简洁且高效的博客框架
- [Redefine](https://github.com/EvanNotFound/hexo-theme-redefine) - 简洁优雅的 Hexo 主题
- [GitHub Pages](https://pages.github.com/) - 免费的静态网站托管服务

---

**最后更新**: 2024-11-03  
**Hexo 版本**: 8.1.0  
**主题版本**: Redefine v2.8.5
