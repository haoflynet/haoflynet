---
title: "Python3 使用MySQL Connector操作数据库"
date: 2015-11-04 17:48:41
categories: 编程之路
---
参考文档：  
<https://dev.mysql.com/doc/connector-python/en/>  

<http://mysql-python.sourceforge.net/MySQLdb.html>  

## 安装方法
```
# ubuntu
sudo apt-get install python3-dev libmysqlclient-dev
pip install mysqlclient

# CentOS
sudo yum install pytho3n-devel mysql-devel
pip install mysqlclient
```
## 数据库的连接
```
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
db = MySQLdb.connect(host='', user='', passwd='', db='', charset='utf8')
cursor = db.cursor()
```


## Difference：两个库的区别



    # MySQL Connector/Python
    Oracle官方的实现，底层完全用C来实现
    默认未开启cursorbuffer，如果需要则显式开启：cnx.cursor(buffered=True)或者mysql.connector.connect(buffered=True)，开启了buffer，可同时使用多个游标

    # MySQLdb
    不完全用C
    默认开启了cursor的，会缓存结果，但是针对特别大的查询，可能会导致程序崩溃





## 插入



    # 同时插入多条数据


    data = [
        ('a', 'b', 'c', 'd'),
        ('e', 'f', 'g', 'h')
    ]
    stmt = 'INSERT INTO table_name (field_name1, field_name2) VALUES(\%s, \%s)'
    cursor.executemany(stmt, data)

## 读取



    # 看了源码发现，fetchone/fatchmany/fetchall实现居然是一样的：https://github.com/PyMySQL/mysqlclient-python/blob/7d289b21728ab1a94bb1f0210a26367c6714d881/MySQLdb/cursors.py，结果都是一次取出保存，这三个方法就是在结果列表里面切片而已

    # fetchone()举例
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

# TroubleShooting

  * 获取insert后的ID值  


        db.insert_id()  # 表示上一次插入数据的ID

  * 多线程的情况下，出现错误"OperationalError:(2013, 'Lost connection to MySQL server during query')"，出现这种情况是因为在多线程的情况下，如果只有一个mysql连接，那么mysql该连接会在执行完一个线程后销毁，需要加锁，在线程里面修改全局变量，会导致该变量的引用出错  


        LOCK.acquire()  
    mysql.cursor.execute(sql)  
    result = mysql.cursor.fetchall()  
    LOCK.release()  
    print(len(result))

  *   
