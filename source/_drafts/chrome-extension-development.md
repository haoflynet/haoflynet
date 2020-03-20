---
title: "Chrome扩展开发手册"
date: 2018-04-10 18:32:00
updated: 2020-03-20 15:02:00
categories: chrome
---

`chrome`浏览器插件的开发类似于小程序开发，仅仅作为一个兴趣爱好，想做一个自己需要的东西而已，没多大的难度，无非就是调用一些API而已。

### 目录结构

实例文件夹结构及内容见:

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
├── popup.html		# 默认的弹出页，就是一个完整的html，需要js脚本的话也需要单独引用。chrome强制要求js与html文件分开放
└── popup.js		# 主要的业务逻辑就在这里面
```

#### manifest.json 详细配置

```javascript
{
  "name": "插件名称",
  "version": "0.1",	// 插件版本
  "description": "插件描述",
  "default_locale": "zh_CN",
  "permissions": [
    "activeTab",	// 使扩展程序在用户调用扩展程序的时候能够临时访问当前活动的标签页，可以代替<all_urls>，在安装过程中不显示警告信息
    "contentMenus",	// 右键菜单
    "declarativeContent", 	
    "notifications",	// 通知
    "storage",	// 本地存储
    "tabs",	// 标签
    "webRequest", // web请求
    "https://*.taobao.com/*", 	// 定义插件能访问哪些域名
    "https://*.tmall.com/*"
  ],
  "options_page": "options.html",
  "background": {		// 注册事件页面
    "scripts": ["background.js"],
    // "page": "background.html",	// 要么是scripts要么是page，如果是js，那么会自动生成一个背景页
    "persistent": false
  },
  // browser_action(浏览器按钮)、page_action(页面按钮)、app(单独的APP)三选一表示浏览器右上角图标的设置
  "page_action": {	// 当某些特定页面打开时才显示图标，否则是灰色
    "default_popup": "popup.html",	// 当用户点击扩展程序图标时弹出的页面
    "default_title": "",
    "default_icon": {
      "16": "images/get_started16.png",
      "32": "images/get_started32.png",
      "48": "images/get_started48.png",
      "128": "images/get_started128.png"
    }
  },
  "browser_action": {
    "default_icon": "img/icon.png",
    "default_title": "图标悬停时的标题",
    "default_popup": "popup.html"
  }
  "icons": {
    "16": "images/get_started16.png",
    "32": "images/get_started32.png",
    "48": "images/get_started48.png",
    "128": "images/get_started128.png"
  },
  "content_scripts": [{	// 定义需要直接注入页面的JS，不会出现在插件的审查弹出内容中，而是直接出现在浏览器当前页面里面，相当于一个附加在后面的js文件
    "matches": ["http//*/*"],
    "js": ["js/query-1.8.3.js", "js/mine.js", "content.js"],
    "css": ["css/custom.css"],
    "run_at": "document_start", // 执行时机，可选document_start, document_end,documen_idle(默认值表示页面空闲时)
  }],
  "homepage_url": "https://haofly.net",	// 插件主页
  "chrome_url_overrides": {	// 覆盖浏览器默认页面
    "newtab": "my_newtab.html",	// 用自己的页面替换新标签页
  }
  "manifest_version": 2
}

```

### 调试技巧

在`扩展程序`管理界面，可以看到自己的插件，点击背景页即可看到自己插件在后台的调试面板。

如果要在后台打印日志，不能直接用`console.log()`而是应该用`    chrome.extension.getBackgroundPage().console.log()`代替。

如果想要调试`popup.js/popup.html`的内容，光有上面的还不够，还得在插件图标上`右键`->`审查弹出的内容`，所以，基本上，得同时打开三个调试面板…不过popup的生命周期仅仅是弹出过后，如果重新点击图标，那么调试面板也需要重新去打开。

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

#### 仅在指定域名激活插件图标

需要在`background.js`中进行如下设置

```javascript
chrome.runtime.onInstalled.addListener(function() {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
          	pageUrl: {hostEquals: 'haofly.net'},
      	  }),
          // 可以直接在这里添加多个
          new chrome.declarativeContent.PageStateMatcher({
          	pageUrl: {hostEquals: 'haofly1.net'},
      	  }),
        ],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
```

#### popup.js与content.js通信

```javascript
// popup.js发送消息
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('my_tag').addEventListener('click', function () {
    console.log('点击特定元素，发送消息给content.js，触发其中的函数');
    
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
            console.log(response.farewell);
        });
    });
 });
});

// content.js直接接收消息
chrome.runtime.onMessage.addListener(msgObj => {	// 这里的msgObj即是发送的对象{greeting: "hello"}
    console.log(msgObj);
});

// content.js接收消息并返回结果
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting == "hello")
      sendResponse({farewell: "goodbye"});
});
```

## TroubleShooting

- **发送http请求网站出现`Access-Control-Allow-Origin not checking in chrome extension`错误**
  原因是并没有向浏览器申请对该域名的访问权限，可以在`manifest.json`中的`permissions`添加该url，可以用正则，例如，如果要匹配所有的网址，啊呢吗`"*://*/*"`
  
- **无法在popup.html中给元素添加onclick属性**: 这是Chrome的限制，可以在`popup.js`中手动给元素添加事件:

  ```javascript
  document.addEventListener('DOMContentLoaded', function() {
      var link = document.getElementById('my_link');
      link.addEventListener('click', function() {
          console.log("that's it");
      });
  });
  ```

  

参考文章:

[官网开发手册](https://developer.chrome.com/extensions/getstarted)

