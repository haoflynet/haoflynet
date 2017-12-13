---
title: "SQLAlchemy手册"
date: 2017-11-15 22:51:39
updated: 2017-12-11 23:14:00
categories: python
---

`SQLAlchemy`是Python最广泛使用的一个ORM(对象关系映射，简单地说就是把数据库的表即各种操作映射到Python对象上面来)工具。它支持操作`PostgreSQL`、`MySQL`、`Oracle`、`Microsoft SQL Server`、`SQLite`等支持SQL的数据库。[文档地址](http://docs.sqlalchemy.org/en/latest/contents.html)

## SQLAlchemy安装

```shell
pip install sqlalchemy
```

## SQLAlchemy连接数据库

```python
# 初始化数据库连接
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
engine = create_engine('mysql://scott:tiger@localhost/foo')
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
Session = scoped_session(session_factory)
some_session = Session()
some_other_session = Session()
some_session is some_other_session # True，在一个线程里面创建的session对象都是一样的了。
```

## Model/数据表定义

### 表定义

```python
Base = 
class User(Base):
    __tablename__ = 'users'		# 定义列名
    __mapper_args__ = {'column_prerfix': '_'}	# 自动给所有的列添加一个前缀
    id = Column('user_id', Integer, primary_key=True)
   
```

### 列定义

```python
# 列类型
## 数字
BigInteger	# 长整型
Boolean		# 布尔值
Enum		# 枚举值，例如class MyEnum(enum.Enum): one=1 two =2. 定义时候Enum(MyEnum)
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
String(50)	# 字符串类型，括号里表示长度
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
```

### 关联关系定义

```python
# One To Many, 外键关系的定义
class Post(Base):
    __tablename__ = 'posts'
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='posts', cascade='all, delete, delete-orphan')	# back_populates属性为反向关系所对应的属性进行命名，cascade属性是一个触发器，表示当删除user的时候，与其关联的posts会自动同时删除，但无论怎样，我更建议自己手动去删除
class User(Base):
    __tablename__ = 'users'
    posts = relationship('Post', back_populates='user')
    
user = User(...)
user.posts = [		# 创建相关联的对象，不需要指定user_id了
    Post(...), Post(...)
]
user.posts		# 获取所关联的posts
post.user		# 获取所关联的user
session.commit()	# 提交创建user和posts
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
query		# 打印sql语句
query.count()
query.statement	# 同上
query.all()		# 获取所有数据
session.query(User.id).distinct().all()
query.limit(2).all()
query.offset(2).all()
query.first()
query.get(2)	# 根据主键获取
query.filter(User.id==2, age>10).first().name
query.filter('id = 2').first()	# 复杂的filter
query.order_by('user_name').all()		# 排序
query(func.count('*')).all()

# 查询列
session.query(User.name)	# 去除指定列
session.query(User.id, User.name)

# 拼接
query2 = query.filter(User.id > 10)	# 拼接相当于AND
query2.filter(or_(User.id == 1))	# or操作

# 关联查询
query(User).join(Post, User.id == Post.user_id).all()	# join查询
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
```

### 插入

```python
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

