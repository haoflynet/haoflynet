api 文档地址http://docs.sqlalchemy.org/en/latest/contents.html



创建连接

```
engine = create_engine('sqlite:////var/www/homepage/blog.db?check_same_thread=False')
```

CRUD

查询语句

query = session.query(User)

print(query)	# 只显示sql语句，不会去查询

query.all()

query.first()

for user in query

user =q uery.get(1)

query.filter(User.username='wang').all()

query.order_by('user_name').all()

query(func.count('*')).all()

