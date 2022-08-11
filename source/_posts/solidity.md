---
title: "Solidity 开发手册"
date: 2022-07-26 12:02:30
updated: 2022-08-01 12:00:00
categories: system
---

## 安装配置

- 开发IDE: 我一般就直接用idea了，有solidity插件，但是以太坊有一个官方的IDE: [remix](https://remix.ethereum.org/)

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
- 变量分类，注意每个变量在声明时都会有一个对应其类型的默认值，没有空值null的概念
  - 状态变量：变量值会一直保存在合约的存储空间中
  - 局部变量：仅在函数执行过程中有效，函数退出后就无效了
  - 全局变量：保存在全局命名空间中的变量，用于获取区块链相关信息
  
- 内置全局变量
  - block.number(uint): 当前区块号
  - block.timestamp(uint): 当前区块的时间戳，等同于now
  - block.gaslimit(uint): 当前区块的gaslimit
  - msg.sender(address): 消息发送者
  - msg.value(uint): 当前消息的wei值
  - now: 当前区块的时间长
  - tx.gasprice(uint): 当前transaction的gas价格
  - tx.origin(address payable): 当前交易的发送者地址

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Token is ERC20 {	// 支持继承
		IERC20 token;
		
		uint256 override amount; 
		
		struct Transaction {	// 创建一个结构体类型
			address user;
			uint timestamp;
		}
		Transaction[] transactions;	// 数组对象
		
		mapping (address => uint256) public investors; // mapping对象，可以用于记录key value的数据

		address public constant MY_ADDRESS = 0x.....;	// 产量可以消耗更低的gas

		// 继承的时候可以写新的构造函数，并且可以将新的构造函数中的参数传递给父类进行初始化
    constructor(uint256 totalSupply, string memory name, string memory symbol, address _anotherToken) ERC20(name, symbol) {
        _mint(msg.sender, totalSupply);
        token IERC20(anotherToken);	// 将另外一个合约作为参数传递进来
        
        
        transactions.push(
        	Transaction('xx', 'bbb')	// 结构体的初始化
        );	// 数组默认有一个push方法
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

<!--more-->

## 常用智能合约概念

### ERC20

### ERC721

- 非同质化代币(NFT)

- 标准方法：

  - balanceof(address _owner): 只是返回账户拥有的NFT的数量
  - ownerOf(uint256 _tokenId): 获取指定NFT token所属的账户地址
  - safeTransferFrom: 将NFT从一个地址转移到另一个地址，from必须是自己的账户地址
  - transferFrom
  - approve：更改或者确认NFT的授权地址，授权将某个NFT转移到另一个账户
  - setApprovalForAllgetApproved
  - isApprovedForAll

- 标准事件

  - Transfer: 当NFT的所有权改变时触发该事件

  - Approval：当更改或确认NFT的授权地址时触发

    

## 智能合约代码库

### [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts)

- 相当于智能合约的标准仓库了，包含了经过社区审查的很多标准的智能合约源代码，不用重复造轮子了
- 测试也可以直接用仓库里面的tests下的测试文件，但是需要注意的是它是用`truffle`的语法来写测试的，如果用的是`hardtest`来运行测试用例，需要安装`hardhat-truffle5`插件，详情见[使用hardhat部署智能合约](https://haofly.net/hardhat)
- 比较常用的有:
  - ERC20：`@openzeppelin/contracts/token/ERC20/ERC20.sol`
- 安装完成后`npm install @openzeppelin/contracts`后可以直接在solidity中进行引入
- 提供了很多的帮助功能
  - Ownable：增加管理员的管理功能，可以直接给方法添加onlyOwner即可实现只有管理员能够执行的方法

```solidity
//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC20Token is ERC20, Ownable {
		AnotherContract anotherContract;	// 可以声明另外一个contract，这样可以在方法里面直接调用它的方法

    constructor(string memory name, string memory symbol, address initialHolder, uint256 initialSupply) ERC20(name, symbol) {
        _mint(initialHolder, initialSupply);
    }

    function mint(address account, uint256 amount) public onlyOwner {
        _mint(account, amount);
    }
}

```

### [Solidity by Example](https://solidity-by-example.org/)

- 也比较多的，但和上面那个比较来就比较逊色了

## TroubleShooting

- **Type literal_string "WALLET_ADDRESS" is not implicity convertiable to expected type address**: 我这边是将`balances["0x..."]`改为了`balances[0x...]`就可以了 
- **Please pass numbers as strings or BN objects to avoid precision errors**: 在solidity中，一般的数字都会要求使用字符串或者大数对象BN来表示，防止精度问题`web3.utils.toWei(String(123), 'ether')`
- **Function has override specified but does not override anything**: override的时候参数多一个少一个居然报的是这个错误
