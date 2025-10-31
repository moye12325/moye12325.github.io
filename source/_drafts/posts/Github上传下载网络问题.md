---
date: 2024-07-22T17:48:07.052Z
updated: null
title: Github上传下载网络问题
slug: '654371'
oid: 669e9b572a6fe84dfe92098a
categories: 所遇问题
type: post
permalink: /posts/所遇问题/654371
---


# Github上传下载网络问题

## 解决 Failed to connect to github.com port 443:connection timed out

```git
添加代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```


```git
取消全局代理：
git config --global --unset http.proxy 
git config --global --unset https.proxy
```



```git
取消全局代理：
git config --global -l 
```