## 以太坊的客户端

### go-ethereum/geth

## 账户

- 以太坊的两种账户
  - 外部账户(EOAs): 由私钥的所有者控制，外部所有的账户之间只能进行ETH和代币交易
  - 合约账户：既有余额也有合约存储，是一种由代码控制，部署在网络上的智能合约。创建合约存在成本，因为需要使用网络存储空间，只能在收到交易时发送交易
- 以太坊账户包含四个字段:
  - nonce: 显示从账户发送的交易数量的计数器，这能确保交易只处理一次
  - balance: 拥有的以太币的数量
  - codeHash: 表示以太坊虚拟机(EVM)上的账户代码
  - storageRoot: 存储哈希
- 每个账户都有一个私钥和一个公钥
- 账户的地址取的是公钥的最后20个字节
- 每对私钥/地址都编码在一个钥匙文件(keystore)里，这是一个json文件，里面的私钥是用户自己的密码进行了加密的。要注意备份`keystore`目录
- 创建账户可以在geth控制台也可以不在控制台创建
- Mist钱包只是一个GUI的创建账户的方式
- 合约地址通常在将合约部署到以太坊区块链时给出。 地址产生自创建人的地址和从创建人地址发送的交易数量
- 帐户和钱包不同。 账户是用户拥有的以太坊账户的密钥和地址对。 钱包是一个界面或者说应用程序，可以让您与以太坊账户交互。

## Ether以太币

- 下面是常用的单位

| Unit  | Wei Value | Wei                       |
| ----- | --------- | ------------------------- |
| wei   | 1 wei     | 1                         |
| ether | 1^18 wei  | 1,000,000,000,000,000,000 |

## 以太坊网络

## 挖矿

## 交易

- A转给B，相当于改变了EVM状态的交易，需要广播到整个网络，任何节点都可以在EVM上广播交易请求，伺候矿工将执行交易并将由此产生的状态变化传播到网络的其他部分

- 交易需要收费并且必须开采才能有效，包括Gas费和挖矿。Gas指矿工处理交易所需的蒜粒，用户必须为此计算支付费用，gasLimit和gasPrice决定支付给矿工的最高交易费用。关于Gas的计算可以参考[这里](https://ethereum.org/zh/developers/docs/transactions/#on-gas)

- 一个交易包括下面信息:

  - recipient: 接收地址
  - signature: 发送者的标识符
  - value: 交易的ETH的金额，以WEI为单位
  - data: 可包括任意数据的可选字段
  - gasLimit: 交易可以消耗的Gas的最大数量，Gas单位代表了计算步骤
  - maxPriorityFeePerGas: 作为矿工消费包含的最大gas数量
  - maxFeePerGas: 愿意为交易支付的最大gas数量，包括baseFeePerGas和amxPriorityFeePerGas

- 交易对象看起来像这样:

  ```json
  {
    from: "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
    to: "0xac03bb73b6a9e108530aff4df5077c2b3d481e5a",
    gasLimit: "21000",
    maxFeePerGas: "300"
    maxPriorityFeePerGas: "10"
    nonce: "0",
    value: "10000000000",
  }
  ```

- 以太坊客户端(如geth)将对此交易进行签名:

  ```json
  {
    "id": 2,
    "jsonrpc": "2.0",
    "method": "account_signTransaction",
    "params": [
      {
        "from": "0x1923f626bb8dc025849e00f99c25fe2b2f7fb0db",
        "gas": "0x55555",
        "maxFeePerGas": "0x1234",
        "maxPriorityFeePerGas": "0x1234",
        "input": "0xabcd",
        "nonce": "0x0",
        "to": "0x07a565b7ed7d7a678680a4c162885bedbb695fe0",
        "value": "0x1234"
      }
    ]
  }
  ```

- 签名后的样子:

  ```json
  {
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
      "raw": "0xf88380018203339407a565b7ed7d7a678680a4c162885bedbb695fe080a44401a6e4000000000000000000000000000000000000000000000000000000000000001226a0223a7c9bcf5531c99be5ea7082183816eb20cfe0bbc322e97cc5c7f71ab8b20ea02aadee6b34b45bb15bc42d9c09de4a6754e7000908da72d48cc7704971491663",
      "tx": {
        "nonce": "0x0",
        "maxFeePerGas": "0x1234",
        "maxPriorityFeePerGas": "0x1234",
        "gas": "0x55555",
        "to": "0x07a565b7ed7d7a678680a4c162885bedbb695fe0",
        "value": "0x1234",
        "input": "0xabcd",
        "v": "0x26",
        "r": "0x223a7c9bcf5531c99be5ea7082183816eb20cfe0bbc322e97cc5c7f71ab8b20e",
        "s": "0x2aadee6b34b45bb15bc42d9c09de4a6754e7000908da72d48cc7704971491663",
        "hash": "0xeba2df809e7a612a0a0d444ccfa5c839624bdc00dd29e3340d46df3870f8a30e"
      }
    }
  }
  ```

## 智能合约

- 只是一个运行在以太坊链上的一个程序，是一个特定地址的一系列代码(函数)和数据(状态)
- 智能合约也是一个以太坊账户，即合约账户，这意味着他们有余额，可以通过网络进行交易。但是无法被人操控，他们是被部署在网络上作为程序运行着
-  个人用户可以通过提交交易执行智能合约的某一个函数来与智能合约进行交互
- 一个智能合约，就像自动售货机一样，是有逻辑被写入进去的。任何人都可以编写智能合约并将其部署到区块链网络上
- 在技术上，部署智能合约是一项交易，所以也需要支付Gas，这比以太坊转账要高得多
- 智能合约编写语言: Solidity、Vyper

### Solidity

- hello world

```solidity
// 确定 Solidity 版本，使用语义化版本。
// 了解更多：https://solidity.readthedocs.io/en/v0.5.10/layout-of-source-files.html#pragma
pragma solidity ^0.5.10;

// 定义合约名称 `HelloWorld`。
// 一个合约是函数和数据（其状态）的集合。
// 一旦部署，合约就会留在以太坊区块链的一个特定地址上。
// 了解更多： https://solidity.readthedocs.io/en/v0.5.10/structure-of-a-contract.html
contract HelloWorld {
    // 定义`string`类型变量 `message`
    // 状态变量是其值永久存储在合约存储中的变量。
    // 关键字 `public` 使得可以从合约外部访问。
    // 并创建了一个其它合约或客户端可以调用访问该值的函数。
    string public message;

    // 类似于很多基于类的面向对象语言，
    // 构造函数是仅在合约创建时执行的特殊函数。
    // 构造器用于初始化合约的数据。
    // 了解更多：https://solidity.readthedocs.io/en/v0.5.10/contracts.html#constructors
    constructor(string memory initMessage) public {
        // 接受一个字符变量 `initMessage`
        // 并为合约的存储变量`message` 赋值
        message = initMessage;
    }

    // 一个 public 函数接受字符参数并更新存储变量 `message`
    function update(string memory newMessage) public {
        message = newMessage;
    }
}

```

- 代币token example

```solidity
pragma solidity ^0.5.10;

contract Token {
    // 一个 `address` 类比于邮件地址 - 它用来识别以太坊的一个帐户。
    // 地址可以代表一个智能合约或一个外部（用户）帐户。
    // 了解更多：https://solidity.readthedocs.io/en/v0.5.10/types.html#address
    address public owner;

    //  `mapping` 是一个哈希表数据结构。
    // 此 `mapping` 将一个无符号整数（代币余额）分配给地址（代币持有者）。
    // 了解更多： https://solidity.readthedocs.io/en/v0.5.10/types.html#mapping-types
    mapping (address => uint) public balances;

    // 事件允许在区块链上记录活动。
    // 以太坊客户端可以监听事件，以便对合约状态更改作出反应。
    // 了解更多： https://solidity.readthedocs.io/en/v0.5.10/contracts.html#events
    event Transfer(address from, address to, uint amount);

    // 初始化合约数据，设置 `owner`为合约创建者的地址。
    constructor() public {
        // 所有智能合约依赖外部交易来触发其函数。
        // `msg` 是一个全局变量，包含了给定交易的相关数据，
        // 例如发送者的地址和包含在交易中的 ETH 数量。
        // 了解更多：https://solidity.readthedocs.io/en/v0.5.10/units-and-global-variables.html#block-and-transaction-properties
        owner = msg.sender;
    }

    // 创建一些新代币并发送给一个地址。
    function mint(address receiver, uint amount) public {
        // `require` 是一个用于强制执行某些条件的控制结构。
        // 如果 `require` 的条件为 `false`，则异常被触发，
        // 所有在当前调用中对状态的更改将被还原。
        // 学习更多: https://solidity.readthedocs.io/en/v0.5.10/control-structures.html#error-handling-assert-require-revert-and-exceptions

        // 只有合约创建人可以调用这个函数
        require(msg.sender == owner, "You are not the owner.");

        // 强制执行代币的最大数量
        require(amount < 1e60, "Maximum issuance exceeded");

        // 将 "收款人"的余额增加"金额"
        balances[receiver] += amount;
    }

    // 从任何调用者那里发送一定数量的代币到一个地址。
    function transfer(address receiver, uint amount) public {
        // 发送者必须有足够数量的代币用于发送
        require(amount <= balances[msg.sender], "Insufficient balance.");

        // 调整两个帐户的余额
        balances[msg.sender] -= amount;
        balances[receiver] += amount;

        // 触发之前定义的事件。
        emit Transfer(msg.sender, receiver, amount);
    }
}
```





以太坊json rpc文档https://eth.wiki/json-rpc/API



在线ABI encode：https://abi.hashex.org/



ABIv2格式不兼容issue：https://github.com/web3p/web3.php/issues/188

https://ethereum.stackexchange.com/questions/64562/about-abi-encoder-v2



keccak_256在线计算https://emn178.github.io/online-tools/keccak_256.html



# replacement transaction underpriced 

price设置太高了，钱不够了