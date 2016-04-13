---
title: "从Tornado谈异步与非阻塞"
date: 2016-04-11 23:59:57
categories: 编程之路
---
在做毕业设计的时候，由于后端有一个耗时任务，所以想到了异步，又由于长期使用Python，进而想到了Tornado，然后，我就半个月没做毕设了，说来全是坑啊。在了解异步与阻塞的原理之前我就盲目地想从代码层面去实现，这样只会浪费时间。所以这里我就先描述一下我对这几个概念的理解。
### 异步与同步：是消息通信机制的层面
采用异步的时候，程序并不关心该操作的结果，所以并不会有返回结果，比如ajax，一般会给异步操作赋予一个回调函数，通过这个回调函数对结果进行处理，而不是直接将结果返回给外部(在ajax如果return结果则会是一个null值)
### 阻塞与非阻塞：指程序在等待调用结果时的状态
如果是阻塞，则程序会一直等待程序返回结果，如果是非阻塞，则不会等待，而继续执行下面或者其他的代码了。
### 阻塞式IO
耗时型任务一般分为两类：CPU耗时型任务和IO耗时型任务。CPU指一般的代码运算执行过程，IO一般分为两大类，计算型IO和阻塞式IO。如果仅有一个线程，那么同一时刻只能有一个任务在计算，但如果是阻塞式IO，它可以让它先阻塞掉，然后去计算其他的任务，等到内核告诉程序那边没有被阻塞了就、再回到之前的地方进行之后的运算。

所以，在了解了这些概念过后，我就知道了为什么要发挥tornado的异步特性就得依赖异步库([Tornado官方提供的第三方异步库](https://github.com/tornadoweb/tornado/wiki/Links))，而不是随便一行代码都能变成异步非阻塞式的代码。比如我试验时使用的一个sleep函数：

```
    def sleep(self):
        for i in range(100000000):
            if i % 100000 == 0:
                print(i)
        self.set_cookie('setting', 'hao')
```

看吧，这是一个计算型任务，由于tornado是单进程单线程，所以无论怎么做也不可能实现在访问该请求的时候访问其他请求，因为CPU只能执行当前任务，其他请求必须等到这个请求结束后才能成功，这也是为什么部署tornado的时候几乎都是用nginx+多实例事实上，同理，其他的框架基本上都是需要nginx、apache等配合才能同时服务于多个请求的。Tornado的异步库，几乎都是用来进行阻塞式IO任务的，所以只有他们才能发挥其异步特性。

Tornado的异步实现就是将当前请求的协程暂停，等待其返回结果，在等待的过程中当前请求不能继续往下执行，但是如果有其他请求(同样是一个协程)，只要不也是阻塞式IO，那么就会直接去处理其他的请求了。

当然，包括nodejs的异步等，这些统统都是有历史原因的，JavaScript和Python在发展之初都只支持单进程单线程，即使使用多线程技术最多也只能利用到100%的单核，多核在这里似乎并不使用，而如果要使用多进程变成，光靠框架是做不到的，必须自己根据实际需求来处理多进程之前的数据共享、资源竞争等问题。所以，在我的理解里，如果能直接利用多线程编程就不需要用服务端异步，毕竟，多线程的发明本身也是为了解决阻塞式IO的问题。

## 多线程实现异步、非阻塞、并行请求、并行计算
其实我认为多线程相比于异步非阻塞有很大的优点，不可否认，多线程在线程切换上存在开销，并且在资源竞争上需要写更多的逻辑，稍微控制不好就会导致服务出错，然而，多线程在处理并行任务上有先天的优势，这一点光看名字就看得出来，下面介绍Tornado的多线程和Flask多线程的用法，其中Tornado的多线程是指由程序将当前请求中的代码交由其他线程处理，而flask的多线程就是类似apache服务器，另起一个进程来处理请求。

注意：两者都可以使用global来引用全局变量

#### Tornado实现：当前请求会立马返回一个结果并断开当前http连接，所以不能在这里设置cookie

```
	import tornado.ioloop
	import tornado.web
	import time
	from concurrent.futures import ThreadPoolExecutor
	import tornado.httpclient
	from tornado.concurrent import run_on_executor

	class Executor(ThreadPoolExecutor):
		_instance = None

    	def __new__(cls, *args, **kwargs):
        	if not getattr(cls, '_instance', None):
            	cls._instance = ThreadPoolExecutor(max_workers=10)
        	return cls._instance

	class SleepHandler(tornado.web.RequestHandler):
    	executor = ThreadPoolExecutor(10)

    	def get(self):
      	tornado.ioloop.IOLoop.instance().add_callback(self.sleep) # 相当于丢到下一个时间循环去  
        	self.write("when i sleep")		# 请求会立马返回这个值并断开连接

    	@run_on_executor
    	def sleep(self):
        	for i in range(100000000):
            	if i % 100000 == 0:
                	print(i)
        	self.set_cookie('username', 'hao')

        	print("yes")
        	return 5

	class TestHandler(tornado.web.RequestHandler):
    	def get(self):
        	if not self.get_cookie('username'):
            	self.write('没有')
        	else:
            	self.write('有')
            	
	application = tornado.web.Application([
		(r"/test", TestHandler),
		(r"/sleep", SleepHandler),
		], debug=True)

	if __name__ == "__main__":
    	application.listen(8888)
    	tornado.ioloop.IOLoop.instance().start()
```

#### flask实现：直接在启动时添加参数，当前请求不会立马返回一个返回值，会一直处于连接状态，所以可以设置cookie

```
	from flask import Flask,request,make_response
	app = Flask(__name__)

	@app.route('/')
	def hello_world():
		username = request.cookies.get('username')
    	if username is None:
       	return '没有'
    	else:
        	return '有'
    	return username

	@app.route('/s')
	def sleep():
    	for i in range(100000000):
        	if i % 100000 == 0:
				print(i)
		resp = make_response('ok')
    	resp.set_cookie('username', 'the username')
    	return resp

	if __name__ == '__main__':
		app.run(debug=True, threaded=True)
```

**参考文章**  
[知乎：怎样理解阻塞非阻塞与同步异步的区别?](https://www.zhihu.com/question/19732473)  
[Tornado文档：异步非阻塞I/O](http://tornadocn.readthedocs.org/zh/latest/guide/async.html)  
[Tornado教程：异步Web服务](http://docs.pythontab.com/tornado/introduction-to-tornado/ch5.html)  
[使用tornado的coroutine进行编程](http://cloudaice.com/tornado-coroutine/)  
[我在segmentfault的提问：无法理解tornado的异步](https://segmentfault.com/q/1010000004910793?_ea=722806)  