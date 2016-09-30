---
title: "使用Supervisor管理进程"
date: 2015-08-11 10:07:33
updated: 2016-09-23 11:03:00
categories: 编程之路
---
参考文章：<http://segmentfault.com/a/1190000002991175>(原文中还有使用OneAPM安装Python探针的应用，可以实时监控web应用数据，暂时还未实践)

supervisor是使用Python编写的进程管理软件，在实际开发中，一般用它来同时开始一批相关的进程，无论是Django的runserver还是直接管理Nginx、Apache等，都比较方便，这里是其使用方法：

## 安装

    # ubuntu
    apt-get install supervisor
    service supervisor restart
    
    # centos
    yum install supervisor
    /etc/init.d/supervisord restart


    # 如果安装出现unix:///var/run/supervisor.sock no such file这样的错误，那么请参考：http://tuzii.me/diary/522dc528848eea683d7724f2/\%E8\%A7\%A3\%E5\%86\%B3ubuntu-supervisor-unix:var-run-supervisor.sock-no-such-file.\%E7\%9A\%84\%E6\%96\%B9\%E6\%B3\%95




    sudo easy_install supervisor
    echo_supervisord_conf > supervisord.conf  # 生成一个配置文件
    sudo supervisord -c supervisord.conf      # 使用该配置文件启动supervisord
    sudo supervisorctl                        # 进入命令行界面管理进程

## 设置一个进程



    # 在supervisord.conf里面添加如下内容
    [program:frontend]                                           # 进程名
    command=/usr/bin/python manage.py runserver 0.0.0.0:8000     # 启动该进程的命令
    directory=/media/sf_company/frontend/frontend                # 在执行上面命令前切换到指定目录
    startsecs=0
    stopwaitsecs=0
    autostart=false
    autorestart=false
    user=root
    stdout_logfile=/root/log/8000_access.log                     # 访问日志
    stderr_logfile=/root/log/8000_error.log                      # 错误日志


这样就创建了一个进程，进程的名称为frontend

## supervisorctl常用命令：



    start name    # 开始一个进程
    stop name    # 终止一个进程
    status   # 查看当前管理状态
