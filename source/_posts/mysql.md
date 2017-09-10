---
title: "MySQL／MariaDB 教程"
date: 2016-08-07 11:01:30
updated: 2017-09-05 18:02:00
categories: database
---
## 安装方法
**CentOS**：[使用yum安装MariaDB](https://mariadb.com/kb/zh-cn/installing-mariadb-with-yum/)，CentOS安装client直接yum install mysql而不是client，而安装mysql则直接用`yum install -y mysql mysql-server mysql-dev mysql-devel`，CentOS7上已经用mariadb代替了mysql，这样子使用：

```shell
yum install mariadb-server mariadb mariadb-devel -y
systemctl start mariadb.service # 启动服务
systemctl enable mariadb.service	# 开机启动
```
Ubuntu: 

```shell
sudo apt-get install mariadb-server mariadb-client libmariadbd-dev

# 如果是开发，还需要安装
sudo apt-get install libmariadb-client-lgpl-dev
sudo ln -s /usr/bin/mariadb_config /usr/bin/mysql_config

# 第一次登录使用
sudo mysql -u root
```

## 常用命令

### 增删改查

#### SQL文件操作

```shell
# 执行sql文件
mysql -uroot -pmysql --default-character-set=gbk  jpkc_db < jpkc_db.sql # 这里可以执行编码格式
```

#### 数据库操作

```shell
## 创建数据库，如果是gbk编码，分别用gbk、gbk_chinese_ci;
CREATE DATABASE 库名 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
TRUNCATE tablename	# 清空数据表
DROP database_name	# 删除数据库
```

#### 数据表操作

```shell
ALTER TABLE 表明 DROP FOREIGN KEY '外键名';		# 删除外键
## 清空数据表
DELETE FROM 表名; # 这种方式比较慢，但是可以恢复
TRUNCATE TABLE 表名 # 这种方式很快，但不会产生二进制日志，无法回复数据
## 给表添加字段
ALTER TABLE 表名 ADD 字段名 属性
## 给表删除字段
ALTER TABLE 表名 DROP COLUMN 字段名  
# 修改列属性
ALTER TABLE 表名 CHANGE COLUMN 列名 新的列名 属性;	
```

#### 数据记录操作

##### 查询

```mysql
# 普通查询
SELECT * FROM table_A
SELECT * FROM ... BETWEEN value1 AND value2
SELECT * FROM ... NOT BETWEEN value1 AND value2
# 分组查询
SELECT count(column_a) as count FROM table_A GROUP_BY coulumn_b

# 多表子查询
## 需要注意的是，子查询后面必须要AS一个别名
update table_1 as a, (select id from biao_2 where name='a') as b set a.title='xx' where a.id=b.id

# 随机读取数据库记录
SELECT * FROM table WHERE id >= (SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table))) ORDER BY id LIMIT 1

# 分页功能，获取m开始的n条记录
SELECT * FROM table_name limit m, n

# 模糊查询
SELECT * FROM table_name like '%abc_';	# 模糊查询，其中%贪婪匹配任意数量的任意字符，_匹配一个任意字符

# 分组GROUP BY
SELECT * FROM table_name GROUP BY 'field';	# 分组显示，有多少不同的field就会有多少条记录，而其他的字段则是随机选择一条记录显示，当然，如果对其他字段进行SUM等操作，那么就可以获取分类的SUM，十分有用
```
##### 连表查询

```shell
# LEFT JOIN ... ON ...
## 会取出左表的全部记录，即使右表没有对应匹配的记录。用这种方式SELECT出来的数据，如果右表数据为空，那么会给NULL

# INNER JOIN ... ON ...
## 语法和LEFT JOIN其实是一样的，只不过右表没有匹配的记录的情况下，最终的结果就不会出现左表的那一条数据
```

##### 修改/更新

```mysql
## 更改某字段的值，特别需要注意的是，mysql和mariadb是没有update from的，sql server才有。更新的时候WHERE语句一定是在SET语句后面，而JOIN语句则是在SET语句前面
UPDATE 表名 SET 字段=新值 WHERE 条件;
UPDATE table_A, table_B SET table_A.a=table_B.a;

## 更新中也能使用CASE，例如
UPDATE `table` SET `field` = CASE
		WHEN id = 1 THEN 2
END
WHERE id in (1,2,3);
```

##### 删除

##### 插入

```shell
# 插入数据
INSERT INTO 表名(属性列表) VALUES(值列表)
# 忽略重复的记录
INSERT IGNORE INTO ... 
```

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
show global variables like 'log_error'; # 日志文件路径

# 记录下所有的sql命令
bin-log = /tmp/mysql.log	# 直接在配置文件里面

# 数据库编码
show variables like 'character%';	# 查看关于编码的几个变量
character_set_client				# 客户端编码方式
character_set_connection			# 建立连接使用的编码方式
character_set_database				# 数据库的编码
character_set_results				# 结果集的编码
character_set_server				# 数据库服务器的编码

# 设置数据库不区分大小写，vim /etc/mysql/my.cnf，在[mysqld]后面添加这句话，然后重启
lower_case_table_names=1

# 查询数据库数据存放目录
show variables like '%datadir%';

# 查看所有的警告
show warnings

# 查看MySQL版本
select @@version

# 查看表的结构
show columns from 表名;
```
### 数据库维护

```shell
# 备份整个数据库
mysqldump -u... -p... -h... -A > all.sql
mysqldump -uroot -pmysql --databases -h127.0.0.1 abc | gzip > test.sql.1.gz # 压缩，只能在本地进行压缩

# 备份多个数据库
mysqldump -u... -p... -h... --databases data1 data2 > backup.sql

# 导入数据
mysql -uroot -pmysql db_name < test.sql
bunzip2 < db_filename.sql.bz2 | mysql -uroot -pmysql db_name

# 忘记密码时候'Access denied for user 'root'@'localhost'的时候，可以用这种方式修改root权限
sudo mysqld_safe --skip-grant-tables	# 这条命令能够登录进去，然后可以执行设置密码的操作
```

### 帮助函数

```mysql
# 字符串相关
left(str, length) # 字符串截取
right(str, length) # 字符串截取
substring(str, pos, len) # 字符串截取
concat(str1, str2)  # 字符串相加

# 时间相关
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

# 统计相关
SUM(field_name)
COUNT(field_name)
SUM(case when field='wang' then 1 else 0 end) as sum_if
COUNT(IF(field='wang',1,NULL)) as count_if	# 使用if做统计

# 逻辑相关
CASE 
	WHEN 'field' = 1 THEN 2
	WHEN 'field' = 2 THEN 3
	ELSE 'field' = 3 THEN 4
END;

IF(sex=1, '男', '女')				# if条件语句
IF(sex=1 OR field='b', 1, NULL)		# 复杂的

# 字符串处理
REPLACE(field_name, "search", "replace")	# 将search替换为replace，正则搜索，例如UPDATE `table` SET `value` = REPLACE(`value`, 'abc', 'def')
```

## TroubleShooting

- **启动错误，提示server PID file could not be found**

  一般是因为MySQL服务卡死了，此时查看进程`ps aux | grep mysql*`，然后把卡死的给kill掉就行了

- **Access denied for user 'root'@'localhost'**

  出现这种情况，可能是给用户分配了'%'权限，而没有分配localhost权限，我去...

- **WorkBench保持连接不断开**: `Edit->Preferences->SQL Editor，设置DBMS connection read time out(in seconds)`


*   关于整型数据长度问题，需要注意的是MySQL里面的整型后面跟的长度并不是指该字段的实际长度，而是客户端显示的长度，实际存储的长度可以更长。这是几个整型数据对应的长度表(来自[MySQL官网](http://dev.mysql.com/doc/refman/5.7/en/integer-types.html)):

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

    所以`INT`整型无论后面定义的多少，都是4个字节32位的长度.
