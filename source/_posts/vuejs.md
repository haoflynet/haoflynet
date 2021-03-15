---
title: "Vue.js教程"
date: 2020-06-12 22:09:39
updated: 2021-03-09 22:35:00
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
  
// v-model
<input type="text" v-model="msg"> // 等价于<input type="text" :value='msg' @input='handleInput'>
  
// 遍历v-for
<li v-for="item in items">{{item}}</li>
<li v-for="(item, index) in items">{{item}}的索引是{{index}}</li>
<li v-for="(value, name, index) in items">遍历key=>value格式的数组，顺便还有索引</li>
<li v-for="(item,index) in items"><span v-if="index !== items.length-1">判断是否是列表最后一个元素，目前没找到更好的方法</span></li>

// v-on
<a v-on:click="doSomething">...</a>
<a @click="doSomething">...</a>

// v-html，将内容不转义直接展示为html内容，如果是用户输入的内容，这里一定要防止XSS攻击，最简单的方法就是使用https://github.com/leizongmin/js-xss在外面处理一下
<div v-html="XSS(data)"></div>
<div v-html="$options.filter.myfilter(data)"></div>	// v-html中使用过滤器

// v-if, v-else, v-else-if, 条件判断
// v-show，只是控制是否展示，DOM是存在的
```

<!--more-->

### 动态数据绑定

```javascript
// 动态绑定class
<div 
:class="{ 'class_name': isOk ? true : false }"
:class="isOk ? 'class1': 'class2':
:class="isOk && class_name"
></div>

// 动态绑定style
<div :style="{ backgroundImage: 'url(' + image + ')'}" // 需要注意的是style名需要变成驼峰格式
```

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

## 路由

- `vue router`默认在跳转新页面会保持当前页面的`scroll`，有时候我们需要在新页面手动`window.scrollTo(0, 0)`

## 页面Script相关方法

### 实例/组件属性

- `$forceUpdate`: 强制页面重新渲染

- `$options`: 获取用户自定义的配置

  ```vue
  {{abc | $options.filters.myFilters}}
  ```

- `parent`: 从子组件访问父组件的实例

- `$ref`: 可以通过`this.$refs.xxx`来访问当前组件的指定的子组件/元素常用于获取表单

  ```vuejs
  <el-form :model="formData" :rules="rules" ref="testForm" @validate="validateForm" inline-message></el-form>
  <my-component ref="mine"></my-component>
  
  <script>
   const fields = this.$refs.contactForm.fields
   this.$refs.contactForm.validate(async (valid) => {})
   this.$refs.mine.myMethod()
   this.$refs.mine.offsetHeight // 获取元素高度宽度
  </script>
  ```

- `$root`: 用来访问`vue`的根实例

- `$watch`: 跟`watch`用法一样

  ```vue
  this.$watch('msg', function (oldValue, newValue) {})
  ```

### 全局API

#### Vue.nextTick

- 在下次DOM更新循环结束知乎执行延迟回调，在修改数据之后立即使用这个方法，可以在该方法里面获取到更新后的DOM
- 因为本质上数据修改后DOM的更新是异步的，该方法提供了一个等待DOM渲染完成后的回调操作

```javascript
// 修改数据
vm.msg = 'Hello'
// DOM 还没有更新，如果这个时候直接去获取DOM只能获取到更新前的
Vue.nextTick(function () {
  // DOM 更新了
})

// 作为一个 Promise 使用 (2.1.0 起新增，详见接下来的提示)
Vue.nextTick()
  .then(function () {
    // DOM 更新了
  })

// 例如，可以在一个组件中每次进入时候重新选然后执行某个操作
watch: {
  visible: {
    handler: function (value) {
      if (value) {
        this.$nextTick(function () {
          this.initSwiper()
        })
      }
    }
  }
}
```

### computed

- 用于计算一些`props`或`data`无法直接得到的变量
- 不会立马取值，用到的时候才会取值，并且有缓存，依赖数据不改变不会更新结果
- 在非严格模式下，如果用引用的方式对数据进行修改，例如`myAttr[key]`，可能会发生值改变了但是`set` 却没有触发器的情况

```vue
<script>
  computed: {
    isOk: {
      get () {
        return this.myList.every((item) => item > 0)
      },
      set (newValue) {
        this.myList.forEach(item => item = newValue)
      }
    }
  }
</script>
```

- **针对类似的get/set方法批量创建computed属性**，可以参考类似`mapGetters`的写法原理

  ```javascript
  const myProps = (computedNames: string[]) => {
    const computedProp: any = {};
    for (const prop of computedNames {
      computedProp[prop] = {
        get() {
          return 'computed' + prop;
        },
        set(newValue: any) {
          ......
        }
      }
    }
    return computedProp;
  }
  
  computed: {
    ...myProps(['value1', 'value2', 'value3']),
  }
  ```

### directives指令

- 指令，如果直接写在组件的`script`中则是局部的，这个用得少
- 定义了后就可以在要使用的标签上添加`v-xxx`，其中的`xxx`为指令名字
- [指令实例: Vue实现简单的鼠标拖拽滚动效果](https://haofly.net/vue-dragscroll/)

### document对象

- 同样可以获取document对象

```javascript
document.body.clientWidth	// 获取屏幕宽度
```

### props

```javascript
props: {
  value: [Number, String, Array]	// props支持多种类型的数据
}
```

### filter

- 过滤器，如果直接写在组件的`script`中则是局部的
- 在filter中无法使用上下文`this`，因为它设计来就仅仅是为了filter

```vue
<template>
  <div>
    {{ myValue | format1('newValue')}}
  </div>
</template>
<script>
  filters: {
    format1(value) {
      return newValue
    }
  }
</script>
```

### watch

- 用于观测值的变化，执行相应的函数
- 子组件如果有个单独的初始化函数可以用它来监听某个`prop`的值变化，变化了则可以执行一次初始化函数
- 与`computed`不同的是，它会立即执行，会先算出来一个老值，数据变化就执行函数

```vue
<script>
  watch: {
    msg: {
      handler: function (newValue, oldValue) {	// 需要触发的方法
        this.method1()
      },
      deep: true	// 是否深度遍历,
      immediate: true // 是否立即执行
    },
    field (value) {
      this.val = value
    },
    'queryData.status': 'fn', // 表示queryData.status值改变后执行methods的fn方法
  }
</script>
```

## 组件通信

### 父子组件通信

- `broadcast + dispatch`的方式已经弃用了

- 子组件如果要监听父组件值的变化，可以直接用`watch`监听`props`，当然如果子组件需要单独修改这值，可以在`datas`里面另外定一个一个变量，例如:

  ```javascript
  props: {
    field1: Boolean
  },
  data (props) {
    return {
      field1Rename: props.field1
    }
  },
  watch: {
    field1: {
      handler: function () {
        field1Rename = this.field1	// 每次父组件改变该prop的时候子组件需要恢复到初始值
      }
    }
  },
  methods: {
    changeField () {
      this.field1Rename = false	// 子组件能够单独修改该字段
    }
  }
  ```

- 下面示例列出了两种方式

```vuejs
// 父组件
<template>
	<div>
	  // 方法一： 直接把属性和函数传送给子组件，自组件能直接使用
    <Son :value="value" :changeValue="changeValue"></Son>
    // 方法二：emit的方式，子组件触发某个事件，父组件监听某个事件触发某个函数
		<Son :value="value" @myClickEvent="changeValue"></Son>
	</div>
</temlate>
<script>
import Son from './Son'
export default {
  components: {
    Son
  },
	data() {
		return {
		 value: 100
		}
	},
	methods: {
	  changeValue(newValue) {
	  	this.value = newValue
	  },
	  changeValue2(newValue) {
	    this.value += newValue
	  }
	}
}
</script>

// 子组件
<template>
	<div>
	  <button @click="changeValue(500)">button1</butotn>
	  <button @click="change">button2</button>
	</div>
</template>
<script>
 export default {
   props: {
     value: {
       type: Number,
       default: 10
     },
     changeValue: {
       type: Function,
       default: ()=> {}
     }
   },
   methods: {
     change () {
       this.$emit('myClickEvent', 10)
     }
   }
 }
</script>
```

### 非父子组件的通信

- 用`$bus`或者`$root`应该都能实现
- 其实是一种发布/订阅模式，谁都能订阅

```vue
// 组件一
<template>
  <div></div>
</template>
<script>
export default {
  mounted () { // 组件挂载的时候即监听该事件
  	this.$root.$on('myEvent:search', (value) => {
     console.log(value)
    })
    
    // 只监听一次，监听完成后立马移除
    this.$root.$once('myEvent:serach', (value) => {})
  },
  // 防止重复进入页面执行多次的现象
  beforeDestroy () {
    this.$root.$off('myEvent:search')
  }
}
</script>

// 组件二，其实是一个输入框
<template>
  <el-input prefix-icon="el-icon-search" placeholder="Search" v-model="keyword" @keyup.enter.native="onInputSearch" />
</template>
<script>
export default {
  data () {
    return {
      keyword: ''
    }
  },
  methods: {
    async onInputSearch () {
      this.$root.$emit('myEvent:search', this.keyword)
      this.keyword = ''
    }
  }
}
</script>

```

## 页面样式

- 经常给`style`标签添加`scoped`属性，表示当前CSS只作用于当前组件中的元素(其实现就是给元素添加data-xxx属性)，当然可以在一个组件中写两个不同的`style`以混用全局和局部样式。

- 使用`scoped`后，父组件的样式不会渗透到子组件，但是一个子组件的根节点会同事受其父组件有作用域的CSS和子组件有作用域的CSS的影响。所以父组件的样式调整可能会影响到子组件

- 如果不使用`scoped`，最好在需要覆盖的样式前加上顶级作用域：

  ```vuejs
  .myDiv .el-tag {
   color: black;
  }
  ```

## 事件处理

### 事件监听

```javascript
// 可以直接在监听里写语句
<button v-on:click="counter += 1">Add 1</button>
// 可以传递一个method给事件监听
<button @click="greet">Greet</button>
// 可以在事件监听的时候带上参数
<button v-on:click="say('what')">Say what</button>
// 可以将事件对象$event传递给方法
<button v-on:click="say('what', $event)">Say what</button>
```

### 事件修饰符

- 用得最多的是拿来阻止某些事件的发生或冒泡，例如`@keydown.enter.native.prevent`可以阻止`textarea`输入换行符，`@keyup.enter.native.stop`阻止回车时间向上冒泡

```vue
<!-- stop: 阻止单击事件继续传播 -->
<a v-on:click.stop="doThis"></a>

<!-- prevent: 提交事件不再重载页面 -->
<form v-on:submit.prevent="onSubmit"></form>

<!-- 多个修饰符可以串联 -->
<a v-on:click.stop.prevent="doThat"></a>

<!-- 可以只有修饰符，没有监听方法 -->
<form v-on:submit.prevent></form>

<!-- 添加事件监听器时使用事件捕获模式 -->
<!-- 即内部元素触发的事件先在此处理，然后才交由内部元素进行处理 -->
<div v-on:click.capture="doThis">...</div>

<!-- 滚动事件的默认行为 (即滚动行为) 将会立即触发 -->
<!-- 而不会等待 `onScroll` 完成  -->
<!-- 这其中包含 `event.preventDefault()` 的情况 -->
<div v-on:scroll.passive="onScroll">...</div>

<!-- 只当在 event.target 是当前元素自身时触发处理函数 -->
<!-- 即事件不是从内部元素触发的 -->
<div v-on:click.self="doThat">...</div>

<!-- 事件将只会触发一次 -->
<a v-on:click.once="doThis"></a>
```

### 手动触发事件

- 由于可以通过`this.$refs.refName.$el` 的方式得到原生的元素，所以原生的方法都能使用

```javascript
this.$refs.myEle.dispatchEvent(new MouseEvent('mouseenter'))	// 手动触发原生mouseenter事件
this.$refs.myEle.click()	// 可以这样直接调用某些自定义了方法的组件的事件(其实是组件的method)
```

### 常用事件

- 如果是普通的`div`标签可以直接加`@click`监听，但是对于自定义的组件则应该加上`native`修饰符才行，监听组件根元素的原生事件

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

## 异常处理

捕获全局异常可以这样做:

```javascript
// 除了errorHandler，还有
Vue.config.errorHandler = function (err, vm, info) {
  console.info(err, vm, info)
}

// 也可以在组件里面使用原生的页面监听方式
window.addEventListener("unhandledrejection", event => {
  console.warn(`UNHANDLED PROMISE REJECTION: ${event.reason}`);
});
window.addEventListener('error', function(event) { ... })
```

## Vuex

- 专为`Vue.js`应用程序开发的状态管理模式，采用集中式存储管理应用的所有组件的状态
- 解决了多个视图依赖于同一状态，来自不同视图的行为需要变更同一个状态的情况，有了`vuex`则就集中式管理了，否则可能需要再每次切换页面将所有的状态都带上才行
- 与全局变量不同，它的状态存储是响应式的。当Vue组件从store中读取状态的时候，若store中的状态发生变化，那么相应的组件也会相应地更新
- 不能直接改变`store`中的状态，改变的唯一途径就是显式地提交(commit) mutation
- `state`即是公共数据池
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
  strict: true, // 是否开启严格模式，当开启后，是无法在mutations外面直接修改数据池里面的值的。如果不开启严格模式，在使用饮用的方式来修改对象的时候可能不会触发某些对象的computed的setterc
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

## 静态文件

- 可以通过`@/assets/fileName`来访问`assets`下的静态文件，例如`<img src="@/assets/filaneme">`
- img的src是无法动态解析的，一般都只能硬编码，不能放一个变量在这里，除非它是`base64`或者把图片放到src同级的static目录下然后用static/a.png这种方式来访问，因为`url-lodaer`无法解析js动态生成的路径

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

- axios默认不会对url进行编码，可以使用`encodeURI`或者`encodeURIComponent`对URL进行编码，前者会避开`&/?/[/]`等url中的功能性字符

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

##  文件上传处理

```javascript
// template只需要input即可
<input type="file" accept="image/*" @change="onFile($event)" multiple />
  
onFile (event) {
  const fileLength = event.target.files.length
  for (let i = 0; i < fileLength; i++) {
    const file = event.target.files[i]
    const reader = new FileReader()
    reader.onload = (e) => {
			// 读取上传照片的size尺寸
      let image = new Image()
      image.src = e.target.result
      image.onload = (e) => {
      if (e.path && e.path[0] && e.path[0].width && e.path[0].height) {
        const width = event.path[0].width
        const height = event.path[0].height
      }
    }
    reader.readAsDataURL(file)
  }
}
```

##### TroubleShooting

- **更改数据页面不渲染**，可能有如下原因
  - 在给data赋值后只是简单地添加新的属性，没有用this.$set等方法，导致没有新添加的属性没有实现双向绑定，从而导致重新渲染失败。常见现象也有改变一个值，第一次改变页面渲染成功，之后再改变页面不会更新等
- **页面跳转出错/NavigationDuplicated**: 页面跳转经常出现莫名其妙的错误，所以一般都会把异常直接忽略，例如`router.push('/next').catch(err => {})`

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
- Toasts Notification Bar 库: vue-toastification
- Table库：vue-good-table
- 时间选择库: vue2-datepicker



