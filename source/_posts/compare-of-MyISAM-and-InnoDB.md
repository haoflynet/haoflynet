---
title: "MySQL之MyISAM与InnoDB两大存储引擎的对比及选择"
date: 2014-11-03 16:17:30
categories: 编程之路
---
参考：<http://www.oschina.net/question/17_4248>

MySQL在5.5X开始，默认的存储引擎改为了InnoDB
Plugin引擎，而我正是在5.5开始使用MySQL的，对两个引擎的区别还不甚了解，所以特别查阅了大量的资料，整理如下：

# 有何区别：

最简单的，一条语句即可看到：  
![](http://7xnc86.com1.z0.glb.clouddn.com/compare-of-MyISAM-and-InnoDB.png)  
更具体的看下面：

## Innodb

  * 索引聚集表，存储结构采用BTREE
  * 数据存储是有顺序的，默认以主键排序，主键就是数据本身，所以对于insert比较多的情况，最好建一个自增主键，以方便保持其顺序性

## MyISAM

# 如何选择

我认为两个引擎没有孰优孰劣之分，具体怎么选择完全看业务需要。

InnoDB适合： 1.数据量巨大时，提高CPU效率，这一点上其他引擎都比不上InnoDB 2.使用事务 3.可靠性好、性能高 4.更新查询都相当频繁
5.表锁定几率较大 6.大量的主键查询 7.并发量大的update语句 8.高压力、高并发

MyISAM适合： 1.磁盘空间较小 2.大量count计算(MyISAM用一个值来记录，而InnoDB每次都扫描全表) 3.插入不频繁，查询频繁
4.不使用实务 5.大量的insert语句
