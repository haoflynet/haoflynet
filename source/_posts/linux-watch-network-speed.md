---
title: "linux命令行查看实时网速"
date: 2014-02-10 19:41:02
updated: 2016-11-09 13:46:00
categories: 编程之路
---
在使用ubuntu desktop的时候，会经常有查看系统当前网速的需求，但是又不愿意花费时间去寻找一款网速查看工具的时候(这样的工具一般都比较臃肿)，那么直接在终端里就能用命令查看网速就很需要了。这里我直接用shell来实现:

```shell
LANG=""
while true
do
	up_time1=`ifconfig $1 | grep "bytes" | awk '{print $6}'`
	down_time1=`ifconfig $1 | grep "bytes" | awk '{print $2}'`
	
	sleep 1
	clear
	
	up_time2=`ifconfig $1 | grep "bytes" | awk '{print $6}'`
	down_time2=`ifconfig $1 | grep "bytes" | awk '{print $2}'`
	
	up_time1=${up_time1}
	up_time2=${up_time2}
	down_time1=${down_time1}
	down_time2=${down_time2}
	
	up_time=`expr $up_time2 - $up_time1`
	down_time=`expr $down_time2 - $down_time1`
	up_time=`expr $up_time / 1024`
	down_time=`expr $down_time / 1024`
	
	echo 上传速度: $up_time kb/s
	echo 下载速度: $down_time kb/s
done
```

最后给该文件添加可执行权限后执行`./run.sh wlan0`.

需要注意的是，我这里使用的是无线网络，所以网卡选择的是默认的`wlan0`，如果是有线网络，默认的参数是`eth0`.