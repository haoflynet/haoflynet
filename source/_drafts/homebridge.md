---
title: "畅玩儿HomeKit/HomeBridge"
date: 2017-11-29 21:52:39
categories: 编程之路
---

`HomeKit`是苹果退出的智能家居解决方案，但原生支持`HomeKit`智能家居的价格完全是可望不可即的。然而，有大神将`HomeKit`的协议进行了破解得到并开源出来[homebridge](https://github.com/nfarina/homebridge)，使得其玩儿法变得超级之多。这里有一份国内智能家居的[homebridge插件清单](http://homekit.yinhh.com/)。

## HomeBridge基础安装与设置

```shell
# 安装
npm install -g --unsafe-perm homebridge
# 运行
homebridge
# 创建配置文件
mkdir ~/.homebridge && cd ~/.homebridge
vim config.json
# 配置文件内容
{
	"bridge": {
      "name": "homebridge的名称，随便填就好了",
      "username": "29:6C:07:85:F3:33",
      "port": 51826,
      "pin": "233-78-123"
	},
	"platforms": [
	]
}
```

在准备就绪以后，就可以一次安装`HomeBridge`的相关插件了。

## 与小米智能家居联动

