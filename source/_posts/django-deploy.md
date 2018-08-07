---
title: "使用nginx+uWSGI部署Django应用"
date: 2018-08-04 21:32:00
updated: 2018-08-06 15:19:00
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
  
          # 下面的配置可以保存成文件然后include
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

  ```tex
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
  # maximum number of worker processes
  processes       = 10
  # the socket (use the full path to be safef
  socket          = /data/swy-api/haidaohai/swy-api.sock
  
  # ... with appropriate permissions - may be needed
  chmod-socket    = 666		# 修改权限，以防出现connect() to unix:///path/to/your/mysite/mysite.sock failed (13: Permission
  denied)错误
  # clear environment on exit
  vacuum          = true
  
  py-autoreload = 1		# python代码变更后自动重启
  ```



综上，其实是和`php-fpm`部署的方式类似，使用wsgi协议启动应用，然后nginx直接获取其socket就行了。