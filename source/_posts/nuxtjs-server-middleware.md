---
title: "为NuxtJs引入Rate Limit服务端渲染中间件(serverMiddleware)"
date: 2020-09-20 16:40:00
categories: server
---

目前项目要为所有的请求添加调用频率限制，使用的是[node-rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible)插件，后端api项目可以直接在将其作为一个[Koa Middleware](https://github.com/animir/node-rate-limiter-flexible/wiki/Koa-Middleware)，但是前端却不能直接这样引用，因为我们前端使用了`nuxtjs`，如果直接将该插件作为`koa middleware`插入`app`中，那么每一个请求都会经过该插件的统计，包括页面中所有的静态文件请求等，但这其实并不是我们想要的，我们其实只想针对路由`route`进行统计和过滤。这时候可以将该插件插入`nuxtjs`的`serverMiddleware`中去，作为`nuxtjs`的服务端中间件使用。

- `serverMiddleware`的执行时机是服务端开始渲染页面之前，所以是**服务端渲染的中间件**

- `serverMiddleware`可以针对指定的路由，如果不指定，则表示针对所有的路由

其配置是在`nuxt.config.js`中的，例如:

```javascript
serverMiddleware: [
  '~/serverMiddleware/rate-limiter.js', // 这里定义我们编写的rate-limiter插件，针对的是所有路由，注意是路由，不是每个页面请求

  // Will register file from project api directory to handle /api/* requires
  { path: '/api', handler: '~/api/index.js' },

    // We can create custom instances too
    { path: '/static2', handler: serveStatic(__dirname + '/static2') }
]
```

<!--more-->

然后我们可以这样定义中间件详情:

```javascript
const { RateLimiterMemory, RLWrapperBlackAndWhite } = require('rate-limiter-flexible')

const rateLimiter = new RLWrapperBlackAndWhite({
  limiter: new RateLimiterMemory({	// 因为nuxtjs没有直连数据库，所以这里使用的是内存来记录
    points: 60,
    duration: 60
  }),
  whiteList: ['::ffff:127.0.0.1'],
  isWhiteListed (ip) {
    return /(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)/.test(ip)
  }
})

export default async function (req, res, next) {
  try {
    await rateLimiter.consume(ctx.ip)
  } catch (rejRes) {
    console.error('Too Many Requests: ' + ctx.ip)
    res.data = {
      msg: 'Too Many Requests'
    }
    res.statusCode = 429
    await res.end()
  }
  await next()
}

```

