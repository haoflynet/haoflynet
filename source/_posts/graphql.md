---
title: "GraphQL 简介"
date: 2018-08-13 22:52:39
updated: 2018-09-03 15:03:00
categories: python
---

Github的API在V3版本使用的是`Restful`风格的API，在V4版本则完全使用`GraphQL`风格的API，我也是从这儿开始认识的。准确地说`GraphQL`是一种用于API的查询语言，我们可以使用它来构建强大的API。

##### GraphQL的优点

- 服务端所有请求入口一般只有一个`/graphql`
- 查询语句一般只使用`POST`或者`GET`请求中的一种，一般不会使用其他的的HTTP动词
- 服务端统一定义资源数据结构，返回数据结构于请求数据结构一样
- 客户端想要什么就请求什么，不要的字段就不获取，不多不少，`Restful API`可做不到这一点
- 客户端如果想要关联的数据，只需要一次请求，而`Restful API`则需要N次

<!--more-->

##### GraphQL的缺点

- 服务端需要做非常多的优化，安全优化、查询优化、缓存优化等
- 服务端得定义并维护大量的schema
- 由于入口只有一个，所以，如果不是用的`GET`，那么查询的请求日志完全看不出来用户在干嘛，`Restful API`很方便查访问日志
- 本身查询语法并不是很好懂，没有json那样直观，在编写的时候基本都得借助格式化UI工具，好在这样的工具很多
- 可能存在N+1问题，查询1个资源关联的N个资源时候，可能并不会合并N个资源的查询。这个需要服务端自己处理该问题，不过现在各种GraphQL框架都使用`DataLoader`的方式解决了该问题，将SQL查询进行合并，例如`graphql-python`就支持该操作
- 安全问题，一是查询要防止出现环，另一个查询要防止用户一次请求大量的数据，导致突然很快耗尽服务器资源

## GraphQL语法

### 查询

```json
// 普通query
{
  hero {
    name
  }
}

// 带参数的查询
{
  human(id: 1000) {
    name
    height
  }
}

// 别名，直接定义返回字段的参数名，相当于返回字段的名称也能自己定义了
{
  empireHero: hero(episode: EMPIRE) {	// 本来的字段名是EMPIRE
    name
  }
  jediHero: hero(episode: JEDI) {
    name
  }
}

// 自定义查询的操作名称，没有强制要求，名称也可以随便取，主要作用就是方便查日志而已
query HeroNameAndFriends {
  hero {
    name
    friends {
      name
    }
  }
}

// 指令(Directives)，好处是可以通过传入的参数确定是否在本次查询时包含某个字段或者跳过某个字段
// @include(if: Boolean)，为true时，包含该字段
// @skip(if: Boolean)，为true时，跳过该字段
query Hero($episode: Episode, $withFriends: Boolean!) {
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}

// 同一个字段如果对应多种类型，可以使用元字段,meta fields，在graphene中，用interfaces表示
{
    book(id:"") {
        name
        bookTarget {
            __typename		// 固定的，表示下面需要按照类型来确定返回字段
            target_name		// 这里定义公共字段
            ... on Novel {	// 下面的字段表示当类型为Novel的时候需要哪些字段
            	novel_name        
            }
            ... on Story {
                story_name
            }
        }
    }   
}
```



##### 扩展阅读

[中文文档网站](http://graphql.cn/)

[使用React及GraphQL的仿hackernews网站](https://github.com/clintonwoo/hackernews-react-graphql)

[阻碍你使用 GraphQL 的十个问题](http://jerryzou.com/posts/10-questions-about-graphql/)

 