---
title: "PHP http请求库Guzzle使用手册"
date: 2018-05-14 10:32:00
categories: php
---

肯定是用的协程不是线程



发送空的request，在pool的时候如果generator循环一直不yield request的话会造成cpu一直被占用，这时候需要可以发送空的promise，代码如下

```php
      yield function() {
        return new Promise();
      };
```

每250毫秒去检查一下curl_multi_exec中的线程的执行结果

