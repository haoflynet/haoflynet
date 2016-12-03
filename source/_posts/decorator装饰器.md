---
title: "Python装饰器"
date: 2016-08-07 07:59:39
categories: python
---
# Python装饰器
装饰器就是一个函数，它接受其它函数为参数返回一个装饰过的函数，装饰器可用于静态方法、属性(@staticmethod)，在函数前后执行特定代码(比如，验证参数、给函数调用做缓存、注册回调函数、给函数打日志)

#### 最简单的装饰器:

	from functools import wraps
	def b(func):
		@wraps(func)
		def decorate(func):
			print('b')
			return func(canshu)	# 如果要传递参数可以在这里进行传递
		return decorate
		
	@b
	def a(canshu):
		print('a')
执行`a()`的时候会分别输出`b`和`a`，需要注意的是，这里不加wraps也是可以的，但是如果不加wraps，那么函数就真的相当于一个新的函数了，通过内省方法获取函数的元信息等都会变成新的，而如果wraps则会消除这样的影响。在flask中如果对views函数进行了装饰，不加wraps会出现这样的错误:

	AssertionError: View function mapping is overwriting an existing endpoint function: decorate
#### 使用类作为装饰器

被装饰的函数会作为实例化参数，得到一个类实例

```python
class LoginCheck:
    def __init__(self, f):
        self._f = f

    def __call__(self, *args):
        Status = check_function()
        if Status is 1:
            return self._f(*args)
        else:
            return alt_function()

def check_function():
    return test

def alt_function():
    return 'Sorry - this is the forced behaviour'

@LoginCheck
def display_members_page():
    print 'This is the members page'
```

### [应用场景](https://www.oreilly.com/ideas/5-reasons-you-need-to-learn-to-write-python-decorators?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+oreilly%2Fradar%2Fatom+%28O%27Reilly+Radar%29)：

1. 日志记录与分析
2. 数据验证(用户合法性校验、数据合法性校验)
3. 重复使用代码
