---
title: "Python教程"
date: 2016-12-20 12:05:30
updated: 2018-03-29 17:44:30
categories: python
---
[Python Developer’s Guide](http://cpython-devguide.readthedocs.io/en/latest/#python-developer-s-guide)

##  安装方法

```shell
# for CentOS
yum groupinstall -y 'development tools'
yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel xz-libs
# for Ubuntu
apt-get install -y build-essential libssl-dev

# Linux下不区分64和32位
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz	
xz -d Python-3.6.0.tar.xz && tar -xvf Python-3.6.0.tar && cd Python-3.6.0
# for Linux
./configure && make && sudo make altinstall	
# for Mac
./configure --enable-framework --with-openssl=/usr/local/opt/openssl	# 不加openssl可能会出现the SSL module is not available的错误
cd

# 如果默认没有安装pip，那么可以这样安装
wget https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

# Python3.5版本默认有安装pip的，如果没有，那么就酱紫
wget https://bootstrap.pypa.io/get-pip.py
python3.3 get-pip.py
```

## 基本语法

<!--more-->

#### 列表

```python
all([])	# 判断列表里面是否所有的值都为1
any([])	# 判断列表里面是否有值都为1

li[10:]		# 如果切片超过了列表的索引范围，并不会报错，仅仅是返回空列表而已
li[::-1]	# 逆序列表
li[::2]		# 列表里面的奇数位，最后那个2表示不长，前面::表示整个数组
li[1::2]	# 列表里面的偶数位
del(list['下标'])	# 删除指定位置的元素，要注意每次都会更新，比如del(list[0], list[0])就是删除前面两个元素
li.index(min(li))	# 列表最小值，返回位置，最大用max
li.index(obj)		# 获取指定值在数组里面的下标
li.remove(obj)	# 删除指定元素

# while/for循环都能用else，我擦嘞
while false:
	sdaghoahg
else:
	aosdhgo

for x in reversed(list) # 列表的反向迭代
for index, value in enumerate(list)	# 遍历的时候带上序号
list(set(list))  # 列表去重，不过会乱序
li.insert(position, item)	# 在列表指定位置插入一个元素
li.append([1,2])	# 添加一个元素
li.extend([1,2])	# 添加多个元素
li_1 + li_2			# 列表相加，例如[1] + [2] = [1, 2]

A.T @ A			# @矩阵乘法

[x*x for x in range(10)]	# 列表推导，得到的是一个数组
(x*x for x in range(10))	# 列表推导，得到的是一个迭代器
```
#### 字符串

```python
# hash值计算，使用hashlib库，其中有sha256/md5等。base64是一个单独的库
```

#### 字典

```python
# 字典遍历
for key in dict:
	print(key, dict[key])
for key, vlaue in dict.items():
	print(key, value)
	
# 特殊的key
li = {
	'a': 'b',
	None: 'c',
	'': ''
}

if 'a' in dict		# 判断key是否存在
dict.get('a', 'b')	# 如果不存在那么给一个默认值
dict.keys()			# 获取所有的key，这里返回的是一个dict_keys，一个迭代器
list(dict)			# 如果仅仅想获得key的数组，可以这样子

# 表达式解析
a = {'x': 1, 'y': 2}
globals().update(a)
print(x, y)

# 漂亮地打印json数据
print(json.dump(sdata, indent=2))

# 有序字典(占用的内存是普通字典的两倍)
from collections import OrderedDict
d = OrderedDict()

# 字典组成的列表排序
通过某个关键字来排序
rows = [{}, {}]  # 假设这是一个由字典组成的列表
from operator import itemgetter
result = sorted(rows, key=itemgetter('onekey'))	# 更复杂的用法可以参见本文下面的sorted方法
通过某个值排序，使用zip()函数，它会先将键和值翻转过来，需要注意的是zip()函数是一个只能访问一次的迭代器
prices = {'A': 1, 'B': 2, 'C': 3}
min_price = min(zip(prices.values(), prices.keys()))  # 获取value最小的
prices_sorted = sorted(zip(prices.values(), prices.keys()))
for a, b in zip(x, y) # 多个列表同时迭代，让长度取决于最短的那一个,这样就不会超出长度
# 字典合并（ChainMap只是将两个字典在逻辑上变为一个，在它上面的修改只会影响第一个字典a)
from collections import ChainMap
c = ChainMap(a, b)

# 要想一个对象继承与一个字典，并且能用json.dumps()转换为json对象，那么可以这样做
class ErrorMsg(dict):
    """自定义错误类"""
    def __init__(self, e: Exception, code: int):
        dict.__init__(self, msg=str(e), code=code)
json.dumps(ErrorMsg(e, 200))	# {"msg":"xxx", "code":200}

# 字典列表的筛选，直接用filter
filter(lambda person: person['name'] == 'haofly', people_list)	# 不过有个缺点，就是不能传值进lambda，不然就直接用以下这种方法吧
[person for person in people_list if person['name'] = name]

# 字典推倒式
d = {key: value for (key, value) in iterable}
```
#### 类/函数

- 定义在`__init__`外的属性相当于静态变量，所有对象公用，`__init__`内部的才是对象私有的

```python
# 几个特殊的方法
x.__class__.__name__  # 获取实例的类名

# 继承相关
ChildClass.mro()	# 按顺序打印类当前类的继承顺序，多继承也会有顺序
super().func()	# 调用父类的方法
super(ChildClass, self).func()	# 2里面调用父类的方法

# 通过字符串调用方法
getattr(foo, 'bar')()	# 第一个参数可以是一个module
hasattr(foo, 'bar')	# 判断对象是否有某个属性

# lambda表达式，相当于一个简单的函数，例如:
g = lambda x: x*2
g(3) # 输出6

# 自定义Beans，类似Java Beans，将字典直接转换为对象的形式，例如
from collections import namedtuple
UserResponse = namedtuple('UserResponse', [
  'uid',
  'name'
])

# 定义静态方法
@staticmethod
def get():
    pass
# 定义类方法，cls表示类本身
def get(cls):
    pass

# 将字典直接作为多个参数传递给函数
dict = {'a': 1, 'b': 2, 'c': 3}
func(**t)	# 将字典的value按照key的作为参数名传入函数，注意这里不是依次
func(*t)	# 将字典的key作为参数依次传入函数
    
```
#####　元类

Python里面所有的类也都是一个对象，type是Python用来创建所有类的元类，元类是用来创建“类”这个对象的东西。通过在类中定义`metaclass`(python2中是在函数内部定义`__metaclass__`属性)，可以指定该类使用哪个元类来创建，如果没有改属性，并且父类里面都没有，那么默认就用type这个元类来创建。很好的元类使用的例子就是Django ORM，这就是元类的作用，把内部很复杂的东西变成一个简单的API。

```python
# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print(cls)		# <class '__main__.ListMetaclass'>
        print(name)		# MyList
        print(bases)	# (<class 'list'>,)
        print(attrs)	# {'__module__': '__main__', '__qualname__': 'MyList'}
        attrs['add'] = lambda self, value: self.append(value) # 给类添加一个add方法
        return type.__new__(cls, name, bases, attrs)
    
class MyList(list, metaclass=ListMetaclass):	# 指定该类在创建的时候用ListMetaclass.__new__来创建
    pass
```

#### 类型检查相关

从3.5开始，Python提供了类型检查功能，当然类型检查仅仅用于检查，并不会对程序的执行有任何的影响，但是配合IDE有代码提示过后，一切都变得方便了起来

```python
# 类型检查
def func(a: int) -> int	# 这表示该函数的参数a要求是整型，返回值是整型号

# 在运行时强制检查类型
@enforce.runtime_validation
def foo(text: str) -> None:...

name: str = 'haofly'	# 直接给变量指定类型
people: People			# 可以用自定义的类

# 返回组合类型
from typing import List, Tuple
Result = Tuple[Tuple[int, int], str]
def foo(strings: str, lines: List[str], line_number: int) -> Result:	# 这样子定义组合的返回类型
  
# 抽象基类abstract base class
from abc import ABCMeta, abstractmethod
class IStream(metaclass=ABCMeta):
  @abstractmethod
  def read(self, abc):
    pass
```

#### 数字

```python
# 随机数
import random
random.choice(list)  # 随机选择一个
random.sample(list, n) # 随机选择n个
random.shuffle(list)  # 打乱选择择后的顺序
random.randint(0, 10)  # 0到10的随机整数
random.random()   # 0到1得浮点数
random.getrandbits(100) # 获取100位随机数
random.uniform(begin, end)  # 生成0到10的随机浮点数

# 四舍五入
round(1.23, 1)   # 第二个参数表示保留几位小数
format(x, '0.2f')  # 保留两位小数

# 除法
14/3 = 4.666666666666667	# 精确除法
14//3 = 4			# 取整
14%3 = 2  # 求余

# 生成一组数
range(2)	// 生成[0, 1]
range(1, 2) // 生成[1]
range(0, 6, 2)	// 生成(0, 2, 4)
xrange用法与range一样，只是返回的不是一个生成好的列表，而是一个生成器，所以性能更好
```
#### 其他类型

##### NamedTuple类似结构体

```python
from typing import NamedTuple
class Student(NamedTuple):
	name: str
    address: str
    age: int = 13
haofly = Student(name='haofly', address='abc', age=12)
isinstance(haofly, tuple) # True
haofly[0]	# haofly
```

##### MappingProxyType只读字典

```python
from types import MappingProxyType
data = MappingProxyType({'a': 1})
```

##### SimpleNamespace简单的“基类”

类似于其他语言的基类，仅仅提供属性的快速访问与设置

```python
from types import SimpleNamespace
data = SimpleNamespace(a=1)
data.b = 2	# 这样data就是namespace(a=1, b=2)
```

#### 文件目录

```python
os.mkdir # 新建目录、文件
os.makedires('a/b')  # 创建多级目录
os.path.join(path, filename)	# 合并成全路径，用这个函数不用管路径用/还是\，也不用管最后有没有/
os.remove(filename)  # 删除单个文件
os.rmdir(dirname)   # 删除空目录

# 用其他库
import shutil
shutil.rmtree('mydir')   # 删除非空目录
shutil.copy(originame, tmpname)  # 复制单个文件
shutil.copytree(root_of_tree, desetination_dir, True) # 复制目录树
os.listdir('dirname')  # 显示一个目录下的所有文件和文件夹的名称
os.path.isdir(filename)  # 是否是目录
os.path.isfile(filename) # 是否是文件
os.path.islink  # 是否是链接
os.path.getsize(filename) # 获取文件大小
os.path.basename(fname)  # 从完整路径获取其路径
os.path.dirname(fname) # 从完整路径获取其名称
os.getcwd()   # 获取当前目录
os.chdir(newdir)  # 切换目录
os.path.exists(name)  # 判断目录是否存在
os.rename(original_name, new_name) # 修改文件名称

# 文件打开与关闭
fp = open('a.txt', 'w')
fp.close()
或者
with open('a.txt', 'w') as fp:   # 这种方式不需要close
	print('it's...', file=fp)
# 或者
import codecs
fp = codecs.open(filename, 'w', 'utf-8') # 这种方式可以解决很多编码问题
fp.write(string)
fp.close()

# 文件操作的标识
w: 只读
r: 只写
r+: 可用于读写，但是如果打开不读，直接就写，可能会覆盖，因为一打开的时候文件指针是在文件开头的

# 读取文件
fp.readline()  # 从文件读取一行数据
for each_line in fp:   # 可迭代获取每一行数据
	print(each_line)
fp.read()  # 读取所有数据
fp.readlines()  # 读取所有的行，返回一个列表，需要注意的是这个只会读取一次，读取第二次的时候就会返回空了
codecs.open(path, 'r', 'utf-8').read().splitlines() # 获取所有的数据，并使用splitlines()分隔行，这样在每行的后面就不会出现换行符了
print('string', file=fp)  # 直接写入文件

# 写入文件
fp.write()
fp.writelines()		# 并不会自动换行
          
# 清空文件内容
fp.seek(0, 0) # 这一句可以保证之前是否读取，都能清空
fp.truncate() # 清空语句

# 文件压缩zip库，这个库是纯Python写的，不是用C，解压速度比较慢，而且不支持压缩的时候加密，如果要想在压缩的时候加密，可以使用网上现成的一个库https://github.com/smihica/pyminizip，依赖于zlib库，但是如果要依赖zlib库为什么不直接用python调用zlib库的代码呢
          
# 计算文件的md5值
import hashlib
hashlib.md5(open('filename.exe', 'rb').read()).hexdigest()
          
# 递归便利文件路径，例如
glob.globa('/path/**/*.avi', recursive=True)	# 可以找到path目录下的所有avi文件
```
#### 异常处理

```python
try:
	raise RuntimeError('错误原因')
except (SystemErrork, SyncError) as e:		# 同时catch多个错误
    raise RuntimeError('')
except Exception as e:
	print(e)或者print(str(e))或者print(unicode(e))
	# 上面是打印基本的错误信息，如果要打印错误信息／文件名／错误行数，那么可以这样子:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(exc_type, fname, exc_tb.tb_lineno)
else:	# 如果没有发生异常会执行这里
  pass
finally:	# 只要离开try代码块都会执行这里的代码，即使执行了except也会执行这里，即使except里面有return语句，也会先执行这里
  pass
```
#### 系统相关

```python
# subprocess
# 执行系统命令
import subprocess
command = '...'
subprocess.check_output(command, shell=True)# 不能实时看到shell的输出
subprocess.check_call(command, shell=True)	# 可以直接看到输出结果
# 注意1: subprocess是不能实现ssh输入密码登录的。OpenSSH并不是使用STDOUT/STDIN与进程进行通信的，而是直接与终端进行通信。所以要实现用程序去与ssh进行交互，最好的方法是使用pexpect模块(pty模块)，它们会建立一个伪终端。另外，如果直接安装了linux的ssh扩展程序sshpass，则可以直接在命令行输入密码了。
# 注意2: subprocess的communicate是管道通信，而不是直接在命令行后面添加参数，所以直接用communicate传输参数对于有些非管道命令(例如ls)是不可行的，例如:
child = subprocess.Popen(['xargs', 'ls'], stdin=subprocess.PIPE,	# 这里必须加xargs universal_newlines=True)
child.communicate(filepath)

# 接收输入
a = input('Input: ')
                         
sys.getsizeof(name)  # 获取变量占用内存的大小

id(x)   # 返回对象标识，即内存地址
                         
platform.system()  # 当前操作系统
platform.release()  # 当前系统版本
sys.version     # python版本
os.environ['name']  # 获取系统环境变量
os.environ['name'] = value  # 设置系统环境变量
os.geteuid() == 0		# 判断当前用户是否拥有root权限(sudo权限)，貌似这是比较简单的方式了
```
#### 网络相关

##### socket网络编程客户端

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# 创建一个socket。AF_INET表示IPv4协议，如果要用IPv6，则用AF_INET6，SOCK_STREAM指定使用面向流的TCP协议。SOCK_DGRAM应该就是UDP协议了
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护，这样可以进行长连接
s.connect(('haofly.net', 80))		# 建立连接
s.send(b'GET / HTTP/1.1\r\nHost: haofly.net\r\nConnection: close\r\n\r\n')	# 向目标服务器发送数据
# 接收数据
buffer = []
while True:
    d = s.recv(1024)	# 每次最多接收1k字节
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
s.close()	# 关闭连接
# 解析数据
header, html = data.split(b'\r\n\r\n', 1)

# 通过主机名获取IP地址，由于该函数调用的是系统函数，所以可能出现无法及时更新host的情况，这种问题，socket并没有提供好的方法来刷新缓存，最好的解析DNS的方法是使用DNSPython库
socket.gethostbyname('haofly.net')
```

##### socket网络编程服务器端

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))	# 监听端口
s.listen(5)	# 开始监听端口，传入的参数指定等待连接的最大数量
while True:
    sock, addr = s.accept()	# 接受一个新连接，accept会等待并返回一个客户端的连接
    t = threading.Thread(target=tcplink, args=(sock, addr))	# 创建一个新的线程来处理TCP连接
    t.start()
    
def tcplink(sock, addr):
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
```

#### 包

```shell
# 在模块级别暴露接口
在目录下面加上__init__.py就变成了一个包，import包内部的模块使用'.'来分割，__init__.py里面可以定义一些全局变量，__all__指定了此包被import *的时候，哪些模块会被import进来。最好在创建一个包的时候都加上这个，避免有些模块被外部引用。如果没有定义__init__，那么import *的时候会将非下划线开头的成员都导入到当前命名空间中。
使用这种方式，在外部引入模块内部的模块会更加方便，而且比较不容易出错。特别是在交叉引用的时候，有时候会无法引用，但是如果直接在内部模块之间引入父模块就不会有这种错误，避免在文件开头交叉引用的时候无法找到模块。

# 单下划线和双下划线
__foo__: 一种约定，表示内部的名字，用来和其他用户自定义的变量名区分
_foo: 私有变量或者临时变量，不能用from import进行导入

# 带点号，表示当前目录下的模块，如
from . import client
# 可以在一个模块的根目录下得__init__.py定义一些基本的东西，比如加载一些模块呀，设置一些全局变量(__author__这样的东西)啥的

package.__version__  ＃获取package的版本

# 从github直接安装包的方法http://stackoverflow.com/questions/8247605/configuring-so-that-pip-install-can-work-from-github?answertab=active#tab-top
# 需要注意的是github上的库要有个固定的目录格式，还要有个setup.py文件，才能直接使用如下的命令，
pip install git+git@github.com:lynzt/python_people_names.git
    
# 将python包打包成debian包，可以用https://github.com/spotify/dh-virtualenv

# 从指定目录引入包，正如PyCharm里面经常不会出现import的问题，是因为它会首先将当前的项目路径添加到环境变量里面去，在终端执行的时候也要
import sys
sys.path.append('..')

# 动态导入模块
__import__(module_name)	# 相当于import
__import__(name = module_name, fromlist=[a, b])	# 相当于from module_name import a, b
## 如果想要动态实现from xxx import *的功能，目前貌似只能这样子做，手动添加到本地的命名空间:
module = __import__('module_name', ['*'])
for k in dir(module):
	locals()[k] = getattr(module, k)
```
#### 名字空间

程序在使用一个名字时，会从当前名字空间开始搜索，顺序则是LEGB:

```python
# locals: 函数内部的名字空间，一般包括函数的局部变量以及形参
# enclosing function: 潜逃函数中外部函数的名字空间
# globals: 当前的模块空间，类似于全局变量。，如果要改变全局变量的值，那么需要用global来声明，如果仅仅是使用该值那么可以不用global声明

# __builtins__: 内置模块空间
```

#### 输入输出

```python
print('string', file=sys.stderr)	# 直接输出到文件

# 输出重定向的方法
import sys
from io import StringIO

old_stdout = sys.stdout
old_stderr = sys.stderr
my_stdout = sys.stdout = StringIO()
my_stderr = sys.stderr = StringIO()

# blah blah lots of code ...

sys.stdout = self.old_stdout
sys.stderr = self.old_stderr

print(my_stdout.getvalue())
print(my_stderr.getvalue())

my_stdout.close()
my_stderr.close()

# 输出重定向到文件
fp = open(...)
sys.stdout = fp
```

## 魔术/自省方法

### 生命周期

```python
__new__		# 用来创建类并返回这个类的实例，在构造函数之前执行，可以决定是否用__init__方法来实例化类，是一个静态方法，创建实例的时候一定会调用。可以用它来作为创建单例的一种途径
__init__	# 用传入的参数来初始化一个实例，在创建实例的时候不一定会调用，比如反序列化的时候就不会执行
__del__		# 类的析构函数，对象在内存中被清理时执行，即使对象在执行中报错也依然会执行
```

### 属性

```python
__dir__		# 实现动态属性
class AttrDict(dict):
    def __getattr__(self, item):	# 是为了直接用点号可以访问动态属性
        return self[item]

    def __dir__(self):				# 是为了能自动完成，和用__dir__能够查找到该动态属性
        return super().__dir__() + [str(k) for k in self.keys()]
    
__getattr__(self, name)			# 定义了试图访问一个不存在的属性时的行为，重载该方法可以实现捕获错误拼写然后进行重定向, 或者对一些废弃的属性进行警告
__setattr__(self, name, value)	# 定义了对属性进行赋值和修改操作时的行为
__delattr__(self, name)			# 定义删除属性时的行为
__getattribute__(self, name)	# 定时访问属性时的行为，无论属性存不存在

# __get__(self, instance, owner)
## 描述起对象，instance是拥有者类的实例，参数owner是拥有者类本身。__get__在其拥有者对其读值的时候调用。

# __set__(self, instance, value)
## 在其拥有者对其进行修改值的时候调用。

# __delete(self, instance)
## 在其拥有者对其进行删除的时候调用。

# __getitem__(self, key)
## 当执行self[key]的时候，调用的就是该方法

# __setitem__(self, key, value)
## 当执行self[key] = value时调用

# __delitem__(self, key)
## 执行del self[key]时调用

# __iter__(self)
## 返回一个迭代器，当执行for x in container或者iter(container)时调用

# __contains__(self, item)
## 执行item in container或者item not in container时调用

# __missing__(slef, key)
## 定义key不在容器中的触发行为
```

### 运算符

```python
## __cmp__(self, other)
## __eq__(self, other)
## __ne__(self, other)
## __lt__(self, other)
## __ge__(self, other)
## __pos__(self)
## __neg__(self)
## __invert__(self)
## __abs__(self)
## __round__(self, n)
## __floor__(self)
## __ceil__(self)
## __trunc__(self)
## __add__(self, other)
## __sub__(self, other)
## __mul__(self, other)
## __floordiv__(self, other)
## __div__(self, other)
## __truediv__(self, other)
## __mod__(self, other)
## __divmod__(self, other)
## __pow__(self, other)
## __lshift__(self, other)
## __rshift__(self, other)
## __and__(self, other)
## __or__(self, other)
## __xor__(self, other)
```

### 类型

```python
## __int__(self): 实现了类型转化为int的行为
## __long__(self)
## __float__(self)
## __complex__(self)
## __oct__(self)
## __hex__(self)
## __index__(self)
## __str__(self)
## __sizeof__(self)
```

### 序列化

```python
## __getinitargs__(self): 
## __getnewargs__(self)
## __getstate__(self)
## __setstate__(self, state)
## __reduce__(self)
## __reduce_ex__(self)
```

### 特殊方法

```python
__call__	# 在定义类的时候，实现该函数，这样该类的实例就变成可调用的了，相当于重载了括号运算符.例如，md5那几个库，使用的时候就是md5(...)，但其实它肯定是个类的实例而不是个简单的函数撒.使用场景例如：
class A():
    def __call__(self, key):
        print(key)
        a = A()
        a('key')	# 打印'key'
        
with		# 关键字的几个魔术方法，用with可以实现在函数前后执行某些语句
## __enter__(self): 会返回一个值，并赋值给as关键词之后的变量
## __exit__(self, exception_type, exception_value, traceback): 定义代码段结束后的一些操作，如果返回True，那么下面的异常会被屏蔽，如果返回None，那么会抛出
class Count():
    def __enter__(self):
        print(time())
    def __exit__(self):
        print(time())
with Count():
    func()		# 这样在函数的开始与结束都能打印出时间了，这只是一个简单例子而已
    
## __slots__	可用于定义一种限制类，建议在有大量实例存在的情况下对类进行优化时才使用。该类没有__dict__属性，所有的属性都被显示地固定在__slots__中，不会中途添加属性或者减少属性。
class test:
	__slots__ = ['field1', 'field2']	# 即可定义
```

## 装饰器

#### property(描述符)

可将类的方法变为类的属性，比如之前用`person.name()`，现在可以直接`person.name`了

## 标准库

#### argparse(命令行程序)

```python
import argparse

parser = argparse.ArgumentParser(description='命令介绍')
parser.add_argument('-d', help='添加一个参数 (default: 一半在括号里面设置用户看的默认值)')
parser.add_argument('-v', '--version', help='设置简写')

# add_argument参数列表
## help: 帮助文档
## type: 固定类型，例如type=int
## action: action可以指定参数应该如何保存，默认是store，可以是store_true/store_const/append/append_const/help。例如action='store_true'
## choices: 可选参数，提供一个列表
## required=True: 必选
## default=xx: 设置默认值
args = parser.parse_args()	# 默认自带了-h, --help参数
args.d	# 获取名为d的参数

# 如果要多级的命令解析，有几个方法:
## 1. 使用第三方库，例如declarative_parser
## 2. 像scrapy那样，直接用print
## 3. 使用原生的group，例如
import argparse
def task_a(alpha):
    print('task a', alpha)
def task_b(beta, gamma):
    print('task b', beta, gamma)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')
    parser_a = subparsers.add_parser('task_a')
    parser_a.add_argument('-a', '--alpha', dest='alpha', help='Alpha description')
    parser_b = subparsers.add_parser('task_b')
    parser_b.add_argument('-b', '--beta', dest='beta', help='Beta description')
    # 可以根据subparser的值判断使用哪一个函数
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)
```

#### collections

[参考](http://my.oschina.net/leejun2005/blog/222236)，提供额外的数据类型

- **namedtuple()**：生成可以使用名字来访问元素内容的tuple子类
- **deque**：双端队列
- **Counter**：计数器，可用于统计字符串中字符数量。找出序列中出现次数最多的元素
- **OrderedDict**：有序字典
- **defaultdict**：带有默认值的字典，这样访问不存在的dict就不会出错了

#### contextlib

加强with语句，with本身是配合`__enter__`和`__exit__`来进行上下文管理的，但是有了`contextlib`，我们可以更方便写适合于with的代码，例如:

```python
@contextlib.contextmanager
def make_context(obj):
    print('__enber__')
    try:
        yield()
    except xxxError as e:
        print(e)
    finally:
        print('__exit__')
        
with make_context(myclass()) as func:
    func....
```

#### copy 深拷贝与浅拷贝

简单地说，python中对象的赋值都是进行对象引用(内存地址、指针)传递，浅拷贝复制了对象，变成了两个对象，但是对于对象中的元素，依然使用的原始的引用，深拷贝则是一个完全新的对象

```python
copy.copy()		# 浅拷贝，字典的copy方法是浅拷贝
copy.deepcopy()	# 深拷贝

# 例如
a = {'a': {'b': 1}}
b = a			# 简单的建立一个对象的引用，"a is b" is True
b = copy.copy()	# 浅拷贝，"a is b" is False, "a['a'] is b['a']" is True，此时b['a']['b']=2会同时改变a['a']['b']的值
b = copy.deepcopy()	# 深拷贝，"a is b" is False, "a['a'] is b['a']" is True，此时b['a']['b']=2，并不会改变a['a']['b']的值
## 浅拷贝
```

#### cProfile/Profile: 函数运行时间度量

```python
import cProfile
from time_profile import *
 
cProfile.run("timeit_profile()")
```

#### ctypes

提供C语言兼容的数据类型，可以方便调用DLL中的函数，例如win/mac平台的系统库。

#### functools

```python
# 偏函数partial: 用于固定函数中的某几个参数形成新的函数
import functools

def add(a, b):
    return a + b

plus3 = functools.partial(add, 3)
plus3(4)	# 输出7

# update_wrapper：主要用在装饰器函数中，使得装饰器返回函数反射得到的是包装函数定义而不是原始函数定义

# wraps：调用函数装饰器partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)的简写

# reduce：等同于内置函数reduce()

# cmp_to_key：将一个函数转换为比较函数
# total_ordering
```

#### heqpq

查找最大或最小的几个元素。

#### inspect

用于直接访问一个类或对象内部的各个属性

```python
inspect.ismodule(object)	# 是否为模块
inspect.isclass(object)		# 是否为类
inspect.getdoc(object)		# 获取documentation信息
inspect.getfile(object)		# 获取对象的文件名
inspect.getsource(object)	# 以string形式返回object的源代码
```

#### itertools

[参考](http://www.wklken.me/posts/2013/08/20/python-extra-itertools.html#itertoolscountstart0-step1)

- **count(start=0, step=1)**：创建连续整数
- **cycle(iterable)**：创建一个迭代器，可以反复循环的，此时用在for里面如果不加终止条件会无限循环
- **repeat(object, times)**：创建一个迭代器，根据指定数量，生成重复的对象
- **chain(\*iterables)**：将多个迭代器作为参数, 但只返回单个迭代器, 它产生所有参数迭代器的内容, 就好像他们是来自于一个单一的序列.
- **compress(data, selectors)**：提供一个选择列表，对原始数据进行筛选
- **dropwhile(predicate, iterable)**：创建一个迭代器，只要函数predicate(item)为True，就丢弃iterable中的项，如果predicate返回False，就会生成iterable中的项和所有后续项
- **groupby(iterable, key)**：返回一个产生按照key进行分组后的值集合的迭代器.
- **ifilter(predicate, iterable)**：与dropwhile相反
- **ifilterfalce(predicate, iterable)**：与上面这个相反
- **islice(iterable, stop)**：返回的迭代器是返回了输入迭代器根据索引来选取的项。可用于跳过一个循环前面几项的for循环。比如跳过前面3个项目: `for x in islice(items, 3, None)`
- **imap(function, \*iterables)**：返回一个迭代器, 它是调用了一个其值在输入迭代器上的函数, 返回结果. 它类似于内置函数 map() , 只是前者在任意输入迭代器结束后就停止(而不是插入None值来补全所有的输入).
- **starmap(function, iterable)**：创建一个迭代器，生成值func(*item),其中item来自iterable，只有当iterable生成的项适用于这种调用函数的方式时，此函数才有效。
- **tee(iterable[, n=2])**：从iterable创建n个独立的迭代器，创建的迭代器以n元组的形式返回，n的默认值为2
- **takewhile(predicate, iterable)**：与takewhile相反
- **izip(\*iterables)**：返回一个合并了多个迭代器为一个元组的迭代器. 它类似于内置函数zip(), 只是它返回的是一个迭代器而不是一个列表
- **izip_longest(\*iterables[, fillvalue])**：与izip()相同，但是迭代过程会持续到所有输入迭代变量iter1,iter2等都耗尽为止，如果没有使用fillvalue关键字参数指定不同的值，则使用None来填充已经使用的迭代变量的值。
- **product(\*iterables[, repeat])**：笛卡尔积，排列组合
- **permutations(iterable[, r])**：排列
- **combinations(ierable, r)**：创建一个迭代器，返回iterable中所有长度为r的子序列，返回的子序列中的项按输入iterable中的顺序排序 (不带重复)
- **combinations_with_replacement(iterable, r)**：创建一个迭代器，返回iterable中所有长度为r的子序列，返回的子序列中的项按输入iterable中的顺序排序 (带重复)

#### iterator迭代器

```python
next(iterator)		# 返回下一个迭代对象
yield a 			# 返回一个迭代对象
yield from iterator	# 相当于for x in iterator \ yield x

# 给生成器传值，例如
def generator():
    jump = yield a
next(iterator)		# 给生成器赋非None值时，只能在开始迭代以后
iterator.send(2)	# 传值给生成器，jump=2
```

#### logging日志模块

日志格式

```tex
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名|
%(funcName)s 调用日志输出函数的函数名|
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮点数表示|
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数|
%(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s 用户输出的消息
```

实例:

```python
# 最复杂的使用
import logging

logger = logging.getLogger('AppName')	# 初始化日志处理器实例，可以用AppName来区分不同的模块
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')	# 定义日志格式

file_handler = logging.FileHandler("test.log")		# 文件日志
console_handler = logging.StreamHandler(sys.stdout)	# 控制台日志
file_handler.setFormatter(formatter)				# 设置日志格式

logger.addHandler(file_handler)			# 为logger添加的日志处理器
logger.removeHandler(file_handler)		# 移除日志处理器

logger.setLevel(logging.INFO)		# 设置日志输出最低级别

logger.debug('this is debug info')
logger.info('this is information')
logger.warn('this is warning message')
logger.error('this is error message')	# 与logger.exception()相同
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')

logger.error('%s service is down', 'own')	# 格式化输出日志

# 比较简单的使用
logging.basicConfig(filename='test.log', level=logging.DEBUG)	# 这样接口
```

#### http.server(SimpleHTTPServer)

最简单的web服务器，十分方便，最多的用途是用来进行局域网其他设备访问本机文件目录`python -m SimpleHTTPServer 8000`即可，`Python3`里面，模块更改为`python3 -m http.server`另外，如果要想使`SimpleHTTPServer`能增加CORS特性，可以创建一个这样的文件`simple-cors-http-server.py`，之后直接用python执行即可，文件内容如下:

```python
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)
```

#### pickle: 序列化工具

将一个对象序列化为一个字节流，这样方便讲对象保存在文件中。对于那种需要在不同地方执行，或者直接想以文件的方式保留执行过程变量，而不借助复杂的数据库的情况，是非常方便的。

```python
import pickle
fp = open('test', 'wb')
pickle.dump(data, fp)		# 将变量写入文件
s = pickle.dumps(data)		# 将对象转换为字符串

fp = open('test', 'rb')
data = pickle.load(fp)		# 将变量读取出来
data = pickle.load(s)		# 将字符串反转成其对应的变量
```

#### smtplib: 用于发送邮件

```python
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.header import Header

# 腾讯SMTP
mail_host = '发件服务器'
mail_user = '发件人'
mail_pass = '收件人'

sender = '发件人'
receivers = ['收件人']

message = MIMEText('这是邮件内容', 'plain', 'utf-8')
message['From'] = "\"%s\" <%s>" % (Header('发件人', 'utf-8'), Header('发件人', 'utf-8'))
message['To'] = Header('to', 'utf-8')
message['Subject'] = Header('邮件主题', 'utf-8')

smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host)
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
print('邮件发送成功')
```

#### sorted: 数组/字典排序

```python
sorted([5,4,3,2,1])	# 输出[1,2,3,4,5]
sorted("This is a test string from Andrew".split(), key=str.lower)	# 用参数key指定比较所用的元素
student_tuples = [('john', 'A', 15),('jane', 'B', 12),('dave', 'B', 10),]
sorted(student_tuples, key=lambda student: student[2])   # 用元组内部的元素进行比较，这种方法同样可以应用于对象内部属性的比较，比如lambda student: student.age，其中lambda可以用itemgetter代替，例如key=itemgetter(2)。而类属性则可以用attrgetter代替，例如key=attrgetter('age')，甚至可以同时选择多个属性，例如itemgetter(2,3)，attrgetter('age', 'name')
sorted([5,3], reverse=False)	# 倒序
```

#### timeit: 时间度量

```python
import timeit
timeit.Timer('x=range(1000)').timeit()	# 可以直接得到代码的执行时间
timeit.Timer('sum(x)', 'x = (i for i in range(1000)').timeit() # 参数
```



- - ​

- **SocketServer**：[参考](http://blog.marchtea.com/archives/60)两种服务模型：ThreadingMinxln(有新请求时，创建一个新的进程)、ForkingMinln(有新请求时，创建一个新的线程)
  - **TCPServer**
  - **UDPServer**
  - **UnixStreamServer**
  - **UnixDatagramServer**

- **weakref**：弱引用，与常规的引用相对，这种引用在对象只剩下一个弱引用的时候，就可能会被回收，多见于类的嵌套定义防止错误回收，weakref的失效依赖于对象实际销毁。gc销毁的时机未知，引用计数的销毁则是可控的，比如(del)，可以减少异常的发生。使用方式例如:

  ```python
  class Parent(object):
      def __init__(self):
          self.children = [Child(self)]

  class Child(object):
      def __init__(self, parent):
          self.parent = weakref.proxy(parent)
  ```


## PIP版本管理

`pip`可以使用`==、>=、<=、>、<`几个符号来指定需要安装的依赖版本，并且可以同时使用多个，例如`Django>1.0,<2.0`则安装的是她们之间的最接近的指定版本的版本，如果想要直接用最新的，那么不用符号，直接写名字就好了。常用命令:

```shell
pip install Django —upgrade 	# 更新指定package
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U	# 升级所有的包
pip install --pre sqlalchemy	# 安装prelease版本
sudo pip3 install scrapy -i https://pypi.douban.com/simple  # 使用豆瓣的PIP源，例如
```

## 语言本身

#### 性能分析与优化

- 使用timeit
- 使用cProfile，精确到函数
- 使用vprof，可视化
- line_profiler，精确到行

#### Python设计模式

## SQLite数据库

Python语言内置了`SQLite`轻量级数据库。

```python
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('正常的sql语句')
cursor.execute('select * from user where id=?', ('1', ))	# 查询语句
cursor.fetchall()	# 获取查询结果
cursor.rowcount	# 获取插入的行数
cursor.close()	# 关闭cursor
conn.commit()	# 提交事务
conn.close()	# 关闭连接
```


## TroubleShooting
- **AttributeError: 'EntryPoint' object has no attribute 'resolve'**
  原因是`cryptography`版本过高或过低，需要制定版本，一般是`pip install cryptography==1.2.1`

- **PEP8三目运算符的换行** 
  可以加括号，例如:

  ```python
  re = (
  	'a'
  	if 'a' == 'b'
  	else 'c'
  )
  ```


- **ValueError: Attempted relative import in non-package**  

  相对路径问题，所谓的相对路径其实是相对于当前module的路径，而不是当前目录的路径，如果当前目录不是module，那么当前module的name就是`__main__`，所以会出错

- **Python中一切都是对象，a=1，b=1，两个是同一个对象，所以Python是无法通过变量名获取同名字符串的**

- **在调试某些代码的时候发现print没有输出**: 这是有可能将print重定向了，这是用sys.stdout.write('')可以实现打印输出到控制台

- **`zsh: no matches found: requests[socks]`**: 原因是zsh这个工具会把方括号解析为正则匹配，这时候只需要加上引号即可，例如`pip install 'requests[socks]'`

- `segmentation fault`，在使用`keyboard`和`pynput`的时候曾经遭遇过不可预料的原因，原因是这两个库都没有考虑中文输入法的问题，对于中文输入法，MacOS的Carbon库有另外兼容的做法(详见Pynput的issue)。最简单的解决方法就是切换到`American`

- **Python序列化出现`maximum recursion depth`错误**。可以设置`sys.setrecursionlimit(1000)`来解决。

- **`__main__ is not a package`**: 去掉import前面的点

- **`ImportError: cannot import name 'xxx'`**。请先检查是否存在交叉引用。

- **安装涉及到openssl lib的库的时候出现错误`openssl/opensslv.h`或者`openssl/err.h` not found等错误**，首先要确定确实有安装该库。Mac下安装用`brew install openssl`，然后如果还是不行就用这种方式进行安装`pip install cryptography --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"`

- `no module named _sqlite3`，原因是系统多个`python`版本导致
  首先安装sqlite库，`yum install sqlite-devel`，然后重新安装`python`

- ​

## 推荐阅读

[Hidden features of Python](http://stackoverflow.com/questions/101268/hidden-features-of-python)

[PyMOTW-3](https://pymotw.com/3/): 由 [Doug Hellmann](http://doughellmann.com/ )所写的Python标准库的示例用法。

[深刻理解Python中的元类(metaclass)](http://blog.jobbole.com/21351/)

[Python项目的配置管理](https://www.keakon.net/2016/10/22/Python%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86)
