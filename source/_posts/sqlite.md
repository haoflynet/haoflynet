---
title: "sqlite教程"
date: 2016-04-05 11:02:30
categories: database
---
# sqlite

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
