---
title: "GraphQL 教程（六）—— N+1问题和缓存等问题"
date: 2019-04-05 22:52:00
categories: graphql
---

## N+1问题

考虑这样一个常见应用场景，前端页面上需要展示一个文章列表，其中包括了文章的标题，并且会同时显示每篇文章的作者名。那么我们可能会按下面几种方案来设计我们的API。

方案一: 对于Restful，设计下面两个接口，客户端总共需要请求1+N次接口，查询数据库1+N次。

```shell
/articles	# 文章列表接口
/articles/{article_id}/author	# 获取文章作者信息接口
```

<!--more-->

方案二: 对于Restful，为避免多次频繁请求获取文章作者信息的接口，可以采取下面两种方式，不过都得修改后端代码，总共需要请求1次接口，查询数据库1+N次。

```shell
/articles?withauthor=true		# 在原接口的基础上添加一个参数表示是否同时获取文章的作者信息
/articlesWithAuthor					# 直接添加一个新的能够通过获取作者信息的文章列表接口
```

方案三：对于GraphQL，我们不需要做任何的修改，因为我们早已经定义好这样的Schema将article与author进行了关联: 

```python
# schemas/article.py
class ArticleSchema(SQLAlchemyObjectType):
    author = graphene.Field("schemas.AuthorSchema", description="文章作者信息")

    def resolve_author(self, info):
        # 下面这一行请自行在demo中去掉注释
        return AuthorManager.get_one(id=self.author_id)

    class Meta:
        model = ArticleModel
        description = "文章Schema"
```

默认是打开了`SQL`日志的，所以我们可以看到最终的结果仍然是1次请求，数据库查询却有1+N次:

```mysql
SELECT * FROM `articles` LIMIT 0, 20;
SELECT * FROM `authors` WHERE `id` = 1;
SELECT * FROM `authors` WHERE `id` = 2;
SELECT * FROM `authors` WHERE `id` = 3;
...
SELECT * FROM `authors` WHERE `id` = N;
```

为了防止N+1问题，社区为`GraphQL`提供了一个解决方案: `DataLoader`。其原理就是，在需要查询数据库的时候将查询进行延迟，等到拿到所有的查询需求之后再一次性查询出来。在`graphene`里面，批量查询可以这样写:

```python
# managers/author.py
class AuthorsDataLoader(DataLoader):
    def batch_load_fn(self, ids):
        query = DBSession().query(AuthorModel).filter(AuthorModel.id.in_(ids))
        articles = dict([(article.id, article) for article in query.all()])
        return Promise.resolve([articles.get(id, None) for id in ids])
```

最终，仅需要两次数据库查询就完成了两个批量查询，即:

```mysql
SELECT * FROM `articles` LIMIT 0, 20;
SELECT * FROM `authors` WHERE `id` IN (1, 2, 3, ..., N);
```

至此，我们通过批量查询的方式完成了减少冗余查询的功能。但是性能问题依然存在。

## 缓存问题

仔细看上面的两条SQL，第一条查询由于是Graphene框架自己帮我完成了解析然后进行查询，所以其实并不是`SELECT *`，但是多级查询的时候，后面的查询逻辑是我自己写的，为了方便我就写的`SELECT *`，大家都应该知道这样子查询数据库会有很大的性能隐患，访问量一旦大了数据库压力会加倍增长。不过好处是，`DataLoader`本身具有缓存结果的功能，它缓存的是`SELECT * FROM authors WHERE id =N`的结果，而不是批量查询的结果，所以，下一次即使是不一样的`IN`列表，依然会有部分能够使用缓存。`DataLoader`默认本身是开启缓存的，如果想自己用`Redis`等来实现对象的缓存，可以在`DataLoader`初始化的时候将`cache`设置为`False`:

```python
# schemas/.__init__.py
def get_dataloaders():
    return {
        "ArticlesDataLoader": ArticlesDataLoader(cache=False),
        "AuthorsDataLoader": AuthorsDataLoader(cache=False),
        "CommentsDataLoader": CommentsDataLoader(),
        "ArticleCommentsDataLoader": ArticleCommentsDataLoader(),
        "OrdinaryWritersDataLoader": OrdinaryWritersDataLoader(cache=True),
        "ProfessionalWritersDataLoader": ProfessionalWritersDataLoader(cache=False),
    }
```

## 验证问题/限流问题

由于只有一个查询入口，不能像Restful那样针对每个接口进行单独的验证或者限流。但是，正如我之前所说的，一个简单的方法就是强制让用户传入规范命名的查询语句，通过命名来进行后续的判断，就能方便地达到我们的要求。

## 分页查询问题

这个有很多种实现方式，大多数是用类似数据库`limit begin, end`的方式，但是为了兼容`Restful`的习惯，我使用的仍然是`Restful`风格的分页方式，返回结果也与`Restful`类似，可以参考代码:

```python
# schemas/__init__.py
class PageInfoSchema(ObjectType):
    """
    专用于分页的schema
    """
    total = graphene.Int(description="总条数")
    current_page = graphene.Int(description="当前页码")
    per_page = graphene.Int(description="每页数量")
    total_pages = graphene.Int(description="总共页码数量")

    @staticmethod
    def paginate(total: int, current_page: int, per_page: int):
        """
        :param total: 总共条数
        :param current_page: 当前页码
        :param per_page: 每页数量
        :return:
        """
        return PageInfoSchema(
            total=int(total),
            current_page=int(current_page),
            per_page=int(per_page),
            total_pages=math.ceil(int(total) / int(per_page)),
        )
```







[GraphQL 教程demo地址](https://github.com/haoflynet/graphql-tutorial)
[GraphQL 教程（一）——What’s GraphQL](https://haofly.net/graphql-tutorial-1/)
[GraphQL 教程（二）—— GraphQL 生态](https://haofly.net/graphql-tutorial-2/)
[GraphQL 教程（三）—— GraphQL 原理](https://haofly.net/graphql-tutorial-3/)
[GraphQL 教程（四）—— Python Demo搭建](https://haofly.net/graphql-tutorial-4/)
[GraphQL 教程（五）—— 增删改查语法及类型系统](https://haofly.net/graphql-tutorial-5/)
[GraphQL 教程（六）—— N+1问题和缓存等问题](https://haofly.net/graphql-tutorial-6/)