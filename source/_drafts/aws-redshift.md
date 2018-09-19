---
title: "Amazon Aws Redshift手册"
date: 2018-08-02 21:32:00
updated: 2018-09-17 15:45:00
categories: aws
---

Aws Redshift是一个由Amzon提供的数据仓库管理系统(RDBMS)，基于PostgreSQL 8.0.2，随着时间的推移，两者之间的差距也越来越大，但就像MySQL与Mariadb一样，两者在语法层面大同小异，Redshift也可以用PostgreSQL的客户端(推荐TablePlus)进行连接和管理。当然，普通数据库和数据仓库需要解决的问题是不一样的，前者是为业务提供保证，后者则是以大数据的分析决策提供便利，两者不能混用。而且Redshift可以说是相当的贵，个人观点是大公司节约成本绝对不能用，小公司数据量不太大的情况下可以用一用。

本文尽量只列出两者不一样的地方，一样的地方可以参考我写的[Postgresql 使用手册](https://haofly.net/postgresql)。另外[官方文档](https://www.amazonaws.cn/documentation/redshift/)是相当完美的，建议第一次接触，按照官方文档一步一步来，就基本上能熟悉所有的操作了。

<!--more-->

## 在线配置

## 增删改查

### 数据库操作

### 数据表操作

- [支持的数据类型](http://docs.amazonaws.cn/redshift/latest/dg/c_Supported_data_types.html)
- 数据库默认是不区分大小写的，表名以及列名都不会区分大小写，所以最好全部用小写
- 自增字段不能使用`serial`，而应该使用`IDENTITY`来创建，即`field_name INT IDENTITY(1, 1)`，表示从1开始，每次自增1
- `redshift`不允许使用`ALTER`修改字段类型
- `distkey`属性的列是不能被`DROP`的

```mysql
ALTER table tableA rename to table2;	# 更改表名
ALTER table tableA DROP COLUMN fieldA;	# 删除列
```

### 数据操作

- http://docs.amazonaws.cn/redshift/latest/dg/c_intro_to_admin.html 数据库使用文档，增删改查.有取消查询的功能等
- SQL语句有最大size的限制，最大不超过16777216字节

#### 查询记录

```mysql
# 去重取出某个key里面最新的一条，这是我能找到的效率最高的一条了
SELECT * FROM table1 WHERE id NOT IN (SELECT id FROM (SELECT id, ROW_NUMBER() OVER(PARTITION BY field1 ORDER BY field2 DESC) AS rnum FROM table1) t WHERE t.rnum>1);
```

#### 新增记录

#### 更新记录

- `redshift`能够一次插入几十万条数据，但是一次`UPDATE`操作却能轻松让CPU负载上到100%(本身实现也是先删除再插入，并且数据库内部存储也会变乱，如果`UPDATE`或者`DELETE`太多，反而需要经常执行`vacuum table1 to 100 percent;`强制回收空间)。对于数据仓库来说，尽量保留数据的真实信息，它也有足够的能力处理大量的历史数据，所以，这里就只能放弃`UPDATE`操作，手动写去重逻辑。[vacuum命令文档](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/r_VACUUM_command.html)

#### 删除记录





##### 扩展阅读

- [amazon-redshift-utils](https://github.com/awslabs/amazon-redshift-utils): redshift相关的各种方便的管理脚本等









http://docs.amazonaws.cn/redshift/latest/dg/c_high_level_system_architecture.html  非常详细的redshift数据仓库架构解释

- 一个集群包含一个或多个数据库。用户数据存储在计算节点上。sql客户端与领导节点进行通信，进而通过计算节点协调查询执行。

- redshift是一个关系型数据库管理系统(RDBMS)。基于PostgreSQL 8.0.2，两者之间的差别越来越大。类似mysql与mariadb一样，redshift也可以用postgresql客户端进行连接和管理

- http://docs.amazonaws.cn/redshift/latest/dg/c_challenges_achieving_high_performance_queries.html 它在性能方面的优势

- http://docs.amazonaws.cn/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html  列式存储优点

- http://docs.amazonaws.cn/redshift/latest/dg/c_workload_mngmt_classification.html   工作负载管理WLM。查询优先级。默认情况下，Amazon Redshift 配置一个具有*并发级别* 5 的队列（这将允许同时运行最多 5 个查询）和一个具有并发级别 1 的预定义的超级用户队列。您可以定义最多 8 个队列。每个队列可配置最高 50 的并发级别。所有用户定义的队列（不包括超级用户队列）的最高并发级别总数为 50。可以通过命令或者管理控制台修改WLM配置。超级用户队列无法进行配置且一次只能处理一个查询，保留此队列以仅作故障排除只用。用户队列可一次处理多达5个查询，可以在需要时通过更改队列的并发级别了来配置此能力。

  若您有多个用户正在对数据库运行查询，您可能会发现另一种配置将更高效。例如，如果一些用户运行资源密集型操作（如 VACUUM），则这些操作可能会对资源不太密集型查询（如报告）产生负面影响。您可考虑添加其他队列并针对不同的工作负载配置它们。

   http://docs.amazonaws.cn/redshift/latest/dg/tutorial-configuring-workload-management.html配置方式

- 

- 几个系统表

  - pg_table_def  包含群集中所有表的有关信息schemaname|tablename|column | type  |encoding|distkey|sortkey | notnull  

- 排序键sortkey(类似于MySQL中的索引)。redshift根据排序键将数据按照排序顺序存储在磁盘中。

  - 如果最近使用的数据查询频率最高，则指定时间戳列作为排序键的第一列
  - 如果您经常对某列进行范围筛选或相等性筛选，则指定该列作为排序键
  - 如果您频繁联接表，则指定联接列作为排序键和分配键

- 分配方式distkey。在执行查询时，查询优化程序根据执行联接和聚合的需要将行重新分配到计算节点。选择表分配方式的目的是通过在执行查询前将数据放在需要的位置来最大程度地减小重新分配步骤的影响。

  - 根据共同列分配事实数据表和一个维度表。事实数据表只能有一个分配键。任何通过其他键联接的表都不能与事实数据表并置。根据联接频率和联接行的大小选择一个要并置的维度。将维度表的主键和事实数据表对应的外键指定为 DISTKEY。
  - 根据筛选的数据集的大小选择最大的维度。只有用于联接的行需要分配，因此需要考虑筛选后的数据集的大小，而不是表的大小。
  - 在筛选结果集中选择基数高的列。例如，如果您在日期列上分配了一个销售表，您可能获得非常均匀的数据分配，除非您的大多数销售都是季节性的。但是，如果您通常使用范围受限谓词进行筛选以缩小日期期间的范围，则大多数筛选行将位于有限的一组切片上并且查询工作负载将偏斜。
  - 将一些维度表改为使用 ALL 分配。如果一个维度表不能与事实数据表或其他重要的联接表并置，您可以通过将整个表分配到所有节点来大大提高查询性能。使用 ALL 分配会使存储空间需求成倍增长，并且会增加加载时间和维护操作，所以在选择 ALL 分配前应权衡所有因素。

- 数据分配：

  将数据加载到表中时，Amazon Redshift 根据表的分配方式将表中的行分配到各个计算节点。在执行查询时，查询优化程序根据执行联接和聚合的需要将行重新分配到计算节点。选择表分配方式的目的是通过在执行查询前将数据放在需要的位置来最大程度地减小重新分配步骤的影响。

   

- 如果您插入、更新或删除了表中的大量行（相对于更改前的行数），请在完成后对表运行 ANALYZE 和 VACUUM 命令。如果在经过一段时间之后您的应用程序中累积了大量小更改，则可能需要安排定期运行 ANALYZE 和 VACUUM 命令。有关更多信息，请参阅 [分析表](http://docs.amazonaws.cn/redshift/latest/dg/t_Analyzing_tables.html) 和 [对表执行 vacuum 操作](http://docs.amazonaws.cn/redshift/latest/dg/t_Reclaiming_storage_space202.html)。 

- 除非您的应用程序强制实施约束，否则不要定义主键和外键约束。Amazon Redshift 不强制实施唯一的主键和外键约束。

- 不要为了方便而习惯使用最大列大小。

- 对日期列使用日期/时间数据类型

- 数据库方面非常棒的优化路线及实践









多个会话或多名用户同时运行查询时，某些查询可能会长时间占用群集资源，从而影响其他查询的性能。例如，假设一组用户时不时提交复杂、耗时的查询（从多个大型表中选择和排序行）。另一组用户经常提交短查询（仅从一个或两个表中选择少量行，运行时长只有数秒）。这种情况下，短时查询可能不得不在队列中等待耗时查询完成。

您可以修改 WLM 配置，为耗时查询和短时查询分别创建队列，以提升系统性能和用户体验。在运行时，您可以根据用户组或查询组将查询路由到这些队列。

 



您可以配置多达八个查询队列，并设置可在每个队列中同时运行的查询数。您可以设置规则以根据运行查询的用户或指定的标签将查询路由到特定的队列。您还可以配置分配到每个队列的内存量，使大型查询在内存更多的队列中运行。您也可以配置 WLM 超时属性以限制耗时查询。 

我们建议您为 WLM 查询队列配置总计 15 个或更少的查询插槽。有关更多信息，请参阅 [并发级别](http://docs.amazonaws.cn/redshift/latest/dg/cm-c-defining-query-queues.html#cm-c-defining-query-queues-concurrency-level)。 



短查询加速http://docs.amazonaws.cn/redshift/latest/dg/wlm-short-query-acceleration.html

动态WLM http://docs.amazonaws.cn/redshift/latest/dg/cm-c-wlm-dynamic-properties.html

数据类型http://docs.amazonaws.cn/redshift/latest/dg/c_Supported_data_types.html

SQL命令 http://docs.amazonaws.cn/redshift/latest/dg/c_SQL_commands.html  防注入的时候可以用

系统表

http://docs.amazonaws.cn/redshift/latest/dg/cm_chap_system-tables.html



创建注释不和create一起，我去

https://stackoverflow.com/questions/32070876/adding-comment-to-field-when-i-create-table

https://blog.csdn.net/xiaoxuechi/article/details/79297009