fetch

```javascript
fetch("/myapi", {
  method: "POST",
  cache: 'no-cache',
  credentials: 'some-origin',
  mode: 'cors', // no-cors, cors, *same-origin
  redirect: 'follow', // manual, *follow, error
  referrer: 'no-referrer', // *client, no-referrer
  headers: {
    'Content-Type': 'applicatoin/json'
  },
  body: JSON.stringify({})
})
  .then(response => response.json())	// 获取JSON格式的返回数据
	.then(data => data);


fetch("/myapi")	// GET请求可以不用加第二个参数
  .then(response => response.json())	// 获取JSON格式的返回数据
	.then(data => data);

// 添加查询参数
fetch('https://example.com?' + new URLSearchParams({
    foo: 'value',
    bar: 2,
}))
```



