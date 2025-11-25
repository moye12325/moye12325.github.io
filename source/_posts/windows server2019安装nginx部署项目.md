---
title: windows server2019安装nginx部署项目
date: 2024-07-22 18:02:56
categories: [Web开发]
tags: ['Java', 'JavaScript', 'Nginx', '机器学习', '部署']
---
# windows安装nginx部署项目

### 1\. 下载和安装Nginx

1. **下载Nginx**：  
   * 访问Nginx的官方网站。  
   * 下载适用于Windows的稳定版本的Nginx压缩包。
2. **解压Nginx**：  
   * 将下载的压缩包解压到你希望安装Nginx的目录，例如 `C:\nginx`。

### 2\. 配置Nginx

1. **修改配置文件**：  
   * 打开 `C:\nginx\conf\nginx.conf` 文件，进行必要的配置。  
   * 下面是一个简单的示例配置，假设你要部署一个静态网站：

```
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

### 3\. 启动Nginx

1. **启动Nginx**：  
   * 打开命令提示符，导航到 `C:\nginx` 目录，运行以下命令启动Nginx：  
   sh  
   复制代码  
   `nginx.exe  
   `
2. **检查Nginx是否启动**：  
   * 打开浏览器，访问 `http://localhost`，应该能看到Nginx的欢迎页面。

### 4\. 部署项目

1. **静态网站**：  
   * 将你的静态网站文件（如HTML、CSS、JavaScript文件）放到 `C:\nginx\html` 目录中。  
   * 修改 `nginx.conf` 文件中的 `root` 指令，指向你的项目目录。例如，如果你的项目文件在 `C:\my_project` 中：  

```
   location / {  
       root   C:\my_project;  
       index  index.html index.htm;  
   }  
```

2. **动态网站**（例如使用FastCGI、PHP等）：  
   * 你可能需要配置FastCGI或其他后端服务，例如PHP-FPM。  
   * 在 `nginx.conf` 中添加适当的location配置。例如，如果使用PHP-FPM：  

```
server {  
       listen       80;  
       server_name  localhost;  
       location / {  
           root   C:\my_project;  
           index  index.php index.html index.htm;  
       }  
       location ~ \.php$ {  
           root           C:\my_project;  
           fastcgi_pass   127.0.0.1:9000;  
           fastcgi_index  index.php;  
           fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;  
           include        fastcgi_params;  
       }  
   }  
```

### 5\. 管理Nginx

1. **重新加载配置**：  
   * 如果修改了配置文件，使用以下命令重新加载配置而不重启Nginx：  
   sh  
   复制代码  
   `nginx.exe -s reload  
   `
2. **停止Nginx**：  
   * 使用以下命令停止Nginx：  
   sh  
   复制代码  
   `nginx.exe -s stop  
   `
3. **检查Nginx状态**：  
   * 在任务管理器中查看 `nginx.exe` 进程，确保Nginx正在运行。

### 常见问题及解决方法

* **端口占用**：如果端口80被其他应用占用，可以在配置文件中修改 `listen` 指令，使用其他端口。
* **权限问题**：确保Nginx目录及项目目录有适当的读写权限。