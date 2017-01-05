---
title: "SaltStack"
date: 2016-08-01 01:02:30
categories: server
---
# SaltStack

salt-minion是可以在单价运行的，相当于就在本机运行，以masterless方式运行。
master需要开启4505和4506端口

## 安装

    # 服务器端
    rpm -Uvh --force
    取消/etc/salt/master里面的注释interface: 0.0.0.0
    
    # 客户端
    vim /etc/salt/minion
    master: salt 取消注释，这里写master的地址
    id:     # 指定ID，如果不指定，默认应该是hostname
    log_file: /var/log/salt/minion # 取消注释，打开日志
    key_logfile: /var/log/salt/key # 取消注释，打开日志
    
    # 重启两个端过后
    在master端执行：
    salt-key -L     # 查看是否有证书签发请求
    salt-key -a 刚才查出来的ID # 同意签发证书
    
    # 测试，在master执行一条命令
    salt '刚才的id' cmd.run 'hostname'

# 创建state

	# 首先得有一个/srv/salt/top.sls，这是必须的
	base:				# 相当于仓库
	  '*':				# 对象名，*表示所有的minion
	    - webserver	# 自定义的资源名
	
	# 针对上面定义的每一个资源需要有相应的配置文件，例如/srv/salt/webserver.sls，以下配置来自http://blog.sctux.com/?p=278
	apache:				# 自定义的资源ID
	  pkg.installed:		# 包管理方式安装下面的包
	    - names:
	      - httpd
	      - httpd-devel
	  service.running:	# 模块名
	    - name: httpd	# 要启动的service
	    - enable: True	# 开机启动
	    - reload: True	# 监视下面的文件，如果有变动就重启
	    - watch:
	      - file: /var/www/html/index.html
	    - require:
	      - pkg: httpd	# 启动服务的前提是有这个包
	  file.managed:		# 模块名
	    - name: /var/www/html/index.html	# 目的文件
	    - source: salt://index.html		# 源文件
	    - user: apache						# 文件所有者
	    - group: root
	    - mode: 644
	    - backup: minion					# 改变之前备份
	    - require:
	      - pkg: httpd
	
	# 官网提供的另外的写法
	apache:
	  pkg:				# 声明state
	    - installed		# 声明函数

## 常用命令

	# 执行远程命令
	salt '目标' <function> [arguments]
	salt '*' test.ping	# ping一下所有的主机
	salt -G 'os:Ubuntu' test.ping # 可以指定某一种系统
	salt -E 'virtmach[0-9]' test.ping # 还能使用正则
	salt -L 'foo,bar,baz,quo' test.ping	# 多个minion
	salt -C 'G@os:Ubuntu and webser* or E@database.*' test.ping	# 反正就是想要的语法都有
	
	# 系统自带的函数
	salt '*' sys.doc
	salt '*' test.ping
	salt '*' cmd.run 'uname -a'	# 这就是执行命令
	salt '*' cmd.exec_code python 'import sys; print sys.version'
	salt '*' pip.install salt timeout=5 upgrade=True
	salt '*' state.highstate # 将配置发往minion