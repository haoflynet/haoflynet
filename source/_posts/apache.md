---
title: "Apache手册"
date: 2013-09-17 08:52:39
updated: 2018-11-21 17:36:00
categories: server
---
## Apache安装与配置

Apache 2.4与2.2配置上的区别见: [Upgrading to 2.4 from 2.2](http://httpd.apache.org/docs/2.4/upgrading.html#access)

## 常用命令

```shell
httpd -v # 查看apache版本
```
## 配置虚拟目录/设置二级域名

<!--more-->

昨天一个学长叫我帮他设置一下虚拟目录，好吧，我确实没听说过，不过还好，查阅了很多的资料终于找到设置方法了(linux系统总是会更改一些目录设置，所以网上的教材大多不适用，而且还重复)。

1. 首先，修改Apache配置。找到Apache的配置文件`/etc/apache2/apache2.conf`修改如下地方(注意记得把其中的注释和中文都去掉，注释最好单独一行)

   ```tex
   #ServerRoot "/Âetc/apache2"   在这一行下面添加主域名
   ServerName haofly.net		# 主机域名解析接口
   ServerAlias a.haofly.net b.haofly.net	# 多域名设置，别名，可以让几个域名同时解析到统一入口
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
   ```

   如果果是在配置laravel，那么还需要打开apache的`mod_rewrite`功能：

   ```shell
   sudo a2enmod rewrite          # 加载模块
   sudo service apache2 restart  # 重启服务
   sudo apache2ctl -M            # 验证是否夹在成功
   ```

2. 添加二级域名配置文件

   既然要设置二级域名，那么二级域名就应该指向另外一个目录，而不是默认的 `/var/www/html/`目录，而一般我们所下载的一些框架，比如微信开发框架、Laravel框架下载下来后都是独立的一个文件夹，最好就放在`/var/www/`目录下面就好了。已知现在在该目录下有一个`laravel`文件夹，其内容就是laravel框架的所有文件，为了使用`laravel.haofly.net`进行访问，那么可以在`/etc/apache2/sites-available/`目录下新建一个文件`vim laravel.conf`，并添加如下内容(available表示可用的，enable表示已经启用的):

   ```tex
   <VirtualHost *:80>
     ServerName laravel.haofly.net
     DocumentRoot "/var/www/laravel/public"
     <Directory "/var/www/laravel/public">
       AllowOverride all
       Order allow,deny
       Allow from all
     </Directory>
   </VirtualHost>
   ```

   如果是非80端口，需要在apache目录的`ports.conf`里面添加一个`listen` 。如果要设置其它的二级域名，做法同上。保存过后，需要在另一个文件里建立一个链接： 

   ```shell
   cd ../sites-enabled
   sudo ln -s ../sites-available/laravel.conf
   sudo service apache2 restart
   ```

3. 检查是否出错。好吧，我才知道，原来apache还有检查配置文件是否出错的命令：

   ```shell
   apachectl -t     检查是否出错
   service apache2 restart 重启apache服务
   ```

   最后在浏览器中输入`laravel.haofly.net`进行检验

## 同一端口多个域名的配置

直接修改默认的配置文件`/etc/apache2/sites-available/default???`

```tex
NamevirtualHost *:80		# 如果不加这一行，那么只有第一个会起作用

<VirtualHost *:80>
	DocumentRoot /var/www/html/test1
	ServerName www.test1.com    
</VirtualHost>

<VirtualHost *:80>
	DocumentRoot /var/www/html/test2
	ServerName www.test2.name
</VirtualHost>
```

### TroubleShooting

- **apache设置子目录**: 今天在配置apache服务器时，想通过ip/zentao来访问ip/zentaopms/www/地址，但是这并不是虚拟服务器的功能，解决方法就是直接给目录创建软链接，没错，软链接也是可以给目录创建的，如：

  ```shell
   ln -s /var/www/html/zentaopms/www/ /var/www/html/zentao
  ```

- **You don't have permission to access /index on this server. Server unable to read htaccess file, denying access to be safe**: 一般原因是apache没有网站目录权限，修改`/var/www/html`文件夹及子文件的权限即可

- **The requested URL /index/login was not found on this server**: 一般是`.htaccess`文件没找到或者`apache`没有开启`rewrite`模式，后者可以使用`a2enmod rewrite`命令进行开启
