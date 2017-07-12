---
title: "wireshark抓包工具教程"
date: 2016-05-07 11:02:30
updated: 2017-07-11 12:45:00
categories: tools
---
## 网络监听原理

### 无线网卡的监听模式

- 托管模式(Managed mode): 在这个模式下，无线网卡只专注于接受从WAP发给自己的数据包文。
- 监听模式(Monitor mode): 无线网卡会监听空气中所有的无线通信。不同的无线网卡启用监听模式的方式可能不相同。

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