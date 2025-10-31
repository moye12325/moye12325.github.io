---
date: 2024-07-18T12:39:34.525Z
updated: null
title: 部署项目--nginx--403
slug: '2'
oid: 66990d06907f41ea6d5d8655
categories: 项目部署
type: post
permalink: /posts/项目部署/2
---


## 部署项目--nginx--403

要在CentOS上部署Vue项目，假设已经打包好了 `dist` 文件夹：

### 1. 准备工作

确保你已经安装了以下软件：

- Node.js 和 npm
- 一个 Web 服务器，例如 Nginx 或 Apache

### 2. 上传打包文件

将 `dist` 文件夹上传到你的 CentOS 服务器上。使用 `scp` 命令或通过 FTP 工具上传文件。

例如使用 `scp` 命令：

`scp -r ./dist username@your_server_ip:/path/to/your/project`

### 3. 安装 Nginx

如果你还没有安装 Nginx，可以通过以下命令安装：

`sudo yum install epel-release sudo yum install nginx`

### 4. 配置 Nginx

编辑 Nginx 配置文件来指向你的 Vue 项目。打开 `/etc/nginx/nginx.conf` 文件，或者在 `/etc/nginx/conf.d/` 目录下创建一个新的配置文件。

例如，在 `/etc/nginx/conf.d/` 目录下创建一个新的配置文件 `vue_project.conf`：

`sudo nano /etc/nginx/conf.d/vue_project.conf`

添加以下配置：

```
server {
    listen       80;
    server_name  your_domain_or_ip;

    location / {
        root   /path/to/your/project/dist;
        try_files $uri $uri/ /index.html;
    }
}

```

将 `/path/to/your/project/dist` 替换为你上传的 `dist` 文件夹的实际路径。

### 5. 启动 Nginx

保存配置文件并重启 Nginx：

`sudo systemctl restart nginx`

### 6. 开启防火墙端口

确保防火墙允许 HTTP 流量：


`sudo firewall-cmd --permanent --add-service=http sudo firewall-cmd --reload`

### 7. 访问你的应用

现在你可以通过你的域名或服务器 IP 访问你的 Vue 应用。例如 `http://your_domain_or_ip`。

## 配置文件编写好之后403 dist文件权限

```
[root@localhost files]# ls -al /var/www/vue_project/ 
总用量 4 
drwxr-xr-x. 3 root root 18 6月 17 21:35 . 
drwxr-xr-x. 5 root root 52 6月 17 21:35 .. 
drwxrwxr-x. 4 moye moye 4096 6月 17 21:30 dist
```

> [!NOTE] 403 错误通常与文件权限有关。 `dist` 文件夹属于用户 `moye`，但是 Nginx 可能以 `nginx` 用户运行。为了确保 Nginx 可以访问你的 `dist` 文件夹，需要调整权限或将文件夹所有者改为 `nginx` 用户。

### 修改文件夹权限和所有者

#### 1. 确认 Nginx 用户

首先，确认 Nginx 服务是以哪个用户运行的。通常是 `nginx` 或 `www-data`。可以通过以下命令查看：

`ps aux | grep nginx`

输出中应该可以看到 Nginx 进程运行的用户，例如：

```
nginx    12345  0.0  0.0 123456  1234 ?        Ss   20:20   0:00 nginx: master process /usr/sbin/nginx
nginx    12346  0.0  0.0 123456  1234 ?        S    20:20   0:00 nginx: worker process

```

这里显示 Nginx 是以 `nginx` 用户运行的。

#### 2. 修改 `dist` 文件夹所有者

将 `dist` 文件夹及其内容的所有者改为 Nginx 用户：

`sudo chown -R nginx:nginx /var/www/vue_project/dist`

#### 3. 确保权限正确

确保 `dist` 文件夹及其内容的权限设置为 `755`，即所有者有读写执行权限，组和其他用户有读取和执行权限：

`sudo chmod -R 755 /var/www/vue_project/dist`

### 检查和重启 Nginx

修改完权限后，重启 Nginx 服务以应用新的配置：

`sudo systemctl restart nginx`

### 确认 Nginx 配置

确保你的 Nginx 配置文件路径正确且没有其他语法错误。可以使用以下命令检查 Nginx 配置文件的语法：

`sudo nginx -t`

如果配置正确，输出应该类似于：

`nginx: the configuration file /etc/nginx/nginx.conf syntax is ok nginx: configuration file /etc/nginx/nginx.conf test is successful`

## 访问依然403

相关信息：

```
[root@localhost files]# ps aux | grep nginx root 11413 0.0 0.0 39448 2092 ? Ss 21:19 0:00 nginx: master process /usr/sbin/nginx root 11965 0.0 0.0 112824 988 pts/5 S+ 21:40 0:00 grep --color=auto nginx nginx 14905 0.0 0.0 41992 2284 ? S 21:36 0:00 nginx: worker process nginx 14907 0.0 0.0 41992 2044 ? S 21:36 0:00 nginx: worker process nginx 14909 0.0 0.0 41992 2044 ? S 21:36 0:00 nginx: worker process nginx 14910 0.0 0.0 41992 2044 ? S 21:36 0:00 nginx: worker process nginx 14911 0.0 0.0 41992 2044 ? S 21:36 0:00 nginx: worker process nginx 14912 0.0 0.0 41992 2044 ? S 21:36 0:00 nginx: worker process nginx 14913 0.0 0.0 41992 2544 ? S 21:36 0:00 nginx: worker process nginx 14914 0.0 0.0 41992 2300 ? S 21:36 0:00 nginx: worker process [root@localhost files]# sudo chown -R nginx

/var/www/vue_project/dist [root@localhost files]# sudo chmod -R 755 /var/www/vue_project/dist [root@localhost files]# sudo systemctl restart nginx [root@localhost files]# sudo nginx -t nginx: the configuration file /etc/nginx/nginx.conf syntax is ok nginx: configuration file /etc/nginx/nginx.conf test is successful [root@localhost files]# [root@localhost files]# [root@localhost files]# [root@localhost files]# sudo systemctl restart nginx
```

### 为什么访问还是403 server { listen 8080; server_name 172.16.105.65;

```
root /var/www/vue_project/dist; index index.html;  location / {     try_files $uri $uri/ /index.html; }  error_page 500 502 503 504 /50x.html; location = /50x.html {     root /usr/share/nginx/html; }

}
```

### 检查 SELinux 设置

有时候，SELinux（Security-Enhanced Linux）会阻止Nginx访问目录。你可以暂时禁用SELinux来测试问题是否出在这里。

1. 暂时禁用SELinux：
`sudo setenforce 0`

2. 重启Nginx：
`sudo systemctl restart nginx`

3. 重新访问网站，看看问题是否解决。如果问题解决了，可以将SELinux设置为宽松模式，允许Nginx访问指定目录：
    
    运行以下命令，允许Nginx访问指定目录：
    `sudo chcon -R -t httpd_sys_content_t /var/www/vue_project/dist`
    
4. 重新启用SELinux：

`sudo setenforce 1`

### 检查文件夹权限

确保上级目录的权限也允许Nginx用户读取。例如：

`sudo chmod 755 /var/www/vue_project sudo chmod 755 /var/www`

### 检查Nginx访问日志和错误日志

查看Nginx访问日志和错误日志，查找更多的错误信息：

`sudo tail -f /var/log/nginx/access.log sudo tail -f /var/log/nginx/error.log`

### 检查防火墙设置

确保防火墙没有阻止端口8080的访问：

`sudo firewall-cmd --permanent --add-port=8080/tcp sudo firewall-cmd --reload`

### 检查SELinux

使用 `sestatus` 命令检查SELinux状态：

`sestatus`

如果SELinux处于启用状态，可以使用以下命令更改文件上下文：

`sudo chcon -R -t httpd_sys_content_t /var/www/vue_project/dist`

### 修改Nginx用户

在 `/etc/nginx/nginx.conf` 中确认Nginx是以哪个用户运行的，并确保目录权限正确：

`user nginx;`

### 重启Nginx并测试

再次重启Nginx并测试：

bash

复制代码

`sudo systemctl restart nginx`


## 后续
如何避免出现这种问题 chunk-vendors.d239ea38.js:6 Mixed Content: The page at 'https://7d9d12b0.r16.vip.cpolar.cn/' was loaded over HTTPS, but requested an insecure XMLHttpRequest endpoint 'http://172.16.105.65:8101/api/user/get/login'. This request has been blocked; the content must be served over HTTPS.

要避免 Mixed Content 问题，你需要确保所有请求都通过 HTTPS 进行。以下是解决该问题的步骤：

### 1. 配置 Nginx 支持 HTTPS

你需要为你的阿里云服务器配置 HTTPS。这包括获取 SSL 证书并配置 Nginx 使用该证书。

#### 获取 SSL 证书

你可以使用免费的 Let's Encrypt 证书或从其他证书颁发机构购买证书。这里以 Let's Encrypt 为例：

安装 Certbot（Let's Encrypt 的客户端）：

`sudo yum install epel-release -y sudo yum install certbot python2-certbot-nginx -y`

获取并安装证书：

`sudo certbot --nginx`

按照提示完成证书的安装过程。

#### 配置 Nginx 使用 HTTPS

打开 Nginx 配置文件：

`sudo vi /etc/nginx/nginx.conf`

添加或修改 server 块以支持 HTTPS：

`http {     ...      server {         listen 80;         server_name 47.121.116.101;          # Redirect all HTTP requests to HTTPS         location / {             return 301 https://$host$request_uri;         }     }      server {         listen 443 ssl;         server_name 47.121.116.101;          ssl_certificate /etc/letsencrypt/live/your_domain/fullchain.pem;         ssl_certificate_key /etc/letsencrypt/live/your_domain/privkey.pem;         ssl_protocols TLSv1 TLSv1.1 TLSv1.2;         ssl_ciphers HIGH:!aNULL:!MD5;          location / {             proxy_pass http://172.16.105.65:8080;  # 假设 Spring Boot 应用运行在 8080 端口             proxy_set_header Host $host;             proxy_set_header X-Real-IP $remote_addr;             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;             proxy_set_header X-Forwarded-Proto $scheme;         }     }      server {         listen 8101 ssl;         server_name 47.121.116.101;          ssl_certificate /etc/letsencrypt/live/your_domain/fullchain.pem;         ssl_certificate_key /etc/letsencrypt/live/your_domain/privkey.pem;         ssl_protocols TLSv1 TLSv1.1 TLSv1.2;         ssl_ciphers HIGH:!aNULL:!MD5;          location / {             proxy_pass http://172.16.105.65:8101;  # 假设另一个服务运行在 8101 端口             proxy_set_header Host $host;             proxy_set_header X-Real-IP $remote_addr;             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;             proxy_set_header X-Forwarded-Proto $scheme;         }     }      ... }`

### 2. 修改前端代码使用 HTTPS

确保前端代码中的请求 URL 也使用 HTTPS：

`const baseUrl =   process.env.NODE_ENV === "development"     ? "https://47.121.116.101:8101"     : "https://47.121.116.101:8101";  OpenAPI.BASE = baseUrl;`

### 3. 配置安全组

确保在阿里云控制台的安全组设置中，443 和 8101 端口已经对外开放。

### 4. 检查 Nginx 配置并重启 Nginx

检查 Nginx 配置是否正确：

`sudo nginx -t`

如果没有错误，重启 Nginx：

`sudo systemctl restart nginx`

通过这些步骤，可以确保所有请求都通过 HTTPS 进行，从而避免 Mixed Content 问题。