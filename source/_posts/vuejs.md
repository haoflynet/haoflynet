---
title: "Vue.js教程"
date: 2020-06-12 22:09:39
categories: js
---

## 模板语法

```javascript
// v-bind
<a v-bind:href="url">...</a>
<a :href="url">...</a>	// 缩写
<a :hidden="shouldHidden==='letshidden'">	// 在v-bind中直接用表达式

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
<div @keyup.188.native="func"></div> // 按下逗号触发
<div @mouseup.native="func"></div> // 鼠标按下
<div @mouseover.native="func"></div> // 鼠标移动到元素上
<div @mouseout.native="func"></div> // 鼠标移开
```

## Vuex

- 转为`Vue.js`应用程序开发的状态管理模式，采用集中式存储管理应用的所有组件的状态
- 解决了多个试图依赖于同一状态，来自不同视图的行为需要变更同一个状态的情况，有了`vuex`则就集中式管理了，否则可能需要再每次切换页面将所有的状态都带上才行

### Getter

- 如果要在页面中派生出一个状态通常会用到`computed`，但是如果每个页面都需要同一个状态，就可以在`store`中定义`getter`(可以认为是针对store的计算属性computed)
- 和`computed`一样，`getter`的返回值会根据它的依赖被缓存起来，且只有当它的依赖值发生了改变才会被重新计算

```javascript
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

##### 相关链接

- 仿造猫眼电影客户端实例: https://github.com/zhixuanziben/gouyan-movie-vue   
- Objc中国的全平台客户端: https://github.com/halfrost/vue-objccn
- 仿闲鱼：https://github.com/Sukura7/vue-ali-xianyu
- 仿hackernews: https://github.com/vuejs/vue-hackernews-2.0
- Flask与Vuejs创建一个简单的单页应用https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs
- [Vue表单可视化生成器](https://github.com/dream2023/vue-ele-form-generator)
- [滚动加载插件vue-infinite-loading](https://peachscript.github.io/vue-infinite-loading/guide/)