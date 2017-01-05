---
title: "redis 教程"
date: 2016-04-11 11:02:40
categories: database
---
# Redis

## 配置文件
在redis shell外部，可以通过命令行的方式获取或者设置一些配置，例如:

	redis-cli config set notify-keyspace-events KEA  # 可以直接设置notify-keyspace-events的信息

常用配置:
	hz = 10  # 表示每秒检查过期键的次数
	save 900 1       # 数据写入硬盘的频率，表示如果900秒内有1个key发生变化就写入一次，300秒内有10个key发生变化写入一次，60秒内10000个key发生变化写入一次
	save 300 10
	save 60 10000
	bind 127.0.0.1   # 绑定IP，表示只有该IP能够连接到该redis，默认所有IP均能连
	requirepass 密码 # 访问需要密码

## 查看信息
`info`命令可以查看redis的所有信息，常用的字段如下:

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

## 常用操作
## 通用

```shell
flushall	# 删除所有数据库的key
flushdb		# 删除当前数据库的key
del key		# 删除某个key

key name	# 查找某个key
keys pattern	# 查找所有符合给定模式pattern 的key
keys * 		# 列出所有的key
exists key	# 查找该key是否存在

expire key seconds	# 为某个key指定生存时间，单位为秒，时间到了后就不存在了，默认时间为永久
ttl key		# 查看剩余生存时间
```

### 字符串

### 列表

```shell
lpush keyname value value2	# 将一个或多个值插入到表头
     lpush keyname value [value ...]    // 将一个或多个值插入表头
  lpushx keyname value [value ...]   // 当且仅当key存在且是一个列表时插入表头
  rpush keyname value               // 插入表尾
  rpushx keyname value              // 当且仅当key存在且是一个列表时插入表尾
  lrange keyname start count        // 从表头的第start位开始取出count个元素
  lindex keyname index              // 返回列表中下标为index的元素
  llen keyname                      // 返回列表长度
  lpop keyname                      // 移除并返回key的头元素
  rpop keyname                      // 移除并返回key的尾元素
  lset key index value              // 将key中下标为index的元素的值设置为value
```

### 集合

```shell
SADD key member [member...]
SMEMBERS key # 返回集合key中的所有成员
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

	> config set notify-keyspace-events Ex	# 必须加E，这样才会通知事件

	第一个终端进行监听:
	> PSUBSCRIBE __keyevent@0__:expired
	
	第二个终端进行操作
	> set a b EX 1
	
	这样第一个终端就会输出过期的键值

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

## TroubleShooting

* **小数据量本地迁移数据**

  网上找到的Redis的迁移方法都是从一个服务器至另一个服务器做主从复制，但我现在面临的情况是如何将localhost的数据迁移到Server上面去，用最笨也最简单的方法，直接将dump.rdb覆盖服务器上Redis目录，需要注意的是，覆盖的时候得先把原Redis进程关闭掉，覆盖后再重启

* **Redis 显示中文**

  启动时`redis-cli --raw`







​    
​    
​    
    6. 排序操作：排序、分页等

          sort key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE destination]
      sort keyname alpha           // 将keyname里面的值按字符排序
      sort keyname alpha limit 0 3 // 讲keyname的值按字符排序并取得前面3个元素返回
      # 如果是在laravel里使用
      Redis::sort('keyname', array('ALPHA' => TRUE));
      Redis::SORT('keyname', array('LIMIT' => array(0, 3));
      j
    
    7. 字符串操作
    
          set key value    // 设置key值为字符串value，会直接覆盖旧值
    
    8. 列表的操作


​    
    9. hash的操作
    10. 集合的操作
    ---
    title: "Windows安装Redis教程"
    date: 2014-12-23 16:53:31
    categories: Redis
    ---
    [Redis](http://redis.io/)：是一个完全免费开源的遵守BSD协议的内存数据库。它和memcache类似，都说是键值对存储，但是它支持更
    多的数据结构，比如字符串、哈希、列表、集合和有序集合等。这里不做详细介绍，只介绍在windows上的安装过程。
    
    环境：Windows 7 64（需要注意的是windows只有64位版本）
    
    # 1.下载
    
    Redis并不直接支持windows，起windows版本是由微软开源团队维护的，可直接到github主页：<https://github.com/MSOp
    enTech/redis>，但不要直接下载zip，里面没有windows的zip包的，应该将整个项目完整clone下来。  
    ![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-redis_0.jpg)  
    
    # 2.解压
    
    其他的都是项目文件，但真正可以在windows下使用的是`/bin/redis/redis-2.8.17.zip`里面，解压后会发现这样有这样几个文件，当然
    ，也可以把这个目录添加到系统的环境变量，以便随时在bash中使用  
    ![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-redis_2.jpg)  
    其中，redis-server.exe就是主程序，redis-cli.exe是命令行工具，redis.windows.conf是配置文件
    
    # 3.测试
    
    执行`redis-server.exe redis.windows.conf`开启Redis服务：  
    
    ![](http://7xnc86.com1.z0.glb.clouddn.com/redis.jpg)  
    然后，windows里面貌似没有把它作为daemon的配置选项，不过，应该没人会在自己的windows里把它作为daemon，只是偶尔开发的时候会使用，所以
    ，另外开一个bash吧，执行以下命令进行测试：



        $ redis-cli.exe
        127.0.0.1:6379> set wang hao
        OK
        127.0.0.1:6379> keys *
        1) "wang"
        127.0.0.1:6379
    
    这就表示成功了，其中，Redis的相关命令中文参考文档可以查看[Redis命令参考简体中文版](http://redis.readthedocs.org/e
    n/2.4/)
    
    4.基本配置
    
    在windows下Redis运行久了，可能会出现如下错误：
    
    _Redis-Server:Windows is reporting that there is insufficient disk space
    available for this file (Windows error 0x70)._
    
    原因是分配的堆的大小太小了，默认的是多少忘了，只有1M还是多少，这时候需要修改其配置文件`redis.windows.conf`，修改maxheap的值为2
    000000000，即2G
