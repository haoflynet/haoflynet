---
title: "nginx教程"
date: 2014-11-07 11:03:30
updated: 2019-05-27 16:01:00
categories: server
---
Nginx用起来比Apache方便简介，也有很多超过Apache的地方。Nginx不仅可以作为http服务器来用，更重要的，它还可以用来做负载均衡和反向代理。[Nginx官方文档](https://docs.nginx.com/nginx/)

- 正向代理：类似fq，服务器代替我们去访问其他的服务
- 反向代理：外部访问内部服务，例如外部用户访问公司内部的各个服务，通过一个nginx进行代理

## 安装nginx

安装方法见: [nginx安装方法](https://nginx.org/en/linux_packages.html)

如果要安装最新稳定版nginx，可以添加这个源:

```tex
[nginx]
name=nginx repo
baseurl=https://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1
```

## 配置文件详解

<!--more-->

- `fastcgi`和`http`的区别是，前者是一个二进制协议，并且是长连接，http不是长连接。

nginx配置文件地址在`/etc/nginx/nginx.conf`，nginx的配置文件里，最重要的section是http区块，里面包含了全局设置、主机设置(server)、上游服务器设置(upstream)、URL设置

```nginx
user www-data;           # nginx所属用户
worker_processes 4;      # 进程数，通常是和CPU数量相等
pid /var/run/nginx.pid;

events{
	worker_connections 768;   # 单个进程并发的最大连接数
	# multi_accept on;
}

http{
	##
	# Basic Settings
	##
	sendfile on; # 开启高效文件传输模式，普通应用可以on，调用sendfile可以减少用户空间与系统空间的切换，直接将数据从磁盘读到系统缓存，增加性能。但是如果是高IO的应用可设置为off，以平衡磁盘与网络IO处理速度，降低系统复杂。如果发现更改了图片但是图片没更新，可以尝试关闭该选项重启nginx试试。
	tcp_nopush on;

	server_tokens off; # 隐藏系统版本号 # server_names_has_bucket_size 64; #
	server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##  
	# Logging Settings  全局日志文件
	##  
	access_log /var/log/nginx/access.log;  
	error_log /var/log/nginx/error.log;  

	##  
	# Gzip Settings Gzip压缩功能，可减少网络传输  
	##
	gzip on;  
	gzip_disable "msie6";
	gzip_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;	# 设置需要压缩的类型，默认有些类型比如json并没有开启

	# gzip_vary on;  
	# gzip_proxied any;  
	# gzip_comp_level 6;  
	# gzip_buffers 16 8k;  
	# gzip_http_version 1.1;  
	
	##  
	# Virtual Host Configs  虚拟主机配置，如果想要把server写在外面，可以在这里设置存放目录
	##  
	include /etc/nginx/conf.d/_.conf;  
	include /etc/nginx/sites-enabled/_;  
	
	# 设置虚拟主机  
	server{  
		listen 80;  
		server_name haofly.net a.haofly.net; 	# 如果是多域名，用逗号分割开 
		root /var/www/haofly;		# 网站根目录
	
		charset utf-8; # 字符集不应该在html里面指定，而直接在服务器端指定  
		
		# 该server日志文件存放路径
		access_log /var/log/nginx/80_access.log; 
		error_log /var/log/nginx/80_error.log;
		
		# 禁用非必要的请求方法，比如只处理GET、POST请求
		if ($request_method !~ ^(GET|HEAD|POST)$ ){
			return 444;
		}
		
		location = /{
          # 完全匹配 =
          # 大小写敏感 ~
          # 忽略大小写 ~*
          # ^~ 前半部分匹配，例如location ^~ /hello 等同于location /hello
          # 正则匹配，例如~* \.(.gif|jpg|png)$
		}
		
		location / {
			root /var/www/haofly;      # 设置根目录              
			index index.html;          # 首页设置                     
			proxy_pass http://name;  # 上面设置的负载均衡服务器列表的名字                    
			proxy_connect_timeout 60; # nginx到后台服务器连接超时时间                    
			proxy_set_header Host $http_host;                    
			proxy_set_header X-Real-IP $remote_addr;                    
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # 负载均衡时将真实IP传递到后端           
		}            
		
		location /blog {
          alias /var/www/blog;	# 别名设置。如果有alias值，那么不管location的路径是怎样的，真实的资源路径都是别名所指定的路径
		}
		
        # 需要注意的是，nginx代理静态文件的时候，首先需要nginx运行用户对文件有读权限，并且需要文件所在福目录的可执行权限，否则可能出现访问静态资源403的问题
		location /static {    # 静态文件由nginx自己处理。如果整个域名全静态代理，可以直接写在location外的root
			root /var/www/haofly;
		} 
	}
```


### 负载均衡配置

```nginx
# 在http里定义upstream
upstream backend {
    server 127.0.0.1:81;
    server 127.0.0.1:82;
}
# 在server里：
location / {
    proxy_pass http://backend;
}
```

### 端口转发配置

```nginx
在server里：
server{
    listen 80;
    server_name haofly.net, *.haofly.net;	# 支持通配符
    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8000;
    }
    access_log /var/log/nginx/haofly.net_access.log;
}
```
### 单独的虚拟目录配置

最好将单独的域名放到单独的配置文件中`/etc/nginx/conf.d/test.conf`

```nginx
server{
        listen 80;
        listen 443 default_server ssl;	# 这样两句可以同时监听80和443端口
        server_name fun.haofly.net;

        charset utf-8;
        access_log /var/log/nginx/fun.log;
        error_log /var/log/nginx/fun_error.log;

        location ^~ /multiple-addresses-in-one-map/ {
                alias /usr/share/nginx/multiple-addresses-in-one-map/;
        }
}
```

### Rewrite规则

是一种以正则方式重写url的语法。

有如下几种重写类型:

- **last**: 表示完成rewrite，浏览器地址栏URL不变。一般用在server和if中。不会终止匹配，新的url会重新从server匹配一遍。
- **break**: 本条规则匹配完成后终止匹配，不再匹配后面的规则，浏览器地址栏URL不变。一般用在location中，会终止匹配，只会往下走，不会整个server重新匹配。
- **redirect**: 返回302临时重定向，浏览器地址栏URL变成转换后的地址
- **permanent**: 返回301永久重定向，浏览器地址栏URL变成转换后的地址

```nginx
# 如果用户访问/test/abc，直接重定向到/abc并且使用test这个upstream
location /test {
	rewrite ^/test(.*)$ $1 break;
    proxy_pass http://test;
    proxy_redirect off;
    proxy_set_header Host $host;
}
```
### 配置nginx IP黑名单

新建配置文件`/etc/nginx/blockips.conf`，内容格式如下

```shell
deny 1.1.1.1;	# 屏蔽单个IP
deny 2.2.2.0/24;# 屏蔽IP段
```

然后在nginx主配置文件`/etc/nginx/nginx.conf`的`http`中导入该文件`include blockips.conf;`

### HTTPS证书配置

```shell
server {
	# http自动跳转到https
    if ($host = haofly.net) {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name api.haofly.net;
    
    # 其中，.pem文件表示证书文件，.key是私钥文件，而目录则是自定义个一个nginx有读权限的目录
    ssl_certificate /etc/cert/api.haofly.net.pem;
    ssl_certificate_key /etc/cert/api.haofly.net.key;
   
    charset utf-8;
    access_log /var/log/nginx/api.haofly.net.log;
    error_log /var/log/nginx/api.haofly.net.error.log;

	location / {
		uwsgi_pass my_upstream;
	}
}
```

## 查看负载均衡状态

nginx提供了默认的模块可以查看负载均衡的统计信息等，只需要在某个server里面添加：

```nginx
location /nginx {    
	stub_status on;  
	access_log   on;  
	auth_basic   "NginxStatus";  
	auth_basic_user_file   /etc/nginx/htpasswd;  
}
```

其中htpasswd是保存用户名和密码的文件，可以自定义位置，每一行一个用户`username:password`这样子保存的，使用crypt3(BASE64)加密，可以用一个PHP文件来生成

	$password = 'hehe';
	$password = crypt($password, base64_encode($password));
	echo $password;

最后访问 <http://...../nginx> 即可看到如下的负载均衡信息：

	Active connections: 1
	server accepts handled requests
	 2 2 37
	Reading: 0 Writing: 1 Waiting: 0

## TroubleShooting

- CentOS下出现负载均衡出现错误：(13: Permission denied) while connecting to upstream:[nginx]，直接执行如下命令：

  ```shell
  sudo cat /var/log/audit/audit.log | grep nginx | grep denied | audit2allow -M mynginx
  sudo semodule -i mynginx.pp  # 貌似在SELinux下，auditallowk可以讲禁止的规则加入到信任
  ```

- `php-fpm`没有打印错误日志，仅仅有访问日志，原因是php-fpm默认是关闭workder进程的错误输出，重定向到了`/dev/null`，所以在errlog里面看不到我们想看的日志，需要做以下更改:

  ```shell
  # vim /etc/php-fpm.conf
  [www]
  catch_workers_output = yes	# 更改为yes
  
  # vim /etc/php.ini
  log_errors = On
  error_log = /var/log/error_log
  error_reporting=E_ALL
  ```

- **HTTP Header中后端服务无法获取有下划线的header**: 没错，无论是`Nginx`还是`Apache`，都是不允许的(在HTTP标准中倒是允许的)，因为`Nginx`的配置文件中的变量都是下划线的，容易引起混淆，当然也可以用`underscores_in_headers on`参数进行开启，不过不建议。

- **client intended to send too large body**: 客户端发送的数据量太大，可以通过更改`http`模块中的`client_max_body_size 1m;`参数，默认为`1m`，看实际需要调整

- **upstream sent too big header while reading response header from upstream: **原因是`upstream`那边响应头过大，可以在`server/location`配置里面适当加大响应缓存大小:

  ```nginx
  fastcgi_buffers 16 16k; 
  fastcgi_buffer_size 32k;
  ```

- **Nginx报错504 gateway timeout**: 首先当然是看业务是否需要那么长的时间，如果实在需要，可以在nginx配置中修改如下参数:

  ```shell
  # fastcgi模式
  fastcgi_connect_timeout 300;
  fastcgi_send_timeout 300;
  fastcgi_read_timeout 300;
  
  # proxy模式
  proxy_connect_timeout 300s;
  proxy_send_timeout 300s;
  proxy_read_timeout 300s;
  ```