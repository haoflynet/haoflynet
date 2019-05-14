---
title: "Scrapy python爬虫"
date: 2016-08-07 11:02:20
updated: 2019-05-08 21:44:01
categories: python
---
## Scrapy

`Scrapy`可以说是Python爬虫界最著名的一个框架了，在我看来也是最全的一个框架，当然优缺点也是很明显的:

- 文档太多，有很多几分钟就能上手的例子
- Scrapy默认将已经抓取过的和队列中的请求都存储在内存中，不过可以使用`JOBDIR`将进度持久化
- Scrapy本身不支持分布式，要支持分布式，需要依靠`scrapy-redis`，但是该库很久没人维护了，不过逻辑比较简单，可以自己造轮子
- Scrapy要抓取Js生成的页面，需要使用其他的工具来辅助，比如Splash，Selenium等
- Scrapy可以通过设置`CONCURRENT_REQUESTS`设置并发的线程数量，默认是16，另外一个控制是`CONCURRENT_REQUESTS_PER_DOMAIN`默认是8。两个变量都是有作用的，并发有多大，程序就会开多少个子线程。当然，具体怎么执行还是得看CPU，例如，在4核8线程上面，同时仅有8个线程在运行(对于Python来说，其实仅有一个线程)，超过的线程，基本上属于等待唤醒的状态，等那8个线程执行完毕或者遇到IO阻塞的时候才会被唤醒。这一点，对于网络延迟很大的任务非常有用，不用再所有线程去等待了。

在学习scrapy的过程中，如果有看源码的兴趣，建议顺便看看`scrapy-redis`，虽然该项目很少维护，但是却非常有利于搞懂`scrapy`框架。

### 基本框架

新建项目，`scrapy startproject test`目录结构如下(mac里面没有把scrapy命令放到bin里面去，直接搜索命令所在地吧)：

```shell
.  
├── scrapy.cfg  
└── ProjectName  
    ├── __init__.py  
    ├── items.py    # 定义items  
    ├── pipelines.py  # 定义items的处理器  
    ├── settings.py    # 全局社会自  
    └── spiders      # 爬虫文件
        ├── __init__.py  
        ├── 一个爬虫  
        └── 又一个爬虫  
```
### 常用命令
```shell
scrapy startproject test    # 创建项目
scrapy genspider haofly haofly.net # 新建爬虫
scrapy list				# 列出当前project所有的spider
scrapy bench			# 基准测试，测试当前硬件的情况下最大的抓取速度
scrapy check			# scrapy自身的单元测试，很多人都不建议用，很难用，而且没没什么作用

scrapy crawl haofly	--loglevel=critical	# 开始一个爬虫，设置日志级别
scrapy crawl haofly --output=output.json # 开始某个爬虫，output参数会把抓取到的item保留到文件中去
scrapy crawl zhaopin -s JOBDIR=crawls/zhaopni-1	# -s参数可以将进度保存下来，这样可以保留爬取进度，下次只需要再执行该命令就能从中断的地方继续
```

### 通用设置
```python
BOT_NAME   # 定义项目名称
ITEM_PIPELINES = {
    'project.pipelines.PostPipeline': 300,   # 处理获取到的Items的各种方法，会按照后面数值从小到大的顺序依次处理
}
EXTENSIONS = {
    'scrapy.extensions.throttle.AutoThrottle': 0,   # 定义扩展程序，AutoThrottle表示自动限制频率的扩展，还要在下面继续配置其参数
}
SPIDER_MIDDLEWARES = {		# 中间件
   'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,	# 处理非200状态码的中间件
   # 'youtube.middlewares.MyCustomSpiderMiddleware': 543,
}

# 配置AutoThrottle插件，会根据爬取的网站的负载自动限制爬取速度，不开的话默认的下载延迟就是0。通过自动调节，可以自动调节并发数和下载延迟。
AUTOTHROTTLE_ENABLED=True   # 是否开启自动限制频率，不开简直太恐怖了  
AUTOTHROTTLE_START_DELAY=1  # 以秒为单位，默认为5  
AUTOTHROTTLE_MAX_DELAY=10   # 默认为60  
AUTOTHROTTLE_DEBUG=False

CONCURRENT_REQUESTS=16   # 全局并发线程的数量
CONCURRENT_REQUESTS_PER_DOMAIN=8	# 针对某一个域名的最大并发量
CONCURRENT_ITEMS=100     # 同时处理的Items的最大值
REACTOR_THREADPOOL_MAXSIZE=20	# 线程池，主要是为了减少创建销毁线程的开销

COOKIES_ENABLED=False  # 是否开起cookie
LOG_LEVEL='DEBUG'    	# LOG级别，在下面介绍了log的几种级别，默认级别是INFO

REDIRECT_ENABLED=False # 禁止重定向
RETRY_ENABLED=False	# 关闭重试

DUPEFILTER_DEBUG = True		# 打开dupefilter的debug
```
### 爬虫主体

当一个请求被`yield`以后，会立马添加到队列中去；当线程空闲的时候则会从队列中取出；然后经过middleware中间件对request进行处理，最后发起真正的请求。

```python
import scrapy
from scrapy import Request

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['test.com']
    start_urls = ['https://www.test.com/']
    handle_httpstatus_list = [301]	# 捕获非200的响应，301表示允许重定向。HTTPERROR_ALLOW_ALL = True表示捕获所有

    def start_requests(self):
      """生成初始请求"""
      yield Request(url, self.parse, meta={})
  
    def parse(self, respone):
        yield item
        
    def parse_another(self, response):
        # 需要注意的是，所有的回调函数，要么返回item list，要么返回request list，如果什么都不返回，例如，直接写了个self.another_func(...)，如果后面没有yield方法，那么该函数并不会执行
        self.parse_page(response)		# 即使你在parse_page里面返回了yield，该函数也不会执行，最好这样
        for item in self.parse_page(response):
            yield item
```

### 请求与响应

```python
request.meta['proxy'] = 'http://xxx.xxx.xxx.xxx:2333'	# 给meta设置proxy字段则会添加代理

response.body				# 获取响应的body
response.body_as_unicode()	# 获取响应编码后的内容
response.requests			# 获取相应的请求
response.status				# 获取HTTP状态码
response.url				# 获取请求的URL
response.headers			# 获取请求头
```

### Items

`Item`只是对爬取结果对象的一个简单封装，提供了简洁的语法。需要注意的是，在pipeline里面处理item的时候必须`return item`否则，其他的item会接受不到，而且会打印一个莫名其妙的`None`，终端也不会显示抓取到的item，也就不将讲item输出到文件了

```python
# items.py中对item进行定义
import scrapy
class ResultItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

# 在爬虫里面可以这样使用
def parse(self, response):
    item = scrapy.Items()
    item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
    item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
    item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
    yield item
    
# item的常用方法
post['name']
post.get('name')
post.get('name', 'no value')
post.keys()
post.items()
dict(post)	# 将Item转换为字典
Post(dist)	# 从字典创建Item
```

### Pipeline

处理item的管道，用来处理爬虫抽取到的数据，可以在这里面进行数据的验证和持久化等操作。要使用`pipeline`，必须在设置里面将`ITEM_PIPELINES`的注释取消掉

```python
class TestPipeline(object):
    def open_spider(self, spider):	# 爬虫开始时候执行
        print('open')
        self.session = DB_Session()

    def close_spider(self, spider):	# 爬虫结束时候执行
        print('close')
        self.session.close()
```

### Middleware中间件

可以直接在`middlewares.py`中进行定义

#### DownloadMiddleware下载中间件

所有的请求在`yield Request`的时候被加入队列，当调度器空闲的时候则取出来，然后以此被下载中间件进行处理(即`process_request`)，最后发起真正的请求。需要注意的是，`process_request`是每个中间件顺序执行的，但是`process_response`则是每个中间件倒序执行的。

```python
class MyMiddleware(object):
    process_request(self, request, spider):
        """
        重试的时候并不会进入这里面
        :return None: 返回None或者无返回，则会继续处理该请求，继续执行被接下来的中间件处理
        : 		Response: 返回Response，则会继续处理该请求，但是不会被其他中间件处理，相当于不请求了直接给一个响应
        		Request: 返回Request，则不会继续处理该请求，相当于新建了一个请求，重新来
        :raise IgnoreRequest: 将会调用process_exception
        """
        pass
    
    process_response(self, request, response, spider):
        """
        所有的有http状态码的响应都会到这里来
        :return Response: 将会继续往下执行
        		Request: 该链条会终端，重新来一个请求
        :raise IgnoreRequest: 
        """
        pass
    
    process_exception(self, exception, spider):
        """
        所有的没有http状态码的异常
        :return None: 将会继续处理
        		Response: 返回一个正常的Response
        		Request: 重新来一个请求
        """
        pass

```

### Signal信号

`scrapy`内部类似于事件触发的机制，通知某件事情发生了。

```python
engine_started()	# 当Scrapy引擎启动爬取时发送该信号
engine_stopped()	# 当Scrapy引擎停止时发送该信号
item_scraped()		# 当item被爬取，并通过所有Pipeline后(没有被丢弃(dropped)，发送该信号
item_dropped()
spider_closed()
spider_opened()
spider_idle(spider)	# spider处于空闲时候的信号
spider_error			
request_scheduled(request, spider)	# 当引擎调度一个Request对象用于下载时，该信号被发送
response_received(resopnse, request, spider)
response_downloaded(response, request, spider)
```

### 日志用法

日志有几种级别，默认是DEBUG，会打印所有的信息，可以在配置文件中进行配置，也可在抓取命令上指定

```python
# 日志打印，日志的几种级别，默认是DEBUG，抓取的时候可指定log级别，也可在配置文件中配置
CRITICAL: 严重错误(critical)
ERROR - 一般错误(regular errors)
WARNING - 警告信息(warning messages)
INFO - 一般信息(informational messages)
DEBUG - 调试信息(debugging messages)

# 如果在spider里面使用，可以直接
self.logger.critical('发生严重错误')

# 如果在其他地方，可以这样用
import logging
logger = logging.getLogger()
logger.warning("This is a warning")
```

###暂停与继续

`scrapy`提供了简单的方法以便于程序意外终止或者主动停止，仅需要在运行爬虫的时候添加参数，用于指定队列状态存储目录，`scrapy`会将序列化后的队列状态存储在该目录中

```shell
scrapy crawl somespider -s JOBDIR=crawls/somespider-1

# 如果想让某个url允许出现重复，那么可以给Request这个参数dont_filter。如果返回200，但是还是想重新请求，想让该url不会被filter掉，那么可以直接生成一个相同的request将dont_filter设置为True就行了
yield Request(url=url, dont_filter=True)
```

### Telnet

`scrapy`运行的时候会打开一个6023端口，用于实时查看爬虫当前的进度。直接`telnet 127.0.0.1 6023`即即可进入

```shell
# est()命令
time()-engine.start_time: 总的执行时间
len(engine.downloader.active): 正在下载的请求数量
len(engine.slot.inprogress): 当前处理进程数量
len(engine.slot.scheduler.mqs): 当前还在排队的请求数量，被yield以后就被放到这里面
len(engine.scraper.slot.queue): 
len(engine.scraper.slot.active): 当前等待处理的响应的书俩昂
engine.scraper.slot.active_size: 所有的响应总的大小
engine.scraper.slot.itemproc_size: 有多少个item等待被处理
engine.scraper.slot.needs_backout()
```

### 其他语法

```python
# 元素选择可使用xpath和css方式，但一般都用css方式方便直观点，比如
response.css('div.no-txt-box p.tit) # 获取符合条件的元素的列表	response.css('p.class::text)[0].extract()   # 获取p元素的内容

# 将item传递到下一级请求中去
yield Request(url, callback=..., meta={'item': item})
item = response.meta['item']

# 处理最开始的请求，生成初始url列表
def start_requests(self):
    """产生种子url"""
    for url in start_urls:
        yield Request(url, self.parse)
```

##TroubleShooting
- **安装出错`libffi`**

   ```shell
   No package 'libffi' found
   c/_cffi_backend.c:13:17: fatal error: ffi.h: No such file or directory
   #include <ffi.h>
   ```
     需要安装这个`sudo apt-get install libffi-dev`

- **ImportError: No module named twisted.internet或者No module named twisted**：
  执行`pip3 install twisted`，如果出现错误`No matching distribution found for Twisted`那么就是系统存在多个`python`版本导致找不到解压`twisted`包的库，这时候需要先安装`sudo apt-get install bzip2 libbz2-dev`，然后重新安装`python3`即可

- **无法捕获除200以外的错误**
  首先，像上面的配置文件中添加`HttpErrorMiddleware`中间件，然后在spider里面定义需要捕获哪些错误

  ```python
  class MySpider(CrawlSpider):
      handle_httpstatus_list = [404]
  ```

- **安装出错`no module named w3lib.http`**
   `pip install w3lib`

- 





    # 打印日志方法
    from scrapy import log
    log.msg("lalalala", level=log.INFO)

**暂停与继续**


    # 要使用暂停与继续功能，必须编写通用爬虫才能，也就是说Spider继承自CrawlSpider而不是BaseSpider，BaseSpider仅仅会抓取start_urls里面的

- **处理不同的item**


    # pipeline处理不同的items
    if isinstance(item, FeedItem)  # 这种判断方式感觉好鸡肋
    
    # 在pipeline中丢弃items不再处理


    raise DropItem("Duplicate item found.")

```python
# 指定需要捕获的html状态
handle_httpstatus_list = [404, 502]

# no module 
```

/tmp/xmlXPathInitipwvpamp.c:1:26: 错误：libxml/xpath.h：没有那个文件或目录

## User-Agent列表

上次爬一个代理网站发现返回521错误，排查了好久居然发现是User-Agent错误，可我明明之前也是选择了不同的User-Agent的呀，难道服务器会记录一个IP对应一个User-Agent.这里罗列一下常用的User-Agent。更全的列表可以参考[user-agent-list](https://raw.githubusercontent.com/basilboli/user-agent-list/master/user-agent-list.txt)

	'Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25',
	'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
	'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
	'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
	'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',
	'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML, like Gecko) Version/7.2.1.0 Safari/536.2+',
	'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
	'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
	    'Mozilla/5.0 
