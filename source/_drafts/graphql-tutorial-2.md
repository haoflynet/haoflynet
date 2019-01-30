---
title: "GraphQL 入门教程（二）—— GraphQL 生态"
date: 2019-01-20 21:52:00
categories: graphql
---

重点介绍Github的Awesome系列[awesome-graphql](https://github.com/chentsulin/awesome-graphql)，这里列举了Github上面开源的并且十分有用的graphql相关的服务端、客户端以及生态链相关的其他工具。graphql发展至今，已有非常完整的开发语言支持，主流的语言Javascript、Python、Java、PHP、Ruby等都有各自的服务端与客户端实现，在`awesome-graphql`上还有部分语言的[实现参考示例代码](https://github.com/chentsulin/awesome-graphql#example)。这里简要介绍几个常见的库：

[Apollo-Client](https://github.com/apollographql/apollo-client): 算是最知名的GraphQL客户端了，因为它是Javascript的客户端。功能丰富，可用于不同的服务端及前端。

[GraphiQL](https://github.com/graphql/graphiql): 一款运行于浏览器的GraphQL IDE，几乎所有的服务端库都会提供这么一个经典的web页面。该页面是一个单体的页面，可以直接在其上运行查询语句，自带代码补全和校错功能，直接查看GraphQL所有的文档(定义好的Schema)，比如[Github API的在线文档](https://developer.github.com/v4/explorer/)，登录后就能在线发送真实的请求获取到我们想要的数据。由于我们之后要进行实践教程，所以这里有今后用于实践的真实的`GraphiQL`。











点击右边`Docs`按钮可以直接查看文档，点击左边的运行按钮即可直接运行查询语句，返回需要的数据。比如









[Graphql-Network](https://github.com/Ghirro/graphql-network): Chrome的调试工具，由于GraphQL查询语句是一串字符串，浏览器`审查元素`看起来非常难看，这个工具则可以将其格式化成我们想要的格式：















[GraphDoc](https://github.com/2fd/graphdoc): 可以将文档页面生成静态文档站点。

[GraphQL-Voyager](https://github.com/APIs-guru/graphql-voyager): 生成交互式的schema图。