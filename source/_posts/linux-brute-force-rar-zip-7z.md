---
title: "Linux使用rarcrack暴力破解RAR，ZIP，7Z压缩包"
date: 2014-02-22 00:26:43
updated: 2016-10-19 09:09:09
categories: 编程之路
---
这里使用的软件名称叫rarcrack，其官方主页: [http://rarcrack.sourceforge.net](http://rarcrack.sourceforge.net/)

该软件用于暴力破解压缩文件的密码，但仅支持RAR, ZIP, 7Z这三种类型的压缩包，其特点是可以使用多线程，而且可以随时暂停与继续(暂停时会在当前目录生成一个xml文件，里面显示了正在尝试的一个密码)。这是真正的暴力破解，因为连字典都没用😂

### rarcrack安装方法

首先从官网下载安装包，然后执行如下命令

```shell
tar -xjf rarcrack-0.2.tar.bz2
cd rarcrack-0.2
make && make install
```

### rarcrack使用方法

执行命令: `rarcrack 文件名 -threads 线程数 -type rar|zip|7z ` 

同时，该软件自带了测试样例，在解压目录里，执行`rarcrack test.zip —threads 4 —type zip`，等待一会儿即可得到结果，其密码是`100`，很简单。在执行过程中，还会打印当前尝试的速度，比如:

```shell
Probing: 'oB' [527 pwds/sec]
Probing: 'Nh' [510 pwds/sec]
Probing: '0c3' [512 pwds/sec]
Probing: '0AV' [514 pwds/sec]
```

如果要改变当前密码破解的位置，可以直接打开xml，修改当前密码到那一行密码即可。xml内容如下:

```tex
<?xml version="1.0" encoding="UTF-8"?>
<rarcrack>
  <abc>0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</abc>
  <current>104</current>
  <good_password>100</good_password>
</rarcrack>
```

在执行过程中，如果出现如下错误:

```shell
gcc -pthread rarcrack.cxml2-config --libs --cflags-O2 -o rarcrack  
/bin/sh: 1: xml2-config: not found  
In file included from rarcrack.c:21:0:  
rarcrack.h:25:48: 致命错误： libxml/xmlmemory.h：没有那个文件或目录  
编译中断。  
make: *** [all] 错误 1
```

那么可以执行`sudo apt-get install libxml2-dev libxslt-dev`进行修复。