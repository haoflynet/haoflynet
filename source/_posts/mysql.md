---
title: "MySQL／MariaDB 教程"
date: 2016-08-07 11:01:30
updated: 2020-07-11 11:44:00
categories: database
---
## 安装方法
**CentOS**：[使用包的方式安装最新MariaDB](https://mariadb.com/kb/en/library/binary-packages/)，CentOS安装client直接yum install mysql而不是client，而安装mysql则直接用`yum install -y mysql mysql-server mysql-dev mysql-devel`，CentOS7上已经用mariadb代替了mysql，这样子使用：

```shell
yum install mariadb-server mariadb-client mariadb-devel -y
systemctl start mariadb.service # 启动服务
systemctl enable mariadb.service	# 开机启动
```
另外，更新方式可以参考这篇文章: [如何更新到MariaDB 10.4](https://www.mysterydata.com/update-upgrade-to-mariadb-10-4-on-vestacp-cwp-centos-7/)

Ubuntu: 

```shell
# 安装最新版本，需要先导入对应的镜像库https://downloads.mariadb.org/mariadb/repositories
sudo apt-get install mariadb-server mariadb-client libmariadbd-dev

# 如果是开发，还需要安装
sudo apt-get install libmariadb-client-lgpl-dev
sudo ln -s /usr/bin/mariadb_config /usr/bin/mysql_config

# 第一次登录使用
sudo mysql -u root
```

<!--more-->

## 常用命令

### SQL文件操作

```shell
# 执行sql文件
mysql -uroot -pmysql --default-character-set=gbk  jpkc_db < jpkc_db.sql # 这里可以执行编码格式
```

### 数据库操作

```shell
## 创建数据库，如果是gbk编码，分别用gbk、gbk_chinese_ci;
CREATE DATABASE 库名 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
TRUNCATE tablename	# 清空数据表
DROP DATABASE database_name	# 删除数据库
```

### 数据表操作

```mysql
CREATE TABLE `table2` SELECT * FROM `table1`;	# 从一张旧表直接建立一张新表
DROP TABLE name; # 删表
ALTER TABLE 表名 RENAME TO 新表名	# 修改表名称
## 清空数据表
DELETE FROM 表名; # 这种方式比较慢，但是可以恢复
TRUNCATE TABLE 表名 # 这种方式很快，但不会产生二进制日志，无法回复数据

ALTER TABLE 表名 DROP FOREIGN KEY '外键名';	# 删除外键
ALTER TABLE 表名 ADD 字段名 属性 AFTER 字段名;	# 给表添加字段
ALTER TABLE 表名 ADD `id` int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST; # 添加字段到最前面
ALTER TABLE 表名 DROP COLUMN 字段名;	# 给表删除字段
ALTER TABLE 表名 CHANGE COLUMN 列名 新的列名 属性;	# 修改列属性
ALTER TABLE 表名 MODIFY COLUMN 列名 属性; # 除了不能修改列名以外，其他都和CHNAGE一样
ALTER TABLE 表名 engine=innodb; # 修改数据表引擎

ALTER TABLE 表名 ADD INDEX 索引名 (列名);# 给表添加索引
ALTER TABLE 表名 ADD UNIQUE `键名`(`列名1`, `列名2`);
ALTER TABLE 表名 DROP INDEX 索引名;	# 给表删除索引

ALTER TABLE 表名 AUTO_INCREMENT = 10;	# 重置自增主键

# mariadb创建Json字段，VARCHAR或者BLOB都可以使用，不对格式做要求，如果要做要求也可以强制做，例如
CREATE TABLE IF NOT EXISTS products(id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  attr VARCHAR(1024),
  CHECK (JSON_VALID(attr)));
```

### 常见表字段

- MySQL每行最大能存储65535字节的内容，所以对于utf8最多存储21844个字符，对于utf8mb4最多存储16383个字符，这也是`VARCHAR/Text`的最大值，`MediumText`长度为16777215。
- 如果是存储`ip`信息的字段一定要兼容`IPv6`(如果用字符存储那么最长39位)

##### timestamp

- `TIMESTAMP(3)/TIMESTAMP(6)`表示精确到毫秒微妙级别
- 对于timestamp字段，如果直接插入数字形式的时间戳可能会变成`0000-00-00 00:00:00`的结果，我们需要使用`FROM_UNIXTIME(1234567890)`函数对其进行转换

##### decimal

- 定义时候需要提供两个参数: `DECIMAL(P, D)`，其中P表示有效数字的精度，范围为`1-65`，D表示小数点后的位数，范围是`0-30`，其中`D<P`

### 数据增删改查

- `LEFT JOIN`是`LEFT OUTER JOIN`的简写，`RIGHT JOIN`是`RIGHT OUTER JOIN`的简写，`JOIN`是`INNER JOIN`的简写
- 获取某个表的自增下一个自增ID: `SHOW TABLE STATUS`，结果中的`auto_increment`

##### 查询

- 在程序中遇到要拼接`SQL`语句的，可以在条件里面加一个`where 1=1`能有效简化代码

```mysql
# 普通查询
SELECT * FROM table_A
SELECT * FROM ... BETWEEN value1 AND value2
SELECT * FROM ... NOT BETWEEN value1 AND value2
SELECT DISTINCT(field_1) FORM ...	# 去重
SELECT * FROM table_A WHERE DATEDIFF(DATE_ADD(CURDATE(), INTERVAL 30 DAY), `expiration_date`) BETWEEN 0 AND 30	# 使用DATE相关函数查询最近30天到期的记录

# 分组查询
SELECT count(column_a) as count FROM table_A GROUP_BY coulumn_b

# 多表子查询
## 需要注意的是，子查询后面必须要AS一个别名
update table_1 as a, (select id from biao_2 where name='a') as b set a.title='xx' where a.id=b.id

# 随机读取数据库记录
SELECT * FROM table WHERE id >= (SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table))) ORDER BY id LIMIT 1
SELECT * FROM table ORDER BY RAND() LIMIT 10;

# 分页功能，获取m开始的n条记录
SELECT * FROM table_name limit m, n

# 模糊查询/正则查找
SELECT * FROM table_name like '%abc_';	# 模糊查询，其中%贪婪匹配任意数量的任意字符，_匹配一个任意字符
SELECT * FROM table_name WHERE field REGEXP '(.*?)wtf';
SELECT * FROM table_name WHERE field REGEXP 'ABC|DEF|GHI';	# 类似于LIKE IN的功能

# 分组GROUP BY
SELECT * FROM table_name GROUP BY `field1`, `field2`;	# 分组显示，有多少不同的field就会有多少条记录，而其他的字段则是随机选择一条记录显示，当然，如果对其他字段进行SUM等操作，那么就可以获取分类的SUM，十分有用

# Having子句，与WHERE不同，它可以和一些统计函数一起使用
SELECT name, SUM(money) FROM users GROUP BY name HAVING SUM(money)>23333 # 这一句就能查找出所拥有的资产综合大于23333的用户
SELECT * FROM virtuals WHERE ip in (SELECT ip FROM virtuals GROUP BY ip HAVING COUNT(ip)>1);	# 可以统计所有有重复的数据

# 找出每个分组的最新的一条记录(目前我能找到的最有效的方法，虽然效率依然很低)
SELECT table1.* FROM table1 LEFT JOIN table2 ON (table1.name = table2.name AND table1.id < table2.id) WHERE m2.id IS NULL;
SELECT * FROM table1 WHERE id IN (SELECT MAX(ID) FROM table1 GROUP BY field1);	# 如果有group by可以通过这种方式找到每个分组中最新的一条记录

# 合并两条SQL的查询结果
SELECT field1 FROM table1
UNION
SELECT field1 FROM table2
```
**LIKE查询的特殊转义**

```shell
/: //
': /'，用于包裹搜索条件
": /"
\: \\\\	# 没错，右斜杠需要这样做
_: 一定要注意下划线，在like里面代表任意一个字符
%: 代表任意数目的任意字符
```

##### 连表查询

```mysql
# LEFT JOIN ... ON ...
## 会取出左表的全部记录，即使右表没有对应匹配的记录。用这种方式SELECT出来的数据，如果右表数据为空，那么会给NULL

# 内连接INNER JOIN ... ON ...(等于与直接用JOIN)
## 语法和LEFT JOIN其实是一样的，只不过右表没有匹配的记录的情况下，最终的结果就不会出现左表的那一条数据
SELECT * FROM table_A LEFT JOIN table_B ON talbe_B.a_id = table_A.id;
SELECT * FROM table_A, table_B WHERE tableB.a_id =table_A.id;	# 设置可以不用join
```

##### 修改/更新

```mysql
## 更改某字段的值，特别需要注意的是，mysql和mariadb是没有update from的，sql server才有。更新的时候WHERE语句一定是在SET语句后面，而JOIN语句则是在SET语句前面
UPDATE 表名 SET 字段=新值,字段2=新值2 WHERE 条件;
UPDATE table_A, table_B SET table_A.a=table_B.a;
UPDATE table_A SET a=x,b=y,c=z;

## 更新中也能使用CASE，例如
UPDATE `table` SET `field` = CASE
		WHEN id = 1 THEN 2
END
WHERE id in (1,2,3);

# 更新的时候使用LEFT JOIN等语句
UPDATE `table`
LEFT JOIN ... ON ...
SET ...
```

##### 删除

```mysql
DELETE `deadline` FROM `deadline` LEFT JOIN `job` 	# 有LEFT JOIN情况时删除指定表的数据
```

##### 插入

```shell
# 插入数据
INSERT INTO 表名(属性列表) VALUES(值列表)
# 忽略重复的记录
INSERT IGNORE INTO ... 
# insert or update，插入或更新部分字段
INSERT INTO 表名 (属性列表) VALUES (值列表) ON DUPLICATE KEY UPDATE field_name=VALUES(field_name)
# 包含子查询的插入INSERT INTO SELECT，后面不用括号
INSERT INTO db_name(field1, field2) SELECT 'field1', `db_name2`.`field` FROM db_name2
```

### 锁

- 常用于：并发读写数据防止读写到错误的数据(例如，两个请求在两个事务中同时对同一个字段执行`+10`的操作，那么可能出现总共`+20`，也可能出现只`+10`的情况)
- `UPDATE`和`DELETE`语句本身就会对行加锁，但是`SELECT`默认不会，需要显式加锁
- `S`锁(共享锁，读锁)：如果在事务里面读取默认是读锁，该事务内无法对其进行修改(要修改必须获取X锁)，同时，其他事务也只能对该数据加S锁，不能加X锁。
- `X`锁(排他锁，写锁)：该事务内可以读写，其他事务在这其间不能对数据加任何的锁。

#### 悲观锁

默认认为需要修改的数据是会发生

- 共享锁：其他事务可读，但不可写

  ```mysql
  SELECT ... LOCK IN SHARE MODE       # 共享锁，其它事务可读，不可更新
  ```

- 排他锁：其他事务不可读写

  ```mysql
  SELECT ... FOR UPDATE       # 排它锁，其它事务不可读写
  ```

#### 乐观锁

- 具体实现逻辑其实是自己实现的
- 如果重试，对性能有一定的影响

默认认为需要修改的数据是不会发生冲突的，在更新之间是不会有任何锁的。

有些实现方法是单独加入了一个版本号码字段，但是如果是字段特殊，并且业务不大复杂，可以直接使用某个需要更新的字段作为版本，例如

```mysql
SELECT * FROM `user` WHERE `id`=1;	# 先普通查询出用户数据
UPDATE `user` SET `money` = `money` + 50 WHERE `id`=1 AND `money`=50;	# 在更新数据时候加上版本字段，这里可以直接使用需要更新的字段money
```

然后在更新操作执行完成后获取影响的行数，如果影响行数为0，表示更新操作不起作用，版本已经发生变化，这时候就需要用户自己去抛错或者编写重试逻辑(重试的时候会重新获取字段值即版本号)。

### 事务

- MySQL的几种事务隔离性:
  - READ UNCOMMITTED
  - READ COMMITTED
  - REPEATABLE READ: 默认的事务隔离级别，可重复读。
  - SERIALIZABLE

### 系统相关

```shell
# 更改密码
## 如果提示权限不足，可以先停止服务，然后这样启动service mysql start --skip-grant-tables
use mysql;
update user set password=PASSWORD('mysql') WHERE user="root";
update user set authentication_string=PASSWORD('mysql') WHERE user="root";	# MySQL5.7以后password字段改为了authentication_string字段
flush privileges;

# 查看用户权限
show grants for 用户名

# 打开远程登录权限，如果是CentOS7还需要打开防火墙firewall-cmd --add-port=3306/tcp
GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "mysql";
flush privileges;                更新权限
select host, user from user;     查看更改

# 查找系统常用变量
show global variables like 'log_error'; # 查看是否开启以及日志文件路径
SET GLOBAL general_log = 'ON';

# 记录下所有的sql命令
SHOW VARIABLES LIKE "general_log%"; SET GLOBAL general_log = 'ON';	# 临时解决方法，数据库重启后失效
bin-log = /tmp/mysql.log	# 能一直都开着

# 数据库编码
show variables like 'character%';	# 查看关于编码的几个变量
character_set_client				# 客户端编码方式
character_set_connection			# 建立连接使用的编码方式
character_set_database				# 数据库的编码
character_set_results				# 结果集的编码
character_set_server				# 数据库服务器的编码

# 设置数据库表名不区分大小写，vim /etc/mysql/my.cnf，在[mysqld]后面添加这句话，然后重启。如果要设置内容的大小写敏感，则是在数据表的字符集上进行设置，_ci表示大小写不敏感，_cs表示大小写敏感
lower_case_table_names=1

# 查询数据库数据存放目录
show variables like '%datadir%';

# 查看所有的警告
show warnings

select @@version	# 查看MySQL版本

# 查看表的结构
show columns from 表名;

# 查看当前连接数和客户端详情
show processlist;

# 查看最近一次死锁发生的原因
SHOW ENGINE INNODB STATUS;
select * from information_schema.innodb_trx;	# 查找当前所有的锁

# 获取数据库当前的时间/查看数据库时区
select curtime();
select now();
show variables like "%time_zone%"
```
### 数据库维护

- mysqldump参数
  - `--default-character-set=utf-8`指定导出的字符编码

```shell
# 备份整个数据库
mysqldump -u... -p... -h... -A > all.sql
mysqldump -uroot -pmysql --databases -h127.0.0.1 abc | gzip > test.sql.1.gz # 压缩，只能在本地进行压缩
mysqldump -u... -p... -h... dbname tablename > table.sql	# 备份单张表
mysqldump -u... -p... -h... -d dbname > db.sql # 备份数据库的结构
mysqldump -u... -p... -h... -d dbname tablename > table.sql # 备份单张表的结构


# 备份多个数据库
mysqldump -u... -p... -h... --databases data1 data2 > backup.sql

# 导入数据
mysql -uroot -pmysql db_name < test.sql
bunzip2 < db_filename.sql.bz2 | mysql -uroot -pmysql db_name

# 忘记密码时候'Access denied for user 'root'@'localhost'的时候，可以用这种方式修改root权限
sudo mysqld_safe --skip-grant-tables	# 这条命令能够登录进去，然后可以执行设置密码的操作
```

### binlog

数据库的sql日志。

使用`canal`可以很方便地监听数据库的所有操作。

### Hint

可以指定查询优化的方式

```shell
FORCE INDEX 	# 强制指定索引
IGNORE INDEX 	# 忽略指定索引
SQL_NO_CACHE 	# 关闭查询缓存，SELECT SQL_NO_CACHE FROM table
SQL_CACHE 		# 强制查询缓存
HIGH_PRIORITY	# 优先操作
LOW_PRIORITY	# 滞后操作
INSERT DELAYED	# 延时插入，INSERT DELAYED INTO table1...
STRAIGHT_JOIN	# 强制连接顺序
SQL_BUFFER_RESULT	# 强制使用临时表(可以很快地释放表锁)
SQL_BIG_RESULT/SQL_SMALL_RESULT	# 分组使用临时表

```

### 帮助函数

```mysql
# 字符串相关
left(str, length) # 字符串截取
right(str, length) # 字符串截取
substring(str, pos, len) # 字符串截取
concat(str1, str2)  # 字符串相加
group_concat('字段名')	# 将group by的结果的指定字段合并成一行，以逗号分割
substring_index('www.baidu.com','.', 1);	# 字符串分割，最后的数字表示取分割后的第几段，-1表示倒数
LENGTH(字段名)	# 获取某个字段的长度，可以这样实现按字段长度进行排序 select * from `test` order by LENGTH(`name`) 
FIND_IN_SET('123', field);	# 从逗号分割的字符串中查找目标 

# 数字相关
FLOOR()	# 取整
ROUND()	# 四舍五入

# 时间相关
CURDATE()			# 获取当前日期
CURRENT_DATE()		# 同上
CURRENT_TIMESTAMP()	# 获取当前时间戳
DATEDIFF('2018-08-08', '2019-08-08')	# 获取日期差，结果是天数，可以为负数
DATE_FORMAT(`create_timestamp`, '%Y%m%d') # 时间戳格式化，可以使用这个方法实现时间戳的按年按月的分组
YEAR(datetime)    # 获取年份
QUARTER(datetime)    # 获取季度数
MONTH(datetime)    # 获取月份
MONTHNAME(datetime)    # 获取月份名字
MONTHNAME(datetime)    # 获取星期名字(比如'Thursday')
WEEKDAY(datetime)    # 获取星期索引
WEEK(date, first)    # 获取当前是一周的第几天，first表示周几算一周的开始
DAYOFMONTH(datetime)  # 获取日期(几号)
DAYOFYEAR(date)    # 返回date在一年中的日数(1-366)
HOUR(datetime)    # 获取小时数
MINUTE(datetime)    # 获取分钟数
SECOND(datetime)    # 获取秒数
DATE_ADD(`field`, interval -1 day)	# 时间减一天
DATE_ADD(`field`, interval 1 week)	# 时间加一周

# 统计相关
SUM(field_name)	# 如果该字段所有的值都为空，那么会返回NULL，而不是0，可以这样做以保证在没有数据的时候返回预期的0: COALESCE(SUM(field_name), 0)
COUNT(field_name)
SUM(case when field='wang' then 1 else 0 end) as sum_if
COUNT(IF(field='wang',1,NULL)) as count_if	# 使用if做统计
COUNT(DISTINCT IF(field='wang', field2, NULL))	# COUNT配合DISTINCT和IF同时使用
COALESCE (field1, field2, field3)	# 只要其中有一个为NULL，表达式的值就为NULL，类似于some，用于判断几个字段是否都为NULL

# 逻辑相关
CASE 
	WHEN 'field' = 1 THEN 2
	WHEN 'field' = 2 THEN 3
	ELSE 'field' = 3 THEN 4
END;
## 或者
CASE field WHEN '1' THEN '2' WHEN '3' ELSE '4' END

IF(sex=1, '男', '女')				# if条件语句
IF(sex=1 OR field='b', 1, NULL)		# 复杂的

# 字符串处理
REPLACE(field_name, "search", "replace")	# 将search替换为replace，例如UPDATE `table` SET `value` = REPLACE(`value`, 'abc', 'def')
REGEXP_REPLACE(field_name, "search", "replace")	# 正则替换，但是是从mysql8.0开始才有的。另外几个相关的正则函数有NOT_REGEXP、REGEXP、REGEXP_INSTR、REGEXP_LIKE、REGEXP_SUBSTR、RLIKE

# JSON相关函数
JSON_ARRAY([])	# 将数组转换为json格式
JSON_ARRAYAGG(字段)	# 返回某个字段值组成的json格式数组
JSON_CONTAINS(field_name, '{"A":"B"}')	# JSON是否包含子文档，例如{"A":"B", "C": "D"}，包含了{"A":"B"}
JSON_KEYS(field_name)	# 获取json数据的所有key
JSON_EXTRACT(字段名,'$.id')	# 获取json数据key=id的值，需要注意的是，结果前后是带有双引号的可用json_unquote函数取消其双引号
JSON_MERGE_PRESERVE(@json1, @json2);	# 合并两个JSON，当key重复的时候，会将value当作数组来合并，功能和JSON_MERGE一样，但是JSON_MERGE快弃用了。一定一定要注意值为NULL的情况，如果@json1为NULL，那么无论@json2是怎样的数组，结果都为NULL
JSON_MERGE_PATCH(@json1, @json2);	# 合并两个JSON，当key重复的时候，会覆盖
JSON_REMOVE(@json1, '$.A'); # 移除指定的key，但是只能移除key->value形式的json数据，如果是数组，不支持用*或**来通配
```

## 数据库优化

### 常见性能问题及优化

- **COUNT(*)优化**: Innodb数据库中表的总行数并没有直接存储，而是每次都执行全表扫描，如果表太大简单的`COUNT(*)`则会非常耗时。这时候不妨选择某个字段添加一个辅助索引，依然会扫描全表，但是`COUNT(*)`的性能能提高很多。因为在使用主键或者唯一索引的时候，InnoDB会先把所有的行读到数据缓冲区，发生了多次IO，而使用了辅助索引以后，由于辅助索引保存的仅仅是index的值，虽然还是读了那么多行到缓冲区，但是数据量则大大减少，仅有一个字段，磁盘IO减少，所以性能提高了。
- **char和varchar**: Char是定长类型，对于经常变更的数据，一般采用CHAR来进行存储，因为CHAR类型在变化的时候不容易产生碎片。VARCHAR是变长类型，它比CHAR更节省空间。
- **使用ENUM枚举类型来代替字符串类型**
- **LIKE查询优化**: 如果是`abc%`型的`like`查询是能用到该字段的索引的，如果是前后都模糊搜索，那么最好是加一个有索引的字段进行筛选，例如时间
- **对于Limit语句，即使where条件有索引，在数据量太大的时候仍然会有问题**: 例如，`LIMIT 10000000000 10`即使只取10条数据依然会很慢，好的做法是每次查询将上一次查询的末尾值拿到，然后在下次查询的时候将该值放入查询中，例如`WHERE time > 'xxx' ORDER BY time LIMIT 10`即可。
- **`wait_timeout`设置**: 最好将全局的`wait_timeout`设置为120，防止因为慢sql太多导致数据库性能变慢，特别是针对大企业的公共数据库。并且连接自己设置的`wait_timeout`依然首先会受到全局设置的影响，当`wait_timeout`超时后会出现**2013: Lost connection to MySQL server during query**错误

### 索引类型

#### 唯一索引

- **注意唯一索引不能建在可以为NULL的字段上，否则，唯一该唯一索引在NULL上不会生效，可以参考底部关于软删除的文章**

#### 聚簇索引(clustered index)

- 索引必须为唯一索引，局促索引不一定是主键，但是主键一定是局促索引
- 叶子结点存储的是整行数据，所以查询速度非常快
- 如果没有主见，那么聚簇索引可能是第一个不允许为null的唯一索引

保存了每一样的所有数据，聚簇索引的选择方法如下:

```shell
1.如果表中定义了PRIMARY KEY，那么InnoDB就会使用它作为聚簇索引；
2.否则，如果没有定义PRIMARY KEY，InnoDB会选择第一个有NOT NULL约束的唯一索引作为PRIMARY KEY，然后InnoDB会使用它作为聚簇索引
3.如果表中没有定义PRIMARY KEY或者合适的唯一索引。InnoDB内部会在含有行ID值的合成列生成隐藏的聚簇索引。这些行使用InnoDB赋予这些表的ID进行排序。行ID是6个字节的字段，且作为新行单一地自增。因此，根据行ID排序的行数据在物理上是根据插入的顺序进行排序
```

#### 辅助索引(secondary index)

聚簇索引以外的就是辅助索引，辅助索引的每一行记录都包含每一行的主键列，辅助索引指向主键，想较于聚簇索引，由于只有一个字段，所以空间占用非常少。当然这就导致肯定需要回表查询，即拿着聚簇索引去查找该行数据

#### 覆盖索引

当sql语句的所求查询字段（select列）和查询条件字段（where子句）全都包含在一个索引中 **（联合索引）**，可以直接使用索引查询而不需要回表。

### 排序算法

#### filesort文件排序

文件排序是通过相应的排序算法，把所有的数据拿出来之后在内存中进行排序。使用firlesort排序主要是因为where语句与order by语句使用了不同的索引；order by中的列的索引不同；对索引同时使用ASC和DESC；left join使用右表字段排序等。

## TroubleShooting

- **启动错误，提示server PID file could not be found**

  一般是因为MySQL服务卡死了，此时查看进程`ps aux | grep mysql*`，然后把卡死的给kill掉就行了

- **Access denied for user 'root'@'localhost'**

  出现这种情况，可能是给用户分配了'%'权限，而没有分配localhost权限，我去...

- **WorkBench保持连接不断开**: `Edit->Preferences->SQL Editor，设置DBMS connection read time out(in seconds)`


*   关于整型数据长度问题，需要注意的是MySQL里面的整型后面跟的长度并不是指该字段的实际长度，而是客户端显示的长度，实际存储的长度可以更长。这是几个整型数据对应的长度表(来自[MySQL官网](http://dev.mysql.com/doc/refman/5.7/en/integer-types.html))，所以`INT`无论后面定义的是多少，都是4个字节32位的长度

| Type      | Storage | Minimum Value         | Maximum Value        |
| --------- | ------- | --------------------- | -------------------- |
|           | (Bytes) | (Signed/Unsigned)     | (Signed/Unsigned)    |
| TINYINT   | 1       | -128                  | 127                  |
|           |         | 0                     | 255                  |
| SMALLINT  | 2       | - 32768               | 32767                |
|           |         | 0                     | 65535                |
| MEDIUMINT | 3       | - 8388608             | 8388607              |
|           |         | 0                     | 16777215             |
| INT       | 4       | - 2147483648          | 2147483647           |
|           |         | 0                     | 4294967295           |
| BIGINT    | 8       | - 9223372036854775808 | 9223372036854775807  |
|           |         | 0                     | 18446744073709551615 |


* **MySQL分页时出现数据丢失或者数据重复的情况**: 如果分页的时候用上了`order_by`并且目标字段并不是索引字段，那么就有可能出现这种情况，一条数据可能既出现在上一页，又出现在下一页。原因是在`mysql5.6`以后，`priority queue`使用的是堆排序，这个排序算法并不稳定，两个相同的值可能在两次排序后的结果不一样。解决方法有两种，一种是给`order_by`后面的字段加索引，另外一种是增加一个是索引的字段，但是不要把主键放到这里面，否则两个索引都不会使用，导致性能非常低，别问我为什么，我被坑过。[参考文章](http://www.foreverlakers.com/2018/01/mysql-order-by-limit-%E5%AF%BC%E8%87%B4%E7%9A%84%E5%88%86%E9%A1%B5%E6%95%B0%E6%8D%AE%E9%87%8D%E5%A4%8D%E9%97%AE%E9%A2%98/)

* **在查询整型字段的时候空字符串表现得和0一样**: 这是MySQL的特性，对于整型字段，空字符串会自动转换成零。另外，对于`timestamp`字段`''`和`0000-00-00 00:00:00`表现得一样，插入`NULL`到不能为`NULL`的`timestamp`字段时，既不会报错又不会插入空值，而是会变成当前的时间。**插入''和使用''去读取可能会有warning，甚至mysql和mariadb表现不同，可能导致查询不到数据，所以建议都用0000-00-00 00:00:00**

* **timestamp字段插入的时候出现`warnning: data truncated for column`**，这是因为`mysql`的`timestamp`类型不是`unix`的时间戳，对于非法的字符串插入`timestamp`的时候结果都是`0000-00-00 00:00:00`。如果要插入，可以用`2017-12-25 12:00:00`这种格式，或者使用函数`FROM_UNIXTIME(1514177748)`进行转换。

* **Invalid use of NULL value**: 原因可能是在将列修改为不允许NULL的时候并且已经存在记录该值为null，则不允许修改，这个时候需要先修改已有记录的值。

* **PhpMyAdmin查询正确，但是导出结果时导出的文件里面只有一条错误的sql语句**: 尝试把要导出的字段及表名不用别名

* **2038问题**: 由于历史原因，`TIMESTAMP`最多只能存储到`2038-01-19 05:14:07`，超过则会报错或者被置为NULL，目前暂时还没有解决办法，但是我相信到时候那帮牛人肯定会直接在数据库程序层面解决的，而不是我们去更改程序。当然，如果用`DATETIME`倒是可以多存储到子子孙孙那里，但是却没有时区概念。现在距离那个时间点还有20年，我的建议是，如果字段是作为创建时间、更新时间、删除时间这种，精度要求比较高并且时区不允许错乱(事实上，所有项目时区都是要有要求的，不能保证每个人使用或者每个服务器的时区是一样的)，就可以用`TIMESTAMP`，像记录某个历史事件、或者万年历、生日这种才需要用`DATETIME`

* **[Table is specified twice, both as a target for 'UPDATE' and as a separate source for data in mysql](https://stackoverflow.com/questions/44970574/table-is-specified-twice-both-as-a-target-for-update-and-as-a-separate-source)**: 在`10.1.24-MariaDB`有问题，但是`10.3.7-MariaDB`上没有问题，应该跟版本有关，解决办法就是在子查询外面再嵌套一层`select * 表名 as 新表名`。

* **column "c.name" must appear in the GROUP BY clause or be used in an aggregate**: 见于SQL与MySQL语法不兼容的情况，在SQL3标准以前，选择显示的字段必须出现在`GROUP BY`中。解决办法要么是将该字段加入`GROUP BY`，要么在子查询中完成聚合，在外部在获取字段。

* **数据写入成功但是却读取不到**: 其中一种原因是使用`mysqldump`进行备份的时候，默认会给数据表加锁，此时如果写入数据，那么主库会写入成功(肯定是在从库进行dump)，但是此时从库上了锁，数据更新有延迟。解决办法是错开高并发写入的时间进行备份，另一种是使用不会锁表的备份方式

* **如何实现上一篇下一篇功能**: 直接在排序好的基础上用大于小于即可，例如:

  ```mysql
  SELECT * FROM `posts` WHERE id=3;
  SELECT * FROM `posts` WHERE id>3 LIMIT 1;
  SELECT * FROM `posts` WHERE id<3 LIMIT 1;
  ```

* **Row size too large. The maximum row size for the used table type, not counting BLOBs, is 65535. You have to change some columns to TEXT or BLOBs**，这是一行的长度超过了65535个字节的限制，一般是因为字段过大或者字段过多，例如`varchar(255)`就能存储255个字符，然而一个字符要占3个字节，就相当于有765个字节了。遇到这种情况，首先应该按实际情况减少部分字段的长度，如果字段不能减少，长度仍然不能减少，就只有用`TEXT`或者`BLOBs`来存储部分字段了，这两种类型不算在65535内。

* **User 'xxx' has exceeded the 'max_user_connections' resource (current value: 10)**，原因是超出了设置的单个用户的最大连接数(可以使用`select @@max_user_connections;`进行查看)，默认为0表示无限制，单如果大于零并且超过了就会出现该错误。可以这样修改`set  @@global.max_user_connections=1;`

* **某个语句一直卡住，或者无法修改表结构，但是又找不到表锁**，可能的原因是客户端有未关闭或提交的事务，会出现`waiting for table metadata lock`，可以先使用`select * from information_schema.innodb_trx;`查看当前有哪些事务锁，然后用`KILL thread_id`杀掉该锁进程。

* **Mariadb/Mysql不锁表实时添加列**: `10.2`开始是默认支持的，但是只能在表最后一列后加，不能出现`after`，参考https://mariadb.com/kb/en/library/instant-add-column-for-innodb/

* **mysqldump出现Access denied for user xxx when using LOCK TABLES**: 可以在`mysqldump`命令添加上`--single-transaction`参数

* **将逗号分割的字符串转换为Array的形式**: 

  ```mysql
  SELECT
    CAST( 
      CONCAT('["', REPLACE(REPLACE(`field`, '"', '\"'), ',', '","'), '"]')
      AS JSON
    );
  ```

##### 扩展阅读

- [记一次神奇的Mysql死锁排查](https://juejin.im/post/5c774114f265da2d993d9908): 一种非常隐蔽的发生死锁的情况。
- [软删除之痛](https://blog.wolfogre.com/posts/trap-of-soft-delete/): 软删除很好用，但还是具体场景具体分析，不要一味地用，需要考虑数据是否有软删的必要，和如何解决软删的副作用