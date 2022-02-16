---
title: "GraphQL 教程（二）—— GraphQL 生态"
date: 2019-03-18 21:52:00
updated: 2019-04-05 22:43:00
categories: graphql
---

GraphQL发展至今，已有Github、Facebook、Airbnb等大厂在大量地使用，大厂在使用的过程中，不断地进行技术沉淀，也诞生了许多实用的开源工具。这里重点介绍Github的Awesome系列[awesome-graphql](https://github.com/chentsulin/awesome-graphql)，它列举了Github上面开源的并且十分有用的graphql相关的服务端、客户端以及生态链相关的其他工具。graphql发展至今，已有非常完整的开发语言支持，主流的语言Javascript、Python、Java、PHP、Ruby等都有各自的服务端与客户端实现，在`awesome-graphql`上还有部分语言的[实现参考示例代码](https://github.com/chentsulin/awesome-graphql#example)。这里简要介绍几个常见的库：

[Apollo-Client](https://github.com/apollographql/apollo-client): 算是最知名的GraphQL客户端了，因为它是Javascript的客户端。功能丰富，可用于不同的服务端及前端。

[GraphiQL](https://github.com/graphql/graphiql): 一款运行于浏览器的GraphQL IDE，几乎所有的服务端库都会提供这么一个经典的web页面。该页面是一个单页面应用，可以直接在其上运行查询语句，自带代码补全和校错功能，直接查看GraphQL所有的文档(定义好的Schema)，比如[Github API的在线文档](https://developer.github.com/v4/explorer/)，登录后就能在线发送真实的请求获取到我们想要的数据。由于我们之后要进行实践教程，所以这里有今后用于实践的真实的Web端，[访问地址](https://project.haofly.net/graphql)

![](https://haofly.net/uploads/graphql-tutorial-2_01.png)

<!--more-->

点击右边的`Docs`按钮就可以直接查看文档，

![](https://haofly.net/uploads/graphql-tutorial-2_02.png)

在左边输入框可以输入查询语句，自带补全和校错功能，`Prettify`用于格式化查询语句，左下角点击`QUERY VARIABLES`可以以JSON格式输入附带的变量等参数。右边就是查询结果

![](https://haofly.net/uploads/graphql-tutorial-2_03.png)

[Graphql-Network](https://github.com/Ghirro/graphql-network): Chrome的调试工具，由于GraphQL查询语句是一串字符串，浏览器`审查元素`看起来非常难看，这个工具则可以将其格式化成我们想要的格式。

格式化前: ![](https://haofly.net/uploads/graphql-tutorial-2_04.png)

格式化后: ![](https://haofly.net/uploads/graphql-tutorial-2_05.png)

[GraphDoc](https://github.com/2fd/graphdoc): 可以将文档页面生成静态文档站点。

[GraphQL-Voyager](https://github.com/APIs-guru/graphql-voyager): 生成交互式的schema图。

另外，当前正在使用GraphQL的大厂有GitHub、Shopify、Twitter、 Coursera、Yelp、Wordpress等



[GraphQL 教程demo地址](https://github.com/haoflynet/graphql-tutorial)
[GraphQL 教程（一）——What’s GraphQL](https://haofly.net/graphql-tutorial-1/)
[GraphQL 教程（二）—— GraphQL 生态](https://haofly.net/graphql-tutorial-2/)
[GraphQL 教程（三）—— GraphQL 原理](https://haofly.net/graphql-tutorial-3/)
[GraphQL 教程（四）—— Python Demo搭建](https://haofly.net/graphql-tutorial-4/)
[GraphQL 教程（五）—— 增删改查语法及类型系统](https://haofly.net/graphql-tutorial-5/)
[GraphQL 教程（六）—— N+1问题和缓存等问题](https://haofly.net/graphql-tutorial-6/)