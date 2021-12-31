---
title: "Postman 高级用法"
date: 2018-09-09 20:32:00
updated: 2021-12-06 18:40:00
categories: tools
---

Postman，一款功能强大的HTTP调试软件(以前只是谷歌浏览器的插件，现在已经独立成软件)，最近接触到它的一些高级用法，才发现它原来并没有我想象中那么简单，还有很多的高级用法。其主要有如下功能:

- HTTP/API调试
- 测试API接口
- 生成API接口文档
- 监控API接口
- mock接口数据

下面列举一些常用的功能使用方法。

<!--more-->

## 主要功能

### 接口直接转换为代码

![接口转换为代码](https://haofly.net/uploads/postman_0.png)

点击上图中的`Code`，可以选择导出成HTTP、C(LibCurl)、cURL、C#(RestSharp)、Go、Java、JavaScript、NodeJS、Objective-C、Ocaml、PHP、Python、Ruby、Shell、Swift等多种语言的代码实现。

### 路由变量Path Variables

- 只需要在url上面这样定义`/test/:id`，在Params下面会自动出现`Path Variables`的，可以设置值以及注释

### 环境变量

点击第一张图片中`No Environment`右边的`设置按钮`可以添加环境变量。同一个接口在不同的环境下，可以设置不同的变量值，比如域名和IP，这个功能能让我们一键切换所需的环境变量。设置环境变量界面如下:

![](https://haofly.net/uploads/postman_1.png)



### Pre-request Script

- 如果需要加解密或者计算hash值等，可以直接在这里面使用`CryptoJS`
- 这里一般可以添加自定义的认证方式

个性化的请求前执行的脚本，可以在这里定义一些变量的获取方式，例如如果要传入一个时间戳字段，可以在这里进行获取，并传入请求，例如:

```javascript
body = pm.request.body	// 获取请求体
timestamp = (Date.parse(new Date()) / 1000).toString();
body = {
    query: pm.request.body.graphql.query
}
sign = CryptoJS.HmacSHA1(timestamp + JSON.stringify(body), pm.environment.get("auth_sk")).toString(CryptoJS.enc.Hex);

pm.environment.set("timestamp", timestamp);
pm.environment.set("auth_sign", sign);
```

#### 在json请求体中写注释

```javascript
// 需要在Pre-request Script中这样写，去除掉注释
if (pm?.request?.body?.options?.raw?.language === 'json') {
    const rawData = pm.request.body.toString();
    const strippedData = rawData.replace(
        /\\"|"(?:\\"|[^"])*"|(\/\/.*|\/\*[\s\S]*?\*\/)/g,
        (m, g) => g ? "" : m
    );
    pm.request.body.update(JSON.stringify(JSON.parse(strippedData)));
}

// 这样就能在json请求体重写注释了
{
  "username": "abc" // required，这里的注释在请求的时候会自动去除掉
}
```

### Tests(相当于after request)

#### 请求完成后自动获取并设置token

```javascript
// 常用于登录注册接口，登录完成后，从response中获取token，并设置到变量中去
var jsonData = JSON.parse(responseBody);

pm.environment.set("REQUEST_TOKEN", jsonData.result.request_token);
pm.environment.set("USER_ID", jsonData.result.user_id);
```

### 自动进行认证

`Postman`自带了多种认证方式，可以让你在请求前自动去进行认证。另外，如果自带的几种认证方式无法满足，可以编写`Pre-request Script`来进行个性化的脚本。

![](https://haofly.net/uploads/postman_6.png)

### 请求示例

点击第一张图片里面的`examples(0)`可以添加请求示例，在这里可以添加请求的请求值与返回值的样例。可以给同一个接口添加多个示例。

### 添加cookie

点击第一张图片里面的`cookies`可以设置指定域名的cookies，一般是从网页上面直接拿下来的，例如如果该接口需要用户登录，但是又不想在`postman`里面写一遍用户登录接口，那么可以在网页上面直接将cookie复制下来即可。

### API Collections备注

在左侧的collections上面点击小箭头即可进入API collections的详情页面，在这里可以直接修改API集合的`Documentation`文档：

![](https://haofly.net/uploads/postman_2.png)

### 测试

基于js的测试工具，在`Tests`标签页预置了多个测试用的代码片段`SNIPPETS`

![](https://haofly.net/uploads/postman_7.png)

#### Monitor定时自动监控接口

postman提供`monitor`功能能够自动监控您的接口或者网页，并且可以直接将结果发送到你的注册邮箱。能够代替某些网站的监控功能了。

![](https://haofly.net/uploads/postman_11.png)
首先，在上面点击`Add a monitor`，然后进行设置保存即可:
![](https://haofly.net/uploads/postman_10.png)


#### 测试整个Collections

在`Collections`的小箭头上面的`Run`能运行整个`Collections`中所有的测试，在这里可以选择运行测试需要的环境变量等：

![](https://haofly.net/uploads/postman_8.png)

![](https://haofly.net/uploads/postman_9.png)



## 奇淫技巧

### 直接粘贴json格式的headers头

需要注意，复制的时候前后一定不能有多余的空格，例如，复制`{"a": "b", "b": 2333}`，那么在`Headers`标签中的第一个key处直接`Ctrl + V`粘贴即可直接格式化

![](https://haofly.net/uploads/postman_3.png)

### 直接URLEncode和URLDecode

![](https://haofly.net/uploads/postman_4.png)

### 在path中定义变量

用冒号表示，下面的`Params`会自动添加

![](https://haofly.net/uploads/postman_5.png)

### 发送数组参数

`key`可以这样写`field[]`多个`field[]`即表示数组了