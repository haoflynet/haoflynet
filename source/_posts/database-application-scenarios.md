---
title: "各种数据库的应用场景以及选型"
date: 2015-12-07 07:48:21
categories: 编程之路
---
## Redis

- 统计：比如行为指标、点击量统计、访问量统计、排行榜、最新或最高的N个数据等 

- 缓存：会话缓存，页面缓存，全局变量缓存  队列：队列服务 

- 过期：需要设置过期时间的数据

## MongoDB

- 文本：日志、文章等

## MariaDB

- 数据引擎丰富，包含以下的存储引擎:
  - Aria(增强版的MyISAM)
  - XtraDB(增强版的InnoDB)
  - FederatedX
  - OQGRAPH
  - SphinxSE
  - IBMDB2I
  - TokuDB
  - Cassandra
  - CONNECT
  - SEQUENCE
  - Spider
  - PBXT
- Group commit for the binary log组提交技术，能够将多个并发提交的事物加入一个队列，对这个队列里的事务，利用一次I/O合并提交，解决写日志频繁刷磁盘的问题
- 基于表的多线程并行复制技术
- 线程池thread pool技术
- 时间精确到微妙级别
- 增加多源复制和基于表的并行复制
- 发展速度远远超过MySQL

## MySQL

## Percona

- 相比于MySQL，它仅仅是针对InnoDB引擎做了性能上的改善，称为XtraDB




  ​

  ​

  ​