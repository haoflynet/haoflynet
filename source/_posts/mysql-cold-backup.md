---
title: "MySQL冷备份过程"
date: 2014-11-04 15:59:41
categories: 编程之路
---
额，这是最简单的备份方式，只需要把mysql的数据文件打包并压缩即可，要恢复的时候再把相应的文件拷过去覆盖就行了。

冷备份实际上是最简单的备份方式(好吧，第一次我就差点把数据库搞崩溃了)，但由于要求停止MySQL服务来进行备份和恢复，并且只能完整备份，所以实用性并不高。

# 备份

首先，进入数据库并找出数据文件存放目录：



    mysql> show variables like '\%dir\%';
    +-----------------------------------------+----------------------------+
    | Variable_name                           | Value                      |
    +-----------------------------------------+----------------------------+
    | basedir                                 | /usr                       |
    | binlog_direct_non_transactional_updates | OFF                        |
    | character_sets_dir                      | /usr/share/mysql/charsets/ |
    | datadir                                 | /var/lib/mysql/            |
    | innodb_data_home_dir                    |                            |
    | innodb_log_group_home_dir               | ./                         |
    | innodb_max_dirty_pages_pct              | 75                         |
    | lc_messages_dir                         | /usr/share/mysql/          |
    | plugin_dir                              | /usr/lib/mysql/plugin/     |
    | slave_load_tmpdir                       | /tmp                       |
    | tmpdir                                  | /tmp                       |
    +-----------------------------------------+----------------------------+
    11 rows in set (0.00 sec)

数据目录就是datadir的所在位置，即`/var/lib/mysql/`

然后执行：



    cd /var/lib/                          # 进入其上级目录
    service mysql stop                    # 关闭mysql服务，这里我其实并没有关闭，但我没有在高                                         数据量下测试过
    tar jcvf ~/backup.tar.bz2 mysql/      # 打包压缩该目录到根目录


#  恢复

执行如下命令即可：



    cd ~/                           # 进入备份文件的保存目录
    tar jxvf backup.tar.bz2 mysql/  # 解压
    gunzip -r mysql/                # 递归解压
    service mysql stop              # 必须先关闭服务
    rm -r /var/lib/mysql/           # 删除原目录
    mv ~/mysql/ /var/lib/           # 把备份的文件移动到/var/lib/里面去替代原来的mysql
    service mysql start             # 重启mysql服务

需要注意的是恢复过后，就和原来数据库一模一样了，包括所有的修改和帐号密码等信息。
