---
title: "Scrapy PySpider python爬虫"
date: 2016-08-07 11:02:20
updated: 2017-10-30 18:00:00
categories: python
---
# Scrapy & PySpider
目前Python爬虫最著名的有两大分支，一个是Scrapy，一个是PySpider，虽然Scrapy用的人更多，更成熟，但是PySpider新特性也十分多.  

两者主要的不同主要在以下几点：  

- Scrapy文档较多，PySpider相对较少，且其官方文档都没说清楚
- Scrapy已经抓取的链接存储在内存中，PySpider持久存储在数据库中
- Scrapy使用Pipeline，PySpider使用消息队列  
- Scrapy只是一个包，PySpider可以看成一个框架或一个service，PySpider占用的内存肯定高(没运行脚本的时候都有100多MB)
- Scrapy要抓取Js生成的页面，得辅助其它package，比如Splash，PySpider貌似也要依靠PhantomJS
- Scrapy没有UI，PySpider有WebUI  
- Scrapy不适用于简单的项目，因为总是会写得复杂，PySpider不适用于复杂的项目，因为写不简单
- 简洁性上我觉得两者都十分简洁

## Scrapy

新建项目，`scrapy startproject test`目录结构如下(mac里面没有把scrapy命令放到bin里面去，直接搜索命令所在地吧)：

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
### 常用命令
```shell
scrapy startproject test    # 创建项目
scrapy genspider haofly haofly.net # 新建爬虫
scrapy crawl haofly --output=output.json --loglevel=critical		# 开始某个爬虫，最好加上输出文件，这样会把抓取到的item保留在文件里，防止数据丢失
scrapy list				# 列出当前project所有的spider
scrapy bench			# 基准测试，测试当前硬件的情况下最大的抓取速度
scrapy check			# scrapy自身的单元测试，很多人都不建议用，很难用，而且没没什么作用
```

### 通用设置
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
    
    # 配置AutoThrottle插件
    AUTOTHROTTLE_ENABLED=True   # 是否开启自动限制频率，不开简直太恐怖了  
    AUTOTHROTTLE_START_DELAY=1  # 以秒为单位，默认为5  
    AUTOTHROTTLE_MAX_DELAY=10   # 默认为60  
    AUTOTHROTTLE_DEBUG=False
    
    CONCURRENT_REQUESTS=16   # 并发线程的数量
    CONCURRENT_ITEMS=100     # 同时处理的Items的最大值
    
    **COOKIES_ENABLED=False  # 是否开起cookie
    LOG_LEVEL='DEBUG'    # LOG级别，在下面介绍了log的几种级别
    REDIRECT_ENABLED=False # 进制重定向**
### 请求与响应

	response.body				# 获取响应的body
	response.body_as_unicode()	# 获取响应编码后的内容
	response.requests			# 获取相应的请求
	response.status				# 获取HTTP状态码
	response.url				# 获取请求的URL
	response.headers			# 获取请求头

### 处理Item

需要注意的是，在pipeline里面处理item的时候必须`return item`否则，其他的item会接受不到，而且会打印一个莫名其妙的`None`，终端也不会显示抓取到的item，也就不能讲item输出到文件了

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



### 其他语法

```python
# 元素选择可使用xpath和css方式，但一般都用css方式方便直观点，比如
response.css('div.no-txt-box p.tit) # 获取符合条件的元素的列表	response.css('p.class::text)[0].extract()   # 获取p元素的内容

# 将item传递到下一级请求中去
yield Request(url, callback=..., meta={'item': item})
item = response.meta['item']

# 处理最开始的请求
def start_requests(self):
    """产生种子url"""
    for url in start_urls:
        yield Request(url, self.parse)
```

## PySpider



##TroubleShooting
- **安装出错**：

   No package 'libffi' found
   	c/_cffi_backend.c:13:17: fatal error: ffi.h: No such file or directory
   	#include <ffi.h>
     需要安装这个`sudo apt-get install libffi-dev`

- **ImportError: No module named twisted.internet**：
  执行`pip3 install twisted`

- **无法捕获除200以外的错误**
  首先，像上面的配置文件中添加`HttpErrorMiddleware`中间件，然后在spider里面定义需要捕获哪些错误

  ```python
  class MySpider(CrawlSpider):
      handle_httpstatus_list = [404]
  ```

  ​

- ​




**日志  
**


    # 打印日志方法
    from scrapy import log
    log.msg("lalalala", level=log.INFO)

**暂停与继续**


    # 要使用暂停与继续功能，必须编写通用爬虫才能，也就是说Spider继承自CrawlSpider而不是BaseSpider，BaseSpider仅仅会抓取start_urls里面的

**TroubleShooting**


- no module named w3lib.http：pip install w3lib
- **处理不同的item**


    # pipeline处理不同的items
    if isinstance(item, FeedItem)  # 这种判断方式感觉好鸡肋
    
    # 在pipeline中丢弃items不再处理


    raise DropItem("Duplicate item found.")

    # 指定需要捕获的html状态
    handle_httpstatus_list = [404, 502]
    
    # no module 

/tmp/xmlXPathInitipwvpamp.c:1:26: 错误：libxml/xpath.h：没有那个文件或目录

## PySpider

元素选择

## User-Agent列表

上次爬一个代理网站发现返回521错误，排查了好久居然发现是User-Agent错误，可我明明之前也是选择了不同的User-Agent的呀，难道服务器会记录一个IP对应一个User-Agent.这里罗列一下常用的User-Agent：

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
