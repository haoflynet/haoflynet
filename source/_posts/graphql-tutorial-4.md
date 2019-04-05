---
title: "GraphQL 教程（四）—— Python Demo搭建"
date: 2019-04-01 22:52:00
updated: 2019-04-05 22:10:00
categories: graphql
---

前面几讲讲了理论层面，大家应该对GraphQL不再陌生了。这里简单讲述一下本教程demo的搭建方式。

## 代码目录结构

```shell
.
├── Dockerfile
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── database.sql # 初始数据库
├── db.py
├── managers # 封装数据库操作
│   ├── __init__.py
│   ├── article.py
│   ├── author.py
│   ├── comment.py
│   ├── ordinary_writer.py
│   └── professional_writer.py
├── models # 数据库映射对象
│   ├── __init__.py
│   ├── article.py
│   ├── author.py
│   ├── comment.py
│   ├── ordinary_writer.py
│   └── professional_writer.py
├── mutations # 操作变更定义
│   ├── __init__.py
│   ├── article.py
│   ├── author.py
│   └── comment.py
├── run.py # 主程序
├── schemas # 模型数据结构定义
│   ├── __init__.py
│   ├── article.py
│   ├── author.py
│   ├── comment.py
│   ├── interfaces.py	# 接口schema
│   ├── ordinary_writer.py
│   └── professional_writer.py
├── settings.py # 数据库连接配置
└── web_template.py # 
```

<!--more-->

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

4. 启动容器

   ```shell
   docker run -it -p 5000:5000 -d graphql:latest
   ```

5. 浏览器打开`http://127.0.01:5000/web`即可访问。

## 直接运行源码

直接参考项目根目录的`Dockerfile`，这里不再赘述，几条命令即可将代码运行起来。





[GraphQL 教程demo地址](https://github.com/haoflynet/graphql-tutorial)
[GraphQL 教程（一）——What’s GraphQL](https://haofly.net/graphql-tutorial-1/)
[GraphQL 教程（二）—— GraphQL 生态](https://haofly.net/graphql-tutorial-2/)
[GraphQL 教程（三）—— GraphQL 原理](https://haofly.net/graphql-tutorial-3/)
[GraphQL 教程（四）—— Python Demo搭建](https://haofly.net/graphql-tutorial-4/)
[GraphQL 教程（五）—— 增删改查语法及类型系统](https://haofly.net/graphql-tutorial-5/)
[GraphQL 教程（六）—— N+1问题和缓存等问题](https://haofly.net/graphql-tutorial-6/)