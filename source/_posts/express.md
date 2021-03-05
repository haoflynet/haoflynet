---
title: "express 教程"
date: 2015-11-01 07:52:39
updated: 2020-11-25 16:22:00
categories: frontend
---
[官网](http://expressjs.com/zh-cn/)说: "高度包容、快速而极简的Node.js Web框架"，我认为Express最大的优点是可用于API开发，而不是web开发，首先，它的路由定义简单，其次，nodejs天生的异步特性使得其性能极佳。

## 安装与启动

```shell
npm install express-generator -g   # 安装应用程序生成器
express myapp  # 生成一个名为myapp的工程目录
cd myapp && npm install # 安装依赖项
DEBUG=myapp:* npm start # MacOS或Linux上启动

DEBUG=express:* node app.js	# 打开调试模式
```

然后在浏览器访问`http://localhost:3000/`即可访问应用程序了。

最简单的例子(这个例子基本不能处理任何其他的请求，除非用上面的生成器来生成，就会带了一些解析请求生成响应的功能):

```javascript
var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
```

## 请求与响应

### 请求

``` javascript
// 获取请求参数，比如访问的事http://192.168.1.1:6004/code?code=xxxxx
req.query.name	// 获取get参数
req.params.id 	// 获取路由中用冒号定义的参数
req.body.name	// 获取POST参数

req.url	// 例如：/?code=xxxxx
req.originalUrl	// 例如：/code?code=xxxxx
req.baseUrl	// /code
req.path // 为什么是/，这里的path应该是指除去路由部分，比如app.use('/code')除去这部分
req.get('host') // 192.168.1.1:6004
```

### 响应

```javascript
res.redirect(301, 'http://google.com')	// 301响应
res.status(200).json({})	// JSON响应
```

## 路由

路由结构定义为:`app.METHOD(PATH, HANDLER)`，例如

```javascript
app.get('/', function(req, res){
  res.send('Hello World!');
})

app.post('/*', function(req, res){});	// 使用通配符的路由参数
```

## 中间件

中间件函数能够访问请求对象(req)、相应对象(res)以及应用程序的请求/相应循环中的下一个中间件函数。

`app.use([path], function)`用于加载处理http请求的中间件(middleware)，请求会以此被use的顺序处理。