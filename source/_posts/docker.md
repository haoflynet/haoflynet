---
title: "Docker"
date: 2015-12-10 07:51:39
updated: 2018-02-12 18:22:00
categories: tools
---
# Docker 使用指南
需要注意的是在Docker里面，镜像和容器是两个概念，镜像类似操作系统的ISO，而容器则是以该ISO为基础生成而来的。

##系统相关

	boot2docker默认用户名是docker，密码是tcuser
## 镜像和容器

```shell
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
```

## 创建容器

<!--more-->

#### 启动参数

```tex
--add-host="host:IP"	# 给hosts添加一行
-d						# 使容器在后台运行(detached mode)
--name haofly			# 给容器命名
--net=host				# 网络模式，host表示容器不会获得独立的Network Namspace，而是和宿主机公用一个Network Namespace。容器将不会虚拟网卡，配置自己的IP，而是使用宿主机器的IP和端口；none表示没有网络；bridge是docker默认的网络设置；container:NAME_or_ID表示container模式，指定新创建的容器和已经存在的一个容器共享一个Network Namespace，和指定的容器共享IP、端口范围等。
--restart=no			# 容器的重启模式，no表示不自动重启，on-failure表示当容器推出码为非零的时候自动重启，always表示总是自动重启，docker重启后也会自动重启，unless-stopped表示只有在docker重启时不重启，其他时候都自动重启。
-v /etc/test/:/etc/internal/test	# 将宿主机的/etc/test目录挂载到容器内部的/etc/internal/test目录
```

#### 启动命令

	# docker run命令用于从镜像创建一个容器
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

## Dockerfile

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
ONBUILD: 后面跟的是其他的普通指令，例如ONBUILDI RUN mkdir test，实际上它是创建了一个模版景象，后续根据该景象创建的子镜像不用重复写它后面的指令，就会执行该指令了
```

## Docker Compose 

Docker Compose主要用于快速在集群中部署分布式应用，主要有两个概念:

- 服务(Service): 一个应用的容器，实际上可以包括若干个运行相同镜像的容器实例
- 项目(Project): 由一组关联的应用容器组成的一个完整业务单元

一个例子:

```shell
weba:				# 给容器取名
    build: ./web	# 如果容器需要使用特定的Dockerfile可以在这里指定
    expose:			# 暴露的接口
        - 80

webb:				# 第二个容器
    build: ./web
    extra_hosts:
      - "haofly.net:172.0.0.1"	# 添加hosts
    command: bash -c "python manage.py migrate && python manage.py runserver"	# 如果要在开机之后执行命令可以这样子做，这是每次开机都会执行这个操作，并且是覆盖了原有的开机启动命令。需要注意的是，有些容器在启动时候会开启一个守护进程，如果该进程没有启动那么容器最后会退出，如果有这样的命令也许要在这里写上
    command: >
        bash -c "python manage.py migrate
        && python manage.py runserver"		# 也可以这样分行写
    expose:
        - 80

haproxy:			# 第三方容器
    image: haproxy:latest	# 直接从镜像启动，而不是Dockerfile启动
    volumes:				# 挂载的卷
        - ./haproxy:/haproxy-override
    links:					# 连接另外的容器
        - weba
        - webb:test.haofly.net	# 分配一个别名，都能ping通的
        - webc
    ports:					# 映射的端口
        - "80:80"
    expose:					# 暴露的端口
        - "80"
```

docker-compose常用命令

```shell
docker-compose stop		# 暂停所有容器
docker-compose up -d	# start所有的容器
docker-compose rm -f 	# 删除所有容器
docker-compose ps 		# 列出所有的容器
```

## 迁移

```shell
docker save -o ubuntu_14.04.tar ubuntu:14.04  # 导出镜像到本地
docker load < ubuntu_14.04.tar   #　加载本地镜像
docker export 容器ID > ubuntu.tar # 导出容器快照到本地
docker import # 导入本地快照
docker commit -m "说明信息" -a "用户信息" # 更改容器后直接将容器作为镜像

# 如果要将本地镜像推送到目标仓库，这样做
docker login hub.haofly.net	# 先登录
docker tab image_id hub.haofly.net/haofly/test:tag	# 更改名称
docker push hub.haofly.net/haofly/test:tag	# 推送
```

## 常用容器/镜像

### Alpine

是一个非常简单的镜像，本身只有几兆，包含了linux最简单的内核，并且功能十分强大。很多的基础镜像都是基于它。当然，有一点特别注意，它没有自带apt-get，也没有bash(sh代替)。不过还好，也能使用阿里的镜像源。这里有它里面的一些基本操作

```shell
apk add --update	# 更新源
apt add --no-cache python	# 安装软件
apt del python			# 删除软件
```

### MySQL/Mariadb容器
	docker run --name some-mariadb -v /Users/haofly/workspace/share:/share --net host -e MYSQL_ROOT_PASSWORD=mysql -d mariadb:tag	# 开启一个mysql容器，可通过exec bash进入容器内
### PHP容器
	docker run --name php-apache -v /Users/haofly/workspace/share/yangqing:/var/www/html -p 80:80 --link some-mysql:mysql -d b664eb500b48 # 这是php-apache，并且连接mysql容器,如果要安装mysql扩展需要在Dockerfile里面去安装
### CentOS容器
	docker run -it -v /Users/haofly/workspace/dbm:/share --name dbm -d index.alauda.cn/library/centos:centos6.6 /bin/bash
	docker run -it -v /Users/haofly/workspace/share:/share --name salt_client --privileged 750109855bc0 /usr/sbin/init	# 对于7.x，如果想在容器里执行systemctl，需要添加privileged参数，并且后面应该用init

### NodeJS容器

```shell
docker run -it -v /Users/haofly/workspace:/workspace -p 4000:4000 -p 4001:4001 --name node -d node:latest /bin/bash
```

### Nginx代理

太好用了，这个

```shell
# 首先，直接拉下这个镜像并创建容器
docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock:ro  --name nginx-proxy jwilder/nginx-proxy:latest

docker run -it -e VIRTUAL_HOST=dev.haofly.net --name dev -d eboraas/laravel # 通过-e VIRTUAL_HOST指定域名，然后把该域名加到hosts里面127.0.0.1  dev.haofly.net，即可访问了，连nginx的配置都不用改
```

## TroubleShooting

- **docker动态添加端口映射**

        方法一：此方法据说不安全，就是在run的时候--net host
        方法二：在virtualbox中添加映射，这个其实没试验过

- **官方mysql镜像打开二进制日志**

        docker run -v /var/lib/mysql:/var/lib/mysql \
                    mysql:5.7 \
                    mysqld \
                    --data \
                    --user=mysql \
                    --server-id=1 \
                    --log-bin=/var/log/mysql/mysql-bin.log \
                    --binlog_do_db=test

- **CentOS7容器无法使用systemctl命令**，提示`Failed to get D-Bus connection: No connection to service manager.`不知道为何不能支持，但可以有其他方法，在创建容器的时候使用如下命令`docker run --privileged XXX /usr/sbin/init`

- **出现`Exit status 255`错误**，可能是虚拟机长期开启未关闭导致的，进入virtualBox将该docker machine关闭即可再次重新打开了

- **时区不对: 不是相差8个小时这么简单，反正很乱**
  在新建容器的时候加上这个参数` -v /etc/localtime:/etc/localtime:ro` 

- **树莓派安装docker后出现错误`libapparmor.so.1: cannot open shared object file: No such file or directory`**，需要执行`apt-get install lxc`

- **更换docker网段**: 目前存在的问题是docker容器的网段为`172.17.0.1/24`，但是公司的内网也是这个网段，导致冲突过后，我在我的容器里面ping不通别人的机器，所以就尝试着在mac上更换docker的默认网段

  ```shell
  cd /Users/haofly/Library/Containers/com.docker.docker/Data/database/com.docker.driver.amd64-linux	# 没错，这里默认是一个git仓库
  vim etc/docker/daemon.json		# 在json文件里面添加一个字段"bip":"172.18.0.1/24"
  git add etc/docker/daemon.json && git commit -m "configure bip"	# 提交过后，docker会自动重启，重启过后，所有的容器以及新开的容器就都会是新的网段了，终于能ping通了
  ```
  **2017年3月份最近更新的docker里面发现已经没有上面那个文件夹了，所以这里我用了另外一种方式**，而这时候我才知道为什么我的docker又出现了网络不通的问题，原因是`docker-compse`启动的容器组会新建一个单独的网桥，而这个网桥的网段每一个都不一样，建多了几个过后就发现，又和内网冲突了。。。

  ```shell
  docker network ls		# 列出所有的网桥
  docker network prune	# 删除没有使用的网桥
  docker network info name	# 查看某个网桥的详细信息
  docker network rm name		# 删除某个网桥
  ```

  删除完有冲突的网桥过后，新建`docker-compose`即可。

- Mac下`~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux`目录占用内存过大**: 目测是一个一直没有被修复的bug，是由于镜像反复拉，容器反复删除重建，但是存储从来不释放造成的，我现在的解决方法是把想要的镜像拉下来到处到存储中去，以后要使用直接拉取，这样避免了每次pull不下来的时候重新pull导致存储不释放的问题

- **阿里源**: 一般都是jessie版本，但是有些镜像的维护者可能会修改为一个比较小众的版本，可能导致某些包没有，这时候修改版本即可。

    ```shell
    # 基本上都是jessie，/etc/apt/sources.list
    deb http://mirrors.aliyun.com/debian jessie main
    deb http://mirrors.aliyun.com/debian jessie-updates main
    deb http://mirrors.aliyun.com/debian-security jessie/updates main

    # alpine版本，/etc/apk/repositories
    http://mirrors.aliyun.com/alpine/v3.4/main
    http://mirrors.aliyun.com/alpine/v3.4/community
    @testing http://mirrors.aliyun.com/alpine/edge/testing
    ```

- ​


