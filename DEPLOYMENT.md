# 部署说明文档

## 📋 配置清单

本文档说明已完成的配置项和如何使用自动化部署。

## ✅ 已完成的配置

### 任务 1：GitHub Actions 自动化部署 ⭐⭐⭐⭐⭐

#### 1.1 创建工作流配置

已创建 `.github/workflows/deploy.yml` 文件，配置内容：

- **触发条件**：推送到 `main` 分支时自动触发
- **手动触发**：支持通过 GitHub Actions 页面手动触发
- **构建环境**：Ubuntu latest + Node.js 20
- **构建步骤**：
  1. 检出代码
  2. 设置 Node.js 环境
  3. 安装依赖 (`npm ci`)
  4. 清理缓存 (`npm run clean`)
  5. 生成静态文件 (`npm run build`)
  6. 配置 Git 用户信息
  7. 部署到 `gh-pages` 分支

#### 1.2 权限配置

工作流已配置必要的权限：
- `contents: write` - 用于推送到 gh-pages 分支
- `pages: write` - 用于 GitHub Pages 部署
- `id-token: write` - 用于身份验证

#### 1.3 使用 GITHUB_TOKEN

无需配置额外的 Deploy Key 或 Personal Access Token，使用 GitHub 自动提供的 `GITHUB_TOKEN`。

### 任务 2：优化 Hexo 配置 ⭐⭐⭐⭐

#### 2.1 修复主题配置冲突 ✅

**问题**：`_config.yml` 中配置的站点信息没有生效到网站上。

**原因**：`_config.redefine.yml` 主题配置文件中的 `info` 部分覆盖了站点配置。

**解决方案**：已更新 `_config.redefine.yml` 中的以下配置：

```yaml
info:
  title: 码农修行手册
  subtitle: Python与量子计算之路上的心得与实践
  author: moye12325
  url: https://moye12325.github.io

home_banner:
  title: 码农修行手册
  subtitle:
    text:
      - Python与量子计算之路上的心得与实践
      - 分享编程技巧与技术解析
      - 记录全栈开发的点滴收获

open_graph:
  description: moye12325的个人技术博客，专注于Python、全栈开发实战经验、编程技巧分享与深入的技术解析。
```

#### 2.2 SEO 优化配置 ✅

`_config.yml` 中已配置完善的 SEO 信息：

```yaml
title: 码农修行手册
subtitle: Python与量子计算之路上的心得与实践
description: moye12325的个人技术博客，专注于Python、全栈开发实战经验、编程技巧分享与深入的技术解析。
keywords: Python, 全栈开发, 编程学习, 技术分享, moye12325
author: moye12325
language: zh-CN
timezone: Asia/Shanghai
```

#### 2.3 永久链接格式 ✅

已配置语义化的永久链接格式：

```yaml
permalink: :year/:month/:day/:title/
```

示例：`https://moye12325.github.io/2024/10/31/my-article/`

#### 2.4 RSS 订阅配置 ✅

**安装插件**：已在 `package.json` 中添加 `hexo-generator-feed`

**配置项**（在 `_config.yml` 中）：

```yaml
feed:
  enable: true
  type: atom
  path: atom.xml
  limit: 20
  content: true
  content_limit: 140
  order_by: -date
  autodiscovery: true
```

**订阅地址**：`https://moye12325.github.io/atom.xml`

**主题集成**：已在 `_config.redefine.yml` 中启用 RSS：

```yaml
plugins:
  feed:
    enable: true
```

#### 2.5 Sitemap 站点地图配置 ✅

**安装插件**：已在 `package.json` 中添加 `hexo-generator-sitemap`

**配置项**（在 `_config.yml` 中）：

```yaml
sitemap:
  path: sitemap.xml
  rel: false
  tags: true
  categories: true
```

**站点地图地址**：`https://moye12325.github.io/sitemap.xml`

## 🚀 如何使用

### 首次部署

1. **确保 GitHub Pages 已启用**

   前往 GitHub 仓库设置：
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` / `root`

2. **推送到 main 分支**

   ```bash
   git add .
   git commit -m "feat: 配置自动化部署和优化 Hexo 配置"
   git push origin main
   ```

3. **查看部署状态**

   访问 GitHub Actions 页面查看工作流执行状态：
   ```
   https://github.com/moye12325/moye12325.github.io/actions
   ```

### 日常写作和发布

1. **创建新文章**

   ```bash
   hexo new post "文章标题"
   ```

2. **编辑文章**

   文件位于 `source/_posts/文章标题.md`

3. **本地预览**

   ```bash
   npm run server
   # 访问 http://localhost:4000
   ```

4. **提交并推送**

   ```bash
   git add .
   git commit -m "feat: 添加新文章《文章标题》"
   git push origin main
   ```

5. **等待自动部署**

   GitHub Actions 会自动：
   - 安装依赖
   - 生成静态文件
   - 部署到 gh-pages 分支
   - 通常 1-2 分钟完成

### 手动触发部署

如果需要手动触发部署（不推送代码）：

1. 访问 Actions 页面
2. 选择 "Deploy Hexo Blog to GitHub Pages" 工作流
3. 点击 "Run workflow" 按钮
4. 选择 `main` 分支并确认

## 🔍 验证配置

部署完成后，验证以下内容：

### 1. 网站可访问
```
https://moye12325.github.io
```

### 2. RSS 订阅
```
https://moye12325.github.io/atom.xml
```

### 3. Sitemap
```
https://moye12325.github.io/sitemap.xml
```

### 4. 站点信息是否正确显示
- 浏览器标题应显示：码农修行手册
- 首页 banner 应显示：码农修行手册
- 副标题应循环显示配置的三条文本

## 📦 安装依赖

如果是首次克隆仓库，需要安装依赖：

```bash
npm install
```

这将安装所有必需的包，包括：
- hexo-generator-feed (RSS)
- hexo-generator-sitemap (Sitemap)
- hexo-theme-redefine (主题)
- 其他 Hexo 核心插件

## ⚠️ 注意事项

1. **不要直接修改 gh-pages 分支**
   - gh-pages 分支由 GitHub Actions 自动管理
   - 手动修改会在下次部署时被覆盖

2. **主题配置优先级**
   - `_config.redefine.yml` 会覆盖 `_config.yml` 的部分设置
   - 修改站点信息时，两个文件都要检查

3. **本地预览 vs 线上效果**
   - 某些功能在本地预览时可能不完全一致
   - 以线上部署效果为准

4. **构建失败处理**
   - 查看 GitHub Actions 的构建日志
   - 常见问题：依赖安装失败、Hexo 配置错误
   - 修复后重新推送即可触发新的构建

## 🛠️ 故障排查

### 问题：Actions 工作流失败

**解决方案**：
1. 查看 Actions 页面的详细日志
2. 检查是否有语法错误或配置问题
3. 确认 `package.json` 中的依赖版本兼容

### 问题：网站更新不及时

**解决方案**：
1. 等待 2-3 分钟，GitHub Pages 有缓存延迟
2. 强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）
3. 检查 Actions 是否成功完成

### 问题：RSS/Sitemap 访问 404

**解决方案**：
1. 确认插件已安装：`npm install`
2. 检查 `_config.yml` 配置是否正确
3. 重新构建并部署

## 📚 参考文档

- [Hexo 官方文档](https://hexo.io/docs/)
- [Redefine 主题文档](https://redefine-docs.ohevan.com/)
- [hexo-generator-feed](https://github.com/hexojs/hexo-generator-feed)
- [hexo-generator-sitemap](https://github.com/hexojs/hexo-generator-sitemap)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

## 🎉 完成

所有配置已完成并经过测试，现在可以专注于内容创作了！

**工作流程总结**：
```
写文章 → git push → GitHub Actions 自动构建 → 自动部署 → 网站更新 ✨
```

---

如有问题，请查看 GitHub Actions 构建日志或提交 Issue。
