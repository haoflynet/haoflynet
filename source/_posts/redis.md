---
title: "redis 手册"
date: 2016-04-11 11:02:40
updated: 2022-11-15 16:32:00
categories: database
---
注意，Redis是单线程的，运行耗时任务时，会阻塞，导致不能响应其他的请求(对于耗时大的删除任务, Redis4.0提供lazy free功能)。

## 配置文件

**如果是线上，可以用rename机制禁用一些命令例如keys、flushall、flushdb**

在redis shell外部，可以通过命令行的方式获取或者设置一些配置，例如:

```shell
redis-cli config set notify-keyspace-events KEA  # 可以直接设置notify-keyspace-events的信息
```

常用配置:
```shell
hz = 10  # 表示每秒检查过期键的次数
save 900 1       # 数据写入硬盘的频率，表示如果900秒内有1个key发生变化就写入一次，300秒内有10个key发生变化写入一次，60秒内10000个key发生变化写入一次
save 300 10
save 60 10000
bind 127.0.0.1   # 绑定IP，表示只有该IP能够连接到该redis，默认所有IP均能连
requirepass 密码 # 访问需要密码
```

<!--  more -->

#### 内存满了的策略

当`redis`使用的内存超过`maxmemory`参数的时候，`maxmemory-policy`这个策略就开始生效了。默认是`noeviction`(不删除键，只返回错误)，可以设置其他的策略如下(LRU算法及最近最少使用算法):

```shell
volatile-lru: 使用LRU算法删除一个键（只对设置了生存时间的键）
volallkeys-lru	使用LRU算法删除一个键
volatile-random	随机删除一个键（只对设置了生存时间的键）
allkeys-random	随机删除一个键
volatile-ttl	删除生存时间最近的一个键
noeviction	不删除键，只返回错误
```

## 查看信息

`info`命令可以查看redis的所有信息，常用的字段如下:

```shell
# Memory	内存信息
used_memory_human: 就是当前Redis所使用的内存
used_memory_peak_human：Redis的内存消耗峰值

# Keyspace
db0:keys=100,expires=1,avg_ttl=7298 # 数据库0，设置了生存时间的key有1个，平均过期时间是7298ms

# stats 记录一般的统计信息
total_connections_received：服务器已经接受的连接请求数量
total_commands_processed：服务器已经执行的命令数量
instantaneous_ops_per_sec：服务器每秒钟执行的命令数量
rejected_connections：因为最大客户端数量限制而被拒绝的连接请求数量
expired_keys：因为过期而呗自动删除的数据库建数量
```

## 常用操作
### 系统

```shell
# redis-cli
redis-cli -h 127.0.0.1 -p 6379 -a password	# 连接服务端
client list		# 列出所有的客户端连接，客户端的IP
client kill 127.0.0.1:44444 # 断开某个连接

# redis-cli --bigkeys	查看redis中非常大的key
```

### 通用

- **严禁在生产环境使用`keys *`进行搜索，因为这表命令会引发Redis锁，导致其他查询不可用，如果真有类似业务，可以使用scan命令**
- `setnx`常用于分布式锁，建议将`value`设置为一个随机字符串，而不是无意义的"OK"啥的，因为这样在释放锁的时候可以验证一下是否释放的是正确的锁

```shell
SETNX	key value	# 将键key的值设置为value，如果key不存在则set成功返回1，如果key存在，则设置不成功返回0，常用与锁中
SET key value	EX 10 PX 10000 NX# 原始SET命令后面其实也可以跟很多参数的，EX表示多少秒后过期，PX表示多少毫秒后过期，NX相当于SETNX，XX表示只有键盘存在时才设置

flushall	# 删除所有数据库的key
flushdb		# 删除当前数据库所有的key
del key		# 删除某个key
redis-cli KEYS *name* | xargs redis-cli DEL	# 使用通配符进行批量删除操作

select 2	# 切换数据库

key name	# 查找某个key
keys pattern	# 查找所有符合给定模式pattern 的key
keys * 		# 列出所有的key
exists key	# 查找该key是否存在
TYPE KEY	# 获取某个key的类型

scan 0	# 使用游标的方式取出一定数量的redis key，与keys不同的是，keys是一次性全部扫描

expire key seconds	# 为某个key指定生存时间，单位为秒，时间到了后就不存在了，默认时间为永久
ttl key		# 查看剩余生存时间
```

### 字符串

### 列表

```shell
lindex keyname index              # 返回列表中下标为index的元素
lpush keyname value value2	# 将一个或多个值插入到表头
lpush keyname value [value ...]    # 将一个或多个值插入表头
lpushx keyname value [value ...]   # 当且仅当key存在且是一个列表时插入表头
rpush keyname value               # 插入表尾
rpushx keyname value              # 当且仅当key存在且是一个列表时插入表尾
lrem key count value			# 从列表删除元素，其中count>0时表示从头往尾移除count个值为value的元素，count为0时表示移除所有，count<-1时则是从尾往头移除
lrange keyname start count        # 从表头的第start位开始取出count个元素
llen keyname                      # 返回列表长度
lpop keyname                      # 移除并返回key的头元素
rpop keyname                  # 移除并返回key的尾元素
lset key index value       # key中下标为index的元素的值设置为value，如果key不存在则会报错no such key
LTRIM key start stop	# 只会保留列表从左往右的start至stop数量的元素
```

### 集合(SET)

```shell
SADD key member [member...]
SMEMBERS key 	# 返回集合key中的所有成员
SISMEMBER key member	# 判断集合key中是否存在成员
```

### 有序集合(ZSET)

- 需要注意`start/stop`和`min/max`的区别，一个是排序后的顺序，一个是score值
- 最大分数值可以用`"+inf"`代替，最小分数值可以用`"-inf"`代替

```shell
ZADD key score member	# 像有序集合中添加元素
ZCARD key	# 返回有序集合的成员数量
ZCOUNT key min max	# 返回有序集key中，score值在min和max之间的成员数量
ZRANGE key start stop [WITHSCORES]	# 返回有序集key中，指定区间内的成员，其中成员的位置按score值递增(从小到大)来排序
ZRANGEBYSCORE key min max # 返回有序集key中，所有score值在min和max之间的成员
ZREM key member	# 移除指定元素
ZREVRANGEBYSCORE key max min	# 与上面相反，这是分数由高到低排列的
```

### Hash(哈希)

```shell
HKEYS key	# 取出哈希表key中所有的域
HEXISTS key field	# 判断field是否存在于hash中
HMGET key field [field...]	# 取出某个key指定域的值
HSET key field value	# 将hash表key中的域field的值设为value，如果key不存在则会新建，返回结果为1，如果已有field则会覆盖，返回结果为0
HSETNX key field value	# 只在 key 指定的哈希集中不存在指定的字段时，设置字段的值。成功返回1，如果已经存在field，那么会失败返回0
HMSET key field value [field value ...]	# 同时将多个field-value(域-值)对设置到哈希表key中，会覆盖哈希表中已存在的域
HINCRBY key field increment	# 将hash key中的域field增加increment，如果没有key则会新建key，如果没有域则默认为0并增加increment
HGETALL key	# 取出hash表中所有的域和值
HVALS key	# 取出哈希表key中所有域的值
```

## 过期策略

根据官方文档，redis对于过期的键有两种策略(过期的键并不会立马执行删除操作)，分为主动与被动:

1. 客户端试图去获取某个key的时候就会直接进行过期删除操作
2. 由服务器去探测，探测方案如下(每秒执行10次下面的操作):  
   1. 从设置了过期时间的所有key中随机取20个键
   2. 删除实际上已经过期了的键
   3. 如果删除的超过了已过期键的25%，重复前面的操作

如果想看效果，那么可以设置100000个过期时间很大的键，再设置一个过期时间很短的键，并开启键空间通知，你就知道多久才会发现那个键了😭，不过，如果全部时间多一样，那100000个键也能在瞬间完成所有通知，也就是说，每次扫描出来的20个键如果都满足第三条要求，那连续探测的频率是非常高的。检测频率可通过`hz`进行设置，默认为20

## Keyspace notifications(键空间通知)
键空间通知，允许Redis客户端从“发布/订阅”通道中建立订阅关系，让客户端能够从Redis中接收到相应的事件。`redis-cli config get notify-keyspace-events`获取其配置值，如果value为空表示没有设置。可以直接用命令设置如:`redis-cli config set notify-keyspace-events KEA`其中，最后面的字符，每个字符都有特殊的含义:

- K: 键空间通知，所有通知以__keyspace@<db>__为前缀
- E: 键事件通知，所有通知以__keyevent@<db>__为前缀
- g: DEL、EXPIRE、RENAME等类型无关的通用命令的通知
- $: 字符串命令的通知
- l: 列表命令的通知
- s: 集合命令的通知
- h: 哈希命令的通知
- z: 有序集合命令的通知
- x: 过期事件: 每当有过期键被删除的通知
- e: 驱逐(evict)事件: 每当有键因为maxmemory政策被删除的通知
- A: 所有通知

使用方法:

```shell
> config set notify-keyspace-events Ex	# 必须加E，这样才会通知事件
第一个终端进行监听:
> PSUBSCRIBE __keyevent@0__:expired

第二个终端进行操作
> set a b EX 1

这样第一个终端就会输出过期的键值
```
## Redis组件

Redis从4.0开始支持组件的开发，能为redis提供更多实用的定制功能，热门组件可以参考[Redis Modules](https://redis.io/modules)

## Redis数据库设计

- 统计聚合情况

  例如，需要统计PV数量，精确到分钟，但是又有按小时、按天、按星期统计的需求，那么可以使用hash来进行聚合统计，例如这样设计

  ```shell
  pv:post:id = {	 # 这是key值
  	'2016-08-22': 2333	# 按天统计
  	'2016-08-22:15': 23	# 按小时统计
  }
  pv:post:id:2016-08-22:15:list = []	# 那一个小时每分钟的数据，作为一个列表
  ```

## Redis Sentinel高可用方案

## Redis Cluster集群方案

和`redis sentinel`不同的是，前者主要是高可用，每一个机器都保存完整的数据，而cluster则住重在分片，当内存占用大于每台机器实际内存时候更实用。Python连接Redis集群需要使用`redis-py-cluster`

## TroubleShooting

* **小数据量本地迁移数据**

  网上找到的Redis的迁移方法都是从一个服务器至另一个服务器做主从复制，但我现在面临的情况是如何将localhost的数据迁移到Server上面去，用最笨也最简单的方法，直接将dump.rdb覆盖服务器上Redis目录，需要注意的是，覆盖的时候得先把原Redis进程关闭掉，覆盖后再重启

* **Redis 显示中文**

  启动时`redis-cli --raw`

* **windows长时间运行出现错误:`Redis-Server:Windows is reporting that there is insufficient disk spaceavailable for this file (Windows error 0x70)`**。原因是分配的堆栈太小了，默认的应该只有1M，这时候需要修改器配置文件`redis.windows.conf`，修改`maxheap`的值为2000000000，即2G

* **Redis自动退出，log无报错**: 目前遇到的情况是可能连接数过高。操作系统让它挂掉了

* **MISCONF Redis is configured to save RDB snapshots, but it is currently not able to persist on disk. Commands that may modify the data set are disabled, because this instance is configured to report errors during writes if RDB snapshotting fails (stop-writes-on-bgsave-error option). Please check the Redis logs for details about the RDB error.**持久化的时候磁盘不可写了，一般是因为磁盘满了

##### 扩展阅读

- [使用Redis锁处理并发问题](https://haofly.net/redis-lock-handle-concurrency)

