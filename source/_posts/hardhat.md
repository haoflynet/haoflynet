---
title: "使用hardhat部署智能合约"
date: 2022-03-21 18:00:00
categories: eth
---

- - 能够非常方便地编写、测试并部署智能合约到以太坊
- 内置了Hardhat Network，不用部署到真是的以太坊网络也能进行测试

## 安装配置

```shell
npm init --yes	# 如果当前目录还不是一个nodejs项目，先初始化
npm install --save-dev hardhat
npm install --save-dev @nomiclabs/hardhat-ethers ethers @nomiclabs/hardhat-waffle ethereum-waffle chai	# 安装一些测试需要用到的依赖

npx hardhat	# 初始化hardhat项目，会生成一个hardhat.config.js配置文件
```

<!--more-->

### 配置文件hardhat.config.js

```javascript
{
  require("@nomiclabs/hardhat-waffle");	// 注意这里一定要引入，否则测试会报错，默认的配置文件中没有这个

  /**
   * @type import('hardhat/config').HardhatUserConfig
   */
  module.exports = {
    solidity: "0.7.3",
    networks: {
      reposten: {	// 如果要部署到其他网络需要在这里定义
      	url: `https://eth-ropsten.alchemyapi.io/v2/${ALCHEMY_API_KEY}`,
      	accounts: [`0x${ROPSTEN_PRIVATE_KEY}`]
      },
      private: {
      url: 'http://127.0.0.1:8545',
      accounts: ['0x111111111']
      }
    }
  };
}
```

### 目录结构

```shell
.
├── artifacts	# 生成的build文件夹
├── contracts	# 存放智能合约源代码的目录
│   └── token.sol
├── scripts	# 存放部署脚本的目录
│   └── deploy.js
├── test	# 存放测试文件的目录
│   └── token.js
└──hardhat.config.js
```

## 使用hardhat

### 常用命令

- 编译目录artifacts中的信息与大多数的合约编译工具的输出是兼容的，例如`Truffle`

```shell
npx hardhat compile	# 编译合约，编译会编译到artifacts目录。默认只会编译更改后的
npx hardhat compile --force 	# 强制重新编译所有合约

npx hardhat test	# 运行测试
```

### 测试

- 一个测试用例`./test/token.js`

```javascript
const { expect } = require("chai");

describe("Token contract", function() {
  it("Test total supply to the owner", async function() {
    const [owner] = await ethers.getSigners();	// 这里只取了默认账户列表中的第一个账户，它也是默认的智能合约的owner

    const Token = await ethers.getContractFactory("Token");	// ContractFactory就是一个部署智能合约的工厂方法，这里并没有实际部署

    const myContract = await Token.deploy();	// 部署智能合约到hardhat本地的测试网络

    const ownerBalance = await myContract.balanceOf(owner.address);
    expect(await myContract.totalSupply()).to.equal(ownerBalance);
  });
});
```

### 部署

- 部署到指定的以太坊网络
- example: `./scripts/deploy.js`

```javascript
async function main() {

  const [deployer] = await ethers.getSigners();	// 这里取测试网络的第一个，当然也可以自己给一个地址
  
  console.log("Account balance:", (await deployer.getBalance()).toString());

  const Token = await ethers.getContractFactory("Token");
  const token = await Token.deploy();

  console.log("Token address:", token.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
```

编写完成后执行命令进行部署

```shell
npx hardhat run scripts/deploy.js	# 默认部署到hardhat本地的测试网络，当然成功后就没了
npx hardhat run scripts/deploy.js --network networkName	# 部署到指定的网络，这里的networkName是在hardhat.config.js中定义的
```

## 调用合约

- 根据我的使用，`artifacts`目录下的东西是编译后的东西，感觉有必要放到git repo中去，这样就不用存储abi到数据库了，而且代码也方便调用。每次部署相同的合约会得到一个不同地址，但编译后的合约肯定是一样的
- 最好存储一下abi信息到数据库，这样后面即使不用hardhat也能比较方便地调用合约方法

```javascript
const hre = require("hardhat");	// 以代码来执行deploy或者使用都是这个前缀

await hre.artifacts.getArtifactPaths()	// 获取工件文件的路径
await hre.artifacts.readArtifacts("contracts/Auction.sol:Auction")	// 获取指定合约的工件的内容

deployedContract = await hre.ethers.getContractAt("Auction", '0xaaaaaaa')	// 直接通过地址获取到部署的智能合约
deployedContract.customFunc()	// 直接调用合约的方法
```

## 参考文章

- [Hardhat新手教程](http://blog.hubwiz.com/2021/02/26/hardhat-beginner-tutorial/): 里面包含代币的完整测试用例