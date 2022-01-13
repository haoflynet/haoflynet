---
title: "SVN 教程"
date: 2015-06-17 11:02:30
updated: 2022-01-04 11:08:00
categories: tools
---
## 安装

### 服务端安装

**[CentOS](https://wiki.centos.org/zh/HowTos/Subversion)**，需要注意的是，完全不需要搭配apache，因为SVN可以自己有一个tcp进程的，通过`svnserve -d -r=/路径`来启动，默认监听端口为3690

### 客户端安装

```shell
brew install svn
```

## 常用命令

### 服务端

```shell
svnadmin create 仓库名 # 新建仓库，该命令会在当前目录创建一个与仓库名同名的文件夹，文件夹下包含该库的所有信息，在`conf`目录下，passwd表示用户名和密码，格式为用户名=密码  
然后修改`svnserve.conf`，把下面几行的注释去掉：
anon-access = read
auth-access = write
password-db = passwd
authz-db = authz
realm = svnhome（注意）
```

### 客户端

```shell
svn status	# 查看当前目录下的改动信息
svn diff # 对比当前目录下的更改
svn revert file	# 放弃某个文件的更改
svn revert -R ./	# 放弃本地所有的更改

svn list URL	# 列出分支和tag
svn checkout URL
svn add file
svn commit file1 file 2 -m "commit comment"	# 直接提交文件

svn update	# 更新svn仓库，相当于git pull
svn log -l 10	# 列出最近10条提交记录
```

### post-commit hook配置

```shell
编辑仓库配置文件里面的hook，内容如下：
REPOS="$1"
REV="$2"s

cd /var/www/directory && /usr/bin/svn update --username user --password pass
```
