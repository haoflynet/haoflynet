---
title: "linux命令行查看实时网速"
date: 2014-02-10 19:41:02
categories: 编程之路
---
> 封面图片来自：Pixabay

>

> 我们有时候经常会想查看系统的网速，但是又懒得打开那些能够查看网速的应用，那么直接在终端里用命令行查看网速就很想需要了。不过，貌似ubuntu并没有提供类
似的命令，所以直接写了个shell来实现，具体代码如下：  
LANG=””  
while true  
do  
up_time1=`ifconfig $1 | grep "bytes" | awk '\{printf $6\}'`  
down_time1=`ifconfig $1 | grep "bytes" | awk '\{print $2\}'`

>

> sleep 1  
clear

>

> up_time2=`ifconfig $1 | grep "bytes" | awk '\{print $6\}'`  
down_time2=`ifconfig $1 | grep "bytes" | awk '\{print $2\}'`

>

> up_time1=$\{up_time1##bytes:\}  
up_time2=$\{up_time2##bytes:\}  
down_time1=$\{down_time1##bytes:\}  
down_time2=$\{down_time2##bytes:\}

>

> up_time=`expr $up_time2 - $up_time1`  
down_time=`expr $down_time2 - $down_time1`  
up_time=`expr $up_time / 1024`  
down_time=`expr $down_time / 1024`

>

> echo 上传速度：$up_time kb/s  
echo 下载速度：$down_time kb/s  
done  
保存该文件为wangsu，并添加可执行的属性，然后执行`./wangsu
wlan0`(我这里用的是无线网，所以是wlan0,如果是有线网，一般参数是eth0)就会看到实时的网速了。最后执行`sudo cp wangsu
/usr/sbin/`命令，将文件复制到/usr/sbin目录，以后就可以直接用命令`wangsu wlan0`查看了

相关命令介绍：

[awk命令详解](http://haofly.net/awk/ "Link: http://haofly.net/awk/" )

[expr 命令详解](http://haofly.net/expr/ "Link: http://haofly.net/expr/" )
