---
title: "axios网络请求"
date: 2021-09-23 18:32:00
updated: 2022-07-05 08:34:00
categories: javascript
---

## 基本请求

```javascript
// 基本请求方式
axios({
  method: 'post',
  url: '/user/123',
  headers: {},
  params: {},
  data: {}, // POST的data
  timeout: 0, 	// 超时时间，默认为0，表示不超时
  responseType: 'json',	// 默认接收JSON格式的响应
  maxRedirects: 5, // 默认重试次数为5
  onUploadProgress: function (progressEvent) {}, // 上传前执行
  onDownloadProgress: function (progressEvent) {},	// 下载前执行
  validateStatus: function (status) {
    return status >= 200 && status < 500	// 定义哪些http状态不会抛错
  }
})
  .then((rersponse: AxiosResponse) => {})
	.catch((error: AxiosError) => {
  	console.log(error.response.status)	// 获取返回状态码
  	console.log(error.message)	// 获取错误信息
    console.log(JSON.parse(error.request.response).message)	// 另外一种错误相应的格式
  	console.log(`${error.config.baseURL}${error.config.url}`) // 获取请求的URL
	})

// 创建一个可复用的client
const client = axios.create({
  baseURL: '',
  headers: {}
})
```

## Axios跨域请求

```javascript
axios.get('/user', {
  withCredentials: true,	// 跨域请求带上认证信息
  params: {}
}).then(...).catch(...)
```

<!--more-->

### XSRF请求

```javascript
axios({
  xsrfCookieName: 'XSRF-TOKEN'	// 带上这个参数能自动从cookie里面获取xsrf的token置入header头
})
```

## 中间件/hook/beforerequest

```javascript
axios.interceptors.request.use((config) => {
  config.headers = {....};
  return config;
});
```

## 取消Axios的HTTP请求

```javascript
const cancelTokenSource = axios.CancelToken.source();
axios.get('/xxx', {
  cancelToken: cancelTokenSource.token
}).then(...).catch(...)

cancelTokenSource..cancel	// 取消请求
```

## Axios设置代理

```javascript
axios({
  proxy: {
    protocol: 'https',
    host: '127.0.0.1',
    port: 9000,
    auth: {
      username: 'haofly',
      password: 'xxx'
    }
  }
})
```

## Axios并发请求

```javascript
function getUserAccount() { return axios.get('/user/12345') }

function getUserPermissions() { return axios.get('/user/12345/permissions') }

Promise.all([getUserAccount(), getUserPermissions()])
  .then(function (results) {
    const acct = results[0];
    const perm = results[1];
  });
```

## Axios下载文件

```javascript
axios.get(url, responseType: 'blob').then(response => {
  console.log(response.data.split('\n')	// 下载csv文件能够直接读取
})

axios({
  method: 'get',
  url: 'http://haofly.net',
  responseType: 'stream'
})
  .then(function (response) {
    response.data.pipe(fs.createWriteStream('aaa.jpg'))
  });
```

## Troubleshooting

- **curl正常，但是axios就是会报Request failed with status code 500错误**: 可能是因为用了代理，我发现有些接口不能用代理(例如https://graph.facebook.com/me?access_token)，只要用代理就报错，无论http还是https的代理，在代码里面设置proxy也会报错，反正就是不行，放在外网服务器就可以了，关键在cmd里面设置代理后用curl又是可以的