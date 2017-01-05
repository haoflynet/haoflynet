---
title: "puppet"
date: 2016-03-07 11:02:30
categories: server
---
# puppet

## 安装
### Server端

    yum install -y puppetserver
    service puppetserver start  # 有些用的是puppetmaster,如果启动报内存限制，那么修改配置/etc/sysconfig/puppetserver将 JAVA_ARGS="-Xms512m -Xmx512m"修改为JAVA_ARGS="-Xms2g -Xmx2g"
### Client端

    sudo rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm # 这里要注意版本是6还是7
    yum install -y puppet-agent

### dashboard的安装
[参考文章](http://centoshowtos.org/configuration-management/puppet/puppet-dashboard/)

    # 首先得有数据库
    create database puppetdash # 创建用户
    grant all privileges on puppetdash.* to puppetdash@localhost identified by 'password';
    flush privileges;
    
    # 安装软件
    rpm -ivh http://yum.puppetlabs.com/el/6/products/x86_64/puppetlabs-release-6-1.noarch.rpm
    yum -y install puppet-dashboard
    
    # 修改puppet-dashboard配置
    cp /usr/share/puppet-dashboard/config/settings.yml.example /usr/share/puppet-dashboard/config/settings.yml
    vim /usr/share/puppet-dashboard/config/database.yml 内容如下：
    /usr/share/puppet-dashboard/config/database.yml
    production:
     database: puppetdash
     username: puppdash
     password: motorrobot
     encoding: utf8
     adapter: mysql
    development:
     database: puppetdash
     username: puppdash
     password: motorrobot
     encoding: utf8
     adapter: mysql
    
    # 生成数据
    cd /usr/share/puppet-dashboard
    rake db:migrate
    /etc/init.d/puppet-dashboard start
    
    # 修改puppet的配置
    vim /etc/puppet/puppet.conf # 添加内容
    report = true
    [master]
    reports = store, http
    reporturl = http://192.168.99.1:3000/reports/upload
    
    # 启动服务
    puppetd -t
    chown puppet-dashboard /usr/share/puppet-dashboard/log/
    chkconfig puppet-dashboard on
    chkconfig puppet-dashboard-workers on
    chkconfig mysqld on
    /etc/init.d/puppet-dashboard restart
    /etc/init.d/puppet-dashboard-workers restart


## [Hello World举例](https://docs.puppetlabs.com/puppet/4.2/reference/quick_start_helloworld.html)

1. 新建module

        cd /opt/puppetlabs/puppet/modules/
        mkdir -p helloworld/manifests/
       
        vim helloworld/manifests/init.pp # 内容如下：
        class helloworld {
            notify { 'hello, world!': }
        }
       
        vim helloworld/manifests/motd.pp # 内容如下：
        class helloworld::motd {
            file { '/etc/motd':
            owner  => 'root',
            group  => 'root',
            mode    => '0644',
            content => "hello, world!\n",
            }
         }

2. 将module添加到主配置文件

        cd /etc/puppetlabs/code/environments/production/manifests
        vim site.pp  # 内容如下：
        node default{
            class { 'helloworld': }
            class { 'helloworld::motd': }
        }

## 测试
分别在两个端启动puppet服务，然后客户端执行`puppet agent -t`


## TroubleShooting
- 客户端显示"no certificate found and waitforcert is disabled"，可以首先在server端`puppet cert list`看看是否有客户端的认证请求，如果有，就在服务器端执行`puppet cert sign agent_name`

- 出现如下错误：

        Exception in thread "main" java.lang.IllegalStateException: Cannot initialize master with partial state; need all files or none.
        Found:
        /etc/puppetlabs/puppet/ssl/private_keys/puppet.novalocal.pem
        Missing:
        /etc/puppetlabs/puppet/ssl/certs/puppet.novalocal.pem

     这个问题一般是由于客户端比服务端先开启服务造成的
     `rm -rf /etc/puppetlabs/puppet/ssl/*`
