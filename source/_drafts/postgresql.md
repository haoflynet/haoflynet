---
title: "PostgreSQL 使用手册"
date: 2018-08-02 14:32:00
updated: 2018-08-03 10:18:00
categories: Database
---

最近在学习AWS的Redshift，它是基于`PostgreSQL`的，顺便学习下。

## 安装PostgreSQL

<!--more-->

## 配置

### 系统表

- `pg_class`: 记录数据库中的表，索引及视图
- `pg_namespace`: 记录数据库中的名字空间
- `pg_attribute`: 记录数据库中表的字段的详细信息。(`attname`字段名字，`atttypid`字段类型id，`attlen`字段长度，`attnotnull`)
- `pg_type`: 记录数据库中所有的数据类型
- `pg_description`: 记录数据库中对象的注释(表以及字段)。(`objoid`对象ID，`objsubid`字段号，`description`描述)

### 索引

- Redshift不能像PostgreSQL那样创建索引，但是提供了一个类似的功能`sort key`，该功能可以和传统数据库一样能够优化存储与查询方面的性能

## 增删该查

### 数据库操作

### 数据表操作

- [PostgreSQL中的数据类型](http://patchouli-know.com/2016/12/15/data-types-in-postgresql/)

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
```

### 数据操作

#### 查询记录

```mysql
SELECT * FROM COMPANY LIMIT 3 OFFSET 2;	# 分页操作，limit操作
```

####新增记录

#### 更新记录

#### 删除记录

### 事务

```mysql
BEGIN;
other sql;
COMMIT;
```



##### 扩展阅读

[PostgreSQL 9.6.0中文手册](http://www.postgres.cn/docs/9.6/index.html)