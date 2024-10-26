---
title: "curl手册"
date: 2016-04-07 08:01:39
updated: 2024-10-11 10:41:00
categories: tools
---
## 常用参数

```shell
--connect-timeout：设置最大连接时间
-d：传递数据，可以是JSON数据也可以是直接的POST数据
-F: 发送form表单数据的一个参数
-I：仅显示文档信息(HTTP状态码什么的)
-k：禁用ssl验证
-o/-O: 下载文件(前者指定下载文件名，后者不用指定)
-s：静默模式，不输出任何东西
-x: 设置代理，代理一定要加端口
-X：请求方式，GET、POST、DELETE等
-H: 设置请求头，比如-H "Content-Type: application/json"
--location: 自动处理重定向
```

<!--more-->

## 常用操作

```shell
# 只获取响应头
curl -X HEAD -I http://haofly.net

# 提交表单
curl -X POST -F 'username=davidwalsh' -F 'password=something' http://domain.tld/post-to-me.php

# 下载文件
curl -o test.txt haofly.net/test

# 打印详细的连接时间、传输时间、下载速度等
curl -w %{http_connect}:%{time_namelookup}:%{time_redirect}:%{time_pretransfer}:%{time_connect}:%{time_starttransfer}:%{time_total}:%{speed_download} haofly.net
curl -o /dev/null -w "Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" https://haofly.net	# 只关心连接时间、处理时间和总耗时
```

## Header头信息参数

```shell
Host: 客户端指定自己想要访问的WEB服务器的域名/IP地址
```

##### TroubleShooting

- **curl: (3) [globbing] nested braces not supported at pos 131**: 特殊字符需要转义，例如`{}`
- **遇到curl编码问题，可以尝试用[在线编码转换网站](https://tool.oschina.net/encode?type=4)进行url encode**