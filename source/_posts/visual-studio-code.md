---
title: "Visual Studio Code使用手册及扩展推荐"
date: 2018-04-09 21:32:00
updated: 2018-05-17 13:48:00
categories: 工具
---
`sublimetext`因为年久失修基本被人遗忘了，`Atom`火了一阵子，由于性能问题也没人再提了，如今最火的最强大的而且还免费的编辑器绝对是`Visual Studio Code`。经历过几次试用与放弃，最终我又回到了`Visual Studio Code`。总的感受来说，因为是编辑器，所以用起来会感觉很轻便；又因为插件丰富，所以各种语言都有比较好的支持。当然，这里也只能说是`比较好`，在专业性上，肯定是比不过`idea`家的东西的，所以现在对于我来说，我会在`Visual Studio Code`上开发`GO`和`Javascript`，在`Idea`上面开发`Python`、`Java`和`Php`。

## 常用快捷键

for mac os

```shell
Cmd + P: 输入文件名，快速打开文件
Cmd + P: 输入:n，直接跳转到指定的行

Cmd + N: 新建文件
Cmd + Shift + N: 打开一个新的窗口(工程)

Cmd + \: 水平增加栏
Cmd + 1/2/3: 在左中右几个编辑器间切换

Cmd + Enter: 在下面插入一行

Cmd + F: 查找
Cmd + Shift + F: 全局查找
Cmd + Shift + H: 查找并替换


Ctrl + Tab: 在最近打开的文件中切换

Option + Shift + F: 格式化代码
Option + Delete: 删除一行
```

## 扩展推荐

<!--more-->

### 通用扩展

- **Auto Close Tag**: 自动关闭标签
- **Copy Relative Path**: 我就不明白了，复制相对路径这个硬需求居然没有自带
- **DotENV**: .env文件扩展
- **embrace**: 快速在选中代码的两边添加引号等符号
- **Gitlens**: 直接查看光标指定位置的代码在git流中的修改时间、作者信息等信息
- **Project Manager**: 快速切换Project，终于不用再重新开窗口了
- **TODO Highlight**: 高亮TODO

### JavaScript系列开发

#### React Native

- **React Native Tools**: 功能最全

### Python开发

如果项目env使用的是`pipenv`，那么需要直接在项目设置(即`.vscode/settings.json`)中指定python解释器的位置，例如`"python.pythonPath": "/home/myuser/.local/share/virtualenvs/projectname/bin/python"  `

- **autoDocstring**: 自动生成python风格的`docstring`
- **Python** 官方插件。

### Go开发

- **Go**: 官方插件。能对go进行快速的编译运行及调试。安装完成后需要`gopath`目录，在用户设置里面添加一条` "go.gopath": "/usr/local/gopath"`，然后在命令面板先执行`Go install tools`命令来安装一些go必要的命令行工具，在调试的时候，如果出现`cannot find delve`错误，表示这个调试组件没安装上，需要手动安装，安装步骤见[derekparker/delve](https://github.com/derekparker/delve/blob/master/Documentation/installation/osx/install.md)

### PHP开发

已经尝试过不只一次，相比于`Phpstorem(EAP)`来说，`visual studio code `在开发的时候无论是哪个层面都比不上`PhpStorem`。

- **PHP DocBlocker**: PHP注释文档自动生成工具
- **PHP Getters & Setters**: 快速`Getter`和`Seters`
- **PHP Intelephense**: 相比于其他几个下载量很高的php扩展，目前发现的只有这个扩展对`goto definition`支持好一点，其他的几乎都不能跳转到`vendor`目录里面去

## 常用设置

### 通用设置

```json
{
    "python.linting.pylintArgs": [
    ],
    
    "python.disablePromptForFeatures": [
        "pylint"
    ],

    "go.gopath": "/usr/local/gopath",	// gopah路径

    "javascript.validate.enable": false,	// 禁止js语法检测，主要针对react native的prop
    "search.useIgnoreFiles": false			// 这样可以在搜索的时候同时搜索vendor目录下的文件
}
```







