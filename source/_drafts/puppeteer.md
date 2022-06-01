监听各种错误

```js
  page
    .on('console', message =>
      console.log(`${message.type().substr(0, 3).toUpperCase()} ${message.text()}`))
    .on('pageerror', ({ message }) => console.log(message))
    .on('response', response =>
      console.log(`${response.status()} ${response.url()}`))
    .on('requestfailed', request =>
      console.log(`${request.failure().errorText} ${request.url()}`))
```





```
等待DOM
await page.waitForFunction(() => !document.querySelector('#nprogress'));



ProtocolError: Could not load body for this request. This might happen if the request is a preflight request可能只是path 请求
```