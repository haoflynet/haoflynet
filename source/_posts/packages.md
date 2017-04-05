---
title: "Python包推荐,PHP包推荐,JS包推荐,Java包推荐"
date: 2016-08-07 11:03:30
updated: 2016-11-28 17:03:00
categories: system
---
# python包／jQuery／Java／PHP包收集与整理

### Python

如果要使用pip安装最新版本可以在后面加上版本号

##### [BeautifulSoup4](http://beautifulsoup.readthedocs.org/zh_CN/latest/)

XML/HTML解析组件

##### coverage

代码覆盖率检测工具

##### django.contrib.syndication.views

Django自带的输出feed的工具

##### [django.core.paginator](https://docs.djangoproject.com/en/1.8/topics/pagination)

这是Django自带的分页工具，非常实用

##### [django-avatar](http://www.jianshu.com/p/da3de42a96b5)

Django头像插件

[**django-extensions**](https://github.com/django-extensions/django-extensions)

Django的扩展包的包，带有非常方便的一些工具，比如自动打印sql语句等。

##### [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)

Django的调试工具集，包含了很多的调试及性能优化工具，应该非常好用，未使用过

##### [django-haystack](https://pypi.python.org/pypi/django-haystack/2.4.0)

Django的全文搜索功能

##### [django-redis](https://pypi.python.org/pypi/django-redis/4.0.0)

在Django中使用Redis必备。需要注意的是，它对value做了序列化，而且在key前面加入了版本号，类似_:1:key，_而且，默认生存时间是300秒，需要加入参数_cache.set(“key”, “value”, timeout=None)_。Redis密码的格式应该是 “LOCATION”: “redis://:密码内容@104.236.170.169:6379/1″,真的服了官网那不明不白的表述了

##### [**django-rest-framework**](http://www.django-rest-framework.org/)

Django的Restful框架

##### [**django-social-auth**](https://github.com/omab/django-social-auth)

Django社会化认证工具

##### [**django-socketio**](https://github.com/stephenmcd/django-socketio)

Django的WebSockets ，好爽

##### [django-wysiwyg](http://django-wysiwyg.readthedocs.org/en/latest/index.html)

Django使用wysiwyg作为富文本编辑器

[**dh-virtualenv**](https://github.com/spotify/dh-virtualenv)

Python部署工具，弃用pip，而是将package打包成`Debian packages`的形式，自动解决各种依赖问题

##### difflib

Python自带模块，比较文本之间的差异，且支持输出可读性强的HTML文档

[**dpart**](https://github.com/douban/dpark)

Spark的Python实现，分布式任务处理

##### [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)

计算字符串相似率

[hashids](https://github.com/hashids/hashids.github.io):

将整数转换为hash值，并且支持反解，这不仅仅是Pythond的一个库，而且支持几十种语言。可用于将后台生成的唯一ID转换成混淆的hash值。

[**httpstat**](https://github.com/reorx/httpstat):

在命令行打印CURL请求的详细信息

##### IPy

IP地址处理模块，可用于计算大量的IP地址，包括IPv4、IPv6网段、网络掩码、广播地址、子网数、IP类型等。[参考文章](http://www.ipython.me/python/python-ipy.html)

##### [jieba](https://pypi.python.org/pypi/jieba/0.36.2 "Link: https://pypi.python.org/pypi/jieba/0.36.2" )([官方文档](https://github.com/fxsjy/jieba))

结巴中文分词，未使用过

##### [lunardate](https://pypi.python.org/pypi/lunardate/0.1.5)

获取农历

##### [MkDocs](http://markdown-docs-zh.readthedocs.org/zh_CN/latest/)

项目文档工具，以markdown的方式攥写spinx烈性的文档

**[MoviePy](http://zulko.github.io/moviepy/getting_started/audioclips.html?highlight=audio)**：Python处理视频文件

[**MRQ**](https://github.com/pricingassistant/mrq): Python的分布式worker任务队列，使用Redis和gevent。既有RQ那样简单，又有Celery的性能。，具有强大的用户面板，可以控制队列中的任务、当前任务、workder的状态，并且能按任务区分日志。

[mysqlclient](https://github.com/PyMySQL/mysqlclient-python): Python3链接MySQL/Mariadb数据库的库，相比于官方的库以及众多其他第三方库，这个库虽然只有一个人在维护开发，但是Pypi的权重值有9，而且Github一直有更新。在安装的时候需要先安装依赖：`sudo apt-get install python-dev libmysqlclient-dev`，Python3要加3，windows下可以直接安装，如果是OS X，那么可能是没有将mysql添加到环境变量，在_.profile_做如下修改

```shell
PATH="/Library/Frameworks/Python.framework/Versions/3.5/bin:/usr/local/bin/python3:/usr/local/mysql/bin:${PATH}"
export PATH
DYLD_LIBRARY_PATH="/usr/local/mysql/lib/${DYLD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH  
```

##### [paramiko](https://pypi.python.org/pypi/paramiko/1.15.2)([官方文档](http://docs.paramiko.org/en/1.15/api/client.html#paramiko.client.SSHClient))

基于Python2/3实现的SSH2的库，支持认证及密钥方式，可以实现远程命令执行、文件传输、中间SSH代理等功能。windows安装的时候会有依赖问题，可见这个[issue](https://github.com/onyxfish/relay/issues/11)

##### pep8

PEP8规范检测工具，使用时直接`pep8 ./`

##### [Pillow](https://pillow.readthedocs.org/en/3.0.x/)

Python图像处理库，与PyLab互斥，只能安装一个哟

##### [progressBar2](http://progressbar-2.readthedocs.org/en/latest/index.html)

在终端显示进度条

##### [psutil](https://pypi.python.org/pypi/psutil)

跨平台的获取系统运行的进程和系统利用率(包括CPU、内存、磁盘、网络等)信息的库，主要用于系统监控，分析和限制系统资源及进程的管理。实现了一些命令行的工具(如：ps、top、lsof、netstat、ifconfig、who、df、kill、free、nice、ionice、iostat、iotop、uptime、pidof、tty、taskset、pmap等)

##### [pyspider](https://github.com/binux/pyspider)

有图形界面的爬虫程序

##### python-nmap

使用Python实现的端口扫描工具

##### [random-avatar](https://github.com/mozillazg/random-avatar)

直接生成指定大小的随机头像，是按照你的IP来计算的

##### [requests](https://pypi.python.org/pypi/requests/2.7.0)

([官方文档](http://cn.python-requests.org/zh_CN/latest/))，比SSL和HttpResponse更加高级，更方便，一句话就可以搞定人家几十句的功能，非常方便

[**SaltStack**]()

基于Python开发的一套C/S架构配置管理工具，底层使用ZeroMQ消息队列pub/sub方式通信，使用SSL整数签发的方式进行认证管理。而Ansible基于ssh协议传输数据，所以SaltStack普遍被认为比Puppet快，缺点是需要安装客户端。

##### [SciPy](http://sourceforge.net/projects/scipy/?source=typ_redirect)

Python科学计算库

[**stackoverflow**](https://github.com/drathier/stack-overflow-import)

直接通过关键字从stackoverflow上面抓去来作为一个工具函数，黑科技

##### [xpinyin](https://github.com/lxneng/xpinyin)

汉字拼音

### PHP

##### [config](https://github.com/hassankhan/config)

轻量级的配置文件读取工具，支持PHP/INI/XML/JSON/YAML文件

##### [guzzle](https://github.com/guzzle/guzzle)

比[requests](https://github.com/rmccue/Requests)更好用的请求库，已经放弃`requests`库了，更新很慢，无法上传文件，目测作者也已经放弃这个库了，已经没有回复PR了。。。

##### [jsonmapper](https://github.com/cweiske/jsonmapper)

自动将JSON对象转换为相应的类对象，相当于Java里面的bean

##### [PhpSms](https://github.com/toplan/phpsms)

可能是目前最聪明、优雅的php短信发送哭了。从此不再为各种原因造成的个别发送失败而烦忧。。。。

### Java

##### [retrofit](https://github.com/square/retrofit)

Java里面非常好用的HTTP client，用起来显得十分简洁，简化了HTTP请求























---|---  

Pandas：大数据处理工具，可将大文件分段读取

**[

/`

pexpect：相当于Linux下得expect，可以实现对ssh、ftp、passwd、telnet等命令进行自动交互。比如可以模拟一个FTP登录时的所有
交互，包括输入主机地址、用户名、密码、上传文件等等。





[

**[PyBrain](http://pybrain.org/)**：Python神经网络库

pyClamad：直接使用ClamAV病毒扫描守护进程clamd，来实现一个高效的病毒检测功能(ClamAV是一款免费而且开源的防毒软件，软件与病毒库的更新
皆由社区免费发布)

pycurl：支持的操作协议有FTP、HTTP、HTTPS、TELNET等



[**python-markdown2**](https://github.com/trentm/python-
markdown2)：Python解析markdown文件





# 如果出现以下错误：

/usr/local/lib/python2.7/dist-
packages/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A
true SSLContext object is not available. This prevents urllib3 from
configuring SSL appropriately and may cause certain SSL connections to fail.
For more information, see https://urllib3.readthedocs.org/en/latest/security.h
tml#insecureplatformwarning.

InsecurePlatformWarning

# 那么这样操作：

pip uninstall requests

pip \\--no-cache-dir install requests[security]

# 如果出现如下错误：

[APP SUBMITTED]: '_socketobject' object has no attribute
'set_tlsext_host_name'

# 那么这样操作：

apt-get purge python-openssl

apt-get install libffi-dev python-pip

pip2.7 install -U pyopenssl  

---|---  

rrdtool：rrdtoo是换装数据库的存储格式，round robin是一种处理定量数据以及当前元素指针的技术，rrdtool主要用来跟踪对象的变化情况
，生成这些变化的走势图，如业务的访问流量、系统性能、磁盘利用率等趋势图

**[

**[scrapy-splash](https://github.com/scrapinghub/scrapy-splash)**：Scrapy对于Splash的封装

**[Silly](http://mp.weixin.qq.com/s?__biz=MjM5NzU0MzU0Nw==&mid=2651370531&idx=1&sn=f7192f06e274c1cff24bab83a30b90dd&scene=23&srcid=06066k74UbShOJyQUZWBcp2H#rd)**: 测试用数据生成器

**[splash](https://github.com/scrapinghub/splash)**：用于获取经过Javascript处理后的html页面，十分有用，只需要将请求的url改为http://localhost:8050/render.html?url=' + url，即可向Splash服务器发送，并获取到js渲染过后的html页面

**suds**：Python仅作为客户端调用webservice

**[Tornado-MySQL](https://github.com/PyMySQL/Tornado-MySQL)**：MySQL对于Tornado的异步实现，支持线程池直接操作

# PHP

**[laravel-5-markdown-editor](**https://github.com/yccphp/laravel-5-markdown-editor**)**: Laravel5 Markdown编辑器

[**PHP Debug Bar**](https://github.com/maximebf/php-debugbar)：方便调试，可以直接在浏览器里面看到变量信息，而不用var_dump()了

**[Carbon](http://laravel5-book.kejyun.com/package/tool/package-tool-carbon.html)**: 各种时间处理

# jQuery/JS

**[Awesomplete](http://leaverou.github.io/awesomplete/#basic-usage "Link: http://leaverou.github.io/awesomplete/#basic-usage" )**：jQuery的联想次插件，必须异步加载哟，例如：

	<script type="text/javascript">
	$(function(){
		var input = document.getElementById("myinput");
		var awesomplete = new Awesomplete(input);
		awesomplete.list = ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE","Node.js" , "Ruby on Rails"];
	
	});
	</script>  

**[BootSideMenu](http://www.htmleaf.com/jQuery/Menu-Navigation/201505131825.html)**：Bootstrap隐藏滑动侧边栏jQuery插件，虽然不大好看，依赖还有点多，不过好用

**[bootstrap-select](https://silviomoreto.github.io/bootstrap-select/)**: 基于Bootstrap和jQuery的下拉选择输入列表插件

**[clipboard.js](https://github.com/zenorocha/clipboard.js)**：纯HTML5实现的复制到粘贴板的插件

**[DataTables](https://datatables.net/)**:表格插件，几乎涵盖了所有想要的功能，定制化非常强

**[editor](https://github.com/lepture/editor)**：一个十分漂亮的markdown编辑器

**[fingerprintjs](https://github.com/Valve/fingerprintjs)**: 浏览器唯一性解决方案

**[hotkeys](http://jslite.io/hotkeys/)**：无任何依赖的键盘事件捕获插件

[**jquery-notebook**](https://github.com/raphaelcruzeiro/jquery-
notebook?utm_source=next.36kr.com)：简洁的网页编辑器

**[simditor](https://github.com/mycolorway/simditor "Link: https://github.com/mycolorway/simditor" )**：采程设计的wysiwyg类型的编辑器

**[three.js](http://threejs.org/ "Link: http://threejs.org/" )**: 有太多酷炫的效果了

[**wysihtml**](https://github.com/Voog/wysihtml)：十分强大的网页编辑器，但是文档几乎没有，上面有Django
版本
