---
title: "SVN 教程"
date: 2016-05-17 11:02:30
categories: tools
---
#SVN指南

## 安装
**[CentOS](https://wiki.centos.org/zh/HowTos/Subversion)**，需要注意的是，完全不需要搭配apache，因为SVN可以自己有一个tcp进程的，通过`svnserve -d -r=/路径`来启动，默认监听端口为3690

## 常用命令

    svnadmin create 仓库名 # 新建仓库，该命令会在当前目录创建一个与仓库名同名的文件夹，文件夹下包含该库的所有信息，在`conf`目录下，passwd表示用户名和密码，格式为用户名=密码  
    然后修改`svnserve.conf`，把下面几行的注释去掉：
    anon-access = read
    auth-access = write
    password-db = passwd
    authz-db = authz
    realm = svnhome（注意）
    
    svn checkout path
    svn add file

### post-commit hook配置

    编辑仓库配置文件里面的hook，内容如下：
    REPOS="$1"
    REV="$2"s
    
    cd /var/www/directory && /usr/bin/svn update --username user --password pass
