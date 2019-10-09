---
title: "React 开发手册"
date: 2019-09-10 14:40:00
updated: 2019-09-16 13:48:00
categories: Javascript
---

## 基本概念

- `React`是一个用于构建用户界面的Javascript库，是`DOM`的一个抽象层
- `React`主要用于构建UI

## 状态管理

### State

### Props

<!--more-->

## 路由

- 主要使用的是`React Router`，包括`react-router`，`react-router-dom`，`react-router-native`

```react
import { Switch, Route } from 'react-router-dom'

const Main = () => (
	<main>
    <Switch>
    	<Route path='/roster' component={Home}/>
    	<Route path='/schedule' component={Post}/>
      <Route path='/about', render={() => <About something={this.something}>}/>	<!--通过这种方式绑定数据或者方法给子路由-->
  	</Switch>
  </main>
)

this.props.location.pathname;	// 获取当前的url路径
```

## 组件

### 组件属性

- 动态添加元素样式`style`

  ```react
  <div style={{display: this.state.show ? "block" : "none"}}>动态样式</div>
  ```

- 动态添加类`class`

  ```shell
  <div className={this.state.show ? "show-class" : "hide-class"}>动态类</div>
  ```

### 常用组件

#### Prompt

- 在路由即将切换前弹出确认框(离开前确认)
- 需要注意的是，如果用户点击了取消，那么会组织路由的切换，但是用户的点击事件如果有监听，依然会触发点击事件的
- 最好在`message`里面判断是否需要展示`Prompt`，不要在`when`里面，因为在`when`里面，每次重新`render`都会执行，但是`message`里面只是在用户真的打算跳转的时候才会执行

```react
<Prompt 
  when={true}
  message={(params) => params.pathname == '/当前路径' ? true : "确认离开" } />	// 当返回文字的时候会弹出确认，而返回true的时候则不会弹出
```

## 条件渲染

如果实在`JSX`外部的`js`部分代码，那么直接使用`js`自己的`if`或者其他条件判断即可完成。在`JSX`内部的话一般则是使用逻辑与`&&`或者三目运算符完成。例如

```react
render() {
  return (
  	<div>
    	{this.state.posts.length > 0 && 
      	<p>There is some posts</p>
      }
    </div>
    <div>
      <p>There is {this.state.posts !== undefined ? this.state.posts.length : 0} posts.</p>
    </div>
  )
}
```

## 必备三方组件

### React-Redux

- 从后端的角度看，就是一个维护全局变量的东西

- `Action`定义了要发生什么，并且携带着数据，`reducer`用来定义发生该事情后需要做什么，`selector`可以理解是从`state`获取数据的API。
- `Redux`可以通过`connect`方法，将`store`的`dispatch`方法保存到组件的`props`中
- `state`与`props`的对应通常需要使用`mapStateToProps`这个函数进行定义。它默认会订阅`Store`，每当`state`更新的时候，就会自动执行，重新计算UI组件的参数
- 下面的方法在跟组件外面包了一层`Provider`，这样所有的子组件默认都能拿到`store`了

```rearct
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import rerducer from './reducers'
import App from './App'

const store = createStore(
  reducer
);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
```
- 可以用`connect`将组件与`store`进行连接，它可以接收四个参数: 
  - `mapStateToProps(state, ownProps) : stateProps`，第一个参数就是Redus的`store`，这个方法的返回值就会作为组件的`props`

### React-Saga

- 从后端的角度看，就是在启动应用的时候，再启动一些单独的线程，这些线程可以异步去做些更改变量或者监听的事情，类似于钩子。

- 可以在这里对异步操作进行集中处理。

- `Effect`的几种方法:

  ```react
  import {take,call,put,select,fork,takeEvery,takeLatest} from 'redux-saga/effects'
  // take: 用来监听action，返回监听到的action对象，例如如果有一个type=login的action，那么在执行dispatch(loginAction)之后，就可以这样获取对象
  const action = yield take('login')
  
  // call: 调用指定函数
  yield call(myfunc, param1, param2);
  
  // put: 和dispatch类似，用于发送action，dispatch in saga
  yidle put({type: 'login'})
  
  // select: 和getState类似，用于获取store中的state
  const state = yield select()
  
  // fork
  
  // takeEvery/takeLatest: 用于监听
  ```

- 简单的例子: 

```react
// 在编写saga的文件里面一般这样写钩子函数
export function * mySaga() {
  console.log("Hello Saga");
}

// 在main.js中，这样引入saga中间件
import createSagaMiddleware from 'redux-saga';
import {helloSaga} from './saga.js';
const sageMiddleware = createSagaMiddleware();
const store = createStore(rerducer, aplyMiddleware(sagaMiddleware));
sagaMiddleware.run(helloSaga);
```

### Styled-Components

- 目的是将`React`组件包装成`Styled`组件

```react
import { Card } from 'antd';

const StyledComponent = styled(Card)`		// 可以接收一个React-Componetn例如Card，也可以接收一个tagName例如div
	div {
		color: red;
	}
	.abc {
		color: blue;
		width: ${props => props.width}	// 变量传递
	}
`
// 在render里面就可以直接使用该组件了
<StyledComponent width={"12px"}></StyledComponent>
```



## 事件

### 支持事件列表

```react
// 焦点事件
onBlur
onFocus
```

## TroubleShooting

- **React 表达式必须有一个父元素**: 常出现在`JSX`的渲染的内嵌语句中返回了错误格式的结果:

  ```react
  render() {
    return (
    {
    	[							// 需要返回的应该是数组而不是混搭
      	<p>abc</p>,
      	<p>def</p>,
      ] 
    })
  }
  ```


##### 扩展阅读

- [在React中使用Redux](https://juejin.im/post/5b755537e51d45661d27cdc3)