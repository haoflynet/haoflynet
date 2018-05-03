---
title: "React Native手册"
date: 2017-05-27 14:59:00
updated: 2018-05-03 23:48:00
categories: js
---

Native App开发的优点

- 拥有系统级别的通知或提醒
- 可以访问本地通讯录、相册等资源
- 可以针对不同的平台提供不同的体验

## 环境搭建

命令行工具: `npm install -g react-native-cli`

测试安装: 

```shell
react-native init testProject	# 新建项目目录
react-native init testProject --version 0.1.2	# 创建指定版本的项目
cd testProject
react-native run-ios	# 
react-native run-android
```

##### 扩展

## 原生库

开发者会将很多原生库打包成一些静态库，或者由js直接封装好了的静态库。一般比较好的静态库都能够使用命令自动链接:`react-native link 某已安装的具体库名`，如果手动链接可以参考文档[linking-libraries-ios](https://facebook.github.io/react-native/docs/linking-libraries-ios.html)

## TroubleShooting

- **":CFBundleIdentifier" Does Not Exist**: 可能是因为你的代码依赖的是老的`react native`或者`node`版本或者`xcode`版本，可以执行以下命令升级依赖:`react nativeupgrade `

- **undefined is not an object evaluating React.PropTypes.string**: 仍然是版本的问题，新版的已经将`React.PropTypes`移到单独的库了([prop-types](https://reactjs.org/blog/2017/04/07/react-v15.5.0.html))。需要注意的是`React.PropTypes.func`更改成了`PropTypes.function`了，其他的名字没有改，只是位置变了。

- **No bundle url present**: 启动的时候报错，有以下几种解决方案:

  - 全部关了以后，看看8081端口是否被占用，然后重新`react-native run-ios`

- **isMounted(...) is deprecated warning**: [目前来看](https://github.com/react-navigation/react-navigation/issues/3956)，并没有什么解决方案。

##### 扩展阅读

- 浅谈前端移动开发[(Ionic与React Native)](http://bbs.reactnative.cn/topic/420/%E6%B5%85%E8%B0%88%E5%89%8D%E7%AB%AF%E7%A7%BB%E5%8A%A8%E5%BC%80%E5%8F%91-ionic-%E4%B8%8E-react-native)
- [30天React Native学习](https://github.com/fangwei716/30-days-of-react-native)


- [仿美团示例项目]( https://github.com/huanxsd/MeiTuan)