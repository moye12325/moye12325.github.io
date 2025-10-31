---
date: 2024-07-22T18:03:24.251Z
updated: null
title: windows server2019搭建sftp
slug: '547346582876005'
oid: 669e9eec2a6fe84dfe920b24
categories: 所遇问题
type: post
permalink: /posts/所遇问题/547346582876005
---


# windows server搭建sftp 并使用xftp传输文件

在Windows Server上搭建SFTP服务器并使用Xftp传输文件的步骤如下：

### 1\. 安装OpenSSH服务器

1. **启用OpenSSH服务器功能**：  
   * 打开PowerShell，以管理员身份运行以下命令以启用OpenSSH服务器功能：  
powershell  
复制代码  
`Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0  
`
2. **启动并配置OpenSSH服务**：  
   * 启动OpenSSH服务器服务：  
powershell  
复制代码  
`Start-Service sshd  
`  
   * 设置OpenSSH服务器服务为开机自启动：  
powershell  
复制代码  
`Set-Service -Name sshd -StartupType 'Automatic'  
`
3. **检查防火墙配置**：  
   * 确保防火墙允许SSH流量。打开Windows防火墙并添加允许端口22的规则：  
powershell  
复制代码  
`New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22  
```

### 2\. 配置SFTP根目录

1. **创建SFTP用户**：  
   * 创建一个用于SFTP的本地用户。例如：  
powershell  
复制代码  
`net user sftpuser MyPassword /add  
`
2. **配置SFTP根目录**：  
   * 创建SFTP根目录并设置相应权限。例如：  
powershell  
复制代码  
`mkdir C:\SFTP-Root  
icacls C:\SFTP-Root /grant "sftpuser:F"  
`
3. **修改OpenSSH配置**：  
   * 打开并编辑 `sshd_config` 文件，通常位于 `C:\ProgramData\ssh\sshd_config`。添加以下配置以限制用户只访问特定目录：  
text  
复制代码  
`Subsystem sftp internal-sftp  
Match User sftpuser  
  ChrootDirectory C:\SFTP-Root  
  ForceCommand internal-sftp  
  AllowTcpForwarding no  
  PermitTunnel no  
  X11Forwarding no  
`
4. **重启SSH服务**：  
powershell  
复制代码  
`Restart-Service sshd  
```

### 3\. 使用Xftp连接SFTP服务器

1. **下载并安装Xftp**：  
   * 从官方站点下载并安装Xftp。
2. **配置Xftp连接**：  
   * 打开Xftp，点击“新建会话”。  
   * 配置会话参数：  
         * 主机名：输入服务器的IP地址或主机名。  
         * 协议：选择SFTP。  
         * 端口：22。  
         * 用户名：输入之前创建的 `sftpuser`。  
         * 密码：输入 `sftpuser` 的密码。
3. **连接并传输文件**：  
   * 保存并连接会话。  
   * 成功连接后，可以在Xftp中浏览和传输文件。

### 常见问题及解决方法

* **无法连接**：确保防火墙规则正确配置，并且OpenSSH服务正在运行。
* **权限问题**：确保用户具有适当的目录权限，并且目录路径正确配置在 `sshd_config` 中。

## 解释net user sftpuser MyPassword /add

命令 `net user sftpuser MyPassword /add` 是一个用于管理Windows操作系统中用户账户的命令。以下是对该命令的详细解释：

### 语法解析

* `net user`：这是一个Windows命令行工具，用于创建和修改用户账户，或显示用户账户的信息。
* `sftpuser`：这是你要创建的新用户的用户名。在这个例子中，用户名是 `sftpuser`。你可以根据需要更改为其他名字。
* `MyPassword`：这是你为新用户设置的密码。在这个例子中，密码是 `MyPassword`。你应该使用一个强密码来确保账户安全。
* `/add`：这个选项表示要添加一个新用户账户。

### 详细说明

* **创建用户**：该命令创建一个名为 `sftpuser` 的新用户账户。
* **设置密码**：该命令同时为这个新用户账户设置密码为 `MyPassword`。
* **添加到系统**：`/add` 选项表示将这个新用户账户添加到本地计算机的用户账户列表中。

### 使用示例

假设你在Windows Server上执行以下命令：

cmd

复制代码
```
net user sftpuser MySecurePassword123! /add
```

该命令会执行以下操作：

1. **创建一个新用户账户**：系统会创建一个名为 `sftpuser` 的新用户。
2. **设置密码**：新用户的密码被设置为 `MySecurePassword123!`。
3. **添加到本地系统**：新用户账户被添加到本地计算机的用户账户列表中。

### 注意事项

* **权限**：运行此命令需要管理员权限。因此，你需要在具有管理员权限的命令提示符或PowerShell中运行该命令。
* **安全性**：确保密码足够强壮，避免使用容易被猜到的密码。
* **用户管理**：你可以使用 `net user` 命令查看和管理已创建的用户账户。例如，运行 `net user` 可以列出所有用户，运行 `net user sftpuser` 可以查看 `sftpuser` 的详细信息。

## 设置好了用户名与密码，还可以访问其他盘


### 1\. 设置文件夹权限

你需要为用户 `sftpuser` 设置其他盘符上的文件夹权限。假设你希望用户访问D盘。

1. **打开文件资源管理器**：  
   * 导航到要授予访问权限的驱动器或文件夹，例如D盘。
2. **右键点击文件夹**：  
   * 选择“属性”。
3. **设置安全权限**：  
   * 转到“安全”选项卡。  
   * 点击“编辑”，然后点击“添加”。  
   * 在弹出的窗口中，输入 `sftpuser`，然后点击“检查名称”进行验证。  
   * 确认后，点击“确定”。  
   * 在权限设置中，勾选 `sftpuser` 所需的权限，例如“读取”、“写入”等。  
   * 点击“应用”，然后点击“确定”。

### 2\. 配置OpenSSH以允许访问其他盘符

如果你正在使用OpenSSH配置SFTP服务器，需要确保 `sftpuser` 的根目录配置正确，并允许用户访问其他盘符。以下是步骤：

1. **打开并编辑sshd\_config文件**：  
   * `sshd_config` 文件通常位于 `C:\ProgramData\ssh\sshd_config`。你可以用文本编辑器打开它，例如记事本。
2. **修改ChrootDirectory配置**：  
   * 确保 `Match User sftpuser` 部分允许访问你指定的目录。例如：  
```
Subsystem sftp internal-sftp  
Match User sftpuser  
  ChrootDirectory C:\  
  ForceCommand internal-sftp  
  AllowTcpForwarding no  
  PermitTunnel no  
  X11Forwarding no  
```

3. **允许用户访问其他盘符**：  
   * 如果你希望用户能访问D盘，确保目录结构合理，并在 `sshd_config` 中配置相应的权限：  

```
Match User sftpuser  
  ChrootDirectory C:\  
  ForceCommand internal-sftp  
  AllowTcpForwarding no  
  PermitTunnel no  
  X11Forwarding no  
```
4. **创建符号链接（可选）**：  
   * 在用户根目录下创建指向其他盘符的符号链接。例如，你可以在 `C:\SFTP-Root` 下创建一个指向D盘的符号链接：  

```
mklink /D C:\SFTP-Root\D-drive D:\  
```


### 3\. 重启SSH服务

完成配置更改后，需要重启SSH服务：

```
Restart-Service sshd
```

### 4\. 验证配置

使用SFTP客户端（如Xftp）登录，确保用户可以访问并操作所需的盘符和文件夹。

### 注意事项

* **权限设置**：确保给定目录及其父目录具有适当的权限，并且用户有权访问这些目录。
* **安全性**：确保仅授予必要的权限，避免不必要的安全风险。
* **配置检查**：每次修改 `sshd_config` 文件后，检查配置语法和功能，以确保不会破坏服务的正常运行。