---
title: "Vue.js教程"
date: 2017-05-25 17:09:39
updated: 2019-03-07 15:48:00
categories: js
---

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

仿造猫眼电影客户端实例: https://github.com/zhixuanziben/gouyan-movie-vue   

Objc中国的全平台客户端: https://github.com/halfrost/vue-objccn

仿闲鱼：https://github.com/Sukura7/vue-ali-xianyu

仿hackernews: https://github.com/vuejs/vue-hackernews-2.0

Flask与Vuejs创建一个简单的单页应用https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs