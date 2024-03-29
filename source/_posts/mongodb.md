---
title: "MongoDB 使用手册"
date: 2018-01-04 21:32:00
updated: 2022-04-10 12:33:00
categories: database
---

[mongodb在线语法测试](https://mongoplayground.net/): 这个是非常方便的验证语法的功能了

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

- Mongodb大版本之间差异比较大，最好安装最新版本，这是[Release Notes](https://docs.mongodb.com/manual/release-notes/)

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
mongo	# 进入命令行

db.serverStatus()	# 查询服务器状态，有几个重要的参数
## version: 当前实例所用的版本
## uptime: 实例运行时间，单位为妙

db.version()	# 查看数据库版本
show dbs	# 查看数据库列表
use xxx # 进入某个数据库
db.dropDatabase()	# 删除当前数据库

db.col.find().explain()	# 在语句后添加explain能够返回查询计划
db.col.find().explain("executionStats")	# 能够返回具体获胜额查询计划以及执行详情
```

### 集合命令

```shell
db.adminCommand({renameCollection: "db1.table1", "db1.table2"})	# 重命名集合

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

db.users.update({}, {$unset:{'name': ''}}, false, true)	# 删除集合中的某个字段
```

### 索引

- 索引相关，注意，ensureIndex在3.0已经弃用了，dropDup参数也弃用了
- 索引可以在数组字段上创建，这回给数组的每个元素都创建一个索引的

```shell
db.col.getIndexes()	# 获取当前collection的所有的索引
db.col.createIndex({"name": 1})	# 创建索引，1表示升序，-1表示降序
db.col.createIndex({"name": 1}, {unique: true})	# 索引规则，unique表示唯一索引，sparse对文档中不存在的字段数据不启用索引，默认是false，为true的话不会查询出不包含该索引的数据；expireAfterSeconds设定集合的生存事件；weights索引权重值；default_language设置索引的语言，默认是英语，zhs表示简体中文
db.col.createIndex({"content": "text"})	# 在content字段上创建全文索引
```

#### 全文索引text

- 全文索引会对每一个词建立一个索引(3.2版本开始才支持中文)

## CURD

`document`表示一条`json`数据

`col`表示一张`collection`的名称

### 查找数据

- 查询`_id`数据需要将字符串转换一下:`{_id: ObjectId('6008c69ecf118e2bfb1e4237')}`

```shell
db.col.find(query, {'createdAt': -1, 'name': 1})	# 其中第二个参数，指定哪些字段返回，不返回哪些字段
db.col.find()	# 返回所有数据
db.col.find().pretty()	# 返回格式化后的json数据
db.col.find().limit(10)	# limit操作
db.col.find().skip(10)	# 跳过前面10条数据
db.col.find().sort({"age": 1})	# 按照某个字段进行排序，1表示升序，-1表示降序
db.col.find({name:/.*abc.*/})	# 正则查找，LIKE查询
db.col.find(			# or 查询
	{
      $or: [
        {key1: value1}, {key2: value2}
      ]
	}
)
db.col.find({"age": {$gt: 24}})	# 大于，响应的还有$gte大于等于，$lt小于，$lte小于等于
db.col.find({"age": {$type: 2}})	# type操作符，找出type为字符串的数据，这个的话得去看对应关系了


# 查询是否存在
db.users.find({'friends': {$exists: true}})	# 查询存在friends字段的用户
db.users.find({'friends.0': {$exists: true}})	# 查询friends数组长度大于等于0的记录

# 聚合查询
db.col.aggregate(AGGREGATE_OPERATION)
db.col.aggregate({$lookup: {from:"users", "localField": "user_id", "foreignField": "_id", as: "user"}})

# 统计
db.col.count({})	# 统计数量
db.col.distinct('user_type')	# distinct操作，直接返回一个数组
db.col.distinct('friends.user_type')	# 可以对子对象进行distinct
db.col.distinct('friends.user_type', {gender: 'female'})	# 只distinct gender=female的friend

# $project映射，可以从结果中提取字段或者重命名字段
db.users.aggregate({
	"$project": {
		"name": 1,	# 要显示的字段
		"_id": 0	# 不要显示的字段
		"name1": "$name"	# 重命名字段
	}
})

# $unwind拆分，对于一对多的关系，如果直接用lookup进行联表查询，那得到的结果会是一个包含的数组，而如果用哦unwind则会像mysql那样得到的是平铺的结果，这样的结构可以再进行关联第三张表。示例: https://mongoplayground.net/p/y32f3W25Q83
db.users.aggregate([
	{"$lookup": {..., "as": "posts"}},
	{"$unwind": "$posts"},
	{"$match": {"posts.status": true}}, # 对连表的数据进行filter match
	{"$lookup": {..., "as": "posts.comments"}},	# 关联第三张表，注意这里的as一定要是关联的第二张表的as作为前缀
	{"$gruop": {
		"_id": "$_id",	 # 以第一张表的id作为group by的依据
		"name": {$first: "$name"},	# 其他的字段取第一个出现的就行了
    "posts": {$push: "$posts"},	# 对于一对多的字段，使用$push关键字
    "posts1": {$push: "$$ROOT"}, # 如果要把第一张表的信息都放进去可以使用$$ROOT
	}},	# 连接了三张表后因为做了一个unwind其实得到的结果是平铺的，但是做了一些连表操作后我们又想得到多层级的json格式的话得进行一次group操作
])
```

### 插入数据

- `insertMany`等好多操作都是3.2版本才开始的，

```shell
db.col.insert(document)	# 会返回一个WriteResult对象
db.col.insertMany([document1, document2])

# 3.0之前的insertMany
var bulk = db.settings.initializeUnorderedBulkOp();
bulk.insert({});
bulk.insert({});
bulk.insert({});
bulk.execute();
```

### 更新数据

```shell
db.collection.update(
	<query>,		# where条件，json格式
	{	# 更新对象以及更新操作符，json格式
		"$set": {
			"name": "test",
			"json_data": {"abc": 123},	# 更新整个JSON数据
			"json_data1.field1": {"abc": 123},	# 更新JSON数据的某个字段
		}
	},		
	{
      upsert: <boolean>,	# 可选(false)，如果为true，那么如果不存在该条数据则会插入新数据
      multi: <boolean>,		# 可选(false)，默认只更新找到的第一条记录，true表示更新全部
      writeConcern: <document>	# 可选，设置抛出异常的级别
	}
)

# update + where
db.col.update({'name': '123'}, {$set: {'title': 'Hello'}})	# 更新name=123的数据，将title更改为hello

# 对结果进行特定的更新操作
db.col.find({gender: 'male'}).forEach(function(obj){
	print(obj.age);
	obj.age = 10;
	db.col.save(obj);
	
	db.col2.find().forEach()	# 这里还能够嵌套
})

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
# 4.0以前可以使用这条命令直接复制数据库，但是那之后就只能用mongodump了
db.copyDatabse('old_name', 'new_name')
# 4.0以后用下面的命令复制数据库
mongodump --archive="mongodump-test-db" --db=test
mongodump --archive="mongodump-test-db" --nsFrom='test.*' --nsTo='examples.*'

# 备份/导出/export
mongodump -h 127.0.0.1:27017 --db DB_NAME --collection COLLECTION	# 备份某个集合
mongodump -d DB_NAME -o ./

# 恢复
mongorestore -h 127.0.0.1:27017 --db DB_NAME <path>	# dump文件夹的路径
```

## 其他功能

### Mongodb实现自增字段

- `MongoDB`没有原生的自增长功能，但是我们可以借助其原子性实现获取并设置自增字段的功能

1. 首先创建一个专门用于保存自增当前索引值的集合`counters`:

   ```json
   {
     "name": "my_table",
     "sequence_value": 1
   }
   ```

2. 创建一个获取并加一的函数

   ````javascript
   function getNextSequenceValue(sequenceName){
      var sequenceDocument = db.counters.findAndModify(
         {
            name: "my_table",
            update: {
              $inc:{sequence_value:1}	// 只要读取一次就自增一
            },
            "new":true
         });
      return sequenceDocument.sequence_value;
   }
   ````

3. 在创建`my_table`文档时只需要`id=getNextSequenceValue('my_table')`即可

## TroubleShooting

- **解决安装完mongo后无法启动的问题**: 遇到一个安装完成后无论是`mongo`还是`sudo service mongo start`还是`sudo systemctl start mongod`都不报错但是实际上却没有启动的问题，可以这样解决，如果还是不行，可以去看`/var/log/mongo`的日志，可能是磁盘空间不足引起的:

  ```shell
  rm -rf /tmp/mongodb-27017.sock /var/lib/mongodb/mongod.lock
  sudo systemctl start mongodb
  sudo service mongodb start	# 或者用这个启动
  ```
