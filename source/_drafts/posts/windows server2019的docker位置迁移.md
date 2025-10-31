---
date: 2024-07-22T18:03:52.044Z
updated: null
title: windows server2019的docker位置迁移
slug: '980943213465568354347'
oid: 669e9f082a6fe84dfe920b5a
categories: 所遇问题
type: post
permalink: /posts/所遇问题/980943213465568354347
---


# 安装好了Docker，希望docker占用e盘的空间

# 解决: 
解决

要将Docker的数据目录移动到E盘并使其使用E盘的空间，可以通过以下步骤来实现：

### 1\. 停止Docker服务

首先，确保Docker服务已停止，以便进行数据迁移和配置更改。

powershell

复制代码
```
Stop-Service docker
```

### 2\. 创建新数据目录

在E盘创建一个新的目录来存储Docker数据。例如，创建一个名为`docker`的目录：

powershell

复制代码
```
New-Item -Path "E:\docker" -ItemType Directory
```

### 3\. 复制现有数据

将现有的Docker数据从默认位置（通常是`C:\ProgramData\Docker`）复制到新位置。

powershell

复制代码
```
robocopy C:\ProgramData\Docker E:\docker /MIR
```


/MIR 选项表示镜像整个目录树，包括子目录和文件。

### 4\. 修改Docker配置

Docker的配置文件通常位于`C:\ProgramData\Docker\config\daemon.json`。如果这个文件不存在，可以创建它。

打开或创建`daemon.json`文件，并添加或修改`data-root`设置，指向新的数据目录。


```
{
    "data-root": "E:\\docker"
}
```

### 5\. 重启Docker服务

配置修改后，重启Docker服务：


```
Start-Service docker
```

### 6\. 验证配置

验证Docker是否正在使用新的数据目录，可以通过检查Docker信息来确认：


```
docker info
```

在输出中查找`Docker Root Dir`，确保它指向新的目录`E:\docker`。

### 7\. 清理旧数据（可选）

如果确认Docker已经成功迁移并正常工作，可以删除旧的Docker数据目录以释放C盘空间。


```
Remove-Item -Recurse -Force C:\ProgramData\Docker
```

通过这些步骤，你可以将Docker的数据目录从C盘迁移到E盘，从而让Docker使用E盘的空间。如果在执行过程中遇到问题或有任何疑问，请随时向我咨询。

# 问题: 
daemon.json文件内容如下，我该怎么改 { "hosts": \[ "npipe://" \] }
# 解决: 

可以在现有的 `daemon.json` 文件中添加 `"data-root"` 配置项来指定新的Docker数据目录。以下是修改后的 `daemon.json` 文件内容：

```
{
    "hosts":  [
        "npipe://"
    ],
    "data-root": "E:\\docker"
}
```

这是一个完整的示例，其中添加了 `data-root` 设置以将Docker的数据存储位置更改为E盘。

### 修改步骤

1. **打开 `daemon.json` 文件**：  
   * 文件路径通常为 `C:\ProgramData\Docker\config\daemon.json`。
2. **编辑文件**：  
   * 将文件内容修改为：

```
{
    "hosts":  [
        "npipe://"
    ],
    "data-root": "E:\\docker"
}
```

1. **保存文件并重启Docker服务**：  
   * 保存文件后，重启Docker服务以应用更改。

```
Restart-Service docker
```

### 验证更改

1. **检查Docker信息**：  
   * 运行以下命令，确认Docker正在使用新的数据目录：

```
docker info
```

1. **查看输出**：  
   * 在输出中查找 `Docker Root Dir`，确保它指向新的目录 `E:\docker`。

### 迁移数据（如果尚未完成）

如果尚未将现有的数据迁移到E盘，可以使用以下命令：

1. **停止Docker服务**：

```
Stop-Service docker
```

1. **创建新目录并复制数据**：

```
New-Item -Path "E:\docker" -ItemType Directory
robocopy C:\ProgramData\Docker E:\docker /MIR
```

1. **启动Docker服务**：

```
Start-Service docker
```