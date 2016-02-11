---
title: "重邮等高校在linux下使用openkeeper代替netkeeper连接网络"
date: 2014-03-02 15:27:56
categories: 编程之路
---
封面图片来自：Pixabay  

首先下载大神们做好的软件包：[点此下载](http://download.csdn.net/detail/haoxiangtianxia/6982631)（
其实这里面也有安装说明的），由重邮linux协会以及linux story团队提供  
重邮BBS地址：<http://bbs.cqupt.edu.cn/nForum/#!article/Unix_Linux/13702>

然后执行以下命令：

1

2

3

4

|

tar -jxv -f openkeeper-cli-1.1.tar.bz2 # 解压缩到当前目录

cd openkeeper-cli-1.1 # 进入目录

ls #显示当前目录文件

32 64 build-essential_11.6ubuntu4_amd64.deb README  

---|---  

如果电脑没有安装build-essential需要先安装它，如果有归档管理器，那么双击`build-
essential_11.6ubuntu4_amd64.deb`即可安装，如果没有或者是你的电脑是32位系统那么就执行`sudo apt-get
install build-essential`即可安装依赖。


然后进入进入目录安装，执行：

1

2

3

|

cd 64 # 进入该目录，如果是32位系统请选择32这个文件夹

sudo chmod 777 install.sh # 给install.sh添加可执行权限

sudo ./install.sh # 执行安装命令  

---|---  

这样就安装好了，安装好后，可以使用如下命令进行配置和连接(此时不一定要当前目录的，因为这几个命令已经放到了你的/usr/bin/中去了)：

1

2

3

|

ok-config # 配置网络参数，这里会要求输入用户名密码以及网卡(网卡默认eth0)

okok # 这一点与README里介绍的不同，我想是因为这个东西是后人对前人改进了的，以前的版本会每十分钟断一次的

okok-stop # 断开网络  

---|---  

如此，便可以连接外网了。以后开机只需要输入`sudo okok`即可。

如果要连接内网，还要进行如下配置：

点击网络设置，如下图：

![](http://7xnc86.com1.z0.glb.clouddn.com/linux-openkeeper-netkeeper_0.png)  

如果没有该网络管理软件，可执行`sudo apt-get install network-manager-network`安装

然后点击以太网里面的一个选项编辑，出现如下对话框：

![](http://7xnc86.com1.z0.glb.clouddn.com/linux-openkeeper-netkeeper_1.png)  

然后选择”821.X安全性“选项卡，这里输入内网的用户名和密码，然后就可以进入内网了

## openkeeper下载地址

因为打包的时候并没有在所有平台尝试，所以选择最好的

[openkeeper-cli-1.1.tar.gz](http://7xjhvx.dl1.z0.glb.clouddn.com/openkeeper-
cli-1.1.tar.gz "Link: http://7xjhvx.dl1.z0.glb.clouddn.com/openkeeper-
cli-1.1.tar.gz" )

[openkeeper-
cli-1.3.1-noarch.tar.gz](http://7xjhvx.dl1.z0.glb.clouddn.com/openkeeper-
cli-1.3.1-noarch.tar.gz)
