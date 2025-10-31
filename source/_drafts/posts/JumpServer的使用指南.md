---
date: 2024-07-22T17:49:23.804Z
updated: null
title: JumpServer的使用指南
slug: '75469673145'
oid: 669e9ba32a6fe84dfe9209c1
categories: 所遇问题
type: post
permalink: /posts/所遇问题/75469673145
---


# 零、

	提交slurm任务的服务器AssetIP：13.13.13.100
jumpserverHostIP：e1wx0vsede2ewknf.ttxs.site

# 一、普通方式登录使用

## 网页内使用与JumpServerClient软件

### 连接终端
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_1.png)

1. 右方终端
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_2.png)

> 两种方式：
> 一是网页内使用终端；
> 二是下载JumpServerClient软件，定向到xshell、mobaxterm等软件地址，同旧堡垒机，方法比较简单，不在此赘述。


![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_3.png)
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_4.png)

2. 左方回到主页
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_5.png)
同上述“1. 右方终端”

### 传输文件
同样是网页内使用与通过JumpServerClient软件定向到具体软件，具体过程类似上述连接终端
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_6.png)

# 二、密钥方式登录
[参考链接1](https://kb.fit2cloud.com/?p=098989ab-b70d-49c2-bf03-04574312ae78)
[参考链接2](https://blog.csdn.net/JiangLaoBi/article/details/130675075)

## 方式一：pem密钥
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_7.png)
会下载一个名为“username”-jumpserver.pem的密钥

填写ssh连接
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_8.png)
填写用户名、勾选public key
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_9.png)
点击浏览选择用户密钥，选择导入，选择刚下载的“username”-jumpserver.pem的密钥，并选中，点击确定。  
或者根据参考链接2的“使用xshell登录，需要页面设置一下，在页面工具处点击用户密钥管理者，将第一步获取的密钥输入。”部分进行设置。

如图所示，已连接。按照提示查询资产，并输入例如“tc6000”，按照对应提示即可连接到服务器。
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_10.png)

### 以mobaxterm为例：

同上即可
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_11.png)

## 方式二：公有&私有参考链接密钥

[参考链接3](https://blog.csdn.net/RedaTao/article/details/119523363)

指定命名防止与其他密钥冲突，例如GitHub的密钥等。一路回车即可。得到如图所示。
`
ssh-keygen -t rsa -C “your email” -f id_rsa_xx
`
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_12.png)

文本文档打开id_rsa_JumpServerLiling.pub，即公钥，复制内容。贴并提交。

> [!Note] 更新密钥会使之前的密钥失效。即方式一的密钥会失效！

![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_13.png)

### 以xshell为例：

新建会话同方式一，选取私钥
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_14.png)

### 以mobaxterm为例：
新建会话同方式一，选取私钥
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_15.png)

# 三、Pycharm连接
[参考链接4](https://kb.fit2cloud.com/?p=d85d8229-151a-42f4-b746-b0e65ab097fa)

## 命令连接堡垒机与资产

需按照提示输入密码。jumpserverUsername与systemUsername默认相同。

### 连接堡垒机

终端中输入命令与密码
`ssh -p2222 jumpserverUsername@jumpserverHostIP`
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_16.png)

### 连接堡垒机中的资产

`ssh -p2222 jumpserverUsername@systemUsername@AssetIP@jumpserverHostIP`
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_17.png)


## PyCharm连接堡垒机与资产

### 连接堡垒机
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_18.png)
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_19.png)
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_20.png)

### 连接堡垒机中的资产
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_21.png)
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_22.png)


# 四、VSCode连接（有问题）
[参考链接5](https://kb.fit2cloud.com/?p=48)
[参考链接6](https://zhuanlan.zhihu.com/p/601987450)

1. 下载安装插件
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_23.png)
2. 点击左下角绿色标识，中间上方选择 “ Connect to Host ”。
![](https://qiniu.kanes.top/blog/JumpServer的使用指南_image_24.png)