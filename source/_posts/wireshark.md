---
title: "wireshark抓包工具教程"
date: 2016-05-07 11:02:30
categories: tools
---
# wireshark抓包工具

## 表达式语法
- **IP过滤**

   ip.src == 192.168.1.1 # 过滤源地址
   	ip.dst == 192.168.1.1 # 过滤目的地址
   	ip.addr == 192.168.1.1 # 过滤源或者目的地址
   	!(ip.src == 192.168.1.1) # 排除某地址
   	http.request.uri matches "login" # 过滤url中含有login的http请求
- **端口过滤**
   tcp.port == 80 
- **协议过滤**
   http  # 只显示http协议
- **内容过滤**
   udp.length > 20
   	http.content_length > 20

## HTTPS

https://imququ.com/post/http2-traffic-in-wireshark.html