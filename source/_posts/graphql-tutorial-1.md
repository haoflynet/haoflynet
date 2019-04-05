---
title: "GraphQL 教程（一）——What’s GraphQL"
date: 2019-01-20 21:52:00
updated: 2019-04-05 22:00:00
categories: graphql
---

> GraphQL exists because JavaScript developers finally realized HTTP API’s were too limiting so they reinvented SQL over JSON because JavaScript developers are obsessed with reinventing everything into JSON API’s。	——@kellabyte
>
> GraphQL 的本质是程序员想对JSON使用SQL。	—— 来自阮一峰的翻译

上面这句话是我见过的对GraphQL的存在最精妙的解释了。

维基百科上的简介是：GraphQL是一个开源的数据查询和操作语言及实现为了实现上述操作的相应运行环境。GraphQL诞生于2012年，之后则是由其创造者Facebook在内部使用。自它被发明以后，一直在默默无闻的改进中，直到2017年，Github[正式发布](https://blog.github.com/2017-05-22-introducing-github-marketplace-and-more-tools-to-customize-your-workflow/)了它[V4版本的API](https://developer.github.com/v4/)(V3版本的规范就是我们熟知的Restful API)，这才让GraphQL走入了包括我在内的大多数程序员的视野，并一度成为开发者讨论的热点。

<!--more-->

几年时间过去了，GraphQL并没有和一些人预期那样完全替代Restful，当然这也并不是它的目标，只是少部分人人的一厢情愿罢了。它的目标是给接口调用者特别是前端程序员提供一个弥补了Restful很多缺点的接口规范。

下面是一个非常直观的例子：

![](https://haofly.net/uploads/graphql-tutorial-1_01.png)

这个简单的需求要是给Restful API做，就是`GET /articles?name=GraphQL`，而得到的结果是`article`所有的属性，假设有10个属性，那就相当于返回的数据中仅有十分之一是我们想要的，剩下的都是无用的网络传输。不多不少，只获取你想要的，并且可以在一次请求中同时取出想关联的数据。

看到这儿，前端开发者们应该要笑cry了，终于不用再在列表页面去请求N次关联数据了，一次性把想要的都取出来，而且也不会有多余的东西。没错，这个东西确实更适合前后端分离的地方，移动端更甚。一方面，前端程序员不用看太多的接口文档，另一方面，也确确实实减少了网络请求量。

还记得我们用的Restful API不，说说我们项目当初为什么选择了它:

1. 统一的操作方法，能通过HTTP动词非常明确地看出当前是在执行什么操作，例如POST表示创建、PUT表示更新、GET表示获取资源、DELETE表示删除资源。不用去自己定义语义化的url命名规范了。放在以前，一个创建文章的请求可能是这样`POST /articles/add`也可能是这样`POST /articles/store`或者是这样`POST /articles/create`，Restful API则统一成这样`POST /articles`。
2. 以资源为对象，能通过url一目了然地知道当前操作的对象。`/articles`肯定在操作`article`，`/articles/123/comments`肯定是在操作id为123的`article`下面的`comments`。
3. 基于传统HTTP协议，学习成本很低，兼容性很高。

但是，经过长期的实践，我们也发现Restful API暴露了很多的问题：

1. 灵活性差。同一个接口必须尽可能多的返回字段以满足不同客户端的需求，否则就得将一个接口拆分出很多返回不同字段的不同的接口，服务端的代码量接口量增加，客户端的请求量同步增加。这一点随着时间的发展、业务复杂性的提高而越发明显。
2. 资源无法嵌套获取。如果要获取一个资源相关联的另一个资源，在大多数情况下，至少得调用两次接口才能完整获取到两个资源的数据，同第一点，不得不获取到两个资源的完整数据，大多数不是我们想要的。
3. 文档维护困难。每次修改接口都得去重新编写或者生成文档。
4. 无状态。所有资源通过URI定位，且这个定位与其他资源无关。
5. 仅支持HTTP协议。

在这里我首先要坦白说，GraphQL不能解决Restful API的所有问题(不然也早就取代它了)，但是它的这些特性或许是你早就想要的：

1. 统一入口，可以用一个url搞定所有的请求，一般直接`POST /graphql?query=`。
2. 规范统一。后端定义了统一的规范化的`schema`，客户端根据`schema`的数据结构来获取和修改数据(并且客户端能通过简单的一个web页面获取到所有`schema`的结构)。无需再为维护文档而费心。
3. 强类型。`schema`定义了数据的类型，服务端、客户端都必须遵循。
4. 高度自由化。客户端能根据需要获取自己想要的数据，不多不少，刚刚好。
5. 减少网络间数据传输，非常适合移动端调用。
6. 与传输层、存储层均无关，因为它本身只是一种查询语言。

推荐在新的面向前端的项目中使用`GraphQL`，如果是已经存在复杂业务逻辑的Rest接口，同样可以在前面封装一个数据处理层。



扩展阅读

英文官网：<https://graphql.org/>

中文官网：http://graphql.cn/

免费书籍：[The Road to GraphQL](https://www.robinwieruch.de/the-road-to-graphql-book/)



[GraphQL 教程demo地址](https://github.com/haoflynet/graphql-tutorial)
[GraphQL 教程（一）——What’s GraphQL](https://haofly.net/graphql-tutorial-1/)
[GraphQL 教程（二）—— GraphQL 生态](https://haofly.net/graphql-tutorial-2/)
[GraphQL 教程（三）—— GraphQL 原理](https://haofly.net/graphql-tutorial-3/)
[GraphQL 教程（四）—— Python Demo搭建](https://haofly.net/graphql-tutorial-4/)
[GraphQL 教程（五）—— 增删改查语法及类型系统](https://haofly.net/graphql-tutorial-5/)
[GraphQL 教程（六）—— N+1问题和缓存等问题](https://haofly.net/graphql-tutorial-6/)