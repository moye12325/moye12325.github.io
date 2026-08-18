---
title: 项目
date: 2026-08-18 17:30:00
updated: 2026-08-18 17:30:00
layout: page
---

## 🚀 项目概览

这里记录了我正在进行与已经完成的技术项目。内容会持续更新，欢迎常来看看。

### 进行中的项目

#### 📧 MailMind — 本地优先的 AI 邮件助手

> **组织**: [Vibe-Coding-X](https://github.com/Vibe-Coding-X) · **仓库**: [mailmind-ai-email-copilot](https://github.com/Vibe-Coding-X/mailmind-ai-email-copilot)

本地优先（local-first）的多邮箱 AI 邮件助手，连接 Gmail / IMAP 邮箱，自动同步邮件并经过 AI 流水线分析，生成结构化的 **Daily Digest（每日摘要）**：哪些邮件需要处理、建议动作和截止时间，而不是又一个收件箱视图。

- **技术栈**: FastAPI · SQLAlchemy 2 · Celery · PostgreSQL · Redis · Next.js 15 · React 19 · TypeScript · Electron
- **核心能力**:
  - 多 Mailbox Provider 抽象（Gmail / IMAP / Outlook 骨架），凭据加密存储
  - AI 供应商链（Mock + OpenAI-compatible）+ `ai_runs` 可追溯审计与防御式 LLM 解析
  - Celery 异步同步 / 摘要任务、失败重试、进度与错误 UI
  - 6 套主题 + 明暗模式 + 中英 i18n
  - Electron 桌面壳，Windows / macOS / Linux 三平台安装包
- **状态**: 进行中（正在做 v0.8 全内置桌面版）

#### 🔌 Codex Provider Hub — Codex / Claude 供应商本地中转与健康监测

> **组织**: [AI-Routing-Research-Institute](https://github.com/AI-Routing-Research-Institute) · **仓库**: [codex-provider-hub](https://github.com/AI-Routing-Research-Institute/codex-provider-hub)

面向个人自部署的 Codex API / Claude Code 多供应商管理工具。只启动一个监听 `127.0.0.1:17890` 的后台服务，同一端口提供 Codex 与 Claude 两个控制台视图，支持即时切换、失败自动重试、Token 统计与供应商健康监测。

- **技术栈**: Python FastAPI · httpx · SQLite · tiktoken · PyInstaller（Windows / macOS 便携版）
- **核心能力**:
  - 从 CC Switch 数据库只读加载 Codex / Claude 供应商，单端口双协议路由
  - 失败自动恢复（连接错误 / 流中断 / 429 / 5xx，含 SSE 内嵌 429 识别）
  - 供应商 / 模型健康探测 Worker + 独立状态页
  - CLI / GUI / TUI 探测工具，隔离 Codex 运行目录验证供应商能力
- **状态**: 进行中（v0.10.x）

### 已完成的项目

| 项目名称 | 技术栈 | 简要介绍 |
| -------- | ------ | -------- |
| 待补充 | Python / Web | 这里将记录重要的项目经验与亮点。 |

### 项目规划

- 构建更多与 AI、数据分析相关的实践项目
- 分享不同技术栈下的完整解决方案
- 优化项目文档与开源协作流程

如果你有项目合作意向，也欢迎联系我👨‍💻。
