---
title: VSCode清理缓存完全指南
date: 2025-11-25 14:15:07
categories: [开发工具]
tags: [VSCode, 工具使用, 缓存清理, 开发环境, 效率提升]
---

VS Code 清理缓存的几种方法:

## 1. 通过命令行清理(最彻底)

关闭 VS Code 后,手动删除以下目录:

**Windows:**
```
%APPDATA%\Code\Cache
%APPDATA%\Code\CachedData
%APPDATA%\Code\Code Cache
%APPDATA%\Code\GPUCache
```

**macOS:**
```
~/Library/Application Support/Code/Cache
~/Library/Application Support/Code/CachedData
~/Library/Application Support/Code/Code Cache
~/Library/Application Support/Code/GPUCache
```

**Linux:**
```
~/.config/Code/Cache
~/.config/Code/CachedData
~/.config/Code/Code Cache
~/.config/Code/GPUCache
```

## 2. 使用内置命令

在 VS Code 中按 `F1` 或 `Ctrl/Cmd + Shift + P`,输入并执行:
- `Developer: Reload Window` - 重新加载窗口
- `Preferences: Clear Editor History` - 清除编辑器历史

## 3. 清理扩展缓存

删除扩展目录下的缓存:
- **Windows:** `%USERPROFILE%\.vscode\extensions`
- **macOS/Linux:** `~/.vscode/extensions`

可以选择性删除不需要的扩展文件夹。

## 4. 重置所有设置(谨慎使用)

如果想完全重置 VS Code,可以删除整个用户数据目录:
- **Windows:** `%APPDATA%\Code`
- **macOS:** `~/Library/Application Support/Code`
- **Linux:** `~/.config/Code`

**注意:** 这会删除所有设置、扩展和数据,建议先备份。

## 5. 工作区缓存

删除项目中的 `.vscode` 文件夹(如果存在),可以清除项目特定的缓存设置。

清理缓存后重启 VS Code 即可生效。如果遇到 VS Code 运行缓慢或异常,清理缓存通常能解决问题。