---
title: "React 开发手册"
date: 2019-09-10 14:40:00
updated: 2021-05-27 08:48:00
categories: Javascript
---

## 基本概念

- `React`是一个用于构建用户界面的Javascript库，是`DOM`的一个抽象层
- `React`主要用于构建UI

## 状态管理

### State

### Props

<!--more-->

### Effect Hook

- 副作用：数据获取、设置订阅、手动更改DOM
- 可以把`useEffect Hook`看作`componentDidMount、componentDidUpdate、componentWillUnmount`这三个函数的组合
- 默认`useEffect`在第一次渲染之后和每次更新之后都会执行
- 在函数组件中执行副作用操作，可以直接使用`state`，不用编写class

```react
import React, { useState, useEffect } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    // Update the document title using the browser API
    document.title = `You clicked ${count} times`;
    
    // 在useEffect中可以这样使用异步方法，如果直接useEffect(async()=>{})的话会报错：useEffect function must return a cleanup function or nothing, Promises ... are not supported, but you can call an async function inside an effect.
    async function fetchAPI() {}
    fetchAPI();
  });

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

## 路由

- 主要使用的是`React Router`，包括`react-router`，`react-router-dom`，`react-router-native`

  ```javascript
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

- 需要注意的是，如果是`Link`链接的路由和当前路由是一样的，那么页面不会发生跳转，什么都不会做，这时候如果是弹出菜单，弹出菜单也不会自动关闭，所以这种情况可以单独处理一下，用`a`标签代替一下，然后使用window.location.href来进行跳转吧，例如:

  ```javascript
  function jumpToMenu(url, e) {
  	e.preventDefault()
    window.location.href = url
  }
  
  <a href={url} onClick={(e) => jumpToMenu(url, e)}>{text}</a>	// 在onClick里面传递参数
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
  <div className={style.style1 + ' ' + style.style2}>多个类</div>
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

### 父子组件资源共享

#### 父组件将方法作为props传递给子组件

```javascript
// 父组件
[MyState, SetMyState] = useEffect(false);
<Child setMyState={SetMyState}>

// 子组件
props.setMyState(true);
```

## JSX语法

### 基本语法

```jsx
<div tabIndex="0">ttt</div>	// 可以使用双引号来直接指定属性值
<img src={user.avatarUrl}</img>	// 也可以使用大括号来指定变量属性值
```

### 代码片段fragments

- 为一个组件添加元素，并且不会在DOM中增加额外的节点，常规的做法是在外层包一个`div`，这样就会多一层DOM元素，为了减少元素数量，可以这样做

```jsx
return (
  <React.Fragment>
    <ChildA />
    <ChildB />
    <ChildC />
  </React.Fragment>
);

// 简写语法<>
return (
<>
  <td>mycontent</td>
  <td>mycontent</td>
</>
)
```

### 条件渲染

如果是在`JSX`外部的`js`部分代码，那么直接使用`js`自己的`if`或者其他条件判断即可完成。在`JSX`内部的话一般则是使用逻辑与`&&`或者三目运算符完成。例如

```react
render() {
  return (
  	<div>
    	{this.state.posts.length > 0 && // 注意两边是大括号
      	<p>There is some posts</p>
      }
      <p>
      	{length > 0 && '还可以这样直接写文字'}
      </p>
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

### Redux-Saga

- 从后端的角度看，就是在启动应用的时候，再启动一些单独的线程，这些线程可以异步去做些更改变量或者监听的事情，类似于钩子。

- 可以在这里对异步操作进行集中处理。

- `Effect`的几种方法:

  ```react
  import {take,call,put,select,fork,takeEvery,takeLatest} from 'redux-saga/effects'
  // take: 用来监听action，返回监听到的action对象，例如如果有一个type=login的action，那么在执行dispatch(loginAction)之后，就可以这样获取对象
  const action = yield take('login')
  
  // call: 调用指定函数
  yield call(myfunc, param1, param2);
  
  // put: 触发dispatch，用于发送action，dispatch in saga
  yield put({type: 'login'})
  
  // select: 和getState类似，用于获取store中的state
  const state = yield select()
  
  // fork
  
  // takeEvery/takeLatest: 用于监听
  ```

- 简单的例子: 

  ```javascript
  // 在编写saga的文件里面一般这样写钩子函数
  export function * mySaga(action) {	// 这里的参数action，是包含了payload,state的对象
    console.log("Hello Saga");
  }
  
  // 在main.js中，这样引入saga中间件
  import createSagaMiddleware from 'redux-saga';
  import {helloSaga} from './saga.js';
  const sageMiddleware = createSagaMiddleware();
  const store = createStore(rerducer, aplyMiddleware(sagaMiddleware));
  sagaMiddleware.run(helloSaga);
  ```

- `saga`中使用`fetch`

  ```shell
  function* onGetSuccess(state) {
  	const res = yield fetch("https://example.com").then(response => response.json());
  }
  ```

### Redux-actions

将`redux-actions`和`react-sage`配合使用可以简化大量的重复代码。在之前我们要创建一个`action`需要线这样子定义:

```javascript
// 在使用redux-actions之前，需要这样创建一个action并使用
export const saveResult = (resultList) => {
  console.log(resultList);
  return {
    type: "SAVE_RESULT",
    resultList
  }
};

// 现在只需要这样定义多个动作
export const actionCreators = createActions({
  ["SAVE_RESULT"]: resultList=>resultList,
});

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

### [SWR](https://github.com/vercel/swr)

- `state-while-revalidate`的缩写，是`HTTP RFC 5861`中描述的一种`Cache-Control`扩展
- `React`的`Hook`组件，用于缓存从远端获取的数据
- 常用语多次请求相同URL获取数据，或者更新数据后，先返回缓存的响应，与此同时去后台发送新的请求，以提高响应速度，减少等待时间
- 请求的结果根据标识`key`放在`redux`里缓存，取数据的时候直接从`redux`里面取
- `SWR`并不是一个请求库，只是一种管理数据的方式

```react
import useSWR from 'swr';

// 请求参数
// key: 表示请求的标识，可以是任意字符串，但是我们一般会设置为请求的url，这样方便识别。如果key传入null就代表不请求数据，什么都不做
// fetcher: 返回请求数据的异步方法，一般会是一个axios对象
// options: 其它配置项
// 返回值
// data: 相应数据
// error: 错误
// isValidating: 是否正在请求或重新验证数据
// mutate(data?, shouldRevalidate): 用于直接修改缓存数据
const { data, error, isValidating, mutate } = useSWR(key, fetcher, options);


const fetcher = Axios.create({
  baseURL: 'https://haofly.net/api/',
  responseType: "json",
});

const { data: user } = useSWR('/user', fetcher);	// SWR会将key作为参数传递给fetcher
const { data: users, mutate } = useSWR(['/users', userIds], fetcher); 	// 可以传递多个参数，swr会将多个参数组合为一个key

import useSWR, { mutate } from 'swr';
mutate('/users');	// 手动再次获取数据，会让所有拥有相同key的swr主动去获取一次数据，并更新缓存

mutate();	// 或者直接用useSWR返回的mutate，可以省略key

mutate('/users', {...users, new: true});	// 触发更新操作，但是在更新操作完成前先直接用第二个参数来代替缓存，相当于先直接修改缓存
mutate({...users, new: true}); // 使用返回的mutate，省略key

const { newDate } = await axios.patch('/users');	// 更新users操作，直接返回新的数据
mutate(updated, false);	// 如果更新操作直接返回更新后的资源，那么mutate可以直接使用它，然而最后一个参数设置为false，这样就可以不用去请求获取新的资源了，表示无需重新验证资源
```

## 事件

### 支持事件列表

```react
// 焦点事件
onBlur
onFocus
```

## TroubleShooting

- **Expected server HTML to contain a matching <p> in <span>**: 注意P标签内部不能嵌套其他p标签

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

## 扩展阅读

- [在React中使用Redux](https://juejin.im/post/5b755537e51d45661d27cdc3)
- [React Icons库](https://react-icons.github.io/react-icons/)
- [在线视频播放库 react-player](https://github.com/cookpete/react-player)