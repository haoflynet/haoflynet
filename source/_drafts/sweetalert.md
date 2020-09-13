---
title: "Sweetalert "
date: 2020-09-08 14:40:00
categories: Javascript
---

如果是超过2个button，那么不能简单地定义一个数组，而是要这样定义

```
buttons: {
    continue: 'Continue last visit',
    new_visit: 'Start a new visit',
    new_visit_with_answers: 'Start a new visit with last answers',
    cancel: 'Cancel'
},
```

https://sweetalert.js.org/docs/#content

```js
swal.close(); 关闭所有
```