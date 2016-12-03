---
title: "wamp环境设置虚拟目录"
date: 2015-03-14 20:48:38
categories: server
---
记得以前在wamp设置虚拟目录的时候都还挺简单的，干脆直接没有记录下来，但这次遇到一些坑，特记录于此。

系统环境：Windows 7 + WampServer2.5

注意事项：下面的步骤一定要参考其完整路径，切勿直接在资源管理器里进行搜索，因为在C:\\wamp\\bin\\apache\\apache2.4.9\\conf目录下
居然有一个original，应该是用来保存最原始的配置信息，对这里面的配置文件进行的更改并不会影响当前的使用。

配置过程：

1.   首先在C:\\wamp\\bin\\apache\\apache2.4.9\\conf\\httpd.conf目录中找到下面两行：

        # Virtual hosts
    Include conf/extra/httpd-vhosts.conf  # 去掉这一行的注释

1.   然后仍然在该文件中找到监听端口的配置

        #Listen 12.34.56.78:80
    Listen 0.0.0.0:80
    Listen [::0]:80
    Listen 8080       # 这一行是自己添加的，我想要它监听8080端口

1.   将vhost的配置文件C:\\wamp\\bin\\apache\\apache2.4.9\\conf\\extra\\httpd-vhosts.conf修改为如下(去掉原来的)：

        <VirtualHost *:80>
        DocumentRoot "c:/wamp/www"
        ServerName localhost
        ServerAlias localhost
        <Directory  "c:/wamp/www">
           AllowOverride All
        Require local
        </Directory>
    </VirtualHost>

    ---
    title: "wamp 局域网403 Forbidden解决方法"
    date: 2014-11-09 16:10:02
    categories: wamp
    ---
    近日，经常需要和对面寝室的同学交流一个网站的设计，但直接把笔记本搬过去太不方便了，于是想到了使用最近刚买的平板电脑，但是平板电脑脸上电脑上的wifi居然无法
    访问笔记本里的wamp服务，出现403错误，好吧，我原以为在局域网内是可以不用设置其他东西的哟。其实解决方法很简单，但是和linux系统不一样，linux使
    用`Allow from all`，而windows使用`Require all granted`解决方法如下：
    
    **环境**：windows7 + wampserver2.5
    
    # 解决步骤：
    
    首先找到wamp的apache配置文件目录，我的在`C:\\wamp\\bin\\apache\\apache2.4.9\\conf\\http.conf`，然后打开它
    后找到，如下几行



        # Each directory to which Apache has access can be configured with respect




        # to which services and features are allowed and/or disabled in that




        # directory (and its subdirectories).




        #




        # First, we configure the "default" to be a very restrictive set of




        # features.




        #




        <Directory />
            AllowOverride All
            #Order Deny,Allow     # 注释掉
            Require all granted   # 添加这一行
        </Directory>





    <VirtualHost *:8080>
        DocumentRoot "f:/workspace/laravel/public"
        ServerName localhost
        ServerAlias localhost
        <Directory  "f:/workspace/laravel/public">
            AllowOverride All
            Require local
        </Directory>
    </VirtualHost>

  1. 重启Apache即可
