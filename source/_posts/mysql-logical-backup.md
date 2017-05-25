---
title: "MySQL逻辑备份过程"
date: 2014-11-04 22:19:36
updated: 2017-05-19 14:50:00
categories: 编程之路
---
MySQL的逻辑备份是使用`mysqldump`命令(文本备份，而非二进制备份)来从数据库中提取数据，并将结果写到一个纯文本上，就是我们平常用`mysqldmin`到处的.sql格式的文件，里面是SQL语句。正是如此，逻辑备份可以在MySQL正在运行时执行，并且可以做到不锁表备份(也可以声明锁定)，一般用于数据迁移或者数据量很小时。

# 备份

下面的命令是直接在linux的cmd里执行，而不是mysql的shell

```shell
mysqldump -q --single-transaction -A -u root -p > all.sql # 导出所有数据库到all.sql
mysqldump -q --single-transaction -u root -p user > user.sql # 导出user数据库
mysqldump -q --single-transaction -u root -p user admin > admin.sql # 导出user数据库里名为admin的表
mysqldump -q -d --skip-triggers user admin-u root -p > admin.sql  # 导出user数据库里名为admin的表的结构
mysqldump -q -d --skip-triggers user -u root -p > jiego.sql   # 导出user数据库的结构
```

其中mysqldump的常用参数如下：

```shell
-B：导出多个数据库
-E：把事件events一起导出
-R：把存储过程routines一并导出
-q：快速模式，不把查询结果显示在终端
--default-character-set=utf8：这点很重要，因为大量的数据库默认都会是utf8
--flush-logs：生成新的二进制日志文件，主要用于增量备份，恢复数据，增量备份必须加此选项，否则会丢失              数据
--lock-all-tables：锁住全局表，会出现写操作等待
--single-transaction：设置本次会话隔离级别为REPEATABLE READ，确保本次会话时，不会看到其他会话已提交了的数据
--triggers：把触发器一并导出，默认开启了此选项的
```

**注**：需要注意的是，在5.5之后，mysqldump默认无法备份`performance_schema`这个数据库，但是可以通过`—databases`指定名字和`--skip-lock-tables`的方式来备份，但是不知道为什么，虽然能备份但是还是会给出错误信息。`performance_schema`是新增的mysql的性能监视引擎，所以我认为不备份也行，本来默认也是关闭的，因为数据库迁移或者恢复的时候可以不用看之前的这些的，有什么问题看系统日志就行了，具体的请参见[官方手册](http://dev.mysql.com/doc/refman/5.5/en/mysqldump.html)。

### 在slave里备份

MySQL5.5之后mysqldump增加了一个参数`--dump-slave`，可以在slave端dump数据，并且可以建立新的slave，可大大降低主服务器的压力。

# 恢复

假设有一个数据库结构的备份文件user.sql，那么可以 在mysql的shell里面执行如下命令

```shell
create database User;     # 首先得创建一个数据库
use User;                 # 选择该数据库
source /root/User.sql;    # 导入sql文件
show tables;              # 查看是否创建成功
```

也可以在创建相应数据后后在linux的shell里执行(在外面创建数据库我没找到方法)

```shell
mysql -u root -p user < user.sql
```