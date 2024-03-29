- ` /etc/postgresql/POSTGRES_VERSION/main`这个目录是在安装`postgresql`的时候就自己初始化了的，如果patroni的postgresql.data_dir指向的是它，那么会被要求重新初始化
- 服务发现工具一般推荐用etcd，只要在yml中配置了`etcd.hosts`，那么只要启动当前节点就会自动加入scope namespace的集群中

## 配置

### 配置文件

```yaml
scope: &scope postgres-cluster # 这里是集群的名称
namespace: /db/	# 在etcd的命名空间
name: &name PG1	# 这是当前实例在集群中的名字标识符

restapi:
  listen: 0.0.0.0:8008	# patroni api的监听地址，如果需要使用HAProxy做读写分离需要将该接口暴露给HAProxy
  connect_address: PUBLIC:8008	# patroni api的连接地址
  authentication:	# restapi的Basic Auth认证，注意访问GET :8008/的时候是不需要认证的
    username: admin
    password: 密码

etcd:
  hosts: "127.0.0.1:2379,127.0.0.2:2379"	# 指定etcd的实例列表

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true

  initdb:
    - encoding: UTF8
    - data-checksums

  pg_hba:
    - host replication replicator 0.0.0.0/0 md5
    - host replication postgres 0.0.0.0/0 md5
    - host all all 0.0.0.0/0 md5

  users:
    admin:
      password: PATRONI_ADMIN_PASSWORD
      options:
        - createrole
        - createdb

postgresql:
  listen: 0.0.0.0:5432
  connect_address: PUBLIC_IP:5432
  data_dir: /var/lib/postgresql/data/pgdata
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: POSTGRES_USERNAME
      password: POSTGRES_PASSWORD
    superuser:
      username: POSTGRES_USERNAME
      password: POSTGRES_PASSWORD
  parameters:
    unix_socket_directories: '.'

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false

log:
  dir: /var/log/
  file_size: 31457280
  level: DEBUG
  loggers:
    patroni: DEBUG
    psycopg2: WARNING
    kazoo.client: WARNING
    urllib3: WARNING
  handlers:
    console:
      class: logging.StreamHandler
      formatter: custom
    file:
      class: logging.handlers.RotatingFileHandler
      formatter: custom
      filename: /var/log/patroni.log
      maxBytes: 30000000
      backupCount: 5
```

## 常用命令

```shell
patronictl -c /etc/patroni/patroni.yml list	# 列出当前集群所有的节点和状态
patronictl -c /etc/patroni/patroni.yml topology	# 用ASCII打印当前的拓扑结构
patronictl -c /etc/patroni/patroni.yml reload cluster-name	# 当patroni.yml更新后可以用这个命令重新加载配置
patronictl -c /etc/patroni/patroni.yml reinit cluster-name cluster-node	# 重新初始化集群中的某个节点
patronictl -c /etc/patroni/patroni.yml failover cluster-name	# 手动执行故障转移，可以选择一个slave节点作为新的master
```

## restfulapi

- 在yml中添加如下配置即可，注意这里的auth认证只针对于写请求，GET请求仍然可以正常访问的

```yaml
restapi:
  listen: 0.0.0.0:8008
  connect_address: PUBLIC_IP:8008
  authentication:
    username: admin
    password: 密码
```

## Patroni+HAProxy实现负载均衡

- 需要注意的是，读写操作都需要将所有的server列出来，并且check port应该设置为patroni的8008端口，patroni默认给master返回200，给slave返回503，这样就可以让HAProxy知道哪些是读服务器，哪些是写服务器了

```shell
listen postgres_write	# 写操作
    bind *:5432
    option httpchk
    option tcplog
    balance leastconn
    mode tcp
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server pg1 192.168.1.1:5432 maxconn 1000 check port 8008
    server pg2 192.168.1.2:5432 maxconn 1000 check port 8008
    server pg3 192.168.1.3:5432 maxconn 1000 check port 8008

listen postgres_read	# 读操作
    bind *:65432
    mode tcp
    option tcplog
    balance leastconn
    option httpchk
    http-check expect status 503
    default-server inter 3s fall 3 rise 3 on-marked-down shutdown-sessions
    server pg1 192.168.1.1:5432 maxconn 1000 check port 8008
    server pg2 192.168.1.2:5432 maxconn 1000 check port 8008
    server pg3 192.168.1.3:5432 maxconn 1000 check port 8008

listen patroni	# restful api接口
    bind *:8008
    mode http
    option httplog
    option httpchk
    http-check expect status 200
    server pg1 192.168.1.1:8008 maxconn 100 check port 8008
    server pg2 192.168.1.2:8008 maxconn 100 check port 8008
    server pg3 192.168.1.3:8008 maxconn 100 check port 8008
```

## TroubleShooting

- **I am (xxx), the leader with the lock明明启动成功了，但是state却显示start failed**: 原因是在启动的时候patroni没有成功启动postgresql，这种情况可以先启动postgresql再启动patroni: `sudo systemctl stop patroni && sudo systemctl start postgresql && sudo systemctl start patroni`

- **卡在了establishing a new patroni connection to the postgres cluster**：肯定是连接问题，但具体是啥问题还得自己去看，我这边的问题是因为没有把`replication`加入`pg_hba.conf`，注意这里即使加入了all也得单独加:

  ```shell
  bootstrap:
    pg_hba:
      - host replication postgres 0.0.0.0/0 md5	# 即使下面有all，也得单独加replication，注意及时用psql能连接上也得加上这个，这是给slave用的
      - host all all 0.0.0.0/0 md5
  ```

- **system ID mismatch, node postgres-cluster-madrid belongs to a different cluster: 7218046306071193898 != 7218061650753527056**： 应该是当前这台机器之前已经加入某个node了，然后又重新布置了一下环境，此时需要清理一下`etcd`的缓存:

  ```shell
  curl -L http://127.0.0.1:2379/v2/keys/db?recursive=true -X DELETE	# 我的patroni.yml的namespace是/db/，所以这样子可以删除所有key，这样做是不会影响集群的，因为每个node每隔几秒都会上报一下自己的状态重新生成键值对
  ```

  