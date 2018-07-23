---
title: "MongoDB 使用手册"
date: 2018-01-04 21:32:00
updated: 2018-07-21 11:33:00
categories: database
---

MongoDB是由C++语言编写的一个基于分布式文件存储的开源数据库。推荐的GUI管理工具[Robo 3T](https://github.com/Studio3T/robomongo)。MongoDB将Json的数据存储为一个文档，但并不是我们能直接读取的普通文件。

基础概念:

- 数据库: 与Mysql的数据库类似
- collection: 与Mysql的`table`类似，集合
- document: 与MySQL的行`row`类似
- field: 与MySQL的列`column`类似
- index: 索引
- primary key: 主键，默认主键是`_id`

## 应用场景

- 爬虫的数据存储，由于多个爬虫爬取数据时字段不统一，用mysql很容易浪费字段

<!--more-->

## 安装配置

[官方安装文档](https://docs.mongodb.com/master/tutorial/install-mongodb-on-red-hat/)

```shell
sudo service mongod start	# 安装完成后启动
sudo systemctl enable mongod	# 加入开机启动

# 设置强制密码访问，首先使用mongo命令进入命令行，然后use admin选择admin这个数据库，在这里新建一个用户，最后配置文件中开启authorization
db.createUser({user: 'root', pwd: 'password', roles: ['root'], mechanisms : ["SCRAM-SHA-1"]})

# vim /etc/mongod.conf	修改相关配置项，这其实是一个yaml文件，需要严格遵守文件格式
net:
  port: 27017
  bindIp: 0.0.0.0	# 允许远程访问
security:
  authorization: enabled # 设置强制密码验证
```

## 系统相关指令

```shell
db.col.stats() 	# 查询当前collection状态，参数如下
ns: 集合的命名空间
count: 集合中的文档总数
size: 占用空间大小，不包括索引，单位为字节
avgObjSize: 平均一个对象占用空间的大小
storageSize: 给整个集合分配的存储空间，如果文档被删除，该值并不会下降
nindexes: 索引个数
totalIndexSize: 所有索引的大小
indexSizes: 所有的索引以及其大小

db.col.status(1024)	# 这样下面那些大小单位就是KB

# 索引相关，注意，ensureIndex在3.0已经弃用了，dropDup参数也弃用了
db.col.createIndex({"name": 1})	# 创建索引，1表示升序，-1表示降序
db.col.createIndex({"name": 1}, {unique: true})	# 索引规则，unique表示唯一索引，sparse对文档中不存在的字段数据不启用索引，默认是false，为true的话不会查询出不包含该索引的数据；expireAfterSeconds设定集合的生存事件；weights索引权重值；default_language设置索引的语言，默认是英语，zhs表示简体中文
db.col.createIndex({"content": "text"})	# 在content字段上创建全文索引
```

## CURD

`document`表示一条`json`数据

`col`表示一张`collection`的名称

### 查找数据

```shell
db.col.find(query, projection)	# 其中第二个参数，是使用投影操作符指定返回的键
db.col.find()	# 返回所有数据
db.col.find().pretty()	# 返回格式化后的json数据
db.col.find().limit(10)	# limit操作
db.col.find().skip(10)	# 跳过前面10条数据
db.col.find().sort({"age": 1})	# 按照某个字段进行排序，1表示升序，-1表示降序
db.col.find({name:/abc/})	# 正则查找
db.col.find(			# or 查询
	{
      $or: [
        {key1: value1}, {key2: value2}
      ]
	}
)
db.col.find({"age": {$gt: 24}})	# 大于，响应的还有$gte大于等于，$lt小于，$lte小于等于
db.col.find({"age": {$type: 2}})	# type操作符，找出type为字符串的数据，这个的话得去看对应关系了
db.col.find({}, {"age": 1})	# projection中的inclusion模式，包含哪些键
db.col.find({}, {"age": 0})	# projection中的exclusion模式，不包含哪些键

# 聚合查询
db.col.aggregate(AGGREGATE_OPERATION)

# 统计
db.col.count({})	# 统计数量
```

### 插入数据

```shell
db.col.insert(document)	# 会返回一个WriteResult对象
```

### 更新数据

```shell
db.collection.update(
	<query>,		# where条件，json格式
	<update>,		# 更新对象以及更新操作符，json格式
	{
      upsert: <boolean>,	# 可选(false)，如果为true，那么如果不存在该条数据则会插入新数据
      multi: <boolean>,		# 可选(false)，默认只更新找到的第一条记录，true表示更新全部
      writeConcern: <document>	# 可选，设置抛出异常的级别
	}
)

# 例如
db.col.update({'name': '123'}, {$set: {'title': 'Hello'}})	# 更新name=123的数据，将title更改为hello

# 通过传入的文档来替换已有的文档
db.collection.save(
	<document>,
	{
      writeConcern: <document>
	}
)
```

### 删除数据

```shell
db.collection.remove(
	<query>,
	{
      justOne: <boolean>,
      writeConcern: <document>
	}
)
```

## 备份与恢复

```shell
# 备份
mongodump -h 127.0.0.1:27017 --db DB_NAME --collection COLLECTION	# 备份某个集合

# 恢复
mongorestore -h 127.0.0.1:27017 --db DB_NAME <path>	# dump文件夹的路径
```

