---
title: "Splash js执行server"
date: 2017-05-01 14:26:00
categories: tools
---
`splash`是一个轻量级的可执行脚本的server，并且提供了友好的API，而且能直接用docker进行部署，使用起来十分方便，对于那种必须通过js才能找到内容的爬虫来说简直是如虎添翼。

## 安装splash

最简单的方式，使用docker安装

```shell
docker pull scrapinghub/splash
docker run --name splash -p 5023:5023 -p 8050:8050 -p 8051:8051 -d scrapinghub/splash	# 即可完成部署
```

其中，`5023`表示`http`，`8050`表示`https`，`8051`则是`telnet` 

## splash的配置

配置文件在`/app/splash/defaults.py`，如果是使用docker，那么直接修改该文件即可

```shell
# 在docker内部直接修改该文件/app/splash/defaults.py
PLUGINS_ENABLED = False		# 是否开启flash的执行，默认是关闭了的
```

## splash的API

splash的API是根据其HTTP的url来定义的，前缀都是docker的域名+ip。

### render.html

例如`http://127.0.0.1:8050/render.html?timeout=600&wait=10&proxy=socks5://192.168.0.6:1086&url=http://haofly.net`

```tex
# 参数说明
url: 要请求的url
timeout: js执行超时时间，默认是30s
wait: 等待js执行完成的时间，默认是0，最大是10
proxy: 设置代理
```

### render.har

获取所有的har数据，即请求该地址的时候该网页所有的请求以及`header`和`body`信息。