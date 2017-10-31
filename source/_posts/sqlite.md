---
title: "SQLite教程"
date: 2016-04-05 11:02:30
updated: 2017-10-31 22:29:00
categories: database
---
SQLite是一个遵守ACID的关系数据库管理系统，本身是一个嵌入式的程序，并不是客户端/服务端模式的架构，可以直接继承到应用程序中，Pyhton就内置了SQLite的。它的数据是直接存储在一个文件里面的。

## 安装

OSX: `brew install sqlite`
重点是无服务器
需要注意的是sqlite3的主键默认是这样的

    conn.execute('''CREATE TABLE IF NOT EXISTS IP
        (
            _id INTEGER PRIMARY KEY,
            ip INT NOT NULL UNIQUE,
            port INT NOT NULL,
            type VARCHAR(5) NOT NULL,
            level VARCHAR(10),
            speed INT,
            address VARCHAR(50),
            last_time INT NOT NULL,
            status INT DEFAULT 0
        );''')


        # -*- coding: utf-8 -*-
        #!/usr/local/bin/python3
    
        import sqlite3
    
        conn = sqlite3.connect('Proxy.db')
    
        # 建表
        conn.execute('''CREATE TABLE IF NOT EXISTS IP
            (
                _id INTEGER PRIMARY KEY,
                ip INT NOT NULL UNIQUE,
                port INT NOT NULL,
                type VARCHAR(5) NOT NULL,
                level VARCHAR(10),
                speed INT,
                address VARCHAR(50),
                last_time INT NOT NULL,
                status INT DEFAULT 0
            );''')
    
        # 插入
        conn.execute('''
            INSERT INTO IP (ip, port, type, level, speed, address, last_time, status)
            VALUES
            (123457891, 80, 'HTTP', '透明', 3, '重庆市', 1234567890, 0);
        ''')
        conn.commit()
    
        # 查询
        cursor = conn.execute('SELECT * FROM IP');
        for row in cursor:
            print(row)
        conn.close()
