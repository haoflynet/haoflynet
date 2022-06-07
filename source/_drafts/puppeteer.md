## 安装配置

### 不同系统的安装

- 先安装依赖: ` sudo apt-get install xdg-utils`

- ubuntu系统下载指定版本可以在[这里](http://archive.ubuntu.com/ubuntu/pool/universe/c/chromium-browser/)找到
- 当我在aws系统中使用apt install的时候发现能安装成功，但是运行时却有bug，无法下载文件，且没有任何的报错。使用`chromium-browser -version`发现是snap版本的，尝试切换成ubuntu版本能够成功，需要这样做: `sudo add-apt-repository ppa:saiarcot895/chromium-beta && sudo apt-get update && sudo apt install chromium-browser`
- Mac M1需要这样安装`brew install chromium --no-quarantine`，安装完成后文件在`/opt/homebrew/bin/chromium`，必须加后面这个参数否则会说文件损坏(damaged)无法打开

### 初始化

```javascript
const browser = await puppeteer.launch({
    executablePath: 'path/to/your/chromium'	// 可以手动指定二进制执行文件
});
```

## 页面操作

```javascript
// 页面等待
await page.waitForFunction(() => !document.querySelector('#nprogress'));
```

## 事件监听

```javascript
page
  .on('console', message => {
        console.log(`${message.type().substr(0, 3).toUpperCase()} ${message.text()}`))
	})
  .on('pageerror', ({ message }) => {
  	console.log(message)
	})
  .on('response', response => {
      console.log(`${response.status()} ${response.url()}`)
  
  		// 监听指定的url请求，主要是否是OPTIONS请求哟
  		if (response.url().endsWith('/userinfo') && response.request().method() !== 'OPTIONS') 			 {
        // 获取json格式的响应
      	const res = await response.json();  
      }
	})
  .on('requestfailed', request => {
      console.log(`${request.failure().errorText} ${request.url()}`)
	})
```