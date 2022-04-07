## 安装和使用

```shell
npm install web3 --save
```

- web3下面的api是分部在不同的命名空间的

```javascript
// 可以全局用
var Web3 = require('web3');
var web3 = new Web3(Web3.givenProvider || 'ws://some.local-or-remote.node:8546');
var eth = web3.eth

// 也可以单独用某一个命名空间的
var Eth = require('web3-eth');
var eth = new Eth(Eth.givenProvider || 'ws://some.local-or-remote.node:8546');

// 可以自定义headers
import {HttpHeader} from "web3-core-helpers";
const headers: HttpHeader[] = [{ name: 'token', value: token }];
web3 = new Web3(new Web3.providers.HttpProvider(rpcUrl || '', { headers }));
```

## API

### web3.eth

```javascript
web3.eth.getTransactionCount('0x...')	// 获取用户的transaction数量
web3.eth.getBalance('0x...')	// 获取指定用户的balance
web3.eth.getTransactionReceipt(hash)	// 获取指定hash的结果
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

## BN大数类型

-  很多web3相关的库都会用到BN大数类型这个库(BigNumber.js)

```javascript
var num = BigNumber.clone()
num(1).div(3).toNumber()	// 将大数类型直接转换为数字
```

