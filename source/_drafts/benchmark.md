---
title: "性能优化工具及好的文章"
date: 2018-08-20 21:32:00
categories: ab
---

```shell
yum install apr-util yum-utils httpd-tools
```

uwsgi processes = 4
每个请求耗时 30ms，一个 process 一秒可以处理 30 左右的请求，4 个 process 可以处理 120 个请求，差不多。

既然是 4 核机器，你把 processes 设置成 8 个试试。



1个请求150ms

100个请求却花了4s。相当于每秒25个请求，

1个请求耗时150ms，一个进程一秒处理1000/150=6.67个请求，2核心，8个进程每秒能处理53.36个请求

如果进程数是4，每个请求耗时30ms，那么一个进程一秒可以处理30左右的请求，4个就可以处理120个。

python进程数量一般是cpu核心数量的2倍。

这个优化不了了的情况下

2核4线程，

我现在有10个进程，假设是10个线程嘛，能同时处理10个。那差不多是1秒撒

如果串行处理100个请求，那么就是10s

2核4线程

16个进程32个线程，

100个请求100个并发需要3s

后端可是





ab -n 100 -c 10 -H "client:xxx" http://test.com/` 其中－n表示请求数，－c表示并发数

ab -p data.txt -T application/json -H "client:xxx" -H "token:xxx" -n400 -c400 http://localhost:8080/xxx



=====的萨嘎===



网页性能https://testerhome.com/topics/16883



http://blog.richardweitech.cn/2018/11/04/nodejs-performance/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io

https://segmentfault.com/a/1190000002491609





https://github.com/apache/jmeter   jmeter ui界面

