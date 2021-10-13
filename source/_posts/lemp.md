---
title: "LEMP: Linux, Nginx, MySQL, PHP-FPM环境"
date: 2016-06-22 22:52:39
updated: 2021-03-04 16:00:00
categories: system
---
# LEMP: Linux, Nginx, MySQL, PHP环境

```shell
# 依赖安装
yum install epel-release gcc automake autoconf libtool make gcc gcc-c++ glibc-y

# MySQL
yum install mysql-server -y
/etc/init.d/mysqld restart
/usr/bin/mysql_secure_installation # 初始化设置数据库

# Nginx
yum install nginx -y
/etc/init.d/nginx start

# PHP
add-apt-repository universe && apt-get install php-fpm php-mysql	# for ubuntu
yum install php-fpm php-mysql	# for centos
vim /etc/php.ini，将cgi.fix_pathinfo=1改为cgi.fix_pathinfo=0
vim /etc/php-fpm.d/www.conf将apache用户更改为nginx用户
user = nginx
group = nginx

service php-fpm restart	# 如果php-fpm: unrecognized service，可以在/usr/lib/systemd/system/目录下看具体的服务名
service nginx restart

# 开机启动
systemctl enable mysqld
systemctl enable php-fpm
systemctl enable nginx

# 老版本使用这个命令
chkconfig --levels 235 mysqld on
chkconfig --levels 235 nginx on
chkconfig --levels 235 php-fpm on
```

### nginx配置php-fpm

```nginx
location ~ \.php$ {    
  fastcgi_pass 127.0.0.1:9000;	# 端口方式
  fastcgi_pass unix:/run/php/php7.0-fpm.sock;	# sodck方式
  
  fastcgi_index index.php;  
  fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;  
  include fastcgi_params;  
}
```

