---
title: "MySQL数据库升级过程"
date: 2016-01-06 08:06:50
categories: 编程之路
---
参考地址：<http://dev.mysql.com/doc/refman/5.6/en/linux-installation-debian.html>  
不知道为什么很多地方的官网都把一个完整的包打散了，然后完整包和分开的包放在同一级目录里，我也是醉了，最终我还是找到了正确的安装方法。  

  1. MySQL社区版官网下载地址：<http://dev.mysql.com/downloads/mysql/>  
需要注意的是，一定要下载结尾为.deb-bundle.tar的包，因为它包含了其它分开的包的所有数据

  2. 一步一步执行下列步骤就可以了：  


        sudo apt-get install libaio1   // 安装基本的依赖
    tar -xvf mysql-server_MVER-DVER_CPU.deb-bundle.tar   //解压
    sudo dpkg -i mysql-common_MVER-DVER_CPU.deb   // 安装common文件
    dpkg-preconfigure mysql-community-server_MVER-DVER_CPU.deb // 预配置，进行mysql的配置，这时候会要求输入root密码等
    sudo dpkg -i mysql-community-server_MVER-DVER_CPU.deb    // 安装mysql-server
    sudo dpkg -i mysql-community-client_MVER-DVER_CPU.deb    // 安装mysql-client
    sudo dpkg -i libmysqlclient18_MVER-DVER_CPU.deb   // 安装公共库

  3. 收尾  


        # 运行兼容检查工具，自动解决不兼容的问题
    命令行执行mysql_upgrade -uroot -pmysql




    不然可能会出现这些错误：
    MySQL unknown column 'password_last_changed'

  4. So Easy
