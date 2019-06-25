---
title: "Spark & PySpark 使用手册"
date: 2019-05-22 21:32:00
updated: 2019-06-20 09:40:00
categories: 编程之路
---
最近公司有一个安全方面的业务，需要实时监控所有访客的情况。之前是定时去查询`Elasticsearch`的接口进行统计分析，但是这个时间间隔不好把握，并且`Elasticsearch`并不适合特别实时的查询操作。实时的分布式流计算引擎首推`Spark`，它与`Hadoop`等相比的优势在[这里](http://dblab.xmu.edu.cn/blog/1710-2/)讲得比较清楚了。

- **RDD(Resilient Distributed Dataset弹性分布式数据集)**：这是spark的主要数据概念。有多种来源，容错机制，并且能缓存、并行计算。RDD在整个计算流程中会经过不同方式的变换，这种变换关系就是一个有向无环图。
- 需要注意的是，所有的方法在定义执行之前都是异步的，所以不能简单地在下面的方法外部添加`try...catch...`进行异常捕获，最好是在传入的函数里面进行异常的捕获(如果是lambda，请确认lambda不会报错，否则如果lambda报错整个程序都会报错并终止允许)
- Spark应用程序可以使用大多数主流语言编写，这里使用的是python，只`pip install pyspark`即可
- **Stage(调度阶段)**: 每个Job会根据RDD大小切分城多个Stage，每个Stage包含一个TaskSet
- **TaskSet(任务集)**: 一组关联的Task集合，不过是没有依赖的
- **Task(任务)**: RDD中的一个分区对应一个Task。
- **Narrow Dependency(窄依赖)**: 比较简单的一对一依赖和多对一依赖(如union)
- **Shuffle Dependency(宽依赖)**: 父RDD的分区被多个子RDD分区所使用，这时父RDD的数据会被再次分割发送给子RDD
- **Spark 内存分配**: 分为这三块:
  - **execution**: 执行内存，基本的算子都是在这里面执行的，这块内存满了就写入磁盘。
  - **storage**: 用于存储broadcast, cache, persist
  - **other**: 程序预留给自己的内存，这个可以不用考虑

<!--more-->

### 基本运算

- 下面是所有运算方法的集合，其中有些方法仅用于键值对，有些方法仅用于数据流

#### Transformation(转换)

这类方法仅仅是定义逻辑，并不会立即执行，即lazy特性。目的是将一个RDD转为新的RDD。

- map(func): 返回一个新的RDD，func会作用于每个map的key，func的返回值即是新的数据。为了便于后面的计算，这一步一般在数据处理的最前面将数据转换为(K, V)的形式，例如计数的过程中首先要`datas.map(lambda a, (a, 1))`将数据转换成(a, 1)的形式以便后面累加
- mappartitions(func, partition): 和map不同的地方在于map的func应用于每个元素，而这里的func会应用于每个分区，能够有效减少调用开销，减少func初始化次数。减少了初始化的内存开销。但是map如果数据量过大，计算后面的时候可以将已经计算过的内存销毁掉，但是mappartitions中如果一个分区太大，一次计算的话可能直接导致内存溢出。
- filter(func): 返回一个新的RDD，func会作用于每个map的key，返回的仅仅是返回True的数据组成的集合，返回None或者False或者不返回都表示被过滤掉
- filtMap(func): 返回一个新的RDD，func可以一次返回多个元素，最后形成的是所有返回的元素组成的新的数据集
- mapValues(func): 返回一个新的RDD，对RDD中的每一个value应用函数func。
- distinct(): 去除重复的元素
- subtractByKey(other): 删除在RDD1中的RDD2中key相同的值
- groupByKey(numPartitions=None): 将(K, V)数据集上所有Key相同的数据聚合到一起，得到的结果是(K, (V1, V2...))
- reduceByKey(func, numPartitions=None): 将(K, V)数据集上所有Key相同的数据聚合到一起，func的参数即是每两个K-V中的V。可以使用这个函数来进行计数，例如reduceByKey(lambda a,b:a+b)就是将key相同数据的Value进行相加。
- reduceByKeyAndWindow(func, invFunc, windowdurartion, slideDuration=None, numPartitions=None, filterFunc=None): 与reduceByKey类似，不过它是在一个时间窗口上进行计算，由于时间窗口的移动，有增加也有减少，所以必须提供一个逻辑和func相反的函数invFunc，例如func为(lambda a, b: a+b)，那么invFunc一般为(lambda a, b: a-b)，其中a和b都是key相同的元素的value
- join(other, numPartitions=None): 将(K, V)和(K, W)类型的数据进行类似于SQL的JOIN操作，得到的结果是这样(K, (V, W))
- union(other): 并集运算，合并两个RDD
- intersection(other): 交集运算，保留在两个RDD中都有的元素
- leftOuterJoin(other): 左外连接
- rightOuterJoin(other): 右外连接

#### Action(执行)

不会产生新的RDD，而是直接运行，得到我们想要的结果。

- collect(): 以数组的形式，返回数据集中所有的元素
- count(): 返回数据集中元素的个数
- take(n): 返回数据集的前N个元素
- takeOrdered(n): 升序排列，取出前N个元素
- takeOrdered(n, lambda x: -x): 降序排列，取出前N个元素
- first(): 返回数据集的第一个元素
- min(): 取出最小值
- max(): 取出最大值
- stdev(): 计算标准差
- sum(): 求和
- mean(): 平均值
- countByKey(): 统计各个key值对应的数据的条数
- lookup(key): 根据传入的key值来查找对应的Value值
- foreach(func): 对集合中每个元素应用func

#### Persistence(持久化)

- persist(): 将数据按默认的方式进行持久化
- unpersist(): 取消持久化
- saveAsTextFile(path): 将数据集保存至文件

### 应用场景

#### 创建简单的RDD

```python
from pyspark.sql import SparkConf, SparkContext
rdd = sc.parallelize(['abc', def'])	// 直接创建rdd
```

#### 读取CSV文件

```python
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("test") \
    .config("spark.some.config.option", "一些设置") \
    .getOrCreate()

df = spark.read.csv("/home/Users/haofly/test.csv", header=True, sep="|")	# 读取文件
print(df.collect())
```

#### Spark Streaming流计算

- DStream(Discretized Stream, 离散化数据流): `Spark Streaming`主要的操作对象，表示连续不断的数据流。其大多数的操作方法与RDD的操作方法一样。
- 无法实现毫秒级的运算，可以通过`StreamingContext`的参数确定秒级间隔
- 可以从文件流、TCP套接字流、RDD队列流读取数据

##### 从文件流读取数据

```python
conf = SparkConf().setAppName("test").setMaster("local[2]")	# 表示运行在本地模式，并且启动2个工作线程
	.set('spark.streaming.kafka.maxRetries', '3')	# 定义找不到leader的重试次数
  .set('spark.streaming.kafka.maxRatePerPartition', '30000')	# 定义找不到leader的重试间隔
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 30)	# 每隔10秒钟自动进行一次流计算

lines = ssc.textFileStream('file:///Users/haofly/log')
words = lines.map(lambda line: line.strip())
words.pprint()
ssc.start()
ssc.awaitTermination()
```

##### 从kafka读取数据

首先得从[maven仓库](https://search.maven.org/search?q=spark-streaming-kafka)下载对应的版本，注意这里需要下载`assembly`的包，这里的2.11是scala的版本，2.4.3是pyspark的版本号，也是spark的版号，如果下载后的包不能用，那就尝试换一个版本吧。可以通过[这篇文章](https://haofly.net/kafka)搭建测试用的kafka集群。

- 需要注意的是针对kafka0.8和0.10版本，`spark`有不同的API，详细对比见https://spark.apache.org/docs/latest/streaming-kafka-integration.html

```python
# 指定spark-streaming-kafka的jar包
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--jars /test/jars/kafka/spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar pyspark-shell"

conf = SparkConf().setAppName("test").setMaster("local[2]")	# 表示运行在本地模式，并且启动2个工作线程
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 10)	# 每隔10秒钟自动进行一次流计算

zkQuorum, topic = "zookeeper:2181", "test"
# 通过zookeeper进行连接
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
# 直接连接kafka的broker
kvs = KafkaUtils.createDirectStream(ssc, 'topic', {
  "metadata.broker.list": "mybroker1:9092,mybroker2:9092"
  "group.id": "myproject"
})
lines = kvs.map(lambda x: x[1])

def myadd(a, b):	# 只能在传入的函数中捕获异常
  try:
	  return a+b
  catch:
    pass	# tolog

def myadd_inv(a, b):
  return a-b

rdd = lines.map(lambda x: (x, 1)).reduceByKeyAndWIndow(myadd, myadd_inv, 60)	# 统计时间窗口60秒内的数据
rdd.pprint()	# 每次统计都打印rdd的数据

ssc.start()		# 异步执行
ssc.awaitTermination()	# 等待终止信号
```

我的业务比较复杂，大致是既要统计域名的访问数量，又要统计访客IP的数量，即要统计1小时内的，又要和过去一小时的进行对比，所以我的转换是这样写的:

```python
# get_domain_and_ip_from_line返回的是(domain, ip)对
rdd = lines.map(get_domain_and_ip_from_line)	# 这里获取原始数据，下面会让它转换成1小时与2小时
rdd = rdd.map(lambda domain_ip: (domain_ip[0], {domain_ip[1]: 1}))	# 这里将数据转换成了(domain, {ip: 1})的形式，方便后面计数
one_hour_rdd = rdd.reduceByKeyAndWindow(domain_ip_add, domain_ip_add_inv, 60 * 60)	# 这里的domain_ip_add有点儿复杂就不写了，大致就是生成域名下的IP统计列表("domain", {"ip1": 123, "ip2": 233, "TOTAL": 356})
two_hour_rdd = rdd.reduceByKeyAndWindow(domain_ip_add, domain_ip_add_inv, 60 * 120)
result = one_hour_rdd.join(two_hour_rdd)
result.pprint()
result.filter(filterFunc)
```

#### 读取图片数据源

Spark2.4开始支持直接将图片作为数据源

```python
val df = spark.read.format("image").load("/images/")
```

### pyspark依赖打包任务提交

如果说只是`local`模式运行，那么是不需要打包，但是如果计算量超级大，一般都是会提供一个集群去运行，这时候需要使用`spark-submit`命令将命令提交到集群。但是如果python项目并不是单文件并且有外部依赖，那么就需要将依赖以及项目都打包后再进行提交。例如我的代码目录如下，程序入口在`main.py`，有部分帮助方法在`utils`目录下。直接把依赖的第三方库`requests`的源码从python运行环境的`site-packages`中复制到项目 目录中，最后将`utils、requests`一起压缩成一个`zip`文件:

```shell
.
├── utils
    ├── __init__.py
    └── ...  
├── main.py
└── requests
    ├── __init__.py
    └── ...  
```

另外，如果依赖非常多，那么可以将代码目录直接移动到`site-packages`下(注意不要和原有依赖重名，并且`pyspark`这个依赖是不用的)。如果有一些依赖是非纯Python的实现，例如`Crypto`加解密相关的依赖，即使本地能跑放上去也可能出现各种问题，例如`Cannot load native module 'Crypto.Cipher._raw_ecb'`，这种时候在尝试多次不行后还是去找找纯Python的实现吧，唉，说多了都是泪。

这里以`yarn`集群为例，提交命令如下，需要注意的是，如果命令行和代码里面都进行了设置，根据我的经验应该是默认以命令行提供的参数为准。

```shell
/usr/local/spark2-client/bin/spark-submit  
	--name my-test-project  
	--master yarn # 设置master
	--deploy-mode cluster 
	--num-executors 2 
	--driver-memory 2g 
	--executor-memory 2g 
	--executor-cores 2 
	--jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar # 这个参数在代码里面设置是不行的
	--py-files test.zip 	# 指定打包后的依赖文件
	main.py	# 指定主程序文件
```

##### TroubleShooting

- **py4j.protocol.PyAJNetworkError: Answer from Java side is empty**: 默认的使用的内存为1G，无论你有没有这么大
- **TypeError: 'JavaPackage' object is not callable**: 如果是使用`spark-submit`命令进行任务的提交，那么在程序内部指定`spark-streaming-kafka-0-8-assembly`路径就不行了，必须给`spark-submit`命令添加上参数(注意版本):`--jars spark-streaming-kafka-0-8-assembly_2.11-2.0.2.jar`

##### 扩展阅读

[Spark 2.2.x 中文官方参考文档](https://spark-reference-doc-cn.readthedocs.io/zh_CN/latest/index.html)

[子雨大叔据之Spark入门教程(Python版)]([http://dblab.xmu.edu.cn/blog/1709-2/](http://dblab.xmu.edu.cn/blog/1709-2/))

[Spark性能优化指南——基础篇](https://tech.meituan.com/2016/04/29/spark-tuning-basic.html)

[Spark性能优化指南——高级篇](https://tech.meituan.com/2016/05/12/spark-tuning-pro.html): 解决数据倾斜(通常出现在distinct、groupByKey、reduceByKey、aggregateByKey、join、cogroup、repartition)的几个方案。

