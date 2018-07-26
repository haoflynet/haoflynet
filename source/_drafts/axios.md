---
title: "axios网络请求"
date: 2017-11-01 21:32:00
categories: 编程之路
---



```javascript
// Optionally the request above could also be done as
axios.get('/user', {
    params: {
      ID: 12345
    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```