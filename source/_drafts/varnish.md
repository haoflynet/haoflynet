## 命令行工具

### vcli

```shell
# auth认证
vcli login

# agent
vcli agent list

# vcl文件编辑
vcli file list
vcli file edit 1	# 1就是文件的ID，编辑完成后保存会将它设置为draft，并不会自动部署

# VCLGroup
vcli vg deploy 1	# 1是VCLGroup的ID，这样会部署和这个group关联的所有的vcl files
```

### varnishadm

```shell
sudo varnishadm

storage.list	
```

## VCL语法

```shell
return (synth(422, "abc"));	# 返回状态码的同时能够指定错误信息
```

### Vsthrottle

-  API请求频率限制

```javascript
vsthrottle.is_denied(client.identity, 15, 10s, 30s) // 第一个参数表示客户端的唯一标识，第二、第三个参数表示频率为10秒内15个请求，最后一个参数表示如果超过了频率需要等待多久后重试
```

