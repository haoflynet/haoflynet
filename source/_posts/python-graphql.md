---
title: "Python使用graphene-sqlalchemy提供GraphQL接口"
date: 2018-08-14 18:52:39
updated: 2018-09-03 16:43:00
categories: python
---

关于`GraphQL`本身的语法，可以参考我写的[GraphQL 使用手册](https://haofly.net/graphql)。

`graphene`是为python提供的`GraphQL`扩展，项目组在[GraphQL Python](https://github.com/graphql-python)。该项目主要有以下几个特点:

- 提供十分方便的自定义功能，从解析到查询到处理结果，都能够自定义
- 有`Dataloader`功能，能解决`N+1`问题
- 与流行框架有现成的集成扩展`graphene-django`、`flask-graphql`、`graphene-gae`以及通用的`graphene-sqlalchemy`
- 支持复杂的Relay查询
- 支持复杂的`Connection`查询，能实现分页的功能
- 支持`NoSQL`、`MySQL`甚至直接支持Python对象作为数据源
- 最大的缺点是，文档写得太简单了，高级用法全得靠自己摸索

下面以实际的例子来说明如何使用，毕竟官方文档那啥。完整的例子见我的gist: [graphene-sqlalchemy使用示例](https://gist.github.com/haoflynet/85ec02eb003f7e4a3a53bcdcdb7dc8b1)

<!--more-->

### 基础使用

##### 示例Model定义

常规方法定义就好。下面均以用户模型与文章模型举例，两者是一对多的关系

```python
class UserModel(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    posts = relationship('PostModel', backref='posts')
    
class PostModel(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    meta = Column(String(255))
```

##### 根据Model定义Schema

- 如果不像为某张表单独建立一个`schema`，那么可以只建立一个`DataLoader`，之前担心查询该表的多个字段的时候会重复查询，后来发现`DataLoader`依然会合并为一句，并且如果在里面进行去重，依然能达到只查询一次的效果。

```python
from graphene_sqlalchemy import SQLAlchemyObjectType

class UserTypeEnum(enum.Enum):
    customer = 'the_customer'
    vip = 'the_vip'

class User(SQLAlchemyObjectType):
    uuid = graphene.String(description='这里写备注，能够在web页面自动显示')
    user_type = graphene.Enum.from_enum(UserTypeEnum, description='枚举类型')
    user_data = graphene.JSONString(description='json格式的字符串类型，注意不会自动转换成json，如果不是一个对象也建议不用单独写schema')
    user_meta = graphene.types.generic.GenericScalar(description="通用类型，可以同时表示String/Boolean/Int/Float/List/Object, 没错，Object可以是JSON对象")
    test = graphene.Field('schemas.OtherSchema')	# 如果出现cannot import xxxschema的错误，可以用这种方式引入，在导入的时候不会去交叉引用
    
    def resolve_user_type(self, info):
        return UserTypeEnum('the_customer')
    
    class Meta:
        model = UserModel
        description = 'Schema的备注'
        only_fields = ('name', )	# 仅能获取某些model字段
        exclude_fields = ("deleted_at",)	# 隐藏某些model的字段
        
class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = PostModel

# 定义一种查询方式，该查询只支持查询user字段
class Query(graphene.ObjectType):
    users = graphene.List(User)		# 这一层是query下面的第一层允许的字段
    test = graphene.Field(graphene.String)	# 自定义返回字段
    
    def resolve_users(self, info):
        return db_session.query(User).all()	# 这里可以自己定义查询方式
    
    def test(self, info):
        return 'ok'

schema = graphene.Schema(query=Query)
```

##### 执行查询

```python
# 这条示例会把所有的user以及它下面的posts全部查询出来，会执行N*N次查询
query = '''
	query {
		users {
			id,
			name,
			posts {
				id, 
				meta                    
			}
        }
    }
'''
result = schema.execute(query, context_value={'session': db_session})
print(result.errors)	# 查看错误
```

### 分页功能/自定义筛选字段

如果要对某个对象列表进行分页，那么需要将该对象定义为`Connection Field`。

##### 定义需要自定义参数的字段

- 其中`args`就是`query`的查询条件，例如`{'limit':10, 'offset':20}`，这里可以自定义更多的参数查询

```python
class UsersConnectionField(SQLAlchemyConnectionField):
    def __init__(self, type, *args, **kwargs):
        super().__init__(type, uuid=String(), *args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super().get_query(model, info, None, **args)
        if 'limit' in args:
            query = query.limit(args['limit'])
        if 'offset' in args:
            query = query.offset(args['offset'])
        return query
```

##### 修改Query

```python
class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int(), offset=graphene.Int())	# 这里需要定义允许的筛选条件

    def resolve_users(self, info, **args):
        query = UsersConnectionField.get_query(UserModel, info, None, **args)	# 需要用新的方式来生成查询语句query
        query = DBSession().query(UserModel).all()	# 这里可以直接直接写sql，跟上面的方式结果一样
        return query.all()
```

##### query添加筛选条件

```python
query = '''
	query {
		users (limit:10, offset:20) {
			id,
			name,
			posts {
				mirrorId
			}
		}
	}
'''
```

### 元字段(meta fields)/interfaces接口/多类型

同一个字段返回多个类型，例如

```json
{
    book(id:"") {
        name
        bookTarget {
            __typename
            target_name
            ... on Novel {
            	novel_name        
            }
            ... on Story {
                story_name
            }
        }
    }   
}
```

可以这样子定义

```python
class bookTargetInterface(graphene.Interface):
    id = graphene.Int()
    
class Novel(graphene.SQLAlchemyObjectType):
    class Meta:
        model = NovelModel
        interfaces = (bookTargetInterface)
        
class Story(graphene.SQLAlchemyObjectType):
    class Meta:
        model = NovelModel
        interfaces = (bookTargetInterface)

# 最后必须在创建schema的时候把接口的实现声明
Schema = graphene.Schema(query=Query, types=[Novel, Story])
```

### DataLoader减少查询次数

上面的示例中，每个users对象对应N个posts，即使是查询一个单独的user也会执行N+1次查询，`DataLoader`方法则可以使用`Promise`的方式合并子查询，使查询次数减少到1+1次。多数的`GraphQL`框架都已支持`DataLoader`方式自动合并`SQL`。

##### 定义DataLoader

```python
from promise.dataloader import DataLoader

class PostsDataLoader(DataLoader):
    def batch_load_fn(self, keys):
        q = db_session.query(PostModel).filter(PostModel.uuid.in_(keys))	# 这里可以对keys进行一次去重操作，因为下面return的时候反正都是有顺序的
        posts = dict([(post.uuid, post) for post in q.all()])
        return Promise.resolve([posts.get(uuid, None) for uuid in keys])
```

##### 子对象查时使用DataLoader

需要修改`User`

```python
class User(SQLAlchemyObjectType):
    posts = graphene.List(Post)
    post = graphene.Field(Post)	# 如果是一对一就这样
    
    other_fields = graphene.Int()	# 同时，如果有其他的字段需要特殊的转换，同样可以在这里添加，然后下面resolve_字段名里面转换即可

    def resolve_posts(self, info, **args):
        return info.context.get('PostsDataLoader').load(self.id).then(lambda response: [response])
    
    def resolve_post(self, info, **args):
        return info.contextg.et('PostsDataLoader').load(self.id).then(lambda responpse: response)	# 如果是一对一就不用写[]，不然会出现类型不兼容的错误

    class Meta:
        model = UserModel
```

##### 查询时传入DataLoader实例

```python
result = schema.execute(query, context_value={'session': db_session, 'PostsDataLoader': PostsDataLoader()})

# DataLoader实例相关方法
dataLoader = DataLoader(cache=False)	# 这里如果不传入cache默认为True，会自动缓存查询结果，这个功能简直太棒了，不过还是要看实际场景看需不需要缓存，看源码可以知道cache的key就是load传入的值
dataLoader.clear(key)	# 清除指定load(key)缓存
dataLoader.clear_all()	# 清除所有缓存
```

## TroubleShooting

- **TypeError: __init__() got multiple values for argument 'type'**: 这是因为想要查询的字段为`type`，但是`graphene.Field`在初始化的时候正好有`type`这个参数，可以这样解决:

  ```python
  class Query(graphene.ObjectType):
      user =graphene.List(
          page=graphene.Int(description="页码数(默认为1)"),
          limit=graphene.Int(description="每页数量(默认为20)"),
          _type=graphene.String(description="类型", name="type"),	# 其实左边的_type怎么命名都无所谓，用户在查询时候都是使用type，但是，内部接收到的参数名字却是_type
      )
  ```
- **You need to pass a valid SQLAlchemy Model in xxxx, received <>**: 明明传入的确实是一个`SQLAlchemy Model`但是却说没有，其实多半是`model`定义有误，可以直接断点调试`SQLAlchemyObjectType`类的`__init_subclass_with_meta__`方法中的`is_mapped_class`，里面实际上报的错误信息更详细地说明了错误在哪里

**扩展阅读**


- [Query Builder + Promise 2.0 + DataLoader #74](https://github.com/graphql-python/graphql-core/pull/74)
- [demo-friends-management](https://github.com/ivanchoo/demo-friends-management/blob/cbc61ebc9c2f06736537032e028aad73785380b7/server/app/graphql/users.py)

