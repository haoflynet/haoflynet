---
title: "LEMP: Linux, Nginx, MySQL, PHP环境"
date: 2016-06-22 22:52:39
categories: system
---
# LEMP: Linux, Nginx, MySQL, PHP环境

# 安装步骤

CentOS 6.x

```shell
yum install epel-release -y

# MySQL
yum install mysql-server -y
/etc/init.d/mysqld restart
/usr/bin/mysql_secure_installation # 初始化设置数据库

# Nginx
yum install nginx -y
/etc/init.d/nginx start

# PHP
yum install php-fpm php-mysql
vim /etc/php.ini，将cgi.fix_pathinfo=1改为cgi.fix_pathinfo=0
vim /etc/php-fpm.d/www.conf将apache用户更改为nginx用户
user = nginx
group = nginx

service php-fpm restart
service nginx restart

# 开机启动
chkconfig --levels 235 mysqld on
chkconfig --levels 235 nginx on
chkconfig --levels 235 php-fpm on


```

