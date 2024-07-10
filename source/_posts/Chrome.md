---
title: "Chrome教程，谷歌浏览器插件推荐"
date: 2013-01-01 08:22:39
updated: 2022-10-10 15:59:00
categories: tools
---
作为一个谷歌的"中毒"用户，用五年的使用经验告诉大家，谷歌浏览器真的是世界上最好的浏览器。该有的插件都有，该有 的调试功能都有，开源的不开源的也都有。至于很多人吐槽谷歌的唯一缺点: 内存占用大的问题，当我切换到Mac上以后就不再关心这个问题了，因为在mac上，内存占用越大，基本上可以保证程序运行越快，谷歌有理由占用大内存。 用过这么多年的谷歌浏览器，已经向多人安利了它，使得他们纷纷放弃原来的浏览器，毕竟，每次他们问我问题的时候，我基本上用谷歌都能快速地调试出来。谷歌浏览器也一次又一次地让我有互联网的未来入口都在浏览器的错觉，直到后来，微信出现了。。。

<!--more-->

## 谷歌搜索技巧

- A AND B: and搜索，默认的空格都是这样
- A OR B: or搜索，可以用`|`
- A -B: 表示搜索A但是结果里不能有B
- *A: 通配符搜索
- `filetype:pdf 机器学习`：搜索指定类型的文件
- `site:v2ex.com 测试`：搜索指定网站
- `intitle: 测试`：仅搜索网页标题
- `inurl: test`：仅搜索url

## 谷歌插件推荐

- **Adblock Plus**：屏蔽广告插件，真的不是有意的，确实有些网站做得有点过分了，看一分钟视频得先看一分钟广告，有些网站不登陆还不准看，更有甚者看到一半给你插一段广告。。。

- **EditThisCookie**: 快速查看与编辑Cookie，web站点调试利器

- **JSON Editor**：JSON编辑器，可快速格式化Json字符串

- **JSONView**: 如果web内容是纯json字符串，那么会被自动格式化为友好的Json格式

- **LastPass**：值得信赖的保存和生成网站密码的插件，只要一个主密码，可以保存所有其它的密码，而且能记住你输入的密码，这样在新打开网页的时候可以直接选择，而且还有安全日记功能，可以保存其它一些重要的信息

- **Octotree**：可以在浏览Github的时候在左边显示目录树

- **OneTab**：不用在关闭的时候把打开的标签保存成书签了，一键把当前打开的所有网页变成稍后阅读

- [permission.site](https://permission.site/): 其实不算插件，但是其专门用于测试谷歌浏览器的各种权限，例如通知、相机、定位、蓝牙等

- **Postman**：谷歌上非常好用的调试工具，可以模拟各种GET和POST等操作，调试利器

- **Proxy SwitchyOmega**：谷歌上的代理软件，你懂的

- **Requestly**：重定向HTTP请求，不仅可以重定向到不同的host(很多情况改hosts就够了)，而且能够将一个url重定向到另外一个url，使得结果完全和另外一个url相同

- **Tampermonkey**: 油猴脚本，可以设定在适当的情况下在当前的网页执行某段js代码，例如自动登录、自动抢票等，简直太方便了

- **Text Mode**：将当前网页以黑白文本方式显示，不显示图片

- **Vimium**：用vim的方式浏览网页，炫酷，按下f键即可选择当前网页的链接

- **Vysor**：在PC端浏览手机，Mac无法使用

- **Wappalyzer**：可以查看当前浏览的网站所采用的框架，前端后端都能识别，比如bootstrap、wordpress等

- **惠惠购物助手**：在网购浏览商品的同时，自动对比其它优质电商同款商品价格，并提供商品价格历史，防止被坑

- **眼不见心不烦**：微博插件，屏蔽了一些神烦的东西

## 常用快捷键(Mac)

- Ctrl + F：查找网页内容
- Ctrl + N: 新打开标签页
- Ctro + w: 关闭当前标签页
- ⌘-Option-U: 查看网页源代码
- `Ctrl+P`: `Sources`源代码查看窗口快速定位
- `Alt+Click`: `Elements`html窗口快速展开DOM

## 奇淫技巧

### [远程调试安卓android设备网页](http://www.ruanyifeng.com/blog/2019/06/android-remote-debugging.html)

- 如果调试页面出现404，那么可能需要梯子

### 自带的长截图功能

按F12进入控制台，然后按`ctrl+shift+p`弹出控制台的输入框，再输入`capture full size screenshot`即可实现长截图功能，可以卸载截图插件了

### 调试的时候保留浏览器请求

![调试的时候保留浏览器请求](https://haofly.net/uploads/chrome_0.jpg)

### 直接复制请求的cURL

cURL能做到一切你想要的，有了cURL就可以方便地写爬虫代码了
​      ![从Chrome复制cURL](https://haofly.net/uploads/chrome-1.jpg)

### 直接在搜索框使用多个搜索引擎

众所周知，Chrome顶部最方便的搜索框只能有一个默认的搜索引擎，就是谷歌自带的，但是如果你要查找什么无聊的东西需要用到百度，这里有个比直接到百度网站更方便的方法:  Chrome设置->搜索->管理搜索引擎，这里可以设置默认的搜索引擎也可以增加其他的搜索引擎，例如我这里的设置，g表示用google搜索，b表示用百度搜索:
​      ![Chrome设置搜索引擎](https://haofly.net/uploads/chrome_3.jpg)


这样如果我想在顶部搜索框直接使用百度搜索就可以这样:
![谷歌浏览器里面使用百度搜索](https://haofly.net/uploads/chrome_2.jpg)

### 禁止加载某些文件

`Network`上面对着请求右键`Block request URL`或者`Block request domain`

### 每次打开新标签页自动打开调试工具

需要在`chrome`启动的时候带上`--auto-open-devtools-for-tabs`参数，mac上面使用如下

```shell
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --auto-open-devtools-for-tabs
```

### 调试元素的鼠标点击等事件:active/focus/hover/visited

在审查元素，选择元素后的右上角点击`:hov`，即可选择指定的事件

### 验证网站的传输协议(HTTP2.0等)

![](https://haofly.net/uploads/chrome_4.png)

### 调试响应式页面时增加设备

- 默认的经常用到的只有iPhone X和iPad，如果想自己增加可以这样做，在调试响应式式点击设备列表最下面`Edit`，然后`Add custom device`
- 这里有另外几种常见设备分辨率

| Device Name       | Width | Height | DPR  |
| ----------------- | ----- | ------ | ---- |
| iPhone 11         | 414   | 896    | 2    |
| iPhone 11 Pro     | 375   | 812    | 3    |
| iPhone 11 Pro Max | 414   | 896    | 3    |
| iPhone XR         | 414   | 896    | 2    |
| iPhone Xs         | 375   | 812    | 3    |
| iPhone Xs Max     | 414   | 896    | 3    |
| iPad Mini 4       | 768   | 1024   | 2    |

### 原生实时字幕

- [Use Live Caption in Chrome](https://support.google.com/chrome/answer/10538231?hl=en)

## 高端操作

#### chrome://flags

- 浏览器一些常量设置
- **allow-insecure-localhost**: 表示是否将本地https标记为安全
- **unsafely-treat-insecure-origin-as-secure**: 将不安全的http标记为安全，需要将对应的http地址填入才行，能够解决http页面无法获取某些浏览器权限的问题，添加完了需要available才行

#### chrome://net-internals

查看浏览器的网络相关设置，例如Proxy，DNS、Sockets、HTTPS证书等，在这里可以查看谷歌加载的nameservers，以及域名解析的缓存，可以在这里清除host缓存、清楚HTTPS缓存(Delete domain security policies)。

#### chrome://webrtc-internals

查看webrtc/socket/udp等的流量

## 浏览器管理

-   chrome://dns/ ：显示DNS状态
-   chrome://cache/：查看缓存状态
-   chrome://flags/#enable-tab-audio-muting: 设置是否开启网页标签的静音功能，这样可以针对单独的标签设置静音
-   chrome://memory-redirect/ ：查看内存信息


## TroubleShooting
- **谷歌浏览器提示输入密钥环**: 其实在装完系统第一次打开谷歌浏览器的时候会提示设置密码的，只是当时我们不知道是什么密码，就把管理员密码输进去了，导致每次打开浏览器都得再输入一次。
  方法一：取消开机自动登录 
  方法二：在终端输入seahorse(如果未安装就安装)，打开该软件后，点击菜单栏的视图——根据密钥环——默认密钥点右键，然后把该密码设置为空。seahorse是一个GNOME程序，用于管理加密密钥，主要功能有创建和管理PGP keys、SSH keys，在密钥服务器发布及获取密钥，缓存密钥密码(这个功能使得我们在使用浏览器登陆某些网站时不用每次都输入密码)、备份密钥及密钥环
- **Network里面有请求出现`block content mixed`**: 原因是当前域名既有https又有http，自己处理吧。

**扩展阅读**

[Chrome 开发者工具的性能选项卡使用教程（译文）](https://juejin.im/post/5efb78945188252e99702b8e)