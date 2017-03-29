---
title: "MAC OSX 教程"
date: 2016-09-06 01:02:30
updated: 2017-03-28 15:08:00
categories: system
---
# MAC指南

## Homebrew

```shell
export ALL_PROXY=socks5://127.0.0.1:1080	# homebrew走ss代理
```

## 更换文件图标

http://www.cnblogs.com/wormday/archive/2011/05/06/2038703.html

## 自制iPhone铃声

[iTunes 簡單自製 iPhone 鈴聲不求人](http://applefans.today/blog/1266100502)

### Mackup配置备份

```shell
brew install mackup

vim ~/.mackup.cfg进行配置
[storage]
engine = file_system	# 表示用文件系统进行存储
path = /Users/haofly/OneDrive	# 指定路径

mackup backup	# 备份命令
mackup restore	# 数据恢复
mackup uninstall# 将配置文件拷回原来的系统目录
```



## TroubleShooting

- **磁盘空间爆了，重启后spotlight一直显示正在索引**: 原因可能是误删了索引的文件(索引文件确实有哦几个G)，修复需要执行以下几个命令：

   sudo mdutil -i off /
   	sudo mdutil -E /
   	sudo mdutil -i on /