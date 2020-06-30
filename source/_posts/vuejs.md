---
title: "Vue.js教程"
date: 2020-06-12 22:09:39
updated: 2020-06-28 14:56:00
categories: js
---

## 模板语法

- 模板中如果遇到这种类型的三目运算符`a ? a : b`，最好用`{a || b}`来代替

```javascript
// v-bind
<a v-bind:href="url">...</a>
<a v-bind:href="`/api/${item.id}`">...</a> // 属性绑定的时候拼接字符串，也可以用['/api/' + item.id]的方式
<a :href="url">...</a>	// 缩写
<a title="test"></a>// 如果仅想传入一个字符串作为props给组件，那么不用加冒号
<a :hidden="shouldHidden==='letshidden'">	// 在v-bind中直接用表达式
<img v-bind:src="pic" v-for="pic in pics" />

// v-on
<a v-on:click="doSomething">...</a>
<a @click="doSomething">...</a>

// v-html，将内容不转义直接展示为html内容，如果是用户输入的内容，这里一定要防止XSS攻击，最简单的方法就是使用https://github.com/leizongmin/js-xss在外面处理一下
<div v-html="XSS(data)"></div>
<div v-html="$options.filter.myfilter(data)"></div>	// v-html中使用过滤器

// v-if, v-else, v-else-if, 条件判断
```

<!--more-->

### slot插槽

- 感觉就是一个简化了的模板，模板有特定的语法传入变量，而这里只是留了一个位置以供插入任何内容

- 说高大上点就是实现了一套内容分发的API，将`<slot></slot>`元素作为承载分发内容的出口。

- 如果没有插槽，那么在组件标签内的内容是不起作用的，例如

  ```javascript
  // 我们定义这样一个组件
  Vue.component('mycomponent', {
  template:`<div>原始内容</div>`
  })
  
  // 然后打算在外部这样使用它
  <mycomponent>其它内容</mycomponent>
  
  // 如果没有插槽，则会渲染为<div>原始内容</div>，使用者的内容没有起到任何作用，这时候如果使用插槽，可以这样定义
  Vue.component('mycomponent', {
  template:`<div>原始内容<slot></slot></div>`
  })
  
  // 同样的时候方式就会输出<div>原始内容其它内容</div>了
  ```

#### 具名插槽

给插槽指定一个名字，常用于一个组件包含多个插槽的情况，例如:

```javascript
// 这样定义组件
Vue.component('mycomponent', {
  template: `
<div>内容1<slot name="插槽1"></slot>内容2<slot name="插槽2"></slot></div>`
})

// 然后可以这样传入内容
<mycomponent>
	<div slot="插槽1">xxx</div>
  <template slot="插槽2">xxx</template>
</mycomponent>
```

#### 作用域插槽

指组件上定义的属性，可以在组件元素内使用。例如

```javascript
Vue.component('mycomponent', {
  template: `<div><slot field1="属性"></slot></div>`
})

<mycomponent>
	<div slot-scope="abc">
  	{{abc}} <!--会发现输出就是{"field1":"属性"}--> 
  </div>  
</mycomponent>
```

## 动态数据绑定

```javascript
// 动态绑定class
<div :class={
  'class_name': isOk ? true : false
}></div>
```

## 常用事件

```javascript
// 鼠标按下
<div id="slider" @mousedown = drag($event)></div>

// 特定按键按下事件
<div @keyup.enter.native="func"></div> // 按下回车触发
<div v-on:keyup.enter="search" v-model="keyword"></div>	// 按下回车触发，这里不能直接传值到函数里面去，所以用v-model进行数据绑定
<div @keyup.188.native="func"></div> // 按下逗号触发
<div @mouseup.native="func"></div> // 鼠标按下
<div @mouseover.native="func"></div> // 鼠标移动到元素上
<div @mouseout.native="func"></div> // 鼠标移开
```

## Vuex

- 专为`Vue.js`应用程序开发的状态管理模式，采用集中式存储管理应用的所有组件的状态
- 解决了多个试图依赖于同一状态，来自不同视图的行为需要变更同一个状态的情况，有了`vuex`则就集中式管理了，否则可能需要再每次切换页面将所有的状态都带上才行
- 与全局变量不同，它的状态存储是响应式的。当Vue组件从store中读取状态的时候，若store中的状态发生变化，那么相应的组件也会相应地更新
- 不能直接改变`store`中的状态，改变的唯一途径就是显式地提交(commit) mutation
- 需要遵守的响应规则:
  - 最好提前在store中初始化好所有所需属性
  - 当需要在对象上添加新属性时，应该选择下面的方法之一
    - 使用`Vue.set(obj, 'newProp', 12)`
    - 以新对象替换老对象，例如`state.obj = { ...state.obj, newProp: 123}`

### Getter

- 如果要在页面中派生出一个状态通常会用到`computed`，但是如果每个页面都需要同一个状态，就可以在`store`中定义`getter`(可以认为是针对store的计算属性computed)
- 和`computed`一样，`getter`的返回值会根据它的依赖被缓存起来，且只有当它的依赖值发生了改变才会被重新计算

```javascript
// 定义方法一: 使用Store直接定义
const store = new Vuex.Store({
  state: {
    todos: [
      { id: 1, text: '...', done: true },
      { id: 2, text: '...', done: false }
    ]
  },
  getters: {
    doneTodos: (state, getters) => {
      return state.todos.filter(todo => todo.done)
    }
  }
})
// 定义方法二: vue框架中可以直接这样定义
// 建立一个getters.js文件
export const foo = state => state.foo;
// 然后在index.js中这样使用
import * as getters from './getters';
Vue.use(Vuex);
export default new Vues.Store({
  state: {foo:'bar'},
  getters
});

// 在组件中可以这样使用它
computed: {
  doneTodosCount () {
    return this.$store.getters.doneTodosCount
  }
}

// 可以定义带参数的getter
getters: {
  // ...
  getTodoById: (state) => (id) => {
    return state.todos.find(todo => todo.id === id)
  }
}
store.getters.getTodoById(2) // -> { id: 2, text: '...', done: false }
```

#### mapGetters

- 可以将`store`中的`getter`映射为局部计算属性，例如

```javascript
import { mapGetters } from 'vuex'

export default {
  // ...
  computed: {
  // 使用对象展开运算符将 getter 混入 computed 对象中，这样可以直接当成当前组件的computed了
    ...mapGetters([
      'doneTodosCount',
      'anotherGetter',
      // ...
    ])
  }
}
```

### Mutation

- 提交mutation是改变store状态的唯一方法

- 每个`mutation`都有一个字符串的事件类型(type)和一个回调函数(handler)。这个回调函数就是实际进行状态更改的地方，并且它会接受state作为第一个参数

- `Mutation`必须是同步函数

- 最好使用常量来替代``Mutation`事件类型，可以使`linter`之类的工具发挥作用。例如

  ```javascript
  export const SOME_MUTATION = 'SOME_MUTATION';
  
  const store = new Vuex.Store({
    state: { ... },
    mutations: {
      // 我们可以使用 ES2015 风格的计算属性命名功能来使用一个常量作为函数名
      [SOME_MUTATION] (state) {
        // mutate state
      }
    }
  })
  ```

可以这样定义`mutation`:

```javascript
const store = new Vuex.Store({
  state: {
    count: 1
  },
  mutations: {
    increment (state) {
      // 变更状态
      state.count++
    }
    increment2 (state, payload) {
  		// 可以在commit的时候传入额外的参数，即mutation的载荷payload
  		state.count += n
		}
  }
})

// 但是不能直接使用，只能通过commit去调用，例如
store.commit('increment')
store.commit('increment2', 10);	// 带额外参数的commit
store.commit({			// 对象风格的提交方式(这种方式会把整个对象作为一个payload)
  type: 'increment', 
  amount: 10
})
this.$store.commit('xxx');	// 在组件中提交Mutation
```

### Action

- 类似于`mutation`，不过它提交的是``mutation`，而不是直接变更状态，并且可以包含任意异步操作
- 如果有异步的操作就交给`Action`，在它内部`commit(mutation)`

定义和使用:

```javascript
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment (state) {
      state.count++
    }
  },
  actions: {
    increment (context) {	// context是与store实例具有相同方法和属性的对象，可以在它上面使用store的state、getters、commit等方法，不过它并不是store实例对象本身
      context.commit('increment')
    },
    increment1 ({ commit }) {	// 使用“参数结构”来简化代码
      setTimeout(() => {
        commit('increment')
      }, 1000)
    },
    checkout ({ commit, state }, products) {	// 官方的购物车例子
    	const savedCartItems = [...state.cart.added]	// 把当前购物车的物品备份起来
    	commit(types.CHECKOUT_REQUEST) // 发出结账请求，然后乐观地清空购物车
    	shop.buyProducts(	// 购物 API 接受一个成功回调和一个失败回调
      	products,
      	() => commit(types.CHECKOUT_SUCCESS),// 成功操作
      	() => commit(types.CHECKOUT_FAILURE, savedCartItems)// 失败操作
    ),
    actionA ({ commit }) {	// 获取Action的执行结果
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          commit('someMutation')
          resolve()
        }, 1000)
      })
  	},
    actionB ({ dispatch, commit }) {	// action的嵌套
      return dispatch('actionA').then(() => {
        commit('someOtherMutation')
      })
  	}，
    async actionA ({ commit }) {
    	commit('gotData', await getData())
  	},
  	async actionB ({ dispatch, commit }) {	// async的嵌套组合方式
    	await dispatch('actionA') // 等待 actionA 完成
    	commit('gotOtherData', await getOtherData())
  	}
  }
})

// 调用/分发Action
store.dispatch('increment')
this.$store.dispatch('xxx')	// 在组件中分发
store.dispatch('actionA').then(() => {});	// 根据Action执行结果来回调
```

### Module

- 为了防止单一的状态树对象过大，需要将`store`分割成模块`module`，每个模块拥有自己的`state/mutation/actin/getter`
- 当然模块内部的mutattion和getter接收的第一个参数是模块的局部状态对象。对于action，局部状态也是`context.state`，根结点状态则为`context.rootState`。作为模块内部的getter，根结点状态会作为第三个参数暴露出来，例如这样定义一个`getter`: `sumWithRootCount(state, getters, rootState)`

可以这样定义`module`:

```javascript
const moduleA = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... },
  getters: { ... }
}

const moduleB = {
  state: () => ({ ... }),
  mutations: { ... },
  actions: { ... }
}

const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
})
store.registerModule('myModule', {});	// 模块动态注册

store.state.a // -> moduleA 的状态
store.state.b // -> moduleB 的状态
```

## 存储

`localStorage`(其实是H5的特性)，主要用来作为本地存储使用，能够解决cookie存储空间不足的问题(每条cookie最大为4k)，`localStorage`默认5M大小。

- 如果要和cookie对比，一般数据量大的会选择使用`localStorage`，因为cookie每次和服务器交互都会带上，只适合小量的数据，例如用户token等信息。
- 仅在客户端保存，不参与和服务器的通信
- 无法再隐私模式下使用
- 生命周期是永久的，只要用户或者程序不主动清除，消息就永远存在，即使重启浏览器都在
- `sessionStorage`，刷新页面数据依然存在，但是关闭页面数据就不存在了

```javascript
localStorage.setItem('accessToken', 'Bearer xxxxxxxx')
localStorage.getItem('accessToken')
localStorage.removeItem('accessToken')

// 如果要读写数组就只能用JSON转一下
localStorage.setItem("mylist", JSON.stringify(list));
JSON.parse(localStorage.getItem("mylist"));

// 查看localStorage中各个值所占用的内存的大小
var _lsTotal=0,_xLen,_x;for(_x in localStorage){ if(!localStorage.hasOwnProperty(_x)){continue;} _xLen= ((localStorage[_x].length + _x.length)* 2);_lsTotal+=_xLen; console.log(_x.substr(0,50)+" = "+ (_xLen/1024).toFixed(2)+" KB")};console.log("Total = " + (_lsTotal / 1024).toFixed(2) + " KB");
```

## 网络交互组件axios

(Vue官方已经不推荐vue-resource，而是推荐axios了)用法其实与Ajax类似，例如:

```javascript
axios({
    url: 'https://haofly.net',
    method: 'post',
    headers: {},
    data: {}
}).then(function (response) {
    console.log(response.data);
});
```

##### TroubleShooting

- **更改数据页面不渲染**，可能有如下原因
  - 在给data赋值后只是简单地添加新的属性，没有用this.$set等方法，导致没有新添加的属性没有实现双向绑定，从而导致重新渲染失败。常见现象也有改变一个值，第一次改变页面渲染成功，之后再改变页面不会更新等
- 

相关链接

- [Vuex文档](https://vuex.vuejs.org/zh/guide/)
- 仿造猫眼电影客户端实例: https://github.com/zhixuanziben/gouyan-movie-vue   
- Objc中国的全平台客户端: https://github.com/halfrost/vue-objccn
- 仿闲鱼：https://github.com/Sukura7/vue-ali-xianyu
- 仿hackernews: https://github.com/vuejs/vue-hackernews-2.0
- Flask与Vuejs创建一个简单的单页应用https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs
- [Vue表单可视化生成器](https://github.com/dream2023/vue-ele-form-generator)
- [滚动加载插件vue-infinite-loading](https://peachscript.github.io/vue-infinite-loading/guide/)
- [Bootstrap Vue](https://bootstrap-vue.org/docs)
- [Echarts Vue](https://github.com/ecomfe/vue-echarts/blob/master/README.zh_CN.md)
- [Vue 开发谷歌浏览器的脚手架](https://github.com/Kocal/vue-web-extension)



