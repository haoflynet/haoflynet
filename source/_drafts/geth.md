## Go Ethereum

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
```

## 常用命令

- 创建的账号会生成一个json文件存储在`data/keystore`下

```shell
geth --datadir ./data account list	# 列出当前所有的account
geth --datadir ./data console	# 进入console

# console控制台命令
personal.newAccount()	# 创建账号
personal.unlockAccount('0x111')	# 解锁账号d

eth.accounts	# 获取当前节点所有的账户信息
eth.getBalance(eth.accounts[0])		# 获取某个账户的balance
user1 = eth.accounts[1]	# 在当前console为账户设置别名

admin.nodeInfo	# 获取当前节点信息
admin.peers	# 获取peer节点信息
net.peerCount	# 获取节点数量
eth.blockNumber	# 查看当前区块数量
eth.getTransaction()

miner.setEtherbase(base)
miner.start(1)	# 执行挖矿操作，参数是线程数
```

### 转账

- Wei是以太坊中的最小货币面额单位，1 ether = 10^18 Wei

```shell
personal.unlockAccount('0x111111')	# 转账钱需要先解锁账号
eth.sendTransaction({from: '0x1111111', to: '0x2222222', value: web3.toWei(2, "ether")})	# 此时暂时看不到余额变化，因为此时交易还没有上链
eth.sendTransaction({from: eth.accounts[0], to: eth.accounts[1], value: web3.toWei(1, "ether")})

miner.start(1)	# 需要执行一次挖矿操作
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
       "timestamp": "0x0",
       "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
       "extraData": "0x00",
       "gasLimit": "0x8000000",	// 执行智能合约的最大值
       "difficulty": "0x1",	// 挖矿的复杂度，越低挖得越快
       "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
       "coinbase": "0x3333333333333333333333333333333333333333",
     	"extradata": "0x00000000000000000000000000000000000000000000000000000000000000007df9a875a174b3bc565e6424a0050ebc1b2d1d820000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",	// 将中间的地址替换为first singer的public address即可，这个好像可以随便填
       "alloc": {	// 预先分配balance到特定的地址，默认留空就可以了，当然也可以给某个address直接制定
         "7df9a875a174b3bc565e6424a0050ebc1b2d1d82": {"balance": "10000"}
       },
       "config": {
         "chainId": 15,	// 当前私有区块链的唯一id，如果是私有倒无所谓，如果要上公链必须唯一，可以去https://chainlist.org 确认
         "homesteadBlock": 0,	// 第一次发布时的区块，默认为0就行
         "eip150Block": 0,
         "eip155Block": 0,	// eip表示Ethereum Improvement Proposals，私有链的话默认为0即可
         "eip158Block": 0 // 私有链默认为0即可
       }
   }
   ```

4. 初始化创世块，如果后续有啥不顺的，可以直接将data下的geth目录和history移除，重新初始化并创建创世块

   ```shell
   geth init --datadir ~/data ~/config/genesis.json
   
   # 如果已经初始化了，可以执行下面命令来启动
   geth --datadir data --networkid 15
   
   rm -rf data/geth data/history ~/.ethash
   ```

5. 启动以太坊私有测试链

   - 这里需要用到服务器的公网IP地址，并且需要将服务器的防火墙允许UDP和TCP的30303端口

   ```shell
   geth --identity "FirstNode" --datadir data --networkid 15 --nat extip:172.16.254.4 console	# 这里的console能够直接进入控制台
   # 其他参数
   --maxpeers 0: 节点数最大值
   --nodiscover: 使节点不可发现，可以防止使用相同network id和创世块的节点连接到你的区块链网络中，只能手动添加节点
   
   # 然后需要另启一个终端，执行下面命令获取引导节点bootstrap node
   geth attach data/geth.ipc --exec admin.nodeInfo.enr
   ```

6. 创建另外的节点

   - 注意必须使用相同的创世块配置
   - 如果是同一个机器上，需要创建不同的data目录
   - 这里的创世块enoce信息，可以在初始节点的console中通过`admin.nodeInfo`获取到

   ```shell
   geth --datadir data2 init ~/config/genesis.json	# 同样需要先初始化
   geth --datadir data2 --networkid 15 --port 30305 --bootnodes "enode://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@172.16.254.4:30303"
   
   # 启动完成后在另一个终端执行下面命令查看是否连接上初始节点
   geth attach data2/geth.ipc --exec admin.peers
   ```

   