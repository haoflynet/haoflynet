## 安装配置

- 如果是使用`hardhat`，那么就不用单独安装了，它会安装指定的版本的`solc`的

```shell
brew update
brew upgrade
brew tap ethereum/ethereum
brew install solidity
```

## 语法

- 函数修饰符
  - view: 可是使用合约中的变量，只是在本地执行，不会消耗gas，不会修改合约状态(例如修改变量、触发事件等)
  - pure: 只能使用局部的变量，入参或者方法内部的变量，既不读取状态，也不改变状态，同样是本地执行，不会消耗gas
  - payable: 表示一个函数能够附加以太币调用，例如一些需要转账的函数
- 函数入参修饰符
  - memory: 表示这里是值传递
  - storage: 表示是指针传递
- 全局变量
  - block.number(uint): 当前区块号
  - block.timestamp(uint): 当前区块的时间戳，等同于now
  - Msg.sender(address): 消息发送者

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Token is ERC20 {	// 支持继承
		address public constant MY_ADDRESS = 0x.....;	// 产量可以消耗更低的gas


		// 继承的时候可以写新的构造函数，并且可以将新的构造函数中的参数传递给父类进行初始化
    constructor(uint256 totalSupply, string memory name, string memory symbol) ERC20(name, symbol) {
        _mint(msg.sender, totalSupply);
    }
    
    // 获取当前的sender
    function getMsgSender() public view returns(address) {
        return msg.sender;
    }
    
    function func1(unit amount) {
    	require(isAllowed[msg.sender], 'Caller not allowed to mint');	// 类似于断言，只有满足前面的条件才行，否则会报错
    	assert(amount > 123);	// 也是断言，但是没有报错信息
    }
}
```

## 智能合约代码库

### [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts)

- 相当于智能合约的标准仓库了，包含了经过社区审查的很多标准的智能合约源代码，不用重复造轮子了
- 测试也可以直接用仓库里面的tests下的测试文件，但是需要注意的是它是用`truffle`的语法来写测试的，如果用的是`hardtest`来运行测试用例，需要安装`hardhat-truffle5`插件，详情见[使用hardhat部署智能合约](https://haofly.net/hardhat)
- 比较常用的有:
  - ERC20：`@openzeppelin/contracts/token/ERC20/ERC20.sol`
- 安装完成后`npm install @openzeppelin/contracts`后可以直接在solidity中进行引入

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Token is ERC20 {
    constructor(uint memory totalSupply, string memory name, string memory symbol) ERC20(name, symbol) {
        _mint(msg.sender, totalSupply);
    }
}
```

### [Solidity by Example](https://solidity-by-example.org/)

- 也比较多的，但和上面那个比较来就比较逊色了

## TroubleShooting

- **Type literal_string "WALLET_ADDRESS" is not implicity convertiable to expected type address**: 我这边是将`balances["0x..."]`改为了`balances[0x...]`就可以了 
- **Please pass numbers as strings or BN objects to avoid precision errors**: 在solidity中，一般的数字都会要求使用字符串或者大数对象BN来表示，防止精度问题`web3.utils.toWei(String(123), 'ether')`
