---
title: "web开发习惯"
date: 2016-07-27 22:52:39
categories: code
---
# web开发约定

## web部署结构
仅用于轻量级web框架，来自于[TornadoWheel](https://github.com/qiwsir/TornadoWheel)

	.工程目录
	├── server.py			# 启动服务
	├── application.py	# 服务基本设置
	├── url.py			# 路由结构
	├── handler/			# 各种请求处理类文件
	├── static/			# 静态文件
	├── optsql/			# 与数据库读写相关的文件
	└── template			# 模板文件
