---
title: "zabbix教程"
date: 2016-04-07 11:02:30
categories: server
---
# zabbix
默认用户名Admin，默认密码zabbix

## 安装

    # 先安装MySQL，根据[初始化数据导入](https://www.zabbix.com/documentation/2.4/manual/appendix/install/db_scripts)来创建用户
    # 安装主程序
    rpm -ivh http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm
    yum install zabbix-server-mysql zabbix-web-mysql # 服务端安装
    yum install zabbix-agent    # 客户端安装
    # 基本配置,vim /etc/zabbix/zabbix_server.conf
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=zabbix
    
    # 安装zabbix的辅助工具
    yum install zabbix-get zabbix-sender
    zabbix_get -s 客户端IP -k "agent.ping" # 在服务端运行该命令可检测服务端是否能娶到数据
    
    # 启动服务
    /etc/init.d/zabbix-server start
    
    # 安装完成后会在httpd目录下面的conf.d生成相应的配置文件，唯一需要改的就是它注释了的date.timezone，修改一下httpd的监听端口和IP就可以访问了,默认用户名密码是Admin zabbix，注意大小写


## 监控配置
    [添加自定义监控项目](http://yangrong.blog.51cto.com/6945369/1548670)
    [邮件报警设置](http://www.osyunwei.com/archives/8113.html)
