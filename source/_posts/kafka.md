---
title: Kafka 教程
date: 2016-12-23 11:20:44
updated: 2019-07-15 17:42:00
categories: tools
---


## 重要概念

### 生产者(Producer)

### 消费者(Consumer)

消费消息。每个`consumer`属于一个特定的`consumer group`。使用`consumer high level API`时，同一个topic的一条消息只能被同一个`consumer group`内的一个`consumer`消费，但多个`consumer group`可同时消费这一消息。每个partition只会由一个consumer消费。

### 集群(Cluster)

宏观来看，Kafka主体包含的就是三部分: 生产者、消费者和集群，一个集群就是多个Broker的集合。

### Broker

已经发布的消息就会保存在集群中的某个Broker中去。

### Topic

用来区别message的种类，比如很多时候，与A相关的日志统一的topic定义为A，B相关的日志统一的topic定义为B，这样就不用一个一个单独地订阅了。物理上不通topic的消息分开存储，逻辑上一个topic的消息虽然保存于一个或多个broker上，但是用户只需指定消息的topic即可生产或消费数据而不必关心数据在哪里。

### Partition

Kafka中每个Topic都会有一个或多个Partition，他是Kafaka数据存储的基本单元，每个Partition对应一个文件夹，文件夹下存储这个Partition的所有消息和索引。Kafka内部会根据算法得出一个值，根据这个值放入对应的partition目录中。所以读取时间复杂度为O(1)。分区的每一个消息都有一个连续的序列号叫做offset，用来在分区中唯一标识这个消息。一个topic可以保存在多个partition。Kafka会保证每个partition内部的顺序，但是不能保证跨partition的全局顺序，如果要保证全局有序，那么topic就只能有一个partition。如果一个group内部的consumer数量小于partition数量，那么至少有一个consumer会消费多个partition。当consumer数量和partition数量相等时效率最高。consumer数量不要大于partition数量，否则会有consumer空闲。consumer会自动负载到不同的partition。

- 对于某一个topic，增加partition可以增加吞吐能力，但无法保证topic级别的有序性。

### Segment

一个partition由多个Segment组成，一个Partition代表一个文件夹，一个Segment则代表该文件夹下的文件。Segment有大小限制，由`log.segment.bytes` 定义。

## 安装

### docker方式安装

`docker-compose.yml`文件:

```yaml
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    environment:
      JMX: 9000
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka	# 这个镜像使用文档见https://github.com/wurstmeister/kafka-docker
    ports:
      - "9092"
    environment:
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://:9092	# 这是重点，否则，在容器内部启动生产者消费者都会失败的
      KAFKA_LISTENERS: PLAINTEXT://:9092
      KAFKA_CREATE_TOPICS: "test:1:1"				# 自动创建一个默认的topic
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "false"		# 禁用掉自动创建topic的功能，使用上面的镜像，kafka的参数设置都可以以这样的方式进行设置
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
  kafka-manager:
    image: sheepkiller/kafka-manager		# 如果要安装web管理工具可以同时安装这个，最后通过宿主机IP的9000端口进行访问，例如172.31.148.174:9000
    links:
      - kafka
      - zookeeper
    environment:
      ZK_HOSTS: zookeeper:2181
      APPLICATION_SECRET: "letmein"
    ports:
      - "9000:9000"
    expose:
      - "9000"
```

安装命令:

```shell
docker-compose up -d			# 默认只会有一个kafka实例
docker-compose scale kafka=n	# 将kafka实例增加到n个，什么都不用修改，就能直接建立一个集群
docker-compose stop				# 暂停所有容器
docker-compose start 			# 开启所有容器
docker-compose rm -f 			# 删除所有容器
```

### kafka命令

#### kafka-console-consumer.sh

```shell
kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic test	# 启动一个消费者，监听test这个topic
```

#### kafka-console-producer.sh

```shell
kafka-console-producer.sh --broker-list localhost:9092 --topic test	# 启动一个生产者，直接输入消息回车即可发送消息了
kafka-console-producer.sh --broker-list localhost:9092 --topic test	< access.log # 直接将文件内容传入kafka
```

#### kafka-consumer-groups.sh

```shell
kafka-consumer-groups.sh --new-consumer --bootstrap-server localhost:9092 --list	# 查看新消费者列表
kafka-consumer-groups.sh --new-consumer --bootstrap-server localhost:9092 --describe --group kafka-python-default-group	# 查看某消费者的消费详情，这里的消费者名称就是kafka-python-default-group
```

#### kafka-producer-perf-test.sh自带的压测工具

```shell
kafka-producer-perf-test.sh --topic test --num-records 10000 --record-size 1 --throughput 100  --producer-props bootstrap.servers=localhost:9092	# 总共100条数据，每条大小是1
```

#### kafka-topics.sh

```shell
kafka-topics.sh --list --zookeeper zookeeper:2181		# 列出所有的topic
kafka-topics.sh --describe --zookeeper zookeeper:2181	# 查看集群描述
```

## 安全认证

Kafka可以配合SSL+ACL来进行安全认证: http://orchome.com/185

## TroubleShooting

- **容器内部启动生产者出现错误:`[2016-12-26 03:03:39,983] WARN Error while fetching metadata with correlation id 0 : {test=UNKNOWN_TOPIC_OR_PARTITION} (org.apache.kafka.clients.NetworkClient)`**

  是因为`docker-compose`文件里面的宿主讥IP设置出错，如果是动态IP的话就没办法了，只能删除重新创建了
  
- **启动生产者或者消费者出现LEADER_NOT_AVAILABLE**：原因是没有执行`docker-compose scale kafka=n`

##### 拓展阅读

- [kafka-python基本使用](https://zhuanlan.zhihu.com/p/38330574)