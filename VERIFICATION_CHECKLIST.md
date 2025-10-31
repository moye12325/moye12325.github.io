# 验证检查清单

在推送到 main 分支并触发部署后，请按此清单验证配置是否正常工作。

## 📋 部署前检查

### 1. 本地文件检查

- [x] `.github/workflows/deploy.yml` - GitHub Actions 工作流配置
- [x] `_config.yml` - 站点配置文件（包含 RSS 和 Sitemap 配置）
- [x] `_config.redefine.yml` - 主题配置文件（已同步站点信息）
- [x] `package.json` - 包含新增的 feed 和 sitemap 插件
- [x] `.gitignore` - 正确配置忽略文件
- [x] `README.md` - 完整的项目说明
- [x] `DEPLOYMENT.md` - 详细的部署文档
- [x] `TASK_SUMMARY.md` - 任务完成总结

### 2. 依赖包检查

确认以下包在 `package.json` 中：

- [x] `hexo-generator-feed` (^3.0.0) - RSS 生成
- [x] `hexo-generator-sitemap` (^3.0.1) - Sitemap 生成
- [x] `hexo-theme-redefine` (^2.8.5) - 主题
- [x] `hexo-deployer-git` (^4.0.0) - Git 部署工具

### 3. 配置文件验证

#### `_config.yml` 关键配置

- [x] `title: 码农修行手册`
- [x] `subtitle: Python与量子计算之路上的心得与实践`
- [x] `description: moye12325的个人技术博客...`
- [x] `keywords: Python, 全栈开发, 编程学习, 技术分享, moye12325`
- [x] `url: https://moye12325.github.io`
- [x] `permalink: :year/:month/:day/:title/`
- [x] `theme: redefine`
- [x] `feed` 配置块已添加
- [x] `sitemap` 配置块已添加

#### `_config.redefine.yml` 关键配置

- [x] `info.title: 码农修行手册`
- [x] `info.subtitle: Python与量子计算之路上的心得与实践`
- [x] `info.author: moye12325`
- [x] `info.url: https://moye12325.github.io`
- [x] `home_banner.title: 码农修行手册`
- [x] `home_banner.subtitle.text` 包含三条配置文本
- [x] `open_graph.description` 已更新
- [x] `plugins.feed.enable: true`

## 🚀 部署后验证

### 1. GitHub Actions 检查

访问：`https://github.com/moye12325/moye12325.github.io/actions`

- [ ] 工作流 "Deploy Hexo Blog to GitHub Pages" 已触发
- [ ] 所有步骤显示绿色✓
- [ ] "Deploy to GitHub Pages" 步骤成功完成
- [ ] 整个工作流在 2-3 分钟内完成

#### 预期的工作流步骤

1. [ ] Checkout repository
2. [ ] Setup Node.js
3. [ ] Install dependencies
4. [ ] Clean Hexo cache
5. [ ] Build Hexo site
6. [ ] Configure Git
7. [ ] Deploy to GitHub Pages

### 2. GitHub Pages 设置检查

访问：`https://github.com/moye12325/moye12325.github.io/settings/pages`

- [ ] Source 设置为：Deploy from a branch
- [ ] Branch 选择：`gh-pages` / `root`
- [ ] 显示：Your site is live at https://moye12325.github.io

### 3. 网站基础功能验证

#### 首页（https://moye12325.github.io）

- [ ] 网站可正常访问，无 404 错误
- [ ] 浏览器标签显示：**码农修行手册**
- [ ] 首页 banner 标题显示：**码农修行手册**
- [ ] 副标题循环显示：
  - [ ] "Python与量子计算之路上的心得与实践"
  - [ ] "分享编程技巧与技术解析"
  - [ ] "记录全栈开发的点滴收获"
- [ ] 页面底部显示作者：moye12325
- [ ] 主题样式正常加载（无样式错误）

#### 页面元数据

按 F12 打开开发者工具，检查 HTML `<head>` 部分：

- [ ] `<title>` 标签包含 "码农修行手册"
- [ ] `<meta name="description">` 包含正确的描述
- [ ] `<meta name="keywords">` 包含配置的关键词
- [ ] `<meta property="og:title">` 等 Open Graph 标签存在
- [ ] `<link rel="alternate" type="application/atom+xml">` RSS 自动发现标签存在

### 4. SEO 功能验证

#### RSS 订阅

访问：`https://moye12325.github.io/atom.xml`

- [ ] 返回 200 状态码（不是 404）
- [ ] 显示 XML 格式的 RSS feed
- [ ] 包含 `<feed>` 根元素
- [ ] 包含网站标题和描述
- [ ] 如果有文章，列出最新 20 篇文章

#### Sitemap

访问：`https://moye12325.github.io/sitemap.xml`

- [ ] 返回 200 状态码（不是 404）
- [ ] 显示 XML 格式的 sitemap
- [ ] 包含 `<urlset>` 根元素
- [ ] 列出网站的主要页面 URL
- [ ] 包含标签和分类页面（如果有）

### 5. 自动部署流程验证

#### 测试自动部署

1. 创建一篇测试文章：

```bash
hexo new post "测试自动部署"
```

2. 编辑 `source/_posts/测试自动部署.md`，添加内容

3. 提交并推送：

```bash
git add .
git commit -m "test: 测试自动部署功能"
git push origin main
```

4. 验证：

- [ ] GitHub Actions 自动触发新的工作流
- [ ] 工作流成功完成
- [ ] 等待 2-3 分钟后，网站上出现新文章
- [ ] RSS feed 包含新文章
- [ ] Sitemap 包含新文章 URL

## 🔍 深度验证（可选）

### 1. 响应式设计

- [ ] 在手机屏幕尺寸下正常显示
- [ ] 导航菜单在移动端可用
- [ ] 文章阅读体验良好

### 2. 主题功能

- [ ] 亮色/暗色主题切换正常工作
- [ ] 代码高亮正常显示
- [ ] 文章目录（TOC）正常生成
- [ ] 文章字数统计和阅读时间显示

### 3. 性能检查

使用 Google PageSpeed Insights 或 Lighthouse：

- [ ] 性能评分 > 80
- [ ] 可访问性评分 > 90
- [ ] 最佳实践评分 > 80
- [ ] SEO 评分 > 90

### 4. 社交媒体分享测试

使用工具检查 Open Graph 标签：
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
- Twitter Card Validator: https://cards-dev.twitter.com/validator

- [ ] 分享时显示正确的标题
- [ ] 分享时显示正确的描述
- [ ] 分享时显示正确的图片

## ⚠️ 常见问题排查

### 问题：GitHub Actions 失败

检查：
1. 查看 Actions 日志，找到失败的步骤
2. 确认 `package.json` 语法正确
3. 确认 `_config.yml` 和 `_config.redefine.yml` 语法正确
4. 确认 main 分支有推送权限

### 问题：网站显示 404

检查：
1. GitHub Pages 设置是否正确（gh-pages 分支）
2. 等待 2-3 分钟让 GitHub Pages 更新
3. 确认 Actions 工作流成功完成
4. 检查 gh-pages 分支是否有内容

### 问题：网站标题未更新

检查：
1. 强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）
2. 确认 `_config.redefine.yml` 中的 `info` 部分已更新
3. 清除浏览器缓存
4. 等待更长时间（可能有 CDN 缓存）

### 问题：RSS/Sitemap 返回 404

检查：
1. 确认插件已安装：`npm install`
2. 确认 `_config.yml` 配置正确
3. 本地测试：`hexo clean && hexo generate`
4. 检查 `public/` 目录是否生成了 `atom.xml` 和 `sitemap.xml`
5. 重新触发部署

### 问题：样式显示异常

检查：
1. 浏览器开发者工具查看 CSS 加载错误
2. 确认 `_config.yml` 中的 `url` 设置正确
3. 确认主题文件完整
4. 尝试更换浏览器测试

## 📊 验证完成度追踪

完成上述所有检查项后，您的博客配置应该是完全正常的。

- **必须完成**：部署前检查 + 部署后验证（第 1-5 部分）
- **推荐完成**：深度验证（第 6 部分）
- **遇到问题**：参考常见问题排查部分

---

## ✅ 验证签名

完成所有验证后，在此处签名：

- 验证人：_______________
- 验证日期：_______________
- 验证结果：[ ] 全部通过 [ ] 部分通过 [ ] 需要修复

---

**祝您使用愉快！开始创作精彩内容吧！** 🎉
