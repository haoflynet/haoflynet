---
title: "rclone网盘同步工具"
date: 2017-08-20 22:52:39
categories: tools
---

推荐一个动漫网站[JA日本动漫交流平台](jac-animation-net.blogspot.hk)，没有这个网站，我也不会想着去找这个好用的工具(看动漫看电影还是支持正版，不过由于某些众所周知的原因，我们有时候没有选择)。该网站是通过google drive进行传播，你可以将文件保存到自己的google drive里面去，然后使用rclone工具进行下载，在没有使用代理的情况下，速度也还是客观的，各方面压制垃圾百度云。百度云上几百G的文件我同步下来花了两周，还是用的aria2，不用aria2的话，基本没有速度。

**rclone支持Google Drive, Amazon Drive, S3, Dropbox, Backblaze B2, One Drive, Swift, Hubic, Cloudfiles, Google Cloud Storage, Yandex Files，不仅支持主流的几个云盘，而且支持几个主流的对象存储平台。软件本身支持跨平台的安装使用。**

### rclone安装

直接参考[官方文档](https://rclone.org/install/)，包括了Linux，MacOS以及源码安装方式

### rclone配置

通过`rclone config`命令可以进行交互式的配置，参见[官方文档](https://rclone.org/drive/)

##### 代理设置

只需要设置环境变量`HTTP_PROXY`或者`HTTPS_PROXY`或者`NO_PROXY`即可，例如`export HTTP_PROXY=127.0.0.1:8118`

### rclone使用

假设上一步添加配置时候取的名字叫`google`，`google drive`里面有目录叫`test`

- rclone ls google:test	       # 列出远程目录下的所有文件 
- rclone sync -v google:test   # 将远程目录下的所有文件同步到本地
- rclone mount /path/本地目录 google:test   # 将远程目录直接挂载到本地，这一步就和很多的同步盘差不多了。我有个猜想是这个能拿来备份timemachine。远程的文件会显示在挂载的目录里面，但是不会下载，只有使用的时候才会下载，使用起来方便，并且节约本地资源。需要注意的是，这还只是个实验功能，可能会不稳定。我使用起来唯一的不爽是不能选择下载下来。
- rcloen copy google: google1  # 直接两个网盘之间对拷文件，并且不会经过本地，真的是太方便了。