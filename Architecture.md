# 博客部署架构方案
 
## 📋 目录
- [方案概述](#方案概述)
- [架构设计](#架构设计)
- [技术选型](#技术选型)
- [部署流程](#部署流程)
- [多终端协作方案](#多终端协作方案)
- [详细实施步骤](#详细实施步骤)
- [日常使用流程](#日常使用流程)
- [成本分析](#成本分析)
 
---
 
## 方案概述
 
### 核心目标
1. **零成本**：充分利用免费服务和已有资源
2. **高可用**：多平台部署，互为备份
3. **高性能**：CDN加速，国内外访问优化
4. **易维护**：换电脑后快速恢复写作环境
 
### 资源清单
- ✅ 已备案域名（自有）
- ✅ 腾讯云CDN（已购买）
- 🆓 GitHub Pages（免费）
- 🆓 Vercel（免费）
- 🆓 GitHub仓库（免费）
- 🆓 Hexo框架（开源）
 
---

## 架构设计
 
```
┌─────────────────────────────────────────────────────────────┐
│                         用户访问                              │
│                    yourdomain.com                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      DNS 智能解析                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 国内流量 → 腾讯云CDN → GitHub Pages/Vercel            │   │
│  │ 国外流量 → Vercel CDN (自带)                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      静态资源存储                             │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  GitHub Pages    │ ◄──► │     Vercel       │            │
│  │   (主站点)       │      │   (备用站点)      │            │
│  └──────────────────┘      └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                  ▲
                  │
┌─────────────────────────────────────────────────────────────┐
│                    自动化部署流程                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  本地/在线编辑 → Push to GitHub → GitHub Actions     │   │
│  │     ↓                                    ↓            │   │
│  │  自动构建 Hexo                   自动部署到 GH Pages  │   │
│  │                                          ↓            │   │
│  │                              Vercel 自动同步部署      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                  ▲
                  │
┌─────────────────────────────────────────────────────────────┐
│                     内容管理仓库                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GitHub 仓库 (Private/Public)                        │   │
│  │  ├── source/_posts/        (博客文章 Markdown)       │   │
│  │  ├── themes/               (主题配置)                │   │
│  │  ├── _config.yml           (Hexo 配置)               │   │
│  │  └── .github/workflows/    (自动化脚本)              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```
 
---
 
## 技术选型
 
### 1. Hexo（静态博客生成器）
**选择理由：**
- ✅ 完全免费开源
- ✅ 主题丰富，生态成熟
- ✅ 支持Markdown写作
- ✅ 构建速度快
- ✅ 中文文档完善
 
**替代方案：** Hugo（速度更快）、Jekyll（GitHub原生支持）
 
### 2. GitHub Pages（主部署平台）
**选择理由：**
- ✅ 完全免费
- ✅ 与GitHub仓库无缝集成
- ✅ 支持自定义域名
- ✅ 自动SSL证书
- ✅ 可靠性高
 
**限制：** 每月100GB流量限制（个人博客完全够用）
 
### 3. Vercel（备用部署平台）
**选择理由：**
- ✅ 完全免费（个人项目）
- ✅ 自动从GitHub同步
- ✅ 全球CDN加速（国外访问极快）
- ✅ 自动SSL证书
- ✅ 零配置部署
 
**优势：** 国外访问速度比GitHub Pages快
 
### 4. 腾讯云CDN（国内加速）
**选择理由：**
- ✅ 已购买，充分利用
- ✅ 国内访问速度优化
- ✅ 满足备案要求
- ✅ 降低源站压力
 
### 5. GitHub Actions（自动化部署）
**选择理由：**
- ✅ 完全免费（每月2000分钟）
- ✅ 自动构建和部署
- ✅ 无需本地环境
 
---
 
## 部署流程
 
### 架构优势
1. **双平台部署**：GitHub Pages + Vercel 互为备份
2. **CDN加速**：国内走腾讯云CDN，国外走Vercel CDN
3. **自动化**：Push代码后自动构建部署
4. **高可用**：任一平台故障，另一个可接管
 
### 访问路径
 
#### 方案A：主推方案（智能分流）
```
国内用户：
域名 → 腾讯云CDN → GitHub Pages
     （或者）
域名 → 腾讯云CDN → Vercel
 
国外用户：
域名 → Vercel CDN → Vercel
```
 
#### 方案B：简化方案
```
所有用户：
域名 → 腾讯云CDN → Vercel
```
 
**推荐：方案A**，国内外都能获得最佳访问速度
 
---
 
## 多终端协作方案
 
### 核心思路：内容源码化管理
 
所有博客内容（Markdown文章、配置文件、主题）都存储在GitHub仓库中，换电脑后只需：
 
### 方案1：GitHub + Codespaces/Gitpod（推荐，最省事）
 
**优势：** 零本地环境，任何设备都能写作
 
#### 使用步骤：
1. 打开GitHub仓库
2. 点击 `Code` → `Codespaces` → `Create codespace`
3. 在线VSCode中直接编辑Markdown
4. 提交后自动部署
 
**成本：** GitHub Codespaces 免费额度每月60小时
 
### 方案2：GitHub Web 编辑器（最简单）
 
**优势：** 无需任何安装，浏览器即可
 
#### 使用步骤：
1. 打开GitHub仓库
2. 进入 `source/_posts/` 目录
3. 点击 `Add file` → `Create new file`
4. 文件名：`2024-01-01-article-title.md`
5. 编辑内容，提交后自动部署
 
### 方案3：本地环境（功能最全）
 
**适用场景：** 需要预览效果、调试主题
 
#### 新电脑快速恢复：
```bash
# 1. 安装Node.js（一次性）
# 访问 nodejs.org 下载安装
 
# 2. 克隆博客仓库
git clone https://github.com/yourusername/blog.git
cd blog
 
# 3. 安装依赖（项目有package.json会自动安装）
npm install
 
# 4. 开始写作
hexo new "文章标题"
hexo server  # 本地预览
 
# 5. 发布
git add .
git commit -m "新文章"
git push
```
 
**只需安装：** Node.js（一个软件），其他都是一行命令搞定
 
### 方案4：移动端写作（随时随地）
 
**工具推荐：**
- **IA Writer** / **Obsidian** / **Notion**：写Markdown
- **Working Copy**（iOS）：直接提交到GitHub
- **MGit**（Android）：Git客户端
 
#### 流程：
1. 移动端编辑器写Markdown
2. 通过Git应用提交到GitHub
3. 自动触发部署
 
---
 
## 详细实施步骤
 
### 第一步：创建Hexo博客仓库
 
```bash
# 本地初始化（只需做一次）
npm install -g hexo-cli
hexo init my-blog
cd my-blog
npm install
 
# 安装必要插件
npm install hexo-deployer-git --save
npm install hexo-generator-searchdb --save
```
 
### 第二步：配置Hexo
 
编辑 `_config.yml`：
 
```yaml
# 网站配置
title: 你的博客标题
subtitle: '副标题'
description: '博客描述'
author: 你的名字
language: zh-CN
timezone: 'Asia/Shanghai'
 
# URL配置
url: https://yourdomain.com
root: /
permalink: :year/:month/:day/:title/
 
# 主题配置
theme: next  # 或其他主题
 
# 部署配置（可选，使用GitHub Actions可不配置）
deploy:
  type: git
  repo: https://github.com/yourusername/yourusername.github.io
  branch: main
```
 
### 第三步：推送到GitHub
 
```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit"
 
# 创建GitHub仓库后
git remote add origin https://github.com/yourusername/blog-source.git
git branch -M main
git push -u origin main
```
 
### 第四步：配置GitHub Actions自动部署
 
创建 `.github/workflows/deploy.yml`：
 
```yaml
name: Deploy Hexo to GitHub Pages
 
on:
  push:
    branches:
      - main  # 监听main分支
 
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout 🛎️
      uses: actions/checkout@v3
      with:
        submodules: true  # 如果使用了Git submodule主题
    
    - name: Setup Node.js 🔧
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install Dependencies 📦
      run: |
        npm install
        npm install hexo-cli -g
    
    - name: Build Hexo 🏗️
      run: |
        hexo clean
        hexo generate
    
    - name: Deploy to GitHub Pages 🚀
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./public
        publish_branch: gh-pages
        cname: yourdomain.com  # 你的域名
```
 
### 第五步：配置GitHub Pages
 
1. 进入仓库 Settings → Pages
2. Source 选择 `gh-pages` 分支
3. Custom domain 填写你的域名
4. 勾选 `Enforce HTTPS`
 
### 第六步：配置Vercel部署
 
#### 方式1：通过Vercel Dashboard
1. 访问 [vercel.com](https://vercel.com)
2. Import GitHub仓库
3. Framework Preset 选择 `Hexo`
4. Build Command: `hexo generate`
5. Output Directory: `public`
6. 点击 Deploy
 
#### 方式2：配置文件（推荐）
创建 `vercel.json`：
 
```json
{
  "build": {
    "env": {
      "NODE_VERSION": "18"
    }
  },
  "buildCommand": "npm install && hexo generate",
  "outputDirectory": "public",
  "framework": "hexo"
}
```
 
### 第七步：配置域名DNS
 
#### 在你的域名服务商处添加解析：
 
##### 方案A：智能解析（推荐）
 
**腾讯云 DNSPod 设置：**
 
```
# 国内线路
类型: CNAME
主机记录: @
记录值: [腾讯云CDN分配的CNAME]
线路类型: 境内
 
# 国外线路
类型: CNAME  
主机记录: @
记录值: cname.vercel-dns.com
线路类型: 境外
```
 
##### 方案B：全部走CDN
 
```
类型: CNAME
主机记录: @
记录值: [腾讯云CDN分配的CNAME]
线路类型: 默认
```
 
### 第八步：配置腾讯云CDN
 
1. **添加加速域名**
   - 域名：`yourdomain.com`
   - 源站类型：`自有源站`
   - 源站地址：`yourusername.github.io` 或 `yourproject.vercel.app`
 
2. **HTTPS配置**
   - 上传SSL证书（免费申请Let's Encrypt）
   - 开启HTTP/2
   - 开启HTTPS强制跳转
 
3. **缓存配置**
   ```
   - *.html: 缓存1小时
   - *.js, *.css: 缓存7天
   - *.jpg, *.png, *.gif: 缓存30天
   ```
 
4. **回源配置**
   - 回源协议：HTTPS
   - 回源Host：源站域名
 
5. **获取CNAME**
   - 复制CDN分配的CNAME地址
   - 添加到DNS解析
 
---
 
## 日常使用流程
 
### 情况1：在主力电脑写作
 
```bash
# 进入博客目录
cd my-blog
 
# 更新代码（如果有其他设备修改过）
git pull
 
# 创建新文章
hexo new "文章标题"
 
# 编辑 source/_posts/文章标题.md
 
# 本地预览（可选）
hexo server
# 访问 http://localhost:4000 查看效果
 
# 提交发布
git add .
git commit -m "发布新文章：文章标题"
git push
 
# 等待1-2分钟，GitHub Actions自动部署完成
```
 
### 情况2：换新电脑/临时电脑
 
```bash
# 只需执行一次
git clone https://github.com/yourusername/blog-source.git
cd blog-source
npm install
 
# 后续使用与情况1相同
```
 
### 情况3：在线编辑（最快速）
 
1. 打开 `github.com/yourusername/blog-source`
2. 按 `.` 键（进入github.dev在线编辑器）
3. 或者访问 `github.dev/yourusername/blog-source`
4. 在 `source/_posts/` 创建新Markdown文件
5. 使用左侧Git面板提交
 
### 情况4：手机/平板写作
 
1. 在Markdown编辑器中写作
2. 保存为 `.md` 文件
3. 使用Git客户端提交到仓库
4. 或通过GitHub App直接创建文件
 
---
 
## 成本分析
 
### 完全免费项目
| 服务 | 费用 | 限额 |
|------|------|------|
| Hexo | 免费 | 无限制 |
| GitHub仓库 | 免费 | 无限制 |
| GitHub Pages | 免费 | 100GB/月流量 |
| GitHub Actions | 免费 | 2000分钟/月 |
| Vercel | 免费 | 100GB/月流量 |
| SSL证书 | 免费 | 自动续期 |
 
### 已有资源
| 资源 | 状态 | 用途 |
|------|------|------|
| 域名 | 已购买+备案 | 博客访问入口 |
| 腾讯云CDN | 已购买 | 国内加速 |
 
### 总成本：¥0
- 博客托管：免费
- 部署流程：免费
- CDN加速：已有资源
- 域名：已购买（沉没成本）
 
### 流量估算
以个人博客为例：
- 日访问量：100-1000 PV
- 月流量：约 1-10 GB
- **结论：** 免费额度完全够用，无需付费
 
---
 
## 高级优化建议
 
### 1. 图床方案
**问题：** 图片存在GitHub会占用仓库空间
 
**解决方案：**
- **免费方案：** GitHub仓库 + jsDelivr CDN加速
- **腾讯云COS：** 已有腾讯云账号，可使用免费额度
- **图床服务：** 路过图床、SM.MS（免费）
 
### 2. 评论系统
- **Giscus：** 基于GitHub Discussions（推荐）
- **Waline：** 基于LeanCloud（免费额度）
- **Twikoo：** 部署在Vercel（免费）
 
### 3. 统计分析
- **Google Analytics：** 免费、功能强大
- **百度统计：** 国内SEO友好
- **不蒜子：** 简单访问计数
 
### 4. SEO优化
```yaml
# 安装SEO插件
npm install hexo-generator-sitemap --save
npm install hexo-generator-baidu-sitemap --save
 
# _config.yml添加
sitemap:
  path: sitemap.xml
baidusitemap:
  path: baidusitemap.xml
```
 
### 5. RSS订阅
```bash
npm install hexo-generator-feed --save
```
 
### 6. 搜索功能
```bash
npm install hexo-generator-searchdb --save
```
 
---
 
## 故障切换方案
 
### 场景1：GitHub Pages访问故障
- **解决：** DNS切换到Vercel
- **操作：** 修改CDN源站为Vercel域名
- **恢复时间：** 5分钟
 
### 场景2：Vercel访问故障
- **解决：** DNS切换到GitHub Pages
- **操作：** 修改CDN源站为GitHub Pages域名
- **恢复时间：** 5分钟
 
### 场景3：CDN故障
- **解决：** DNS直接解析到Vercel/GitHub Pages
- **影响：** 国内访问速度下降，但不影响可用性
 
---
 
## 维护清单
 
### 每次写文章
- [ ] `git pull` 拉取最新代码
- [ ] `hexo new "标题"` 创建文章
- [ ] 编辑Markdown文件
- [ ] `git push` 提交发布
 
### 每月检查
- [ ] 查看CDN流量使用情况
- [ ] 查看GitHub Actions构建状态
- [ ] 备份重要文章（虽然Git已经是备份）
 
### 每季度优化
- [ ] 检查主题是否有更新
- [ ] 检查Hexo版本更新
- [ ] 清理CDN缓存（如果需要）
- [ ] 分析访问统计，优化内容
 
---
 
## 总结
 
### ✅ 方案优势
1. **真正零成本**：所有服务都是免费的
2. **高可用性**：双平台部署，CDN加速
3. **易于迁移**：内容在Git仓库，随时恢复
4. **自动化**：Push即部署，无需手动操作
5. **性能优秀**：国内外都有CDN加速
6. **扩展性强**：可随时添加新功能
 
### 🎯 适用人群
- ✅ 个人博客作者
- ✅ 技术写作者
- ✅ 经常换电脑的用户
- ✅ 追求性价比的用户
- ✅ 需要国内备案的用户
 
### 🚀 快速开始
1. 30分钟：搭建基础框架
2. 1小时：完成所有配置
3. 5分钟：发布第一篇文章
4. 永久：零成本运行
 
---
 
## 附录：常用命令速查
 
```bash
# Hexo常用命令
hexo new "标题"        # 新建文章
hexo new page "页面"   # 新建页面
hexo generate          # 生成静态文件
hexo server            # 启动本地预览
hexo clean             # 清理缓存
 
# Git常用命令
git pull               # 拉取更新
git add .              # 添加所有更改
git commit -m "说明"   # 提交更改
git push               # 推送到远程
 
# npm常用命令
npm install            # 安装依赖
npm update             # 更新依赖
npm run build          # 构建项目
 
# 快速发布流程（一行命令）
hexo clean && hexo g && git add . && git commit -m "update" && git push
```
 
---
 
## 问题排查
 
### Q1: Push后没有自动部署
- 检查GitHub Actions是否运行（Actions标签页）
- 查看构建日志找到错误原因
- 确认 `.github/workflows/deploy.yml` 配置正确
 
### Q2: 域名无法访问
- 检查DNS解析是否生效（`nslookup yourdomain.com`）
- 检查CDN配置是否正确
- 检查源站是否可访问
 
### Q3: 本地预览正常，部署后样式错乱
- 检查 `_config.yml` 中的 `url` 和 `root` 配置
- 检查是否使用了绝对路径
- 清理CDN缓存
 
### Q4: GitHub Actions构建失败
- 检查 `package.json` 依赖是否完整
- 检查Node.js版本是否兼容
- 查看Actions日志中的具体错误
 
---
 
**🎉 恭喜！你现在拥有一个零成本、高可用、易维护的博客系统！**
 
**📝 开始你的第一篇博客吧：`hexo new "Hello World"`**
