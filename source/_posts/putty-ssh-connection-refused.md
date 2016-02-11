---
title: "putty使用ssh由主机登录虚拟机connection refused问题"
date: 2014-09-18 23:50:51
categories: 编程之路
---
参考文章：<http://www.lamp99.com/wirtualbox_centos_web.html>

# 现象

使用putty的ssh功能登录虚拟机里的linux系统时出现这样的错误提示：

**Network error: Connection refused.**

# 原因

原因太多了，而且不同的网络连接方式，不同的虚拟机，不同的linux系统都会莫名其妙出现这个问题，所以在这里，我只能每次遇到问题就记录下解决方案，以后依次尝试
就行了。之所以要在这里记录下来，是因为不知道为什么每次我遇到的问题在网上都很难找到解决办法，不知道是不是因为我总是做一些奇葩的操作。。。

# 解决方案一：

来自[红黑联盟 ](http://www.2cto.com/os/201205/130781.html)这个方法的状况是虚拟机和主机能够互相ping通，但就
是连不上ssh。虚拟机能够上网，使用的是网络地址转换(NAT)的连接方式。
首先在windows的命令行cmd中使用_**ipconfig**_命令查看以太网适配器(VirtualBox Host-Only
Network)的IPv4地址。我的是192.168.56.101。 然后在虚拟机终端里面使用_**ifconfig**_查看内部网络地址，一般就是eth0
的nat地址，在centos里面是enp0s3的inet地址，我的是10.0.2.15。 最后在该虚拟机设置端口转发  
![](http://7xnc86.com1.z0.glb.clouddn.com/putty-ssh-connection-refused_0.jpg)  
像如下这样添加一条规则：  
![](http://7xnc86.com1.z0.glb.clouddn.com/putty-ssh-connection-refused_1.jpg)  
添加后就可以通过putty的ssh登录主机了，ip是192.168.56.101.(需要注意的是，如果虚拟网卡的IPv4是自动获取ip的那么每次都会改变ip
，在这里直接把两个IP都写成255.255.255.255即可)
