---
title: "Docker"
date: 2016-08-07 07:51:39
categories: tools
---
# Docker 使用指南
需要注意的是在Docker里面，镜像和容器是两个概念，镜像类似操作系统的ISO，而容器则是以该ISO为基础生成而来的。

##系统相关

	boot2docker默认用户名是docker，密码是tcuser
## 镜像和容器

	docker pull ubuntu:14.04.1 # 拉取官方镜像
	docker pull registry.hub.docker.com/ubuntu:14.04  # 拉取特定网站的镜像
	docker pull index.alauda.cn/library/centos:centos6.6 # 灵雀云的镜像，镜像中心https://hub.alauda.cn/
	docker images # 列出所有的镜像
	
	docker ps    		# 列出正在运行的容器
	docker ps -a -s	# 列出所有容器,-s可以列出大小信息
	docker ps -q 		# 只列出容器的ID
	
	docker rm # 删除容器
	docker rmi # 删除镜像
	
	docker tag id name:tag	# 给镜像更改名称


## 创建容器

	# docker run命令用于从镜像创建一个容器
	# --add-host="host:IP"	# 给hosts添加一行，这个非常有用
	# -d：使容器在后台运行(detached mode)，不加则默认是前台模式，启动后会将当前命令行窗口挂在到容器中
	# --name：指定名称，如--name haofly
	# -t：分配一个伪终端
	# -i参数表示将STDIN持续打开而不管是否已经attached
	docker run -t -i ubuntu:14.04.1      # 从ubuntu:14.04.1镜像创建一个容器
	docker run -t -i ubuntu:14.04.1 /bin/bash # 从ubuntu:14.04.1创建容器并在容器中执行命令
	docker run -t -i -d ubuntu:14.04.1  # 创建容器并作为daemon运行
	docker run -t -i -p 80:80 ubuntu:14.04.1 # 创建容器并映射容器的80端口到主机的80端口
	docker run -t -i -v /etc/hehe/:/etc/haha ubuntu:14.04.1 # 创建容器并映射主机的/etc/hehe目录到容器的/etc/haha目录
	docker run -t -i
	exit # 退出容器
	docker logs 容器名称  # 获取容器的输出信息，但是通过docker exec进入容器的时候，其标准输出并未被主进程相关联，所以docker exec所执行进程的标准输出不会进入容器的日志文件。即docker容器的日志只负责应用本身的标准输出，不包括docker exec衍生进程的标准输出(http://docs.daocloud.io/allen-docker/docker-exec)
	docker run -t -i -d -p 80:80 -v /home/haofly/docker/test/mysite:/mysite django-apache:latest # 我当前机器上的一条执行自己创建的镜像的命令

## 容器操作

	docker start：和docker run后面参数一样，只是它是重启容器，而docker run是创建容器
	docker stop 容器名/ID：停止某个容器
	docker attach 容器名/ID：直接进入容器，查看容器当前的标准输出
	docker exec -it 容器名 bash  # ssh进一个容器
	docker inspect 容器名：查看一个容器的详细信息

## 通过Dockerfile创建镜像
Dockerfile是一个制作镜像的脚本工具，通过它可以比直接拷贝docker容器更方便地迁移，只需要拷贝一个Dockerfile然后在本地构建一个即可。

	docker build -t local:mine .
Dockerfile的语法说明:

```SHELL
#: Dockerfile中用#来进行注释
FROM: 指定基于哪个镜像创建,这样会先pull该镜像.例如`FROM ubuntu:14.04.1`
MAINTAINER: 指定创建作者的信息.例如`MAINTAINER haofly <haoflynet@gmail.com>`
ADD: 将指定的主机目录中的文件代替要构建的镜像中的文件,这条命令通常用于镜像源的更换,例如`ADD sources.list_aliyun /etc/apt/sources.list`,这样,镜像中的/etc/apt/sources.list文件就被sources.list_aliyun文件替代了
RUN: 执行一条shell命令
EXPOSE: 暴露什么端口给主机,需要注意的是,即使指定了,也得在docker run的时候通过-p参数执行端口的映射
WORKDIR: 切换工作目录,这样下面的CMD等就可以在新的目录执行
CMD: 一般写于最后,因为它是容器启动时才执行的命令,并且无论写多少,都只执行最后那一条,一般用于容器中镜像的启动,例如`CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]`,当然,也可不加括号和引号,直接用shell的方式写一条命令.但是如果docker run 中指定了命令过后,CMD将不被执行
ENTRYPOINT: 和CMD类似,但是如果docker run中指定了命令,它仍然会被执行
ENV: 指定环境变量
ARG: 指定参数，比如ockerfile里面定义了`ARG JAVA_HOME`，那么可以在构建的时候用docker build JAVA_HOME=$JAVA_HOME对该参数进行赋值
```

## 迁移

```shell
docker save -o ubuntu_14.04.tar ubuntu:14.04  # 导出镜像到本地
docker load < ubuntu_14.04.tar   #　加载本地镜像
docker export 容器ID > ubuntu.tar # 导出容器快照到本地
docker import # 导入本地快照

# 如果要将本地镜像推送到目标仓库，这样做
docker login hub.haofly.net	# 先登录
docker tab image_id hub.haofly.net/haofly/test:tag	# 更改名称
docker push hub.haofly.net/haofly/test:tag	# 推送
```

## 常用容器/镜像
### MySQL/Mariadb容器
	docker run --name some-mariadb -v /Users/haofly/workspace/share:/share --net host -e MYSQL_ROOT_PASSWORD=mysql -d mariadb:tag	# 开启一个mysql容器，可通过exec bash进入容器内
### PHP容器
	docker run --name php-apache -v /Users/haofly/workspace/share/yangqing:/var/www/html -p 80:80 --link some-mysql:mysql -d b664eb500b48 # 这是php-apache，并且连接mysql容器,如果要安装mysql扩展需要在Dockerfile里面去安装
### CentOS容器
	docker run -it -v /Users/haofly/workspace/ZBJ_dbm:/share --name dbm -d index.alauda.cn/library/centos:centos6.6 /bin/bash
	docker run -it -v /Users/haofly/workspace/share:/share --name salt_client --privileged 750109855bc0 /usr/sbin/init	# 对于7.x，如果想在容器里执行systemctl，需要添加privileged参数，并且后面应该用init

### Nginx代理

太好用了，这个

```shell
# 首先，直接拉下这个镜像并创建容器
docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock:ro  --name nginx-proxy jwilder/nginx-proxy:latest

docker run -it -e VIRTUAL_HOST=dev.haofly.net --name dev -d eboraas/laravel # 通过-e VIRTUAL_HOST指定域名，然后把该域名加到hosts里面127.0.0.1  dev.haofly.net，即可访问了，连nginx的配置都不用改
```

## TroubleShooting

- 动态添加端口映射

        方法一：此方法据说不安全，就是在run的时候--net host
        方法二：在virtualbox中添加映射，这个其实没试验过

- 官方mysql镜像打开二进制日志

        docker run -v /var/lib/mysql:/var/lib/mysql \
                    mysql:5.7 \
                    mysqld \
                    --data \
                    --user=mysql \
                    --server-id=1 \
                    --log-bin=/var/log/mysql/mysql-bin.log \
                    --binlog_do_db=test

- CentOS7容器无法使用systemctl命令，提示`Failed to get D-Bus connection: No connection to service manager.`不知道为何不能支持，但可以有其他方法，在创建容器的时候使用如下命令`docker run --privileged XXX /usr/sbin/init`

- 出现`Exit status 255`错误，可能是虚拟机长期开启未关闭导致的，进入virtualBox将该docker machine关闭即可再次重新打开了

- **时区不对: 不是相差8个小时这么简单，反正很乱**
  在新建容器的时候加上这个参数` -v /etc/localtime:/etc/localtime:ro` 

- 树莓派安装后出现错误`libapparmor.so.1: cannot open shared object file: No such file or directory`，需要执行`apt-get install lxc`

- ​








	  * docker commit : 更改容器后要把更改后的容器作为一个镜像,注意这里和直接用Dockerfile不一样

	        docker commit -m "说明信息" -a "用户信息

	  * docker save : 导出镜像到本地

	        docker save -o ubuntu_14.04.1.tar ubuntu:14.04.1

	  * docker load : 加载本地镜像,导入用docker save命令保存的本地镜像

	        docker load < ubuntu_14.04.1.tar

	  * docker export : 导出容器快照到本地

	        docker export 容器ID > ubuntu.tar

	  * docker import : 导出本地快照
	  * docker kill : 杀死正在运行的容器,后跟容器ID
	
	        docker kill $(docker ps -a -q)
	
	  * docker rm : 移除容器,后跟容器ID
	
	        docker rm $(docker ps -a -q)  # 删除所有已停止的容器
	
	  * docker rmi : 删除镜像,后跟镜像名称或ID
	
	        docker rmi $(docker images -q -a)
	
	  *
		---
		title: "Docker 之Dockerfile的使用"
		date: 2015-02-01 08:58:06
		categories: docker
		---
		使用Dockerfile可以方便地build自己的Docker镜像,并且Dockerfile语法简单,清晰明了.Dockerfile中每一条指令都对应镜像中
		的一层,后面的层会依赖前面的层,每一层都会有一个唯一的ID,这样前半部分都相同的Dockerfile那前半部分构建时都一样,会自动复用.
	
		一般,如果Dockerfile就位于当前目录,那么可以直接执行一下命令进行构建(-t参数指定REPOSITORY名称,默认的Tag为latest)`dock
		er build -t="haofly" .`

