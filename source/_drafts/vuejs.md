---
title: "Vue.js教程"
date: 2017-05-25 17:09:39
updated: 2020-06-10 15:48:00
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

// v-if, v-else, v-else-if, 条件判断
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