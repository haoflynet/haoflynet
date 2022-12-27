---
title: "Sentry 使用手册"
date: 2019-09-05 14:40:00
categories: Javascript
---

虽然后台可以设置不传递第三方插件的错误，但是在特殊情况有些第三方错误无法被识别依然会上传上来，比如在安装了grammarly的safari浏览器里面在使用该插件的时候就会报错，且错误上没有特别的标志。`Unhandled Promise Rejection: [object Object] `，所以在后台直接忽略或者在代码里面这样忽略

```
{ "values":[ { "type":"UnhandledRejection", "value":"Non-Error promise rejection captured with keys: [object has no keys]", "mechanism":{ "synthetic":true, "handled":false, "type":"onunhandledrejection" } } ] }
```

## Troubleshooting
- **yarn install的时候出现错误@sentry/cli error @sentry/cli: Command failed. Exit code: 1 Command: node scripts/install.js**，报错信息没有写明具体的原因，反正可能和yarn有关，用npm单独安装即可`npm install @sentry/cli`
