---
title: "GraphQL 教程（五）—— 增删改查语法及类型系统"
date: 2019-04-02 22:52:00
updated: 2019-04-04 16:44:44
categories: graphql
---

本讲将会介绍GraphQL的基础语法，毕竟业务永远都离不开增删改查。

除“读“操作可以直接与数据库model相映射以外，跟”写“有关的操作的后端定义依然是需要自己去实现业务相关的映射逻辑的。当然，无论读写都是需要定义相应的Model的，可以在Web上面查看已经定义的Mutation:

![](https://haofly.net/uploads/graphql-tutorial-5_01.png)

<!--more-->

## 基本语法

### 查询记录

#### 嵌套查询

 获取文章列表及其评论内容

```json
{
  articles {
    datas {
      title
      comments {
        content
      }
    }
  }
}
```
#### 带参数的搜索

```json
{
  articles(limit:1, page:2) {
    pageInfo {
      totalPages
      perPage
    }
    datas {
      title
      comments {
        content
      }
    }
  }
}
```
#### 聚合查询

同时查询多个不关联的`Schema`，常用于同一个前端页面中不同信息的获取

```json
query All {
  articles(limit:1, page:2) {
    datas {
      title
    }
  }
  
  authors (limit:1){
  	datas {
      name
    }  
  }
}
```

#### 使用别名查询相同对象

得到的结果将会以别名进行命名

```json
{
  articleA: article(title: "标题4") {
    content
  }
  articleB: article(title: "标题3") {
    content
  }
}
```

#### 使用片段查询相同字段

即使能使用别名查询相同的对象，但是在大多数情况，依然会取相同对象的相同字段，这时候可以使用片段来定义我们需要取用的字段，而不用每个对象都去重复写了。并且片段内同样可以定义变量

```json
{
  articleA: article(title: "标题4") {
    ...articleFields
  }
  
  articleB: article(title: "标题3") {
    ...articleFields  
  }
}

fragment articleFields on ArticleSchema {
    id
    content
    createdAt
    updatedAt
}
```

#### 带变量的查询

页面上，左下角可以输入查询参数`QUERY VARIABLES`，可以输入变量的值`{ "limit": 2 }`，下面的查询中`limit`默认值为1

```json
query Test($limit: Int = 1) {
  articles(limit: $limit, page:2) {
    datas {
      title
    }
  }
  
  authors (limit: $limit){
  	datas {
      name
    }  
  }
}

```

#### 为操作命名

前面的语法大多数都省略了查询名称，这是因为查询名称的有无对查询结果并无影响，但是在写入或者是需要详细记录用户查询日志的时候，我们可以让用户传入查询名称，甚至可以用这个来做鉴权。

一个简单的查询名称如下所示，其中操作类型可以为`query`、`mutation`或`subscription`。

```json
query myArticle {
  article (title:"文章4") {
    content
  }
}
```

#### 使用指令(Directives)实现条件查询

当我们要通过某个条件来判断是否获取某个字段的时候可以使用指令来实现，指令包括两种，`@include(if: Boolean)`表示在参数为true时包含此字段，`@skip(if: Boolean)`表示在参数为true时跳过此字段。

```json
query Test($limit: Int = 1, $withComments: Boolean!) {
  articles(limit: $limit, page:2) {
    datas {
      title
      comments @include(if: $withComments) {
        id
        content
      }
    }
  }
  
  authors (limit: $limit){
  	datas {
      name
    }  
  }
}
```

对应的参数为，如果改变`withComments`的真假会得到不同的结果。

```json
{
  "limit": 2,
  "withComments": false
}
```

#### 使用内联片段(Inline Fragments)实现接口类型查询

这里的接口并不是指API接口，而是指对象类型的接口，例如`PHP/Java`开发中的`interface`类，在python里面直接就是某个基类，基于接口可以实现不同的对象。下面的方式就能查询出作者信息，并根据业余作者和专业作者的不同查询出不同的字段。`__typename`可以在结果中返回其`Schema`名称，即**元字段**。

```json
{
  authors {
    datas {
      name
      writer {
        authorId
        __typename
        ... on OrdinaryWriterSchema {
          job
        }
        ... on ProfessionalWriterSchema {
          publishingHouse
        }
      }
    }
  }
}
```

### 添加记录

添加文章操作

```json
// 根据文章ID删除文章操作
mutation {
  createArticle(authorId:123, content:"abc",title:"def") {
    ok
    article {
      content
      title
    }
  }
}
```

### 删除记录

```json
// 根据文章ID删除文章
mutation {
  deleteArticle(articleId:6) {
    ok
  }
}
```


### 更新记录

```json
// 根据文章ID更新文章内容
mutation {
  updateArticle(articleId:2, content:"更新内容") {
    ok
    article {
      title
      content
    }
  }
}
```

## 类型系统

`demo`中涉及到了`GraphQL`的大部分对象类型，总结一下，`GraphQL`包含如下几种类型系统

#### 查询和变更类型

即`query`和`mutation`

#### 标量类型

包含`Int`(32位有符号整数)、`Float`(有符号双精度浮点数)、`String`(UTF-8字符序列)、`Boolean`、自定义类型。

#### 枚举类型

#### 列表和非空

类型定义的时候，后面加感叹号表示非空，它也可用在变量查询中。

````json
type ArticleSchema {
  title: String!
  comments: [CommentSchema]!
}
````

#### 接口类型(Interfaces)

类似基类或者抽象类，上面查询示例中有实际的例子。

```json
interface AuthorWriterInterface {
  author_id: Int!
}
```

#### 联合类型(Union Types)

和接口类型非常相似，但是它不用指定类型间的相同字段。这样表示：

```json
union writers = OrdinaryWriterSchema | ProfessionalWriterSchema
```

#### 输入类型(Input Types)

将一组需要复用的输入字段作为一个整体进行输入，只能用于输入，与返回的`Schema`无关。例如

```json
input addArticleInput {
  title: String!
  content: String!
}
```

那么可以定义一个包含该输入类型的动作：

```json
mutation CreateArticle($request: addArticleInput!) {
  createArticleMutation(request: $request) {
    article
  }
}
```

然后直接在`variables`中这样定义

```json
{
  "request": {
    "title": "标题",
    "content": "内容"
  }
}
```





[GraphQL 教程demo地址](https://github.com/haoflynet/graphql-tutorial)
[GraphQL 教程（一）——What’s GraphQL](https://haofly.net/graphql-tutorial-1/)
[GraphQL 教程（二）—— GraphQL 生态](https://haofly.net/graphql-tutorial-2/)
[GraphQL 教程（三）—— GraphQL 原理](https://haofly.net/graphql-tutorial-3/)
[GraphQL 教程（四）—— Python Demo搭建](https://haofly.net/graphql-tutorial-4/)
[GraphQL 教程（五）—— 增删改查语法及类型系统](https://haofly.net/graphql-tutorial-5/)
[GraphQL 教程（六）—— N+1问题和缓存等问题](https://haofly.net/graphql-tutorial-6/)