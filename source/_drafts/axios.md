---
title: "axios网络请求"
date: 2017-11-01 21:32:00
categories: 编程之路
---



```javascript
const cancelTokenSource = axios.CancelToken.source();

// Optionally the request above could also be done as
axios.get('/user', {
  	cancelToken: cancelTokenSource.token
  	withCredentials: true,	// 跨域请求带上认证信息
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

cancelTokenSOurce.cancel();	// 取消请求
```