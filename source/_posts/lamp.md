---
title: "LAMP 手册"
date: 2016-07-28 22:52:39
updated: 2018-02-18 23:29:00
categories: server
---
# LAMP
Linux+Apache+MySQL+PHP，这是最流行也是我最熟悉的服务器架构了，其实网上有很多一键安装的版本，有些版本的linux甚至提供了_**apt
-get install lamp**_这样的一键安装程序，但是虽然他们是一个整体，但为了保证其独立性，我还是每次安装都会分别安装的。特别是某些框架或者是l
inux下的管理软件(比如现在所使用的禅道管理软件)在安装的时候经常都会有独立的打包程序，但我觉得那样会破坏apache等服务的独立性，所以独立安装，感觉舒
服一点。下面介绍一下安装过程：

## CentOS 6.x + Apache + Mariadb + PHP

<!--more-->

[编译方式安装](https://yhigu.wordpress.com/2016/03/02/install-latest-version-of-apach-and-php-on-centos-6-7-from-source-code/) 
[CentOS安装LNMP](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-centos-6) 
[包管理方式安装:](https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-centos-6) 
**apache**：

	sudo yum install httpd -y
	sudo service httpd start
**mariadb**：添加文件`/etc/yum.repos.d/MariaDB.repo`，内容如下：

	[mariadb]
	name = MariaDB
	baseurl = http://yum.mariadb.org/5.5/centos6-amd64/
	gpgkey = https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
	gpgcheck = 1
然后进行安装

	# 安装Mariadb
	sudo yum install MariaDB-server MariaDB-client
	# 启动数据库
	sudo /etc/init.d/mysql start
	
	# 如果出现无法更改数据库初始化密码的情况，可先stop mysql，然后通过下面的方式跳过验证来启动mysql即可更改密码：mysqld_safe --skip-grant-tables
**php**：

	sudo yum install php php-mysql
**自动启动**：

	sudo chkconfig httpd on
	sudo chkconfig mysqld on

# 环境：Ubuntu14.04 server

如果是CentOS 7可参考<http://www.howtoforge.com/apache_php_mysql_on_centos_7_lamp>

# MySQL安装



    apt-get install mysql-server mysql-client

# Apache安装



    apt-get install apache2

# PHP安装

最好把所需要的包都安装上，如果无法一次安装就依次安装吧



    apt-get install php5 libapache2-mod-php5 php5-json php5-gd php5-ldap php5-odbc php5-xmlrpc curl mcrypt php5-mysql php5-curl php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-ming php5-ps php5-pspell php5-recode php5-sqlite php5-tidy php5-xsl

以下是一些模块的具体功能：



    php5-mysql：操作MySQL数据库

安装完成以后，可以在_**/var/www/html**_中编写一个测试程序phpinfo.php：



    <?php
    phpinfo();
    ?>

最后在浏览器中输入<http://localhost/phpinfo.php，(如果是远程就直接把localhost替换成对应的IP即可)即可出现如下php
信息页面>：  
![](http://7xnc86.com1.z0.glb.clouddn.com/linux-install-lamp_0.jpg)  
**PS：**

mcrypt模块就是laravel所需要的模块，如果没有那么打开laravel就会出现**_Mcrypt PHP extension
required._**的错误，所以，必须进行声明。如果是后来才install mcrypt模块的那么还需要加载一下`sudo php5enmod
mcrypt`
