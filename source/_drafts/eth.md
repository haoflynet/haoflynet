- 区块链是一种特殊的分布式数据库，只能坐插入和查找操作
- 任何人都可以架设服务器加入区块链网络，成为一个节点，没有中心节点，每个节点都是平等的，都保存着整个数据库
- 以太坊Ethereum是一个分布式的计算机，每一个节点都会执行字节码(智能合约)，然后把结果存在区块链上
- 挖矿机制:
  - POW(Proof of Work, mine)工作证明。例如莱特币，比特币等。干得越多，得到越多
  - POS(Proof of Stake, mint)股权证明/权益证明。例如狗狗币，点点币等。根据持有货币的量和时间给你发利息的一个制度。比特币的产品会减少，挖矿的动力也会减少，以后可能连节点都找不到了。在POS体系中，只有打开钱包客户端程序，才能发现POS区块，才会获得利息。在POW体系中，如果超过51%的算力就能进行攻击，但是在POS中，因为有些币是利息产生的，攻击者不仅要超过51%的算力，还要超过51%的货币量。持有越多，获得越多。不过也会导致持币集中化，流动性变差，因为想要利息，所以不想套现了。限制每人每秒只能计算一次哈希值，想要挖得快就得拥有多。
- 因为是不可更改且验证了的，所以只需要找最后一个区块就可以找到用户的余额。每个区块记录的是当前区块的交易记录以及最后的余额
- 如果转账给了一个不存在的钱包，在矿工确认前可以挽回，晚上有方法，不过也比较困难，如果矿工确认了就找不回来了
- 以太坊测试链，这里可以直接从测试链获取eth：https://faucets.chain.link/rinkeby
- Provider: 提供者，是一个连接以太坊网络的抽象，用于查询以太坊网络状态或者发送更改状态的交易。

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
- 账户是公开透明的，只要知道地址，就可以查询任何用户的余额

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
  - gasLimit: 交易可以消耗的Gas的最大数量，Gas单位代表了计算步骤，一个单独交易的上限，最终的消耗不会多于`gas price * gas limit`
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
- 要调用区块链上的智能合约，不仅要有合约地址，就必须要有ABI(Application Binary Interface)的内容，因为程序是二进制的，所以必须要正确地将入参和出参编译才行，所以就需要用到ABI。当然智能合约一般也就是部署的人来开发应用
- 我们无法列出某个区块链上的智能合约，因为链上就只有一些bytecode，根本不知道那是啥，只有知道那个地址，并且知道ABI才能知道这是个什么样的智能合约

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

### ERC-20代币

- ERC(Ethereum Request for Comments)，以太坊注释请求
- ERC-20代币并不存入账户，而是仅存在于合约内部，如同独立的数据库。它指定代币的规则，并保留一个映射用户余额的以太坊地址列表
- 为了转移代币，用户必须将交易发送到智能合约，要求合约将部分余额分配到其他地方
- 代币无法开采，新代币的创建成为铸造(minting)，合约上线后，开发人员将根据计划和路线图分配供应量。一般通过首次代币发行(ICO)、首次交易所发行(IEO)或证券型代币发行(STO)来完成。投资者将以太币发送至合约地址并获得新代币作为回报。代币发行不一定自动执行，许多众筹活动支持用户使用各种数字货币来完成支付，然后将相应余额分配到用户的地址
- 标准ERC-20的代币总量是不变的，当然只要兼容，完全可以自己编写一个增发的功能
- ERC-20标准的函数
  - totalSupply： 返回合约所持有的代币的总供应量
  - balanceOf(address _owner): 返回该地址所以持有的代币余额 
  - transfer(): 转账，调用后会触发事件，基告知区块链包含针对此函数的调用
  - transferFrom(): 与`transfer`类似，但是它不一定是转自己的钱，只要对方授权过，那么可以将对方的钱转给另一个人，也会触发`transfer`的事件
  - approve(): 可以限制智能合约从余额中提取的代币数量(比如付费订阅的场景，允许你定时扣定量的钱)
  - allowance(): 和approve结合使用，收于代币管理权限
  - name(可选)
  - symbol(可选)
  - decimal(可选)
- 代币种类
  - 稳定币(与法币挂钩的代币): 通常使用ERC-20代币标准，例如BUSD合约交易。对于主流法定货币支持的稳定币，发行方可以持有欧元、美元等储备金，然后针对储备金中的每个单位发型代币。例如将一万元存入金库，发行方可以创建1万枚代币，每枚代币可兑换1美元。
  - 证券型代币: 发行方不同，代表的是有价的证券(股票等)
  - 效用代币: 最常见的，没有任何实际资产提供支持。

代币token example

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

### ERC721、ERC721A(NFT)

- 目前流通中的NFT项目，大多数是基于OpenZeppelin的ERC721来实现。我去，这个就是非同质化代币NFT，不可像钱那样，你的一美元肯定等于我的一美元，并且每个NFT是独一无二的，且不可分割
- ERC721 NFT为了能够简单地知道该合约内的发行总量、持有者等情况，一般都会实现另外一个标准ERC721Enumerable(totalSupply、tokenByIndex、tokenOfOwnerByIndex)。但是实现这些事需要存储数据的，这也是为什么要话费大量gas的原因
- 继承标准
  - ERC721A: 能够大量减少gas fee。铸造一个ERC721A的NFT话费的gas比ERC721少一倍多。针对ERC721Enumerable以及mint等做了很多的优化，减少了数据存储量
- 每个NFT都有一个id，mint的时候相当于就是放了一些id进去
- NFT在公开发售之前，都会让一小部分被授权的地址，可以提前购买preSale。因为能够保证取得购买资格，无需与他人疯抢，所以很多人都像被加入白名单。https://www.frank.hk/blog/nft-whitelist/，比直接存储所有的白名单用户要少存储很多数据

### Ecrow托管



## RPC客户端

- 客户端通过http RPC的方式进行调用

- web3.js

- web3.py

  ```shell
  pip install web3
  ```


## Infura

- 作用是不用启节点就能连接RPC服务，如果不能直接连接对方的network rpc服务，那么只有自己启一个节点才能连接RPC服务，infura就是代替你启动节点，你可以直接使用API。同步节点并存储区块链数据可能需要好几天



以太坊json rpc文档https://eth.wiki/json-rpc/API



在线ABI encode：https://abi.hashex.org/



ABIv2格式不兼容issue：https://github.com/web3p/web3.php/issues/188

https://ethereum.stackexchange.com/questions/64562/about-abi-encoder-v2



keccak_256在线计算https://emn178.github.io/online-tools/keccak_256.html



# replacement transaction underpriced 

price设置太高了，钱不够了