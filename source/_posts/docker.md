---
title: "Docker 手册"
date: 2015-12-10 07:51:39
updated: 2021-02-25 14:23:00
categories: tools
---
在Docker里面，镜像和容器是两个概念，镜像类似操作系统的ISO，而容器则是以该ISO为基础生成而来的。

##系统相关

[安装方法](https://docs.docker.com/install/linux/docker-ce/centos/#install-docker-ce-1)

`boot2docker`默认用户名是`docker`，密码是`tcuser`。

现在`docker for mac`不再依赖`virtualbox`等虚拟化软件，但是其采用了虚拟化技术，仍然是有虚拟机的，可以通过这条命令进入虚拟机查看``screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty` `

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

```shell
--add-host=host:IP	# 给hosts添加一行
-d						# 使容器在后台运行(detached mode)
--env-file ./env	# 指定环境变量所在的文件
-t					# 启用tty模式，有些镜像不启用tty模式的话执行完第一条命令后就立马退出
--name haofly			# 给容器命名
--net=host				# 网络模式，host表示容器不会获得独立的Network Namspace，而是和宿主机公用一个Network Namespace。容器将不会虚拟网卡，配置自己的IP，而是使用宿主机器的IP和端口；none表示没有网络；bridge是docker默认的网络设置；container:NAME_or_ID表示container模式，指定新创建的容器和已经存在的一个容器共享一个Network Namespace，和指定的容器共享IP、端口范围等。
--restart=no			# 容器的重启模式，no表示不自动重启，on-failure表示当容器推出码为非零的时候自动重启，always表示总是自动重启，docker重启后也会自动重启，unless-stopped表示只有在docker重启时不重启，其他时候都自动重启。
--rm					# 如果有重名的容器，则删除原有容器再新建，前提是原有容器必须是停止的状态。并且加入了这个参数以后如果docker重启或者容器exit，该容器都会被删除
-v /etc/test/:/etc/internal/test	# 将宿主机的/etc/test目录挂载到容器内部的/etc/internal/test目录
```

#### 启动命令

```shell
# docker run命令用于从镜像创建一个容器
# -i参数表示将STDIN持续打开而不管是否已经attached
docker run -t -i ubuntu:14.04.1      # 从ubuntu:14.04.1镜像创建一个容器
docker run -t -i ubuntu:14.04.1 /bin/bash # 从ubuntu:14.04.1创建容器并在容器中执行命令
docker run -t -i -d ubuntu:14.04.1  # 创建容器并作为daemon运行
docker run -t -i -p 80:80 ubuntu:14.04.1 # 创建容器并映射容器的80端口到主机的80端口
docker run -t -i -p 127.0.0.1:80:80 ubuntu:14.04.1 # 指定端口映射的IP，默认是0.0.0.0
docker run -t -i -v /etc/hehe/:/etc/haha ubuntu:14.04.1 # 创建容器并映射主机的/etc/hehe目录到容器的/etc/haha目录
docker run -t -i
exit # 退出容器
docker logs 容器名称  # 获取容器的输出信息，但是通过docker exec进入容器的时候，其标准输出并未被主进程相关联，所以docker exec所执行进程的标准输出不会进入容器的日志文件。即docker容器的日志只负责应用本身的标准输出，不包括docker exec衍生进程的标准输出(http://docs.daocloud.io/allen-docker/docker-exec)
docker run -t -i -d -p 80:80 -v /home/haofly/docker/test/mysite:/mysite django-apache:latest # 我当前机器上的一条执行自己创建的镜像的命令
```

## 容器操作

```shell
docker start	#和docker run后面参数一样，只是它是重启容器，而docker run是创建容器
docker stop 容器名/ID	#停止某个容器
docker attach 容器名/ID	# 直接进入容器，查看容器当前的标准输出
docker exec -it 容器名 bash  # ssh进一个容器
docker exec -it 容器名 sh -c "command"	# 让容器执行某条命令
docker inspect 容器名	# 查看一个容器的详细信息
docker stats # 查看所有容器的运行时信息，包括cpu占用，内存占用，进程ID等
docker cp ./xx 容器ID:/www/	# 将宿主机的文件拷贝到运行中的容器
docker update --restart=no 容器名	# 禁止容器自动重启
```

## Dockerfile

Dockerfile是一个制作镜像的脚本工具，通过它可以比直接拷贝docker容器更方便地迁移，只需要拷贝一个Dockerfile然后在本地构建一个即可。

```shell
docker build -t local:mine .
docker build --add-host=google.com:8.8.8.8 -t local:latest .	# docker build阶段的add-host仅仅用于构建阶段，这个hosts是不会打包进镜像的
```
- 在Dockerfile中应该尽可能晚的添加应用程序源代码，才能充分利用layer的缓存。这意味着`COPY`这种命令尽量放到后面，并且尽量只`COPY`需要的文件
- 尽量合并RUN命令，特别是`yum`等的更新安装命令，并且给加上`–no-install-recommends`参数不安装不需要的依赖`apt-get -y install --no-install-recommends 包名`
- 为渐小镜像大小可以移除安装缓存，`apt-get -y vim && rm -rf /var/lib/apt/lists/*`或者`yum clean all`

Dockerfile的语法说明:

```SHELL
#: Dockerfile中用#来进行注释
FROM: 指定基于哪个镜像创建,这样会先pull该镜像.例如`FROM ubuntu:14.04.1`
MAINTAINER: 指定创建作者的信息.例如`MAINTAINER haofly <haoflynet@gmail.com>`
ADD: 将指定的主机目录中的文件代替要构建的镜像中的文件,这条命令通常用于镜像源的更换,例如`ADD sources.list_aliyun /etc/apt/sources.list`,这样,镜像中的/etc/apt/sources.list文件就被sources.list_aliyun文件替代了。最好用COPY，因为ADD可能会做一些其他的功能，例如add一个tar.gz包时会自动解压
COPY: 和ADD功能一样，不过ADD指令还支持通过URL从远程服务器读取资源并复制到镜像中。不过远程资源其实更推荐用RUN wget
RUN: 执行一条shell命令
EXPOSE: 暴露什么端口给主机,需要注意的是,即使指定了,也得在docker run的时候通过-p参数执行端口的映射
WORKDIR: 切换工作目录,这样下面的CMD等就可以在新的目录执行，并且每次exec进入容器的时候默认目录也会被切换为这个
CMD: 一般写于最后,因为它是容器启动时才执行的命令,并且无论写多少,都只执行最后那一条,一般用于容器中镜像的启动,例如`CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]`,当然,也可不加括号和引号,直接用shell的方式写一条命令.但是如果docker run 中指定了命令过后,CMD将不被执行
ENTRYPOINT: 和CMD类似,但是如果docker run中指定了命令,它仍然会被执行
ENV: 指定环境变量，在dockerfile里面使用export是没用的
ARG: 指定参数，比如ockerfile里面定义了`ARG JAVA_HOME`，那么可以在构建的时候用docker build JAVA_HOME=$JAVA_HOME对该参数进行赋值
ONBUILD: 后面跟的是其他的普通指令，例如ONBUILDI RUN mkdir test，实际上它是创建了一个模版景象，后续根据该景象创建的子镜像不用重复写它后面的指令，就会执行该指令了
```

## Docker Compose 

Docker Compose主要用于快速在集群中部署分布式应用，主要有两个概念:

- 服务(Service): 一个应用的容器，实际上可以包括若干个运行相同镜像的容器实例
- 项目(Project): 由一组关联的应用容器组成的一个完整业务单元

linux需要单独安装该工具，[其他平台安装教程](<https://docs.docker.com/compose/install/#install-compose>)

```json
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

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
    privileged: true		# 开启特权模式
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
        
python:
		image: python
		tty: true		# 有些镜像启动时候不用tty会直接退出
```

### docker-compose常用命令

```shell
docker-compose stop		# 暂停所有容器
docker-compose up -d	# start所有的容器
docker-compose rm -f 	# 删除所有容器
docker-compose ps 		# 列出所有的容器
```

### 网络设置

```yam
networks:	# 与version同级
  default:
    external:
      name: mynet # 在外部自己创建的network
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

## 容器网络

更改默认网桥`bridge`的网段请参考本文`TroubleShooting`

```shell
docker network ls		# 列出所有的网桥
docker network prune	# 删除没有使用的网桥
docker network inspect name	# 查看某个网桥的详细信息
docker network rm name		# 删除某个网桥
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

- `AWS`的数据库跟`Mariadb`数据库有些地方不兼容，最好用`MySQL`

```shell
docker run --name some-mariadb -v /Users/haofly/workspace/share:/share --net host -e MYSQL_ROOT_PASSWORD=mysql -d mariadb:tag	# 开启一个mysql容器，可通过exec bash进入容器内

docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql -p 3306:3306 -d mysql:5.7.26
```
### PHP容器

- 如果网络有问题，那么可以在`https://github.com/richarvey/nginx-php-fpm`项目中的Dockerfile手动创建镜像

```shell
docker run --name php-apache -v /Users/haofly/workspace/share/yangqing:/var/www/html -p 80:80 --link some-mysql:mysql -d b664eb500b48 # 这是php-apache，并且连接mysql容器,如果要安装mysql扩展需要在Dockerfile里面去安装

apt-get install libpng-dev -y && docker-php-ext-install gd	# 安装GD扩展
apt-get install libzip-dev zlib1g-dev && docker-php-ext-install zip # 安装zip扩展
apt-get install libxml2-dev && docker-php-ext-install xml # 安装xml扩展
docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable pdo_mysql	# 安装Mysql扩展
```
### 在PHP容器中安装PHP扩展

```shell
docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable pdo_mysql	# mysql扩展
```

### CentOS容器

```shell
docker run -it -v /Users/haofly/workspace/dbm:/share --name dbm -d index.alauda.cn/library/centos:centos6.6 /bin/bash
docker run -it -v /Users/haofly/workspace/share:/share --name salt_client --privileged 750109855bc0 /usr/sbin/init	# 对于7.x，如果想在容器里执行systemctl，需要添加privileged参数，并且后面应该用init
```

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

### Postgres容器

```shell
docker run --name postgres -e POSTGRES_PASSWORD=the_password -p 5432:5432 -d postgres
```

## TroubleShooting

- **docker动态添加端口映射**

        方法一：此方法据说不安全，就是在run的时候--net host
        方法二：在virtualbox中添加映射，这个其实没试验过

- **官方mysql镜像打开二进制日志**

    ```shell
    docker run -v /var/lib/mysql:/var/lib/mysql \
                mysql:5.7 \
                mysqld \
                --data \
                --user=mysql \
                --server-id=1 \
                --log-bin=/var/log/mysql/mysql-bin.log \
                --binlog_do_db=test
    ```

- **CentOS7容器无法使用systemctl命令提示`Failed to get D-Bus connection: No connection to service manager.`/ 无法设置交换分区等错误**。新版本默认不会提供特权模式，容器内部的root用户并不是真正的root用户，有很多权限都没有，可以在创建容器的时候添加特权模式`docker run --privileged XXX /usr/sbin/init`

- **出现`Exit status 255`错误**，可能是虚拟机长期开启未关闭导致的，进入virtualBox将该docker machine关闭即可再次重新打开了

- **时区不对: 不是相差8个小时这么简单，反正很乱**
  在新建容器的时候加上这个参数` -v /etc/localtime:/etc/localtime:ro` 

- **树莓派安装docker后出现错误`libapparmor.so.1: cannot open shared object file: No such file or directory`**，需要执行`apt-get install lxc`

- **更换docker网段**: 目前存在的问题是docker容器的网段为`172.17.0.1/24`，但是公司的内网也是这个网段，导致冲突过后，我在我的容器里面ping不通别人的机器，所以就尝试着在mac上更换docker的默认网段。以前的版本是需要直接去修改`~/Library/Containers/com.docker.docker/Data/database/com.docker.driver.amd64-linux/etc/docker/daemon.json`，但是新版本已经不能直接在那里修改了，修改网段更加方便了。直接在`Preferences->Daemon->Advanced`里面的json文件进行修改(注意不是直接Preferences->Advanced)。

  ```json
  {
    "debug" : true,
    "experimental" : true,
    "bip" : "192.168.1.5/24"	// 默认网段是172.17.0.0/16，这里修改为一个不和内网冲突的网段即可
  }
  ```

- **Mac下`~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux`目录占用内存过大**: 目测是一个一直没有被修复的bug，是由于镜像反复拉，容器反复删除重建，但是存储从来不释放造成的，我现在的解决方法是把想要的镜像拉下来到处到存储中去，以后要使用直接拉取，这样避免了每次pull不下来的时候重新pull导致存储不释放的问题

- **阿里源**: 一般都是jessie版本，但是有些镜像的维护者可能会修改为一个比较小众的版本，可能导致某些包没有，这时候修改版本即可。

    ```shell
    # 基本上都是jessie，/etc/apt/sources.list
    deb http://mirrors.aliyun.com/debian jessie main
    deb http://mirrors.aliyun.com/debian jessie-updates main
    deb http://mirrors.aliyun.com/debian-security jessie/updates main
    
    # alpine版本，/etc/apk/repositories
    http://mirrors.aliyun.com/alpine/v3.7/main
    http://mirrors.aliyun.com/alpine/v3.7/community
    @testing http://mirrors.aliyun.com/alpine/edge/testing
    ```

- **windows找不到`/var/run/docker.sock`**: 在最新的windows版本的docker里面，直接找是找不到这个文件的，需要添加环境变量`COMPOSE_CONVERT_WINDOWS_PATHS = 1`

- **Apache相关的容器可能意外退出后重新启动不起来**，原因是意外退出，pid文件还在，需要在启动的时候添加一条命令: `rm -f /var/run/apache2/apache2.pid`

- **dockerfile长文本**

    ```shell
    echo "第一行\n\
    第二行\n\
    " > /etc/conf
    ```

- **容器内部无网络**: 首先可以使用`--net=host`使用主机的网络来检查是否是容器内部的网络问题，如果使用该参数依然无法访问网络，那么使用`ping`直接`ping`IP地址，如果IP通但是域名不通，那就是dns的问题，去查看一下容器的dns配置，一般目录是在`/etc/resolv.conf`

- **exited with code 0** 容器没有任何报错就退出，日志也没有。有可能是因为该镜像的启动命令不是`daemon`方式，容器启动完成后立马就退出了，这个时候可以参照上面的`-t`或者`docker-compose`里面的`tty: true`进行设置

- **启动docker出现错误Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock dial unix /var/run/docker.sock: connect: permission denied**: 可能权限有问题，可以这样修复:

    ```shell
    sudo groupadd docker
    sudo usermod -aG docker ${USER}
    # 然后该用户重新登录即可
    ```

    
