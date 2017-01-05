---
title: "Apache手册"
date: 2013-09-17 08:52:39
categories: server
---
# Apache教程

## 常用命令

    httpd -v # 查看版本

## TroubleShooting
### [编译安装方法](yum install apr-devel apr-util-devel gcc pcre-devel.x86_64 zlib-devel openssl-devel)

参考：<http://ifalone.me/569.html> <http://laravel-
recipes.com/recipes/25/creating-an-apache-virtualhost>

**环境：Ubuntu14.04 + LAMP**

昨天一个学长叫我帮他设置一下虚拟目录，好吧，我确实没听说过，不过还好，查阅了很多的资料终于找到设置方法了(linux系统总是会更改一些目录设置，所以网上的教
材大多不适用，而且还重复)。

# 修改Apache配置

找到Apache的配置文件_**/etc/apache2/apache2.conf**_修改如下地方(注意记得把其中的注释和中文都去掉，注释最好单独一行)：



    #ServerRoot "/Âetc/apache2"   在这一行下面添加主域名
    ServerName haofly.net
    .....................
    <Directory />
        Options FollowSymLinks
        AllowOverride None




    # Require all denied    # 将这一行去掉




    </Directory>




    # 并在下面添加这样的一个Directory，这一句可以解决无法通过路由访问除根目录以外的




    <Directory /var/www/laravel/public>
        Options FollowSymLinks
        AllowOverride All
    </Directory>
    ...................




    # Include the virtual host configurations:




    IncludeOptional sites-enabled/*.conf   # 这两行不用修改，这里就是放置二级域名配置的地方

如果是在配置laravel，那么还需要打开apache的mod_rewrite功能：



    sudo a2enmod rewrite          # 加载模块
    sudo service apache2 restart  # 重启服务
    sudo apache2ctl -M            # 验证是否夹在成功

# 添加二级域名配置文件

既然要设置二级域名，那么二级域名就应该指向另外一个目录，而不是默认的_**/var/www/html/**_目录，而一般我们所下载的一些框架，比如微信开发框
架、Laravel框架下载下来后都是独立的一个文件夹，最好就放在_**/var/www/**_目录下面就好了。已知现在在该目录下有一个_**laravel*
*_文件夹，其中就是laravel框架的所有文件，为了使用_**laravel.haofly.net**_进行访问，那么可以在_**/etc/apache2
/sites-available/**_目录下新建一个文件**_vim laravel.conf_**，并添加如下内容：

(available表示可用的，enable表示已经启用的)



    <VirtualHost *:80>
      ServerName laravel.haofly.net
      DocumentRoot "/var/www/laravel/public"
      <Directory "/var/www/laravel/public">
        AllowOverride all
        Order allow,deny
        Allow from all
      </Directory>
    </VirtualHost>

如果是非80端口，需要在apache目录的ports.conf里面添加一个listen

如果要设置其它的二级域名，做法同上。保存过后，要在另一个文件里建立一个链接：



    cd ../sites-enabled
    sudo ln -s ../sites-available/laravel.conf
    sudo service apache2 restart

# 检查是否出错

好吧，我才知道，原来apache还有检查配置文件是否出错的命令：



    apachectl -t     检查是否出错
    service apache2 restart 重启apache服务

最后在浏览器中输入laravel.haofly.net进行检验

# PS：

今天在配置apache服务器时，想通过ip/zentao来访问ip/zentaopms/www/地址，但是这并不是虚拟服务器的功能，解决方法就是直接给目录创
建软链接，没错，软链接也是可以给目录创建的，如：



     ln -s /var/www/html/zentaopms/www/ /var/www/html/zentao

Apache 2.4与2.2配置上的区别见：<http://httpd.apache.org/docs/2.4/upgrading.html#access>