web3的前端库，目前就这几个库，https://wagmi.sh/docs/comparison



## 安装配置

- client用于管理连接状态和配置

```javascript
import { WagmiConfig, createClient } from 'wagmi'

const client = createClient()

function App() {
  return (
    <WagmiConfig client={client}>
      <YourRoutes />
    </WagmiConfig>
  )
}
```

- createClient的其他配置

```javascript
const client = createClient({
  autoConnect: true,	// 自动连接上一次连接的网络，默认为false,
  connectors: [	// 用于管理钱包的连接，默认为[new InjectedConnector()]
    new InjectedConnector(),
    new WalletConnectConnector({
      options: {
        qrcode: true,
      },
    }),
  ],
  provider(config) {	// 用于管理连接的链，默认值为(config) => getDefaultProvider(config.chainId)
    return new providers.AlchemyProvider(config.chainId, 'Your Alchemy ID')
  },
  storage: createStorage({ storage: window.localStorage }),	// 存储策略，默认用的是window.localStorage
  webSocketProvider(config) { // webSocketProvider才使用
    return new providers.AlchemyWebSocketProvider(
      config.chainId,
      'Your Alchemy ID',
    )
  },
})
```

- configureChains直接配置链

```javascript
import { chain, configureChains } from 'wagmi'
import { jsonRpcProvider } from 'wagmi/providers/jsonRpc'

const { chains, provider } = configureChains(
  [chain.mainnet, chain.polygon],
  [
    jsonRpcProvider({
      rpc: (chain) => ({
        http: `https://${chain.id}.example.com`,
      }),
    }),
  ],
)
```



## hooks

### useConnect

- 连接钱包

```javascript
const {
  activeConnector,
  connect,
  connectors,
  error,
  isConnecting,
  pendingConnector
} = useConnect({
  connector: new InjectedConnector(),
})

<button onClick={() => connect()}>Connect Wallet</button>
```

### useAccount

- 获取account相关信息

```javascript
const { data: {address} } = useAccount()
account.address // 钱包地址
```

### useBalance

-  查询account的balance

```javascript
const { data: {formatted, symbol, decimals, value}, isError, isLoading } = useBalance({
    addressOrName: '0xabcdiahgoihdsiog',
  	chainId: 1,	// 可选，指定chainId
  	formatUnits: 'gwei', // 可选，指定单位，wei、kwei、mwei、gwei、szabo、finney、ether
  	token: '0xxaadsgiahigohoaigh', // 指定erc20的contract地址，可以直接获取到相应的token
  	watch: true,	// 当有新的blocks的时候自动更新数据
  	cacheTime: 2_000, // 缓存时间，默认为0
})
```

### useToken

- 获取token

```javascript
 const { data, isError, isLoading } = useToken({
    address: '0xc18360217d8f7ab5e7c516566761ea12ce7f9d72',
  })
```

### useSendTransaction

- 发送transaction

```javascript
const { data, isIdle, isError, isLoading, isSuccess, sendTransaction } =
    useSendTransaction({
      request: {
        to: 'awkweb.eth',
        value: BigNumber.from('1000000000000000000'), // 1 ETH
      },
    })
```

### useWaitForTransaction

- 查询transaction

```javascript
 const { data, isError, isLoading } = useWaitForTransaction({
    hash: '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',
  })
```

### useContract

- 获取智能合约

```javascript
const contract = useContract({
    addressOrName: '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e',
    contractInterface: ensRegistryABI,
  })
```

### useContractEvent

- 监听contract的事件

```javascript
useContractEvent(
    {
      addressOrName: '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e',
      contractInterface: ensRegistryABI,
    },
    'NewOwner',
    (event) => console.log(event),
  )
```

### useContractRead

- 调用智能合约的只读接口

```javascript
const { data, isError, isLoading } = useContractRead(
    {
      addressOrName: '0xecb504d39723b0be0e3a9aa33d646642d1051ee1',
      contractInterface: wagmigotchiABI,
    },
    'getHunger',
  	{ // 第三个参数可选，可以指定函数的参数
      args: '0xA0Cf798816D4b9b9866b5330EEa46a18382f251e',
    },
  )
```

### useContractWrite

- 调用智能合约的写接口

```javascript
const { data, isError, isLoading, write } = useContractWrite(
    {
      addressOrName: '0xecb504d39723b0be0e3a9aa33d646642d1051ee1',
      contractInterface: wagmigotchiABI,
    },
    'feed',
  )
```

### useSinger

- 获取签名

```javascript
const { data: signer, isError, isLoading } = useSigner()

const contract = useContract({
  addressOrName: '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e',
  contractInterface: ensRegistryABI,
  signerOrProvider: signer,
})
```

### useSignMessage

- 对消息进行签名

```javascript
const { data, isError, isLoading, isSuccess, signMessage } = useSignMessage({
    message: 'gm wagmi frens',
  })
```

### useSignTypedData

- 签名typed data

### useBlockNumber

- 查询blockNumber
### useProvider

- 获取provider

### useDisconnect

### useNetwork

- 切换网络

### useEnsName

```javascript
const { data: ensName } = useEnsName({ address: account.address })
```

### useEnsAvatar

### useEnsResolver

### useFeeData

- 获取网络的fee信息

### useWebSocketProvider

