---
title: "nginx教程"
date: 2014-11-07 11:03:30
updated: 2024-04-19 08:28:00
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

## Web项目目录的常用权限

```shell
find /A -type d -exec chmod 0755 {} \;
find /A -type f -exec chmod 0644 {} \;
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
  # 访问频率限制。limit_req_zone只能在http中使用，limit_req可以用在http、server和location中
  ##
  limit_req_zone $binary_remote_addr zone=myzone:10m rate=5r/s;	# ，key可以设置为binary_remote_addr表示针对某个域名，存储访问数量的zone叫myzone，大小为10M，频率为5个请求每秒
  limit_req zone=myzone burst=5 nodelay;	# 限制每个IP每秒不超过20个请求
  
	##  
	# Logging Settings  全局日志文件
	##  
	access_log /var/log/nginx/access.log;  
	error_log /var/log/nginx/error.log;  

	##  
	# Gzip Settings Gzip压缩功能，可减少网络传输
  # 注意一定要加上gzip_types否则不成功，不知道为啥，另外可以通过检查response header(Content-Encoding)看是否成功，以及调试工具最下面的transferred和resources的大小对比就知道了
	##
	gzip on;  
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
		server_name haofly.net a.haofly.net; 	# 如果是多域名，用空格分割开 
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
      		# 前缀匹配，一般用来匹配目录 ^~
          # 正则匹配，大小写敏感 ~
          # 正则匹配，忽略大小写 ~*
          # ^~ 前半部分匹配，例如location ^~ /hello 等同于location /hello
          # 正则匹配，例如~* \.(.gif|jpg|png)$
      		# 任何匹配未成功的	/
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
		
        # 需要注意的是，nginx代理静态文件的时候，首先需要nginx运行用户对文件有读权限，并且需要文件所在目录的可执行权限(如果还是不行，可以继续往该目录的上一级来查看权限问题)，否则可能出现访问静态资源403的问题
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

### 端口转发配置/获取真实IP

- `proxy_set_header`几个配置可以让程序获取到真实的用户IP，而不是多级代理时候的`nginx`内网地址

```nginx
在server里：
server{
    listen 80;
    server_name haofly.net *.haofly.net;	# 支持通配符，多个域名之间一定不能用逗号，否则会出现莫名其妙的问题
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

### 自定义日志格式

- 日志的一些变量:
  - `$host`访问的域名
  - `$remote_addr/$http_x_forwarded_for`客户端IP地址
  - `$time_local`访问时间
  - `$status`访问状态码
  - `$upstream_response_time`应用返回到Nginx的时间
  - `$request_time`请求时间
  - `$http_referer`请求来源
  - `$http_user_agent`访问客户端
  - `$body_bytes_sent`返回给客户端的大小

`nginx`的默认日志格式为

```nginx
log_format '$remote_addr - $remote_user [$time_local] '
						'"$request" $status $body_bytes_sent '
						'"$http_referer" "$http_user_agent" "$gzip_ratio"';
```

将真实IP记录在日志中，而不是代理的日志(需要设置`proxy_set_header`等信息，参考代理配置):

```nginx
# my_format即是自己定义的日志格式别名
# 返回真实IP
# 记录upstream的响应时间
log_format my_format '$http_x_forwarded_for - $remote_addr - $request_time - $upstream_response_time - $remote_user [$time_local] '
						'"$request" $status $body_bytes_sent '
						'"$http_referer" "$http_user_agent" "$gzip_ratio"';

# 定义在http区块中，然后在server区块中这样使用即可覆盖默认的日志配置
# 需要注意的是千万别在http区块中使用，否则会重复打印多条日志
server {
  access_log /var/log/nginx/access.log my_format;
}
```

### Rewrite规则

- 是一种以正则方式重写url的语法

- 关于uri的变量

  ```shell
  $request_uri # 包含请求参数的原始uri，例如/nginx.php?id=123
  $uri	# 不带请求参数的原始uri，例如/nginx.php
  $document_uri	# 同上
  $args	# 请求参数
  $query_string	# 同上
  $content_length
  $content_type
  $host
  $http_cookie
  $request_method
  $scheme	# http或https
  $server_name
  $server_PORT
  ```

- 有如下几种重写类型:
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
- 如果怎么`rewrite`程序都获取不到正确的请求地址，例如CI框架，那么可能是应用程序读取的是`REQUEST_URI`而不是`proxy_pass`过去的地址，可以这样传递以改变`$request_uri`的值:

  ```nginx
  set $request_url $request_uri;
  if ($request_uri ~ ^/admin/(.*)$ ) {
    set $request_url /$1;
  }
  
  location /v2 {
  set $request_url $uri;	# 如果要给所有请求加一个前缀，可以这样做
    rewrite ^/v2/(.*)$ /$1 last;
  }
  
  location /admin {
  set $request_url $uri;
    rewrite ^/admin/(.*)$ /$1 last;
  }
  location / {
    try_files $uri $uri/ /index.php;	# try_files指令回按顺序检查文件是否存在，返回第一个找到的文件或文件夹
  }
  
  location ~* \.php$ {
  	rewrite ^/admin/(.*)$ /$1 break;
      
    include test/fastcgi-php.conf;
      
    fastcgi_param  REQUEST_URI        $request_url;
    fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
  }
  ```

#### 去掉uri中的一段

- 例如用户访问`/abc/def.html`，我们将其重定向到`/def.html`

```nginx
# 方法一
location ^~/abc/ {
  proxy_pass http://abc/;	# 这里proxy_pass的结尾有/，将会把/abc/*后面的路径直接拼接到后面，实现了移除abc的效果
}

# 方法二
location ^~/abc/ {
  rewrite ^/abc/(.*)$ /$1 break;	# 将匹配到的路径作为第一个参数来重新匹配，下一次就不回进入location /abc了
  proxy_pass http://abc;
}
```

#### 重定向指定文件的访问

例如，重定向favicon.ico文件

```nginx
location /favicon.ico {
 	alias /var/www/html/mypath/favicon.ico; 
}

location = /favicon.ico {	# 有时候要用=，不知道为什么
 	alias /var/www/html/mypath/favicon.ico; 
}
```

### 配置nginx IP黑白名单

新建配置文件`/etc/nginx/blockips.conf`，内容格式如下

```shell
deny 1.1.1.1;	# 屏蔽单个IP
deny 2.2.2.0/24;# 屏蔽IP段

# 白名单的话可以这样做
allow 1.1.1.1;
deny all;
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

### 本地localhost开启https/ssl

配置流程主要参考的是[local-cert-generator](https://github.com/dakshshah96/local-cert-generator/)

1. 生成根证书

   ```shell
   openssl genrsa -des3 -out rootCA.key 2048
   openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 7300 -out rootCA.pem
   ```

2. 打开MacOS的`Keychain Access`然后点击左下角`Category->Certificates`，然后点击顶部菜单`File->Import Items`选择刚才生成的`rootCA.pem`，然后双击，选择始终信任该证书:
   ![](https://haofly.net/uploads/nginx_0.png)

3. 签发证书

   ```shell
   openssl req -new -sha256 -nodes -out server.csr -newkey rsa:2048 -keyout server.key -config server.csr.cnf	# server.csr.cnf见https://github.com/dakshshah96/local-cert-generator/blob/master/server.csr.cnf
   openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 825 -sha256 -extfile v3.ext # v3.ext见https://github.com/dakshshah96/local-cert-generator/blob/master/v3.ext
   ```

4. 把上一步生成的证书配置到`nginx` 中即可

   ```nginx
   server {
     listen 443 ssl;
     charset utf-8;
     server_name localhost;
   
     ssl_certificate /etc/nginx/conf.d/server.crt;
     ssl_certificate_key /etc/nginx/conf.d/server.key;
     location / {
       proxy_pass http://127.0.0.1:8000;	# 这里是服务的地址
     }
   }
   ```

### Nginx直接返回文本/Json

```shell
location ~ ^/json {
    default_type application/json;
    return 200 '{"status":"success","result":"nginx json"}';
}
```

### Nginx根据日期转发/Nginx获取日期

```shell
location = / {
  if ($time_iso8601 ~ ^\d+-0[1-9]-\d+) {	# 1-9月转发到path1，其他时间转发到path2
    rewrite ^/$ /path1 redirect;
  }
  rewrite ^/$ /path2 redirect;
}
```

### Nginx编写.htaccess

- 其实不算是`.htaccess`就是一个配置文件而已
- 需要在项目目录下新建`.htaccess`，语法需要是`nginx`的语法，而不是`apache`的
- 然后在`nginx`该`server`配置中`include`该文件即可

### 返回stream响应

```nginx
location / {
    # 需要禁用缓冲
    proxy_buffering off;
    fastcgi_buffering off;
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

## 常用模块

### nginx-http-concat: 合并前端资源

前端可以直接访问`/js/??jquery.js,index.js,second.js`同时获取三个js文件，而不用发送三个请求了

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
  fastcgi_connect_timeout 300s;
  fastcgi_send_timeout 300s;
  fastcgi_read_timeout 300s;
  
  # proxy模式
  proxy_connect_timeout 300s;
  proxy_send_timeout 300s;
  proxy_read_timeout 300s;
  ```

- **上述timeout都不起作用**: 看看会不会是aws的负载均衡器设置了超时时间的。MMP，ClashX可能也会导致刚好1分钟60秒超时的问题

- **Nginx报错502 Bad Gateway**: 

  方法一：检查upstream是否正常
  方法二：修改了timeout参数
  方法三：可以尝试在nginx配置中提高这两个fastcgi参数:

  ```shell
  fastcgi_buffers 16 16k;
  fastcgi_buffer_size 32k;
  ```

  方法四：如果是docker里面的nginx，查看网页上是否访问到代理的IP上面去了

- **wordpress无限重定向**: 可能是在aws的elb中只发了http请求到后端，但是url访问的却是https，导致wordpress搞不清楚了，可以在nginx这边加上一个fastcgi配置:

  ```shell
  fastcgi_param HTTPS on;
  ```

- **改了各种配置都还是499错误** 发现关了代理就好了，mmp
