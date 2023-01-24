---
title: "React 开发手册"
date: 2019-09-10 14:40:00
updated: 2023-01-11 21:38:00
categories: Javascript
---

## 基本概念

- `React`是一个用于构建用户界面的Javascript库，是`DOM`的一个抽象层
- `React`主要用于构建UI

## 状态管理

### Props

<!--more-->

- props.children，类似于`vue`种的槽，只要组件内部有元素，那么它就是props.children，内部可以直接拿来用，例如:

  ```react
  <MyComponent>
  	<div>test</div>
  </MyComponent>
  
  function MyComponent(props) {
    return (
    	<div>
      	{props.children}
      </div>
    )
  } 
  ```

### Hooks

#### useEffect

- 副作用：数据获取、设置订阅、手动更改DOM，我们可以在函数组件中像类组件那样获取改变state

- 可以把`useEffect Hook`看作`componentDidMount、componentDidUpdate、componentWillUnmount`这三个函数的组合，组件渲染完成后执行某些操作

- 官方建议一个组件中不同的功能最好分开写`useEffect`

- 默认`useEffect`每次重新渲染都会执行一次，可以传入第二个参数来控制渲染的次数，**注意第二个参数最好不要穿入肯定不会变的复杂对象，例如函数等，否则肯可能造成每次都重新渲染**:

  - 不传第二个参数，每次render都会执行
  - 传入空数组，只会执行一次
  - 传入一个值，当那个值改变的时候就执行
  - 传入多个值，当其中某个值改变的时候就执行

  ```javascript
  useEffect(() => {}, [props.user])	// 这样当props.user改变的时候能够重新执行一次函数
  ```

- 副作用清除机制，在useEffect中返回一个函数，能够有效防止内存溢出等异常:

  ```javascript
  useEffect(() => {
    Client.subscribe(args, callBackFunc());	// 如果我们需要在渲染完成后进行订阅
    return function cleanup () {	// 如果需要在组件卸载的时候退出订阅就能这样做
      Client.unsubscribe();
    }
  })
  
  // interval或者timeout都是需要清理的，否则每次页面有个状态变更重新渲染的时候就会重新新建，造成内存泄漏
  useEffect(() => {
    const interval = setInterval(() => {});
    return () => clearInterval(interval);	
  })
  ```

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

#### useMemo/useCallback

- 两个比较类似，都是性能优化的手段，类似于类组件中的`shouldComponentUpdate`，在子组件中可以判断该组件的props和state是否有变化，避免服组件重新render的时候每次都重新渲染子组件

- useMemo返回一个值，避免在每次渲染时候都重新进行计算

  ```jsx
  const data = {简单的计算过程}	// 注意如果是简单的数据转换可以不用useEffect或者useMemo，直接这样即可
  const data = useMemo(() => {复杂的计算过程}, [originalData]) // 这样除非originalData变了，否则父组件的改变不会引起子组件的变化
  
  // 如果一个useEffect依赖于某个需要计算的值，那么这个值最好被useMemo包裹
  useEffect(() => {doSomething()}, [data]) // 这里应该监听data而不是originalData
  ```

- useCallback返回一个函数，当把它返回的这个函数作为子组件使用时，可以避免每次父组件更新时都重新渲染子组件

  ```jsx
  const myButton = useCallback(<Button>{label}</Button>, [label])                       
  ```

### Ref

```javascript
const ref = useRef(null)

const scroll = (offset) => {
  ref.current.scrollLeft += offset;
}

return (<div ref={ref} onClick={() => scroll(20)}></div>)
```

### Context

- 和`Redux`类似，也有一个`Provider`在最外面
- Context更适合存储全局的一些属性，例如用户选择的语言、地区偏好、UI主题等
- 还是觉得`Redux`方便好理解一点，而且功能强大一点，`Redux`才是做了一个完整的状态管理功能，`context`主要就是存储一个全局的数据，当然使用了context数据的的UI组件在context数据变化时也会刷新，是整个UI树的更新，用户体验和性能都会有问题
- 使用Context不用从最父级的组件一层一层往下传递了

```javascript
const WebContext: Context<boolean> = createContext<boolean>(true);
const ThemeContext = React.createContext('light');

<WebContext.Provider value={isWeb}>
  <ThemeContext.Provider value="dark">
  	<ReduxProvider store={store}></ReduxProvider>
	</ThemeContext.Provider>
</WebContext.Provider>

// 其他组件
class ThemedButton extends React.Component {
  // 指定 contextType 读取当前的 theme context。
  // React 会往上找到最近的 theme Provider，然后使用它的值。
  // 在这个例子中，当前的 theme 值为 “dark”。
  static contextType = ThemeContext;
  render() {
    return <Button theme={this.context} />;
  }
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

### 组件定义

### 函数组件

- 函数组件中能使用`useState`

```java
// typescript中需要这样定义，FC是TypeScript使用的一个范性，意思是FunctionComponent
// typescript中需要定义入参类型，可以这样定义
interface CurrentProps {
	field1: string;
  field2: number;
}

const MyComponent: FC<CurrentProps> = (props) => {
  
}
```

### 组件属性

- 动态添加元素样式`style`

  ```react
  <div style={{display: this.state.show ? "block" : "none"}}>动态样式</div>
  ```

- 动态添加类/条件渲染类`class`

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

#### 父组件传递props给子组件，可以直接在父组件修改，会更新给子组件的

#### 父组件将方法作为props传递给子组件

```javascript
// 父组件
[MyState, SetMyState] = useState(false);
<Child setMyState={SetMyState}>

// 子组件
props.setMyState(true);
```

## JSX语法

### 基本语法

```jsx
<div tabIndex="0">ttt</div>	// 可以使用双引号来直接指定属性值
<img src={user.avatarUrl}</img>	// 也可以使用大括号来指定变量属性值
<input value={user.name} />	// 设置input的默认值

// 传递变量到scss中
const myStyle = `--bg-url: ${myUrl}`
<div style={myStyle}></div>	// 可以通过这种方式将变量
  
{/ 注释 /}
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

- 如果是在`JSX`外部的`js`部分代码，那么直接使用`js`自己的`if`或者其他条件判断即可完成。在`JSX`内部的话一般则是使用逻辑与`&&`或者三目运算符完成。
- **如果条件渲染的结果全是字符串0，那么应该是条件没有转换为布尔值，可以使用双感叹号来转换，例如!!this.posts**
- 如果需要用条件判断是否有子组件可以使用`React.isValidElement(children)`来判断

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

### map循环

```jsx
<Nav>
  {
  	props.menus?.map((menu, i) => {
  		return (
        menu?.children?.length > 0
        ? <NavDropdown title={menu.title} key={i}>
          {
            menu.children?.map((subMenu, subIndex) => {
              <NavDropdown.Item href={subMenu.url} key={`${subIndex}-${i}`}>{subMenu.title}</NavDropdown.Item>
            })
          }
          </NavDropdown>
        : <NavLink href={menu.url} title={menu.title} key={i}/>
    	)
		})
	}
  {// 对于字典类型，只能这样做了
    Object.keys(props.menus).map(key, index) => {
      value = props.menus[key]
    }
  }
</Nav>
```

## 推荐三方组件

### prop-types

- 类似于typescript，能够有效限制与定义组件中的prop参数类型
- 不过建议在pages页面(非component)中禁用eslint的`react/prop-types: 'off'`功能，因为页面的props可能太多，也和component中的有重复

```javascript
import PropTypes from 'prop-types';

MyComponent.propTypes = {
  optionalArray: PropTypes.array,
  optionalBool: PropTypes.bool.isRequired,	// 布尔值，isRequired表示必填
  optionalFunc: PropTypes.func,
  optionalObject: PropTypes.object,
  optionalSymbol: PropTypes.symbol,
  requiredAny: PropTypes.any.isRequired,	// 任意类型
  optionalEnum: PropTypes.oneOf(['News', 'Photos']),	// 枚举类型
  optionalUnion: PropTypes.oneOfType([	// 可以是多个类型
    PropTypes.string,	// 字符串类型
    PropTypes.number,	// 数字类型
    PropTypes.instanceOf(Message)
  ]),
  optionalArrayOf: PropTypes.arrayOf(PropTypes.number), // 指定数组元素
  optionalObjectWithShape: PropTypes.shape({	// 定义对象的内部字段
    color: PropTypes.string,
    fontSize: PropTypes.number
  }),
   optionalObjectWithStrictShape: PropTypes.exact({	// 只允许特定的值
    name: PropTypes.string,
    quantity: PropTypes.number
  }),
}
```

### [react-animated-number](https://github.com/ameyms/react-animated-number)

- 数字变化动态效果
- 虽然这个库很久没维护了，但是对比其他的库，这个库是我找到的唯一能满足我要求的

### [React Hook Form](https://www.npmjs.com/package/react-hook-form)

- 表单hook

```jsx
const { register, trigger, formState: { errors } } = useForm();
<input {...register("firstName", { required: true })} />	// 注册字段

<button onClick={() => handleSubmit(onSubmit)()}	// 手动触发onSubmit检查

<input name="singleErrorInput" />
<ErrorMessage errors={errors} name="singleErrorInput" />	// 错误提示文本组件，需要先安装@hookform/error-message
```

### React-Redux

- 从后端的角度看，就是一个维护全局变量的东西(也有同一个页面不同组件使用相同的东西，比如当前用户的用户名用户头像啥的)
- 个人现在都用mobx了，好配置得多
- [Redux with typescript](https://redux-toolkit.js.org/usage/usage-with-typescript): Typescript里面如何定义，这里还有个[example project](https://github.com/leandroercoli/InstagramClone/tree/master)
- `Action`定义了要发生什么，并且携带着数据(可以在`action`里面调用API，将结果进行`dispatch`，类似于vuex中的`action`将结果进行`mutation`)，`reducer`用来定义发生该事情后需要做什么(类似于vuex中的mutation)，`selector`可以理解是从`state`获取数据的API。
- `Redux`可以通过`connect`方法，将`store`的`dispatch`方法保存到组件的`props`中
- `state`与`props`的对应通常需要使用`mapStateToProps`这个函数进行定义。它默认会订阅`Store`，每当`state`更新的时候，就会自动执行，重新计算UI组件的参数
- 下面的方法在根组件外面包了一层`Provider`，这样所有的子组件默认都能拿到`store`了
- 异步操作需要结合[Thunk](https://cn.redux.js.org/tutorials/essentials/part-5-async-logic/)，太麻烦了
- 注意如果使用useselect等在第一次没有值，页面第二次渲染才有值，可能是因为没有将这些状态持久化造成的

```react
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import rerducer from './reducers'
import App from './App'

const store = createStore(
  reducer
);

store.subscribe(subscribe)	// 设置监听函数，一旦State发生变化，就自动执行这个函数

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);

// actions，和vuex中的actions类似
export function getUser(token: string) {
  return async (dispatch) => {
    const { data } = await fetcher.post(...)
    // dispatch的调用方法和vuex中的mutation类似
    dispatch({
      type: 'SET_USER',
      payload: data.user,
    });
  };
}

// reducer类似于vuex中的mutation
const userStateValue = {email: '', id: ''}
const initialState = (typeof localStorage === 'undefined' || !window.localStorage.getItem('user'))
  ? userStateValue
  : JSON.parse(window.localStorage.getItem('user') || '{}');

const reducer: Reducer<AppState, AppActionTypes> = (
  state = initialState,
  action
) => {
  switch (action.type) {
    case 'SET_USER':
      const payload = action.payload
      newState = {
        id: payload?.id || state.id,
        firstName: payload?.firstName || state.firstName,
        lastName: payload?.lastName || state.lastName,
        username: payload?.username || state.username,
        email: payload?.email || state.email,
        accessToken: payload?.accessToken || state.accessToken,
      }
      if (typeof localStorage !== 'undefined') {
        window.localStorage.setItem('user', JSON.stringify(newState))
      }
      return newState
    default:
      return state;
  }
};


const store = useSelector<State, AppState>((state) => state.app);
const isAuth = !!store.token && !!store.user && !!store.user.name;
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

将`redux-actions`和`react-saga`配合使用可以简化大量的重复代码。在之前我们要创建一个`action`需要线这样子定义:

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

### [react-timeago](https://github.com/nmn/react-timeago)

- 能够直接展示`1 hour ago / 2 days ago`等信息，不用去找啥时间组件了

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
// 监听全局scroll事件
useEffect(() => {
  window.addEventListener('scroll', onScroll)
})

onInput((e) => setValue(e.target.value))

// 焦点事件
onBlur
onFocus
onKeyPress // 当键盘按下，function(e) => {e.charCode === 13}， charCode等与13的时候表示回车
```

## TroubleShooting

- **引入json格式的文件**: 可以直接`import data from 'path/to/my.json'`

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

- **Warning: Function components cannot be given refs. Attempts to access this ref will fail. Did you mean to use React.forwardRef()**: 可以尝试将函数组件修改为这样:

  ```javascript
  export const MyComponent = React.forwardRef(({...props}: InputProps, ref) => {
   ...
  });
  ```

## 扩展阅读

- [在React中使用Redux](https://juejin.im/post/5b755537e51d45661d27cdc3)
- [React Icons库](https://react-icons.github.io/react-icons/)
- [在线视频播放库 react-player](https://github.com/cookpete/react-player)
- [Victory](https://haofly.net/victory): 比较原生的charts库，甚至可以用于`React-Native`
- [react-grid-layout](https://www.npmjs.com/package/react-grid-layout): 可拖动的grid布局