---
title: "Atom手册"
date: 2015-12-22 08:40:39
categories: tools
---
# Atom

## TroubleShooting
- 使用Python3，直接在文件头添加`#!/usr/local/bin/python3`
- atom-script输出中文出现unicodeerror错误，可以这样输出：

  	import io, sys
  	sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
  	sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
  	print ('中文')
- **设置shadowsocks代理**  
  vim ~/.atom/.apmrc  
```
strict-ssl = false
http-proxy = http://127.0.0.1:8090/proxy.pac
```
apm config list查看是否设置成功
```
http-proxy = "http://127.0.0.1:8090/proxy.pac"
```
- ** **
