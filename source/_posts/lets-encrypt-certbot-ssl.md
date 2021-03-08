---
title: "使用certbot为Nginx一键配置Let's Encrypt SSL安全证书"
date: 2018-06-16 21:32:00
updated: 2021-03-01 14:00:00
categories: server
---

还记得`Let's Encrypt`刚出来的时候，繁琐的手动配置简直是让人心力交瘁。这几天，由于购买了阿里的服务器，并且也需要提供后端服务，于是不得不再次需要去配置免费ssl证书的，但是，这次，让我出乎意料的是，配置ssl证书居然这么简单。

`certbot`是`Let's Encrypt`官网推荐的自动化配置工具，[工具官网](https://certbot.eff.org/)可以选择针对Apache/Nginx/Haproxy/Plesk等不同服务器不同操作系统的安装配置方法。这里只介绍最常用的Nginx+CentOS组合。

<!--more-->

## Certbot配置

~~首先，不得不说，`certbot`有几个不得不解决的依赖问题。~~

1. ~~`certbot`依赖的python2的`urllib3`库版本为1.21.1版本，如果已经安装了更高版本的`urllib3`库，那么降级吧`pip install urllib3==1.21.1`，[issue参考](https://community.letsencrypt.org/t/certbot-not-working-with-centos7-and-nginx/45646/2)~~

2. ~~如果python2的`requests`库版本小于2.6.0，那么自觉升级`pip install --upgrade --force-reinstall 'requests==2.6.0'`，[issue参考](如果requests<2.6.0那么强制升级。https://github.com/certbot/certbot/issues/5534)~~

3. 接下来真正的安装过程:

   ```shell
   # for ubuntu
   add-apt-repository ppa:certbot/certbot && apt update
   apt install certbot python3-acme python3-augeas python3-certbot python3-certbot-nginx python3-certbot-apache	# nginx和apache根据实际需要选择
   
   # for centos
   yum install epel-release -y && yum update -y
   yum install certbot python3-acme python3-augeas python3-certbot python3-certbot-nginx python3-certbot-apache -y
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
   # 第二步询问你在遇到http的时候是否需要重定向到https
   Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
   ```

   就这样，配置就算完成了，可以看到新的nginx配置已经写入到配置文件中，访问域名也会自动跳转到https了。

6. 当然，`Let's Encrypt`只有90天的有效期，可以使用这条命令更新证书: `sudo certbot renew --dry-run`，官方建议每天随机运行两次该命令，如果证书没有过期，运行命令并不会对你的服务器造成什么影响，所以就添加如下定时任务:

   ```shell
   0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew 
   ```

## Let's Encrypt证书迁移

- 要把证书从一台服务器迁移到另外一台服务器，其实挺简单的主要是那几个link文件需要重新链接一下，迁移步骤如下:

- 在旧服务器上执行以下命令

```shell
certbot renew	# 先在原服务器上更新一下证书
certbot certificates	# 查看原服务器上证书信息
ls -l /etc/letsencrypt/live/haofly.net/	# 查看软链接信息，信息可能如下，需要注意每个.pem前的数字表示续期第几次了
lrwxrwxrwx 1 root root 34 Jan 22 10:00 cert.pem -> ../../archive/haofly.net/cert3.pem
lrwxrwxrwx 1 root root 35 Jan 22 10:00 chain.pem -> ../../archive/haofly.net/chain3.pem
lrwxrwxrwx 1 root root 39 Jan 22 10:00 fullchain.pem -> ../../archive/haofly.net/fullchain3.pem
lrwxrwxrwx 1 root root 37 Jan 22 10:00 privkey.pem -> ../../archive/haofly.net/privkey3.pem

zip letsencrypt.zip /etc/letsencrypt	# 将letsencrypt文件夹直接打包
```

- 在新服务器上执行以下命令

```shell
cd /etc && unzip letsencrypt.zip	# 解压letsencrypt文件
cd letsencrypt/live/haofly.net
for i in cert chain fullchain privkey ;	# 重新建立软连接，这一这里的.pem文件前缀就是旧服务器上的续期次数
do
rm ${i}.pem
ln -s ../../archive/cnzhx.net/${i}3.pem ${i}.pem
done

certbot renew --dry-run	# 运行一次renew看看是否正常--dry-run表示只运行不用保存结果
```

## Let's Encrypt添加新域名

```shell
certbot certificates	# 先查看当前有哪些域名，比如有haofly.net
certbot --cert-name haofly.net -d haofly.net,2.haofly.net,3.haofly.net	# 需要注意的是必须把之前的给加上，如果不加某个域名也可以直接表示移除该域名
```

## 定时更新证书

```shell
0 3 * * * certbot renew --post-hook "systemctl reload nginx"	# 更新完成后重启nginx
```

## Troubleshooting

- **如果安装时出现错误: Problem binding to port 80: Could not bind to IPv4 or IPv6.**此时需要把nginx暂停一下`service nginx stop`