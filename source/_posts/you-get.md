---
title: "you-get神器使用指南"
date: 2017-10-10 22:52:39
updated: 2017-10-10 22:42:00
categories: tools
---

`you-get`，强大的视频网站下载工具。与aria2相比，其功能主要用于音视频网站内容的获取，通过音视频网页的url链接直接下载媒体内容，几乎支持所有国内外的主流视频网站(例如: youtube、优酷、Bilibili、爱奇艺等)。这里的视频链接不是指真正视频的链接，而是视频网站的url即可，即使视频网站使用了各种方式混淆也能进行快速下载。使用它无论下载什么网站的视频都能达到满速下载，下载youtube也能几十兆每秒的速度(当然得有能慢速的代理)。

需要注意的是，`you-get`也可以用于其官方没有列出的网站的视频下载，但是无法保证速度和下载稳定性，建议对于其他的网站，使用[`aria2`](https://haofly.net/aria2)工具进行下载

#### 安装you-get

```shell
pip install you-get

# 最好安装ffmpeg依赖，否则很多网站视频是获取不了，目前最新稳定版是3.3.4
sudo apt-get install ffmpeg
```

#### you-get命令用法

```shell
you-get '视频链接'		# 最简单的下载
you-get -i '视频链接'	# 列出视频信息，可以看到该网页提供的视频的信息，一般默认的就好，但有时候也有更高清的可供选择，通过这种方式可以获取其itag，然后用下面的方式进行下载
you-get --itag=127 '视频链接'	# 下载指定质量的视频，国内网站一般默认就是最高清的，但是国外的还有更高清的
you-get -x 127.0.0.1:8118 '视频链接'	# 设置http代理
```

###you-get代码用法

和众多其他命令行工具一样，`you-get`同样支持在代码中直接使用

```python
from you_get.extractors import *	# 可以获取到各个网站的下载器
download_urls([url], title, 'mp4', 0, './videos')
```
