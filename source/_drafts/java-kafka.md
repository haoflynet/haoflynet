---
title: "Java 连接kafka进行监听"
date: 2019-12-05 15:14:00
---

我之前有文章介绍`kafka`以及如何在本地通过`docker`创建`kafka`集群，这里只是介绍如何在`java`项目中直接使用`kafka`客户端。

##### Spring引入kafka客户端

首先需要在`pom.xml`引入如下依赖，需要注意的是，kafka的客户端版本号和服务端的版本号兼容性要求比较高(无论是不是java都这样，所以一定要找到正确的版本，可以参考[Apache Kafka](https://cwiki.apache.org/confluence/display/KAFKA/Compatibility+Matrix)):

```java
<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId>kafka-clients</artifactId>
  <version>1.0.2</version>
</dependency>
```

- 监听最好是新建一个线程，这里直接用的是`Spring`的`@Async`注解

<!--more-->

##### 消费者定义

```java
Properties props = new Properities();
props.put("bootstarp.servers", "127.0.0.2:9092,127.0.0.2:9093:127.0.0.2:9094");	// 设置broker servers
props.put("group.id", "消费者group名");
props.put("enable.auto.commit", "true");
props.put("auto.commit.interval.ms", "1000");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("监听的topic"));

while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);	// 100表示超时时间
	for (ConsumerRecord<String, String> record : records) {
    System.out.println(record.value());	// 原始数据
    System.out.println(record.offset());	// 当前的偏移量
}
```