---
title: "Python 连接FTP/FTPS"
date: 2020-11-07 22:33:39
categories: python
---

python自带库ftplib对ftp的连接提供了支持。下面是其基本的语法

```python
ftp = ftplib.FTP(timeout=300)	# 连接基本的FTP
ftp = ftplib.FTP_TLS(timeout=300)	# 连接FTPS

ftp.connect(host, port)	# 连接目标服务器
ftp.login(username, password)	# 登陆目标服务器
ftp.mkd('/abc')	# 创建远程目录
ftp.dir()	# 显示当前目录下的文件及目录，会直接打印到标准输出
ftp.nlst()	# 返回当前目录下的文件及目录
ftp.cwd('')	# 切换目录
ftp.pwd()	# 返回当前所在目录
ftp.rmd(dirname)	# 删除远程目录
ftp.delete(filename)	# 删除远程文件
ftp.rename(fromname, toname)	# 给远程文件重命名
ftp.close()	# 关闭连接

## 上传文件
local_file_handler = open('test.txt', 'rb')
ftp.storbinary("STOR " + os.path.join(remote_path, filename), local_file_handler)
    
## 下载文件
local_file_handler = open('test.txt', 'rb')
ftp.retrbinary("RETR " + os.path.join(remote_path, filename), file_handler.write)
local_file_handler.seek(0)
```

<!--more-->

### Troubleshooting

- **ftplib出现ssl.SSLError: [SSL] internal error (_ssl.c:1123)**: 我的情况是服务器的ssl版本太高了(ubuntu20.04)，并且目标FTPS服务器的ssl版本太低了，看论坛好像确实是有这么一个[bug](https://bugs.python.org/issue41561)，在python方面没有找到解决方案，最终找到几个命令行工具来完成需求：
  上传使用的是`ftp-uploader`，直接用`apt`命令安装的；下载则是用的`lftp`，但是参数比较多: `
  
  ```shell
  /usr/bin/lftp -c 'set ftp:ssl-allow true ; set ssl:priority NORMAL:+VERS-TLS1.1:+VERS-TLS1.2; 
  set ssl:verify-certificate no; open -u 用户名,密码 -e "cd 目录; mget 文件名; quit" 目标服务器
  ```

##### 扩展

- [一个测试用的FTP服务器](https://dlptest.com/ftp-test/)