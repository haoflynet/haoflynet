---
title: "MySQL之调优方法"
date: 2015-12-10 08:25:34
categories: 编程之路
---
  * 数据库分析调优步骤  


        1.将sql语句记录下来
    2.看查询更新的比例(如果太多，可以抽样查看)
    3.看最多查询的数据表有哪些，最多更新的数据表有哪些
    4.看最多查询的数据表最多查询的SQL是什么样子的，最多更新的数据表最多执行的SQL语句是怎样的，算出各自每秒的请求频率
    5.关键分析，最多查询的SQL，基于同一主键查询的比例多不多(看能不能缓存化)
    6.应对大翻页的问题，其实是不需要精确的返回结果数的，像淘宝这些都不会超过100页的



  * 数据库配置：  


        innodb_read_io_threads/innodb_write_io_threads：这两个参数指Innodb数据库读写的IO进程数，默认为4

  * 慢查询日志：  


        # 开启慢查询
    > show variables like 'slow_query_log'   # 查看是否开起慢查询
    > set global slow_query_log_file = ''
    > set global log_queries_not_using_indexes = on
    > set global long_query_time = 1

  * 分库分表  
表的垂直拆分：把原来一个有很多列的表拆分成多个表，解决了表宽的问题，通常，把不常用的字段单独存放到一个表中，大字段单独存放，一起使用的字段一起存放

  * 语句分析：使用explan查询SQL的执行计划
  * 其它工具  


        Mysqldumpslow：慢查询日志的分析工具
