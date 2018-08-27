---
title: "Tornado 手册"
date: 2015-08-05 12:02:30
updated: 2018-08-27 10:24:00
categories: python
---
# Tornado
[中文文档](http://www.tornadoweb.cn/documentation) 
是不是很神奇，我居然会学习除Django以外的另一种Python Web框架。但事实确实如此，我学了，并且用了一下，感觉和Django确实存在很大的不同的。 
学这个的主要原因是要参加饿了么的黑客马拉松，主题是使用Python或Java或Node设计Resutful API，来应对高并发的请求，保证数据的一致性。虽然最后的分数并不理想，但是在这次比赛中学到了很多的东西，Tornado就是其中之一。 
以前只听说过Tornado比Django拥有更高的并发和异步特性，只听过Django坚持自己造轮子，其他语言的Web框架也只用过PHP的Laravel，当安装完Tornado后完全不知道该怎么玩儿，怎么着玩意儿自己不会生成一个项目，项目的框架还要自己写。后来才体会到，这样的好处，简洁、直观、轻便，它只提供最基础的东西，其他一切问题都由你自己来解决，同时，短短几千行的源代码，在遇到问题的时候，我们完全可以直接看源代码来查找问题出在哪儿，这就是简洁带来的好处。另外异步的作用也只有在实际需要的时候才能体会出来。由于我从来没写过异步的代码，所以，只是按照之前写代码那样，而没有根据异步的特性来实现，异步的代码是要在会阻塞的地方使用回调函数来实现，所以，我的程序并不能得高分。不过后来才知道Tornado通过gen将同步代码转换为异步的实现。  

要想自己定义代码结构，可以参考[qiwsir/TornadoWheel](https://github.com/qiwsir/TornadoWheel)

<!--more-->

## 基本框架

[Tornado项目基本结构](https://github.com/haoflynet/project-structure/tree/master/Tornado)，需要注意的是Tornado要想实现`Rest`，只能用第三方库或者自己写，所以我研究出这样一种结构，可以直接实现Rest，非常实用。其中`Tornado`使用`sqlalchemy`连接数据库时推荐使用`tornado-sqlalchemy`库，它让`sqlalchemy`拥有了异步的特性，可以参见基本结构里的结构。

### 路由

```python
(r"/voices/(?P<user_id>\d*)", UserHandler)	# 带命名参数的路由
```

### handler

```python
class HelloHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)	# 实用线程池去执行
    
    def get(self):
        self.write('hello world!')
         
    @run_on_executor	# 以线程池的方式执行，手动异步
    def post(self):
        xxx
        
    def optinons(self):	# 跨域访问支持
        self.set_status(204)
        self.finish()
        
    def set_default_headers(self):	# set_default_headers会在请求开始的时候设置HTTP头，这里的例子是用于支持CORS的
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def initialize(self):			# handler开始前执行
        self.db_session = db.DB_Session()	
    
    def on_finish(self):			# handler结束后执行，如果内部跑错误也会执行
        self.db_session.close()
```

### Request

```python
self.request.body					# 获取请求内容，字节类型
self.request.arguments				# 获取全部请求参数
self.request.query_arguments		# 获取全部GET请求参数
self.request.body_arguments			# 获取全部POST请求参数
name = self.get_argument('name')	# 获取GET或者POST参数
self.request.remote_ip				# 获取客户端真实IP
data = tornado.escape.json_decode(self.request.body)	# 获取请求的json数据
```

### Response

`self.finish()`代表http请求会断开，但是并不代表请求处理逻辑的终结。和回应无关的请求逻辑完全可以放在`finish`之后进行。`write`之后可以`finish`，但是`finish`之后不能再`write`。`write`可以执行多次，如果是字符串，那么结果会累加，如果是`json`那么结果会取第一个`json`。

```python
self.write(result)	# 如果参数是一个字典，那么会直接返回json数据。如果是字符串也是可以的。但是这里不能允许为数组，因为存在一个潜在的垮与安全漏洞。详情见http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write，简单的原因就是因为数组作为javascript脚本是合法的，而json数据作为script是不合法的，如果用数组，可能会泄露敏感信息
```

## 特殊的帮助函数
#### 处理json请求
`data = tornado.escape.json_decode(self.request.body)`， tornado提供的转义HTML、JSONURL和其他数据的工具，需要注意的是如果是ajax请求，这样子传递可以很好地处理数组的问题:

	$.ajax({
	    url: 'http://127.0.0.1:8888/submit',
	    type: 'POST',
	    dataType: 'json',
	    contentType: 'application/json',
	    data: JSON.stringify(data),
	    error: function(){
	        console.log('error');
	    },
	    success: function(re){
	        console.log('success');
	    },
	});
#### 返回json数据
直接`self.write(字典)`就行了

## 部署

`Tornado`本身提供了自己的`WebServer`，可以直接写一个`main()`函数去包装启动程序:

```python
def main():
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
```

然而`WSGI`才是Python官方认可的规范，但是呢，虽然`Tornado`提供了兼容`WSGI`的方式，但是如果采用这种方式，`Tornado`本身的优点(单线程异步)就发挥不出来了。`Tornado`官方的[Running and deploying](http://www.tornadoweb.org/en/stable/guide/running.html)也认为直接用自己的`WebServer`是更好的方法。

## TroubleShooting


*   


静态文件设置了后，必须访问static前缀