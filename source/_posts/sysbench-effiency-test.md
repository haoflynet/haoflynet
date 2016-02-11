---
title: "Sysbench性能测试工具的使用"
date: 2014-11-03 17:14:04
categories: 编程之路
---
参考：《MySQL管理之道》

# 简介

Sysbench是一个模块化、跨平台、多线程基准测试工具，主要用于评估测试各种不同系统参数下的数据库负载情况。

# 安装



    sudo apt-get install sysbench

#  参数列表

General options：



    --num-threads=N          线程数，默认为1
    --max-requests=N         并发请求限制，默认为10000
    --max-time=N             最大执行时间，默认为0
    --forced-shutdown=STRING 最大执行时间后多久强制关闭
    --thread-stack-size=SIZE 每个线程的栈大小，默认32K
    --init-rng=[on|off]      初始化随机数生成器，默认off
    --test=STRING            test to run
    --debug=[on|off]         打印更多的调试信息，默认off
    --validate=[on|off]      尽可能执行验证检查，默认off
    --help=[on|off]          查看帮助
    --version=[on|off]       查看版本

Compiled-in tests：



    fileio    磁盘I/O性能测试
    cpu       CPU性能测试
    memory    内存分配及传输速度测试
    threads   POSIX线程性能测试
    mutex     调度程序性能测试
    oltp      数据库性能测试(OLTP基准测试)

#  使用举例

测试Mysql的InnoDB存储引擎，其中16个并发连接，最大请求1万个，表记录有9百万条：



    sysbench --test=oltp -MySQL-table-engine=innodb \\
    --oltp-table-size=9000000 \\
    --max-requests=10000 \\
    --num-threads=16 \\
    --MySQL-host = 127.0.0.1 \\
    --MySQL-port = 3306 \\
    --MySQL-user = root \\
    --MySQL-password = 123456 \\
    --MySQL-db = test \\
    --MySQL-socket=/tmp/MySQL.sock prepare
