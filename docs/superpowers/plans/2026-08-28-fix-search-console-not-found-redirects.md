# Search Console 历史失效链接修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 Google Search Console 报告中的 26 个仍属于本站的历史大小写/特殊字符 URL 永久跳转到当前规范 URL，并确认线上响应正常。

**Architecture:** 在 Vercel 的 `redirects` 中保留旧 URL 到规范 URL 的一对一永久重定向。对中文、空格、反引号等路径统一使用 URL 编码，避免部署平台在匹配规则时与请求路径的解码阶段不一致；废弃的 `xlog.kanes.top` 和 `server.kanes.top` 不在本仓库中处理。

**Tech Stack:** Vercel `vercel.json`、PowerShell 网络检查、Git。

## Global Constraints

- GitHub 相关 Git 操作必须通过 `http://127.0.0.1:7897` 代理。
- 不为已废弃的 `xlog.kanes.top`、`server.kanes.top` 增加博客仓库规则。
- 提交前必须通过 JSON、构建和格式检查；推送后只有旧 URL 返回 `301/308` 且最终规范 URL 返回 `200`，才报告修复完成。

---

### Task 1: 复现并确认 Vercel 路径匹配问题

**Files:**
- Read: `vercel.json`
- Read: `F:\未找到.txt`

- [x] **Step 1: 检查当前重定向规则与工作区状态**

```powershell
git status --short --branch
Get-Content -Raw -LiteralPath 'vercel.json'
```

- [x] **Step 2: 对报告中的中文/空格路径发起线上请求**

使用 `Invoke-WebRequest -Method Head -MaximumRedirection 0` 检查旧路径的状态码和 `Location`，记录仍返回 404 的规则匹配差异。

### Task 2: 将 Vercel 规则改为编码路径

**Files:**
- Modify: `vercel.json` 的 `redirects`

- [x] **Step 1: 先运行配置检查，确认当前中文旧路径没有得到期望的 3xx**

用与 Task 1 相同的 URL 集合检查，作为回归基线。

- [x] **Step 2: 修改规则**

仅将含中文、空格、反引号或其他特殊字符的 `source` 与 `destination` 改为对应的 percent-encoded 路径；ASCII-only 规则保持不变。

- [x] **Step 3: 验证 JSON 和规则数量**

```powershell
node -e "const c=require('./vercel.json'); if(c.redirects.length!==27) process.exit(1); console.log('vercel.json OK:', c.redirects.length, 'redirects')"
```

### Task 3: 构建、部署后线上回归并推送

**Files:**
- Verify: `vercel.json`

- [x] **Step 1: 运行构建与格式检查**

```powershell
npm run build
git diff --check
```

- [x] **Step 2: 提交配置修复**

```powershell
git add vercel.json docs/superpowers/plans/2026-08-28-fix-search-console-not-found-redirects.md
git commit -m "fix(seo): 编码历史失效 URL 重定向"
```

- [x] **Step 3: 通过本地代理推送到远程**

```powershell
git -c http.proxy='http://127.0.0.1:7897' -c https.proxy='http://127.0.0.1:7897' push origin main
```

- [x] **Step 4: 部署完成后逐条核验**

报告中的 26 个本站旧 URL 必须返回 `301/308` 并指向规范 URL；每个规范 URL 必须最终返回 `200`。两个废弃域名只记录为不在本仓库修复范围内。
