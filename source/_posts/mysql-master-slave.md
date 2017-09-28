---
title: "Mysql之主从复制"
date: 2016-01-06 07:35:43
updated: 2017-09-29 00:51:00
categories: 编程之路
---
参考地址：<http://369369.blog.51cto.com/319630/790921>  

原来想要简单地实现MySQL的主从复制其实也是很简单的(这里当然不包括服务监控和容错处理啦)

1.要检查主从服务器的MySQL版本，最好版本一致，不然会出现各种问题，特别是，5.5和5.6是不会兼容的  

2.修改两个服务器的mysql配置`vim /etc/my.cnf`
```tex
[mysqld]
log-bin=mysql-bin    // 打开二进制日志
server-id=41         // 服务器的唯一ID，为0表示拒绝所有从服务器的连接
```
分别修改两个服务器配置然后分别重启

3.主服务器建立账户：这个账户与普通账户不一样，它只能用于主从复制中：  
```shell
mysql> GRANT REPLICATION SLAVE ON *.* to 'master'@'%' identified by 'mysql';
```
4.查看服务器状态
```shell
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+  
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |  
+------------------+----------+--------------+------------------+-------------------+  
| mysql-bin.000004 |   615261 |              |                  |                   |  
+------------------+----------+--------------+------------------+-------------------+  
1 row in set (0.00 sec)
```

需要注意的是，这两个值都得记下来哟

5.将主服务器数据库dump然后导入到从服务器，记下了Position就不用担心dump后新增数据的情况，会自动同步的

6.配置从服务器
```shell
mysql> change master to master_host='192.168.1.41', master_user='xiaohao', master_password='mysql', master_log_file='mysql-bin.000004', master_log_pos=615261;  # 这里就是刚才的Position
```
7.启动从服务器  
```shell
mysql> start slave;   # 同理，停止用stop slave
```
8.查看复制状态  
```shell
mysql> show slave status\G  
**_*_****_*_****_*_****_*_* 1. row ****_*_****_*_****_*_******  
Slave_IO_State: Waiting for master to send event  
Master_Host: 192.168.1.41  
Master_User: xiaohao  
Master_Port: 3306  
Connect_Retry: 60  
Master_Log_File: mysql-bin.000004  
Read_Master_Log_Pos: 652289  
Relay_Log_File: ubuntu-relay-bin.000002  
Relay_Log_Pos: 37345  
Relay_Master_Log_File: mysql-bin.000004  
Slave_IO_Running: Yes  
Slave_SQL_Running: Yes  
Replicate_Do_DB:
```
必须保证Slave_IO_Running和Slave_SQL_Running都为Yes的时候才正确的

# **TroubleShooting：**
  * **出现错误：Slave SQL for channel '': Slave failed to initialize relay log info structure from the repository, Error_code: 1872**是因为relay-log有问题，这时候修改从服务器mysql配置，在[mysqld]中加入`relay-log-recovery=1`，这样表示，服务器启动之后，删除所有已有的relay日志，重新接收主库的relay日志

