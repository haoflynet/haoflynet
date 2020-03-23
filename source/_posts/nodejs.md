---
title: "node.js教程"
date: 2015-12-07 10:02:30
updated: 2020-03-10 07:50:30
categories: frontend
---
# node.js教程

## 安装
需要注意的是，关于npm的所有命令，最好都不要用root用户执行，否则会出现各种不可预料甚至连官方文档都说不清的问题

稳定版: 

```shell
# centos用下面命令安装指定版本nodejs
sudo curl --silent --location https://rpm.nodesource.com/setup_6.x | sudo bash -
sudo yum install -y nodejs

# ubuntu用下面命令安装指定版本nodejs
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

- 报名前面带"@"符号的，表示是属于某个组织，又组织上传到镜像源里面的

#### Nvm

可以通过`nvm`来同时使用多个`node`版本，mac上可以直接`brew install nvm`进行安装，安装完成后根据提示添加`sh`的`rc`文件，常用命令如下:

```shell
nvm ls-remote	# 查看所有可用的node版本
nvm install xxx	# 下载需要的版本
nvm use xxx	# 使用指定的版本
nvm alias default xxx 	# 设置默认的node版本
```

#### Npm

```shell
npm init		# 将当前目录设置为一个npm库，自动生成package.json文件，如果没有package.json文件可以用这个方法生成，它也会自动把node_module下的已安装包加进来的
npm install 包名 --save	# 安装包，并且更新到package.json中去
npm install 报名 --save-dev	# 安装包，并且更新到package.json的开发依赖中区
npm list --depth=0	# 列出已安装模块
npm list -g --depth=0 # 列出全局安装的包
npm list --depth=0 2> /dev/null	# 忽略标准错误输出(npm ERR!这种错误将被忽略
npm update 			# 升级当前目录下的所有模块
npm update 包名		# 更新指定包
npm install npm -g	# 升级npm
npm install -g n && n stable # 升级node.js到最新稳定版
升级node.js

npm config delete name	# 删除某个配置

# 代理设置
npm config set proxy=http://127.0.0.1:1080
npm config set proxy=https://127.0.0.1:1080
```
#### yarn

- `yarn`从`1.10x`开始会在`yarn.lock`中增加`integrity`字段，用于验证包的有效性

```shell
yarn add 包名	# 安装包
npm install yarn@latest -g	# 升级yarn
```

## TroubleShooting

- **Permission Denied**问题，使用npm命令总是会出现这个问题，解决方法最简单的是把npm目录的拥有者修改为当前用户的名字` sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}`
- **安装包时报错Unexpected end of JSON input while parsing near ' : '** 尝试先执行`npm cache clean --force`，然后再安装
- **gyp: No Xcode or CLT version detected!**: 需要先安装`xcode`命令工具: `xcode-select --install`

##### 扩展阅读

**[N-club](https://github.com/nswbmw/N-club):** 使用Koa + MongoDB + Redis搭建的论坛系统

[不容错谷哦的Node.js项目架构](https://mp.weixin.qq.com/s/nivph5JV_sovSDDSCsKmAA)