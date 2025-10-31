---
date: 2024-07-22T18:01:07.342Z
updated: null
title: windows server2019安装docker
slug: '86704361347697'
oid: 669e9e632a6fe84dfe920ab4
categories: 所遇问题
type: post
permalink: /posts/所遇问题/86704361347697
---


# windows server2019安装docker

## 安装

在Windows Server 2019上安装Docker的步骤如下：

### 1\. 系统要求

确保你的Windows Server 2019版本支持容器功能。建议更新系统到最新的修补程序和服务包。

### 2\. 启用容器功能

1. 打开PowerShell，以管理员身份运行以下命令启用容器和Hyper-V功能：

powershell

复制代码
```
Install-WindowsFeature -Name containers -IncludeAllSubFeature
Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart
```

1. 系统会提示重启服务器，重启后继续下一步。

### 3\. 安装Docker

1. 下载Docker安装脚本：  
   * 打开PowerShell，以管理员身份运行以下命令下载并安装Docker：

powershell

复制代码
```
Invoke-WebRequest -Uri https://download.docker.com/components/engine/windows-server/20H2/docker-20.10.6.zip -OutFile docker-20.10.6.zip
Expand-Archive docker-20.10.6.zip -DestinationPath $Env:ProgramFiles
```

1. 将Docker目录添加到系统路径中：

powershell

复制代码
```
$env:Path += ";C:\Program Files\Docker"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
```

1. 安装并启动Docker服务：

powershell

复制代码
```
dockerd --register-service
Start-Service docker
```

### 4\. 验证Docker安装

1. 检查Docker版本，确保安装成功：

powershell

复制代码
```
docker version
```

1. 运行测试容器，确保Docker正常工作：

powershell

复制代码
```
docker run hello-world
```

### 5\. 设置Docker为开机自启动（可选）

1. 设置Docker服务为开机自启动：

powershell

复制代码
```
Set-Service -Name docker -StartupType Automatic
```

# 常见问题及解决方法

* **权限问题**：确保使用管理员权限运行PowerShell。
* **网络问题**：确保服务器可以访问外部网络以下载Docker和容器镜像。

## 问题1
```
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containers/Main/helpful\_tools/Install-DockerCE/install-docker-ce.ps1" -o install-docker-ce.ps1 .\\install-docker-ce.ps1
```

可以使用Microsoft提供的脚本来安装Docker CE。这是一个简化的安装方法。以下是详细步骤：

### 1\. 下载并运行安装脚本

1. 打开PowerShell，以管理员身份运行以下命令以下载安装脚本：

powershell

复制代码
```
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containers/Main/helpful_tools/Install-DockerCE/install-docker-ce.ps1" -OutFile install-docker-ce.ps1
```

1. 运行安装脚本：

powershell

复制代码
```
.\install-docker-ce.ps1
```

### 2\. 运行安装脚本后验证安装

1. 验证Docker是否成功安装：

powershell

复制代码
```
docker version
```

1. 运行一个简单的容器以确认Docker功能正常：

powershell

复制代码
```
docker run hello-world
```

### 常见问题及解决方法

1. **脚本执行策略**：  
   * 如果遇到脚本执行策略限制的问题，可以临时允许脚本运行：

powershell

复制代码
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

1. **网络问题**：  
   * 确保你的服务器可以访问互联网，以便下载Docker和所需的组件。
2. **服务启动失败**：  
   * 如果Docker服务未能启动，可以尝试手动启动服务并查看日志：

powershell

复制代码
```
Start-Service docker
Get-EventLog -LogName Application -Source Docker
```


## 问题2

```
PS C:\\Windows\\system32> Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containe rs/Main/helpful\_tools/Install-DockerCE/install-docker-ce.ps1" -o install-docker-ce.ps1 PS C:\\Windows\\system32> .\\install-docker-ce.ps1 Querying status of Windows feature: Containers... Enabling feature Containers... 警告: 必须重新启动此服务器才能完成安装过程。 Restart is required; restarting now... Creating scheduled task action (C:\\Windows\\system32\\install-docker-ce.ps1 )... Creating scheduled task trigger... Registering script to re-run at next user logon... Restart-Computer : 无法重新启动计算机 WIN-IGD6VS6HTO6，并显示以下错误消息: 无法启动系统关机，因为有其他用户登录到计算机 。。 所在位置 C:\\Windows\\system32\\install-docker-ce.ps1:167 字符: 13 + Restart-Computer + \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~ + CategoryInfo : OperationStopped: (WIN-IGD6VS6HTO6:String) \[Restart-Computer\], InvalidOperationException + FullyQualifiedErrorId : RestartcomputerFailed,Microsoft.PowerShell.Commands.RestartComputerCommand
```

### 
由于脚本需要重启计算机并在重启后继续执行，但当前计算机上有其他用户登录，导致无法自动重启。你可以手动重启计算机，然后再次运行安装脚本。以下是详细步骤：

### 1\. 手动重启计算机

1. 先保存好当前工作，然后手动重启计算机。

### 2\. 重启后重新运行脚本

1. 重启后，重新以管理员身份打开PowerShell，然后再次运行安装脚本：

powershell

复制代码
```
.\install-docker-ce.ps1
```

### 3\. 验证Docker安装

1. 验证Docker是否成功安装：

powershell

复制代码
```
docker version
```

1. 运行一个简单的容器以确认Docker功能正常：

powershell

复制代码
```
docker run hello-world
```

## 问题3

```
PS C:\\Windows\\system32> .\\install-docker-ce.ps1 Querying status of Windows feature: Containers... Feature Containers is already enabled. DOCKER default Checking Docker versions C:\\Windows\\system32\\install-docker-ce.ps1 : 无法连接到远程服务器 所在位置 行:1 字符: 1 + .\\install-docker-ce.ps1 + \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~ + CategoryInfo : NotSpecified: (:) \[Write-Error\], WriteErrorException + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException,install-docker-ce.ps1
```

看起来脚本在检查Docker版本时无法连接到远程服务器。这可能是由于网络连接问题、DNS问题或防火墙阻止访问Docker下载服务器导致的。你可以尝试以下几种解决方法：

### 方法一：检查网络连接

1. **检查互联网连接**：  
   * 确保你的服务器可以访问互联网。尝试在PowerShell中运行以下命令，确认可以访问外部网站：

powershell

复制代码
```
Invoke-WebRequest -UseBasicParsing "https://www.google.com"
```

1. **检查DNS解析**：  
   * 确保DNS解析正常。尝试在PowerShell中运行以下命令，确认DNS解析正常：

powershell

复制代码
```
nslookup www.google.com
```

### 方法二：手动下载Docker

1. **手动下载Docker二进制文件**：  
   * 如果无法通过脚本自动下载Docker，可以手动下载Docker二进制文件。  
   * 访问Docker官网下载最新的Docker二进制文件。
2. **解压并配置Docker**：  
   * 将下载的压缩包解压到适当的位置，例如 `C:\Program Files\Docker`。
3. **配置环境变量**：  
   * 将Docker目录添加到系统路径中：

powershell

复制代码
```
$env:Path += ";C:\Program Files\Docker"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
```

1. **安装并启动Docker服务**：

powershell

复制代码
```
dockerd --register-service
Start-Service docker
```

### 方法三：使用离线安装包

1. **下载离线安装包**：  
   * 从Docker官网或其他可信来源下载Docker的离线安装包。
2. **安装Docker**：  
   * 根据下载的离线安装包中的说明进行安装。

### 方法四：检查防火墙和代理设置

1. **检查防火墙设置**：  
   * 确保防火墙没有阻止PowerShell或HTTP流量。
2. **检查代理设置**：  
   * 如果你的网络使用代理，请确保在PowerShell中配置代理设置：

powershell

复制代码
```
[system.net.webrequest]::defaultwebproxy = New-Object system.net.webproxy('http://问题r-proxy-url:port')
[system.net.webrequest]::defaultwebproxy.credentials = [System.Net.CredentialCache]::DefaultCredentials
```