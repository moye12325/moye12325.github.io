---
date: 2025-04-25T06:07:12.080Z
updated: 2025-05-08T11:50:16.570Z
title: 小白也能懂的Python协程与asyncio指南
slug: asyncio
oid: 680b269081920129eb6743be
categories: Python
type: post
permalink: /posts/Python/asyncio
---


# 小白也能懂的Python协程与asyncio指南

## 一、从生活场景理解异步编程

### 1.1 买奶茶的两种方式
假设你要买三杯奶茶，每杯制作需要2分钟：

**传统方式（同步）：**

```python
def 买奶茶_同步():
    for _ in range(3):
        等待2分钟()  # 干等着不动
        拿奶茶()

# 总耗时：3×2=6分钟 ❌
```



**聪明方式（异步）：**

```python
async def 买奶茶_异步():
    订单列表 = [下单(), 下单(), 下单()]  # 同时下单
    await asyncio.gather(*订单列表)  # 边等边玩手机

# 总耗时：2分钟 ✅
```


### 1.2 协程就像外卖小哥
想象一个外卖小哥同时处理多个订单：
- 到A店取餐（等待时去B店）
- 途中接新订单（灵活调整路线）
- 送达后立即接下一单（不浪费时间）

这就是协程的工作方式！不需要多个小哥（线程），一个就能高效完成任务。

---

## 二、最简协程入门（附可运行代码）

### 2.1 Hello协程版

```python
import asyncio

async def 打招呼(name):  # 关键1：async定义协程
    print(f"{name}开始做事")
    await asyncio.sleep(1)  # 关键2：遇到等待就挂起
    print(f"{name}事情做完啦")

async def 主任务():
    await asyncio.gather(
        打招呼("小明"),
        打招呼("小红")
    )

asyncio.run(主任务())  # 关键3：启动事件循环
```


**输出结果：**
```
小明开始做事
小红开始做事
（等待1秒）
小明事情做完啦
小红事情做完啦
```


### 2.2 执行过程图解


![|700x615](https://qiniu.kanes.top/blog/154916547.png)

---

## 三、必须掌握的3个核心概念

### 3.1 协程三要素

| 要素        | 说明         | 类比            |
| --------- | ---------- | ------------- |
| async def | 声明协程函数     | 给外卖订单贴上"加急"标签 |
| await     | 暂停并让出控制权   | 小哥暂时离开去送其他订单  |
| 事件循环      | 协调所有任务的调度员 | 外卖平台派单系统      |

### 3.2 常见误区清单

1. 错误：在普通函数中使用await


   ```python
   def 普通函数():
       await asyncio.sleep(1)  # 报错！
   ```
   

2. 错误：忘记创建任务



   ```python
   async def 错误示例():
       # 顺序执行，没有并发！
       await 任务1()
       await 任务2()
   ```
   

3. 正确做法：


   ```python
   async def 正确示例():
       task1 = asyncio.create_task(任务1())
       task2 = asyncio.create_task(任务2())
       await task1
       await task2
   ```

---

## 四、手把手实战：下载多张图片

### 4.1 同步版本（龟速）


```python
import requests

def 下载图片(url):
    print(f"开始下载 {url}")
    data = requests.get(url).content
    with open("图片.jpg", "wb") as f:
        f.write(data)
    print(f"下载完成 {url}")

def 主函数():
    urls = ["url1", "url2", "url3"]  # 假设3个图片地址
    for url in urls:
        下载图片(url)

# 总耗时：单张耗时 × 数量
```

### 4.2 异步版本（飞一般的感觉）


```python
import aiohttp

async def 异步下载(url):
    async with aiohttp.ClientSession() as session:
        print(f"开始下载 {url}")
        async with session.get(url) as response:
            data = await response.read()
        with open(f"{url.split('/')[-1]}", "wb") as f:
            f.write(data)
        print(f"下载完成 {url}")

async def 主任务():
    urls = ["url1", "url2", "url3"]
    await asyncio.gather(*[异步下载(url) for url in urls])

asyncio.run(主任务())
```

### 4.3 性能对比
| 图片数量 | 同步耗时 | 异步耗时 | 速度提升 |
|---------|---------|----------|---------|
| 10      | 20s     | 2s       | 10倍    |
| 100     | 200s    | 5s       | 40倍    |

---

## 五、常见问题解答

### Q1：协程和多线程有什么区别？
| 特性         | 协程                 | 多线程               |
|--------------|----------------------|---------------------|
| 资源占用     | 一个线程搞定所有     | 每个线程需要独立资源 |
| 切换方式     | 主动让出控制权       | 被系统强制切换       |
| 适用场景     | 适合大量IO操作       | 适合计算密集型任务   |
| 编程难度     | 需要理解异步语法     | 需要处理线程安全问题 |

### Q2：什么时候不能用协程？
- 需要大量CPU计算的场景（如视频转码）
- 使用不支持异步的库（比如传统的数据库驱动）
- 需要跨核并行计算（需结合多进程）

### Q3：如何调试协程程序？
1. 使用`asyncio.run()`作为入口
2. 在协程内使用普通print语句
3. 使用专业调试器：

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## 六、最佳学习路线建议

### 6.1 新手三步走

1. 先写同步代码理解业务流程
2. 将耗时操作替换为async/await
3. 用`asyncio.gather`实现并发

### 6.2 推荐练习项目

| 项目类型  | 实现功能       | 技能点    |
| ----- | ---------- | ------ |
| 天气查询器 | 同时查询多个城市天气 | 基础异步请求 |
| 网页监控  | 定时检查多个网站状态 | 异步定时任务 |
| 聊天机器人 | 同时处理多个用户消息 | 并发消息处理 |

---

## 七、记住这5句话就够了

1. **async def**：声明协程的起跑线
2. **await**：遇到IO就举手暂停
3. **事件循环**：幕后总调度员
4. **create_task**：把协程变成可执行任务
5. **asyncio.run()**：程序启动开关