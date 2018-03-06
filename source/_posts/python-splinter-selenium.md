---
title: "Python使用Splinter(Selenium)进行浏览器模拟测试"
date: 2016-08-10 19:56:39
updated: 2017-12-12 18:43:00
categories: python
---
每次看到selenium都觉得很牛，但是苦于文档(包括英文)太少，我到今天才真正完整地安装使用了一把。我不喜欢来一个项目就在自己电脑上搭一个运行环境，而是喜欢在docker或者虚拟机里进行操作，问题是docker或者虚拟机里并没有任何的可视化的浏览器，而Selenium又依赖于这些浏览器驱动，我是最讨厌安装驱动的，因为驱动这个东西电脑不同差距特别大，总是会出现各种问题。而在服务器上如何安装selenium或者splinter，这个过程在网上基本是找不到的，所以这里记录下自己的安装方法。

注：这里之所以要使用`splinter`，而不只使用`selenium`是因为`splinter`在`selenium`之上又封装了一层，使得接口更为简单。

## Linux install Splinter(Selenium)

首先，需要安装必要的python包`pip3 install splinter selenium xvfbwrapper`需要注意的是，splinter只有在使用浏览器的时候才需要安装selenium，如果仅仅是在flask或者django中进行测试是不需要的。

### 安装chromedriver

[ChromeDriver首页-WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/)，下载对应操作系统的最新的chromedriver

```shell
wget http://chromedriver.storage.googleapis.com/2.23/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin	# 添加到PATH即可

chromedriver	# 运行命令进行测试，没抛错则表示正确了
```

##### Docker版本Selenium

https://github.com/SeleniumHQ/docker-selenium

##### handless browser

https://zhuanlan.zhihu.com/p/26810049?utm_medium=social&utm_source=qq

### Linux Server(Raspberry Pi)安装浏览器

上面的方式是直接打开浏览器的方式，但是在Server上面没有界面，也就没有浏览器，这种情况就得安装单独的真对server的浏览器了。最先我想使用ChromeDriver，但是无论怎么折腾也安装不上，于是就用了Firefox，发现一篇很好的[教程](http://www.installationpage.com/selenium/how-to-run-selenium-headless-firefox-in-ubuntu/)。它这个版本被称作`Selenium headless firefox`。安装步骤如下:

```shell
# 添加repository，并安装firefox
sudo add-apt-repository ppa:mozillateam/firefox-stable
sudo apt-get update
sudo apt-get install firefox

# 安装Xvfb: 是用来虚拟X服务程序，实现X11显示的协议
sudo apt-get install xvfb
sudo Xvfb :10 -ac  # 10表示编号

# 设置环境变量
export DISPLAY=:10

# 就可以使用了
firefox
```

## 开始Splinter(Selenium)

### 无桌面环境

```python
from splinter import Browser
from xvfbwrapper import Xvfb
from selenium.webdriver.chrome.options import Options

# 由于是在server上运行chrome，所以必须用一些模拟器
vdisplay = Xvfb()
vdisplay.start()

# 这些设置都是必要的
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")

# 这里才是正式的使用了
browser = Browser('chrome', options=chrome_options, executable_path='/root/bin/chromedriver')
browser.visit('https://haofly.net')
print(browser.title)

browser.quit()
vdisplay.stop()
```

### 桌面环境

如果直接在本地有桌面环境的情况下进行测试那么，直接这样子:

```python
from splinter import Browser
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
browser = Browser('chrome', executable_path='/Users/haofly/share/chromedriver', user_agent='User-Agent设置', options=chrome_options)
browser.driver.set_window_size(1500, 900)	# 设置浏览器的size
browser.visit('https://wiki.haofly.net')
print(browser.title)
```

### Options选项

通过`chrome_options.add_argument('')`可以设置非常多的浏览器的参数

```she
disable-infobars	// 禁用网页上部的提示栏，比如2.28的webdriver开始会提示你Chrome正受到自动测试软件的控制，这个特性应该是chrome为了安全给加的
```

### 获取所有网络请求

很多时候访问一个页面，在该页面可能会同时访问其他的资源，例如js，css，甚至其他一些关键信息。这时候就要求我们能够获取中间的所有的请求，但是`selenium`是不带这个功能的，只能使用一些代理，例如：[browsermob-proxy](https://github.com/lightbody/browsermob-proxy)。其不需要安装，只需要下载`bin`包，然后在使用的时候指定路径即可。例如：

```python
from browsermobproxy import Server
server = Server("~/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))
browser = Browser('chrome', executable_path='~/share/chromedriver2.28', options=chrome_options)
browser.driver.set_window_size(1500, 900)	# 设置浏览器的size

proxy.new_har()
browser.visit('https://haofly.net')
print(proxy.har)		# 以json的形式打印出中间所有的网络请求
```

## 浏览器操作

```python
browser.windows	# 所有打开了的窗口
browser.windows[0]	# 第一个窗口
browser.windows.current 	# 当前窗口
browser.windows.current = browser.windows[2]	# 切换窗口
browser.window[0].close()	# 关闭窗口
browser.window[0].close_others()	# 关闭其他窗口
browser.window[0].is_current # 序号为零的窗口是否是当前的窗口
browser.window[0].next	# 下一个窗口
browser.window[0].prev	# 上一个窗口
```

## 页面操作

```python
browser.visit(url)	# 访问URL
browser.reload()	# 重新加载当前页
browser.back()		# 回退
browser.forward()	# 向前

browser.find_by_tag('h1').mouse_over()	# 鼠标移动到某个元素上
browser.find_by_tag('h1').mouse_out()	# 鼠标移开
browser.find_by_tag('h1').click()		# 鼠标点击事件
browser.find_ty_tag('h1').double_click()# 鼠标双击事件
browser.find_by_tag('h1').right_click()	# 鼠标右键点击

draggable = browser.find_by_tag('h1')		# 鼠标拖曳事件
target = browser.find_by_css('.container')
draggable.drag_and_drop(target)	

# 点击链接
browser.click_link_by_href('http://www.the_site.com/my_link')
browser.click_link_by_partial_href('my_link')
browser.click_link_by_text()
browser.click_link_by_partial_text('part of link text')
browser.click_link_by_id('link_id')

# 点击按钮
browser.find_by_name('send').first.click()
browser.find_link_by_text('my link').first.click()

# 表单填写
browser.fill('query', 'my name')
browser.attach_file('file', '/path/to/file/somefile.jpg')
browser.choose('some-radio', 'radio-value')
browser.check('check-name') # checkbox
browser.choose('name', 'value')	# radio
browser.uncheck('some-check')
browser.select('uf', 'rj')
```

## 数据获取

```python
browser.title	# 获取网页title
browser.html	# 获取网页内容
browser.url		# 获取网页url
browser.find_by_css('h1').first.value	# 获取元素值

browser.is_text_present('', wait_time=None)  # html里面是否存在某个字符串

# 查找css元素
browser.find_by_css('h1')
browser.find_by_xpath('//h1')
browser.find_by_tag('h1')
browser.find_by_name('name')
browser.find_by_text('Hello World!')[1]
browser.find_by_id('firstheader').last
browser.find_by_value('query').first

# 寻找网页链接
browser.find_link_by_text()
browser.find_link_by_partial_text()
browser.find_link_by_href()
browser.find_link_by_partial_href()

# 可以连续用的
browser.find_by_tag('div').first.find_by_name('name')
```

## TroubleShooting

- **Chrome driver crashes when opens a new tab**

  原因可能是服务器内存太低了，需要加大虚拟内存

- **selenium.common.exceptions.WebDriverException: Message: session not created exception**，将webdriver更新到最新版基本上能解决问题

##### 相关文章

[Getting Started with Headless Chrome](https://developers.google.com/web/updates/2017/04/headless-chrome?utm_campaign=CodeTengu&utm_medium=email&utm_source=CodeTengu_89)

[Setting up a Digital Ocean server for Selenium, Chrome, and Python](http://jonathansoma.com/lede/algorithms-2017/servers/setting-up/)