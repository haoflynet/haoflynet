---
title: "使用Supervisor管理进程"
date: 2015-08-11 10:07:33
updated: 2018-08-13 16:03:00
categories: 编程之路
---
supervisor是使用Python编写的进程管理软件，在实际开发中，一般用它来同时开始一批相关的进程，无论是Django的runserver还是直接管理Nginx、Apache等，都比较方便，这里是其使用方法：

## 安装supervisor

```shell
# ubuntu
apt-get install supervisor
service supervisor restart

# centos
yum install supervisor
/etc/init.d/supervisord restart
```
<!--more-->

## 使用

- **初次安装supervisor由于系统不同安装版本不同，可能没有自动生成配置文件，一定要手动去生成一次，因为你并不知道配置文件里面哪些是必须的...**

```shell
sudo easy_install supervisor
echo_supervisord_conf > supervisord.conf  # 生成一个配置文件
sudo supervisord -c supervisord.conf      # 使用该配置文件启动supervisord
sudo supervisorctl                        # 进入命令行界面管理进程
```

## 配置

- **需要注意的是用supervisor管理的进程千万不要开启daemon模式，否则supervisor会认为程序没有启动成功，导致无限开进程...**

```shell
# 在supervisord.conf里面添加如下内容
[program:frontend]                                           # 进程名
process_name=%(program_name)s_%(process_num)02d # 指定当前进程的名称
command=/usr/bin/python manage.py runserver 0.0.0.0:8000     # 启动该进程的命令
directory=/media/sf_company/frontend/frontend                # 在执行上面命令前切换到指定目录
startsecs=0
startretries=3		# 启动失败自动重试次数，并不是程序退出autorestart的次数
stopwaitsecs=0
autostart=false
autorestart=false	# 当未false的时候不会自动重启，当未true的时候只要挂了就会重启，当未unexpected的时候，如果退出码是unexpected才会重启
user=root
stdout_logfile=/root/log/8000_access.log                     # 访问日志
stderr_logfile=/root/log/8000_error.log                      # 错误日志
redirect_stderr=true	# 将错误重定向到stdout，默认未false

# 分组的配置，可以统一管理几个程序，需要注意的是，group下面只有programs和priority两个属性可以设置，像autostart等参数在这里面设置是无效的
[group:my_group]
programs=program_name1,program_name2
priority=999
```

这样就创建了一个进程，进程的名称为frontend。

由于ubuntu上面supervisor的配置文件可以放在`/etc/supervisor.d/*.ini`里面比较方便，但是会出现一些错误。如果是单独的ini文件，那么不仅要写`program`这个section还应该把`supervisord`、`supervisorctl`两个区块都加上，哪怕不写任何东西。

## supervisorctl常用命令：

```shell
supervisorctl start name    # 开始一个进程
supervisorctl stop name    # 终止一个进程
supervisorctl status   # 查看当前管理状态
```

### TroubleShooting

- **安装过程出现`unix:///var/run/supervisor.sock no such file`**:

  ```shell
  # 首先删除通过apt-get安装的supervisor
  sudo apt-get remove supervisor
  # 然后把相应的进程kill掉
  sudo ps -ef | grep supervisor
  # 最后直接用easy_install安装
  sudo easy_install supervisor
  # 然后生成配置文件
  sudo echo_supervisor_conf > /etc/supervisord.conf
  # 最后启动
  sudo supervisord
  sudo supervisorctl
  ```

- **执行`sudo supervisorctl reload`**时出现错误`error: <class 'socket.error'>, [Errno 2] No such file or directory: file: /usr/lib64/python2.7/socket.py line: 224`原因是supervisor没有启动而重启造成的，我也不知道为什么报的错误会是这个错误。这时候只需要启动supervisor即可



参考文章：<http://segmentfault.com/a/1190000002991175>(原文中还有使用OneAPM安装Python探针的应用，可以实时监控web应用数据，暂时还未实践)