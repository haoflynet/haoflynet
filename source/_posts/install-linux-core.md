---
title: "Linux 内核的安装"
date: 2014-02-02 11:14:24
categories: 编程之路
---
封面图片来自Pixabay  

系统环境：64位ubuntu

Linux内核的安装主要有以下两种方法：

### 方法一：安装编译好的通用内核DEB包

(包括内核核心文件linux-image，内核头文件linux-headers，内核通用头文件linux-headers三个文件)

ubuntu内核DEB包 [下载地址](http://kernel.ubuntu.com/~kernel-
ppa/mainline/)（带了rc的内核为非稳定版本）

这是最简单的方法，因为是通用的，所以不需要去配置任何东西

首先通过上述下载地址下载到以下三个DEB包(注：32位系统请下载i386版本)：

– linux-image-3.13.0-031300-generic_3.13.0-031300.201401192235_amd64.deb  
– linux-headers-3.13.0-031300-generic_3.13.0-031300.201401192235_amd64.deb  
– linux-header-3.13.0-031300_3.13.0-031300.201401192235_all.deb
(这个文件不用区分32位和64位)

然后把他们放到同一个文件夹，在该文件夹内打开终端，执行如下命令：

sudo dpkg -i *.deb 安装DEB包

sudo update-grub 刷新grub

### 方法二：下载内核源代码，按照个人需求编译安装

此方法较为复杂，而且可能会出现很多问题，但是对于想了解内核以及想提高性能的用户就非常适用了，因为通过此方法可以精简内核，提高系统效率

首先下载[最新稳定版内核源代码](<http://kernel.org)，然后在该目录打开终>端

将源代码解压，如果右键不能直接提取那就执行命令：

1

2

|

内核解压命令为`xz -kd 文件名

然后再解压tar：`tar –xvf 文件名.tar  

---|---  

如果之前编译过那么就需要清理一下，在终端执行命令： make mrproper

当然，如果是刚从网上下载下来的就不需要这一步

然后在该目录内执行 make menuconfig  
在图形化界面配置各个选项

详细的内核配置说明见：[Linux内核配置详细说明](http://haofly.net/linux-kernel/)

当然，我这里列举了通常需要修改的项目：[Linux内核个性化配置](http://haofly.net/kernel-mainmenu/)

配置好后，在终端执行(注：下面的命令参数中-x表示设置的线程数，设置多线程可加快编译时间，比如我是双核处理器那就选4线程，x为4)：

make -jx 编译内核  
make modules -jx 编译内核模块  
make headers -jx 编译内核头文件  
sudo make headers_install 安装内核头文件  
sudo make modules_install 安装内核模块  
sudo make install 安装内核  
sudo reboot 重启以验证内核

可能遇到的错误：  
执行`make menuconfig`的时候如果出现如下错误，那么

*** Unable to find the ncurses libraries or the  
*** required header files.  
*** ‘make menuconfig’ requires the ncurses libraries.  
***  
*** Install ncurses (ncurses-devel) and try again.  
***  
make[1]: *** [scripts/kconfig/dochecklxdialog] 错误 1  
make: *** [menuconfig] 错误 2  
那么可以执行 sudo apt-get install libncurses5-dev
