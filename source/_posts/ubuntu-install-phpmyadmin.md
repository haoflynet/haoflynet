---
title: "Ubuntu安装phpmyadmin"
date: 2014-11-09 15:26:43
categories: 编程之路
---
参考：<https://www.digitalocean.com/community/tutorials/how-to-install-and-
secure-phpmyadmin-on-ubuntu-12-04>

最近由于工作需要，必须得短时间内建立好一个数据库，但是不想在平板电脑上装太多的软件，所以直接在服务器上安装了phpmyadmin，发现其安装方法不是一条ap
t就能解决的，所以特别记录一下：

系统环境：ubuntu14.04(server) + apache2 + MySQL5.5

安装步骤：

# 1.获取phpmyadmin



    sudo apt-get install phpmyadmin apache2-utils

#  2.修改配置文件

在apache配置文件里面添加声明：



    vim /etc/apache2/apache2.conf




    # 在该文件里面添加如下一行即可




    Include /etc/phpmyadmin/apache.conf

#  3.重启服务



    service apache2 restart

#  4.安全问题

phpmyadmin的远程访问方面的安全问题，我还没去涉及，可以直接参考本文章顶部的参考文章进行配置。
