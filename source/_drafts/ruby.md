---
title: "Ruby手册"
date: 2017-11-01 21:32:00
categories: ruby
---

很早就想学Ruby了。

## 安装Ruby

```shell
# rvm类似于nvm，可以安装不同版本的ruby
curl -sSL https://get.rvm.io | bash -s stable	# 安装rvm
rvm pkg install openssl	# 有些时候需要提前装这个，不然会出现莫名其妙的错误
rvm install 2.7.2 -C --with-openssl-dir=$HOME/.rvm/usr
rvm install ruby	# 安装ruby
rvm implode # 卸载rvm

# 还有一个工具叫rbenv
sudo apt install rbenv -y
rbenv install 3.0.2	# 安装指定版本的rub
```

