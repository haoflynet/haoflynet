---
title: "MAC使用Aria2高速下载百度网盘内容"
date: 2017-01-18 13:47:00
categories: tools
---
### Aria2简介

[Aria2](https://github.com/aria2/aria2/)是一个轻量级的多源多线程的跨平台的命令行下载工具，支持HTTP/HTTPs、FTP、SFTP、BitTorrent和Metalink等下载方式。

### Mac安装和使用Aria2

1. 安装Aria2命令行工具

```shell
brew install aria2	# 这样即可，如果下载不下来，就让brew走全局shadowsocks代理
```

2. (可选)安装[ria2GUI](https://github.com/yangshun1029/aria2gui)，这是Aria2的桌面GUI程序，集成了aria2c，支持多线程下载，为完成任务退出自动保存，支持PT/BT，可以显示整体下载速度。方便管理，从github进行下载，下载完成后直接解压打开就是个dmg应用了。

3. 安装百度网盘的导出工具，[谷歌浏览器插件下载地址](https://github.com/acgotaku/BaiduExporter)，由于谷歌把它禁用了，得自己下载来使用(貌似是违反了谷歌插件的不能改变网页内容的条例)。

4. 现在可以打开百度网盘，直接选择导出到rpc即可开始下载了。

   ​