---
title: "[转]RESTful API设计指南"
date: 2015-04-11 23:24:07
updated: 2019-12-13 16:02:00
categories: 编程之路
---
原文地址：[阮一峰的网络日志](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)

网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备......）。

因此，必须有一种统一的机制，方便不同的前端设备与后端进行通信。这导致API构架的流行，甚至出现"[API First](http://x.vindicosuite.com/click/fbfpc=1;v=5;m=3;l=401071;c=776283;b=3368032;dct=http\%3A//www.google.com.hk/search\%3Fq\%3DAPI+first)"的设计思想。[RESTful API](http://en.wikipedia.org/wiki/Representational_state_transfer)是目前比较成熟的一套互联网应用程序的API设计理论。我以前写过一篇[《理解RESTful架构》](http://www.ruanyifeng.com/blog/2011/09/restful.html)，探讨如何理解这个概念。

今天，我将介绍RESTfulAPI的设计细节，探讨如何设计一套合理、好用的API。我的主要参考了两篇文章（[1](http://codeplanet.io/principles-good-restful-api-design/)，[2](https://bourgeois.me/rest/)）。

# 一、协议

API与用户的通信协议，总是使用[HTTPs协议](http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html)

# 二、域名

应该尽量将API部署在专用域名之下。

```
https://api.example.com
```

如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下。

```
https://example.org/api/
```

#  三、版本（Versioning）

应该将API的版本号放入URL。

```
https://api.example.com/v1/
```

另一种做法是，将版本号放在HTTP头信息中，但不如放入URL方便和直观。[Github](https://developer.github.com/v3/media/#request-specific-version)采用这种做法。

# 四、路径（Endpoint）

路径又称"终点"（endpoint），表示API的具体网址。

在RESTful架构中，每个网址代表一种资源（resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合"（collection），所以API中的名词也应该使用复数。

举例来说，有一个API提供动物园（zoo）的信息，还包括各种动物和雇员的信息，则它的路径应该设计成下面这样。

* <https://api.example.com/v1/zoos>
* <https://api.example.com/v1/animals>
    * <https://api.example.com/v1/employees>

# 五、HTTP动词

对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

* GET（SELECT）：从服务器取出资源（一项或多项）。
* POST（CREATE）：在服务器新建一个资源。
    * PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
    * PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
    * DELETE（DELETE）：从服务器删除资源。
      还有两个不常用的HTTP动词。

    * HEAD：获取资源的元数据。
    * OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。
      下面是一些例子。

    * GET /zoos：列出所有动物园
    * POST /zoos：新建一个动物园
    * GET /zoos/ID：获取某个指定动物园的信息
    * PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
    * PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
    * DELETE /zoos/ID：删除某个动物园
    * GET /zoos/ID/animals：列出某个指定动物园的所有动物
    * DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物

# 六、过滤信息（Filltering）

如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。

下面是一些常见的参数。

* ?limit=10：指定返回记录的数量
* ?offset=10：指定返回记录的开始位置。
    * ?page=2&per_page=100：指定第几页，以及每页的记录数。
    * ?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
    * ?animal_type_id=1：指定筛选条件
      参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /zoo/ID/animals 与 GET
      /animals?zoo_id=ID 的含义是相同的。

# 七、状态码(Status Codes)

服务器向用户返回的状态码和提示信息，常见的有以下一些（方括号中是该状态码对应的HTTP动词）。

* 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
* 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
* 202 Accepted - [_]：表示一个请求已经进入后台排队（异步任务）
* 204 NO CONTENT - [DELETE]：用户删除数据成功。
* 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
* 401 Unauthorized - [_]：表示用户没有权限（令牌、用户名、密码错误）。
* 403 Forbidden - [_] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
* 404 NOT FOUND - [_]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
* 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
* 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
* 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
* 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
    状态码的完全列表参见[这里](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)。

# 八、错误处理（Error handling）

如果状态码是4xx，就应该向用户返回出错信息。一般来说，返回的信息中将error作为键名，出错信息作为键值即可。

```
{
	error: "Invalid API key"
}
```

# 九、返回结果

针对不同操作，服务器向用户返回的结果应该符合以下规范。

* GET /collection：返回资源对象的列表（数组）
* GET /collection/resource：返回单个资源对象
    * POST /collection：返回新生成的资源对象
    * PUT /collection/resource：返回完整的资源对象
    * PATCH /collection/resource：返回完整的资源对象
    * DELETE /collection/resource：返回一个空文档

# 十、Hypermedia API

RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。

比如，当用户向api.example.com的根目录发出请求，会得到这样一个文档。

```json
{
  	"link": {
      "rel": "collection https://www.example.com/zoos",
      "href": "https://api.example.com/zoos",
      "title": "List of zoos",
      "type": "application/vnd.yourformat+json"
	}
}
```

上面代码表示，文档中有一个link属性，用户读取这个属性就知道下一步该调用什么API了。rel表示这个API与当前网址的关系（collection关系，并给出该collection的网址），href表示API的路径，title表示API的标题，type表示返回类型。

Hypermedia API的设计被称为[HATEOAS](http://en.wikipedia.org/wiki/HATEOAS)。Github的API就是这种设计，访问[api.github.com](https://api.github.com/)会得到一个所有可用API的网址列表。

```
{
"current_user_url": "https://api.github.com/user",
"authorizations_url": "https://api.github.com/authorizations",
// ...
}
```

从上面可以看到，如果想获取当前用户的信息，应该去访问[api.github.com/user](https://api.github.com/user)，然后就得到了下面结果。

```
{
"message": "Requires authentication",
"documentation_url": "https://developer.github.com/v3"
}
```

上面代码表示，服务器给出了提示信息，以及文档的网址。

# 十一、其他

（1）API的身份认证应该使用[OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)框架。

（2）服务器返回的数据格式，应该尽量使用JSON，避免使用XML。

（完）

## 扩展阅读

[RESETful API 设计规范](https://segmentfault.com/a/1190000015384373)

[微软的Rest API设计指南](https://github.com/microsoft/api-guidelines/blob/master/Guidelines.md)

## 个人总结

- RESTful设计风格是仅仅针对API的设计，其他的，比如新建功能页面的url还是需要自己另外定义的，当然可以在后面直接加参数，比如`GET /zoos?add=1`

- 对于文件的上传，无法使用`application/json`，而只能使用`Multipart/form-data`的方式

- 如果我们要是用名称而不是ID来作为url的关键字，那么可能出现关键字与url重复的问题，例如`/users/:username/cars`与`/users/cars`，这个例子不是很恰当，但是已经可以看出问题了，前者表示某个用户所拥有的车，后者表示属于所有人的车，但是如果有个人的名字就叫`cars`呢，就会出现设计上的错误。为了规避这种情况，最好的办法就是提取出几个关键字，应该尽量少，例如github就不能注册名为`teams`的账号，注册时就会提示这是一个保留字。这只是大多数情况，少数情况，资源并不完全属于我们，我们无法确定资源是否会占用保留字，那么这时候就只能添加特殊字符了，例如`$`，另外一个做法是使用下划线，例如`/users/_regist`

- 有些人喜欢所有的接口的http状态码全部返回`200`，然后从返回的Json数据里面判断请求是否正常，理由却是统一管理返回数据格式，前端更好判断。我的理解是，这样完全不符合restful的设计规范。首先，永远无法保证请求永远返回200，所以，前端反而会多写一些判断；另外，如果按照请求错误的不同返回不同的http状态码，也是一种规范，因为http状态码对应的错误原因本身就是统一的；还有一点，对于日志监控来说，比如ELK这种自动分析日志的工具，当然是返回http状态码更好一点。

  这里还有另外一种将错误信息具体化的方法，就是在`HTTP_CODE`外，添加一个错误码头进行返回，例如`HTTP_CODE=403`时`X-status=4031`可以表示用户密码错误等具体错误信息。另外`HTTP_CODE`其实是支持用小数进行扩展的，例如`403`表示禁止访问，那么`403.1`可以表示禁止可执行访问，`403.2`表示禁止读访问

