# 码农修行手册 | moye12325.github.io

基于 Hexo + GitHub Pages 搭建的个人技术博客，专注于 Python、全栈开发、编程技巧分享与技术解析。

## 📚 分支说明

- **`main`** - Hexo 源码、配置文件及自动部署配置
- **`gh-pages`** - 构建后的静态网站，用于 GitHub Pages 托管
- **`master`** - 已废弃，仅作为占位分支

⚠️ **重要提示**：开发请在 `main` 分支进行，不要直接修改 `gh-pages` 分支！

## 🚀 快速开始

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/moye12325/moye12325.github.io.git
cd moye12325.github.io

# 切换到 main 分支
git checkout main

# 安装依赖
npm install

# 启动本地服务器
npm run server

# 访问 http://localhost:4000
```

### 写作流程

```bash
# 创建新文章
hexo new post "文章标题"

# 编辑文章
# 文件位于: source/_posts/文章标题.md

# 本地预览
npm run server

# 提交到 GitHub
git add .
git commit -m "feat: 添加新文章"
git push origin main
```

## 🤖 自动化部署

本项目已配置 GitHub Actions 自动化部署：

- ✅ 推送到 `main` 分支自动触发构建
- ✅ 自动生成静态文件
- ✅ 自动部署到 `gh-pages` 分支
- ✅ 无需手动执行 `hexo deploy`

工作流配置文件：`.github/workflows/deploy.yml`

## 📝 可用命令

```bash
npm run build    # 生成静态文件
npm run clean    # 清理缓存和生成的文件
npm run deploy   # 部署到 GitHub Pages（不推荐，使用 Git push 触发自动部署）
npm run server   # 启动本地预览服务器
```

## 🎨 主题配置

本博客使用 [Hexo Theme Redefine](https://github.com/EvanNotFound/hexo-theme-redefine) 主题。

- 主题配置文件：`_config.redefine.yml`
- 站点配置文件：`_config.yml`

### 主要特性

- 🎯 响应式设计，完美支持移动端
- 🌓 支持亮色/暗色主题切换
- 📊 文章字数统计和阅读时间
- 🔍 本地搜索功能
- 📱 社交媒体链接
- 💬 评论系统支持（Waline/Gitalk/Twikoo/Giscus）

## 🔧 配置说明

### SEO 优化

已配置以下 SEO 优化：

- ✅ 站点标题、描述、关键词
- ✅ Open Graph 元标签
- ✅ RSS 订阅 (`/atom.xml`)
- ✅ Sitemap 站点地图 (`/sitemap.xml`)
- ✅ 语义化的永久链接格式

### RSS 订阅

订阅地址：`https://moye12325.github.io/atom.xml`

### Sitemap

站点地图：`https://moye12325.github.io/sitemap.xml`

## 📦 依赖插件

- `hexo-generator-feed` - RSS 订阅生成
- `hexo-generator-sitemap` - 站点地图生成
- `hexo-deployer-git` - Git 部署工具
- `hexo-renderer-marked` - Markdown 渲染
- `hexo-theme-redefine` - 主题

## 🛠️ 技术栈

- **框架**: [Hexo](https://hexo.io/)
- **主题**: [Redefine](https://redefine-docs.ohevan.com/)
- **托管**: GitHub Pages
- **CI/CD**: GitHub Actions
- **语言**: Node.js

## 📄 许可证

本项目内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。

## 📧 联系方式

- 博客：https://moye12325.github.io
- GitHub：[@moye12325](https://github.com/moye12325)

---

**持续学习，不断精进** 💪
