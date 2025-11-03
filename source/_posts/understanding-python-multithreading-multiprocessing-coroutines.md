---
title: 深入浅出Python多线程、多进程、协程
date: '2025-05-08 01:15:09'
updated: '2025-05-08 11:47:17'
categories:
  - Python
tags:
  - Python
summary: >
  1.  多进程 (Multiprocessing): 操作系统层面的并行。每个进程有自己独立的内存空间，进程之间互不影响。适合执行 CPU 密集型
  任务，可以充分利用多核 CPU。创建和销毁进程开销较大。 2.  多线程 (Multithreading):
  在同一个进程内创建多个执行流。线程共享进程的内存空间。适合执行 I/O 密集型 任务（如网络请求、文件读写），因为在等待 I/O 时，其他线程
---
1.  **多进程 (Multiprocessing):** 操作系统层面的并行。每个进程有自己独立的内存空间，进程之间互不影响。适合执行 **CPU 密集型** 任务，可以充分利用多核 CPU。创建和销毁进程开销较大。
2.  **多线程 (Multithreading):** 在同一个进程内创建多个执行流。线程共享进程的内存空间。适合执行 **I/O 密集型** 任务（如网络请求、文件读写），因为在等待 I/O 时，其他线程可以继续执行。但在 Python 中受 **GIL (Global Interpreter Lock)** 的限制，同一时刻只有一个线程能执行 Python 字节码，所以在 CPU 密集型任务上，多线程并不能实现真正的并行。创建和销毁线程开销比进程小。
3.  **协程 (Coroutines):** 用户空间的协作式多任务。协程是轻量级的，由程序自身控制切换，而不是由操作系统调度。它们在一个线程内执行，通过 `await` 或 `yield from` 主动让出控制权，允许其他协程运行。特别适合处理 **大量 I/O 密集型** 任务，因为切换开销非常小。协程不能利用多核 CPU 进行并行计算。
---

### 1. 多进程 (Multiprocessing)

使用 `multiprocessing` 模块。请注意，在 Windows 上运行多进程代码时，通常需要将主逻辑放在 `if __name__ == "__main__":` 块中。

```python
import multiprocessing
import time
import os

def process_task(name, duration):
    """模拟一个耗时任务"""
    print(f"进程 {name} (PID: {os.getpid()}) 开始，耗时 {duration} 秒...")
    time.sleep(duration)
    print(f"进程 {name} (PID: {os.getpid()}) 结束")

if __name__ == "__main__": # Windows 需要这个保护
    print("--- 开始多进程示例 ---")
    start_time = time.time()

    # 创建两个进程
    p1 = multiprocessing.Process(target=process_task, args=("进程A", 2))
    p2 = multiprocessing.Process(target=process_task, args=("进程B", 3))

    # 启动进程
    p1.start()
    p2.start()

    # 等待所有进程完成
    p1.join()
    p2.join()

    end_time = time.time()
    print(f"--- 多进程示例结束，总耗时: {end_time - start_time:.2f} 秒 ---")
    # 理论上，如果CPU是多核且两个任务都是CPU密集型，总耗时会接近max(2, 3)=3秒
    # 但我们这里用sleep模拟IO，所以总耗时仍然会接近max(2, 3)=3秒，但关键在于它们是并行执行的
```

**运行结果分析：**
进程A和进程B几乎同时开始，并且它们的**PID是不同**的。**总耗时接近两个任务中耗时最长的那个**。这表明它们是并行执行的，各自在独立的进程中运行。

---

### 2. 多线程 (Multithreading)

使用 `threading` 模块。线程在同一个进程内运行，共享内存。

```python
import threading
import time
import os

def thread_task(name, duration):
    """模拟一个耗时任务"""
    # 注意：这里模拟的是IO密集型任务（等待）
    print(f"线程 {name} (PID: {os.getpid()}) 开始，耗时 {duration} 秒...")
    time.sleep(duration)
    print(f"线程 {name} (PID: {os.getpid()}) 结束")

if __name__ == "__main__": # 尽管threading不强制，但习惯上也会放在这里
    print("--- 开始多线程示例 ---")
    start_time = time.time()

    # 创建两个线程
    t1 = threading.Thread(target=thread_task, args=("线程A", 2))
    t2 = threading.Thread(target=thread_task, args=("线程B", 3))

    # 启动线程
    t1.start()
    t2.start()

    # 等待所有线程完成
    t1.join()
    t2.join()

    end_time = time.time()
    print(f"--- 多线程示例结束，总耗时: {end_time - start_time:.2f} 秒 ---")
    # 因为是模拟IO（sleep会释放GIL），所以总耗时会接近max(2, 3)=3秒。
    # 如果是纯CPU计算任务，受GIL影响，总耗时会接近2+3=5秒。
```

**运行结果分析：**
线程A和线程B几乎同时开始，但它们的**PID是相同**的，因为它们**在同一个进程内**。总耗时接近两个任务中耗时最长的那个，因为 `time.sleep()` 在等待时会释放 GIL，允许其他线程运行。

---

### 3. 协程 (Coroutines) - 使用 `asyncio`

使用 `asyncio` 模块。协程是单线程的，通过事件循环 (event loop) 来调度。`await` 是关键，它表示当前协程暂停执行，将控制权交还给事件循环，允许事件循环去运行其他准备好的协程。

```python
import asyncio
import time
import os

async def async_task(name, duration):
    """模拟一个异步耗时任务"""
    # 注意：这里必须使用 await asyncio.sleep() 来模拟异步等待
    print(f"协程 {name} (PID: {os.getpid()}) 开始，耗时 {duration} 秒...")
    await asyncio.sleep(duration) # <-- 关键：协程在这里让出控制权
    print(f"协程 {name} (PID: {os.getpid()}) 结束")

async def main():
    """主协程，创建并运行其他协程"""
    print("--- 开始协程示例 ---")
    start_time = time.time()

    # 创建两个协程对象
    task1 = async_task("协程A", 2)
    task2 = async_task("协程B", 3)

    # 使用 asyncio.gather 并发运行协程，并等待它们完成
    await asyncio.gather(task1, task2)

    end_time = time.time()
    print(f"--- 协程示例结束，总耗时: {end_time - start_time:.2f} 秒 ---")
    # 总耗时接近max(2, 3)=3秒，因为它们在等待时可以切换执行。
    
if __name__ == "__main__":
    asyncio.run(main()) # 启动事件循环并运行主协程
```

**运行结果分析：**
协程A和协程B几乎同时开始，它们的**PID也是相同**的（因为它们都在同一个进程的同一个线程里运行）。总耗时接近两个任务中耗时最长的那个。这是因为当协程A执行到 `await asyncio.sleep(2)` 时，它会将控制权交给事件循环，事件循环发现协程B已经准备好运行（它也刚启动），就会切换到协程B执行。当协程B也遇到 `await asyncio.sleep(3)` 时，同样让出控制权。事件循环会等待哪个协程先完成等待，然后恢复其执行。

---

### 4. 总结与对比

| 特性           | 多进程 (multiprocessing)         | 多线程 (threading)                              | 协程 (asyncio)                                 |
| :----------- | :---------------------------- | :------------------------------------------- | :------------------------------------------- |
| **并行/并发**    | **并行** (Parallelism) - 真正利用多核 | **并发** (Concurrency) - IO密集型效率高，CPU密集型受GIL限制 | **并发** (Concurrency) - 协作式，单线程内切换            |
| **资源消耗**     | 重 (独立内存空间)                    | 轻 (共享内存空间)                                   | 最轻 (用户空间，栈开销小)                               |
| **切换方式**     | 操作系统调度 (抢占式)                  | 操作系统调度 (抢占式)                                 | 程序控制 (`await`/`yield from`) (协作式)            |
| **适用场景**     | CPU 密集型任务，需要充分利用多核            | I/O 密集型任务，简单的并发需求                            | 大量 I/O 密集型任务，高并发连接                           |
| **数据共享**     | 需要 IPC (管道、队列等)，复杂            | 共享内存，需要锁等同步机制，较复杂                            | 共享内存，通常通过参数传递或共享对象，需注意协程安全                   |
| **错误处理**     | 一个进程崩溃不影响其他进程                 | 一个线程崩溃可能导致整个进程崩溃                             | 一个协程异常通常只影响自身，但未捕获可能影响事件循环                   |
| **Python限制** | 不受 GIL 影响 (每个进程有自己的解释器)       | 受 GIL 影响 (同一时刻只有一个线程执行 Python 字节码)           | 不受 GIL 直接影响 (因为只在一个线程内)，但 CPU 密集型任务会阻塞整个事件循环 |

### 5. 协程的async await asyncio

#### 如果没写 `asyncio`、`await`、`async` 会发生什么？

`async`、`await` 和 `asyncio` 是协程协作模型的**语法糖和运行时环境**，缺一不可

1. **没写 `async def`：**
    
    - 如果您定义一个函数，但忘了写 `async def`，它就是一个普通的同步函数。
    - **后果：**
        - **无法使用 `await`：** 如果在这个函数内部使用了 `await`，Python 会直接报 `SyntaxError` 错误，因为 `await` 只能在 `async def` 函数内部使用。
        - **无法被 `await`：** 这个普通函数调用后直接返回结果（或抛出异常），它不是一个可等待对象，你不能在其他 `async def` 函数内部 `await` 它。

```python
    # 错误示例：在普通函数中使用 await
    # def blocking_function(): # 缺少 async
    #     await asyncio.sleep(1) # SyntaxError: 'await' not in async function
    #     print("这将无法运行")
```
    
2. **没写 `await`：**
    
    - 如果在一个 `async def` 函数内部，调用了一个可等待对象（比如另一个协程函数返回的对象 `Workspace_url(...)` 或 `asyncio.sleep(...)`），但**忘了写 `await`**。
    - **后果：**
        - **不会等待：** 当前协程会**立即继续执行**，不会暂停，也不会等待那个可等待对象的结果。
        - **可等待对象被忽略 (或产生警告)：** 调用 `Workspace_url(...)` 或 `asyncio.sleep(...)` 会返回一个协程对象，但因为前面没有 `await`，这个协程对象**不会被提交给事件循环调度执行**。它就像一个被创建出来但没有被使用的变量一样，静静地躺在那里，直到被垃圾回收。这通常会导致预期的异步操作根本没有发生。Python 解释器可能会发出一个运行时警告，提示你有一个协程从未被 awaited。这是 `asyncio` 编程中一个非常常见的错误来源。

    
3. **没写 `asyncio.run()` (或等效的事件循环启动代码)：**
    
    - 如果您定义了一个顶层的 `async def main()` 函数，但只是简单地调用 `main()`。
    - **后果：**
        - **异步代码不会运行：** 调用 `main()` 只会返回一个协程对象。这个协程对象包含了所有异步逻辑的代码，但它**没有被提交给任何事件循环来执行**。事件循环是异步代码运行所必需的“引擎”。没有启动事件循环并把顶层协程交给它，任何 `async def` 函数内部的代码（包括 `await` 调用）都不会被执行。

    ```Python
    async def my_app():
        print("我是一个异步应用")
        await asyncio.sleep(1)
        print("我本该运行完毕")
    
    # 错误示例：直接调用 async 函数
    # my_app() # 调用后返回一个协程对象，但不会打印任何东西
    # print("程序结束") # 这句话会立即执行
    
    # 正确做法是：
    # asyncio.run(my_app()) # 启动事件循环并运行 my_app 协程
    ```

- `async def` 标记函数是异步的，使其调用返回协程对象。
- `await` 在异步函数内部使用，标记一个暂停点，将控制权交还给事件循环，并等待一个可等待对象完成。
- `asyncio` (特别是事件循环，通过 `asyncio.run` 或其他方式启动) 是执行协程的运行时环境，它接收协程对象，调度它们的执行，并在 `await` 点之间切换。

### 6. 协程的create_task


怎么才能让多个协程**同时**开始运行，而不是一个 `await` 完再 `await` 另一个（那样是串行了）？

`asyncio.create_task()` 就是解决这个问题的关键函数之一。

#### `asyncio.create_task(coro)` 的作用

- **功能：** 将一个**协程对象** (`coro`) 包装成一个 **`Task`** 对象，并将其**安排到当前正在运行的事件循环中等待执行**。
- **返回值：** 返回一个 `asyncio.Task` 对象。

#### `Task` 是什么？

- `asyncio.Task` 是 `asyncio` 提供的核心对象之一。
- 可以被看作是**事件循环中正在运行（或已安排好要运行）的一个协程的句柄或代表**。
- `Task` 对象本身**是可等待的 (awaitable)**。可以 `await` 一个 Task 对象来等待它包装的协程完成并获取结果。
- `Task` 对象提供了检查协程状态（是否完成、是否被取消）、获取结果、获取异常或取消协程的方法。

#### `asyncio.create_task()` vs 直接 `await`

1. **直接 `await` 一个协程调用：**
    
    ```Python
    async def main():
        print("main start")
        await some_async_function() # <-- 当前 main 协程会在这里暂停，直到 some_async_function 完成
        print("main end")
    
    async def some_async_function():
        print("some_async_function start")
        await asyncio.sleep(2)
        print("some_async_function end")
    
    # 执行顺序： main start -> some_async_function start -> 等待2秒 -> some_async_function end -> main end
    # main 函数在等待 some_async_function 完成，是串行等待。
    ```
    
    直接 `await` 意味着**当前协程必须等待**被 `await` 的可等待对象完成，才能继续往下执行。
    
2. **使用 `asyncio.create_task()`：**
    
    ```Python
    async def main():
        print("main start")
        # 创建一个 Task，将 some_async_function 安排到事件循环
        task = asyncio.create_task(some_async_function())
        print("some_async_function 已安排为 Task，main 继续执行")
    
        # 此时 main 协程会立即往下执行，不会等待 task 完成
        # task 会在事件循环中与 main 并发运行
    
        # 如果 main 函数不在这里 await task，它会很快运行完毕
        # 为了确保 main 等待 task 真正完成，我们需要在某个地方 await task
        await task # <-- main 在这里等待 task 完成
        print("task 完成，main end")
    
    async def some_async_function():
        print("some_async_function start")
        await asyncio.sleep(2)
        print("some_async_function end")
    
    # 执行顺序： main start -> some_async_function 已安排... -> main 继续执行 -> (事件循环切换) some_async_function start -> (事件循环切换) main 继续执行... -> (事件循环切换) 等待2秒 -> some_async_function end -> (事件循环切换) task 完成，main end
    # main 和 task 是并发运行的。main 在调度 task 后没有立即阻塞，而是继续往下执行了。
    # 最后的 await task 确保 main 不会在 task 完成前结束。
    ```
    
    `asyncio.create_task()` 告诉事件循环：“这是另一个协程任务，把它加到你的待办列表里，在合适的时候运行它。” 调用 `create_task` 的协程**不会暂停**，它会立即返回一个 `Task` 对象，然后继续执行自己的代码。

#### `create_task()` 的典型应用场景

1. **启动“后台”任务：** 想让某个协程开始执行，但不关心何时完成，或者只是偶尔需要检查它的状态。比如，启动一个日志记录协程、一个监控协程等。
2. **需要独立管理任务时：** 可能需要获取 Task 对象来取消一个正在运行的任务 (`task.cancel()`)，或者检查它是否已经完成 (`task.done()`)，或者获取结果 (`task.result()`)。
3. **与 `asyncio.gather()` 结合使用：** `asyncio.gather()` 可以直接接受协程对象，也可以接受 Task 对象。虽然直接传协程对象更简洁，但在需要先创建 Task 对象进行一些预处理或管理时，`create_task` 就很有用。

#### `asyncio.gather()` 与 `create_task()` 的配合

用 `create_task` 启动多个协程，然后用 `asyncio.gather` 一起等待它们完成。



```Python
async def download_page(url):
    print(f"开始下载: {url}")
    await asyncio.sleep(random.randint(1, 3)) # 模拟下载时间
    print(f"下载完成: {url}")
    return f"Content of {url[:20]}..."

async def main_with_gather():
    urls = ["url1", "url2", "url3"] # 真实的 URL
    print("main_with_gather: 准备创建任务")

    # 创建 Task 列表
    tasks = []
    for url in urls:
        # 调用 download_page 返回协程对象，然后用 create_task 包成 Task
        task = asyncio.create_task(download_page(url))
        tasks.append(task)
    print("main_with_gather: 所有任务已创建")

    # await asyncio.gather 等待 tasks 列表中的所有 Task 完成
    # 在等待期间，事件循环会调度 tasks 中的协程并发运行
    results = await asyncio.gather(*tasks)
    print("main_with_gather: 所有任务已完成")

    for result in results:
        print(f"结果: {result}")

import random
if __name__ == "__main__":
    asyncio.run(main_with_gather())
```

`asyncio.create_task()` 将每个 `download_page(url)` 协程变成了可以在事件循环中独立运行的 Task。`await asyncio.gather(*tasks)` 则让 `main_with_gather` 协程暂停，直到所有这些 Task 都完成。在这段等待期间，事件循环会负责在这些 Task 之间切换执行，从而实现并发下载。

**注意：** `create_task()` 必须在**事件循环已经运行之后**调用。在使用 `asyncio.run(main())` 进入 `main` 协程时，事件循环就已经在运行了，所以可以在 `main` 或由 `main` 调用的其他协程中安全地使用 `create_task`。

#### Task 对象的一些方法

- `task.done()`: 检查 Task 是否已完成 (包括正常完成、抛出异常或被取消)。
- `task.result()`: 获取 Task 的结果。如果在 Task 完成前调用，会抛出 `InvalidStateError`；如果 Task 因异常完成，会重新抛出该异常。
- `task.exception()`: 获取 Task 完成时的异常。如果正常完成或未完成，返回 `None`。
- `task.cancel()`: 请求取消 Task。Task 内部会收到一个 `asyncio.CancelledError` 异常。Task 需要自己处理这个异常来实现优雅取消。
- `task.cancelled()`: 检查 Task 是否被取消。

### 7. 协程通用模板

```python
# 这是一个 Python 协程 (asyncio) 的通用代码模板

import asyncio
import time
import random # 导入 random 用于模拟不同任务的耗时

# =============================================================================
# 步骤 1: 定义独立的异步任务 (协程函数)
# 使用 async def 关键字定义，表示这是一个协程函数。
# 协程函数内部会使用 await 调用其他可等待对象（如异步 I/O 操作、asyncio 提供的异步工具或其它协程）。
# 这些函数通常包含实际的异步工作负载。
# =============================================================================
async def async_worker_task(task_id: int, simulate_duration: int):
    """
    定义一个异步工作任务的协程函数。

    Args:
        task_id: 任务的唯一标识符。
        simulate_duration: 模拟任务需要花费的秒数（实际是 await asyncio.sleep 的时间）。
    """
    # 任务开始时的打印，通常会看到多个任务的“开始”打印几乎同时出现
    print(f"[任务 {task_id}] 开始执行, 预计耗时 {simulate_duration} 秒...")

    # 使用 await 来执行一个异步操作。
    # asyncio.sleep() 是一个可等待对象，await 它时，当前协程会暂停，
    # 控制权会交给事件循环，事件循环可以去运行其他准备好的协程。
    # 这模拟了等待一个异步 I/O 操作（如网络响应、数据库查询结果等）的过程，期间不阻塞整个线程。
    await asyncio.sleep(simulate_duration)

    # 任务完成时的打印
    print(f"[任务 {task_id}] 执行完毕。")

    # 任务可以返回一个结果
    return f"任务 {task_id} 完成，耗时 {simulate_duration} 秒。"


# =============================================================================
# 步骤 2: 定义主异步函数 (Orchestrator / 入口)
# 这是整个异步程序的入口点，也是一个 async def 函数。
# 它负责创建、组织和调度其他的协程任务。
# 通常会在这里使用 asyncio.gather 或 asyncio.create_task 来管理多个任务的并发执行。
# =============================================================================
async def main_async_orchestrator():
    """
    主异步函数，负责创建和运行 worker 任务。
    """
    print("主协调器: 异步流程开始")
    start_time = time.time()

    # 准备一些任务的参数
    task_configurations = [
        (1, random.randint(1, 4)), # 任务1，随机耗时1-4秒
        (2, random.randint(2, 5)), # 任务2，随机耗时2-5秒
        (3, random.randint(1, 3)), # 任务3，随机耗时1-3秒
        (4, random.randint(3, 6)), # 任务4，随机耗时3-6秒
    ]

    # =========================================================================
    # 步骤 3: 创建协程对象
    # 调用 async def 函数会返回一个协程对象，此时协程内部的代码还没有开始执行。
    # =========================================================================
    # 创建一个协程对象列表
    coroutine_objects = [
        async_worker_task(task_id, duration)
        for task_id, duration in task_configurations
    ]
    print(f"主协调器: 已创建 {len(coroutine_objects)} 个协程对象。")


    # =========================================================================
    # 步骤 4: 并发执行协程任务
    # 使用 asyncio.gather() 是最常用的方法，它可以并发地运行列表中的所有“可等待对象”
    # （包括协程对象和 Task 对象），并等待它们全部完成。
    # await asyncio.gather(...) 会暂停当前主协程，并将控制权交给事件循环，
    # 事件循环会同时调度 coroutine_objects 中的协程运行。
    # 当所有协程都完成后，gather 返回一个包含所有协程返回值的列表。
    # =========================================================================
    print("主协调器: 使用 asyncio.gather 并发运行任务...")
    # await 是这里的关键，主协程会在这里等待所有子任务完成
    results = await asyncio.gather(*coroutine_objects)

    print("主协调器: 所有并发任务已完成。")
    print("主协调器: 所有任务的结果如下:")
    for res in results:
        print(f"- {res}")

    # =========================================================================
    # 可选: 演示使用 asyncio.create_task 创建任务而不立即等待
    # 如果你不想等待某个任务，只想让它在后台运行，可以使用 asyncio.create_task()
    # background_task = asyncio.create_task(some_other_async_task())
    # print("主协调器: 启动了一个后台任务...")
    # 注意：如果主协程在后台任务完成前结束，后台任务可能会被取消，
    # 如果需要确保后台任务完成，你可能需要在某个地方 await background_task
    # =========================================================================

    end_time = time.time()
    print(f"主协调器: 异步流程结束。总耗时: {end_time - start_time:.2f} 秒")


# =============================================================================
# 步骤 5: 程序的入口点
# 使用标准的 if __name__ == "__main__": 保护块。
# 在这里调用 asyncio.run() 来启动事件循环，并运行顶层的主异步函数。
# asyncio.run() 是 Python 3.7+ 推荐的方式，它会负责创建事件循环、
# 运行传入的协程直到完成，并最后关闭事件循环。
# =============================================================================
if __name__ == "__main__":
    print("程序开始")
    # 调用 asyncio.run() 来执行我们的主异步函数 main_async_orchestrator
    asyncio.run(main_async_orchestrator())
    print("程序已完全退出。")
```

```text
程序开始
主协调器: 异步流程开始
主协调器: 已创建 4 个协程对象。
主协调器: 使用 asyncio.gather 并发运行任务...
[任务 1] 开始执行, 预计耗时 2 秒...
[任务 2] 开始执行, 预计耗时 5 秒...
[任务 3] 开始执行, 预计耗时 2 秒...
[任务 4] 开始执行, 预计耗时 5 秒...
[任务 1] 执行完毕。
[任务 3] 执行完毕。
[任务 2] 执行完毕。
[任务 4] 执行完毕。
主协调器: 所有并发任务已完成。
主协调器: 所有任务的结果如下: 
- 任务 1 完成，耗时 2 秒。    
- 任务 2 完成，耗时 5 秒。
- 任务 3 完成，耗时 2 秒。
- 任务 4 完成，耗时 5 秒。
主协调器: 异步流程结束。总耗时: 5.00 秒
程序已完全退出。
```
