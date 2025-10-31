---
date: 2025-05-08T01:17:25.250Z
updated: 2025-10-30T08:03:08.392Z
title: ZeroMQ实践
slug: zeromq-practice
oid: 681c062581920129eb679d3d
categories: Python
type: post
permalink: /posts/Python/zeromq-practice
---


## ZeroMQ实践


[ZeroMQ](https://zeromq.org/get-started/?language=python&library=pyzmq#)，是一个**高性能的异步消息库**或**并发框架**。将复杂的底层网络通信细节抽象化，提供了一系列灵活的消息模式，让构建复杂的分布式应用变得更简单。

### ZeroMQ 的核心理念：模式、抽象与性能

与传统的中心化消息 Broker 不同，ZeroMQ 倡导一种更加**去中心化 (brokerless)** 或**分布式**的设计理念（当然，也可以基于它构建 Broker）。它的核心优势在于：

1. **消息模式 (Messaging Patterns):** ZeroMQ 没有让用户直接操作原始的 Socket 去头疼连接、发送、接收、错误处理、重试等细节。相反，它提供了几种经典的、开箱即用的消息模式。每种模式都内置了特定的通信逻辑和扩展性能力，只需要选择适合场景的模式即可。
    
    - **请求/应答 (REQ/REP):** 经典的客户端/服务器模式。REQ 发送请求，REP 接收请求并回应答。简单直观。
    - **发布/订阅 (PUB/SUB):** 一种数据分发模式。PUB 向某个主题发布消息，多个 SUB 订阅感兴趣的主题并接收消息。实现一对多广播。
    - **推/拉 (PUSH/PULL):** 一种工作分发和收集模式。PUSH 将任务推给多个 PULL Worker，PULL Worker 拉取任务执行。实现多对多负载均衡和结果收集。
    - **成对 (PAIR):** 最简单的点对点模式。没有内置模式逻辑，通常用于固定的一对一连接。 这些模式是 ZeroMQ 的精髓，它们提供了比原始 Socket 高得多的抽象级别。
    
2. **Socket 的增强 (Sockets on Steroids):** ZeroMQ 的 Socket 和传统的 Socket 不是一回事。它们是模式的端点。用户不需要关心底层的连接建立、断开、消息队列管理、错误处理等，ZeroMQ 在内部帮你搞定了。只需要 `bind` 或 `connect` 到指定的地址，然后 `send` 或 `recv` 消息。
    
3. **高性能与可伸缩性：** ZeroMQ 设计之初就考虑了性能。使用异步 I/O，智能的消息批处理和路由，避免许多传统消息队列的瓶颈。其去中心化的特性也意味着没有中心 Broker 的单点压力和故障风险（除非选择构建 Broker）。
    

### ZeroMQ 的核心组件：Context、Socket、Poller

1. **Context (上下文):**
    
    -  ZeroMQ 运行时环境的**管理者**，负责资源的分配和管理，包括底层的 I/O 线程。
    - 可以将 Context 理解为 ZeroMQ 的**工厂**，所有的 Socket 都必须通过 Context 来创建 (`context.socket(...)`)。
    - 通常一个应用或一个线程只需要创建一个 Context。
2. **Socket (套接字):**
    
    -  ZeroMQ 中进行消息传输的**主要对象**。
    - 每个 Socket 都有一个特定的**类型**（如 `zmq.REQ`, `zmq.PUB` 等），这个类型决定 Socket 遵循哪种消息模式。
    - Socket 可以**绑定 (bind)** 到一个地址（通常是服务器端），监听连接。
    - Socket 可以**连接 (connect)** 到一个地址（通常是客户端），发起连接。
    - 通过 `send()` 和 `recv()` 方法来发送和接收消息。ZeroMQ 的消息是**字节串 (bytes)**，`send_string()`/`recv_string()` 提供方便的字符串处理。消息可以由多个帧组成 (`send_multipart()`/`recv_multipart()`)。
    - **注意：** 默认情况下，`socket.send()` 和 `socket.recv()` 是**阻塞的**。如果缓冲区满或没有消息，它们会暂停当前线程的执行。
3. **Poller (轮询器):**
    
    - 在传统的**同步 (阻塞)** ZeroMQ 编程中，如果需要**同时**监听多个 Socket 的消息，直接在一个 Socket 上调用 `recv()` 会阻塞住，则无法处理其他 Socket 的消息。
    - `zmq.Poller` 就是用来解决这个问题的。可以向 Poller **注册**多个关心的 Socket 和事件（比如 `zmq.POLLIN` 表示有消息可读）。
    - 然后调用 `poller.poll(timeout)` 方法。这个方法会**阻塞**，但它同时监控所有注册的 Socket。一旦有 Socket 发生了关心的事件，`poll()` 就会返回，告知哪些 Socket 已经准备好了（比如可以调用 `recv()` 了）。
    - **重要：** 在使用异步 ZeroMQ (`zmq.asyncio`) 时，通常**不需要**直接使用 `zmq.Poller`，因为异步框架（asyncio 事件循环）会负责底层的事件监控和调度。

### ZeroMQ 的传输协议：tcp、ipc、inproc

1. **`tcp://`:**
    
    - 基于 TCP/IP 协议。
    - 用于**进程间**或**机器间**的网络通信。
    - 地址格式：`tcp://host:port` (如 `tcp://127.0.0.1:5555` 或 `tcp://*:5555`)。
2. **`ipc://`:**
    
    - 基于本地**进程间通信 (IPC)** 机制（如 Unix Domain Sockets 或 Windows 命名管道）。
    - 用于**同一机器的不同进程间**通信。
    - 通常比 `tcp://` 更快。
    - 地址格式：`ipc://pathname` (如 `ipc:///tmp/my_socket`).
3. **`inproc://`:**
    
    - 基于**进程内内存传递**。
    - **只能用于同一个操作系统进程内的不同线程或协程之间通信**。
    - 速度极快，没有网络开销。
    - **非常重要：** 一个进程中 `bind` 的 `inproc://` 地址，在其他进程中是**完全不可见且无法连接**的。
    - 地址格式：`inproc://transport_name` (如 `inproc://my_internal_channel`).


 - **代码实例**

```python
# zmq_server.py - ZeroMQ 请求应答模式的服务器端

import zmq
import time

# 1. 创建 ZeroMQ Context 对象
# Context 是 ZeroMQ 运行时环境的管理者
context = zmq.Context()

# 2. 创建一个 REP (Reply) Socket
# REP Socket 用于接收请求并发送应答
socket = context.socket(zmq.REP)

# 3. 将 Socket 绑定到一个地址
# "tcp://*:5555" 表示使用 TCP 协议，绑定到所有可用网络接口的 5555 端口
# "*" 表示绑定到所有本地地址，方便客户端连接
bind_address = "tcp://localhost:5555"
socket.bind(bind_address)

print(f"ZeroMQ REP 服务器已启动，绑定在 {bind_address}")
print("等待接收请求...")

try:
    # 服务器通常在一个无限循环中运行，不断接收和处理请求
    while True:
        # 4. 接收请求
        # socket.recv_string() 会阻塞，直到收到一个字符串消息
        message = socket.recv_string()
        print(f"收到请求: '{message}'")

        # 模拟处理请求的过程
        time.sleep(1) # 假装服务器需要处理一下

        # 5. 准备应答消息
        reply_message = f"服务器收到你的消息: '{message}'"

        # 6. 发送应答
        # socket.send_string() 会发送一个字符串应答
        # 在 REP-REQ 模式中，REP Socket 必须在发送应答前先接收一个请求
        socket.send_string(reply_message)
        print(f"发送应答: '{reply_message}'")

except KeyboardInterrupt:
    print("\n检测到 Ctrl+C，正在关闭服务器...")
finally:
    # 清理 ZeroMQ 资源
    socket.close()
    context.term()
    print("服务器已安全关闭。")
```

```python
# zmq_client.py - ZeroMQ 请求应答模式的客户端

import zmq

# 1. 创建 ZeroMQ Context 对象
context = zmq.Context()

# 2. 创建一个 REQ (Request) Socket
# REQ Socket 用于发送请求并接收应答
socket = context.socket(zmq.REQ)

# 3. 连接到服务器的地址
# "tcp://localhost:5555" 表示使用 TCP 协议，连接到本地的 5555 端口
# 如果服务器在另一台机器上，请将 'localhost' 替换为服务器的实际 IP 地址
connect_address = "tcp://localhost:5555"
socket.connect(connect_address)

print(f"ZeroMQ REQ 客户端已启动，连接到 {connect_address}")
print("你可以输入消息发送给服务器，输入 'quit' 退出。")

try:
    # 客户端通常在一个循环中运行，允许发送多条消息
    while True:
        # 获取用户输入
        user_input = input("请输入消息: ")

        # 检查是否输入 'quit'
        if user_input.lower() == 'quit':
            break

        # 4. 发送请求
        # socket.send_string() 会发送用户输入的字符串消息
        # 在 REQ-REP 模式中，REQ Socket 必须在发送请求后等待一个应答，不能连续发送请求
        print(f"发送请求: '{user_input}'")
        socket.send_string(user_input)

        # 5. 接收应答
        # socket.recv_string() 会阻塞，直到收到服务器的应答消息
        reply_message = socket.recv_string()
        print(f"收到应答: '{reply_message}'")
        print("-" * 20) # 分隔线

except KeyboardInterrupt:
    print("\n检测到 Ctrl+C，正在关闭客户端...")
finally:
    # 清理 ZeroMQ 资源
    socket.close()
    context.term()
    print("客户端已安全关闭。")
```

![image.png|700x453](https://qiniu.kanes.top/blog/20250506201630375.png)



---

### 异步：zmq.asyncio

默认的 ZeroMQ Socket 是阻塞的。如果Python 应用是基于 `asyncio` 构建的，那么在一个协程中调用阻塞的 `socket.recv()` 或 `socket.send()` 会**暂停整个事件循环**，导致其他所有协程都无法运行，异步的优势荡然无存。

`zmq.asyncio` 子模块就是为了解决这个问题而生的。它提供了 ZeroMQ Socket 的异步版本，其 `send()` 和 `recv()` 方法变成了**可等待的 (awaitable)**。

**使用 `zmq.asyncio`：**

1. 导入 `zmq.asyncio`，通常取别名 `azmq`：`import zmq.asyncio as azmq`。
2. 创建异步 Context：`context = azmq.Context()`。这个 Context 会自动感知并集成当前的 `asyncio` 事件循环。
3. 创建的 Socket：`socket = context.socket(socket_type)`。从这个 Context 创建的 Socket 具有异步特性。
4. 在协程中使用 `await` 调用异步 Socket 方法：`await socket.send(...)`, `await socket.recv(...)`。
5. 当一个协程 `await` 一个异步 Socket 操作时，如果该操作不能立即完成（比如没有收到消息），当前协程会**暂停**并**让出控制权**给 `asyncio` 事件循环，允许事件循环去执行其他准备好的协程。当 Socket 操作完成后，事件循环会通知并恢复该协程。

**异步 (Asyncio) Socket 示例 (简版 inproc 通信):**

```python
# inproc_asyncio_example.py - 在同一个进程内使用 inproc:// 传输协议

import asyncio
import zmq
import zmq.asyncio as azmq # 使用异步版本

# 定义 inproc 地址
INPROC_ADDRESS = "inproc://my_async_channel"

# 异步 REP Worker 协程 (运行在同一个进程内)
async def async_rep_worker(context: azmq.Context):
    # 从传入的异步 Context 创建 REP Socket
    socket = context.socket(zmq.REP)
    # 绑定到 inproc 地址
    socket.bind(INPROC_ADDRESS)
    print(f"REP Worker (进程内) 已启动，绑定到 {INPROC_ADDRESS}")

    try:
        while True:
            # 异步接收请求
            message = await socket.recv_string()
            print(f"REP Worker (进程内) 收到请求: '{message}'")

            # 模拟处理
            await asyncio.sleep(0.5)

            reply = f"REP Worker (进程内) 收到并处理了: '{message}'"
            # 异步发送应答
            await socket.send_string(reply)
            print(f"REP Worker (进程内) 发送应答: '{reply}'")

    except asyncio.CancelledError:
        print("\nREP Worker (进程内) 被取消，正在退出...")
    finally:
        socket.close()
        print("REP Worker (进程内) Socket 已关闭。")


# 异步 REQ Client 协程 (运行在同一个进程内)
async def async_req_client(context: azmq.Context):
     # 从传入的异步 Context 创建 REQ Socket
    socket = context.socket(zmq.REQ)
    # 连接到 inproc 地址 (注意：这个地址必须在同一个进程内已经被某个 socket 绑定了)
    socket.connect(INPROC_ADDRESS)
    print(f"REQ Client (进程内) 已启动，连接到 {INPROC_ADDRESS}")

    try:
        for i in range(3):
            request = f"进程内请求 {i+1}"
            print(f"REQ Client (进程内) 发送请求: '{request}'")
            # 异步发送请求
            await socket.send_string(request)

            # 异步接收应答
            reply = await socket.recv_string()
            print(f"REQ Client (进程内) 收到应答: '{reply}'")
            await asyncio.sleep(0.1) # 稍微等一下再发下一个请求
            
    finally:
        socket.close()
        print("REQ Client (进程内) Socket 已关闭。")

# 主异步函数，启动和管理 Worker 和 Client 协程
async def main():
    # 在主函数中创建唯一一个异步 Context
    # 这个 Context 将用于创建所有需要通过 inproc 通信的 Socket
    context = azmq.Context()
    print("主程序: Asyncio Context 已创建")

    # 使用 asyncio.create_task 启动 Worker 和 Client 协程
    # 它们将在同一个事件循环、同一个进程内并发运行
    worker_task = asyncio.create_task(async_rep_worker(context))
    client_task = asyncio.create_task(async_req_client(context))

    # 等待 Client 任务完成它的请求
    await client_task
    print("主程序: Client 任务完成。")

    # Client 任务完成后，取消 Worker 任务以退出
    worker_task.cancel()
    try:
        await worker_task # 等待 Worker 任务响应取消信号
    except asyncio.CancelledError:
        print("主程序: Worker 任务已被取消。")

    # Context 的清理通常由 asyncio.run() 负责，或者可以手动 context.term()
    # context.term() # 如果手动管理循环，需要 term

# 程序的入口点
if __name__ == "__main__":
    print("--- 进程内 ZeroMQ (inproc) 示例启动 ---")
    # 使用 asyncio.run 运行主异步函数
    # 这将启动事件循环，并在同一个进程中调度 worker_task 和 client_task
    asyncio.run(main())
    print("--- 进程内 ZeroMQ (inproc) 示例结束 ---")
```


![image.png|0x0](https://qiniu.kanes.top/blog/20250506202007962.png)



### ZeroMQ 的适用场景

- **构建微服务之间的通信：** 提供灵活的消息路由和高效传输。
- **分布式任务队列：** 使用 PUSH/PULL 模式分发任务给 Worker 集群。
- **数据发布与订阅系统：** 使用 PUB/SUB 模式高效广播数据给多个消费者。
- **高性能的数据管道：** 在不同应用组件间快速传递大量消息。
- **替代复杂的原始 Socket 编程：** 当需要多对多、一对多等复杂通信拓扑时，ZMQ 的模式能大大简化代码。
- **需要高性能但又不想引入重量级 Broker 的场景。**