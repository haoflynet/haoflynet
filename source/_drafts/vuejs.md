---
title: "Vue.js教程"
date: 2017-05-25 17:09:39
updated: 2017-08-29 17:48:00
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



##### 相关链接

仿造猫眼电影客户端实例: https://github.com/zhixuanziben/gouyan-movie-vue   

Objc中国的全平台客户端: https://github.com/halfrost/vue-objccn

仿闲鱼：https://github.com/Sukura7/vue-ali-xianyu

仿hackernews: https://github.com/vuejs/vue-hackernews-2.0