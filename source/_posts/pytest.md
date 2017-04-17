---
title: "python测试教程，pytest的使用"
date: 2015-09-07 3:12:30
updated: 2017-03-13 15:34:00
categories: python
---
## Python自带和测试相关的功能

```python
assert 1=1	# 直接断言
```

# pytest

Python的测试类，调研了一下nose和pytest，虽然nose的使用量确实比pytest多一点，但是活跃度并不高，从15年后就没发布新版本了，而pytest的github还在一直刷。所以选择了pytest来学习python的测试。

#### 单元测试原则：分离、简单，两个测试用例不能有任何依赖

## 常用方法

```python
# 测试类有如下几个特殊方法
setup_class 	# 测试类开始的时候执行
teardown_class	# 测试类结束的时候执行
setup/setup_method			# 每个测试方法开始的时候执行
teardown/teardown_method	# 每个测试方法结束的时候执行
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
