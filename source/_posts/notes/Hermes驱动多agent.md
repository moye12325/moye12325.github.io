---
description: "这篇文章梳理 Hermes 在多 Agent 协作开发中的角色定位、任务拆解方式、文档体系、分支策略、评审流程与落地步骤，帮助个人开发者用工程化方法组织多个 AI Agent 协同交付。"
title: Hermes 驱动多 Agent 协作开发教程
date: 2026-06-17 15:11:19
updated: 2026-06-17 15:11:19
categories:
  - 随笔
tags:
  - AI
  - Agent
  - 工程化
  - 协作开发
summary: >
  这篇文章梳理 Hermes 在多 Agent 协作开发中的角色定位、任务拆解方式、文档体系、分支策略、评审流程与落地步骤，帮助个人开发者用工程化方法组织多个 AI Agent 协同交付。
---

## 1. 背景

在传统开发中，一个项目通常由产品、架构、前端、后端、测试、运维等角色共同完成。随着 Claude Code、Codex、Cursor Agent 等 AI 编程工具逐渐成熟，个人开发者也可以模拟一个小型工程团队：让不同 AI Agent 承担不同角色，并由一个总控 Agent 进行任务拆解、上下文管理、代码审查和合并决策。

本文介绍一种基于 Hermes 的多 Agent 协作开发方法。

在这个模式中：

* Hermes 负责整体调度、任务拆解、边界控制和结果验收。
* Claude Code / Codex Agent 负责具体模块实现。
* 文档体系负责约束所有 Agent 的行为。
* Git 分支和任务卡负责隔离工作范围。
* Reviewer Agent 负责审查代码质量、架构一致性和安全风险。

本文以 MailMind 项目为例，说明如何使用 Hermes 驱动多个 Agent 协作开发一个 AI Email Copilot。

---
description: "Hermes 在多 Agent 协作中相当于："

## 2. 核心理念

Hermes 多 Agent 协作开发的本质不是“同时打开多个 AI 写代码”，而是：

> 用文档、任务边界和验收标准约束多个 AI Agent，让它们像工程团队一样协同工作。

如果没有任务拆解和边界控制，多个 AI Agent 同时开发很容易造成：

* 重复实现同一功能；
* 多个 Agent 修改同一文件；
* API 合同不一致；
* 数据库模型被随意扩展；
* 安全规则被忽略；
* 项目结构快速失控；
* 最后代码看似很多，但无法集成。

因此，Hermes 的核心价值不是写代码，而是驾驭代码生成过程。

---

## 3. Hermes 的角色定位

Hermes 在多 Agent 协作中相当于：

```text
项目经理 + 架构师 + Tech Lead + Code Reviewer + 合并守门人
```

Hermes 的主要职责包括：

1. 阅读并维护项目核心文档。
2. 将需求拆解为小任务。
3. 为每个任务选择合适的 Agent。
4. 明确每个 Agent 可以修改哪些文件。
5. 明确每个 Agent 不能修改哪些文件。
6. 控制 MVP 范围，防止功能膨胀。
7. 审查各 Agent 的输出是否符合设计。
8. 处理跨模块冲突。
9. 决定是否合并代码。
10. 维护项目整体一致性。

Hermes 不应该直接承担所有编码任务。它更像一个总控系统，负责让多个 Agent 各司其职。

---

## 4. 多 Agent 协作前需要准备什么

在启动多个 Agent 之前，必须先准备基础文档。否则 Agent 会缺乏共同上下文，各自按照自己的理解写代码。

推荐至少准备以下文档：

```text
README.md
docs/product/PRD.md
docs/architecture/SYSTEM_DESIGN.md
docs/database/DATABASE_DESIGN.md
docs/api/API_DESIGN.md
docs/ai/AI_PIPELINE.md
docs/security/SECURITY.md
docs/engineering/AGENTS.md
docs/engineering/TASK_BREAKDOWN.md
docs/engineering/DEVELOPMENT.md
```

其中最关键的是：

| 文档                 | 作用                          |
| ------------------ | --------------------------- |
| PRD.md             | 定义产品要做什么                    |
| SYSTEM_DESIGN.md   | 定义系统如何分层                    |
| DATABASE_DESIGN.md | 定义数据模型                      |
| API_DESIGN.md      | 定义前后端接口合同                   |
| AI_PIPELINE.md     | 定义 AI 输入、输出、Prompt 和 Schema |
| SECURITY.md        | 定义 Token、邮件、日志和权限安全规则       |
| AGENTS.md          | 定义各 Agent 的职责和禁区            |
| TASK_BREAKDOWN.md  | 定义可执行任务列表                   |

如果这些文档不完整，Hermes 可以先委派 Agent 编写文档，而不是直接写代码。

---

## 5. 推荐 Agent 编队

以 MailMind 项目为例，可以将多个 Agent 分为以下角色。

```text
Hermes Orchestrator
├── Frontend Agent
├── Backend API Agent
├── Gmail Integration Agent
├── AI Pipeline Agent
├── Database Agent
├── DevOps Agent
├── Test Agent
└── Reviewer Agent
```

### 5.1 Frontend Agent

Frontend Agent 负责前端界面和交互。

主要职责：

* 初始化 Next.js 项目；
* 实现 Daily Digest Dashboard；
* 实现邮件详情页；
* 实现设置页；
* 实现 Job 状态轮询；
* 实现 API Client；
* 处理 loading、error、stale、failed 等状态。

允许修改：

```text
frontend/
```

禁止修改：

```text
backend/
database migrations
Gmail Provider
AI Pipeline
docker-compose.yml
```

---

### 5.2 Backend API Agent

Backend API Agent 负责 FastAPI 接口和业务编排。

主要职责：

* 实现 API Router；
* 定义请求和响应 Schema；
* 实现 Digest API；
* 实现 Email API；
* 实现 Job API；
* 编排 Service 层逻辑。

允许修改：

```text
backend/app/api/
backend/app/schemas/
backend/app/services/
```

禁止事项：

* 不直接调用 Gmail API；
* 不直接调用 LLM；
* 不直接写复杂 SQL；
* 不修改前端代码；
* 不擅自变更数据库结构。

---

### 5.3 Gmail Integration Agent

Gmail Integration Agent 负责 Gmail 接入。

主要职责：

* Google OAuth；
* Token refresh；
* GmailProvider；
* 获取今日邮件；
* 获取邮件详情；
* 标记已读；
* 标记未读；
* Gmail 邮件结构标准化。

允许修改：

```text
backend/app/providers/
backend/app/services/token_service.py
backend/app/services/email_sync_service.py
```

禁止事项：

* 不生成 Daily Digest；
* 不写前端；
* 不写 AI Prompt；
* 不擅自新增数据库表。

---

### 5.4 AI Pipeline Agent

AI Pipeline Agent 负责 AI 分析链路。

主要职责：

* EmailPreprocessor；
* DigestInputBuilder；
* LLMClient；
* StructuredOutputParser；
* DigestDecisionEngine；
* Prompt 版本管理；
* JSON Schema 校验；
* AI 输出标准化。

允许修改：

```text
backend/app/ai/
backend/app/services/ai_service.py
docs/ai/
```

禁止事项：

* 不调用 Gmail API；
* 不修改 OAuth；
* 不修改前端；
* 不擅自改数据库结构。

---

### 5.5 Database Agent

Database Agent 负责数据库模型和迁移。

主要职责：

* SQLAlchemy Models；
* Alembic Migrations；
* 表结构设计；
* 索引设计；
* 外键约束；
* 枚举定义；
* 初始化脚本。

允许修改：

```text
backend/app/db/
backend/app/models/
backend/migrations/
docs/database/
```

禁止事项：

* 不创建重复职责的数据表；
* 不把 AI 建议和用户行为混在一张表；
* 不把 Gmail 状态和本地处理状态混为一谈；
* 不修改 API 合同，除非 Hermes 批准。

---

### 5.6 DevOps Agent

DevOps Agent 负责本地开发环境和部署脚本。

主要职责：

* Docker Compose；
* PostgreSQL；
* Redis；
* Backend 启动；
* Frontend 启动；
* Celery Worker；
* Celery Beat；
* `.env.example`；
* 开发脚本；
* DEVELOPMENT.md。

允许修改：

```text
docker-compose.yml
docker/
.env.example
scripts/
docs/engineering/DEVELOPMENT.md
```

禁止事项：

* 不修改业务逻辑；
* 不修改 AI Prompt；
* 不修改 Gmail Scope；
* 不提交真实密钥。

---

### 5.7 Test Agent

Test Agent 负责编写测试。

主要职责：

* API 测试；
* Service 测试；
* Gmail Provider Mock；
* AI Schema 测试；
* Digest 生成测试；
* Job 状态测试；
* 安全回归测试。

允许修改：

```text
tests/
backend/tests/
frontend tests if configured
```

禁止事项：

* 不新增功能；
* 不使用真实 Gmail 凭据；
* 不使用真实 LLM API Key；
* 不为了测试通过而修改生产逻辑。

---

### 5.8 Reviewer Agent

Reviewer Agent 不写功能代码，只做审查。

主要职责：

* 检查是否符合 PRD；
* 检查是否符合架构设计；
* 检查是否超出 MVP 范围；
* 检查是否破坏 API 合同；
* 检查是否出现重复数据模型；
* 检查是否泄露 Token、邮件正文或 Prompt；
* 检查是否缺少测试；
* 检查是否需要更新文档。

Reviewer Agent 是多 Agent 协作中非常关键的一环。没有 Reviewer，多个 Agent 的代码很容易各自正确、整体错误。

---

## 6. 多 Agent 开发流程

推荐流程如下：

```text
Step 1：Hermes 阅读项目文档
Step 2：Hermes 拆解任务
Step 3：Hermes 为每个 Agent 分配任务卡
Step 4：每个 Agent 在独立分支开发
Step 5：Agent 提交实现说明
Step 6：Reviewer Agent 审查
Step 7：Hermes 汇总结果并处理冲突
Step 8：人工最终确认合并
Step 9：更新文档和任务状态
```

这个流程的核心是：

> 先定义边界，再让 Agent 写代码。

不要直接说“帮我实现整个后端”。这种任务太大，Agent 会自行发挥，最终很难集成。

---

## 7. 任务卡设计

Hermes 给 Agent 分配任务时，应使用任务卡，而不是一句话描述。

推荐任务卡模板：

```text
Task ID:
Role:
Goal:

Input Documents:
- ...

Allowed Files:
- ...

Forbidden Files:
- ...

Implementation Requirements:
1.
2.
3.

Acceptance Criteria:
1.
2.
3.

Out of Scope:
1.
2.
3.

Notes:
```

示例：

```text
Task ID: FE-001
Role: Frontend Agent
Goal: Implement the Daily Digest dashboard page using mock API data.

Input Documents:
- docs/product/PRD.md
- docs/architecture/SYSTEM_DESIGN.md
- docs/api/API_DESIGN.md

Allowed Files:
- frontend/src/app/dashboard/
- frontend/src/components/digest/
- frontend/src/lib/api.ts

Forbidden Files:
- backend/
- docs/database/
- docker-compose.yml

Implementation Requirements:
1. Show digest status bar.
2. Show urgent, review, and ignore sections.
3. Show stale digest notification.
4. Use mock API data.

Acceptance Criteria:
1. Dashboard page renders without backend.
2. Stale state displays "new emails not included" message.
3. No backend files are modified.

Out of Scope:
1. Gmail OAuth.
2. Real AI generation.
3. Email status sync.
```

任务卡越清晰，Agent 越不容易跑偏。

---

## 8. 分支策略

多个 Agent 不应该直接修改 main 分支。

推荐使用独立分支：

```text
feature/frontend-dashboard
feature/backend-api
feature/gmail-provider
feature/ai-pipeline
feature/database-models
feature/devops-compose
test/digest-api
docs/database-design
```

原则：

1. 一个任务一个分支；
2. 一个 Agent 不要同时做多个大任务；
3. 不同 Agent 尽量不要修改同一批文件；
4. 合并前必须 review；
5. 冲突由 Hermes 统一判断。

---

## 9. 哪些任务可以并行

适合并行的任务：

```text
Frontend 静态页面
Database Schema 设计
API 文档设计
AI Pipeline 文档设计
Docker Compose
README / 文档整理
Mock API
测试框架搭建
```

不适合过早并行的任务：

```text
真实 Gmail OAuth
真实 AI Digest
前后端联调
数据库迁移与 API 同时大改
Gmail Provider 与 Email Service 同时乱改
```

推荐顺序：

```text
1. 文档冻结
2. 数据库设计
3. API 设计
4. AI Pipeline 设计
5. 工程骨架
6. Mock 闭环
7. 真实 Gmail
8. 真实 AI
9. 已读未读同步
10. 测试与 Review
```

---

## 10. 推荐开发阶段

### Phase 0：文档冻结

目标：

```text
明确 MVP 范围、架构边界、数据模型和接口合同。
```

产物：

```text
PRD.md
SYSTEM_DESIGN.md
DATABASE_DESIGN.md
API_DESIGN.md
AI_PIPELINE.md
AGENTS.md
TASK_BREAKDOWN.md
```

### Phase 1：工程骨架

目标：

```text
项目能启动，但可以还没有真实业务。
```

委派：

```text
DevOps Agent：Docker Compose + .env.example
Backend Agent：FastAPI skeleton
Frontend Agent：Next.js skeleton
Database Agent：SQLAlchemy models
```

验收：

```text
PostgreSQL 启动
Redis 启动
Backend 启动
Frontend 启动
Worker 可启动
```

### Phase 2：Mock 闭环

目标：

```text
前端 Dashboard 能调用后端 Mock API，并展示 Daily Digest。
```

委派：

```text
Backend API Agent：实现 mock /api/digest/today
Frontend Agent：实现 Dashboard 页面
Test Agent：测试 API Response
```

验收：

```text
Dashboard 能展示 overview
Dashboard 能展示 urgent/review/ignore
Dashboard 能展示 stale 状态
```

### Phase 3：真实 Gmail

目标：

```text
完成 Gmail OAuth 和今日邮件同步。
```

委派：

```text
Gmail Integration Agent：OAuth + GmailProvider
Backend API Agent：接入 mailbox API
Database Agent：完善 mailboxes/emails 表
Test Agent：Gmail Mock 测试
```

验收：

```text
用户可连接 Gmail
系统可同步今日邮件
邮件可写入 emails 表
Token 可刷新
```

### Phase 4：真实 AI

目标：

```text
完成真实 Daily Digest 生成。
```

委派：

```text
AI Pipeline Agent：LLMClient + JSON Parser
Backend API Agent：接入 generate_digest
Database Agent：写入 daily_digests 和 digest_items
Test Agent：测试 AI 输出 Schema
```

验收：

```text
AI 返回结构化 JSON
daily_digests 生成成功
digest_items 写入成功
Dashboard 展示真实 AI 结果
```

### Phase 5：完整 MVP 闭环

目标：

```text
从 Gmail 到 AI 看板再到邮件操作形成完整闭环。
```

验收链路：

```text
连接 Gmail
同步今日邮件
生成 Daily Digest
展示 Dashboard
检测新邮件
刷新日报
进入邮件详情
标记已读/未读
同步至 Gmail
```

---

## 11. Hermes 的关键职责

Hermes 每次分配任务时都要回答 5 个问题：

1. 这个任务属于哪个模块？
2. 应该由哪个 Agent 做？
3. 允许它改哪些文件？
4. 明确禁止它改哪些文件？
5. 如何验收它的结果？

如果这 5 个问题答不清楚，说明任务还不能分配。

---

## 12. 典型错误与规避方法

### 错误一：任务太大

错误任务：

```text
实现 MailMind 后端。
```

正确任务：

```text
实现 GET /api/digest/today，先返回 mock digest 数据。
```

---

### 错误二：多个 Agent 改同一文件

规避方式：

* 一个任务一个分支；
* 每张任务卡写明 allowed files；
* Hermes 统一合并；
* Reviewer 检查越界修改。

---

### 错误三：没有 API 合同就让前后端并行

后果：

```text
前端假设字段叫 suggestedAction
后端返回 suggested_action
AI 输出叫 action
数据库字段叫 action_type
```

最终一地鸡毛。

规避方式：

```text
先写 API_DESIGN.md，再并行开发前后端。
```

---

### 错误四：AI 输出没有 Schema

后果：

```text
这次 AI 返回 urgent_emails
下次返回 important
再下次返回 must_handle
前端和数据库全部崩。
```

规避方式：

```text
AI 输出必须通过 JSON Schema 校验。
```

---

### 错误五：安全规则写在脑子里

后果：

```text
Agent 不小心把 token 打进日志。
Agent 把完整邮件正文存进 raw_ai_output。
Agent 把 .env 提交上 GitHub。
```

规避方式：

```text
SECURITY.md + AGENTS.md 明确禁止。
```

---

## 13. Review Checklist

Reviewer Agent 或 Hermes 审查代码时，应检查：

```text
是否符合 PRD？
是否符合 SYSTEM_DESIGN.md？
是否符合 API_DESIGN.md？
是否超出 MVP？
是否修改了禁止修改的文件？
是否引入不必要依赖？
是否泄露 Token / API Key？
是否记录完整邮件正文？
是否记录完整 AI Prompt？
是否新增重复表？
是否绕过 Provider Adapter？
是否绕过 AI Pipeline？
是否缺少测试？
是否需要更新文档？
```

---

## 14. 适合 MailMind 的第一批任务

推荐第一批任务如下：

```text
DOC-001: 整理 docs 目录结构
DOC-002: 编写 DATABASE_DESIGN.md
DOC-003: 编写 API_DESIGN.md
DOC-004: 编写 AI_PIPELINE.md
DOC-005: 编写 SECURITY.md
DEVOPS-001: 添加 docker-compose.yml
BACKEND-001: 初始化 FastAPI 项目骨架
FRONTEND-001: 初始化 Next.js 项目骨架
BACKEND-002: 实现 mock /api/digest/today
FRONTEND-002: 实现 Daily Digest Dashboard mock 页面
TEST-001: 添加后端基础测试框架
```

注意：第一批任务不要直接上 Gmail OAuth 和真实 AI。先跑通 Mock 闭环，再接真实外部服务。

---

## 15. 最佳实践总结

Hermes 多 Agent 协作开发的关键不是“Agent 数量越多越好”，而是：

```text
文档越清楚，Agent 越稳定。
任务越小，输出越可靠。
边界越明确，冲突越少。
验收越具体，返工越少。
```

推荐原则：

```text
先文档，后代码。
先合同，后并行。
先 Mock，后真实服务。
先小任务，后大功能。
先 Review，后合并。
```

---

## 16. 最终工作模式

一个理想的 Hermes 多 Agent 工作流应该是：

```text
PRD 定方向
SYSTEM_DESIGN 定架构
DATABASE_DESIGN 定数据
API_DESIGN 定接口
AI_PIPELINE 定 AI 输出
SECURITY 定安全边界
AGENTS 定协作规则
TASK_BREAKDOWN 定执行路径

Hermes 拆任务
Agent 分模块实现
Reviewer 审查
Hermes 合并
人类最终确认
```

最终目标不是让 AI 随便写更多代码，而是让 AI 在明确边界内稳定地产出可集成、可维护、可验证的工程成果。

---

## 17. 一句话总结

Hermes 驱动多 Agent 协作开发，本质上是一种面向 AI 编程时代的工程组织方式：

> 让 Hermes 负责方向、边界和验收，让多个 Agent 在清晰约束下并行完成模块化开发。

