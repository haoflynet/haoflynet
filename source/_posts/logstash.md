---
title: "logstash 手册"
date: 2019-11-29 15:26:00
categories: 大叔据
---

`Logstash`是一个开源的数据转化工具，可以将不同的数据源的数据进行收集、分析、处理，并存储到指定的介质，常用于搜集服务器上的日志到`elasticsearch`，或者快速地将数据从一种介质转移到另一种介质。

[官方](https://www.elastic.co/guide/en/logstash/7.4/installing-logstash.html)提供了多种安装方式，也可以直接下载源码，源码解压即可用。

## 常用命令

```shell
./bin/logstash -f getdata.conf	# 执行指定的配置文件
./bin/logstash -e input { } filter { } output { }	# 直接执行指定的输入、过滤、输出管道，格式就是配置文件的格式，但要注意大括号前后都要加上空格，以免命令解析失败
```

## 常用插件

### logstash-input-jdbc

<!--more-->

- 用于连接数据库
- 使用`./bin/logstash-plugin install logstash-input-jdbc`进行安装
- 一定要单独下载`mysql-connector-java`的`jar`包，并一定得放在`logstash`的安装目录中的`logstash-core/lib/lib/jars`下(注意`logstash`的安装目录不一定在`/opt`下面)，否则会出现找不到`com.mysql.jdbc.Driver/jdbc_driver_library`的错误，可以在这里[下载](https://mvnrepository.com/artifact/mysql/mysql-connector-java/6.0.6)指定的jar包版本
- 下面的参考配置，当实际执行的时候，其实是定时去执行这样的查询语句:`SELECT id, field1, field2 FROM database_name.table_name WHERE id > 1000 ORDER BY id ASC LIMIT 1000, 1000`，并会一直去执行，根据官方论坛的反馈，它没有终止条件，所以如果想要停止查询，只能主动`kill`掉该进程
- 参考配置文件如下:

```shell
input {
    jdbc {
        type => "type_name1"
        jdbc_connection_string => "jdbc:mysql://localhost:3306/database_name?serverTimezone=Asia/Shanghai&useUnicode=true&characterEncoding=utf-8&zeroDateTimeBehavior=convertToNull&&useSSL=false&&allowMultiQueries=true"
        jdbc_user => "database_name"
        jdbc_password => "database_password"
        jdbc_paging_enabled => "true"	# 支持分页
        jdbc_driver_library => "/opt/logstash/logstash-core/lib/jars/mysql-connector-java-6.0.6.jar"	# 指定mysql-connector-java的jar包位置
        jdbc_driver_class => "com.mysql.jdbc.Driver"         
        jdbc_default_timezone =>"Asia/Shanghai"
        jdbc_page_size => "1000"	# 每页数量
        statement => "SELECT id, field1, field2 FROM database_name.table_name WHERE id > :sql_last_value ORDER BY id ASC;"	# 定义查询语句(这里不用写上分页关键字，会自动分页)
        schedule => "* * * * *"	# 定时多久去查询一次
        use_column_value => true
        tracking_column => "id"	# 跟踪列，会根据指定的列来进行跟踪，防止重复拉取
        last_run_metadata_path => "/tmp/last_run_metadata"	# 自定义跟踪文件地址，会将当前的跟踪列的最大值填入，下一次只会找比它大的数据
    }
    jdbc {
    	...	# 参考上面的配置，可以同时连接多个数据库
    }
 }
filter {
  if [type]=="type_name1"{
  	mutate {
		replace => { my_field2 => "field1" }	# 可以改变某个列的名称
		replace => { business => "自定义的字段值" }	# 可以自己添加列
  }
  if [type]=="type_name2"{
  	...
  }
}
output { 
	if [type]=="type_name1"{
		elasticsearch {		# 直接输出到es
		hosts => "localhost:9202"
		index => "my_index"	# 自定义的索引名
		document_id => "%{id}"	# 指定需要以哪一列来作为es的doc的id
	}
	if [type]=="type_name2"{
		...
	}
}
```

## TroubleShooting

- **`ERROR: Installation aborted, verification failed for logstash-input-jdbc`**，加上忽略验证的参数试试`./logstash-plugin install --no-verify logstash-input-jdbc` 