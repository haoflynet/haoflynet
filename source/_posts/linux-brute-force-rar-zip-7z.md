---
title: "Linux暴力破解RAR，ZIP，7Z压缩包"
date: 2014-02-22 00:26:43
categories: 编程之路
---
封面图片来自Pixabay

这里使用的软件名称叫rarcrack,其官方主页：<http://rarcrack.sourceforge.net/>

该软件用于暴力破解压缩文件的密码，但仅支持RAR, ZIP,
7Z这三种类型，其特点是可以使用多线程而且可以暂停与继续(会在当前目录生成一个xml文件，里面显示了正在尝试的一个密码)。

### 安装方法

首先从官网下载安装包，然后执行如下命令  
$ tar -xjf rarcrack-0.2.tar.bz2  
$ cd rarcrack-0.2.tar.bz2  
$ make  
$ make install

### 使用方法

rarcrack 文件名 [–threads thread_num] [–type rar|zip|7z]

该软件还自带了测试样例，该目录内，执行`rarcrack test.rar --threads 4 --type
rar`，等待一会儿即可得到结果，其密码是`100`。

如果要改变尝试的位置可以直接打开xml，修改当前密码那一行即可。

如果出现如下错误：  
gcc -pthread rarcrack.c`xml2-config --libs --cflags`-O2 -o rarcrack  
/bin/sh: 1: xml2-config: not found  
In file included from rarcrack.c:21:0:  
rarcrack.h:25:48: 致命错误： libxml/xmlmemory.h：没有那个文件或目录  
编译中断。  
make: *** [all] 错误 1

则执行：`sudo apt-get install libxml2-dev libxslt-dev`
