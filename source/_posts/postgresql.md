---
title: "PostgreSQL 使用手册"
date: 2021-03-30 08:32:00
updated: 2021-06-30 22:45:00
categories: Database
---

最近在学习AWS的Redshift，它是基于`PostgreSQL`的，顺便学习下。

## 安装PostgreSQL

## 配置

- 默认端口为5432，默认用户名为`postgres`

### 系统表

- `pg_class`: 记录数据库中的表，索引及视图
- `pg_namespace`: 记录数据库中的名字空间
- `pg_attribute`: 记录数据库中表的字段的详细信息。(`attname`字段名字，`atttypid`字段类型id，`attlen`字段长度，`attnotnull`)
- `pg_type`: 记录数据库中所有的数据类型
- `pg_description`: 记录数据库中对象的注释(表以及字段)。(`objoid`对象ID，`objsubid`字段号，`description`描述)

<!--more-->

### 索引

- Redshift不能像PostgreSQL那样创建索引，但是提供了一个类似的功能`sort key`，该功能可以和传统数据库一样能够优化存储与查询方面的性能

## 增删该查

### 数据库操作

### 数据表操作

- [PostgreSQL中的数据类型](http://patchouli-know.com/2016/12/15/data-types-in-postgresql/)
- 如果是自增类型，从10开始推荐使用`IDENTITY`。之前是用`serial/serial8`类型

```mysql
# 使用表名查询表字段的定义
SELECT a.attnum,
       a.attname AS field,
       t.typname AS type,
       a.attlen AS length,
       a.atttypmod AS lengthvar,
       a.attnotnull AS notnull,
       b.description AS comment
  FROM pg_class c,
       pg_attribute a
       LEFT OUTER JOIN pg_description b ON a.attrelid=b.objoid AND a.attnum = b.objsubid,
       pg_type t
 WHERE c.relname = '表名'
       and a.attnum > 0
       and a.attrelid = c.oid
       and a.atttypid = t.oid
 ORDER BY a.attnum
 
# 添加注释，在创建的时候不能添加，只能用不同的语句加注释
COMMENT ON TABLE users IS "This is user table" # 给表添加注释
COMMENT ON COLUMN users.userid IS 'This is user ID';	# 给表字段添加注释

ALTER TABLE test DROP COLUMN name;	# 删除字段
ALTER TABLE test ADD COLUMN name VARCHAR(255);	# 添加字段

```

### 数据操作

#### 查询记录

```mysql
SELECT * FROM COMPANY LIMIT 3 OFFSET 2;	# 分页操作，limit操作
```

#### 新增记录

#### 更新记录

#### 删除记录

### 事务

```mysql
BEGIN;
other sql;
COMMIT;
```

## TroubleShooting

- **ProgrammingError: Statement is too large. Statement Size: 40000000 bytes. Maximum Allowed: 16777216 bytes**: 这是因为`PostgreSQL`默认设置最大的sql语句为16M，所以尽量一条语句的大小尽量控制在这之下

- **Permission denied for relation**: 那是因为该用户没有表的访问权限，可以这样做:

  ```mysql
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to test;	# 分配所有公共表权限
   GRANT ALL PRIVILEGES ON TABLE table-name TO test;	# 分配指定表的权限
  ```

- **Unique violation: 7 ERROR: duplicate key value violates unique constraint "users_pkey"**
  尝试执行以下命令重置一下主见索引，原理见[stackoverflow](https://stackoverflow.com/questions/37970743/postgresql-unique-violation-7-error-duplicate-key-value-violates-unique-const)：

  ```shell
  SELECT setval(pg_get_serial_sequence('users', 'id'), coalesce(max(id)+1, 1), false) FROM users;
  ```

  

##### 扩展阅读

[PostgreSQL 9.6.0中文手册](http://www.postgres.cn/docs/9.6/index.html)