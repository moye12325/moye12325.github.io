---
title: Windows Terminal + PowerShell 7 + Oh My Posh 美化折腾记
date: 2024-12-01 11:58:00
categories: [工具配置]
tags: ['PowerShell', 'Windows Terminal', 'Oh My Posh', '终端美化']
---


最近想给自己的 PowerShell 终端来个大变身，毕竟每天对着黑底白字的命令行确实有点单调。网上搜了一圈，发现 Oh My Posh 这个工具挺火的，于是开始了这趟折腾之旅。

## 安装遇到的第一个坑

按照网上的教程，我直接复制了这条安装命令：

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://ohmyposh.dev/install.ps1'))
```

结果立马遇到了权限问题。说实话，Windows 的权限机制有时候真的让人头疼。

冷静下来想了想，其实解决办法也不复杂。最直接的方式就是**以管理员身份运行 PowerShell**，然后再执行安装命令。不过我发现还有更简单的路子——用 winget：

```powershell
winget install JanDeDobbeleer.OhMyPosh -s winget
```

一行搞定，省心多了。

## 意外发现：其实已经装好了

运行完命令后，系统提示找不到可用的升级，这才意识到我电脑上可能早就装过了。验证一下：

```powershell
oh-my-posh --version
```

果然，`28.1.0` 版本赫然在目。虽然安装脚本报了个 `Add-AppxPackage` 模块加载的错，但好在并不影响使用。

## 配置文件在哪里?

接下来就是配置环节了。按照惯例，应该编辑 PowerShell 的配置文件 `$PROFILE`。先检查一下这个文件存不存在：

```powershell
Test-Path $PROFILE
```

返回 `False`。好吧，看来得从零开始创建。

网上找到的配置模板大概是这样的：

```powershell
C:\\Users\\用户名\\AppData\\Local\\Programs\\oh-my-posh\\bin\\oh-my-posh.exe init pwsh --config $env:POSH_THEMES_PATH\montys.omp.json | Invoke-Expression

Import-Module posh-git
Import-Module PSReadLine

Set-PSReadLineOption -PredictionSource History
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
```

这个配置看起来挺全面的：Oh My Posh 负责美化提示符，posh-git 显示 Git 状态，PSReadLine 则让命令补全更智能。

不过我发现了几个可以优化的地方：

1. **硬编码路径没必要**。既然 `oh-my-posh` 已经在 PATH 里了，直接写命令名就行，不用整那么长的绝对路径。
    
2. **加个容错处理**。万一 posh-git 没装，脚本就会报错。加上 `-ErrorAction SilentlyContinue` 可以避免这个问题。
    
3. **编码要用 UTF8**。否则配置文件里的中文注释可能乱码。
    

改进后的版本：

```powershell
New-Item -Path $PROFILE -Type File -Force

@"
# Oh My Posh 初始化
oh-my-posh init pwsh --config `$env:POSH_THEMES_PATH\montys.omp.json | Invoke-Expression

# 引入 posh-git
Import-Module posh-git -ErrorAction SilentlyContinue

# 引入 PSReadLine
Import-Module PSReadLine

# 历史命令智能补全
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
"@ | Set-Content -Path $PROFILE -Encoding UTF8
```

## 只对 PowerShell 7 生效

电脑上还有 Windows PowerShell 5.1 和 CMD，这个配置对它们管用吗？

答案是**不管用**。不同的 Shell 配置文件路径完全不同：

- **PowerShell 7**: `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
- **Windows PowerShell 5.1**: `~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
- **CMD**: 压根不支持这种配置方式

如果你两个版本的 PowerShell 都在用，可以创建一个共享配置文件，然后在各自的 `$PROFILE` 里引用它。不过说实话，既然 PowerShell 7 才是未来，我建议就配置它一个就够了。

## 字体显示乱码

配置完重启终端，提示符确实变漂亮了，但仔细一看：

```
◆ DESKTOP-0M9LU6E ◆ ◆ ◆ ◆ 0ms ◆ 11:39 AM ◆ ◆
⚡BY250013 ❯❯
```

![image.png](https://qiniu.kanes.top/blog/20251201115836486.png)


一开始我以为是字体问题，后来发现其实是 `montys` 这个主题本身就爱用菱形分隔符。要彻底解决，得换个主题。

先看看都有哪些主题可选：

```powershell
Get-ChildItem $env:POSH_THEMES_PATH
```

然后直接测试几个常用的：

```powershell
# 简洁风格
oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\jandedobbeleer.omp.json | Invoke-Expression

# 极简风格
oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\pure.omp.json | Invoke-Expression

# 经典 agnoster
oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\agnoster.omp.json | Invoke-Expression
```

每执行一个命令，提示符立马就变样，实时预览效果相当直观。

我最后选了 `jandedobbeleer`，这是 Oh My Posh 作者自己在用的主题，显示效果稳定，信息该有的都有，又不会过分花哨。

找到心仪的主题后，打开配置文件：

```powershell
notepad $PROFILE
```

把第一行的主题名改掉：

```powershell
oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\jandedobbeleer.omp.json | Invoke-Expression
```

保存，重启 PowerShell，搞定。

## 安装依赖模块

配置文件里用到了 `posh-git` 和 `PSReadLine`，记得先装上：

```powershell
Install-Module posh-git -Scope CurrentUser -Force
Install-Module PSReadLine -Scope CurrentUser -Force -SkipPublisherCheck
```

`PSReadLine` 一般系统都自带了，但保险起见还是跑一遍。

装完之后重新加载配置：

```powershell
. $PROFILE
```

这些配置带来的体验提升还挺明显的：

- 输入命令开头几个字母，按 ↑ 就能快速翻到历史命令
- Tab 补全会弹出菜单，不用一个个试
- Git 仓库里工作时，提示符会直接显示分支名和状态

## 写在最后

折腾了一下午，终端总算变得顺眼多了。回过头来看，整个过程其实也没那么复杂，主要就是三步：

1. 装 Oh My Posh（winget 一行搞定）
2. 创建配置文件（选个主题，配点快捷键）
3. 装依赖模块（posh-git 和 PSReadLine）
