---
title: "python单元测试"
date: 2015-09-07 3:12:30
updated: 2019-08-19 17:19:00
categories: python
---
## pytest

Python的测试类，调研了一下nose和pytest，虽然nose的使用量确实比pytest多一点，但是活跃度并不高，从15年后就没发布新版本了，而pytest的github还在一直刷。所以选择了pytest来学习python的测试。

### 常用命令

```python
pytest test.py		# 测试脚本
pytest -x					# 当第一次出现失败的时候就停止测试
pytest --maxfail=2	# 设置最大失败次数
```

### 测试类

```python
class TestName:	# 测试类必须以Test开头
  def setup_class(self):
    """测试类开始的时候执行，相当于__init__"""
  def teardown_class(self):
    """测试类结束的时候执行，相当于__del__"""
  def setup_method(self):
    """每个测试方法开始的时候执行"""
  def teardown_method(self):
    """每个测试方法结束的时候执行"""
  def test_one(self):	# 测试方法必须以test_开头
    assert 1 is 2
    
    with pytest.raises(MyException) as e:	# 断言下面的语句会抛出指定的错误
      x = 1/1
```

## mock对象
mock确实是用来代替我们的测试对象。表面上看，用了mock那还干嘛要测试，其实，不明白的原因是mock的应用场景并不是单纯地代替测试对象，而是代替的那些在当前测试用例并不十分必要，而且该测试对象耗时或者不稳定，和我们真正要测试的代码逻辑无关，那么久可以使用mock来模拟该对象的返回值，实现我们真正想要的测试用例。比如我们现在是要测试函数b，但是函数b却依赖函数a，我们在这里并不关心a，只需要拿到它的返回值而已，所以可以用mock来模拟，以防止a函数本身可能发生的不稳定、耗时等现象。  
另外，mock还可以用来保存几个测试用例的全局变量(要说的话，几个测试用例之间是不能有依赖的，只是我现在的场景是需要登录一个网站然后测试里面的功能，只能用mock来保存cookies)pytest测试类是不能更改类变量的。比如：

	class TestClass:
		var1 = '123'
		mock = mock.Mock()
		
		def testLogin(self):
			r = requests.post(url, data={})
			self.mock.cookies.return_value = r.cookies.items()
		def testFun(self):
			r = request.get(url, cookies=self.mock.cookies())
