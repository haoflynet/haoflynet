---
title: "ElasticSearch 操作手册"
date: 2019-12-05 17:14:00
updated: 2019-12-17 17:55:00
---
ELK是`elastic`公司提供的一整套日志收集与展示的解决方案，我司目前大量采用ELK来进行日志的搜集与展示。它主要由`ElasticSearch`、`Logstash`、`Kibana`三部分组成。简单地解释就是，`Kibana`主要用于前端汇总展示数据，`Logstash`主要用于日志的搜集(前几天写过[Logstash的使用手册](https://haofly.net/logstash/))，而`ElasticSearch`则是其核心，`Es`是一个开源的分布式搜索引擎，支持分布式、自动发现、自动分片、索引副本、restful风格接口、多数据源、自动搜索负载等特性。除了被大量用于日志搜索意外，它还常作为一个全文搜索引擎用于海量数据的快速搜索与分析。

可以把`es`看作一个分布式的数据库，可以在多台服务器上运行多个`Elastic`实例，每个`Elastic`示例可以被称为一个节点`Node`，一组节点组成一个集群(Cluster)。`Es`里面每条记录叫做文档`Document`，一个类型的文档放在一起作为一个索引`Index`，文档内部也可以进行逻辑分组，叫做`Type`。不同的`Index`里面数据的结构不一样，同一个`Index`下不同的`Type`数据结构是类似的。

## API

### 索引操作

<!--more-->

```shell
curl -X GET localhost:9200/_cat/indices?v	# 列出所有的索引Index
curl -X GET localhost:9200/索引名称	# 列出指定索引的详情
curl -X GET localhost:9200/_mapping?pretty=true # 列出所有索引Index对应的所有的Type
curl -X GET localhost:9200/索引名称/_search?from=0&size=1000	# 搜索某个索引下的文档

curl -X PUT localhost:9200/索引名称/_settings?preserve_existing=true	# 修改索引配置，例如如果PUT数据为{"index.max_result_window": "10000000"}，那么可以将index.max_result_window这个值设置为指定值
curl -X PUT localhost:9200/_all/_settings?preserve_existing=true	# 同时修改所有索引的配置
```

### 搜索

- 默认的搜索结果最多只有一万条，可以参考上面的更改设置的方式修改指定索引的返回数据量。如果要修改默认动作，可以直接在`/etc/elasticsearch/elasticsearch.yml`配置文件中添加这个参数`index.max_result_window: 100000000`

- 分页最好使用`scroll`方式，而不用`from  size`的方式，因为`from size`的分页方式可能造成严重的性能问题，比如有1亿条数据，from=100000000，size=100，在查询阶段，每个`shards`都会返回100000100条数据给`node`，而`node`再将他们整合，直到找到100条数据。

- 遍历数据推荐使用`scroll`的方式，在初次请求后拿到一个`scroll_id`，之后的请求携带上它即可完成自动分页，直到返回的数据为空即表示遍历完成:

  ```shell
  curl -X POST localhost:9200/索引名称/_search?scroll=1m {查询结构体}	# 这个请求会附带返回一个scroll_id
  curl -X POST localhost:9200/索引名称/_search?scroll=上一次的值
  ```

文档搜索的结果一般包含如下字段

```json
{
	took: 4,	// 执行搜索花费的时间(毫秒)
	timed_out: false,	// 搜索是否超时
	_shards: {	// 有多少个分片被搜索了，里面包含了搜索到的各个分片的统计
		total: 1,
		successful: 1,
		skipped: 0,
		failed: 0
	},
	hits: {	// 搜索结果
		total: {
			value: 10000,
			relation: "gte"
		},
		max_score: 1,
		hits: [
			{
				_index: "索引名",
				_type: "Type名",
				_id: "Document的ID",
				_score: 1,	// 结果的排序
				_source: {	// 原始结果
					@timestamp: "2019-10-11T09:19:13.929Z",
					user_id: 4042615,
					@version: "1",
					createtime: 1460959801,
					task_id: 3260344,
					type: "结果的Type"
			},
    ]
  }
}
```

##### TroubleShooting

- **version conflict, document already exists (current version [1])或者version conflict, required seqNo [88099], primary term [1]. current document has seqNo [88150] and primary term [1]**: 可能是并发插入同一个id造成，es有一个`_version`作为版本号来避免这个问题，但是需要业务自己选择；或者在更新的时候加上`retry_on_conflict=5`设置冲突发生时的重试次数。但是我个人认为要么业务对并发先后无要求，要么就改成单进程或者写单独逻辑来控制，因为重试依然不能保证顺序性。

##### 扩展阅读

- [Java ElasticSearch客户端使用示例](https://haofly.net/java-es/)