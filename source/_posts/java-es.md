---
title: "Java ElasticSearch客户端使用示例"
date: 2019-12-05 18:14:00
updated: 2019-12-16 10:30:00
---

#### es的引入及配置

要想使用Java版的`es`客户端，首先需要在`pom.xml`引入如下依赖

```xml
<dependency>
  <groupId>org.elasticsearch.client</groupId>
  <artifactId>elasticsearch-rest-high-level-client</artifactId>
  <version>7.4.0</version>
</dependency>
```

<!--more-->

新建配置文件，这样可以使用自动注入

```java
package com.haofly.net.common.elasticsearch.config;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EsConfig {
    private String host = "127.0.0.1";
    private Integer port = 9202;
  
    @Bean
    public HttpHost getHttpHost(){
        return new HttpHost(host,port);
    }
    @Bean(destroyMethod = "close")
    public RestHighLevelClient getHlvClient(){
        return new RestHighLevelClient(RestClient.builder(getHttpHost()));
    }
    public String getHost() {
        return host;
    }
    public void setHost(String host) {
        this.host = host;
    }
    public Integer getPort() {
        return port;
    }
    public void setPort(Integer port) {
        this.port = port;
    }
}
```

在代码层，只需要直接注入即可，例如在Servic种可以这样引入:

```java
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
public class EsService {
  @Autowired
  RestHighLevelClient restHighLevelClient;
}
```

#### java es的增删改查

基本数据定义，下面的示例种出现的数据原型如下

```java
String index = "索引"
String type = "类型";
String primaryId = "主键ID";
String data = "{\"field\":\"JSON格式字符串\"}";
HashMap<String, String> datas = new HashMap<>();
datas.put("4", "{\"bbbbbbbbbbbbbb\":\"cccccccccc\"}");
String gteTime = "1234567890000";
String lteTime = "1234567890000";
Integer from = 12345;	// 偏移量
Integer size = 1000;	// 每页数量
```

##### 查询搜索

```java
SearchRequest request = new SearchRequest(index);

// 构造查询请求
SearchSourceBuilder ssb = new SearchSourceBuilder();
BoolQueryBuilder boolQueryBuilder = new BoolQueryBuilder();

// 时间范围参数
RangeQueryBuilder rangeQueryBuilder = new RangeQueryBuilder("@timestamp");
rangeQueryBuilder.gte(gteTime).lte(lteTime);
boolQueryBuilder.must(rangeQueryBuilder);

// 查询语句参数，需要注意的是如果是不需要匹配value中的每一个字符，则需要在前后加上双引号
QueryStringQueryBuilder queryStringQueryBuilder = new QueryStringQueryBuilder("\"value1\"").field("fieldName").defaultOperator(Operator.AND);
boolQueryBuilder.must(queryStringQueryBuilder);

ssb.query(boolQueryBuilder);
ssb.from(from);	// 设置偏移量
ssb.size(size);	// 设置每页数量

HighlightBuilder highlightBuilder = new HighlightBuilder();
highlightBuilder.field("*");	// 获取所有字段
ssb.highlighter(highlightBuilder);
request.source(ssb);

// 发送查询请求
SearchResponse searchResponse = restHighLevelClient.search(
  request, RequestOptions.DEFAULT);
```

以上的查询会解析成类似于这样的查询参数(索引是单独的参数)

```json
{
  "from": 9000,
  "size": 1000,
  "query": {
    "bool": {
      "must": [
        {
          "should": [
            {
              "query_string": {
                "fields": [
                  "fieldName1",
                ],
                "query": "value1"
              }
            }
          ]
        }
        {
          "range": {
            "@timestamp": {
              "from": "1546272000000",
              "to": "1577808000000",
              "include_lower": true,
              "include_upper": true,
              "boost": 1
            }
          }
        }
      ],
      "adjust_pure_negative": true,
      "boost": 1
    }
  },
  "highlight": {
    "fields": {
      "*": {}
    }
  }
}
```

##### 单条文档操作

```java
// 单条插入
IndexRequest request = new IndexRequest(index, primaryId);
request.source(data, XContentType.JSON);
restHighLevelClient.index(request, RequestOptions.DEFAULT);

// 更新或插入单条doc，有就更新，没有就创建
UpdateRequest request = new UpdateRequest(index, primaryId)
  .doc(data, XContentType.JSON)
  .upsert(data, XContentType.JSON);
restHighLevelClient.update(request, RequestOptions.DEFAULT);

// 单条更新
UpdateRequest request = new UpdateRequest(index, primaryId)
  .doc(data, XContentType.JSON);
restHighLevelClient.update(request, RequestOptions.DEFAULT);

// 单条删除
DeleteRequest request = new DeleteRequest(index, primaryId);
restHighLevelClient.delete(request, RequestOptions.DEFAULT);
```

##### 批量操作

```java
// 批量插入doc
BulkRequest request = new BulkRequest();
for (Map.Entry<String, String> data : datas.entrySet()) {
	request.add(new IndexRequest(index, data.getKey())
              .source(data.getValue(), XContentType.JSON));
}
BulkResponse bulkResponse = restHighLevelClient.bulk(request, RequestOptions.DEFAULT);
if (bulkResponse == null || !bulkResponse.hasFailures()) {
	return bulkResponse == null ? 0 : datas.size();
}
Integer success = 0;	// 插入成功的数量
for (BulkItemResponse bulkItemResponse : bulkResponse) {
	if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.INDEX
		|| bulkItemResponse.getOpType() == DocWriteRequest.OpType.CREATE) {
			success++;
	}
}

// 批量更新doc
BulkRequest request = new BulkRequest();
for (Map.Entry<String, String> data : datas.entrySet()) {
	request.add(new UpdateRequest(index, data.getKey())
              .doc(data.getValue(), XContentType.JSON));
}
BulkResponse bulkResponse = restHighLevelClient.bulk(request, RequestOptions.DEFAULT);
if (bulkResponse == null || !bulkResponse.hasFailures()) {
	return bulkResponse == null ? 0 : datas.size();
}
Integer success = 0;	// 更新成功的数量
for (BulkItemResponse bulkItemResponse : bulkResponse) {
	if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.INDEX
			|| bulkItemResponse.getOpType() == DocWriteRequest.OpType.CREATE) {
				success++;
	}
}

// 批量删除，根据ID进行删除
BulkRequest request = new BulkRequest();
for (String id : ids) {
	request.add(new DeleteRequest(index, id));
}
BulkResponse bulkResponse = restHighLevelClient.bulk(request, RequestOptions.DEFAULT);
if (bulkResponse == null || !bulkResponse.hasFailures()) {
	return bulkResponse == null ? 0 : ids.size();
}
Integer success = 0;	// 删除成功的数量
for (BulkItemResponse bulkItemResponse : bulkResponse) {
	if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.INDEX
		|| bulkItemResponse.getOpType() == DocWriteRequest.OpType.CREATE) {
			success++;
	}
}
```

