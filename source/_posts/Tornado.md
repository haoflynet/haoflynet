---
title: "Tornado 教程"
date: 2015-08-05 12:02:30
updated: 2017-10-29 20:24:00
categories: python
---
# Tornado
[中文文档](http://www.tornadoweb.cn/documentation) 
是不是很神奇，我居然会学习除Django以外的另一种Python Web框架。但事实确实如此，我学了，并且用了一下，感觉和Django确实存在很大的不同的。 
学这个的主要原因是要参加饿了么的黑客马拉松，主题是使用Python或Java或Node设计Resutful API，来应对高并发的请求，保证数据的一致性。虽然最后的分数并不理想，但是在这次比赛中学到了很多的东西，Tornado就是其中之一。 
以前只听说过Tornado比Django拥有更高的并发和异步特性，只听过Django坚持自己造轮子，其他语言的Web框架也只用过PHP的Laravel，当安装完Tornado后完全不知道该怎么玩儿，怎么着玩意儿自己不会生成一个项目，项目的框架还要自己写。后来才体会到，这样的好处，简洁、直观、轻便，它只提供最基础的东西，其他一切问题都由你自己来解决，同时，短短几千行的源代码，在遇到问题的时候，我们完全可以直接看源代码来查找问题出在哪儿，这就是简洁带来的好处。另外异步的作用也只有在实际需要的时候才能体会出来。由于我从来没写过异步的代码，所以，只是按照之前写代码那样，而没有根据异步的特性来实现，异步的代码是要在会阻塞的地方使用回调函数来实现，所以，我的程序并不能得高分。不过后来才知道Tornado通过gen将同步代码转换为异步的实现。  

要想自己定义代码结构，可以参考[qiwsir/TornadoWheel](https://github.com/qiwsir/TornadoWheel)

## 基本框架

[项目初始化结构](https://github.com/haoflynet/project-structure/tree/master/Tornado)

## Response & Request


	self.request.body					# 请求内容，字节类型
	self.request.arguments				# 获取全部请求参数
	self.request.query_arguments		# 获取全部GET请求参数
	self.request.body_arguments		# 获取全部POST请求参数
	name = self.get_argument('name')	# 获取POST参数
	self.request.remote_ip				# 获取客户端真实IP

## 特殊的帮助函数
#### 处理json请求
`data = tornado.escape.json_decode(self.request.body`， tornado提供的转义HTML、JSONURL和其他数据的工具，需要注意的是如果是ajax请求，这样子传递可以很好地处理数组的问题:

	$.ajax({
	    url: 'http://127.0.0.1:8888/submit',
	    type: 'POST',
	    dataType: 'json',
	    contentType: 'application/json',
	    data: JSON.stringify(data),
	    error: function(){
	        console.log('error');
	    },
	    success: function(re){
	        console.log('success');
	    },
	});
#### 返回json数据
直接`self.write(字典)`就行了
​	

## TroubleShooting


*   


静态文件设置了后，必须访问static前缀