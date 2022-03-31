## 安装配置

```shell
# Mac安装
xcode-select --install
brew install openssl libffi autoconf automake libtool leveldb
brew install leveldb
pip install -e .'[dev]'	# 如果出现错误zsh: no matches found: .[dev]就用引号包起来
```

## 语法

```python
from web3 import Web3, HTTPProvider

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/YOUR_INFURA_KEY"))

调用智能合约
contract_address = Web3.toChecksumAddress(ERC20_CONTRACT_ADDRESS)
contract = web3.eth.contract(contract_address, abi=ABI)

print('ERC20 contract name: ' + contract.functions.name().call())
print('ERC20 contract symbol: ' + contract.functions.symbol().call())
```

