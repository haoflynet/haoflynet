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
    console.log(error, error.response.data);
  });

axios.post('/user', {
  firstName: 'Fred',
  lastName: 'Flintstone'
})

cancelTokenSOurce.cancel();	// 取消请求



使用API发送请求
// Send a POST request
axios({
  method: 'post',
  url: '/user/12345',
  headers: {},
  params: {},
  timeout: 0,	// 超时时间，默认为0，不超时,
  responseType: 'json', // 默认接收JSON响应
  xsrfCookieName: 'XSRF-TOKEN',
  onUploadProgress: function (progressEvent) {
    
  },
  onDoanloadProgress: function (progressEvent) {
    
  },
  validateStatus: function (status) {
    return status >= 200 && status < 300; // default
  },
    proxy: {	// 代理设置
    protocol: 'https',
    host: '127.0.0.1',
    port: 9000,
    auth: {
      username: 'haofly',
      password: 'xxxxxxxx'
    }
  },
  maxRedirects: 5, // 默认重试次数为5
  data: {
    firstName: 'hao',
    lastName: 'fly'
  }
});
// GET request for remote image in node.js
axios({
  method: 'get',
  url: 'http://haofly.net',
  responseType: 'stream'
})
  .then(function (response) {
    response.data.pipe(fs.createWriteStream('aaa.jpg'))
  });


并发请求
function getUserAccount() {
  return axios.get('/user/12345');
}

function getUserPermissions() {
  return axios.get('/user/12345/permissions');
}

Promise.all([getUserAccount(), getUserPermissions()])
  .then(function (results) {
    const acct = results[0];
    const perm = results[1];
  });
```

## Troubleshooting

- **curl正常，但是axios就是会报Request failed with status code 500错误**: 可能是因为用了代理，我发现有些接口不能用代理(例如https://graph.facebook.com/me?access_token)，只要用代理就报错，无论http还是https的代理，在代码里面设置proxy也会报错，反正就是不行，放在外网服务器就可以了，关键在cmd里面设置代理后用curl又是可以的