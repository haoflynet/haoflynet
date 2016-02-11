---
title: "windows + wamp环境下安装Laravel框架"
date: 2014-09-20 23:31:13
categories: 编程之路
---
其实官网已经有很详细的[教程](http://v4.golaravel.com/docs/4.2/installation)，但由于其方法太多，身为天秤座的
我还是喜欢用一个方法，所以在这里把它记录下来。

# 环境：Windows + wamp

# Composer安装

点击下载，下载之后，直接安装即可，安装完成后，就可以在windows的文件窗口中就可以使用右键看到关于composer的几个菜单。

# Laravel安装

首先，使用composer安装laravel的安装器



    composer global require "laravel/installer"

然后再将其加入系统路径(在环境变量里添加如下目录)：



    C:\\Users\\haofly\\AppData\\Roaming\\Composer\\vendor\\bin

之后再打开终端检查是否安装成功，如果出现如下信息表示安装成功了



    C:\\Users\\haofly>laravel
    Laravel Installer version 1.2.0




    Usage:
     [options] command [arguments]




    Options:
     --help (-h)           Display this help message
     --quiet (-q)          Do not output any message
     --verbose (-v|vv|vvv) Increase the verbosity of messages: 1 for normal output,
    2 for more verbose output and 3 for debug
     --version (-V)        Display this application version
     --ansi                Force ANSI output
     --no-ansi             Disable ANSI output
     --no-interaction (-n) Do not ask any interactive question




    Available commands:
     help   Displays help for a command
     list   Lists commands
     new    Create a new Laravel application.


之后就可以在wamp环境的www目录下执行如下命令即可建立新的项目了：



    >> laravel new 项目名
    Crafting application...
    Generating optimized class loader
    Compiling common classes
    Compiling views
    Application key [.......] set successfully.
    Application ready! Build something amazing.

# Apache配置

这里就是官网说的不大明显的地方了，害我之前做错了一步。 现在需要打开apache的mod_rewrite模式，打开apache的配置文件httpd.conf
(我的电脑是D:\\wamp\\bin\\apache\\apache2.4.9\\conf\\httpd.conf)，把下面一行前面的注释去掉



    LoadModule rewrite_module modules/mod_rewrite.so


此时重启wamp服务，就可以访问localhost/laravel/public的欢迎页了  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-wamp-install-laravel.png)  

# 测试环境

在我使用apache设置了虚拟目录后访问[http://localhost:8080即访问到laravel项目，laravel自带了一个登录的页面`http
://localhost:8080/home`，当然要成功注册和的登录，必须先将默认的...](http://localhost:8080即访问到larav
el项目，laravel自带了一个登录的页面<code>http://localhost:8080/home</code>，当然要成功注册和的登录，必须先将
默认的数据库及数据表建立好)：

首先，在数据库的配置文件 `learnlaravel5/.env`里面填好数据库的基本信息



    DB_HOST=localhost
    DB_DATABASE=faxie
    DB_USERNAME=root
    DB_PASSWORD=mysql

然后执行前移数据库操作



    php artisan migrate

如果能成功建立好数据库，那么就能够注册和登录了。

# Laravel的基本配置

laravel的配置文件在app.php里(我的电脑是D:\\wamp\\www\\laravel\\app\\config下的app.php)，可以配置如下信息：

'debug' => false 可以改为true，需要注意的是在实际发布中千万不能使用true，不然可能被用户看到重要信息
如果要配置数据库，可以在下面对应的数据库里面选择并修改。
