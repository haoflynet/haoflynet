---
title: "使用Redis锁处理并发问题"
date: 2019-07-15 19:02:40
updated: 2020-04-13 18:20:00
categories: redis
---

上周“被”上线了一个紧急项目，周五下班接到需求，周一开始思考解决方案，周三开发完成，周四走流程上线，也算是面向领导编程了。之前的项目里面由于是自运维，然后大多数又都赶时间，所以在处理定时任务上面基本都是自己在服务器上添加`crontab`，而不是让多个实例自己去处理定时任务的并发锁，之后`Laravel 5.5`开始自带并发锁，我们也打算尽快升级。但是这次项目是`Python`项目，无奈只能自己实现一下，以下这个方案实现起来非常简单且易于理解。这篇文章要解决的主要问题是:**使用Redis锁处理并发问题，保证多进程仅有一个实例在运行，当运行中的实例down了后其它实例中的一个能顶上来，保证有且仅有一个实例在运行**

```python
import redis
r = redis.Redis(...)

last_heart = 0		# 记录上一次得到的锁心跳
free_lock_try = 6	# 锁无心跳的最大次数 

while not r.setnx('mylock', 1):
    now_heart = r.get('mylock')
    print(f"没获取到锁,now_heart={now_heart},last_heart={last_heart},free_lock_try={free_lock_try}")
    if now_heart == last_heart:
        free_lock_try = free_lock_try - 1
        if free_lock_try == 0:	# 锁已经1分钟没有心跳了
            old_heart = r.getset('mylock', 1)	# 将lock重置为1，并返回set之前的心跳值
            if old_heart < now_heart:
                time.sleep(10)
                continue
            else:
                break	# 成功获取到锁，退出循环
    else:
        free_lock_try = 6	# 锁有心跳，重置free_lock_try值
        last_heart = now_heart
    time.sleep(10)

def producer_exit():
    """程序正常退出时候自动清理锁"""
    r.delete('mylock')
import atexit
atexit.register(producer_exit)

# 业务代码
while True:
  r.incr('mylock')	# 让锁心跳加一
  ...
```

我们来看看这段程序都解决了并发锁中的哪些问题

1. 高并发下，多个进程无法同时获取到锁。这里使用的是`redis.setnx`，如果锁已经存在，其他进程是无法重置锁并获取到锁的。另外当多个进程同时发现有锁已经没有心跳了，使用的是`redis.getset`将心跳重置为1，都能`set`成功，但是`get`出来的值多个进程是不一样的，只有真正获取到锁的进程返回的是之前进程的心跳，而其他进程获取到的都是1。
2. 有锁进程正常退出，可以使用`atexit`注册进程退出函数删除锁，这里也可以不要，不过下次启动得等新的进程等待几次心跳
3. 有锁进程意外退出，退出后心跳不再增加，超过`free_lock_try`次数后，其他进程会重新设置并获取锁
4. 所有进程全都意外退出，这个问题不是锁来关心的，可以使用`supervisor`进行守护进程。