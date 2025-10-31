---
date: 2024-07-18T12:26:14.976Z
updated: 2024-07-18T13:44:19.292Z
title: 项目部署--nginx--端口转发
slug: '1'
oid: 669909e6907f41ea6d5d84d9
categories: 项目部署
type: post
permalink: /posts/项目部署/1
---


## 项目部署--nginx--端口转发
## 内网与阿里云服务器的通信

```
docker run --rm --device /dev/net/tun --cap-add NET_ADMIN -ti --net=host -p 127.0.0.1:1080:1080 -p 127.0.0.1:8888:8888 -e EC_VER=7.6.7 -e CLI_OPTS="-d your_vpn_addr -u your_username -p your_pwd" hagb/docker-easyconnect:cli
```

 your_vpn_addr your_username your_pwd 三个替换成你的就可以了


## 端口转发 -- 基于nginx

用Nginx实现端口转发可以更灵活和高效。需要在阿里云服务器上安装并配置Nginx以实现从阿里云服务器到局域网服务器的请求转发。以下是详细步骤：

### 1. 安装Nginx

在阿里云服务器上安装Nginx：

```
sudo yum install epel-release -y 
sudo yum install nginx -y sudo systemctl start nginx 
sudo systemctl enable nginx
```

### 2. 配置Nginx

编辑Nginx配置文件：

```
sudo vi /etc/nginx/nginx.conf
```

在`http`部分添加一个新的server块：

```
http {
    server {
        listen 80;
        server_name your_domain_or_ip;

        location / {
            proxy_pass http://172.16.105.65:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
将`your_domain_or_ip`替换为你的域名或阿里云服务器的IP地址。

### 3. 检查Nginx配置并重启Nginx

检查Nginx配置是否正确：

`sudo nginx -t`

如果没有错误，重启Nginx：

`sudo systemctl restart nginx`

### 4. 配置安全组

确保在阿里云控制台的安全组设置中，80端口已经对外开放。

### 5. 部署Vue前端和Spring Boot后端

- 将Vue前端项目打包（生成`dist`目录），并将其放置在Spring Boot应用的`static`目录下。
- 启动Spring Boot应用：
    `java -jar your-springboot-application.jar`
    

### 6. 测试

通过访问你的域名，确认请求是否成功转发到局域网服务器上的Spring Boot应用。

## TIPS

前后端项目都部署在局域网服务器，则后端请求也得写成阿里云的 ip + port 
并且配置端口转发，一定不要忘记开放安全规则！