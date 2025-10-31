---
date: 2025-06-10T01:39:31.211Z
updated: null
title: WSL2 中 `git pull` 失败的 TLS 握手错误排查与解决
slug: '97655532543870'
oid: 68478cd381920129eb68341f
categories: 默认分类
type: post
permalink: /posts/默认分类/97655532543870
---


## WSL2 中 `git pull` 失败的 TLS 握手错误排查与解决

在使用 WSL2 环境执行 `git pull` 操作时，可能遇到因 TLS/SSL 握手失败导致的连接错误。常见的错误信息包括 `gnutls_handshake() failed: The TLS connection was non-properly terminated.` 或 `OpenSSL SSL_connect: SSL_ERROR_SYSCALL`。此类问题通常与网络代理、SSL 证书信任链或底层 TLS 库兼容性相关。

---

### 问题定位

错误消息直接指示 TLS/SSL 握手过程异常终止。在深入排查前，建议进行基础连通性与配置检查：

1. **系统时间同步：** 通过 `date -R` 命令验证 WSL2 系统时间是否与实际时间一致。时间不同步可能导致证书验证失败。
2. **网络可达性：** 使用 `ping your-repo-domain.com` 确认目标代码仓库域名可解析且网络可达。
3. **Git 代理配置：** 执行 `git config --global http.proxy` 和 `git config --global https.proxy` 检查 Git 全局代理设置。如存在配置，可尝试使用 `git config --global --unset http.proxy` 临时移除。

若基础检查无异常，且问题依旧，则需进一步分析 TLS 握手过程。通过 `curl -v` 命令可获取详细的连接日志：


```bash
curl -v https://your-repo-domain.com/path/to/repo.git/info/refs?service=git-upload-pack
```

`curl -v` 输出中若包含 `Uses proxy env variable https_proxy == 'http://X.X.X.X:YYYY'`，且代理连接成功 (`CONNECT tunnel established, response 200`)，但最终因 `OpenSSL SSL_connect: SSL_ERROR_SYSCALL` 失败，则高度指向代理对 TLS 流量的拦截。代理通常运行在 Windows 宿主机上，并通过其 IP 地址（例如 WSL2 的默认网关 IP）提供服务。此类代理进行 HTTPS 流量拦截时，会使用自身生成的 SSL 证书充当中间人，而 WSL2 默认不信任此证书。

例如，若证书颁发者显示为非公共信任的机构（如 `WR2`），则进一步证实代理拦截是核心问题。

---

### 解决方案：信任代理根证书

核心解决方案是使 WSL2 信任代理服务器所使用的根证书。

#### 步骤一：获取代理根证书

1. **从 Windows 浏览器导出证书：**
    - 在 Windows 宿主机浏览器中，访问任意 HTTPS 网站（例如 `https://www.baidu.com`）。
    - 点击地址栏左侧的**锁图标**，查看**证书信息**。
    - 在证书路径或认证路径中，查找由**非公共信任机构（如 `WR2`）**颁发的根证书。
    - 选中该证书，点击**“查看证书”**，切换至**“详细信息”**选项卡。
    - 点击**“复制到文件...”**按钮，选择 **“Base-64 编码 X.509 (.CER)”** 格式。
    - 将文件保存至 Windows 的**下载文件夹**，文件名示例：`my_proxy_root.crt`。

#### 步骤二：复制证书至 WSL2

假设 Windows 用户名为 `YourWindowsUsername`：

```Bash
cp "/mnt/c/Users/YourWindowsUsername/Downloads/my_proxy_root.crt" ~/
```

#### 步骤三：将证书添加至 WSL2 信任存储

```Bash
sudo cp ~/my_proxy_root.crt /usr/local/share/ca-certificates/my_proxy_root.crt
sudo update-ca-certificates
```

执行 `update-ca-certificates` 命令后，系统将更新其信任证书列表，并报告证书已成功添加。

#### 步骤四：验证并重试 Git 操作

确认 WSL2 会话中代理环境变量已正确设置（例如 `https_proxy`）。必要时可手动设置：

```Bash
# 验证代理环境变量
echo $https_proxy

# 必要时手动设置
# export https_proxy='http://[代理IP]:[代理端口]'
# export http_proxy='http://[代理IP]:[代理端口]'
# export no_proxy='localhost,127.0.0.1,::1,[内部IP范围]'

git pull
```

---

### 推荐替代方案：切换至 SSH 协议

若 HTTPS 代理配置复杂或稳定性不足，**SSH 协议**是更简洁、更可靠的解决方案。SSH 连接不依赖 HTTP/HTTPS 代理，从而规避了 SSL 拦截及证书信任问题。

1. **生成 SSH 密钥对：**
          
    ```Bash
    ssh-keygen -t ed25519 -C "user_email@example.com"
    ```
    
    接受默认路径及空密码短语（实现免密）。
    
2. **配置公钥至代码托管平台：**
    
    - 复制公钥内容：`cat ~/.ssh/id_ed25519.pub`。
    - 登录目标代码托管平台（如 GitLab、GitHub），在用户设置中添加此公钥。
3. **测试 SSH 连接：**
           
    ```Bash
    ssh -T git@your-repo-domain.com
    ```
    
    首次连接将触发**主机指纹验证**提示。务必**核对指纹**（例如，咨询管理员获取官方指纹），确认无误后**输入 `yes` 并回车**。成功后，将显示欢迎信息。
    
4. 修改本地仓库远程 URL：
    
    进入本地仓库目录：
            
    ```Bash
    git remote set-url origin git@your-repo-domain.com:your_group/your_repo.git
    ```
    
5. **执行 `git pull`：**
            
    ```Bash
    git pull
    ```
    
    此时，Git 将通过 SSH 协议拉取代码，绕过 HTTPS 代理及证书信任问题。
    

---