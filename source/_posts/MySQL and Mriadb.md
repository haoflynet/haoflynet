---
title: "MySQL／MariaDB 教程"
date: 2016-08-07 11:01:30
updated: 2016-10-11 09:02:00
categories: database
---
# MySQL/MariaDB使用教程
## 安装方法
**CentOS**：[使用yum安装MariaDB](https://mariadb.com/kb/zh-cn/installing-mariadb-with-yum/)，CentOS安装client直接yum install mysql而不是client，而安装mysql则直接用`yum install -y mysql mysql-server mysql-dev mysql-devel`，CentOS7上已经用mariadb代替了mysql，这样子使用：

	yum install mariadb-server mariadb mariadb-devel -y
	systemctl start mariadb.service # 启动服务
	systemctl enable mariadb.service	# 开机启动
Ubuntu(Raspberry):

```shell
sudo apt install mariadb-server mariadb-client
```

## 常用命令

### 增删改查

	# 创建数据库，如果是gbk编码，分别用gbk、gbk_chinese_ci;
	CREATE DATABASE 库名 CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci; 
	CREATE DATABASE 库名 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
	
	# 执行sql文件
	mysql -uroot -pmysql --default-character-set=gbk  jpkc_db < jpkc_db.sql # 这里可以执行编码格式
	
	# 修改字段
	ALTER TABLE 表名 CHANGE COLUMN 列名 新的列名 属性;	# 修改列属性
	
	# 外键约束操作
	ALTER TABLE 表明 DROP FOREIGN KEY '外键名';			# 删除外键
	
	TRUNCATE tablename	# 清空数据表
### 系统相关

	# 更改密码
	如果提示权限不足，可以先停止服务，然后这样启动service mysql start --skip-grant-tables
	use mysql;
	update user set password=PASSWORD('mysql') WHERE user="root";
	flush privileges;
	
	# 查找系统常用变量
	show global variables like 'log_error'; # 日志文件路径
	
	# 记录下所有的sql命令
	bin-log = /tmp/mysql.log	# 直接在配置文件里面
### 数据库维护

	# 备份整个数据库
	mysqldump -u... -p... -h... -A > all.sql
	mysqldump -uroot -pmysql --databases -h127.0.0.1 abc | gzip > test.sql.1.gz # 压缩，只能在本地进行压缩
	
	# 备份多个数据库
	mysqldump -u... -p... -h... --databases data1 data2 > backup.sql


## TroubleShooting
### 启动错误，提示server PID file could not be found
一般是因为MySQL服务卡死了，此时查看进程`ps aux | grep mysql*`，然后把卡死的给kill掉就行了
### Access denied for user 'root'@'localhost'
出现这种情况，可能是给用户分配了'%'权限，而没有分配localhost权限，我去...



*   数据库的增删改查  

*   # 创建数据库


    # 插入一组数据
    INSERT INTO 表名(属性列表) VALUES(值列表)
    INSERT IGNORE INTO ...  # 忽略重复的记录
    
    # 更改某字段的值
    UPDATE 表名 SET 字段=新值 WHERE 条件
    
    # 删除数据库
    drop database User;
    # 清空数据表
    DELETE FROM 表名; # 这种方式比较慢，但是可以恢复
    TRUNCATE TABLE 表名 # 这种方式很快，但不会产生二进制日志，无法回复数据
    
    # 给表添加字段
    ALTER TABLE 表名 ADD 字段名 属性
    # 给表删除字段
    ALTER TABLE 表名 DROP COLUMN 字段名  


* 常用函数  


        left(str, length) # 字符串截取
    right(str, length) # 字符串截取
    substring(str, pos, len) # 字符串截取
    concat(str1, str2)  # 字符串相加
    
    # 关于时间
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


* workbench使用：  


        # 保持连接不断开：
    Edit->Preferences->SQL Editor，设置DBMS connection read time out(in seconds)

* 查询语句的技巧  


        # 多表子查询
    update table_1 as a, (select id from biao_2 where name='a') as b set a.title='xx' where a.id=b.id
    
    # 随机读取数据库记录
    SELECT * FROM table WHERE id >= (SELECT FLOOR(RAND() * (SELECT MAX(id) FROM table))) ORDER BY id LIMIT 1
    
    # 分页功能，获取m开始的n条记录
    SELECT * FROM table_name limit m, n

* MySQL配置  


        # 设置数据库不区分大小写，vim /etc/mysql/my.cnf
    在[mysqld]后面添加：lower_case_table_names=1，然后重启
    
    # 打开远程登录权限
    GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "mysql";
    flush privileges;                更新权限
    select host, user from user;     查看更改
    
    # 新建用户
    grant 权限 on 数据库名.表名 用户名@主机地址identified by "密码";
    
    # 修改用户密码
    update mysql.user set password=PASSWORD('新密码') where user='root';
    flush privileges;
    
    # 查看用户权限
    show grants for 用户名

* 查询数据库信息  


        # 查询数据库数据存放目录
    show variables like '\%datadir\%';
    
    # 查看所有的警告
    show warnings
    
    # 查看MySQL版本
    select @@version
    
    # 查看表的结构
    show columns from 表名;
    
    # 修改表的字符集
    alter table 表名 convert to character set utf8 collate utf8_general_ci;


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
