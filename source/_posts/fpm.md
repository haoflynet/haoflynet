---
title: "fpm 打包工具"
date: 2016-08-07 05:52:39
updated: 2018-10-18 16:47:00
categories: tools
---

# fpm打包工具

## 安装过程

```shell
yum install -y rpm-build ruby-devel virtualenv gcc
pip install virtualenv-tools 
gem install fpm
fpm -h
```
## 常用参数
- -a: 架构名称，值可以为`  x86_64`
- --config-files: 指定配置文件，可以指定多个
- -d '名称': 指定程序依赖，多个依赖的话就写多个-d
- --debug：打印编译时的详细日志
- -C: 指定在打包前需要进入的目录(打包时的相对路径)，相当于把那个目录打包
- -n: 包名
- -s: 源的类型，值可以为dir,rpm,gem,python,virtualenv,empty,tar,deb,cpan,npm,osxpkg,pear,pkgin,zip
- -t: 目标类型，值可以为rpm,deb,solaris,puppet,dir,osxpkg,p5p,puppet,sh,solaris,tar,zip
- -v: 版本号，例如`1.0.0`
- --before-install 名称.sh: 安装前执行的脚本
- --after-install 名称.sh: 安装后执行的脚本
- --before-remove 名称.sh: 卸载前执行的操作
- --after-remove 名称.sh: 卸载后执行的操作
- --prefix=目录: 指定软件之后要安装的路径
- --description '这里写描述'
- --url: 软件的网官网
- --license '2-clause BSD-like license': 
- --prefix: 指定安装目录
- --vendor: 供应商名称
- --verbose: 打印详细安装过程
- -m, --maintainer: 维护者
- --rpm-sumarry '': 简介
- --description '': 详情

## 以Virtualenv的方式打包Python包

相比与`-s python`的方式，将源设置为`virtualenv(即-s virtualenv)`的好处是不会破坏系统本身的python环境，不会与已经安装的包或者其他程序依赖的包产生冲突。举例，有一个需要打包的python包源码目录结构为：

```python
.
├── Pipfile			# 自己开发时使用的是pipfile进行依赖管理，当然对fpm打包没有影响
├── Pipfile.lock
├── README.md
├── etc				# 一些典型的配置文件
│   ├── logrotate.d	# 日志轮转配置文件
│   │   └── my-agent
│   ├── rc.d		# 系统服务配置文件，该文件编写方式有点特殊，可以去谷歌一下
│   │   └── init.d
│   │       └── my-agent
│   └── my-agent	# 程序本身配置文件
│       └── default.conf
├── usr        # lib文件默认会被加入/usr/lib中，所以，这里直接以目录树形式存储
│   └── lib
│       └── my-agent
│           └── agent.state
├── scripts
│   ├── my-agent-after-install.sh
│   └── my-agent-before-remove.sh
├── setup.py		# 正常打python egg包所需要的文件，里面定义了包的一些元信息
└── src				# 程序源码
    ├── xxx.py
	└── __init__.py
```

然后使用这样的命令进行打包

```shell
fpm \
	--debug \
	-s virtualenv \		# 指定以virtualenv的形式进行打包
	-t rpm \
	-n my-agent \
	-a 'x86_64' \
	-v 0.1.0 \
	--license '2-clause BSD-like license' \
	--vendor 'Hao inc.' \
	--category 'System Environment/Daemons' \
	-m 'haofly' \
	--config-files etc/my-agent/default.conf \
	--config-files etc/logrotate.d/my-agent \
	--config-files etc/rc.d/init.d/my-agent \
	--after-install ./scripts/my-agent-after-install.sh \
	--before-remove ./scripts/my-agent-before-uninstall.sh \
	--url 'https://haofly.net' \
	--rpm-summary 'rpm summary.' \
	--description 'package description' \
	--prefix /usr/share/my-agent \	# 指定安装目录，如果不指定会默认安装到/usr/share/python/下面
	.
```

## 其他相关命令

```shell
rpm localinstall 包名 # 在新的机器上安装该软件
rpm -qpl 包名  # 查看包的信息
```

[打包nginx例子](http://www.z-dig.com/fpm-custom-nginx-rpm-package.html)

这是我打包tengine的命令`fpm -s dir -t rpm -n tengine -v 2.1.2 -C /etc/nginx -d 'pcre-devel' -d 'openssl' -d 'openssl-devel' --before-install /share/before-install.sh --after-install /share/after-install.sh --before-remove /share/before-remove.sh --after-remove /share/after-remove.sh --description 'Haofly first fpm package' --url 'http://haofly.net' --prefix=/etc/nginx
`