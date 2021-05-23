---
title: "node.js教程"
date: 2015-12-07 10:02:30
updated: 2021-05-22 22:50:30
categories: frontend
---
# node.js教程

## 安装
需要注意的是，关于npm的所有命令，最好都不要用root用户执行，否则会出现各种不可预料甚至连官方文档都说不清的问题

稳定版: 

```shell
# centos用下面命令安装指定版本nodejs
sudo curl --silent --location https://rpm.nodesource.com/setup_10.x | sudo bash -
sudo yum install -y nodejs

# ubuntu用下面命令安装指定版本nodejs
sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
docker里面没有sudo就直接
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y nodejs

# 添加淘宝镜像，既然用的阿里云，那淘宝的镜像也就不介意了...
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
安装package.json 直接`npm install`后面不加package.json的名字

## package.json文件

```json
{
  "scripts": {	// 指定了运行脚本命令的npm命令行缩写
    "start": "node index.js",
    "test": "",
  },
  "bin": {	// 用于指定各个内部命令对应的可执行文件的位置
    "someTool": "./bin/someTool.js"	// 当然这也可以直接在scripts里面写成./node_modules/bin/someTool.js
  },
  "engines": {	// 指定了运行环境
    "node": ">=0.10.3 <0.12",
		"npm": "~1.0.20"
  },
  "dependencies": {	// 指定项目运行所依赖的模块
    "aaa": "~1.2.2",	// 波浪号，这里表示>1.2.2(1.2.x)且<1.3.x
    "bbb": "^1.2.2",	// 插入号，这里表示>1.2.2(1.x.x)且<2.x.x
    "ccc": "latest", // 安装最新版本
  },
  "devDependencies": {	// 指定项目开发所依赖的模块
    
  }
}
```

## 常用命令

- 报名前面带"@"符号的，表示是属于某个组织，又组织上传到镜像源里面的

#### Nvm

- 可以通过`node -v > .nvmrc`将当前node版本限制在文件中，之后在当前目录只需要执行`nvm use`即可自动选择对应的版本

可以通过`nvm`来同时使用多个`node`版本，mac上可以直接`brew install nvm`进行安装，安装完成后根据提示添加`sh`的`rc`文件，常用命令如下:

```shell
nvm ls-remote	# 查看所有可用的node版本
nvm install xxx	# 下载需要的版本
nvm use xxx	# 使用指定的版本
nvm alias default xxx 	# 设置默认的node版本
```

#### npm

```shell
npm init		# 将当前目录设置为一个npm库，自动生成package.json文件，如果没有package.json文件可以用这个方法生成，它也会自动把node_module下的已安装包加进来的
npm install 包名 --save	# 安装包，并且更新到package.json中去
npm install 包名 --save-dev	# 安装包，并且更新到package.json的开发依赖中区
npm install 包名@3.1.0 --save	# 安装指定版本的包
npm install git+https://github.com/haoflynet/example.git	# 从Github仓库安装模块
npm list --depth=0	# 列出已安装模块
npm list -g --depth=0 # 列出全局安装的包
npm list --depth=0 2> /dev/null	# 忽略标准错误输出(npm ERR!这种错误将被忽略
npm view 包名 versions	# 列出指定包的所有版本
npm update 			# 升级当前目录下的所有模块
npm update 包名		# 更新指定包
npm install npm -g	# 升级npm
npm install -g n && n stable # 升级node.js到最新稳定版
升级node.js

npm config delete name	# 删除某个配置

#  代理设置
npm config set proxy=http://127.0.0.1:1080 && npm config set proxy=https://127.0.0.1:1080
```
#### Yarn

- `yarn`从`1.10x`开始会在`yarn.lock`中增加`integrity`字段，用于验证包的有效性

```shell
yarn add 包名	# 安装包
npm install yarn@latest -g	# 升级yarn
yarn dev -p 8000	# yarn能直接将参数传递给scripts，npm不行
```

## ~~使用Forever管理NodeJs应用~~(生产环境最好用[pm2](https://haofly.net/pm2))

- 直接使用`sudo npm install forever -g`进行安装

### forever常用命令

```shell
forever list	# 查看当前所有管理的服务
forever stopall 	# 停止所有服务
forever stop 服务ID	# 停止指定服务
forever restartall	# 重启所有服务
forever logs -f 服务ID	# 查看某个服务的日志

# 下面这些命令一般用于非config文件启动方式
forever server.js	# 直接启动进程
forever start server.js	# 以daemon方式启动进程
forever start -l /var/log/forever.log -a server.js	# 指定日志文件
forever start -o /var/log/forever/out.log -e /var/log/forever/err.log -a server.js	# 分别指定日志和错误日志文件，-a表示追加
forever start -w server.js	# 监听文件夹下所有文件的改动并自动重启
```

## 常用包推荐

- [uuid](): uuid首选version 4，每秒生成10亿个，大约需要85年才会重复

## TroubleShooting

- **Permission Denied**问题，使用npm命令总是会出现这个问题，解决方法最简单的是把npm目录的拥有者修改为当前用户的名字` sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}`
- **安装包时报错Unexpected end of JSON input while parsing near ' : '** 尝试先执行`npm cache clean --force`，然后再安装
- **gyp: No Xcode or CLT version detected!**: 需要先安装`xcode`命令工具: `xcode-select --install`
- **npm install结果被系统killed掉了**: 一般是内存不足，可以使用增加swap的方法，参考[Linux 手册](https://haofly.net/linux/index.html)
- **ReferenceError: describe is not defined NodeJs**: 应该是`mocha`这个测试库报的错，安装它即可: `npm install mocha -g`
- **wasm code commit Allocation failed - process out of memory**: 在Apple m1(apple silicon)上npm编译失败，可以尝试将`node`升级到`v15.3.0`及以上
- **a promise was created in a handler but was not returned from it**: 通常是`bluebird`报错，函数没有正确地返回，遇到这个情况一个是验证回掉函数`then`是否有正确的返回，如果没有，那么可以添加一个`return null`语句，需要注意的是，如果`then`回掉里面只有一个语句，例如`.then(res => res + 'abc')`，这样不用单独写`return`，但如果里面的语句不只一句就得加了
- **Node Sass does not yet support your current environment: Windows 64-bit with Unsupported runtime (88)**: `npm rebuild node-sass`
- **Error: spawn ../node_modules/optipng-bin/vendor/optipng ENOENT**: 尝试执行`npm rebuild`
- **this._settlePromiseFromHandler is not a function**: 尝试删除`node_module`目录并重新安装

##### 扩展阅读

**[N-club](https://github.com/nswbmw/N-club):** 使用Koa + MongoDB + Redis搭建的论坛系统

[不容错谷哦的Node.js项目架构](https://mp.weixin.qq.com/s/nivph5JV_sovSDDSCsKmAA)