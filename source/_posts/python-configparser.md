---
title: "Python3使用configparser模块设置配置信息"
date: 2014-10-19 20:47:37
categories: 编程之路
---
参考文档：<https://docs.python.org/3/library/configparser.html#module-configparser>

今天在研究MySQL Connector for Python的时候无意间发现原来Python自带了设置与读取配置信息的模块的，有了这么一个功能就能够在一个
单独的文件里面写上一些敏感信息，比如你的数据库的用户名密码等，以后要使用的时候直接读取该文件即可。这里简要描述一下其使用方法。

首先，得要有一个文件用来保存配置信息，格式如下setting.conf：



    [DATABASE]
    Port = 21
    Username = haofly
    Password = 123456
    Database = test




    [DEFAULT]
    User = hg


需要注意的是，在配置文件里字符串是不加引号的，因为无论是字符串还是数字，读取出来都是字符串的形式。

在另一个文件中使用方法如下：



    import configparser




    config = configparser.ConfigParser()
    config.sections()
    config.read('co.config')
    print(config['DATABASE']['Username'])

打印出来`haofly`
