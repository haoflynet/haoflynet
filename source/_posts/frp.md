---
title: "使用frp实现内网穿透"
date: 2018-09-21 09:32:00
categories: 编程之路
---

我以前写过一篇[内网穿透方案](https://haofly.net/internal-network-penetration/)，最近接触了`frp`，觉得这才是最简单最实用功能最强大的内网穿透工具。它有如下一些显著的优点:

- 客户端和服务端的配置都超级简单，并且中英文文档都非常丰富
- 能通过自定义的域名访问部署于内网的web服务
- 能实现DNS查询请求的转发
- 能通过设置密码的方式实现安全地内网服务访问(使用者需单运行frp client)
- 能够实现点对点内网穿透(使用者需运行frp client，并且还处于开发阶段)
- 提供Dashboard随时监控流量信息

### 配置frp

<!--more-->
官网的[README](https://github.com/fatedier/frp/blob/master/README_zh.md)已经非常详细了，架构图我这里也不说说明了。唯一需要说明的是，这里必须要要有一个在公网的服务器，毕竟大局网，没有公网服务器是不可能的。

这里只列举我自己的一份实现了我想要的功能的配置:

- 假设家里的客户端命名为NAS，公网服务器命名为SERVER，而需要访问的笔记本为MAC

#### 公网服务器端SERVER配置

- 公网服务器的防火墙不仅要允许`bind_port`如果客户端有其他的端口，也都得允许

首先在github的frp仓库的release页面下载最新指定系统的frp，然后解压缩。

```shell
# vim frps.ini
[common]
bind_port = 7000	# 默认的端口，这也是
```
然后这样启动：`./frps -c ./frps.ini`


#### 被访问端NAS(CLIENT)配置

- 如果公网服务器SERVER端没有启动服务或者没有开启端口，这边是启动不成功的。

首先在github的frp仓库的release页面下载最新指定系统的frp，然后解压缩。

```shell
# vim frpc.ini
[common]
server_addr = x.x.x.x	# 公网服务器的IP
server_port = 7000		# 公网服务器的bind_port
admin_addr = 127.0.0.1	# 本地管理地址，主要用于热加载(重启)
admin_port = 7400

[ssh]					# 首先当然是需要ssh服务啦
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6000		# 公网服务器必须开放该端口，访问端(客户端)MAC在访问时候就提供该端口

[mysql]					# 可以自己添加需要开放的其他服务
type = tcp
local_ip = 127.0.0.1
local_port = 3306
remote_port = 3306
```

然后这样启动: `./frpc -c ./frpc.ini`，然后之后如果修改了配置文件可以使用命令`./frpc reload -c ./frpc.ini`进行重启，`x.x.x.x`而不用中断服务。

接着就可以在访问端`MAC`使用命令`ssh -oPort=6000 user@x.x.x.x`登录内网中的服务器了，其中`user`是内网服务器的用户，`x.x.x.x`是公网服务器的IP。

同时也可以通过其他的端口访问其他的服务了。

#### 访问端MAC(CLIENT)配置

- 只有需要更安全访问时才需要在访问端启动一个`CLIENT`，简单地说就是加一个密码。

同样需要在github的frp仓库的release页面下载最新指定系统的frp，然后解压缩。

```shell
# vim frpc.ini
[common]
server_addr = x.x.x.x
server_port = 7000

[mysql]
type = stcp
role = visitor
server_name = secret_mysql	# 必须和NAS端的名字一样
sk = abcdefg
bind_addr = 127.0.0.1
bind_port = 6000
```

然后启动本地CLIENT: `./frpc -c ./frpc.ini`。这时候，公网服务器端SERVER只开放了7000和6000端口。我们可以这样访问NAS的mysql服务: `mysql -uroot -pmysql -P3307 -h127.0.0.1`来访问内网的MySQL服务了。