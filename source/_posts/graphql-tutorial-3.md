---
title: "GraphQL 入门教程（三）—— GraphQL 原理"
date: 2019-03-21 22:52:00
categories: graphql
---

对于简单的GraphQL查询，其实很简单，任何一个会CRUD的开发者都知道，使用简单的if … else … 就能实现逐字段的遍历查询。这也就是GraphQL的核心算法，只是针对每个字段，GraphQL会提供一个resolver去实现特殊的字段获取方式，详情可以看demo代码，例如: https://github.com/haoflynet/graphql-tutorial/blob/master/schemas/article.py。

假设有这样一个查询:

```json
{
  articles {
    title // SEELCT `title` FROM `articles`;
    comments {
      content // for id in article_ids: SELECT `content` FROM `comments` WHERE `article_id`=id;
    }
  }
}
```

<!--more-->

服务器收到请求后，首先会验证语法是否正确，然后逐级检查其对应的Schema，`article`对应`ArticleSchema`，然后字符串`title`是`ArticleSchema`本来的属性，`comments`则被解析为包含`CommentSchema`的列表，所以，在解析`comments`的时候会去获取下级的列表，最后再在每一个`CommentSchema`中获取字符串`Content`。

服务端实现原理非常容易理解，但是，如果仅此而已，那会出现很明显的性能问题。比如如果想要在查询文章列表的时候顺带把每篇文章的作者及评论都查询出来，那按照上面的逻辑，假设有n篇文章，总共的查询次数就应该是1(1次查询出文章列表)+n(n篇文章查询作者)+n(n篇文章查询其评论列表)，典型的n+1问题，对性能有很大的影响。这还只是两级查询的情况，如果层层嵌套，甚至不小心搞成了“环”，那服务器的性能甚至会出现指数级增长。好在社区为这个问题提供了比较巧妙的方法，即[DataLoader](http://link.zhihu.com/?target=https%3A//github.com/facebook/dataloader)，自动将某些重复的查询进行批处理，例如这里就可以改成1(1次查询出文章列表)+1(1次IN查询作者列表)+1(1次IN查询评论列表)，即

```json
{
  articles {
  	title // SEELCT `title` FROM `articles`;
    datas {
      author {
        name // SELECT `name` FROM `authors` WHERE `id` IN (article_ids);
      }
      comments {
        content // SELECT `content` FROM `content` WHERE `article_id` IN (article_ids)
      }
    }
  }
}
```

具体例子可见[demo](https://github.com/haoflynet/graphql-tutorial)中每个`manager`下面的`DataLoader`查询类。
