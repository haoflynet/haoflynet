---
title: "fpm 打包工具"
date: 2016-08-07 05:52:39
categories: tools
---

# fpm打包工具

## 安装过程

    yum install -y rpmbuild ruby-devel gcc
    gem install fpm
    fpm -h
## 常用参数
- -s: 源的类型，值可以为dir,rpm,gem,pyton
- -t: 目标类型，值可以为rpm,deb,solaris,puppet
- -n: 包名
- -v: 版本号
- -C: 指定在打包前需要进入的目录，相当于把那个目录打包
- -d '名称': 指定程序依赖，多个依赖的话就写多个-d
- --before-install 名称.sh: 安装前执行的脚本
- --after-install 名称.sh: 安装后执行的脚本
- --before-remove 名称.sh: 卸载前执行的操作
- --after-remove 名称.sh: 卸载后执行的操作
- --prefix=目录: 指定软件之后要安装的路径
- --description '这里写描述'
- --url: 软件的网站

## 其他命令

    rpm localinstall 包名 # 在新的机器上安装该软件
    rpm -qpl 包名  # 查看包的信息

[打包nginx例子](http://www.z-dig.com/fpm-custom-nginx-rpm-package.html)

这是我打包tengine的命令`fpm -s dir -t rpm -n tengine -v 2.1.2 -C /etc/nginx -d 'pcre-devel' -d 'openssl' -d 'openssl-devel' --before-install /share/before-install.sh --after-install /share/after-install.sh --before-remove /share/before-remove.sh --after-remove /share/after-remove.sh --description 'Haofly first fpm package' --url 'http://haofly.net' --prefix=/etc/nginx
`