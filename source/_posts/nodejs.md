---
title: "node.js教程"
date: 2015-12-07 10:02:30
updated: 2016-02-22 11:00:00
categories: frontend
---
# node.js教程

## 安装
需要注意的是，关于npm的所有命令，最好都不要用root用户执行，否则会出现各种不可预料甚至连官方文档都说不清的问题

稳定版: 

```shell
＃ centos用
sudo curl --silent --location https://rpm.nodesource.com/setup_6.x | sudo bash -
sudo yum install -y nodejs

＃ ubuntu用
sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
docker里面没有sudo就直接
curl -sL https://deb.nodesource.com/setup_4.x | bash -
apt-get install -y nodejs

# 添加淘宝镜像，既然用的阿里云，那淘宝的镜像也就不介意了...
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
测试版:
把4换成6就行了

安装package.json 直接`npm install`后面不加package.json的名字


## 常用命令

```shell
npm init		# 将当前目录设置为一个npm库，自动生成package.json文件
npm install 包名 --save	# 安装包，并且更新到package.json中去
npm install 报名 --save-dev	# 安装包，并且更新到package.json的开发依赖中区
npm list --depth=0	# 列出已安装模块
npm list -g --depth=0 # 列出全局安装的包
npm list --depth=0 2> /dev/null	# 忽略标准错误输出(npm ERR!这种错误将被忽略)
npm update 			# 升级当前目录下的所有模块
npm update 包名		# 更新指定包
npm install npm -g	# 升级npm
npm install -g n && n stable # 升级node.js到最新稳定版
升级node.js
```