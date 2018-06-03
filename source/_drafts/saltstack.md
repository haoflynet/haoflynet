---
title: "SaltStack"
date: 2018-11-01 21:32:00
categories: 编程之路
---



http://blog.51cto.com/pankuo/2047503

https://blog.csdn.net/fanren224/article/details/73431542



http://blog.51cto.com/szcto/1767976  模块大全(内置了的)

### [Salt中ZeroMQ那点事，非常完整的流程简介](http://pengyao.org/salt-zeromq-01.html)

创建定时任务相关   https://github.com/saltstack/salt/blob/e974cf385d3ac0b86959a0eca88d96c9e3527ec3/salt/states/incron.py









ZeroMQ 是一款消息队列软件，SaltStack 通过消息队列来管理成千上万台主机客户端，传输指令执行相关的操作。而且采用 RSA key 方式进行身份确认，传输采用 AES 方式进行加密，这使得它的安全性得到了保证。(主控端（Master）与被控端（Minion）基于证书认证，确保安全可靠的通信；)

 管理端称为 Master，客户端称为 Minion。SaltStack 具备配置管理、远程执行、监控等功能，一般可以理解为是简化版的 Puppet 和加强版的 Func。SaltStack 本身是基于 Python 语言开发实现，结合了轻量级的消息队列软件 ZeroMQ 与 Python 第三方模块（Pyzmq、PyCrypto、Pyjinjia2、python-msgpack 和 PyYAML 等）构建。

SaltStack 客户端（Minion）在启动时，会自动生成一套密钥，包含私钥和公钥。之后将公钥发送给服务器端，服务器端验证并接受公钥，以此来建立可靠且加密的通信连接。同时通过消息队列 ZeroMQ 在客户端与服务端之间建立消息发布连接。

1. SaltStack 的 Master 与 Minion 之间通过 ZeroMq 进行消息传递，使用了 ZeroMq 的发布订阅模式，连接方式包括 TCP 和 IPC。

 其实，只是用了zeromq的发布订阅而已的啦。

1. Minion 从消息总线上接收到要处理的命令，交给 minion._handle_aes 处理。

 

1. Salt.client.LocalClient.cmd_cli 通过轮询获取 Job 执行结果，将结果输出到终端。

 

 





Saltstack目前最主要的三大主要功能

·  远程执行

·  配置管理

·  云管理

通过Saltstack批量执行系统命令，包括系统重启，查看系统负载，添加/删除用户等等



salt '*' cmd.run 'w'

远程命令执行（cmd模块），格式：salt  'client配置的id' 模块.方法  '命令参数'           （其中'*'表示所有的client）



还要支持灰度，如果一条命令要在所有机器上面执行，那么可以选择先在某几台机器上面执行

http://blog.51cto.com/szgb17/1914622

http://blog.51cto.com/szgb17/1914622



Saltstack**的三种运行方式**

·  Local

·  Master/Minion

·  Salt SSH

Saltstack最传统的运行方式还是C/S模式，需要在被管理节点上安装Minion客户端；其实Saltstack也支持SSH方式，无需安装Agent，通过SSH实现管理 













salt '*' cron.set_job root '*' '*' '*' '*' 1 /usr/local/weekly    我还能说啥，这个就6了