---
title: "MAC使用Aria2高速下载百度网盘内容"
date: 2017-01-18 13:47:00
updated: 2017-08-31 14:50:00
categories: tools
---
### Aria2简介

[Aria2](https://github.com/aria2/aria2/)是一个轻量级的多源多线程的跨平台的命令行下载工具，支持HTTP/HTTPs、FTP、SFTP、BitTorrent和Metalink等下载方式。当然，目测，国内更多用于百度云的下载，不过，自从我家里用了linux的nas，并且迅雷已经不能用的情况下，我也更倾向于使用aria2。

相比于`you-get`以及其他的下载工具，`aria2`最大的优点是其内部的连接数控制缓存控制能够明显提高下载速度，并且不会轻易失败

## Aria2的安装

**For Mac**: `brew install aria2`

**For Debian**: `apt-get install aria2` 

## Aria2的使用

```shell
# 参数说明
--all-proxy=127.0.0.1:8181	# 设置http代理，包括了http/https/ftp
-c: 断点续传，如果有只下载了部分的文件那么继续下载
-k20M: 多大的缓存，默认是20M，建议修改为-k1M，因为网络环境不好
-s5: 使用多少个连接数，默认为5，建议为10
-x1: 每个服务器的最大连接数，默认为1，建议为16
```











1. (可选)安装[ria2GUI](https://github.com/yangshun1029/aria2gui)，这是Aria2的桌面GUI程序，集成了aria2c，支持多线程下载，为完成任务退出自动保存，支持PT/BT，可以显示整体下载速度。方便管理，从github进行下载，下载完成后直接解压打开就是个dmg应用了。


2. 安装百度网盘的导出工具，[谷歌浏览器插件下载地址](https://github.com/acgotaku/BaiduExporter)，由于谷歌把它禁用了，得自己下载来使用(貌似是违反了谷歌插件的不能改变网页内容的条例)。

3. 现在可以打开百度网盘，直接选择导出到rpc即可开始下载了。

   ​