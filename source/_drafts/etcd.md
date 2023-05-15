## 安装配置

```shell
/usr/local/bin/etcd 
	--listen-client-urls 'http://0.0.0.0:2379' 	# 侦听地址
	--advertise-client-urls 'http://公网IP:2379' -enable-v2
```

## Restful API

```shell
curl http://127.0.0.1:2379/v2/members	# 列出etcd集群的成员
curl http://127.0.0.1:2379/v2/keys	# 列出所有的key
```

