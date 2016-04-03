---
title: "MySQL单机多实例"
date: 2016-03-09 14:37:29
categories: 编程之路
---
这是我们公司的实习内容之一，以前一直以为在单机上部署多个MySQL就是起多个进程就行了，too yuang too simple，原来MySQL默认提供了单机多实例功能的。  
配置和使用过程如下(CentOS)：

1. `mysqld_multi --example`这个可以直接查看MySQL提供的多实例配置文件的配置内容样例，基本上可以直接拿来就用
2. `mysql_install_db --datadir=/tmp/mariadb/data1`以这种方式创建多个数据库存放目录，**一定要注意不要放在/root目录下，不然会出现什么Aria无法加载的情况**
3. `vim /etc/my.cnf`内容如下：

        [mysqld_multi]
        mysqld     = /usr/bin/mysqld_safe
        mysqladmin = /usr/bin/mysqladmin
        user       = root # mysql
        password   = mysql

        [mysqld2]
        socket     = /tmp/mysql.sock2
        port       = 3307
        pid-file   = /tmp/hostname.pid2
        datadir    = /tmp/data1
        user       = mysql

        [mysqld3]
        socket     = /tmp/mysql.sock3
        port       = 3308
        pid-file   = /tmp/hostname.pid3
        datadir    = /tmp/data2
        user       = mysql
4. 启动实例

        mysqld_multi start      # 启动实例
        mysqld_multi stop
        mysqld_multi report     # 查看两个实例运行状态
w
另外，实例的日志文件默认是在实例文件夹下的`localhost.localdomain.err`文件里，启动完实例后，还要连接实例进行初始密码设置
