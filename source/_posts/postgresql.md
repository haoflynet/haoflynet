---
title: "PostgreSQL 使用手册"
date: 2021-03-30 08:32:00
updated: 2023-04-21 12:45:00
categories: Database
---

最近在学习AWS的Redshift，它是基于`PostgreSQL`的，顺便学习下。

## 安装PostgreSQL

```shell
sudo apt-get install -y postgresql	# 安装后默认就启动了的
sudo apt-get install -y postgresql-client postgresql-client-common # 安装命令行客户端

# 完整卸载postgresql
sudo systemctl stop postgresql 	# 注意如果已经启动了postgresql必须在重装前将其停止，否则5432端口被占用后重新安装的实例默认会是5433端口
sudo apt-get --purge remove postgresql\* -y && sudo rm -rf /etc/postgresql-common/ && sudo rm -rf /etc/postgresql/
```

## 配置

- 默认端口为5432，默认用户名为`postgres`
- Mysql安装postgres命令行工具pg_dump等: `brew install libpq`
- 配置文件默认在: `/etc/postgresql/{version}/main/postgresql.conf`，配置文件修改后需要重启`sudo systemctl restart postgresql`
  - 监听`0.0.0.0`，需要修改`listen_addresses = 'localhost'为listen_addresses = '*'`


### 系统表

- `pg_class`: 记录数据库中的表，索引及视图
- `pg_namespace`: 记录数据库中的名字空间
- `pg_attribute`: 记录数据库中表的字段的详细信息。(`attname`字段名字，`atttypid`字段类型id，`attlen`字段长度，`attnotnull`)
- `pg_type`: 记录数据库中所有的数据类型
- `pg_description`: 记录数据库中对象的注释(表以及字段)。(`objoid`对象ID，`objsubid`字段号，`description`描述)

<!--more-->

### 索引

- Redshift不能像PostgreSQL那样创建索引，但是提供了一个类似的功能`sort key`，该功能可以和传统数据库一样能够优化存储与查询方面的性能

### 系统管理

- 角色和用户是不同的，角色相当于一批用户，类似于岗位，比如开发者角色等

```shell
-- 注释 # 注释就用--来写

SELECT version();	# 获取数据库版本

# sudo apt-get install postgresql-client，命令行得先安装客户端，但是客户端的版本必须和服务端的版本一致，这就很麻烦了
psql -U postgres -h xxx -w --password	# 使用命令行登录postgres数据库

select pg_size_pretty(pg_database_size('tablename')) as size;
pg_dump -U username your_database > db_dump.bak	# 备份数据库，导出数据库
psql -U postgres -h xxx 数据库名 < db_dump.back # 恢复restore数据库，该数据库需要先创建

SELECT * FROM pg_stat_activity;	# 检查当前有哪些session，哪些连接
select pg_terminate_backend(pid) from pg_stat_activity; # 删除某个session
select pg_size_pretty(pg_database_size('dbname')) as size; # 查询数据库大小/容量

SELECT * FROM pg_stat_replication; # 查看主从复制状态

\du	# 获取当前系统所有的角色roles
SELECT * FROM pg_roles;	# 同上
SELECT * FROM information_schema.role_table_grants WHERE grantee = '角色名';	# 查询一个角色在哪些表有权哪些权限，也可以用\z命令查看不过没这么直观
```

## 增删该查

### 数据库操作

```shell
# postgres shell中执行
\list	# 列出当前的数据库，这里不要加分号。等同于SELECT * from pg_database;
\c 数据库名 # 切换数据库
\dt	# 列出当前的表

DROP DATABASE name; # 删除数据库

# 如果是sql语句，必须加分号，且关键字必须大写
CREATE DATABASE 数据库名;	# 创建数据库，那些
CREATE USER 用户名 WITH ENCRYPTED PASSWORD '密码';	# 创建用户
ALTER USER postgres WITH ENCRYPTED PASSWORD '新密码'; # 修改用户密码
GRANT ALL PRIVILEGES ON DATABASE 数据库名 TO 用户名;	# 给用户分配某个数据库的权限

# 给某个用户分配某个db的权限，注意这里的schema是固定写public，缺少权限可能报错ERROR: permission denied for relation tablename

\c 数据库名;	# 写切到该数据库
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to username;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to username;
```

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
SELECT * FROM sfdc_contact WHERE "last_name"='Acevedo' AND "first_name"='Antonio';	# 字段名用双引号，字段值用单引号

# json字段查询
SELECT * FROM users, jsonb_array_elements(users.data) r WHERE r->>'name' = 'value';	# 如果users表的data字段是一个数组，可以用这种方式查询数组的key value
SELECT * FROM users WHERE data->>'FirstName' = 'haofly' ORDER BY id DESC LIMIT 50;	# 根据json的key查询
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

## PostgREST

- 自动为PostgrSQL提供Restful API
- 官网提供的安装方式不大一样，不能用`apt-get install`直接安装，所以可以这样做

```shell
mkdir ~/postgrest && cd ~/postgrest
export POSTGREST_VERSION=v10.1.2	# 去官网查看最新版本: https://github.com/PostgREST/postgrest/releases
wget https://github.com/PostgREST/postgrest/releases/download/${POSTGREST_VERSION}/postgrest-${POSTGREST_VERSION}-linux-static-x64.tar.xz && tar xvf postgrest-${POSTGREST_VERSION}-linux-static-x64.tar.xz

# 自己添加配置文件postgrest.conf
echo '
db-uri = "postgres://postgres:password@127.0.0.1:5432/postgres"
db-schemas = "public"
db-anon-role = "web_anon"	# 这个角色后面需要在postgresql中手动创建
server-port = 3000	# default is 3000
' | tee postgrest.conf

# 进入postgresql执行一下命令创建web_anon角色
create role web_anon nologin;
grant web_anon to postgres;	# 授权postgres用户拥有web_anon角色的权限
grant usage on schema public to web_anon; # 授予web_anon对public模式的使用权限
grant select on public.users to web_anon;	# 授予web_anon角色对public模式中的users表的select权限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO web_anon;	# 授予web_anon角色对public模式中的所有表都具有select权


# 运行postgrest
./postgrest postgrest.conf

# 访问接口
curl http://localhost:3000/表名?field=eq.value
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

- **must appear in the GROUP BY clause or be used in an aggregate function(列必须出现在group by子句中或聚合函数中)**: postgresql一个非常常见的问题，常常在使用聚合函数的时候出现，例如count。没有啥一劳永逸的解决方法，反正遇到这种问题，它让你加哪个列到group by里面就加进去吧，一定要看看sql的输出结果，看看是不是自己想要的。(这个才是sql的标准，mysql没有完全执行。。。)

- 

##### 扩展阅读

[PostgreSQL 9.6.0中文手册](http://www.postgres.cn/docs/9.6/index.html)