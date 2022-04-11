Mocha是一个测试库，通常搭配`chai`一起使用，`chai`是一个帮助测试的库，里面包含了很多测试用的功能

## 命令参数

```shell
mocha --bail	# 只要有一个测试没通过就停止后面的测试
mocha --grep "abc"	# 搜索测试用例的名称(it块的字符串)，只执行匹配的测试用例
mocha --grep "abc" --invert	# 只执行不满足这个条件的测试
mocha -t 2000 test.js	# 设置超市时间
```

## Mocha

```javascript
describe('Test my code', function () {
  let globalVar;
  
  before(function () {	// 在本区块的所有测试用例之前执行
    
  })
  after(function(){})
  
  beforeEach(async function () {	// 在本区块的每个测试用例之前执行
    globalVar = await ...
  })
  
  afterEach(function() {})
  
  // describe可以包含1个或者多个it块或者describe块
  describe("Test my function", function () {
    // it测试块是最小的测试单元，测试用例
    it('input 1', function() {
      
    })
    
    it('input 2', function() {
      
    })
  })
})
```

## Chai断言库

```javascript
// 判断是否相等
expect(2 + 2).to.equal(4)
expect(2 + 2).to.not.equal(4)
expect({a: 'b'}).to.not.equal({a: 'b'})
expect({a: 'b'}).to.deep.equal({a: 'b'})

// 布尔值/空值
expect('abc').to.be.ok
expect(false).to.not.be.ok
expect(undefined).to.not.be.ok
expect(null).to.not.be.ok
expect(true).to.be.true
expect(1).to.be.true
expect(0).to.be.false
expect(null).to.be.null
expect(undefined).not.to.be.null
expect(null).to.not.be.undeinfed
expect(4).not.to.be.NaN
expect([]).to.be.empty
expect('').to.be.empty

// 是否包含
expect([1,2,3]).to.include(2)
expect('foobar').to.contain('foo')
expect('foobar').to.match(/foo/)
expect({foo: 'bar'}).to.include.keys('foo')

// 类型判断
expect(obj).to.be.an.instanceOf(Obj)

// 错误判断，但是这种只能用于同步的函数
expect(fn).to.throw(Error)
// 异步的错误判断就只能这样了
let err
try {
  await fn()
} catch (error) {
  err = error
}
except(err).to.be.an(Error.name)
```










```




"test-lib": "export NODE_ENV=test && mocha --require ts-node/register src/lib/*.test.ts" --timeout 2000000 # 默认只有2000ms
```

```
import { expect } from 'chai'
```

```
expect(typeof response.multicastId).to.equal('number')
```

