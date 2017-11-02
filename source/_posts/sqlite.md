---
title: "SQLite教程"
date: 2016-04-05 11:02:30
updated: 2017-11-02 22:29:00
categories: database
---
SQLite是一个遵守ACID的关系数据库管理系统，本身是一个嵌入式的程序，并不是客户端/服务端模式的架构，可以直接继承到应用程序中，Pyhton就内置了SQLite的。它的数据是直接存储在一个文件里面的。

## 安装

OSX: `brew install sqlite`。

客户端: [sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser)

需要注意的是sqlite3的主键默认是这样的。

## TroubleShooting

- **报错`sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in thread xxxx `**，原因是SQLite是不能多个线程同时访问的，要么直接不适用多线程，更好的做法是在连接是添加`check_same_thread`参数。

  ```shell
  connect = sqlite3.connect('test.db', check_same_thread=False) # 允许在其他线程中使用这个连接
  ```

- ​