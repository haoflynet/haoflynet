---
title: "使用certbot为Nginx一键配置Let's Encrypt SSL安全证书"
date: 2018-06-16 21:32:00
categories: server
---

还记得`Let's Encrypt`刚出来的时候，繁琐的手动配置简直是让人心力交瘁。这几天，由于购买了阿里的服务器，并且也需要提供后端服务，于是不得不再次需要去配置免费ssl证书的，但是，这次，让我出乎意料的是，配置ssl证书居然这么简单。

`certbot`是`Let's Encrypt`官网推荐的自动化配置工具，[工具官网](https://certbot.eff.org/)可以选择针对Apache/Nginx/Haproxy/Plesk等不同服务器不同操作系统的安装配置方法。这里只介绍最常用的Nginx+CentOS组合。

<!--more-->

首先，不得不说，`certbot`有几个不得不解决的依赖问题。

1. `certbot`依赖的python2的`urllib3`库版本为1.21.1版本，如果已经安装了更高版本的`urllib3`库，那么降级吧`pip install urllib3==1.21.1`，[issue参考](https://community.letsencrypt.org/t/certbot-not-working-with-centos7-and-nginx/45646/2)

2. 如果python2的`requests`库版本小于2.6.0，那么自觉升级`pip install --upgrade --force-reinstall 'requests==2.6.0'`，[issue参考](如果requests<2.6.0那么强制升级。https://github.com/certbot/certbot/issues/5534)

3. 接下来真正的安装过程:

   ```shell
   yum install epel-release -y && yum update -y
   yum install python2-certbot-nginx -y
   ```

4. 确保你的nginx配置已经有配置域名，并且域名解析也已经指向该IP地址，域名能够通过80端口正常访问。

5. 当安装完成以后，一切就简单了，运行`certbot --nginx`，会以提问的方式询问你几个配置问题:

   ```shell
   # 第一步会读取你的nginx配置，询问你需要对哪些域名需要添加ssl
   Which names would you like to activate HTTPS for?
   -------------------------------------------------------------------------------
   1: a.haofly.net
   2: b.haofly.net
   -------------------------------------------------------------------------------
   # 第二部询问你在遇到http的时候是否需要重定向到https
   Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
   ```

   就这样，配置就算完成了，可以看到新的nginx配置已经写入到配置文件中，访问域名也会自动跳转到https了。

6. 当然，`Let's Encrypted`只有90天的有效期，可以使用这条命令更新证书: `sudo certbot renew --dry-run`，官方建议每天随机运行两次该命令，如果证书没有过期，运行命令并不会对你的服务器造成什么影响，所以就添加如下定时任务:

   ```shell
   0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew 
   ```

   