Mocha是一个测试库，通常搭配`chai`一起使用，`chai`是一个帮助测试的库，里面包含了很多测试用的功能

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










```




"test-lib": "export NODE_ENV=test && mocha --require ts-node/register src/lib/*.test.ts" --timeout 2000000 # 默认只有2000ms
```

```
import { expect } from 'chai'
```

```
expect(typeof response.multicastId).to.equal('number')
```

