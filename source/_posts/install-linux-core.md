---
title: "Linux 内核的安装"
date: 2014-02-02 11:14:24
updated: 2016-10-09 22:03:00
categories: 编程之路
---
系统环境: `ubuntu 64位`

Linux内核的安装主要有以下两种方式：

### 方法一、安装编译好的通用内核DEB包

通用内核DEB包包含了linux内核得三个核心文件:

`linux-image`: 内核核心文件
`linux-headers`: 内核头文件
`linux-headers-generic`: 内核通用头文件

[ubuntu内核DEB包下载地址](http://kernel.ubuntu.com/~kernel-ppa/mainline/)(带了rc的内核为非稳定版本)，这是最简单且最通用的方法，因为不需要去配置任何东西，几条命令就让系统自己配置好了。我们需要下载的三个文件为(注意平台，通常是`amd64`,32位版本则使用`i386`):

- [linux-image-4.8.1-040801-generic_4.8.1-040801.201610071031_amd64.deb](http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.8.1/linux-image-4.8.1-040801-generic_4.8.1-040801.201610071031_amd64.deb)
- [linux-headers-4.8.1-040801-generic_4.8.1-040801.201610071031_amd64.deb](http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.8.1/linux-headers-4.8.1-040801-generic_4.8.1-040801.201610071031_amd64.deb)
- [linux-headers-4.8.1-040801_4.8.1-040801.201610071031_all.deb](http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.8.1/linux-headers-4.8.1-040801_4.8.1-040801.201610071031_all.deb)

把他们放到同一个文件夹，然后在该文件夹内执行下面命令进行安装:

```shell
sudo dpkg -i *.deb	# 安装DEB包
sudo update-grup 	# 刷新grub
```

### 方法二、下载内核源代码，按照个人需求编译安装

此方法较为复杂，而且可能会出现很多问题，但是对于想了解内核以及想提高性能的用户就非常适用了，因为普遍认为通过此方法可以精简内核，提高系统效率。

首先下载[最新稳定版内核源代码](http://kernel.org)，然后在该目录打开终端，执行如下命令进行接呀:

```shell
xz -kd 文件名
tar -xvf 文件名.tar
```

然后执行编译步骤，如果之前编译过需要重新编译，首先得清理一下:`make mrproper`

再执行命令`make menuconfig`在图形化界面配置各个选项。

都配置好过后，在终端以此执行如下命令(下面的命令参数重的-x表示设置的线程数，设置多线程可以加快编译速度，比如我是双核处理器那就选4线程，x为4):

```shell
make -jx 					# 编译内核  
make modules -jx 			# 编译内核模块  
make headers -jx 			# 编译内核头文件  
sudo make headers_install 	# 安装内核头文件  
sudo make modules_install 	# 安装内核模块  
sudo make install 			# 安装内核  
sudo reboot 				# 重启以验证内核
```

**TroubleShooting**

##### 执行`make menuconfig`的时候出现如下错误

```shell
*** Unable to find the ncurses libraries or the  
*** required header files.  
*** ‘make menuconfig’ requires the ncurses libraries.  
---
*** Install ncurses (ncurses-devel) and try again.  
---
make[1]: *** [scripts/kconfig/dochecklxdialog] 错误 1  
make: *** [menuconfig] 错误 2  
```

那么执行这条命令可以解决:`sudo apt-get install libncurses5-dev`