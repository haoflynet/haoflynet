---
title: "ionic 教程"
date: 2016-07-27 22:52:39
updated: 2017-10-10 18:00:00
categories: frontend
---
基于AngularJS进行的封装，性能中等。

## ionic开发环境部署

`ionic`app主要使用命令行进行构建并使用`Cordova`用来构建和打包。首先安装[NodeJs](https://haofly.net/nodejs)，然后在[ionic官网](https://dashboard.ionicjs.com)注册一个账号

```shell
npm install -g inoic cordova	# 安装命令行工具
ionic start test				# 创建一个测试项目，期间会提示你登录你的账号
cd test
git push ionic master			# 初始化项目完成后按照提示进行push操作，push到ionic的控制台里面去
ionic serve						# 自动打开网页，第一个项目能跑起来了
```

此时可以去ionic的控制台查看该项目的信息以及设置一些自动构建相关配置了。但是目前只能在web端访问，如果想要生成ios或者android平台的项目还需要安装单独的工具:

```shell
# for IOS，必须首先安装xcode
xcode-select --install	# 安装xcode命令行工具
npm install -g ios-deploy	# 安装ios部署工具
```











函数传递参数

```javascript
import {NavParams} from "ionic-angular";

export class Profile {
  private person;
  constructor(public params:NavParams) {
    this.person = CONTRIBUTORS[params.get('num')];	// 参数是以字典形式传进来的
  }
}

# 在外部
openProfilePage(num) {
  this.nav.push(Profile, {num: num});
}
```

