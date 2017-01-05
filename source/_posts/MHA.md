---
title: "MHA 教程"
date: 2016-07-07 11:02:30
categories: database
---
# MhA
很强大，不过我认为已经是老古董了，本身没有自带MySQL代理，配合Atlas能发挥很好的作用，不过由于很久没更新，导致很多问题至今未解决，比如，更换主从过后会宕掉，主机恢复后不能自动加入等特性。
[安装教程1](http://huoding.com/2011/12/18/139)
[安装教程2](http://ruiaylin.github.io/2015/03/03/master-ha-install-conf/)


    [server default]
    ssh_user=root
    user=mha_test
    password=mysql
    secondary_check_script=masterha_secondary_check -s remote_host1 -s remote_host2 # 这里要修改名字哟
    master_ip_failover_script=/script/masterha/master_ip_failover # 该脚本就是主机宕掉后的触发脚本
