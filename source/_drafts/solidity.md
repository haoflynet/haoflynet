## 语法

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Token is ERC20 {	// 支持继承
		// 继承的时候可以写新的构造函数，并且可以将新的构造函数中的参数传递给父类进行初始化
    constructor(uint256 totalSupply, string memory name, string memory symbol) ERC20(name, symbol) {
        _mint(msg.sender, totalSupply);
    }
}
```

## 智能合约仓库

### [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts)

- 相当于智能合约的标准仓库了，包含了经过社区审查的很多标准的智能合约源代码，不用重复造轮子了
- 但是这里面的测试方法看起来挺全面，但是不方便拿来用，得改一些东西，有点儿麻烦
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

- 也比较多的
