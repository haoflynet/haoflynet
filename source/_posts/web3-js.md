---
title: "web3js 使用手册"
date: 2022-04-14 18:02:30
updated: 2022-09-06 12:00:00
categories: eth
---

## 安装和使用

```shell
npm install web3 --save
```

- web3下面的api是分部在不同的命名空间的

```javascript
// 可以全局用
var Web3 = require('web3');
var web3 = new Web3(Web3.givenProvider || 'ws://some.local-or-remote.node:8546');
const web3 = new Web3(new Web3.providers.WebsocketProvider('WSS_ENDPOINT', {
  reconnect: {	// 断开重连选项
    auto: true,
    delay: 5000, // ms
    maxAttempts: 5,
    onTimeout: false
  }
}));
var eth = web3.eth

// 也可以单独用某一个命名空间的
var Eth = require('web3-eth');
var eth = new Eth(Eth.givenProvider || 'ws://some.local-or-remote.node:8546');

// 可以自定义headers
import {HttpHeader} from "web3-core-helpers";
const headers: HttpHeader[] = [{ name: 'token', value: token }];
web3 = new Web3(new Web3.providers.HttpProvider(rpcUrl || '', { headers }));
```

<!--more-->

## API

### web3.eth

```javascript
web3.eth.getTransactionCount('0x...')	// 获取用户的transaction数量
web3.eth.getBalance('0x...')	// 获取指定用户的balance
web3.eth.getTransactionReceipt(hash)	// 获取指定hash的结果，结果只能通过status判断是成功还是失败，但是没有具体的原因
// 获取transaction失败的原因
tx = await web3.eth.getTransaction(hash)
try {
  await web3.eth.call(tx)
} catch (e) {
  console.log(e.message)
}
```

#### web3.eth.accounts

```javascript
const account web3.eth.accounts.privateKeyToAccount('0xaaaaa');	// 通过私钥获取账户信息
{
  address: '0xaaaa', // 账户的钱包地址
  privateKey: '0xaaaa',
  signTransaction: function(tx){...}, // 还能直接得到签名方法
  sign: function(data){...},
  encrypt: function(password){...}
}
```

#### web3.eth.contract

调用智能合约

```javascript
// 初始化
var Contract = require('web3-eth-contract');
Contract.setProvider(RPC_ENDPOINT);
const contract = new Contract(ABI_arr, Contract_address)

// 调用contract的方法
contract.methods.name().call()	

// 如果是需要签名的方法，必须这样做
const rawTransaction = {
  from: "账户地址",
  gasPrice: web3.utils.toHex(20 * 1e9),
  gasLimit: web3.utils.toHex(210000),
  to: "合约地址",
  value: 0x0,
  data: contract.methods.transfer("账户地址", web3.utils.toHex(1000)).encodeABI(),	// 调用合约的方法的话data得是这样
  nonce: web3.utils.toHex(transactionCount)
}
const signedTx = await eth.accounts.signTransaction(rawTransaction, "账户的private key");
const res = await eth.sendSignedTransaction(signedTx.rawTransaction);	// 发送transaction到network，注意链上必须有矿工来在挖矿该transaction才能执行完成
```

#### web3.eth.net

```javascript
web3.eth.net.isListening()	// 代替低版本的isConnected()
```

### events事件监听

```javascript
// 这里的eventName就是在solidity中定义的事件的名称
contract.events.eventName({
  filter: {},
  fromBlock: 0
}, (error, event) => {})
```

## BN大数类型

-  很多web3相关的库都会用到BN大数类型这个库(BigNumber.js)

```javascript
var num = BigNumber.clone()
num(1).div(3).toNumber()	// 将大数类型直接转换为数字
```

## Troubleshooting

- **Web3 is undfeind / TypeError: Cannot read property 'providers' of undefined**: typescript里面遇到这个问题，可以用`(Web3 as any)`代替
  
- **replacement transaction underpriced**: 我遇到两种情况：
  一是提交transaction的时候nonce设置为了一样的，并且gas fee也一样，所以会报错，要么nonce不一样，如果真的要在之前的操作确认前进行覆盖，必须提高gas fee人家才愿意先挖你这个。
  二是无论怎样提高gas price，transaction依然在queued队列中(注意不是pending)，原因是nonce没有连续(可能是由于在geth中清空了transaction导致的或者乱修改nonce导致的)，queued中的nonce和`getTransactionCount`的nonce值中间有空的，这个时候尝试调用其他的transaction，直到nonce连续为止就能执行了
  
- **在前端集成的时候出现proces is not devined的问题**: 我是在vite框架中遇到的，解决办法如下:

  ```javascript
  // 在index.html中添加
  <script type="module">
    window.global = window;
    import process from "process";
    import { Buffer } from "buffer";
  
    window.process = process;
    window.Buffer = Buffer;
  </script>
  
  // 在vite.config.ts中添加npm install agent-base process
  resolve: {
    alias: {
      process: 'process/browser',
      util: 'util',
      https: 'agent-base',
      http: 'agent-base',
      zlib: 'browserify-zlib'
    }
  },
  ```

  
