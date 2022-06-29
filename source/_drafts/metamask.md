- 很多类似的钱包应用都是注入了`window.ethereum`，使得连接钱包变得通用

## API调用

### 连接钱包/获取Accounts

```javascript
const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
const account = accounts[0];
```



e认证流程https://www.toptal.com/ethereum/one-click-login-flows-a-metamask-tutorial

nonce也可以直接前端随机弄，安全性差那么一点点，但是方便一些





metamask能够在前端将transaction签名并发送到当前连接的网络，它不能仅将签名的data给你，而是会直接帮你发送到网络，其他的签名方法不能用于签名transaction，可能也是防止你把签了名的数据到处到其他network里面提交