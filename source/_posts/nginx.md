---
title: "nginx教程"
date: 2014-11-07 11:03:30
updated: 2017-06-09 17:04:00
categories: server
---
Nginx用起来比Apache方便简介，也有很多超过Apache的地方。Nginx不仅可以作为http服务器来用，更重要的，它还可以用来做负载均衡和反向代理.  

安装方法见: [Centos使用nginx安装方法](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-6-with-yum)

## 配置文件详解

nginx配置文件地址在`/etc/nginx/nginx.conf`，nginx的配置文件里，最重要的section是http区块，里面包含了全局设置、主机设置(server)、上游服务器设置(upstream)、URL设置

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
		sendfile on; # 开启高效文件传输模式，如果是高IO的应用可设置为off
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
			server_name haofly.net;  
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
	          # 前半部分匹配 ^~
	          # 正则匹配，例如~* \.(.gif|jpg|png)$
			}
			
			location / {
				root /var/www/haofly;      # 设置根目录              
				index index.html;          # 首页设置                     
				proxy_pass http://name;  # 上面设置的负载均衡服务器列表的名字                    
				proxy_connect_timeout 60; # nginx到后台服务器连接超时时间                    
				proxy_set_header Host $http_host;                    
				proxy_set_header X-Real-IP $remote_addr;                    
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;            
			}            
			
			location /blog {
	          alias /var/www/blog;	# 别名设置
			}
			
			location /static {    # 静态文件由nginx自己处理                					
				root /var/www/haofly;
			} 
		}


### 负载均衡配置

    在http里：
    upstream backend {
        server 127.0.0.1:81;
        server 127.0.0.1:82;
    }
    在server里：
    location / {
        proxy_pass http://backend;
    }

### 端口转发配置

    在server里：
    server{
        listen 80;
        server_name haofly.net;
        location / {
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://127.0.0.1:8000;
        }
        access_log /var/log/nginx/haofly.net_access.log;
   }

## 单独的虚拟目录配置

	server{
	        listen 80;
	        server_name fun.haofly.net;
	
	        charset utf-8;
	        access_log /var/log/nginx/fun.log;
	        error_log /var/log/nginx/fun_error.log;
	
	        location ^~ /multiple-addresses-in-one-map/ {
	                alias /usr/share/nginx/multiple-addresses-in-one-map/;
	        }
	}


## 查看负载均衡状态
nginx提供了默认的模块可以查看负载均衡的统计信息等，只需要在某个server里面添加：

	location /nginx {    
		stub_status on;  
		access_log   on;  
		auth_basic   "NginxStatus";  
		auth_basic_user_file   /etc/nginx/htpasswd;  
	}

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

- ​











