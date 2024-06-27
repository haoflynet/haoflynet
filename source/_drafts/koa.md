---
title: "Koa"
date: 2017-05-11 22:52:39
categories: nodejs
---

## koa router

```shell
npm install @koa/router # 安装
```

使用方法

 ```javascript
 const Router = require('@koa/router');
 const app = new Koa();
 const router = new Router();
 
 router.post('/v1/a', async (ctx) => {});
 router.get('/v1/:id', async(ctx) => { // 定义路由参数
   const id = ctx.params.id
 })
 
 app.use(router.routes());
 ```



## Request and Response

```javascript
// Request
ctx.request.body // 获取POST的body
ctx.request.url // 获取请求path
ctx.request.headers // 获取headers
`${ctx.protocol}://${ctx.host}${ctx.url}` // 获取完整的URL
ctx.ip // 获取客户端的IP，默认从X-Forwarded-For中获取

// Response
```



##### 实例

**[jackblog-api-koa](https://github.com/jackhutu/jackblog-api-koa)**: 使用koa写的个人博客系统，基于RESTful架构，使用Node.js,koa,MongoDB,Redis,Token Auth,七牛云存储等。

[Koa2-blog](https://github.com/wclimb/Koa2-blog): 使用Koa2编写的博客系统