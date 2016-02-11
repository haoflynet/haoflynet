---
title: "Unitedstack(阿里云)中数据库无法远程登录解决办法"
date: 2014-11-10 16:31:10
categories: 编程之路
---
OK，昨晚熬夜到两点都没解决这个问题，不过还好昨晚至少知道了问题没有出现在配置上，而是IP有问题。今天写了一张工单给ustack的客服，终于知道答案了。

**现象**：ustack的云服务器中的mysql数据库无法实现远程登录。

**环境**：Ubuntu14.04(server) + ustack服务器

**解决**：

# 1.修改默认安全组

阿里云没有安全组功能，默认不对端口进行限制

ustack的安全组是云主机虚拟网卡上行和下行流量的防火墙，就相当与其NAT的防火墙，而DigitalOcean没有这个东西，不信你可以试试`ifconfi
g`，该命令在ustack可以看到两张网卡，但是却没有外网ip的网卡，而DigitalOcean则可以直接看到外网ip的网卡切没有内网的ip。以下是usta
ck的默认安全组：  
![](http://7xnc86.com1.z0.glb.clouddn.com/database-remote-login.png)  
可以看到其上行流量是完全开放的，但是下行却只开放了几个端口，可以在这里面添加安全规则，也可以自己另外建立安全组，然后在虚拟网卡里面绑定到相应的虚拟网卡就可以
生效了，然后重启一下服务器(没尝试过不重启会不会生效，反正我是重启了的)。

# 2.MySQL授权root用户远程登录

需要注意的是，最好不要用root用户远程登录，可自己新建一个用户用于远程登录，并限制一些权限，由于我这只是测试用的服务器，所以无所谓。首先在服务器中执行如下
命令：



    mysql -u root -p   # 登录MySQL
    mysql> use mysql;
    mysql> select host, user from user;   # 查看是否已经分配了权限
    +-----------+------------------+
    | host      | user             |
    +-----------+------------------+
    | 127.0.0.1 | root             |
    | ::1       | root             |
    | localhost | debian-sys-maint |
    | localhost | root             |
    | tech      | root             |
    +-----------+------------------+
    6 rows in set (0.00 sec)
    mysql> grant all privileges on 星__.星__ to 'root'@'\%' identified by 'password' with grant option;
    mysql> select host, user from user;    # 结果中的\%就表示所有IP都可以用root用户登录
    +-----------+------------------+
    | host      | user             |
    +-----------+------------------+
    | \%         | root             |
    | 127.0.0.1 | root             |
    | ::1       | root             |
    | localhost | debian-sys-maint |
    | localhost | root             |
    | tech      | root             |
    +-----------+------------------+
    6 rows in set (0.00 sec)


#  3.修改MySQL侦听端口

修改MySQL配置文件`/etc/mysql/my.cnf`，将`bind-address`后的值`localhost`修改为ustack服务器的内网IP(
注意这里修改成的是内网ip，因为ustack是用的NAT方式转发过去的，它本身根本无法识别外网IP)

阿里云需要将bind-address设置为服务器的外网IP

DigitalOcean也要设置为外网IP(DO貌似没有内网IP)

# 4.测试

在另一台电脑上执行`mysql -h 外网IP -uroot -p`，这里的IP是外网IP，如果能访问就表示设置成功了。
