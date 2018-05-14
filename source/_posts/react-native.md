---
title: "React Native手册"
date: 2017-05-27 14:59:00
updated: 2018-05-13 17:48:00
categories: js
---

## 基础概念

**特别注意: **

- 如果是自己开发新产品，那么希望每次都把各个基础组件升级到最新稳定版。
- 初学者不要用网上的一些`generator`生成程序框架，好多组件用不到，而且版本不对基本上也运行不起来

`React Native`开发的优点

- 拥有系统级别的通知或提醒
- 可以访问本地通讯录、相册等资源
- 可以针对不同的平台提供不同的体验

`React Native`采用的是`ES2015`(即ES6)的语法标准，模板上使用了自己的`JSX`语法(在代码中嵌入结构标记)。

### 环境搭建

命令行工具: `npm install -g react-native-cli`

测试安装: 

```shell
react-native init testProject	# 新建项目目录，并初始化项目
react-native init testProject --version 0.1.2	# 创建指定版本的项目
cd testProject
react-native run-ios	# 第一次启动会很慢。等模拟器运行起来后可以直接Cmd+R刷新应用，Cmd+D打开调试菜单
react-native run-android
```

### prop

属性，相当于传递给`JSX`的变量。

### state

状态，这个才相当于是属性，是可以随时改变的。

## 布局

不用css，但是类似css。所有的组件都有`style`属性。样式名是将默认的css的命名更改为了驼峰命名。一般使用`StyleSheet.create`在组件外面集中定义组件的样式。例如:

```js
// 指定固定的高度和宽度用width和height，React Native中的尺寸都是无单位的。
<View style={{width: 50, height: 50, backgroundColor: 'powderblue'}} />

// 弹性的高度和宽度用flex。flex为1的时候表示撑满所有的剩余空间，如果多个并列子组件一起使用，则他们会平分空间，并且值越大所占比例就越大。例如
<View style={{flex: 2, backgroundColor: 'skyblue'}} />

// 这样还能直接看出来层级关系。例如<Text style={styles.red}>test</Text>
const styles = StyleSheet.create({
  bigblue: {
    color: 'blue',
    fontWeight: 'bold',
    fontSize: 30,
  },
  red: {
    color: 'red',
  },
});
```

#### Flexbox布局

规定某个组件的子元素的布局。

```javascript
// flexDirection: 规定布局方向，默认是column垂直方向布局，row表示水平方向布局。
<View style={{flex: 1, flexDirection: 'row'}}>
// justifyContent: 规定子元素沿着主轴的排列方式。可选项有flex-start、center、flex-end、space-around以及space-between
<View style={{flex: 1, justifyContent: 'row'}}>
// alignItems: 规定子元素沿着次轴(与主元素垂直的轴)的排列方式。可选项有flex-start、center、flex-end、stretch
```

## 组件

### Button按钮

```javascript
<Button
	onPress={() => this._func()}
	title="按钮标题必填"
/>
```

### Component

一个页面需要一个`Component`：

```javascript
export class HomeScreen extends Component {
  constructor(props) {		// 构造函数
    super(props);
    this.state = {
      recognized: '',
      pitch: '',
    };
  }
  componentDidMount() {}	// 组件加载完成后执行，在render之后
  render() {}		// 
}
```

### Navigation导航组件

[Navigation文档](https://reactnavigation.org/docs/hello-react-navigation.html)，Navigation已经单独成为一个模块，强烈建议不再使用老的导航器，[导航器对比](https://www.jianshu.com/p/98db12a6afec)，在这里有其更详细的文档。在`0.44`版本移除了[`Navigator`](https://facebook.github.io/react-native/docs/navigator.html)，该模块被移动到[react-native-custom-components](https://github.com/facebookarchive/react-native-custom-components)现在也仅用于兼容老版本。

默认就使用`React Navigation`，如果仅仅是`Ios`那么推荐用`NavigatorIOS`。使用前得先安装`npm install --save react-navigation`。

```javascript
// StackNavigator用于创建多页面应用。其中每一个都是一个Component
import React from 'react';
import { View, Text } from 'react-native';
import { StackNavigator } from 'react-navigation';

class HomeScreen extends React.Component {
  render() {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Home Screen</Text>
      </View>
    );
  }
}

export default StackNavigator({
  Home: {
    screen: HomeScreen,
  },
});
```

## 网络请求

`React Native`使用的网络请求是[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)，但是，统治js的http请求库明显是`axios`，所以我还是喜欢用`axios`，另外，网络请求天生就应该是异步的，这两个库都是不支持同步的。

```javascript
// 安装npm install --save axios
import axios from 'axios';
axios.get('...').then((response)=>(console.log(response.data))); // 得到响应结果，不用像fetch那样responseJson了
```

## 原生库

开发者会将很多原生库打包成一些静态库，或者由js直接封装好了的静态库。一般比较好的静态库都能够使用命令自动链接:`react-native link 某已安装的具体库名`，如果手动链接可以参考文档[linking-libraries-ios](https://facebook.github.io/react-native/docs/linking-libraries-ios.html)

## TroubleShooting

- **":CFBundleIdentifier" Does Not Exist**: 可能是因为你的代码依赖的是老的`react native`或者`node`版本或者`xcode`版本，可以执行以下命令升级依赖:`react nativeupgrade `
- **undefined is not an object evaluating React.PropTypes.string**: 仍然是版本的问题，新版的已经将`React.PropTypes`移到单独的库了([prop-types](https://reactjs.org/blog/2017/04/07/react-v15.5.0.html))。需要注意的是`React.PropTypes.func`更改成了`PropTypes.function`了，其他的名字没有改，只是位置变了。
- **No bundle url present**: 启动的时候报错，有以下几种解决方案:

  - 全部关了以后，看看8081端口是否被占用，然后重新`react-native run-ios`
- **isMounted(...) is deprecated warning**: [目前来看](https://github.com/react-navigation/react-navigation/issues/3956)，并没有什么解决方案。
- **闪退**: 有如下几种情况
  - 没有给API添加对应的权限，具体权限列表可以参见: [Swift开发MacOS应用](https://haofly.net/swift-macos)

##### 扩展阅读

- 浅谈前端移动开发[(Ionic与React Native)](http://bbs.reactnative.cn/topic/420/%E6%B5%85%E8%B0%88%E5%89%8D%E7%AB%AF%E7%A7%BB%E5%8A%A8%E5%BC%80%E5%8F%91-ionic-%E4%B8%8E-react-native)
- [30天React Native学习](https://github.com/fangwei716/30-days-of-react-native)


- [仿美团示例项目]( https://github.com/huanxsd/MeiTuan)