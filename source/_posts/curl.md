---
title: "curl 教程"
date: 2016-04-07 08:01:39
updated: 2017-06-23 15:17:00
categories: tools
---
# curl

## 常用参数

	--connect-timeout：设置最大连接时间
	-d：传递json数据
	-F: 发送form表单数据的一个参数
	-I：仅显示文档信息(HTTP状态码什么的)
	-s：静默模式，不输出任何东西
	-X：请求方式，GET、POST、DELETE等
	-H: 设置请求头，比如-H "Content-Type: application/json"

```
curl -X POST -F 'username=davidwalsh' -F 'password=something' http://domain.tld/post-to-me.php
```
## 常用操作

```shell
# 只获取响应头
curl -X HEAD -I http://haofly.net
```

