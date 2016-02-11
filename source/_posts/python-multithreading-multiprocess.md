---
title: "python多进程和多线程"
date: 2015-12-30 03:28:42
categories: 编程之路
---
多线程和多进程能极大限度的利用线代计算机强大的CPU，在IO密集型的应用场景里十分常见，目前项目中有个需求，是需要向别人网站发送请求等待响应，不过必须等页面
的js执行完毕后才能获取内容，就得将执行时间设置得长一点，比如10s，如果每个请求都等这么久那效率实在太慢，所以趁此机会，学习了一下Python的多进程和多
线程编程。  

在Python里面多进程和多线程的区别

  * Python里的多线程只能利用CPU的一个核(由于全局解释锁的历史原因)，而多进程则能利用多核的优势
  * 多线程一般来说比多进程快，毕竟共享内存，但是多线程也更危险，因为一个线程崩溃可能导致整个程序崩溃

# **Python多线程**

  * 定义与使用  


        import threading

    class Thread(threading.Thread):
        def __init__(self, 变量):
            threading.Thread.__init__(self)
            self.变量 = 变量
        def run(self):
            逻辑
    thread = Thread(参数) # 定义一个线程
    thread.start()        # 开启一个线程

  * 全局变量：加锁，对于全局变量，如果仅仅是引用其值，而不对其进行修改，那么可以直接引用，如果要进行修改，就必须加锁，否则会出现不可预期的错误，比如可能会导致MySQL连接意外断开  


        LOCK = threading.Lock()  # 在全局定义一个锁
    # 局部使用
    LOCK.acquire()
    修改全局变量
    LOCK.release()

  * 局部变量：虽然局部变量简单的使用直接用就行，但是如果要在run里面进行各个函数之间的传递那就麻烦了，所以提供了ThreadLocal来将线程内部的局部变量变为一个字典，其它函数直接调用即可  


        LOCAL = threading.local() # 在全局定义，每个线程引用该值结果都仅仅会得到自己的私有变量
    # 在Thread类里面的run函数赋值，不能在__init__里面定义，因为那时候线程还没启起来
    LOCAL.变量名 = 值 # 就这样

  * 常用方法  


        threading.activeCount()  # 获取当前线程数量，我一般用这个来控制线程最大的数量
    threading.currentThread() # 获取当前线程对象
    threading.currentThread().getName() # 获取当前线程的名称
    exit()         # 终止当前线程，网上好多人问怎么没有API，后来发现exit就行了...并不会影响到其它线程和主线程

# **Python多进程**

waiting...
