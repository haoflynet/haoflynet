---
title: "Python Redis模块的使用"
date: 2015-05-29 21:42:08
categories: 编程之路
---
Python可以使用redis模块直接操作Redis数据库

PyPI文档：<https://pypi.python.org/pypi/redis/2.10.3>

可直接使用pip进行安装。

redis-py使用两个类来完成Redis的操作。

redis-py使用一个连接池来管理Redis server。每个Redis实例都默认会创建自己的连接池。

## 基本使用

    import redis
    # 数据库的连接
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')   # 添加一条记录
    r.get('foo')          # 获取某字段的值

如果是使用连接池创建的，那么可以直接从连接池获取对象实例：

    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)

## Pipelines

Pipelines是redis的一个子类，用于同时提交多条命令(批量执行)，依次减少TCP请求，提高性能。常见使用方法：



    r = redis.Redis(......)
    pipe = r.pipeline()




    # 这样下面的redis命令都会先被缓冲




    pipe.set('foo', 'bar')
    pipe.get('bing')




    # 下面的命令会提交所有的命令到服务器




    pipe.execute()




    # 十分高级的魔术方法：




    pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').exectue()
