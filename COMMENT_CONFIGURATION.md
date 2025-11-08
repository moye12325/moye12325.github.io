# 评论功能配置指南

## 问题描述

博客的评论功能暂不可用。本指南将教你如何配置评论系统。

---

## 支持的评论系统

Redefine 主题支持多种评论系统。以下是最常用的几种：

### 1. Disqus（国际化，需要科学上网）
### 2. Valine（基于 LeanCloud，支持中文）
### 3. Waline（Valine 的升级版，推荐）
### 4. Gitalk（基于 GitHub Issues）
### 5. Utterances（基于 GitHub Discussions）

---

## 推荐方案：使用 Waline

Waline 是一个简洁、高效的评论系统，特别适合中文博客。

### 第一步：部署 Waline 服务

#### 方式 1：使用 Vercel 部署（推荐）

1. **创建 GitHub 仓库**
   - Fork 或 Clone：https://github.com/walinejs/waline
   - 或直接使用模板：https://vercel.com/new?template=walinejs/waline

2. **部署到 Vercel**
   - 访问 https://vercel.com
   - 使用 GitHub 账号登录
   - 点击 "New Project"
   - 选择 Waline 仓库
   - 点击 "Deploy"

3. **配置环境变量**
   - 在 Vercel 项目设置中添加：
     ```
     MONGODB_URI=<你的 MongoDB 连接字符串>
     JWT_TOKEN=<随机生成的密钥>
     ```

4. **获取部署 URL**
   - 部署完成后，Vercel 会提供一个 URL，例如：
     ```
     https://your-waline.vercel.app
     ```

#### 方式 2：使用 MongoDB Atlas（数据库）

1. **创建 MongoDB 账户**
   - 访问 https://www.mongodb.com/cloud/atlas
   - 注册免费账户
   - 创建一个集群

2. **获取连接字符串**
   - 在 MongoDB Atlas 中获取连接字符串
   - 格式：`mongodb+srv://username:password@cluster.mongodb.net/database`

---

### 第二步：配置 Hexo 主题

编辑 `_config.redefine.yml` 文件，找到评论配置部分：

**文件位置**：`_config.redefine.yml`

**查找评论配置**（搜索 "comment"）：

```yaml
# COMMENT SYSTEM
comment:
  # Comment system
  # Options: disqus, valine, waline, gitalk, utterances
  system: waline
  
  # Waline configuration
  waline:
    # Waline server URL
    serverURL: https://your-waline.vercel.app
    # Waline API path (usually /api)
    path: /api
    # Enable emoji
    emoji: true
    # Enable dark mode
    dark: auto
    # Required fields
    requiredMeta: ['name', 'email']
    # Placeholder
    placeholder: 请输入评论...
```

**修改步骤**：

1. 打开 `_config.redefine.yml`
2. 找到 `comment:` 部分
3. 将 `system:` 改为 `waline`
4. 将 `serverURL:` 改为你的 Waline 服务 URL
5. 保存文件
6. 重启服务器：`npm run server`

---

## 其他评论系统配置

### Gitalk 配置

```yaml
comment:
  system: gitalk
  gitalk:
    owner: your-github-username
    repo: your-repo-name
    clientID: your-github-oauth-app-id
    clientSecret: your-github-oauth-app-secret
    admin: [your-github-username]
```

**获取 OAuth 信息**：
1. 访问 https://github.com/settings/developers
2. 点击 "New OAuth App"
3. 填写应用信息
4. 获取 Client ID 和 Client Secret

### Utterances 配置

```yaml
comment:
  system: utterances
  utterances:
    repo: your-username/your-repo
    issueTerm: pathname
    label: comments
    theme: github-light
```

**配置步骤**：
1. 访问 https://github.com/apps/utterances
2. 安装应用到你的仓库
3. 获取仓库名称

---

## 验证配置

### 1. 本地预览
```bash
npm run server
```
访问 http://localhost:4000/your-article，查看评论区域

### 2. 检查浏览器控制台
- 按 F12 打开开发者工具
- 查看 Console 标签，检查是否有错误信息
- 查看 Network 标签，检查是否成功加载评论脚本

### 3. 测试评论功能
- 尝试发表评论
- 检查是否成功提交
- 验证评论是否显示

---

## 常见问题

### Q: 评论系统显示不出来？

**A**: 检查以下几点：
1. 确认已在 `_config.redefine.yml` 中启用评论系统
2. 检查服务 URL 是否正确
3. 清除浏览器缓存：Ctrl+Shift+Delete
4. 检查浏览器控制台是否有错误信息

### Q: 评论无法提交？

**A**: 可能的原因：
1. 服务 URL 无法访问
2. 数据库连接失败
3. 环境变量配置不正确
4. 浏览器安全限制（CORS 问题）

### Q: 如何禁用某些页面的评论？

**A**: 在文章 Front Matter 中添加：
```yaml
---
title: 文章标题
comments: false  # 禁用评论
---
```

### Q: 如何迁移现有评论？

**A**: 不同的评论系统有不同的迁移方式。建议：
1. 查看目标系统的官方文档
2. 使用官方提供的迁移工具
3. 如果没有工具，可能需要手动导入

---

## 推荐配置方案

对于中文博客，推荐使用 **Waline**：

**优点**：
- ✅ 支持中文
- ✅ 部署简单（Vercel）
- ✅ 功能完整
- ✅ 用户体验好
- ✅ 免费

**配置示例**：
```yaml
comment:
  system: waline
  waline:
    serverURL: https://your-waline.vercel.app
    emoji: true
    dark: auto
    requiredMeta: ['name', 'email']
    placeholder: 欢迎留言！
```

---

## 下一步

1. **选择评论系统**（推荐 Waline）
2. **部署服务**（如果需要）
3. **配置 `_config.redefine.yml`**
4. **本地测试**
5. **提交到 Git**

---

## 相关资源

- **Waline 官方文档**：https://waline.js.org/
- **Gitalk 官方文档**：https://github.com/gitalk/gitalk
- **Utterances 官方文档**：https://utteranc.es/
- **Redefine 主题文档**：https://redefine-docs.ohevan.com/

---

**最后更新**: 2025-11-08
**Hexo 版本**: 8.1.0
**主题**: Redefine v2.8.5

