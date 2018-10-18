---
title: "使用nginx+uWSGI部署Django/Python应用"
date: 2018-08-04 21:32:00
updated: 2018-10-16 22:19:00
categories: python
---

使用`Django`可以追溯到15年，但是这还是第一次使用`Nginx+uWSGI`的方式对其进行部署，以前要么是小项目直接`runserver`，要么用`nginx`做`http`转发，但是使用`Nginx+uWSGI`明显是部署`Django`最好的方式了。至于为什么一定要用这样的方式，这篇文章讲得比较好[《部署Django项目背后的原理：为什么需要Nginx和Gunicron这些东西》](https://www.kawabangga.com/posts/2941)

<!--more-->

## 部署步骤

- 首先，要保证你的应用能使用`python manage.py runserver`命令启动起来

- 安装uWSGI，`pip install uwsgi`

- 测试让uWSGI直接运行项目于http上，`uwsgi --http :8000 --module mysite.wsgi`，这里的`mysite.wsgi`即是你的项目目录下的`wsgi.py`文件，实际的目录应该是`mysite/mysite/wsgi.py`

- 安装nginx，参考[Nginx教程](http://haofly.net/nginx)

- 配置nginx，参考上面的nginx教程，进行配置，主要是添加如下一个server:

  ```nginx
  upstream django {
  	# server unix:///pathto/mysite/mysite/mysite.sock;
  	server 127.0.0.1:8000;	# 这个时候就相当于一个端口转发
  }
  
  server {
  	listen 80;
  	charset utf-8;
  
  	location / {
  		uwsgi_pass django;
  
          # 下面的配置可以保存成文件然后include，有些nginx版本自带了/etc/nginx/uwsgi_params的，直接在这里include uwsgi_params即可
  		uwsgi_param  QUERY_STRING       $query_string;
  		uwsgi_param  REQUEST_METHOD     $request_method;
  		uwsgi_param  CONTENT_TYPE       $content_type;
  		uwsgi_param  CONTENT_LENGTH     $content_length;
  
  		uwsgi_param  REQUEST_URI        $request_uri;
  		uwsgi_param  PATH_INFO          $document_uri;
  		uwsgi_param  DOCUMENT_ROOT      $document_root;
  		uwsgi_param  SERVER_PROTOCOL    $server_protocol;
  		uwsgi_param  REQUEST_SCHEME     $scheme;
  		uwsgi_param  HTTPS              $https if_not_empty;
  
  		uwsgi_param  REMOTE_ADDR        $remote_addr;
  		uwsgi_param  REMOTE_PORT        $remote_port;
  		uwsgi_param  SERVER_PORT        $server_port;
  		uwsgi_param  SERVER_NAME        $server_name;
  	}
  }
  ```

  然后重启nginx，就能访问刚才用`uwsgi`命令启动的8000端口的服务了

- 使用socket的方式启动应用程序，`usgi --socket :8000 --module mysite.wsgi`，然后在nginx配置的`upstream`那里将原来的端口方式修改成socket的方式：`server unix:///pathto/mysite/mysite/mysite.sock;`其中`mysite.sock`，然后重启nginx查看是否仍然能正常访问。

- 将`socket`的启动参数写入到文件，这里我是直接把配置文件放到项目目录下的，方便以后启动:

  ```shell
  # sudo /usr/local/bin/uwsgi --ini /data/mysite/mysite/uwsgi.ini --daemonize /var/log/uwsgi.log  启动命令
  
  # uwsgi.ini file
  [uwsgi]
  
  # Django-related settings
  # the base directory (full path)
  chdir           = /data/mysite
  
  # Django's wsgi file
  module          = mysite.wsgi
  
  # the virtualenv (full path)
  # home            = /path/to/virtualenv
  
  # process-related settings
  # master
  master          = true
  # maximum number of worker processes进程数量一般与CPU数量相等
  processes       = 8
  threads 		= 32	# 默认一个进程是一个线程，可以直接提高线程的数量
  
  # the socket (use the full path to be safef
  socket          = /path/to/swy-api.sock	// 随便放哪里，也可以放在项目目录下
  
  # ... with appropriate permissions - may be needed
  chmod-socket    = 666		# 修改权限，以防出现connect() to unix:///path/to/your/mysite/mysite.sock failed (13: Permission
  denied)错误
  # clear environment on exit
  vacuum          = true
  
  py-autoreload = 1		# python代码变更后自动重启，线上更新代码后不要依赖于这个重启，最好supervisor重启所有进程，否则可能有些进程没生效
  buffer-size = 65535		# 针对莫名其妙出现502错误的一个可能的解决方法
  ```

综上，其实是和`php-fpm`部署的方式类似，使用wsgi协议启动应用，然后nginx直接获取其socket就行了。

### 使用supervisor管理uwsgi

如果仅仅用上面的方式来启动应用，应用有修改后，`py-autoreload`会自动重启应用，但是如果想要批量管理进程，例如批量开启或重启或关闭就有点麻烦了，并且程序挂了也没有自动重启机制，所以这里要用到`supervisor`。按照[使用Supervisor管理进程](https://haofly.net/supervisor)安装`supervisor`并生成配置文件后，在配置文件中添加以下的`program`即可

```shell
[program:uwsgi]
command=/usr/local/bin/uwsgi --ini /path/to/uwsgi.ini
user=root
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/uwsgi.stdout.log
stderr_logfile=/var/log/supervisor/uwsgi.stderr.log
redirect_stderr=true
```

## TroubleShooting

- **莫名其妙出现502错误，但是程序没有挂也确实没有错误日志**: 可以尝试设置uwsgi的`buffer-size=65535`缓存值，默认是4096，如果不行就在nginx上面设

##### 扩展阅读

- [uwsgitop](https://github.com/xrmx/uwsgitop)：可以像top命令那样打印`uwsgi`各个进程的实时状态