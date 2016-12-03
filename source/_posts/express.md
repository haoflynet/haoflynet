---
title: "express 教程"
date: 2016-08-07 07:52:39
categories: frontend
---
#  Express

[官网](http://expressjs.com/zh-cn/)说: "高度包容、快速而极简的Node.js Web框架"，我认为Express最大的优点是可用于API开发，而不是web开发，首先，它的路由定义简单，其次，nodejs天生的异步特性使得其性能极佳。

### 安装方式

```
npm install express-generator -g   # 安装应用程序生成器
express myapp  # 生成一个名为myapp的工程目录
cd myapp && npm install # 安装依赖项
DEBUG=myapp:* npm start # MacOS或Linux上启动
```

然后在浏览器访问`http://localhost:3000/`即可访问应用程序了.

## 请求与相应

### 请求

``` 
# 获取请求参数
req.query.name
```

## 路由

路由结构定义为:`app.METHOD(PATH, HANDLER)`，例如

```app
app.get('/', function(req, res){
  res.send('Hello World!');
})
```

## 中间件

中间件函数能够访问请求对象(req)、相应对象(res)以及应用程序的请求/相应循环中的下一个中间件函数。

`app.use([path], function)`用于加载处理http请求的中间件(middleware)，请求会以此被use的顺序处理。