---
title: "vps上使用nginx反向代理某些你懂的网站"
date: 2015-05-16 20:38:05
categories: 就是爱玩
---
之前在Github的学生计划中获得的$100 Digitalocean支付券放在那里没怎么用，由于今天碰巧登录不上1024，于是想到直接通过自己的vps来做
反向代理试试(之所以不用shadowsocks，是因为我在DO上搭建的shadowsocks一直都很慢，慢得我无法原谅。。。)

好了，这里说一下ubuntu server上通过nginx反向代理http网站的过程：

首先是一条命令安装nginx`sudo apt-get install nginx`

然后直接修改nginx的server配置文件_/etc/nginx/sites-enabled/default_，修改为如下：



    server \{
            listen 100;  # 指定端口地址
            server_name localhost;





        access_log /var/log/nginx/access_100.log
        error_log /var/log/nginx/error_100.log;
        location / \{
                sub_filter haofly.net localhost;
                proxy_pass http://haofly.net;
                proxy_redirect http://haofly.net  /;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Referer http://$host;
        \}


\}

如果有多个就写多个server，之后就可以使用服务器的IP+端口访问haofly.net网站了。

反向代理的速度和直接访问院网站的速度几乎一样，所以我想到了其它的用途，比如Ubuntu的官方镜像源的代理等。
