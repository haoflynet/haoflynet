---
title: "Web状态代码解释及常见出错原因"
date: 2014-12-27 15:16:40
categories: 编程之路
---
由于在实际项目中，经常遇到前后端传递错误代码，或者发现错误代码的情况，而每次遇到都不一定能快速找到原因，所以这里就把常见的错误代码列出来，并附上我在实际开发
中所遇到的问题的原因。



### 1xx消息

  * 100：continu
  * 101：Switching Protocols
  * 102：Processing

### 2xx成功：表示请求成功

  * 200：OK，请求成功就返回它
  * 201：created
  * 202：accepted
  * 203：non-authoritative information
  * 204：no content
  * 205：reset contentt
  * 206：partial content
  * 207 multi-status

###  3xx重定向：用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息

  * 300：multiplechoices
  * 301：moved permanently
  * 302：temporarily moved，暂时性转移，一般是在代码中使用有redirect时产生的
  * 303：see other
  * 304：not modified
  * 305：use proxy
  * 306：switch proxy
  * 307：temporary redirect

###  4xx请求错误：用于指出客户端的错误

  * 400：bad request
  * 401：unauthorized
  * 402：payment required
  * 403：禁止访问，一般是未给代码赋予相应的权限导致无法访问
  * 404：not found，未找到资源，可能是该文件被删除或路由指向错误.
  * 405：资源被禁止，可能是访问该代码段需要某前提条件，如laravel的filter，例如没有登录等
  * 406：not acceptable
  * 407：proxy authentication required
  * 408：request timeout
  * 409：conflict
  * 410：gone
  * 411：length required
  * 412：precondition failed
  * 413：request entity too large
  * 414：request-uri too long
  * 415：unsupported media type
  * 416：requested range not satisfiable
  * 417：expectation failed
  * 421：there are too many connection
  * 422：未找到属性，可能是拼写错误，laravel里面validate的验证失败返回值也是422
  * 424：failed dependency
  * 425：unordered collection
  * 426：upgrade required
  * 429：retry with

###  5：用于支持服务器错误

  * 500：内部服务器错误，一般是代码在执行中发生了错误，没有做异常处理
  * 501：not implemented
  * 502：bad gateway
  * 503：服务不可用
  * 504：Gateway Time-out，是代理服务器尝试执行请求时，未能及时从上游服务器收到响应
  * 505：http version not supported
  * 506：variant also negotiates
  * 507：insufficient storage
  * 509：bandwidth limit exceeded
  * 510：not extended
