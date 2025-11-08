# GitHub Pages 部署故障排查指南

## 问题描述

GitHub Pages 上的博客显示不正常：
- ❌ 导航栏不显示
- ❌ 只有默认的 Hexo 博客
- ❌ 主题配置没有被应用

## 根本原因分析

### 已验证的事项 ✅

1. ✅ `_config.redefine.yml` 已被提交到 Git
2. ✅ 356 个文章文件已被提交到 Git
3. ✅ GitHub Actions 工作流配置正确
4. ✅ `package.json` 中正确声明了主题依赖

### 可能的问题 🔴

1. **GitHub Actions 工作流执行失败** - 构建过程中出错
2. **GitHub Pages 源分支配置错误** - 指向了错误的分支
3. **构建缓存问题** - GitHub Pages 缓存了旧版本
4. **权限问题** - GitHub Actions 没有写权限

---

## 快速诊断步骤

### 步骤 1：检查 GitHub Actions 执行日志

1. 打开仓库：https://github.com/moye12325/moye12325.github.io
2. 点击 **Actions** 标签
3. 查看最近的工作流运行
4. 检查是否有 ❌ 失败的构建

**常见错误**：
- `npm install` 失败 → 检查 package.json 依赖
- `hexo generate` 失败 → 检查文章 front matter
- 主题加载失败 → 检查 _config.redefine.yml

### 步骤 2：检查 GitHub Pages 设置

1. 打开仓库 **Settings** → **Pages**
2. 验证配置：
   - **Source**: `Deploy from a branch`
   - **Branch**: `gh-pages` 和 `/ (root)`

### 步骤 3：检查 gh-pages 分支

1. 切换到 `gh-pages` 分支
2. 验证存在 `index.html` 和其他文件
3. 检查最后修改时间（应该是最近的）

---

## 修复方案

### 方案 A：强制重新部署（推荐）

```bash
# 1. 清理本地构建
npm run clean

# 2. 重新生成
npm run build

# 3. 提交更改
git add .
git commit -m "fix: force rebuild and redeploy"

# 4. 推送到 main 分支
git push origin main
```

### 方案 B：手动触发工作流

1. 打开 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 "Deploy Hexo to GitHub Pages" 工作流
4. 点击 **Run workflow** 按钮
5. 选择 `main` 分支
6. 点击 **Run workflow**

### 方案 C：清除 GitHub Pages 缓存

1. 进入 **Settings** → **Pages**
2. 临时改变 **Source** 设置
3. 等待 1-2 分钟
4. 改回 `gh-pages` 分支
5. 等待 GitHub Pages 重新部署

---

## 工作流改进

已更新 `.github/workflows/deploy.yml`，包含：

✅ 手动触发选项 (`workflow_dispatch`)
✅ 权限配置 (`permissions`)
✅ npm 缓存优化
✅ 构建输出检查
✅ 调试信息

---

## 验证部署成功

部署完成后，检查以下项目：

- [ ] 导航栏显示正常（首页|博客|随笔|项目|关于|友链）
- [ ] 博客文章列表显示（不只是默认文章）
- [ ] 主题样式正确应用
- [ ] 所有导航链接可点击
- [ ] 移动端显示正常

---

## 常见问题解答

### Q: 为什么本地正常但 GitHub Pages 不正常？

**A**: 最常见的原因是：
1. 文件没有被提交到 Git
2. GitHub Actions 构建失败
3. GitHub Pages 缓存问题

### Q: 如何查看 GitHub Actions 的详细日志？

**A**: 
1. 打开 Actions 标签
2. 点击最近的工作流运行
3. 点击 "build-and-deploy" 任务
4. 展开各个步骤查看日志

### Q: 如何手动部署而不等待 GitHub Actions？

**A**: 使用 `npm run deploy` 命令（需要配置 SSH 密钥）

---

## 下一步

1. 按照上述诊断步骤检查问题
2. 选择合适的修复方案
3. 验证部署是否成功
4. 如果仍有问题，检查 GitHub Actions 日志中的具体错误信息

---

**最后更新**: 2025-11-08
**Hexo 版本**: 8.1.0
**主题**: Redefine v2.8.5

