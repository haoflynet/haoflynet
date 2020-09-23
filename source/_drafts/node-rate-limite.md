# **[node-rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible)**

```javascript
const rateLimiter = new RLWrapperBlackAndWhite({
  limiter: new RateLimiterMySQL({
    storeClient: mysql.createPool({
      connectionLimit: 100,
      host: dbOptions.host,
      user: dbConfig.username,
      password: dbConfig.password,
    }),
    dbName: dbConfig.database,
    tableName: 'reqRateLimit',
    points: config.rateLimit.points,
    duration: config.rateLimit.duration,
  }),
  whiteList: config.rateLimit.whiteList,
  isWhiteListed(ip) {
    return /(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)/.test(ip)
  }
});


nuxt.js的使用
const rateLimiter = new RLWrapperBlackAndWhite({
  limiter: new RateLimiterMemory({
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
    await rateLimiter.consume(getRealIpFromCtx(req.ctx))
  } catch (rejRes) {
    console.error('Too Many Requests: ' + getRealIpFromCtx(req.ctx))
    res.data = {
      msg: 'Too Many Requests'
    }
    res.statusCode = 429
    await res.end()
  }
  await next()
}

```

