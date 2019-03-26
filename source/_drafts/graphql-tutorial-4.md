---
title: "GraphQL 入门教程（四）—— Python Demo搭建"
date: 2019-03-21 22:52:00
categories: graphql
---

前面几讲讲了理论层面，大家应该对GraphQL不再陌生了。这里简单讲述一下本教程demo的搭建方式。

## Docker安装方式

`Docker`推荐的是将不同的服务分离成不同的容器，但是由于这里只有源程序和MySQL两个，不需要复杂的编排，所以我直接放到了一个容器中。

1. 安装docker工具，[安装方式](https://haofly.net/docker/index.html)

2. 下载项目源码

   ```shell
   git clone git@github.com:haoflynet/graphql-tutorial.git
   ```

3. 编译构建镜像

   ```shell
   cd graphql-tutorial
   docker build -t graphql:latest .
   ```


## 直接运行源码

这里不做详细记录，可以参考`Dockerfile`，简单地说就是:

1. 安装Python3.7并安装依赖
2. 新建数据库，并导入初始化数据
3. `python3.7 run app.py`

## 增删该查

### 添加记录

```json
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
mutation {
  deleteArticle(articleId:6) {
    ok
  }
}
```

### 查询记录

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

### 更新记录

```json
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



