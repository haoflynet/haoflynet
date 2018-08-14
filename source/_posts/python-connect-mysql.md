---
title: "Python3 使用MySQL Connector操作数据库"
date: 2015-11-04 17:48:41
updated: 2018-08-08 18:45:22
categories: 编程之路
---
## 安装方法

支持`python3`的`mysql driver`有`mysqlclient`和`pymysql`，不推荐只支持2的`MySQLdb`

```shell
# ubuntu
sudo apt-get install python3-dev libmysqlclient-dev
pip install mysqlclient

# CentOS
sudo yum install pytho36-devel mysql-devel	# python36-devel指定python版本
sudo yum install mariadb-devel MariaDB-shared	# 如果不安装会出现cannot find -lmariadb错误
pip install mysqlclient
```
<!--more-->

## 数据库的连接

这里有所有的[连接参数列表](https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html)

```python
# 使用Oracle官方提供的数据库引擎的连接方法
import mysql.connector
cnx = mysql.connector.connect(  
                          user='',
                          password='',
                          host='',
                          database='',  
                          pool_size=3 # 连接池大小)
cnx.close()

# 使用基于MySQLdb的连接方法，比如mysqlclient
import MySQLdb
db = MySQLdb.connect(
	host='', 
    user='', 
    passwd='', 
    db='', 
    charset='utf8', 
    autocommit=True)
cursor = db.cursor()
```


## Difference：两个库的区别

```shell
# MySQL Connector/Python
Oracle官方的实现，底层完全用C来实现
默认未开启cursorbuffer，如果需要则显式开启：cnx.cursor(buffered=True)或者mysql.connector.connect(buffered=True)，开启了buffer，可同时使用多个游标

# MySQLdb
不完全用C
默认开启了cursor的，会缓存结果，但是针对特别大的查询，可能会导致程序崩溃
```

## CURD操作

### 插入

    # 插入一条数据
    insert_stmt = (
      "INSERT INTO employees (emp_no, first_name, last_name, hire_date) "
      "VALUES (%s, %s, %s, %s)"
    )
    data = (2, 'Jane', 'Doe', datetime.date(2012, 3, 23))
    cursor.execute(insert_stmt, data)
    
    # 同时插入多条数据
    data = [
        ('a', 'b', 'c', 'd'),
        ('e', 'f', 'g', 'h')
    ]
    stmt = 'INSERT INTO table_name (field_name1, field_name2)' 				'VALUES(%s, %s)'
    cursor.executemany(stmt, data)
### 读取

```python
# 看了源码发现，fetchone/fatchmany/fetchall实现居然是一样的：https://github.com/PyMySQL/mysqlclient-python/blob/7d289b21728ab1a94bb1f0210a26367c6714d881/MySQLdb/cursors.py，结果都是一次取出保存，这三个方法就是在结果列表里面切片而已

# fetchone
cursor.execute('select * FROM user")
row = cursor.fetchone()
while row is not None:
    print(row)
    row = cursor.fetchone()  

# cursor可以直接拿来做迭代器
cursor.execute(sql)
for row in cursor:
    print(row)

# fetchmany()：获取固定数量的结果，当然，每次fetch过后指针会偏移到后面那个地方
rows = cursor.fetchmany(size=1)
```
# TroubleShooting

* 获取insert后的ID值  

  ```shell
  db.insert_id()  # 表示上一次插入数据的ID
  ```

* 获取原始SQL语句

  ```python
  print(cursor._last_executed)
  ```

* 多线程的情况下，出现错误"OperationalError:(2013, 'Lost connection to MySQL server during query')"，出现这种情况是因为在多线程的情况下，如果只有一个mysql连接，那么mysql该连接会在执行完一个线程后销毁，需要加锁，在线程里面修改全局变量，会导致该变量的引用出错  

  ```python
  LOCK.acquire()  
  mysql.cursor.execute(sql)  
  result = mysql.cursor.fetchall()  
  LOCK.release()
  print(len(result))
  ```

* **Can't connect to local mySQL server ough socket '/tmp/mysql.sock**

  可能原因是由于MySQL是编译安装的，没有放在默认的目录，导致python找不到默认的sock文件，可以用一个软连接将实际文件链接到这个默认的目录下面

* **EnvironmentError: mysql_config not found**，原因在mac环境下没有安装mysql包，需要`brew isntall mysql`

   


##### 参考文章

<https://dev.mysql.com/doc/connector-python/en/>  

<http://mysql-python.sourceforge.net/MySQLdb.html>  