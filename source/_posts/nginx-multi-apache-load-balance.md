---
title: "nginx + 多apache 做反向代理实现负载均衡并设置二级域名"
date: 2014-10-23 08:03:02
categories: 编程之路
---
参考文章：[http://blog.csdn.net/yanggd1987/article/details/31375573
](http://blog.csdn.net/yanggd1987/article/details/31375573)
<http://www.oschina.net/question/56436_109188>

在网上找了几天时间，发现网上的方法都有一定的局限性，因为我想要的是在同一台服务器上实现一个nginx做反向代理到多个apache(再一次感叹网上好多教程的落
后和千篇一律)。这里再次记录本次的配置过程。

环境：Ubuntu14.04 server + nginx(1.4.6) + apache2(2.4.7)
目的：使用nginx做代理，分别代理到apache的四个监听端口8080/8081/8082/8083 优点：Nginx可应付高并发，使用Proxy做代理效
率也较高，占用资源少，再使用apache处理后端，也更稳定，现在一般的做法是是用nginx处理前端，apache处理后端，我这里暂时全部交由apache处理
。当然，我这里都是在同一台服务器上做的，除了减少单个apache的并发处理数量，对性能来说并没有显著的提升。

### 1.安装nginx和apache2

安装到没什么好说的，直接`apt-get`安装即可。

### 2.修改nginx的配置文件/etc/nginx/nginx.etc

在http字段(就是那个大括号里面)添加如下内容：



    upstream balance\{
        server localhost:8080;
        server localhost:8081;
        server localhost:8082;
        server localhost:8083;
    \}




    server\{
        listen 80;
        server_name haofly.net;
        localhost /\{
            proxy_pass http://balance;
        \}
    \}

其中nginx是让upstream里面的各个IP/端口实现轮询访问，研究一下nginx的配置文件，还可以对轮询访问加上一些限制条件，比如轮训机制、权值分配等
，这里不做详述。

需要注意的是如果是二级域名，那么upstream里面的server依然写成`localhost:port`的形式，而不用去写什么二级域名，二级域名在apac
he的配置文件里面定义，nginx会直接将那些都传给它的。

### 3.修改apache的配置文件

主配置文件`/etc/apache2/apache2.conf`，在#ServerRoot
"/etc/apache"下添加一行指明ServerName，例如：



    #ServerRoot "/etc/apache2"
    ServerName haofly.net

虚拟目录配置文件(这就相当于为apache多开了几个线程，就好像是有多个apache在同时工作一样) `vim /etc/apache2/sites-
available/000-default.conf`(这是默认的那个80端口的配置文件)，只需要把里面的80端口改为8080即可。然后再新建几个配置文件
`vim /etc/apache2/sites-available/proxy01.conf`内容如下：



    <VirtualHost *:8081>
        ServerAdmin localhost:8081
        DocumentRoot /var/www/html





    ErrorLog $\{APACHE_LOG_DIR\}/error.log
    CustomLog $\{APACHE_LOG_DIR\}/access.log combined


</VIrtualHost>

8082端口的配置文件proxy02.conf只需要把端口改为8082即可，另外为方便测试，我们需要把8083端口的配置文件特殊化一下，`vim
/etc/apache2/sites-available/proxy03.conf`，内容如下：



    <VirtualHost *:8083>
        ServerAdmin localhost:8083
        DocumentRoot /var/www/test





    ErrorLog $\{APACHE_LOG_DIR\}/error.log
    CustomLog $\{APACHE_LOG_DIR\}/access.log combined


</VIrtualHost>

其实只是修改了DocumentRoot，使它指向/var/www/test，这样就方便测试了，在/var/www/test下新建一个文件`vim
/var/www/test/index.html`，内容如下



    <html>
     hehe
    </html>

在把配置文件链接到`/etc/apache2/sites-available`文件夹：



    cd ../sites-enabled
    sudo ln -s ../sites-available/proxy01.conf
    sudo ln -s ../sites-available/proxy02.conf
    sudo ln -s ../sites-available/proxy03.conf

最后再修改apache的端口文件`vim /etc/apache2/ports.conf`，把Listen *80修改为：



    Listen 8080
    Listen 8081
    Listen 8082
    Listen 8083

###  4.测试

首先检查配置文件是否有语法错误



    nginx -t
    apachectl -t

如果都OK，就可以重启了：



    service apache2 restart
    service nginx stop
    service nginx start

然后在浏览器输入上面的Servername，即http://haofly.net，多刷新几次，就会发现，有时候出现的是apache的界面，有时候出现的是te
st下那个hehe界面。

### 5.nginx添加二级域名

比apache简单多了，我这里不仅添加了二级域名，并且也实现了一个反向代理，在/etc/nginx/nginx.conf里面的http里面添加一个upstr
eam和一个server即可：



    upstream \{
       server localhost:8084;
    \}
    server \{
        server_name aa.hostname.com;
        listen               80;
        location / \{
          proxy_pass http://er;
          proxy_redirect default;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection $http_connection;
        \}
    \}

然后就像[Linux使用虚拟主机设置一、二级域名和虚拟目录](http://haofly.net/linuxvirtualhost/ "Link:
http://haofly.net/linuxvirtualhost/" ) 那样设置apache即可。
