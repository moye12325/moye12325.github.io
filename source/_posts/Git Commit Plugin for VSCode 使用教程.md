---
title: Git Commit Plugin for VSCode 使用教程
date: 2025-12-12 10:43:00
categories: [工具配置]
tags: ['VSCode', 'Git', '插件', '开发工具']
---

## 📖 插件简介

Git Commit Plugin 是一个帮助开发者规范 Git 提交信息的 VSCode 插件，基于**约定式提交（Conventional Commits）**规范，让团队的提交历史更清晰、更易读。

---

## 🎯 核心概念

### 提交信息结构

标准的提交信息由以下几部分组成：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**各部分说明：**

|字段|说明|是否必填|示例|
|---|---|---|---|
|**type**|提交类型|✅ 必填|`feat`, `fix`, `docs`|
|**scope**|影响范围|❌ 可选|`auth`, `user`, `config`|
|**subject**|简短描述|✅ 必填|`添加用户登录功能`|
|**body**|详细说明|❌ 可选|多行详细描述|
|**footer**|备注信息|❌ 可选|`Fixes #123`|

---

## 📷 插件界面说明

### 界面1：提交类型选择


![image.png](https://qiniu.kanes.top/blog/20251212104410224.png)


**提交类型一览：**

|图标|类型|说明|使用场景|
|---|---|---|---|
|🎉|**init**|项目初始化|首次提交|
|✨|**feat**|新增功能|添加新特性|
|🐛|**fix**|修复 bug|修复问题|
|📝|**docs**|文档修改|更新文档、注释|
|🎨|**style**|代码格式|格式化、缩进调整|
|🔨|**refactor**|代码重构|优化代码结构|
|⚡|**perf**|性能优化|提升性能|
|✅|**test**|测试相关|添加测试用例|
|🔧|**build**|构建/依赖|修改依赖、配置|

### 界面2：提交信息编辑页面

**需要截图的内容：**

![image.png](https://qiniu.kanes.top/blog/20251212104345884.png)


**界面说明：**

- **Scope（范围）**: 填写本次修改涉及的模块
- **Subject（主题）**: 简短概述（建议不超过50字符）
- **Body（正文）**: 详细说明，可使用 `<br>` 换行
- **Footer（备注）**: 关联 issue，如 `Fixes #123`
### 界面3：模板选择

**需要截图的内容：**

![image.png](https://qiniu.kanes.top/blog/20251212104424529.png)


**两种模板对比：**

|模板|格式|示例|
|---|---|---|
|**Angular**|`🐛 fix(scope): 主题`|`✨ feat(auth): 添加登录功能`|
|**git-cz**|`fix(scope): 🐛 主题`|`feat(auth): ✨ 添加登录功能`|

**推荐使用 Angular 模板**，因为图标在最前面更醒目，查看 Git 历史时更容易区分。

---

## 🚀 实战案例

### 案例：实现 `git commit -m "主题" -m "详细说明"`

**需求：** 提交一个 bug 修复，包含简短描述和详细说明：

```bash
git commit -m "适配Batch需求，修复部分问题" \
           -m "- 修复 param_options 类型处理 - 添加错误处理机制"
```

### 操作步骤：

#### 1️⃣ 启动插件

- 按下快捷键或点击插件图标打开提交界面

#### 2️⃣ 选择提交类型

- 选择：`🐛 fix`

#### 3️⃣ 填写范围（Scope）

```
Flows Config
```

#### 4️⃣ 填写主题（Subject）- 对应第一个 `-m`

```
适配Batch需求，修复部分问题
```

#### 5️⃣ 填写正文（Body）- 对应第二个 `-m`

```
- 修复 param_options 类型处理以支持 dict 和 QDict 格式
- 在恢复实验缓存参数选项时添加适当的错误处理
```

#### 6️⃣ 填写备注（Footer）- 可选

```
Fixes #256
```

#### 7️⃣ 点击 Complete 完成提交

### 最终生成的提交信息：

```
🐛 fix(Flows Config): 适配Batch需求，修复部分问题

- 修复 param_options 类型处理以支持 dict 和 QDict 格式
- 在恢复实验缓存参数选项时添加适当的错误处理

Fixes #256
```

---

## 💡 最佳实践

### ✅ 推荐做法

1. **Subject 简洁明了**
    
    - ✅ `修复用户登录失败问题`
    - ❌ `修复了一个在用户登录时可能会出现的各种奇怪问题`
2. **Body 详细具体**
    
    - 说明修改的原因
    - 列出主要改动点
    - 使用列表符号 `-` 或数字
3. **使用正确的 type**
    
    - 新功能用 `feat`
    - 修 bug 用 `fix`
    - 改文档用 `docs`
4. **关联 issue**
    
    - 在 Footer 中使用 `Fixes #123` 或 `Closes #456`

### ❌ 常见错误

1. **Subject 太长**
    
    - 建议控制在 50 字符以内
2. **type 使用错误**
    
    - 代码重构不要用 `feat`，应该用 `refactor`
    - 格式调整不要用 `fix`，应该用 `style`
3. **缺少详细说明**
    
    - 复杂改动务必在 Body 中详细说明

---

## 🔧 配置建议

### 团队协作配置

1. **统一模板风格**
    
    - 团队成员统一使用 Angular 或 git-cz 模板
2. **定义 Scope 规范**
    
    - 例如：`auth`, `user`, `payment`, `config` 等
    - 建立团队 Scope 列表文档
3. **提交信息检查**
    
    - 配合 `commitlint` 工具进行提交信息校验
    - 在 CI/CD 中加入提交信息检查

---

## 📚 相关资源

- [约定式提交规范](https://www.conventionalcommits.org/)
- [Angular 提交规范](https://github.com/angular/angular/blob/main/CONTRIBUTING.md)
- [Commitizen 工具](https://github.com/commitizen/cz-cli)

---

## ❓ 常见问题

### Q1: Subject 和 Body 有什么区别？

**A:** Subject 是简短概述（一句话），Body 是详细说明（多行文本）。相当于 `git commit -m "Subject" -m "Body"`。

### Q2: 什么时候需要填写 Body？

**A:** 当修改较复杂、需要详细说明时填写。简单改动可以只填 Subject。

### Q3: Footer 主要用来做什么？

**A:** 主要用于关联 issue，如 `Fixes #123` 会自动关闭对应的 issue。

### Q4: 可以不填 Scope 吗？

**A:** 可以，Scope 是可选的。但建议填写，便于快速定位改动范围。

