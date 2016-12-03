---
title: "phpMyAdmin教程"
date: 2016-08-03 11:02:30
categories: php
---
# phpMyAdmin

[CentOS 6.4安装phpMyAdmin](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-a-centos-6-4-vps)

### 连接多个主机的配置
[参考文章](http://blog.51yip.com/mysql/1250.html)
配置如下：
1. 将phpMyAdmin根目录下的config.sample.inc.php，重命名为config.inc.php
2. 修改config.inc.php文件，添加如下内容：

        $connect_hosts = array(
            1 => array(
                "host"	=> "127.0.0.1",
                "port"	=> "3307",
                "socket"=> "/tmp/mysql.sock2",
                "user"	=> "root",
                "password"	=> "mysql",
                "connect_type"	=> "socket"
                ),
            2 => array(
                "host"	=> "127.0.0.1",
                "port"	=> "3309",
                "user"	=> "root",
                "password"	=> "mysql",
                "connect_type"	=> "tcp"
                )
            );
       
        for ($i=1;$i<=count($connect_hosts);$i++){  
            $cfg['Servers'][$i]['auth_type'] = 'cookie';  
            $cfg['Servers'][$i]['host'] = $connect_hosts[$i]['host'];   //修改host  
            $cfg['Servers'][$i]['connect_type'] = $conenct_hosts[$i]['connect_type'];  
            $cfg['Servers'][$i]['port'] = $connect_hosts[$i]['port'];
            if (array_key_exists('socket', $connect_hosts[$i])){
            $cfg['Servers'][$i]['socket'] = $conenct_hosts[$i]['socket'];
            }
            $cfg['Servers'][$i]['compress'] = false;  
            $cfg['Servers'][$i]['extension'] = 'mysql';  
            $cfg['Servers'][$i]['AllowNoPassword'] = true;  
            $cfg['Servers'][$i]['user'] = $connect_hosts[$i]['user'];  //修改用户名  
            $cfg['Servers'][$i]['password'] = $connect_hosts[$i]['password']; //密码  
            $cfg['Servers'][$i]['bs_garbage_threshold'] = 50;  
            $cfg['Servers'][$i]['bs_repository_threshold'] = '32M';  
            $cfg['Servers'][$i]['bs_temp_blob_timeout'] = 600;  
            $cfg['Servers'][$i]['bs_temp_log_threshold'] = '32M';  
        }
3. 重启apache

## TroubleShooting
- 如果出现`#2002 无法登录 MySQL 服务器`错误，可能是地址填写的是localhost而不是127.0.0.1所致
