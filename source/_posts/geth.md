---
title: "Geth 搭建私链 private blockchain"
date: 2022-03-18 18:00:00
updated: 2022-06-30 18:34:00
categories: eth
---

## Go Ethereum

- 对于RPC端口，如果实在得暴露到公网，其实也没啥，注意不要在network里面创建账户，即使有也要把私钥放到其他地方物理隔离，当然换端口以及防火墙也是基本操作。也可以在nginx层添加一个HTTP basic Auth认证。网上很多黑客一直在扫30303和8545端口

## 安装配置

```shell
# macos
brew tap ethereum/ethereum
brew install ethereum

# ubuntu
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum
curl -LSs https://raw.githubusercontent.com/gochain/web3/master/install.sh | sh	# 安装web3 CLI
```

## 常用命令

- 直接在节点上创建的账号会生成一个json文件存储在`data/keystore`下

```shell
geth --datadir ./data account list	# 列出当前所有的account
geth --datadir ./data console	# 进入console

# console控制台命令
personal.newAccount('password')	# 创建账号
personal.unlockAccount('0x111')	# 解锁账号d

eth.accounts	# 获取当前节点所有的账户信息
eth.getBalance(eth.accounts[0])		# 获取某个账户的balance
user1 = eth.accounts[1]	# 在当前console为账户设置别名

admin.nodeInfo	# 获取当前节点信息
admin.peers	# 获取peer节点信息
net.peerCount	# 获取节点数量
eth.blockNumber	# 查看当前区块数量
eth.getTransaction()
eth.pendingTransactions	# 获取当前所有pending的transaction
eth.coinbase	# 获取当前的矿工

miner.setEtherbase(base)
miner.start(1)	# 执行挖矿操作，参数是线程数

web3 account extract --keyfile data/keystore/UTC--2022-03-16T02-29-14.506737237Z--XXXXXXXX --password XXXXXXXX # 获取在当前网络上创建的账户的私钥

txpool.status # 查看当前pending和queued的transaction的状态
```

<!--more-->

### 转账操作

- Wei是以太坊中的最小货币面额单位，1 ether = 10^18 Wei

```shell
personal.unlockAccount('0x111111')	# 转账前需要先解锁账号
eth.sendTransaction({from: '0x1111111', to: '0x2222222', value: web3.toWei(2, "ether")})	# 此时暂时看不到余额变化，因为此时交易还没有上链

miner.start(1)	# 需要执行一次挖矿操作，让矿工来打包确认
miner.stop()	# 就能发现余额发生变化了
```

## 搭建私有链private blockchain

1. 新建目录

   ```shell
   mkdir ~/config	# 配置目录
   mkdir ~/data	# 数据目录
   ```

2. 创建第一个账户方便测试，记录下public address和secret key file地址，可以给它初始化balance。后面也可以用这条命令创建更多的测试账户

   ```shell
   geth account new --datadir data
   ```

3. 首先配置一个初始块(initial block)/创世块(Genesis Block)

   ```json
   // vim ~/config/genesis.json
   {
       "nonce": "0x0000000000000042",
       "timestamp": "0x0",	// 设置创世块的时间戳
       "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",	// 上一个区块的hash，创世块的话就为0
       "extraData": "0x00",	// 附加信息，随便写就行了
       "gasLimit": "0x8000000",	// 设置对GAS的消耗总量限制，用来限制区块能包含的交易信息总和，执行智能合约的最大值
       "difficulty": "0x0",	// 挖矿的复杂度，越低挖得越快，不过经过我的测试，在aws的
       "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
       "coinbase": "0x3333333333333333333333333333333333333333",	// 矿工的账号，随便填
       "alloc": {	// 预先分配balance到特定的地址，默认留空就可以了，当然也可以给某个address直接制定
         "7df9a875a174b3bc565e6424a0050ebc1b2d1d82": {"balance": "10000"}
       },
       "config": {
         "chainId": 202203101600,	// 当前私有区块链的唯一id，如果是私有倒无所谓，如果要上公链必须唯一，可以去https://chainlist.org 确认
         "homesteadBlock": 0,	// 第一次发布时的区块，默认为0就行
         "eip150Block": 0,
         "eip155Block": 0,	// eip表示Ethereum Improvement Proposals，私有链的话默认为0即可
         "eip158Block": 0, // 私有链默认为0即可
         "byzantiumBlock": 0,
         "constantinopleBlock": 0,
         "petersburgBlock": 0,
         "istanbulBlock": 0
       }
   }
   ```

4. 初始化创世块，如果后续有啥不顺的，可以直接将data下的geth目录和history移除，重新初始化并创建创世块

   ```shell
   geth init --datadir ~/data ~/config/genesis.json
   
   # 如果已经初始化了，可以执行下面命令来启动
   geth --datadir data --networkid 15
   ```
   
5. 启动以太坊私有测试链

   - 这里需要用到服务器的公网IP地址，并且需要将服务器的防火墙允许UDP和TCP的30303端口
   - 如果开启了RPC服务，那么每个人都能够访问你的节点，最好还是关闭了。虽然有unlockAccount的存在，但是如果输入密码短时间内不会再次要求输入密码，黑客会不断尝试转账交易。目前能做的主要有更换端口，设置访问墙，nginx http basic auth。
   -  API支持HTTP-RPC，WS-RPC，GraphQL(基于HTTP-RPC)
   - 如果开启了graphql可以直接访问`http://ip:8545/graphql/ui`，但是实际看感觉graphql的api不全呀，就只能查一些区块的东西，contract的基本不支持，这应该是目前的支持列表[EIP-1767](https://eips.ethereum.org/EIPS/eip-1767)

   ```shell
   geth --identity "FirstNode" --nodiscover --datadir data --allow-insecure-unlock --http --http.addr "0.0.0.0" --http.corsdomain '*' --http.api "eth,net,web3,personal" --graphql --graphql.corsdomain '*' --nat extip:172.168.254.4 --networkid 202203101600 console	# 这里的console能够直接进入控制台
   # 参数列表，注意网上很多教程的rpc现在已经被http替代了
   --identity "First"	# 自定义节点名称
   --networkid 123	# 设置network的id
   --nat extip:172.16.254.4	# 将当前节点暴露到公网
   --maxpeers 0: 节点数最大值
   --nodiscover: 使节点不可发现，可以防止使用相同network id和创世块的节点连接到你的区块链网络中，只能手动添加节点
   --nousb: 关闭USB硬件钱包
   --allow-insecure-unlock	# 允许通过HTTP-RPC来解锁account，是一个比较危险的操作，建议不开启，只有测试的时候可以开启一下
   --http.api	admin.debug,web3,eth,txpool,personal,ethash,miner,net	# 支持哪些http api
   --http.corsdomain '*'	# 允许哪些域名能够跨于连接
   --http.vhosts '*'	# 允许用哪些域名访问当前的network

   # 然后需要另启一个终端，执行下面命令获取引导节点bootstrap node
   geth attach data/geth.ipc --exec admin.nodeInfo.enr
   ```

6. 创建另外的节点(member节点)

   - 注意必须使用相同的创世块配置
   - 如果是同一个机器上，需要创建不同的data目录
   - 这里的创世块enoce信息，可以在初始节点的console中通过`admin.nodeInfo`获取到

   ```shell
   geth --datadir data2 init ~/config/genesis.json	# 同样需要先初始化
   geth --datadir data2 --networkid 15 --port 30305 --bootnodes "enode://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@172.16.254.4:30303"
   
   # 启动完成后在另一个终端执行下面命令查看是否连接上初始节点
   geth attach data2/geth.ipc --exec admin.peers
   ```


## TroubleShooting

- **客户端报错the method xxx does not exist/is not available**: 需要将要使用的api添加到`--http.api`参数中，例如`--http.api "eth,web3,personal,miner"`

- **Error: invalid opcode: SHR**: 需要在创世块配置里面加上

  ```
  "byzantiumBlock": 0,
  "constantinopleBlock": 0
  ```

- **移除所有pending的transaction**: 删除`data/geth/transactions.rlp`，然后重启geth服务端，注意queued的transaction不会清除，nonce从0开始，导致queud队列中的一直执行不了，此时只需要把中间空白的nonce值补齐就行(创建transaction)

- **invalid host specified**: 可能是在运行network的时候没有指定hosts，参考上面的配置