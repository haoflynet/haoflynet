---
title: "CORS 跨域请求简介"
date: 2018-09-14 20:00:00
categories: 编程
---

CORS，即`Cross-origin resource sharing`，跨域资源共享，常用于帮助浏览器实现向不同的域名发送请求的功能。

浏览器为了安全着想，采用了同源策略(即url协议、域名、端口中任何一个不一样，就认定是跨域的)。默认是不允许js向不同的域名请求资源的，这样可能发生CSRF攻击。例如B域名有个删除数据的接口，用户登录了B域名后，关闭网页，当然一般情况cookie会在浏览器保留一段时间，如果用户在访问A域名时，A域名在网页上面悄悄向B域名发送删除请求，如果浏览器没有限制，而B域名的cookie也确实存在，则会造成严重后果。

既然后果很严重，为什么还需要`CORS`呢，一是前端可能需要向不同的域名获取资源，二是随着前后端分离的发展，前端和后端域名如果不同，也许要跨域，如果相同，那运维就要多加配置去让两者在同一个域名下了，增加维护成本。

需要注意的是，开启`CORS`后，会有一定的风险，**尽量不要将`Access-Control-Allow-Origin`设置为允许所有来源，即'*'**，另外，前端一定要做好数据的验证，对于用于的输入，不要直接拿来作为html元素或者script片段进行执行

<!--more-->

### 服务器开启CORS

- 程序举例：
  - python自带`httpserver`开启`CORS`: 见[Python 手册](https://haofly.net/python/index.html)
  - `Tornado`开启`CORS`: 见[Tornado 手册](https://haofly.net/tornado/index.html)
  - `Flask`开启`CORS`: 见[Flask 手册](https://haofly.net/flask/index.html)

在每次需要`CORS`的时候，浏览器会首先发送一个`OPTIONS`请求用于预检，预检的时候，会带上`Origin(来源域名)`、`Access-Control-Request-Method(请求方式)`、`Access-Control-Request-Headers(额外头信息)`，预检的这一步，前端不需要做任何的额外操作，`OPTIONS`是浏览器去发送的，服务器收到该请求并检查完这几个关键头信息后，如果没问题，就会进行这样的响应(所以服务器这边是要接收一个`OPTIONS`请求的接口的)，内容随便，浏览器只需要头:

- `Access-Control-Allow-Origin`: 必须，允许的来源域名，例如:`https://haofly.net:11111`。

- `Access-Control-Allow-Method`: 允许的请求方法，例如`PUT, GET, POST`
- `Access-Control-Allow-headers`: 指定浏览器CORS请求额外发送的头信息字段，逗号分割
- `Access-Control-Allow-Credentials`: 是否允许携带cookie，`true`
- `Access-Control-Max-Age`: 预检有效期，在指定事件内不需要再次预检

而预检成功后，以后每次请求只需要返回一个`Access-Control-Allow-Origin`即可。

##### 扩展阅读

[阮一峰跨域资源共享 CORS 详解](http://www.ruanyifeng.com/blog/2016/04/cors.html)