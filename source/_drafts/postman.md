---
title: "Postman 高级用法"
date: 2018-08-07 21:32:00
categories: tools
---

Postman，一款功能强大的HTTP调试软件(以前只是谷歌浏览器的插件，现在已经独立成软件)，最近接触到它的一些高级用法，才发现它原来并没有我想象中那么简单，还有很多的高级用法。其主要有如下功能:

- HTTP/API调试
- 测试API接口
- 生成API接口文档
- 监控API接口
- mock接口数据

下面列举一些常用的功能使用方法。

### 接口直接转换为代码

[postman_01]

可以选择导出成HTTP、C(LibCurl)、cURL、C#(RestSharp)、Go、Java、JavaScript、NodeJS、Objective-C、Ocaml、PHP、Python、Ruby、Shell、Swift等多种语言的代码实现。

### 环境变量

[postman_02]

在[postman_01]那里点击Environment，就可以进入环境变量的设置界面。

同一个接口在不同的环境下，同一个变量可能会有不同的值，比如域名和IP，这个功能能让我们一键切换所需的环境变量。

### 请求示例

在[postman_01]那里的`examples(0)`可以添加请求示例，可以添加请求值与返回值的示例。

### 添加cookie

在[postman_01]那里的cookie可以添加指定域名的cookies

### 测试







https://www.jianshu.com/p/391e995881c0

