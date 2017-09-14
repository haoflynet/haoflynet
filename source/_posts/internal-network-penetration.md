---
title: "内网穿透方案"
date: 2015-12-04 07:39:55
updated: 2017-09-10 18:28:00
categories: 编程之路
---
背景: 天朝大局域网，网上都说可以打电话叫客服切换到公网IP，但是电信、移动宽带，无论打客服还是安装师傅，居然从上到下都不知道公网IP是什么，他们以为我要公网IP是要独立宽带，公网IP和共享宽带明明是两个概念好不好，你可以封80端口，但是其它什么端口至少给我留一个总行吧，客服没用，就只能自己动手了。  

## SSH Tunnel

使用SSH进行的Tunnel进行端口转发，对于不需要访问desktop来说是最简单的一种内网穿透方案，当然，唯一的要求是你得有一个有公网IP的服务器做代理。  

    1. 首先，在内网主机上执行ssh命令:


```shell
ssh -NfR 外网ssh端口号:localhost:本地ssh端口号 远端IP
```

    2. 在代理服务器上执行通过ssh连接内网的服务器:


```shell
ssh -p 刚才定义的远程端口号  localhost
```

    3. SSH太容易掉线了，为了不掉线，有多种方法：  


```shell
# 首先，修改SSH配置，代理服务器段：vim /etc/ssh/sshd_config，修改或新增如下两项
ClinetAliveInterval 60
ClientAliveCountMax 10
#然后重启SSH服务：service sshd restart
# 内网服务器端：vim /etc/ssh/ssh_config，修改或新增
Host *
ServerAliveInterval 30

# 但其实，这两种方法都还是容易掉线，接下来，终极解决方案  


```

事实上，上面的方法非常容易断开ssh连接，这里有一个一劳永逸的方案: 写一个python脚本，然后nohup keepalived.py &，在脚本里新建一个ssh连接，不断发送空格即可


```python
​```
#!/usr/bin/python
#coding: utf-8
import paramiko, time

class myssh():  
	def **init**(self, ip, port, username, password):  
	self.ssh = paramiko.SSHClient()  
	self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
	self.ssh.connect(ip, port, username, password, timeout=5)  

	def exec(self, cmd):  
		return self.ssh.exec_command(cmd)  

if '__name__ == '__main__':  
	ssh = myssh('localhost', 8022, 'haofly', '896499825')  
	while True:  
		ssh.exec(' ')  
		time.sleep(30)  
	ssh.close()
```

**推荐阅读**
[几个内网穿透，内网网站穿透，内网端口映射到公网的服务推荐](https://v2ex.com/t/268495#reply11)
