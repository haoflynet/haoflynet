- ERC20是以太坊中的一种代币标准，只要遵循这个标准，任何与ERC20兼容的软件都能轻松管理你的代币。

- 这里的代币在英文世界一般就叫`Token`

- 它遵循着这样的标准
  - 代币的总量在初始化的时候决定，后期无法更改
  - 任何人都可以接受代币，只要是个合法的地址，无论这个地址是否被某个人拥有
  - 只要拥有代币就能转代币给别人

详细代码如下:

```solidity
pragma solidity ^0.7.0;

library SafeMath {
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}

contract Token {
    string name_;	// 代币的名字
    string symbol_;	// 代币的符号，简称
    uint8 decimals_;	// 支持到小数点的后几位
    uint256 totalSupply_;	// 发行代币的总量

    using SafeMath for uint256;

    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;

    // 初始化，并把初始化的发行数量分配给拥有者
    constructor(
        // string memory name,
        // string memory symbol,
        // uint8 decimals,
        // uint256 totalSupply
    ) public {
        // name_ = name;
        // symbol_ = symbol;
        // decimals_ = decimals;
        // totalSupply_ = totalSupply;
        // balances[msg.sender] = totalSupply;
        name_ = "dog bi";
        symbol_ = "dogs";
        decimals_ = 18;
        totalSupply_ = 10000000000000000000;
        balances[msg.sender] = 10000000000000000000;
        // balances[0x111111] = 10000000000000000000; // 也可以直接指定地址
    }

    function name() public override view returns (string memory) {
        return name_;
    }

    function symbol() public override view returns (string memory) {
        return symbol_;
    }

    function decimals() public override view returns (uint8) {
        return decimals_;
    }

    function totalSupply() public override view returns (uint256) {
        return totalSupply_;
    }

		// 获取该地址代币的余额
    function balanceOf(address _owner)
        public
        override
        view
        returns (uint256 balance)
    {
        return balances[_owner];
    }

		// 将自己的token转账给_to地址，_value为转账个数
    function transfer(address _to, uint256 _value)
        public
        override
        returns (bool success)
    {
        // 检查发送者账户余额是否足够
        require(_value <= balances[msg.sender]);
        // 发送者减少余额
        balances[msg.sender] -= _value;
        // 接受者增加余额
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

		 // 与approve搭配使用，approve批准之后，调用transferFrom函数来转移token
    function transferFrom(
        address _from,
        address _to,
        uint256 _value
    ) public override returns (bool success) {
        // 检查发送者的余额是否足够
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);
        balances[_from] -= _value;
        allowed[_from][msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

		// 批准_spender账户从自己的账户转移_value个token。可以分多次转移
    function approve(address _spender, uint256 _value)
        public
        override
        returns (bool success)
    {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

		// 返回_spender还能提取token的个数
    function allowance(address _owner, address _spender)
        public
        override
        view
        returns (uint256 remaining)
    {
        return allowed[_owner][_spender];
    }
}

```

