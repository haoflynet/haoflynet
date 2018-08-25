---
title: "SQLAlchemy手册"
date: 2017-11-15 22:51:39
updated: 2018-08-23 15:44:00
categories: python
---

`SQLAlchemy`是Python最广泛使用的一个ORM(对象关系映射，简单地说就是把数据库的表即各种操作映射到Python对象上面来)工具。它支持操作`PostgreSQL`、`MySQL`、`Oracle`、`Microsoft SQL Server`、`SQLite`等支持SQL的数据库。[文档地址](http://docs.sqlalchemy.org/en/latest/contents.html)

- 需要特别注意的是，`SQLAlchemy`只是适用于一些通用的微型框架，而全栈框架`Django`的orm在结合特定框架用起来可能更加便利，所以在使用`SQLAlchemy`的时候，如果不知道怎么完成复杂的定义，那就干脆自己写sql吧，自己去join什么的
- 有另外一个选择`peewee`，提供类似Django那样又好的查询API，比`SQLAlchemy`易用，虽然可能没那么强大，性能可能也没那么好(并没有人去对比过性能)，但是`peewee`还不支持`Oracle`等数据库，虽然我不用，但是为了防止以后多学习一门，就决定是`SQLAlchemy`了
- `SQLAlchemy`本身并不支持异步，在`tornado/sanic`中只有手动去执行异步

## SQLAlchemy安装

```shell
pip install sqlalchemy
```

## SQLAlchemy连接数据库

<!--more-->

```python
# 初始化数据库连接
## echo默认为False，当为True的时候，会把sqlalchemy的所有日志包括连接数据库后做的所有操作都会打印出来，对于调试来说是非常方便的
## pool_size是连接池中连接的数量
## max_overflow指允许的最大连接池大小，当超过pool_size后如果仍需要连接仍然可以创建新的连接，而当超过max_overflow后则不会创建新的连接，必须等到之前的连接完成以后，默认为10，为0表示不限制
## pool_recycle表示连接在给定时间之后会被回收，不能超过8小时
## pool_timeout表示等待多少秒后，如果仍然没有获取到连接则放弃获取
## pool_pre_ping表示每次取出一个连接时，会发送一个select 1来检查连接是否有效
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
engine = create_engine('mysql://scott:tiger@localhost/foo?charset=utf8', echo=True, pool_size=5, max_overflow=10, pool_recycle=-1, pool_timeout=30, pool_pre_ping=True)
engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
engine = create_engine('sqlite:///foo.db')

DBSession = sessionmaker(bind=engine)	# 创建DBSession类型，可视为当前数据库的连接
session = DBSession()	# 创建一个session对象

# session基本操作
new_user = User(id='1', name='haofly')	# 新建一个User对象
session.add(new_user)
session.commit()	# 提交
session.close()		# 关闭session
```

需要注意的是，如果没有修改autocommit的默认值(False)，那么一个session会一直保持，直到该session被回滚、关闭、提交才结束。每次发起请求，都创建一个新的session(注意不是创建新的连接，创建session并不会有多大的开销)，一个session就是一个transaction的支持。我们可以让session是一个全局的对象，这样和数据库通信的session在任何时候只有一个，但是全局的session不是线程安全的，如果多线程的情况下，可能会造成commit错乱，`tornado`这种单线程程序由于其异步的特性也不可以那样做(Tornado可以在每个`Handler`的初始化进行session的创建与提交销毁)。当然，如果是在单线程的情况下，我们完全可以保持session的单例，减少一丢丢的开销。

```python
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=some_engine)
Session = scoped_session(session_factory)	# 为了保证每个线程获得的session对象是唯一的
some_session = Session()
some_other_session = Session()
some_session is some_other_session # True，在一个线程里面创建的session对象都是一样的了。
```

## Model/数据表定义

### 表定义

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'		# 定义列名
    __mapper_args__ = {'column_prerfix': '_'}	# 自动给所有的列添加一个前缀
    id = Column('user_id', Integer, primary_key=True)
    
    class __str__(self):	# print(object)的时候输出的，默认仅输出类名
        return f'<{self.__class__.__module__}.{self.__class__.__name__}(id={self.id})>'
    
User.__table__.columns	# 获取table中定义的字段(这种方式获取到的字段不会包括关系那些字段)
```

### 列定义

```python
# 列类型
## 数字
BigInteger	# 长整型
Boolean		# 布尔值
Enum		# 枚举值，例如Column(Enum('A', 'B"))，对象取值的时候，取出来的字段是Enum对象，需要.value才能得到真正的值
Float
SmallInteger
Integer(unsigned=False)		# 整型
Interval
Numeric
## 字符
JSON
LargeBinary(length=None)	# 二进制
PickleType	# pickle类型
SchemaType
String(50)	# 字符串varchar类型，括号里表示长度
Text(length=None)
Unicode
UnicodeText
## 时间
Date
DateTime	# daatetime.datetime()对象
Time		# datetime.time()对象
TIMESTAMP	# 时间戳

# 关联列属性
fullname = column_property(firstname + ' ' + lastname)	# 表示这一列的值由指定的列值确定

# 列属性
primary_key=True	# 是否是主键
comment=''			# 注释，1.2版本才有的新特性
table_name.column_name.name	# .name获取真实的列名
```

### 关联关系定义

- `relationship`的几个常用的参数
  - `backref`是在一对多或者多对一关系之间简历双向的关系
  - `lazy`懒加载，默认为`True`
  - `remote_side`: 外键是自身时使用，例如`remote_side=[id]`
  - `secondary`: 指向多对多的中间表

#### 一对多/多对一

```python
class User(Base):
    __tablename__ = 'users'
    id= Column(Integer, primary_key=True)
    posts = relationship('Post', backref='post')

class Post(Base):
    __tablename__ = 'posts'
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts', cascade='all, delete, delete-orphan')	# back_populates属性为反向关系所对应的属性进行命名，其值应该是User里面定义的属性名称，cascade属性是一个触发器，表示当删除user的时候，与其关联的posts会自动同时删除，但无论怎样，我更建议自己手动去删除

    
user = User(...)
user.posts = [		# 创建相关联的对象，不需要指定user_id了
    Post(...), Post(...)
]
user.posts		# 获取所关联的posts
post.user		# 获取所关联的user
session.commit()	# 提交创建user和posts
```

#### 一对一

仅需要将上面的一对多关系中`uselist=False`即可

```python
class User(Base):
    __tablename__ = 'users'
    posts = relationship('Post', uselist=False, back_populates='post')
```

#### 多对多

- 关于一个表同一个字段对应多张表的外键(类似`Laravel/Django`中的`target_id/targe_type`定义方式)，`sqlalchemy`没有一个官方的定义方式，有个现成的[Generic relationships](https://sqlalchemy-utils.readthedocs.io/en/latest/generic_relationship.html)，但是该库作者已经许久没维护了。我的建议是自己join吧。
- 如上一条`SQlAlchemy`里面比较难实现复杂的多对多关系，所以官方的文档就干脆建议大家连关系表都不用单独建daemon了，直接按照下面的方法来更简单。

```python
# 一个用户对应多个权限，一个权限对应多个用户
user_privilege_relationship = Table('user_privilge_relationships', Base.metadata, 
                           Column('user_id', Integer, ForeignKey('users.id'))
                           Column('privilege_id', Integer, ForeignKey('privilege.id'))
                                   )
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    privileges = relationship('Privilege', secondary=user_privilege_relationship, backref='users')
    
class Privilege(Base)
	__tablename__ = 'privileges'
    id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=user_privilege_relationship, backref='privileges')
```

### 列方法

```python
# 类属性
@hybrid_property
def fullname(self):
    return self.firstname + ' ' + self.lastname	# 这样就可以用user.fullname访问该属性

# 验证列
@validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address
```

## CRUD

### 查询

```python
# 查询表
query = session.query(User)
print(query)		# 得到sql语句
query.statement	# 同上
query.count()	# COUNT操作
query.get(2)	# 根据主键获取的简便写法
query.first()	# 只获取第一条
query.all()		# 获取所有数据
session.query(User.id).distinct().all()	# DISTINCT操作
query.limit(2).offset(2).all() # limit offset要注意如果page相乘的时候page-1

# 筛选
query.filter(
    User.id==2, 
   	User.age>10, 
    User.deleted_at == None, # IS NULL用None代替
    User.name.in_(['hao', 'fly'])	# IN操作
).first().name
query.filter('id = 2').first()	# 复杂的filter
query.order_by('user_name').all()		# 排序
query.order_by(desc('name')).all()		# 倒序排序，from sqlalchemy import desc
query(func.count('*')).all()

# 查询列
session.query(User.name)	# 去除指定列
session.query(User.id, User.name)

# 拼接
query2.filter(or_(User.id == 1))	# or操作

# 关联查询
query(User).join(Post, User.id == Post.user_id).all()	# join查询
query(User).join(Post, and_(User.id == Post.user_id, User.deleted_at==None))	# JOIN ... ON (xxx AND xxx)，join的and操作

## 关联查询外键
query.filter(Post.user == user)
query.filter(Post.user == None)
query.filter(User.posts.contains(post))
query.filter(User.posts.any(title='hao'))
query.filter(Post.user.has(name='haofly'))
from sqlalchemy.sql import exists
stmt = exists().where(Post.user_id==User.id)
for name, in session.query(User.name).filter(stmt):	# 查询存在Post的user
    print(name)
    
# LIKE查询
query.filter(User.name.like('%王%'))
```

### 插入

```python
session.add(User(name='haofly'))	# 直接插入一条数据

# 批量插入ORM版
session.bulk_save_objects([User(name="wang") for i in xrange(1000)])

# 批量插入非ORM版
session.execute(
    User.__table__.insert(),
    [{'name': 'wang', 'age': 10}, {}]
)
session.commit()
```

### 修改

```python
query.filter(...).update({User.age: 10})
session.flush()	# 写数据库，不提交

user.name = 'new'
session.commit()
```

### 删除

```python
session.delete(user)
```

### 其他

```python
session.rollback()	# 回滚
session.commit()	# 提交
```

## TroubleShooting

- **Tornado中使用SQLAlchemy连接SQLite进行commit操作的时候程序中断: Segment Fault**: 原因是`SQLite`的自增主键`id`重复了😂

- **UnicodeEncodeError：'latin-1' codec can't encode characters in position 0-1: ordinal not in range(256)**: 连接数据库没有指定utf8的charset，参考本文连接数据库设置。

   

