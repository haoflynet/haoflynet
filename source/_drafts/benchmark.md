---
title: "压力测试工具-ab使用手册"
date: 2018-08-20 21:32:00
categories: ab
---

```shell
yum install apr-util yum-utils httpd-tools
```

uwsgi processes = 4
每个请求耗时 30ms，一个 process 一秒可以处理 30 左右的请求，4 个 process 可以处理 120 个请求，差不多。

既然是 4 核机器，你把 processes 设置成 8 个试试。



ab -n 100 -c 10 -H "client:xxx" http://test.com/` 其中－n表示请求数，－c表示并发数

ab -p data.txt -T application/json -H "client:xxx" -H "token:xxx" -n400 -c400 http://localhost:8080/xxx



=====的萨嘎===





https://segmentfault.com/a/1190000002491609





https://github.com/apache/jmeter   jmeter ui界面

