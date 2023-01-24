---
title: "SQLAlchemy手册"
date: 2017-11-15 22:51:39
updated: 2023-01-19 23:11:00
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

DBSession = sessionmaker(bind=engine, autocommit=True)	# 创建DBSession类型，可视为当前数据库的连接
session = DBSession()	# 创建一个session对象

# session基本操作
new_user = User(id='1', name='haofly')	# 新建一个User对象
session.add(new_user)
session.commit()	# 提交
session.close()		# 关闭session
```

需要注意的是，如果没有修改autocommit的默认值(False)，那么一个session会一直保持，直到该session被回滚、关闭、提交才结束。每次发起请求，都创建一个新的session(注意不是创建新的连接，创建session并不会有多大的开销)，一个session就是一个transaction的支持。我们可以让session是一个全局的对象，这样和数据库通信的session在任何时候只有一个，但是全局的session不是线程安全的，如果多线程的情况下，可能会造成commit错乱，`tornado`这种单线程程序由于其异步的特性也不可以那样做(Tornado可以在每个`Handler`的初始化进行session的创建与提交销毁)。当然，如果是在单线程的情况下，我们完全可以保持session的单例，减少一丢丢的开销。下面这种方式对于多线程还是单现成都是非常推荐的做法：

```python
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=some_engine)
Session = scoped_session(session_factory)	# 为了保证线程获得的session对象是唯一的
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
nullable=False	# 是否可为空，默认为True
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

- 像`join`自身类似的需求，可以使用别名`user_model1 = aliased(UserModel)`

- 目前没有找到合适的方法去返回影响的行数，但是在`UPDATE/DELETE`方法中可以使用`result.rowcount`来返回SQL中where语句匹配到的行数，折衷方案是可以多加一个where条件去返回实际的影响行数。

- 执行原生语句，返回的是`ResultProxy`对象:

  ```python
  result = conn.execute("INSERT INTO user (name) VALUES ('haofly')")
  result = conn.execute("INSERT INTO user (name) VALUES ('haofly') RETURNING id")	# 插入并拿到插入的id
  result.fetchall()
  ```

- 执行原生语句的时候，防止SQL注入:

  ```python
  bind_sql = 'SELECT * FROM xxx WHERE field = :value'
  session.execute(bind_sql, {'value': 'value1'})
  
  # 或者用下面的方式插入一个字典或者列表
  session.execute(MyModel.__table__.insert(), modelDict)
  session.execute(MyModel.__table__.insert(), modelDicts)
  ```

### 查询

- `filter_by`只能用`=`，而`filter`可以用`==,!=`等多种取值方式，且必须带表名

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
    getattr(User, 'icon_id') == 3,	# 通过字段名的字符串形式获取属性
    User.id==2, 
   	User.age>10, # 大于、小于、等于直接写
    User.deleted_at == None, # IS NULL用None代替
    User.name.in_(['hao', 'fly'])	# IN操作
).first().name
query.filter('id = 2').first()	# 复杂的filter
query.filter_by(deleted_at == None)	# flask-sqlalchemy的查询方式
query.order_by('user_name').all()		# 排序
query.order_by(desc('name')).all()		# 倒序排序，from sqlalchemy import desc

# 使用功能函数
query(func.count('*')).all()
query(func.json_contains(User.age, '{"A":"B"}')).all()	# 使用JSON_CONTAINS

# 查询列
session.query(User.name)	# 去除指定列
session.query(User.id, User.name)
session.query.with_entities(User.id, User.name)	# 获取指定列

# 拼接
query2.filter(or_(User.id == 1))	# or操作，or ...
query2.filter(or_(User.id == 1, User.name.like('')))	# or操作，or (xxx AND xxx)

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
MyModel.query.filter(User.name.like('%hao%'))
```

### 插入

- 注意在连接数据库时`autoflush`参数默认为`True`，但是并不是`add`之后就自动将语句`flush`到数据库，而是指每次查询前回自动`flush`，所以无论`autoflush`是否为`True`，`add`之后都需要手动`session.flush()`

```python
session.add(User(name='haofly'))	# 直接插入一条数据
session.flush()	# 必须手动flush

# 批量插入ORM版
session.bulk_save_objects([User(name="wang") for i in xrange(1000)])

# 批量插入非ORM版
result = session.execute(
    User.__table__.insert(),
    [{'name': 'wang', 'age': 10}, {}]
)
session.commit()

result.lastrowid	# 获取上一次插入的主键id
modelobj.id	# 如果是ORM，那么直接在add后获取主键id值就行了
```

### 修改

```python
query.filter(...).update({User.age: 10})
session.flush()

user.name = 'new'
session.commit()
```

### 删除

```python
session.delete(user)
session.flush()
```

### 自定义SQL构造

```python
# 在所有的Insert语句前加上指定的前缀/后缀，例如加上ON DUPLICATE KEY UPDATE。例如下面这个例子，当传入append_string参数时会将指定的字符串添加到后面
from sqlalchemy.sql.expression import Insert

@compiles(Insert)
def prefix_inserts(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'append_string' in insert.kwargs:
        return s + " " + insert.kwargs['append_string']
    return s
  
session.execute(MyModel.__table__.insert(append_string = 'ON DUPLICATE KEY UPDATE fieldname="abc"'), objects)
```

### 其他

```python
session.rollback()	# 回滚
session.commit()	# 提交
```

## Event事件

### Attribute Events属性相关事件

```python
append/bulk_replace/dispose_collection/init_collection/init_scalar/modified/remove/set
```

###Mapper Events

都无法获取请求context，接收的参数仅仅是Mapper、Connection、Target(目标model对象)

```python
after_configuree/after_delete/after_insert/after_update/before_configured/before_delete/ 
before_insert/before_update/instrument_class/mapper_configured
```

例如

```python
@event.listens_for(Test, 'after_update')
def receive_after_update(mapper: Mapper, connection: Connection, target: Test):
    print('receive_after_update')

    state = inspect(target)
    # model能够记住自己的历史状态，所以这里可以直接获取哪些字段被更改了
    for attr in state.attrs:
        hist = attr.load_history()
        if hist.has_changes():
            print('change ' + attr.key + ' from ' + str(hist.non_added()[0]) + ' to ' + str(hist.non_deleted()[0]))
```

### Instance Events

```python
expire/first_init/init/init_failure/load/pickle/refresh/refresh_flush/unpickle
```

### Session Events

```python
after_attach/after_begin/after_bulk_delete/after_bulk_update/after_commit/after_flush/after_flush_postexec/after_rollback/after_soft_rollback/after_transaction_create/after_transaction_end/before_attach/before_commit/before_flush/deleted_to_detached/deleted_to_persistent/detached_to_persistent/loaded_as_persistent/pending_to_persistent/pending_to_transient/persistent_to_deleted/persistent_to_detached/persistent_to_transient/transient_to_pending
```

## TroubleShooting

- **Tornado中使用SQLAlchemy连接SQLite进行commit操作的时候程序中断: Segment Fault**: 原因是`SQLite`的自增主键`id`重复了😂
- **UnicodeEncodeError：'latin-1' codec can't encode characters in position 0-1: ordinal not in range(256)**: 连接数据库没有指定utf8的charset，参考本文连接数据库设置。
- **UnicodeEncodeError: 'ascii' codec can't encode characters in position 7-8: ordinal not in range(128)**: 除了上面那种可能，还有种可能是直接把含有中文的json对象拿来给model的字符类型赋值了
- **Can't recoonect until invalid transaction is rolled back**: 要么在每次执行sql语句之后主动close，要么在连接的时候设置`autocommit=True` 
- **MySQL server has gone away**: 程序运行久了出现该问题。如果是使用了线程池，那么可能的原因是线程池的回收时间大于了mysql的最长交互时间(可使用`SHOW VARIABLES LIKE '%interactive_timeout%';`查看)。这个时候可以把`POOL_RECYCLE`参数设置为比那个时间小就行了。
- **2013 Lost connection to MySQL server during query**: 原因是超过了`wait_timeout`规定的时间了，首先`show GLOBAL variables LIke '%wait_timeout%'`看看全局的超时时间是多少(这里一定要先看GLOBAL的，因为当前session的会首先被全局的影响)，这种情况，尽量优化sql，实在不行再修改这个配置。
- **SqlAlchemy实现ON DUPLICATE KEY UPDATE**: 目前没找到ORM的实现方式，但是有相对[复杂的方式](https://stackoverflow.com/questions/6611563/sqlalchemy-on-duplicate-key-update)，更简单的方式是直接执行原生语句，在后面添加`ON DUPLICATE KEY UPDATE`即可。可以参见上面的自定义SQL构造方法。

##### 扩展阅读

[SQLAlchemy 的 scoped_session 是啥玩意](https://farer.org/2017/10/28/sqlalchemy_scoped_session/)

