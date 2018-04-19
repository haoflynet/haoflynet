---
title: "Chrome扩展开发手册"
date: 2018-04-10 18:32:00
updated: 2018-04-16 17:56:00
categories: chrome
---

`chrome`浏览器插件的开发类似于小程序开发，仅仅作为一个兴趣爱好，想做一个自己需要的东西而已，没多大的难度，无非就是调用一些API而已。

### 目录结构

实例文件夹结构及内容见: []()

```shell
.
├── background.js			# 注册监听事件，可以在这里面声明遇到哪些域名才激活插件
├── images
│   ├── get_started128.png
│   ├── get_started16.png
│   ├── get_started32.png
│   └── get_started48.png
├── manifest.json			# 入口文件，定义了插件的基本信息。page_action定义了有哪些页面，default_popup表示点击后默认的弹出页
├── options.html
├── options.js
├── popup.html		# 默认的弹出页，就是一个完整的html，需要js脚本的话也许要单独引用。chrome强制要求js与html文件分开放
└── popup.js		# 该样例里面主要的业务逻辑就在这里面
```

### 调试技巧

在`扩展程序`管理界面，可以看到自己的插件，点击背景页即可看到自己插件在后台的调试面板。

如果要在后台打印日志，不能直接用`console.log()`而是应该用`    chrome.extension.getBackgroundPage().console.log()`代替。

如果想要调试`popup.js`的内容，光有上面的还不够，还得在插件图标上`右键`->`审查弹出的内容`，所以，基本上，得同时打开三个调试面板…不过popup的生命周期仅仅是弹出过后，如果重新点击图标，那么调试面板也需要重新去打开。

### API/权限列表

[官方API列表](https://developers.chrome.com/extensions/api_index)

[官方权限列表](https://developer.chrome.com/apps/declare_permissions)

常用功能:

| API名称                                    | 权限名称           | 描述                                                         |
| ------------------------------------------ | ------------------ | ------------------------------------------------------------ |
| alarms                                     | chrome.alarms API  | 通知                                                         |
| cookies                                    |                    | 操作cookie                                                   |
| tabs.executeScript/tabs.insertCSS/tabs.Tab | activeTab          | 使用户在调用扩展程序时(如单击浏览器按钮)能够访问当前活动的标签页。这样可以不用申明对哪些网站有持续的访问权限，而是用户点击的时候才有访问标签页的权限 |
| declarativeContent                         | declarativeContent | 根据网页URL和内容以及CSS来展示页面按钮，而不需要读取网页内容的权限。 |

## 常用功能实现

- **仅在指定域名激活插件图标**: 需要在`background.js`中进行如下设置

  ```javascript
  chrome.runtime.onInstalled.addListener(function() {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'haofly.net'},
        })],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
  ```

- ​

## TroubleShooting

- **发送http请求网站出现`Access-Control-Allow-Origin not checking in chrome extension`错误**
  原因是并没有向浏览器申请对该域名的访问权限，可以在`manifest.json`中的`permissions`添加该url，可以用正则，例如，如果要匹配所有的网址，啊呢吗`"*://*/*"`
- ​

参考文章:

[官网开发手册](https://developer.chrome.com/extensions/getstarted)

