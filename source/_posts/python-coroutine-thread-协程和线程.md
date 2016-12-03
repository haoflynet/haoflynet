---
title: "Python协程与线程"
date: 2016-08-04 11:02:30
updated: 2016-11-30 14:44:00
categories: python
---
## 迭代器/生成器

```python
next(iterator)		# 返回下一个迭代对象
yield a 			# 返回一个迭代对象
yield from iterator	# 相当于for x in iterator \ yield x

# 给生成器传值，例如
def generator():
    jump = yield a
next(iterator)		# 给生成器赋非None值时，只能在开始迭代以后
iterator.send(2)	# 传值给生成器，jump=2
```

## 线程

**线程安全与线程不安全**: 多个线程同时访问一个方法，得到的结果一样就是线程安全的，不一样则是线程不安全的。gevent库是基于事件驱动模型，它的线程是否安全完全看多线程程序是怎么写的，如果仅仅只有gevent一个线程那么不存在线程安全问题。

threading库

```python
lock = threading.Lock()
lock.acquire()
xxxxx
lock.release()
# 更方便的使用：
lock = threading.Lock()
with lock:
	xxxxxxx
```

## 进程

multiprocessing库

## 线程池/进程池

Pool

## 协程(asyncio)

位于标准库中，使用协程来编写单线程的并发，通过IO多路复用技术访问套接字。

```python
import asyncio

# 用装饰器来标记作为协程的函数
@asyncio.coroutine
def countdown(number, n):
    while n > 0:
        print('T-minus', n, '({})'.format(number))
        yield from asyncio.sleep(1)	# 这里会返回一个asyncio.Future对象并将其传递给时间循环，同时暂停这一协程的执行，时间循环监听这一对象，1秒钟后，时间循环会选择刚刚这个协程，将future对象的结果返回给它，然后协程继续执行。这一过程会持续到所有的协程程序全部完成。
        n -= 1

loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(countdown("A", 2)),
    asyncio.ensure_future(countdown("B", 3))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# 在3.5里面，有了新的语法，添加了types.coroutine修饰器
async def slow_operation(n):		# 以这种方式定义协程，在协程里面不能有yield语句，只有return和await可以用于返回
    await asyncio.sleep(1)	# await接受的对象必须是awaitable对象，必须是定义了__await__()方法且这一方法必须返回一个不是协程的迭代器，协程本身也被认为是awaitable对象
    print('Slow operation {} complete'.format(n))

async def main():
    await asyncio.wait([
        slow_operation(1),
        slow_operation(2),
        slow_operation(3),
        ])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

## 并发框架

### concurrent.futures

该库通过相同的API同时支持线程与协程，以POOL的方式进行并行任务的管理。其中`Executors`用于管理`workers`，而`futures`则用于表示一个异步计算的结果，当调用future时会被立即返回，但是不一定就是最终结果。

`ThreadPoolExcutor`改为`ProcessPoolExecutor`就是线程了，真方便。

```python
# 来源: https://pymotw.com/3/concurrent.futures/
# 该例表示一个最大执行进程数为2个的执行器，同时处理5个任务
def task(n):
    print('{}: sleeping {}'.format(
        threading.current_thread().name,
        n)
    )
    time.sleep(n / 10)
    print('{}: done with {}'.format(
        threading.current_thread().name,
        n)
    )
    return n / 10

ex = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
results = ex.map(task, range(5, 0, -1))
print('main: unprocessed results {}'.format(results))	# 这里返回的是一个迭代器
print('main: waiting for real results')
real_results = list(results)
print('main: results: {}'.format(real_results)) # 返回真实的结果


# 用map只能处理相同的任务，可以通过submit来执行需要执行的任务
from concurrent import futures
import threading
import time

def task(n):
    print('{}: sleeping {}'.format(
        threading.current_thread().name,
        n)
    )
    time.sleep(n / 10)
    print('{}: done with {}'.format(
        threading.current_thread().name,
        n)
    )
    return n / 10

ex = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
f = ex.submit(task, 5)
print('main: future: {}'.format(f))
print('main: waiting for results')
result = f.result()
print('main: result: {}'.format(result))
print('main: future after result: {}'.format(f))

# 不按照顺序来获取结果，只要有个任务完成，就执行输出结果，上面那几个方法必须等所有任务执行完了顺序输出，而这个则是只要完成一个就输出一个
wait_for = [
    ex.submit(task, i)
    for i in range(5, 0, -1)
]
for f in futures.as_completed(wait_for):
    print('main: result: {}'.format(f.result()))
```

#### 回调

```python
from concurrent import futures
import time

def task(n):
    print('{}: sleeping'.format(n))
    time.sleep(0.5)
    print('{}: done'.format(n))
    return n / 10

def done(fn):
    if fn.cancelled():
        print('{}: canceled'.format(fn.arg))
    elif fn.done():
        error = fn.exception()
        if error:
            print('{}: error returned: {}'.format(
                fn.arg, error))
        else:
            result = fn.result()
            print('{}: value returned: {}'.format(
                fn.arg, result))

if __name__ == '__main__':
    ex = futures.ThreadPoolExecutor(max_workers=2)
    print('main: starting')
    f = ex.submit(task, 5)
    f.arg = 5
    f.add_done_callback(done)
    result = f.result()
```

#### 任务的取消

`Future`只要还未开始就能被取消，f.cancel()

#### 任务的异常

通过`f.exception()`可以获取到任务抛出了什么样的异常

### gevent

```python
# 最简单的使用
import gevent

def foo():
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')

def bar(abc):
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')

gevent.joinall([		# 把gevent.spawn()放到joinall过后才会真正开始执行
    gevent.spawn(foo),
    gevent.spawn(bar, '参数'),
])

print('abc')	# 这行代码会等待所有协程执行完了过后才会执行
```













``