---
title: RabbitMQ知识总结
date: '2024-10-29 18:15:28'
updated: '2024-10-29 18:16:06'
categories:
  - Java
tags:
  - Java
summary: >
  RabbitMQ 是一个基于 AMQP（Advanced Message Queuing
  Protocol）的消息队列系统，支持高并发、可扩展，并提供多种客户端和协议支持。其核心概念包括生产者、消费者，交换器、队列和绑定。消息通过交换器路由到队列，保证了消息传输和处理的可靠性。RabbitMQ的工作模式包括简单模式、工作模式、发布订阅模式、路由模式和主题模式。消息传输使用信道来传输数据，并通过事务机制和Confirm机制保证消息的可靠性。高可用性方面，RabbitMQ提供普通集群模式和镜像集群模式。为解决延时和过期失效问题，可以设置消息的TTL和采用批量重导的方式补充丢失的数据。
---
## 安装RabbitMQ之后，执行了rabbitmq-plugins enable rabbitmq_management，却仍然打不开管理端界面http://localhost:15672

执行了 `rabbitmq-plugins enable rabbitmq_management` 命令后，仍然无法打开 RabbitMQ 管理端界面，可能是由于以下几个原因造成的：

1. **RabbitMQ 服务未启动**：确保 RabbitMQ 服务正在运行。可以通过以下命令检查 RabbitMQ 服务的状态：
   ```sh
   sudo systemctl status rabbitmq-server
   ```
   如果服务未启动，可以通过以下命令启动服务：
   ```sh
   sudo systemctl start rabbitmq-server
   ```

2. **防火墙问题**：确保防火墙没有阻止端口 15672。可以临时关闭防火墙以排除这一问题：
   ```sh
   sudo ufw disable
   ```
   或者添加规则允许端口 15672：
   ```sh
   sudo ufw allow 15672
   ```

3. **监听地址问题**：RabbitMQ 默认监听所有接口地址。如果您的 RabbitMQ 配置文件 `rabbitmq.config` 中指定了不同的监听地址，可能需要修改为 `0.0.0.0` 或您的本地 IP 地址。配置文件通常位于 `/etc/rabbitmq/rabbitmq.config`。

4. **插件是否正确启用**：确保插件正确启用，可以通过以下命令列出已启用的插件：
   ```sh
   rabbitmq-plugins list
   ```
   确认 `rabbitmq_management` 插件在已启用插件列表中。

5. **查看日志**：检查 RabbitMQ 的日志文件以获取更多信息。日志文件通常位于 `/var/log/rabbitmq/` 目录下，可以查看 `rabbit@<hostname>.log` 和 `rabbit@<hostname>-sasl.log` 文件中的内容。

6. **重新启用插件**：尝试禁用并重新启用 `rabbitmq_management` 插件：
   ```sh
   rabbitmq-plugins disable rabbitmq_management
   rabbitmq-plugins enable rabbitmq_management
   ```

如果以上步骤仍未解决问题，请提供更多的错误信息或日志内容以便进一步诊断。

## 系统是windows

在 Windows 上安装 RabbitMQ 并启用管理插件后，如果无法访问管理界面 http://localhost:15672，请按以下步骤进行故障排除：

1. **确保 RabbitMQ 服务已启动**：
   - 打开任务管理器，查看 RabbitMQ 服务是否正在运行。
   - 或者在命令提示符中输入以下命令查看服务状态：
     ```sh
     net start | find "RabbitMQ"
     ```
   - 如果服务未启动，可以手动启动服务：
     ```sh
     net start RabbitMQ
     ```

2. **确认管理插件已启用**：
   - 在命令提示符中输入以下命令查看已启用的插件：
     ```sh
     rabbitmq-plugins list
     ```
   - 确认 `rabbitmq_management` 插件在启用的插件列表中。如果未启用，请启用它：
     ```sh
     rabbitmq-plugins enable rabbitmq_management
     ```

3. **检查端口占用情况**：
   - 确保端口 15672 未被其他程序占用。可以使用以下命令查看端口占用情况：
     ```sh
     netstat -aon | findstr :15672
     ```
   - 如果发现端口被其他程序占用，需要停止该程序或更改 RabbitMQ 管理插件的端口。

4. **防火墙设置**：
   - 确保 Windows 防火墙没有阻止端口 15672。可以临时关闭防火墙以排除这一问题：
     ```sh
     netsh advfirewall set allprofiles state off
     ```
   - 或者在防火墙设置中添加入站规则，允许端口 15672。

5. **检查 RabbitMQ 日志**：
   - 查看 RabbitMQ 的日志文件以获取更多信息。默认情况下，日志文件位于 `%APPDATA%\RabbitMQ\log` 目录下。检查 `rabbit@<hostname>.log` 和 `rabbit@<hostname>-sasl.log` 文件中的内容。

6. **重新启用管理插件**：
   - 尝试禁用并重新启用 `rabbitmq_management` 插件：
     ```sh
     rabbitmq-plugins disable rabbitmq_management
     rabbitmq-plugins enable rabbitmq_management
     ```

7. **检查配置文件**：
   - 检查 RabbitMQ 的配置文件 `rabbitmq.config` 中是否有任何与管理插件相关的设置。如果配置文件中指定了监听地址，确保它包含 `0.0.0.0` 或本地 IP 地址。

如果以上步骤仍未解决问题，请提供更多的错误信息或日志内容以便进一步诊断。

在 RabbitMQ 中，插件列表中的状态标记解释如下：

- `[ ]` 表示插件未启用。
- `[e]` 表示插件是其他插件依赖的，并已隐式启用。
- `[E]` 表示插件已显式启用。

在你的情况下：

- `[E] rabbitmq_management` 表示 `rabbitmq_management` 插件已显式启用。
- `[e] rabbitmq_management_agent` 表示 `rabbitmq_management_agent` 插件是 `rabbitmq_management` 插件依赖的，因此已隐式启用。
- `[e] rabbitmq_web_dispatch` 表示 `rabbitmq_web_dispatch` 插件也是 `rabbitmq_management` 插件依赖的，因此已隐式启用。

尽管这些插件已启用，你仍然无法访问管理界面。接下来，可以尝试以下步骤进行进一步的故障排除：

### 1. 确认 RabbitMQ 服务已启动
确保 RabbitMQ 服务正在运行：
1. 打开命令提示符（以管理员身份运行）。
2. 输入以下命令检查 RabbitMQ 服务状态：
   ```sh
   net start | find "RabbitMQ"
   ```
   确保 RabbitMQ 服务在运行。如果未运行，可以手动启动服务：
   ```sh
   net start RabbitMQ
   ```

### 2. 检查端口占用情况
确保端口 15672 未被其他程序占用：
1. 在命令提示符中输入以下命令查看端口占用情况：
   ```sh
   netstat -aon | findstr :15672
   ```
2. 如果发现端口被其他程序占用，需要停止该程序或更改 RabbitMQ 管理插件的端口。

### 3. 查看 RabbitMQ 日志
检查 RabbitMQ 的日志文件以获取更多信息。日志文件通常位于 `%APPDATA%\RabbitMQ\log` 目录下。查看 `rabbit@<hostname>.log` 和 `rabbit@<hostname>-sasl.log` 文件中的内容，看看是否有任何错误信息。

### 4. 确认 RabbitMQ 节点状态
确保 RabbitMQ 节点正在正常运行：
1. 在命令提示符中输入以下命令查看节点状态：
   ```sh
   rabbitmqctl status
   ```
   确认节点状态正常，没有错误信息。

### 5. 重新启用管理插件
尝试禁用并重新启用 `rabbitmq_management` 插件：
1. 在命令提示符中输入以下命令禁用管理插件：
   ```sh
   rabbitmq-plugins disable rabbitmq_management
   ```
2. 然后重新启用管理插件：
   ```sh
   rabbitmq-plugins enable rabbitmq_management
   ```

### 6. 检查配置文件
检查 RabbitMQ 的配置文件 `rabbitmq.config` 中是否有任何与管理插件相关的设置。确保配置文件没有错误，并且正确配置了监听地址。配置文件通常位于 RabbitMQ 安装目录的 `etc/rabbitmq` 子目录中。

通过以上步骤逐步排查问题，应该能够找出并解决 RabbitMQ 管理界面无法访问的问题。如果仍然遇到问题，请提供更多的日志信息或错误消息，以便进一步诊断。

## rabbitmqctl status
在命令提示符中运行 `rabbitmqctl status` 命令可以帮助你查看 RabbitMQ 节点的状态，并提供关于服务器的有用信息。这是你应该在命令提示符中执行的步骤：

1. 打开命令提示符（以管理员身份运行）。
2. 导航到 RabbitMQ 的 `sbin` 目录。假设 RabbitMQ 安装在 `D:\Program Files\RabbitMQ Server\rabbitmq_server-3.12.13` 目录中，输入以下命令：
   ```sh
   cd "D:\Program Files\RabbitMQ Server\rabbitmq_server-3.12.13\sbin"
   ```
3. 运行 `rabbitmqctl status` 命令：
   ```sh
   rabbitmqctl status
   ```

此命令将输出有关 RabbitMQ 节点的详细状态信息，包括版本、节点名称、启用的插件、进程 ID 等。

### 示例输出

正常情况下，你会看到类似于以下的输出：

```
Status of node rabbit@your-hostname ...
Runtime

OS PID: 12345
OS: Windows
...
Plugins
Running plugins: 
 * rabbitmq_management
 * rabbitmq_management_agent
 * rabbitmq_web_dispatch
...
```

### 可能的问题和解决方案

1. **无法联系节点**：
   - 如果你看到 `failed to contact node rabbit@your-hostname`，这通常意味着 RabbitMQ 节点未启动或网络配置有问题。
   - 确保 RabbitMQ 服务已启动：`net start RabbitMQ`
   - 确保主机名解析正确，可以尝试使用 `127.0.0.1` 或 `localhost`。

2. **节点未启动**：
   - 如果 RabbitMQ 节点未启动，可以尝试重新启动 RabbitMQ 服务：
     ```sh
     net stop RabbitMQ
     net start RabbitMQ
     ```

3. **插件未启用或配置错误**：
   - 确保 `rabbitmq_management` 插件已启用并正确配置。
   - 尝试禁用并重新启用管理插件：
     ```sh
     rabbitmq-plugins disable rabbitmq_management
     rabbitmq-plugins enable rabbitmq_management
     ```

4. **日志检查**：
   - 检查日志文件中是否有任何错误信息。日志文件通常位于 `%APPDATA%\RabbitMQ\log` 目录下。

请执行上述命令，并分享 `rabbitmqctl status` 命令的输出，以便进一步诊断和解决问题。

D:\Program Files\RabbitMQ Server\rabbitmq_server-3 Error: unable to perform an operation on node 'rab ns below. Most common reasons for this are: * Target node is unreachable (e.g. due to hostnam * CLI tool fails to authenticate with the server * Target node is not running In addition to the diagnostics info below: * See the CLI, clustering and networking guides o * Consult server logs on node rabbit@DESKTOP-QHP9 * If target node is configured to use long node n DIAGNOSTICS =========== attempted to contact: ['rabbit@DESKTOP-QHP9QTC'] rabbit@DESKTOP-QHP9QTC: * connected to epmd (port 4369) on DESKTOP-QHP9Q * epmd reports node 'rabbit' uses port 25672 for * TCP connection succeeded but Erlang distributi * suggestion: check if the Erlang cookie is iden * suggestion: check if all server nodes and CLI * suggestion: check if inter-node connections ma t * suggestion: see the CLI, clustering and netwo Current node details: * node name: 'rabbitmqcli-363-rabbit@DESKTOP-QHP9 * effective user's home directory: c:/Users/19423 * Erlang cookie hash: JS8ISKmqZdJN69PIbYuGOw==
![](https://qiniu.kanes.top/blog/RabbitMQ_image_1.png)


你的 RabbitMQ 节点存在通信问题，可能是由于 Erlang cookie 不匹配或网络配置问题。以下是一些详细的故障排除步骤：

### 1. 检查 Erlang Cookie
Erlang cookie 是用于节点间通信的安全凭证。CLI 工具和 RabbitMQ 节点需要使用相同的 cookie。

#### 检查并同步 Erlang Cookie
1. **找到 Erlang Cookie 文件位置**：
   - 默认情况下，Erlang cookie 文件位于用户的主目录下。路径通常是 `C:\Users\<username>\.erlang.cookie`。

2. **确保 CLI 和节点使用相同的 Erlang Cookie**：
   - 打开 `C:\Users\<username>\.erlang.cookie` 文件，确保文件内容一致。
   - 如果内容不一致，将 RabbitMQ 节点的 cookie 内容复制到 CLI 用户的 cookie 文件中。

#### 更改 RabbitMQ 节点的 Cookie 文件位置
1. **找到 RabbitMQ 节点的 cookie 文件**：
   - RabbitMQ 服务运行用户的 home 目录下的 `.erlang.cookie` 文件。对于 Windows 服务用户，路径通常是 `C:\Windows\System32\config\systemprofile\.erlang.cookie`。

2. **将内容同步**：
   - 确保 `C:\Windows\System32\config\systemprofile\.erlang.cookie` 文件和 `C:\Users\<username>\.erlang.cookie` 文件内容一致。

### 2. 检查主机名解析和网络配置
确保主机名解析正确并且网络配置无误。

1. **检查主机名解析**：
   - 确保主机名 `DESKTOP-QHP9QTC` 可以正确解析。可以在命令提示符中执行 `ping DESKTOP-QHP9QTC` 确认主机名解析。

2. **检查防火墙和端口**：
   - 确保防火墙没有阻止 RabbitMQ 使用的端口（4369 和 25672）。可以临时关闭防火墙以排除这一问题：
     ```sh
     netsh advfirewall set allprofiles state off
     ```

### 3. 重新启动 RabbitMQ 服务
尝试重新启动 RabbitMQ 服务以确保配置生效。

1. **停止 RabbitMQ 服务**：
   ```sh
   net stop RabbitMQ
   ```

2. **启动 RabbitMQ 服务**：
   ```sh
   net start RabbitMQ
   ```

### 4. 检查日志文件
查看 RabbitMQ 日志文件以获取更多信息。日志文件通常位于 `%APPDATA%\RabbitMQ\log` 目录下。检查 `rabbit@<hostname>.log` 和 `rabbit@<hostname>-sasl.log` 文件中的内容。

### 5. 检查配置文件
确保 RabbitMQ 的配置文件正确配置了节点名称和其他参数。配置文件通常位于 RabbitMQ 安装目录的 `etc\rabbitmq` 子目录中。

### 示例操作步骤

1. 同步 Erlang cookie：
   ```sh
   type "C:\Windows\System32\config\systemprofile\.erlang.cookie"
   type "C:\Users\<username>\.erlang.cookie"
   ```

2. 验证主机名解析：
   ```sh
   ping DESKTOP-QHP9QTC
   ```

3. 重新启动 RabbitMQ 服务：
   ```sh
   net stop RabbitMQ
   net start RabbitMQ
   ```

4. 查看日志文件：
   打开 `%APPDATA%\RabbitMQ\log` 目录下的日志文件。

执行这些步骤后，再次尝试访问 RabbitMQ 管理界面，并使用 `rabbitmqctl status` 检查节点状态。

## RabbitMQ 节点的 cookie 与 Erlang Cookie确实不一致，应该把谁的复制给谁

为了解决 Erlang cookie 不一致的问题，确保 RabbitMQ 服务用户和命令行工具使用相同的 cookie 文件。通常，我们将命令行工具用户的 cookie 复制到 RabbitMQ 服务用户的 cookie 文件中。这是因为命令行工具通常会使用当前用户的 home 目录中的 cookie，而 RabbitMQ 服务用户的 cookie 文件可能位于系统目录中。

### 步骤如下：

#### 1. 确定当前命令行工具用户的 cookie 文件
命令行工具用户的 cookie 文件通常位于：
```
C:\Users\<your-username>\.erlang.cookie
```

#### 2. 确定 RabbitMQ 服务用户的 cookie 文件
RabbitMQ 服务用户的 cookie 文件通常位于：
```
C:\Windows\System32\config\systemprofile\.erlang.cookie
```

#### 3. 将命令行工具用户的 cookie 复制到 RabbitMQ 服务用户的 cookie 文件中
1. **打开命令提示符（以管理员身份运行）**。
2. **查看命令行工具用户的 cookie 文件内容**：
   ```sh
   type "C:\Users\<your-username>\.erlang.cookie"
   ```
3. **将内容复制到 RabbitMQ 服务用户的 cookie 文件中**：
   ```sh
   copy "C:\Users\<your-username>\.erlang.cookie" "C:\Windows\System32\config\systemprofile\.erlang.cookie"
   ```

### 例子：

假设你的用户名是 `your-username`，具体步骤如下：

1. **查看命令行工具用户的 cookie 文件内容**：
   ```sh
   type "C:\Users\your-username\.erlang.cookie"
   ```
   记下显示的内容。

2. **将内容复制到 RabbitMQ 服务用户的 cookie 文件中**：
   ```sh
   copy "C:\Users\your-username\.erlang.cookie" "C:\Windows\System32\config\systemprofile\.erlang.cookie"
   ```

### 重新启动 RabbitMQ 服务

为了确保配置生效，重新启动 RabbitMQ 服务：

1. **停止 RabbitMQ 服务**：
   ```sh
   net stop RabbitMQ
   ```

2. **启动 RabbitMQ 服务**：
   ```sh
   net start RabbitMQ
   ```

### 验证

执行 `rabbitmqctl status` 命令，验证是否可以成功获取 RabbitMQ 节点的状态：

```sh
rabbitmqctl status
```

通过以上步骤，确保 Erlang cookie 一致性问题得到解决，然后再尝试访问 RabbitMQ 管理界面。
