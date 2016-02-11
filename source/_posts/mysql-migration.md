---
title: "MySQL数据库目录存放位置迁移"
date: 2015-12-17 12:29:11
categories: 编程之路
---
迁移MySQL的数据库目录，其实并不难呀  

  1. 查看MySQL数据存放目录  


        > show variables like '\%dir\%';
    datadir的值就是mysql当前的存放目录，默认是/usr/local/mysql/data

  2. 进行迁移  


        service mysqld stop
    cp -r /usr/local/mysql/data/*  /path/to/mypath

  3. 修改配置  


        chown mysql:mysql -R /path/to/mypath




    # 修改/etc/my.cnf文件和/etc/init.d/mysqld文件，




    将datadir的值更改为新目录

  4. 重启服务  


        service mysqld start

﻿  
