---
date: 2024-07-22T18:04:39.671Z
updated: null
title: Windows Server安装Docker Compose
slug: '679870432655658776954'
oid: 669e9f372a6fe84dfe920b8d
categories: 所遇问题
type: post
permalink: /posts/所遇问题/679870432655658776954
---


# Windows Server安装Docker Compose

要在Windows Server上使用Docker Compose，首先需要安装Docker Compose工具。以下是安装和使用Docker Compose的步骤：

### 1\. 下载Docker Compose

1. 打开PowerShell，以管理员身份运行以下命令下载Docker Compose的最新版本：

```
Invoke-WebRequest "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Windows-x86_64.exe" -OutFile "$Env:ProgramFiles\docker\docker-compose.exe"
```

### 2\. 添加Docker Compose到系统路径

1. 确保Docker Compose可执行文件位于系统路径中。通常，下载到`$Env:ProgramFiles\docker`目录已经包含在系统路径中。如果不确定，可以手动添加。

### 3\. 验证安装

1. 在PowerShell中运行以下命令验证Docker Compose是否成功安装：

```
docker-compose --version
```

### 4\. 使用Docker Compose

1. 创建一个`docker-compose.yml`文件。例如，以下是一个简单的`docker-compose.yml`示例：

```
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
```

1. 在包含`docker-compose.yml`文件的目录中，运行以下命令启动服务：

```
docker-compose up -d
```

### 5\. 管理Docker Compose服务

1. 停止服务：

```
docker-compose down
```

1. 查看服务状态：

```
docker-compose ps
```

## 问题
```
PS C:\\Windows\\system32> Invoke-WebRequest "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Windows-x86\_64.exe" -OutFile "$Env:ProgramFiles\\docker\\docker-compose.exe" Invoke-WebRequest : 未能找到路径“C:\\Program Files\\docker\\docker-compose.exe”的一部分。 所在位置 行:1 字符: 1 + Invoke-WebRequest "https://github.com/docker/compose/releases/downloa ... + \~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~\~ + CategoryInfo : NotSpecified: (:) \[Invoke-WebRequest\], DirectoryNotFoundException + FullyQualifiedErrorId : System.IO.DirectoryNotFoundException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand
```
 `C:\Program Files\docker` 目录不存在。你需要先创建该目录，然后再下载 `docker-compose.exe`。以下是修正后的步骤：

### 1\. 创建目录

1. 打开PowerShell，以管理员身份运行以下命令创建 `docker` 目录：

```
New-Item -Path "$Env:ProgramFiles\docker" -ItemType Directory -Force
```

### 2\. 下载Docker Compose

1. 运行以下命令下载Docker Compose到新创建的目录：

```
Invoke-WebRequest "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Windows-x86_64.exe" -OutFile "$Env:ProgramFiles\docker\docker-compose.exe"
```

### 3\. 添加Docker Compose到系统路径（可选）

1. 确保Docker Compose可执行文件位于系统路径中。你可以手动添加，也可以通过PowerShell脚本自动添加。下面是自动添加的脚本：

```
$env:Path += ";$Env:ProgramFiles\docker"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
```

### 4\. 验证安装

1. 在PowerShell中运行以下命令验证Docker Compose是否成功安装：

```
docker-compose --version
```

### 5\. 使用Docker Compose

1. 创建一个`docker-compose.yml`文件。例如，以下是一个简单的`docker-compose.yml`示例：

```
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
```

1. 在包含`docker-compose.yml`文件的目录中，运行以下命令启动服务：

```
docker-compose up -d
```

### 6\. 管理Docker Compose服务

1. 停止服务：

```
docker-compose down
```

1. 查看服务状态：

```
docker-compose ps
```