---
title: "Python手册"
date: 2013-08-20 12:05:30
updated: 2023-07-28 09:36:30
categories: python
---
[Python 包/pcakge排名](https://hugovk.github.io/top-pypi-packages/): `pypi.org`那个搜索不知道结果是些啥玩意儿，最好在这里搜，前5000基本上都是主流的

##  安装方法

```shell
# for CentOS
yum groupinstall -y 'development tools'
yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel xz-libs  libffi-devel
# for Ubuntu
apt-get install -y build-essential libssl-dev libffi-dev
# for alpine
apk add --update alpine-sdk

# Linux下不区分64和32位
wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tar.xz	
xz -d Python-3.9.9.tar.xz
tar -xvf Python-3.9.9.tar
cd Python-3.9.9
# for Linux
./configure && make && sudo make altinstall		# altinstall能够不覆盖默认的python路径及可执行文件。但是注意通过altinstall安装的python在使用pip install后的包如果有可执行文件可能会覆盖默认的
# for Mac
./configure --enable-framework --with-openssl=/usr/local/opt/openssl	# 不加openssl可能会出现the SSL module is not available的错误
cd

# 如果默认没有安装pip，那么可以这样安装
wget https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

# Python3.5版本默认有安装pip的，如果没有，那么就酱紫
wget https://bootstrap.pypa.io/get-pip.py
python3.3 get-pip.py

python3 -m venv/ path/to/venv	# 创建virtualenv环境
```

## 基本语法

<!--more-->

- 3.8开始支持海象运算符，又能少写一行代码了

  ```python
  if (n := len(a)) > 10:
    print(n)
  ```


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

# while/for循环都能用else，我擦嘞。else是指执行完了才会去执行，如果中途是break跳出循环的，则else不会被执行
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
#### 元组tuple

```python
a = ('1', )
b = '2'
a + (b,)	# 元组中添加元素
```

#### 字符串

```python
# hash值计算，使用hashlib库，其中有sha256/md5等。base64是一个单独的库
```

#### 字典

- 字典也能用生成式，例如`{a.id: a.value for a in list}`
- **使用del删除字典的元素后，内存并不会释放，可能会有内存泄漏的问题**

```python
# 字典遍历
for key in dict:
	print(key, dict[key])
for key in dict.keys():	# 这种方式能在遍历的时候删除字典元素，如果用上面的方式进行删除会报错RuntimeError: dictionary changed size during iteration
    del dict[key]
for key, vlaue in dict.items():
	print(key, value)
	
# 特殊的key
li = {
	'a': 'b',
	None: 'c',
	'': ''
}

if 'a' in dict		# 判断key是否存在
if dict.get('a', {}).get('b', {}).get('c')	# 一下判断多个层级，这样不用每层都是一个if条件了
dict.get('a', 'b')	# 如果不存在那么给一个默认值
dict['abc'] = 'xxx'	# 添加新key
dict.keys()			# 获取所有的key，这里返回的是一个dict_keys，一个迭代器
dict.values()	# 获取所有的value
list(dict)			# 如果仅仅想获得key的数组
list(dict.values())	# 获取value的数组

# 表达式解析
a = {'x': 1, 'y': 2}
globals().update(a)
print(x, y)

# 漂亮地打印json数据
print(json.dump(sdata, indent=2))

# 有序字典(占用的内存是普通字典的两倍)
from collections import OrderedDict
d = OrderedDict()
for k, v in d.items(): # 有序字典的遍历

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

sorted(mydict.keys())	# 字典按key值排序
sorted(mydict.items(), key=lambda item:item[1])	# 字典按value值排序

# 字典合并（ChainMap只是将两个字典在逻辑上变为一个，在它上面的修改只会影响第一个字典a)
from collections import ChainMap
c = ChainMap(a, b)

# 要想一个对象继承与一个字典，并且能用json.dumps()转换为json对象，那么可以这样做
class ErrorMsg(dict):
    """自定义错误类"""
    def __init__(self, e: Exception, code: int):
        dict.__init__(self, msg=str(e), code=code)
class CustomError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status
json.dumps(ErrorMsg(e, 200))	# {"msg":"xxx", "code":200}

# 字典列表的筛选，直接用filter
filter(lambda person: person['name'] == 'haofly', people_list)	# 不过有个缺点，就是不能传值进lambda，不然就直接用以下这种方法吧
[person for person in people_list if person['name'] = name]

# 字典推倒式
d = {key: value for (key, value) in iterable}

# 字典相加/字典合并
dict(dict1.items() + dict2.items())
dict(dict1, **dict2)
dict1.update(dict2)	# 这种方式不会返回新的字典，只会更新原有dict1字典

# 打乱字典顺序
import random
dict_list = list(dict1.items())
random.shuffle(dict_list)
dict2 = dict(dict_list)
```
#### 集合

```python
a = {'a', 'b'}	# 集合定义
a.add('b')	# 给集合添加元素
a.remove('b')	# 给集合移除元素
a.clear()	# 清空集合
```

#### 类/函数

- 定义在`__init__`外的属性相当于静态变量，所有对象公用，`__init__`内部的才是对象私有的
- 在3以前，类有经典类和新式类(显示继承自object)的区分，区别就是前者是深度优先去搜索方法，后者是广度优先去搜索方法，3以后都是新式类了

```python
# 几个特殊的方法
x.__class__.__name__  # 获取实例的类名

# 继承相关
super().__init__()	# 继承时需要调用父类的初始化方法
super(self.__class__, self).__init__()	# python2里面的父类初始化
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
func(*l)	# 将数组以此传入函数

# attr，python3.7新增特性
@attr.s
class Product(object):
    id = attr.ib()
    name = attr.ib()
    comment = attr.ib(repr=False, cmp=False, hash=False)	# repr=False的时候该字段不会在打印类的时候打印出来
    price = attr.ib(validator=[attr.validators.instance_of(int), check_func])	# 直接在定义的时候指定验证函数
    min_price = attr.ib(converter=int)	# 直接将类型进行转化
    x = attr.ib(metadata={'a': 'b'})	# 直接给属性设置元数据
    
    # 通过装饰起的方式直接对类的属性进行验证
    @id.validator
    def check(self, attribute, value):
        raise ValueError(...)
new Project(1, 'name')	# 好处是不用在__init__里面一个一个定义所有的属性了
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

#### 类型检查相关(Type Hint)

从3.5开始，Python提供了类型检查功能，当然类型检查仅仅用于检查，并不会对程序的执行有任何的影响，但是配合IDE有代码提示过后，一切都变得方便了起来

```python
type('string') is str	# 获取变量类型
isinstance('string', str)	# 判断变量类型

a:int=123	# 直接定义变量的类型
b: typing.Optional[int] = None

# 类型检查
def func(a: int) -> int	# 这表示该函数的参数a要求是整型，返回值是整型号
def func(a: int=None) # 参数赋予默认值
def func(a: int=None) -> typing.Optional[int]	# 返回int或者None
def func(a: Union[int, str])	# 入参允许int或者str

# 在运行时强制检查类型
@enforce.runtime_validation
def foo(text: str) -> None:...

name: str = 'haofly'	# 直接给变量指定类型
people: People			# 可以用自定义的类

# 返回组合类型
from typing import List, Tuple
Result = Tuple[Tuple[int, int], str]
def foo(strings: str, lines: List[str], line_number: int) -> Result:	# 这样子定义组合的返回类型
  
# or，指定可以为多种类型，例如AnyStr就是TypeVar('AnyStr', str, bytes)定义的
MY_TYPE = TypeVar('MY_TYPE', str, int)

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
random.sample(list, n) # 随机选择n个，可以实现随机字符串
random.shuffle(list)  # 打乱选择择后的顺序
random.randint(0, 10)  # 0到10的随机整数
random.random()   # 0到1得浮点数
random.getrandbits(100) # 获取100位随机数
random.uniform(begin, end)  # 生成0到10的随机浮点数

# 四舍五入
math.ceil(10/3) = 4	# 向上取整
math.floor(10/3)= 3	# 向下取整
round(1.23, 1)   # 第二个参数表示保留几位小数
format(x, '0.2f')  # 保留两位小数
abs(-123)	# 获取绝对值

# 除法
14/3 = 4.666666666666667	# 精确除法
14//3 = 4			# 取整，整除
14%3 = 2  # 求余

# 生成一组数
range(2)	// 生成[0, 1]
range(1, 2) // 生成[1]
range(0, 6, 2)	// 生成(0, 2, 4)
xrange用法与range一样，只是返回的不是一个生成好的列表，而是一个生成器，所以性能更好
```
#### 其他类型

#### Enum枚举类型

```python
# 直接定义
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr'))
# 精确控制值
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
Weekday['Sun'].value	# 得到value值为0
[e.value for e in Weekday]	# 获取枚举所有的值
Weekday(1).name	# 通过枚举value获取name
```

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
pathlib.Path('src/').mkdir(parents=True, exist_ok=True)	# 在指定目录下新建目录
os.path.join(path, filename)	# 合并成全路径，用这个函数不用管路径用/还是\，也不用管最后有没有/
os.path.abspath(__file__)	# 获取当前文件的绝对路径
pathlib.Path(__file__)	# 同上
pathlib.Path(__file__).resolve().parent.parent	# 直接获取父级目录
pathlib.Path(__file__).resolve().parent.joinpath('abc')	# 代替os.path.join功能
os.path.expanduser('~')	# 得到当前用户的家目录
pathlib.Path.home()		# 同上

os.path.basedir('/a/b')	# 获取当前目录或文件的父路径，例如/a/b返回/a，但是/a/b/返回/a/b
os.remove(filename)  # 删除单个文件
os.rmdir(dirname)   # 删除空目录
os.walk(dirname)	# 遍历目录，返回的是迭代器，每一个元素表示(dirpath, dirnames, filenames)即目录路径，包含的子目录列表，包含的文件列表

# shutil库
import shutil
shutil.rmtree('mydir')   # 删除非空目录
shutil.copy(originame, tmpname)  # 复制单个文件
shutil.copytree(root_of_tree, desetination_dir, True) # 复制目录树
os.listdir('dirname')  # 显示一个目录下的所有文件和文件夹的名称
os.path.isabs(filename)  # 是否是绝对路径
os.path.isdir(filename)  # 是否是目录
os.path.isfile(filename) # 是否是文件
os.path.islink  # 是否是链接
os.path.getsize(filename) # 获取文件大小
os.path.getatime(filename)	# 获取文件的访问时间
os.path.getctime(filename)	# 获取文件创建时间
os.path.getmtime(filename)	# 获取文件最近一次内容更改的时间
os.path.basename(fname)  # 从完整路径获取其文件名
os.path.dirname(fname) # 从完整路径获取其名称
os.getcwd()   # 获取当前目录
os.chdir(newdir)  # 切换目录
os.path.exists(name)  # 判断目录是否存在
os.rename(original_name, new_name) # 修改文件名称
pathlib.Path('.original_name').rename('newname')

# 文件打开与关闭,'r+b'表示打开二进制的读写。第三个参数为buffering用于设置buffer，0代表关闭buffer只能用于二进制，1代表line buffer只能用于文本，>1表示初始化的buffer的大小
fp = open('a.txt', 'w', 1)
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
        
# 验证文件或者文件夹的可读可写
os.access(path, os.W_OK)
os.access(path, os.R_OK)
        
# 读取文件
fp.readline()  # 从文件读取一行数据
for each_line in fp:   # 可迭代获取每一行数据
	print(each_line)
fp.read()  # 读取所有数据
fp.readlines()  # 读取所有的行，返回一个列表，需要注意的是这个只会读取一次，读取第二次的时候就会返回空了
codecs.open(path, 'r', 'utf-8').read().splitlines() # 获取所有的数据，并使用splitlines()分隔行，这样在每行的后面就不会出现换行符了
print('string', file=fp)  # 直接写入文件

# 写入文件
## 使用fileinput实现只修改文件中某一行的功能
fp.write()
fp.writelines()		# 并不会自动换行
          
# 清空文件内容
fp.seek(0, 0) # 这一句可以保证之前是否读取，都能清空
fp.truncate() # 清空语句

# 文件压缩zipfile库，这个库是纯Python写的，不是用C，解压速度比较慢，而且不支持压缩的时候加密，如果要想在压缩的时候加密，可以使用网上现成的一个库https://github.com/smihica/pyminizip，依赖于zlib库，但是如果要依赖zlib库为什么不直接用python调用zlib库的代码呢
          
# 计算文件的md5值
import hashlib
hashlib.md5(open('filename.exe', 'rb').read()).hexdigest()
          
# 递归便利文件路径，例如
glob.globa('/path/**/*.avi', recursive=True)	# 可以找到path目录下的所有avi文件
```
#### 异常处理

```python
import traceback
try:
  raise RuntimeError('错误原因')
except (SystemErrork, SyncError) as e:		# 同时catch多个错误
  traceback.print_exc()	# 直接打印异常Exception的堆栈信息
  print(traceback.format_exc())	# 以字符串的形式打印栈信息
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

# 同时except多个异常
except (OneExcetion, SecondException) as e:
  pass

# 自定义异常
class BadRequestException(BaseException):
    def __init__(self, message, status=400):
        super().__init__(message, status)
        self.message = message

    def __str__(self):
        return self.message
```
#### 系统相关

```python
# subprocess
# 执行系统命令
# python3开始，call/check_call/check_output全部用run(..., check=True)代替# stdout=subprocess.PIPE表示将输出重定向到管道，这样主程序就没有实时输出，如果不指定，默认子程序会实时输出的。不过这种情况，我们必须正确处理管道的输出，否则如果任由子程序一直输出，可能会造成死锁。
# shell=True/False表示命令是否通过shell来执行。
# Popen与这些run的区别是Popen不会阻塞，不用等待结果，而且可以与子线程进行交流(获取其运行状态)，和js里面的Promise类似
import subprocess
result = subprocess.check_output(command, shell=True, encoding='utf-8')# 不能实时看到shell的输出，输出会以返回值返回，程序出错抛出异常。等价于run(..., check=True, stdout=PIPE).stdout
subprocess.check_output(command, shell=True, stdin=subprocess.PIPE)	# 这样就是异步了
try:
  subprocess.check_output(command, shell=True, stderr=subprocess.PIPE)
  
  # 如果程序正常退出，但是却有stderr，那么可以这样获取标准错误输出
  output = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  print(output.stderr, output.stdout)
except subprocess.CalledProcessError as e:	# 获取正确的错误输出
    print('exit code: {}'.format(e.returncode))
    print('stdout: {}'.format(e.output.decode(sys.getfilesystemencoding())))
    print('stderr: {}'.format(e.stderr.decode(sys.getfilesystemencoding())))
result = subprocess.check_call(command, shell=True)	# 可以直接看到输出结果，程序出错会抛出异常，程序成功返回0。等价于run(..., check=True)
result = subprocess.call(command, shell=True)	# 跟check_call返回结果一样。等价于run(...).returncode
# 注意1: subprocess是不能实现ssh输入密码登录的。OpenSSH并不是使用STDOUT/STDIN与进程进行通信的，而是直接与终端进行通信。所以要实现用程序去与ssh进行交互，最好的方法是使用pexpect模块(pty模块)，它们会建立一个伪终端。另外，如果直接安装了linux的ssh扩展程序sshpass，则可以直接在命令行输入密码了。
# 注意2: subprocess的communicate是管道通信，而不是直接在命令行后面添加参数，所以直接用communicate传输参数对于有些非管道命令(例如ls)是不可行的，例如:
child = subprocess.Popen(['xargs', 'ls'], stdin=subprocess.PIPE,	# 这里必须加xargs universal_newlines=True)
child.poll()	# 检查子进程是否结束，并且返回returncode属性
child.wait()	# 等待子进程结束，并且返回returncode属性
child.send_signal(signal)	# 向子进程发送信号
child.terminate()	# 停止子进程
child.kill()		# 杀死子进程
child.pid			# 获取子进程的ID
child.returncode	# 获取子进程的返回值，如果还没有结束，则会返回None
stdoutdata, stderrdata = child.communicate(input=None)	# 与子进程进行交互，向stdin，或从stdout/stderr中读取数据，不过要读取或者输入那么在创建Popen对象的时候就得设置响应的PIPE。input指定发送到子进程的参数。该命令会一直等到进程退出

# 接收输入
a = input('Input: ')
                         
sys.getsizeof(name)  # 获取变量占用内存的大小，但这只是对象本身，它内部包含的其他对象的引用并不会计算在内的
sys.argv	# 获取命令行参数                         

id(x)   # 返回对象标识，即内存地址
                         
platform.system()  # 当前操作系统
platform.release()  # 当前系统版本
sys.version     # python版本
os.dup2(fp1, fp2)	# 将文件描述符fp1复制到fp2
os.environ['name']  # 获取系统环境变量
os.environ['name'] = value  # 设置系统环境变量
os.geteuid() == 0		# 判断当前用户是否拥有root权限(sudo权限)，貌似这是比较简单的方式了
os.setsid()		# 将当前进程设置为头领进程，相当于让系统觉得它没有子进程，它本身就是一个父进程
os.umask(0)		# 修改文件模式，让当前进程拥有所有读写执行的权限
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

socket.connect_ex((host, port)) == 0	# 类似于telnet验证目标端口是否开放
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
使用这种方式，在外部引入模块内部的模块会更加方便，而且比较不容易出错。特别是在交叉引用的时候，有时候会无法引用，但是如果直接在内部模块之间引入父模块就不会有这种错误，避免在文件开头交叉引用的时候无法找到模块。另外__init__.py是给包外部文件import的，内部文件之间引用不用从__init__.py中import

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

# 从指定目录引入包，正如PyCharm里面经常不会出现import的问题，是因为它会首先将当前的项目路径添加到环境变量里面去，在终端执行的时候需要添加下面的代码，或者直接执行` export PYTHONPATH=$PYTHONPATH:/path/to/project`
import sys
sys.path.append('..')

# 动态导入模块
__import__(module_name)	# 相当于import
__import__(name = module_name, fromlist=[a, b])	# 相当于from module_name import a, b
## 如果想要动态实现from xxx import *的功能，目前貌似只能这样子做，手动添加到本地的命名空间:
module = __import__('module_name', ['*'])
for k in dir(module):
	locals()[k] = getattr(module, k)
	
# 编码注释风格
#!/usr/bin/python
# -*- coding: <encoding name> -*-

# 直接用代码形式安装包
from pip import operations, main	# pip version < 10
from pip._internal import operations, main # pip version >= 10
operations.freeze.freeze()	# 返回所有安装的包
main(['install', 'requests'])	# 安装包
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

- Python默认会有输出缓冲区，所以有时候`print`没有输出不用担心(systemd journal看不到print输出)，可能是缓冲区没有刷新，可以在运行程序的命令加上`-u`参数，例如`python -u main.py`，或者直接添加一个环境变量`PYTHONUNBUFFERED=1`

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

# 使用__new__创建单例，只需要给类添加如下方法即可
def __new__(cls, *args, **kwargs):
    if cls._singleton is None:
        cls._singleton = object.__new__(cls)

        return cls._singleton
```

### 属性

```python
__dir__		# 实现动态属性
class AttrDict(dict):
    def __getattr__(self, item):	# 当对象的属性不存在时会调用该方法，你可以在该方法里面定义自定义的属性，但是一定要注意当不存在时，最后要抛出AttributeError
      if item in self.my_dict:	# 不能在这里面直接调用getattr方法，因为不存在就会出现递归错误
        return self[item]
      raise AttributeError

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

```python
# 普通的函数装饰器
def new_func(func):
    def wrapper(*args, **kwargs):
        print('in wrapper')
        return func(*args, **kwargs)
    return wrapper

@new_func
def test():
    pass
        
# 类装饰器
class NewClass:
    def __init__(self, func):
        self._func = func
 	def __call__(self):
        print('调用')
        self._func()
@NewClass
def test():
    pass

# 类装饰器dataclasses
## python3.7使用这个可以生成__init__、__repr__和比较相关的魔术方法
@dataclass
class A:
  a: float
  b: int = 1	# 可以不用写构造方法了
    
```



#### property(描述符)

可将类的方法变为类的属性，比如之前用`person.name()`，现在可以直接`person.name`了。

```python
class A:
  @property
  def value(self):
    return 'ok'
A().value	# 即可访问
```

## 标准库

#### argparse(命令行程序)

`optparse`从2.7开始不推荐使用了

```python
import argparse

parser = argparse.ArgumentParser(description='命令介绍', usage='[options] (start|stop|status|restart|condrestart|version)', epilog='help信息之后的信息')
parser.add_argument('action', choices=('start', 'stop', 'status', 'restart'))
parser.add_argument('-d', help='添加一个参数 (default: 一半在括号里面设置用户看的默认值)')
parser.add_argument('-v', '--version', help='设置简写')
parser.add_argument('-v', '--version', action='version', version='1.0')	# 版本信息
parser.add_argument('-c', metavar='FILENAME')	# 参数的参数值，例如这里会输出-c FILENAME
parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
if len(sys.argv) == 1:	# 如果没有桉树默认打印help信息
    parser.print_help()
    sys.exit()

# add_argument参数列表
## help: 帮助文档
## type: 固定类型，例如type=int
## action: action可以指定参数应该如何保存，默认是store，存放在const中，可以是store_true/store_const/append/append_const/help。例如action='store_true'
## choices: 可选参数，提供一个列表
## required=True: 必选
## default=xx: 设置默认值
args = parser.parse_args()	# 默认自带了-h, --help参数
args.d	# 获取名为d的参数
vars(args)	# 将所有参数转换为字典格式

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

#### ast抽象语法树

ast作用在python代码的语法被解析后，被编译成字节码之前，所以我用它来检测代码中是否有未安装的包，解析在docstring中定义的meta等，因为代码还未执行，所以并不会报错。

```python
with open(file, 'r') as fp:
    syntax_tree = ast.parse(fp.read())
print(ast.get_docstring(syntax_truee))
```

ast还能代替`eval`的功能执行安全的操作将字符串类型的对象转换为对应的对象。(`eval`)会转换所有的操作，有很大的安全风险。

```python
ast.literal_eval("{'field1' : 'value1', 'field2' : 'value2'}")	# 会直接输出一个字典
```

#### atexit

可以定义整个程序结束之前需要执行的代码，相当于程序的析构函数，可以使用register函数注册程序退出时的回调函数。当然，如果程序`crash`掉或者通过`os._exit()`退出，该函数不会被执行。可以同时注册多个函数，到时候会按照逆序来执行。

```python
import atexit
atexit.register(my_func)
```

#### collections

[参考](http://my.oschina.net/leejun2005/blog/222236)，提供额外的数据类型

- **namedtuple()**：生成可以使用名字来访问元素内容的tuple子类
- **deque**：双端队列
- **Counter**：计数器，可用于统计字符串中字符数量。找出序列中出现次数最多的元素
- **OrderedDict**：有序字典
- **defaultdict**：带有默认值的字典，这样访问不存在的dict就不会出错了

#### ConfigParser配置读取

```python
cf = configparser.ConfigParser()
cf.read('test.conf')	# 需要注意的是，使用同一个cf，多次read相同或者不同的文件，结果会累加覆盖
cf.sections()	# 得到所有的section名列表
cf.options('db')	# 得到section为db下面的配置名称列表
cf.items('db')		# 得到section为db下面的配置的列表(每个配置都是一个二维元组)
cf.get('db', 'host')	# 得到某个session下某个配置的值
cf.getboolean('db', 'host')
cf.getfloat('db', 'host')
cf.getint('db', 'host')
cf.has_option('section', 'option')
cf.has_section('section')

cf.read_dict({'section1': {}})	# 从字典中读取配置
cf.add_section('section')	# 添加section
cf.set('section', 'option', 'value=None')	# 给指定section添加一个配置项，section必须存在
fp.write(cf)		# 将配置写入文件
```

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
b = copy.copy(a)	# 浅拷贝，"a is b" is False, "a['a'] is b['a']" is True，此时b['a']['b']=2会同时改变a['a']['b']的值
b = copy.deepcopy(a)	# 深拷贝，"a is b" is False, "a['a'] is b['a']" is True，此时b['a']['b']=2，并不会改变a['a']['b']的值
## 浅拷贝
```

#### cProfile/Profile: 函数运行时间度量

```python
import cProfile
from time_profile import *
 
cProfile.run("timeit_profile()")
```

#### [csv](https://docs.python.org/3/library/csv.html)

- Python内置了csv读写库的

#### ctypes

提供C语言兼容的数据类型，可以方便调用DLL中的函数，例如win/mac平台的系统库。

- `Python3`里面跟C语言传参时需要`encode('utf-8')`一下，以防出现`<class 'TypeError'>: wrong type`错误

```python
from ctypes import *
dll = cdll.LoadLibrary('./libtest.so')
print(dll.__dict)
```

#### functools

```python
# 偏函数partial: 用于固定函数中的某几个参数形成新的函数，在传入匿名的回调函数的时候非常有用
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

#### importlib

- **resources**: 在静态文件所在的文件夹添加一个`__init__.py`文件，那么这个文件夹就变成一个`module`，就可以使用`importlib.resourcesd来直接导入静态文件，而不用像以前那样拼接参数了。

#### inspect

用于直接访问一个类或对象内部的各个属性

```python
inspect.ismodule(object)	# 是否为模块
inspect.isclass(object)		# 是否为类
inspect.getdoc(object)		# 获取documentation信息
inspect.getfile(object)		# 获取对象的文件名
inspect.getsource(object)	# 以string形式返回object的源代码
inspect.getfullargspec(func).args	# 获取函数的参数列表
```

#### ipaddress

IP地址处理模块

```python
ip = ipaddress.ip_address('192.0.2.1')	# 新建一个IP地址对象IPv4Address('192.0.2.1')
network = ipaddress.ip_network('192.0.2.1/24', strict=False)	# 新建一个网络段
ip in network	# 判断ip是否在某个地址段内
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

logging.basicConfig(filename='test.log', level=logging.DEBUG)	# 比较直接简单那的用法

logger.info('test', extra={'key': value})	# 传递给formatter的参数(如果formatter里面有自定义参数)

# logging日志默认是按照系统的时区输出的，如果想换自己的时区，可以有这两种方法
## 方法一，python程序中直接修改当前环境变量，但是可能影响当前项目其他代码的时区获取
os.environ['TZ'] = 'Asia/Chongqing'
time.tzset()
## 方法二，使用pytz
from pytz import timezone, utc
def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Asia/Chongqing")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()
logging.Formatter.converter = customTime
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

将一个对象序列化为一个字节流，这样方便将对象保存在文件中。对于那种需要在不同地方执行，或者直接想以文件的方式保留执行过程变量，而不借助复杂的数据库的情况，是非常方便的。

- 需要注意的是pickle会将对象引用的所有的对象都进行序列化，所以体积往往会比`getsizeof`大得多。如果想要渐小体积，可以直接用`ba2.BZ2File(filename, 'w')`来写入文件，用`bz2.open(filename)`来读取文件
- `pickle.dump`的第三个参数是协议版本，如果是同版本语言之间`dump`和`load`，那么完全可以用`pickle.HIGHEST_PROTOCOL`目前是5，而默认值`pickle.DEFAULT_PROTOCOL`默认是3，会根据语言版本不同而改变，最好就用最新的，在效率上肯定更好

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
from email.header import Header
from email.mime.text import MIMEText

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

# TLS加密方式
smtp = smtplib.SMTP(smtpHost, smtpPort)
smtp.starttls()
smtp.login(mail_user, mail_pass)

# SSL加密方式
smtp = smtplib.SMTP_SSL(smtpHost, smtpPort)
smtp.login(mail_user, mail_pass)
```

#### sorted: 数组/字典排序

```python
sorted([5,4,3,2,1])	# 输出[1,2,3,4,5]
sorted("This is a test string from Andrew".split(), key=str.lower)	# 用参数key指定比较所用的元素
student_tuples = [('john', 'A', 15),('jane', 'B', 12),('dave', 'B', 10),]
sorted(student_tuples, key=lambda student: student[2])   # 用元组内部的元素进行比较，这种方法同样可以应用于对象内部属性的比较，比如lambda student: student.age，其中lambda可以用itemgetter代替，例如key=itemgetter(2)。而类属性则可以用attrgetter代替，例如key=attrgetter('age')，甚至可以同时选择多个属性，例如itemgetter(2,3)，attrgetter('age', 'name')
sorted([5,3], reverse=False)	# 倒序
```

#### sys

- **executable**: 获取解释器的路径
- **meta_path**: 这个功能就强大了，可以实现在import的时候触发相关操作，相当于import操作的一个hook。

#### timeit: 时间度量

```python
import timeit
timeit.Timer('x=range(1000)').timeit()	# 可以直接得到代码的执行时间
timeit.Timer('sum(x)', 'x = (i for i in range(1000)').timeit() # 参数
```

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

## PIP版本管理/包管理

`pip`可以使用`==、>=、<=、>、<`几个符号来指定需要安装的依赖版本，并且可以同时使用多个，例如`Django>1.0,<2.0`则安装的是她们之间的最接近的指定版本的版本，如果想要直接用最新的，那么不用符号，直接写名字就好了。常用命令:

```shell
pip install Django --upgrade 	# 更新指定package
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U	# 升级所有的包
pip install --pre sqlalchemy	# 安装prelease版本
sudo pip3 install scrapy -i https://pypi.douban.com/simple  # 使用豆瓣的PIP源，例如
```

### pipenv

最新的包管理工具，使用`pip install pipenv`直接安装。其配置文件

```shell
[[source]]		# 源地址
url = "https://pypi.python.org/simple"
verify_ssl = true
name = "pypi"

[[source]]
url = "https://pypi.douban.org/simple"
verify_ssl = true
name = "douban"

[packages]		# 运行锁依赖的包
sqlalchemy = "*"
mysqlclient = "*"
sanic-graphql = "*"
graphene = "*"
graphene-sqlalchemy = {version='*', index='douban'}	# 指定需要的源
django = ">=2.0.0"	# 指定版本

[dev-packages]	# 开发所依赖的包

[requires]		# 需要的python版本，把本模块删除表示不限制python版本
python_version = "3.7"
```

pipenv常用命令

```shell
pipenv --python 3.7		# 指定python版本
pipenv check					# 检查已安装的包中是否有安全隐患
pipenv check --style test.py	# 检查指定文件的编码风格
pipenv uninstall --all	# 删除所有的安装包
```

## 语言本身

#### 性能分析与优化

- 使用timeit
- 使用cProfile，精确到函数
- 使用vprof，可视化
- line_profiler，精确到行

## SQLite数据库

Python语言内置了`SQLite`轻量级数据库。

```python
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('正常的sql语句')
cursor.execute('select * from user where id=?', ('1', ))	# 查询语句
cursor.fetchall()	# 获取查询结果
cursor.lastrowid	# 获取刚才插入的行的id
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

- **Python序列化出现`maximum recursion depth`错误**。可以设置`sys.setrecursionlimit(2000)`来解决，默认的递归深度是1000

- **`__main__ is not a package`**: 去掉import前面的点

- **`ImportError: cannot import name 'xxx'`**。请先检查是否存在交叉引用。

- **安装涉及到openssl lib的库的时候出现错误`openssl/opensslv.h`或者`openssl/err.h` not found等错误**，首先要确定确实有安装该库。Mac下安装用`brew install openssl`，然后如果还是不行就用这种方式进行安装`pip install cryptography --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"`

- `no module named _sqlite3`，原因是系统多个`python`版本导致
  首先安装sqlite库，`yum install sqlite-devel`，然后重新安装`python`

- **Python执行js**: `js2py`和`execjs`都只能执行简单的js脚本，要复杂的，还是直接调用系统解析器吧，例如`node -e`

- **unknown file type, first eight bytes**: 这是在加载动态链接库.so的时候发生，原因是该.so文件是在linux平台下编译的，而我实在macos上调用，所以发生该错误。解决方法是在macos重新编译生成.so文件，或者直接在linux下调用。

- **pip出现`ImportError: No module named pkg_resources`错误**:安装工具 `pip install setuptools`

- **ImportError: cannot import name 'sysconfig'**: 

  ```shell
  sudo apt-get install zlib1g-dev
  sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
  ```

- **TypeError: must be type, not classobj**: 在2里面，继承的时候，父类没有继承自object

- **`pipenv`初始化的目录出错**: 请检查其上级或者上上级目录里是否有`Pipenv`文件，如果有没必要的文件，删除即可

- **Unsupported operation :not writeable python**: 一般是在写文件时候打开方式没有加'w'，而是直接`open('file')`

- **fatal error: Python.h No such file or directory**: 需要安装python相关的开发库: `yum install python-devel`

- **gcc failed with exit status 1**: 原因是没有安装python开发相关扩展，需要先安装`yum install python-devel`

- **Libraries for snappy compression codec not found**: 需要安装依赖库

    ```shell
    sudo apt-get install libsnappy-dev	# debian
    yum install snappy-devel	# centos
    brew install snapy	# macos
    
    pip install python-snappy	# 成功
    ```

- **from Crypto.Cipher import AES报错No module named 'Crypto'**: 卸载`pycrypto`直接安装`pycryptodome`
  
- **安装完fabric但是执行却报错: no module named fabric.api **可以尝试这样解决:
  
  ```shell
  pip uninstall fabric
  pip install fabric3
  ```
  
- **mac安装pillow, no module named PIL**:
  
  ```shell
  xcode-select --install
  brew install libjpeg
  pip install Pillow
  ```
  
- **ModuleNotFoundError: No module named 'pip._internal'**: 可以尝试用这种方法:
  
  ```shell
  sudo pip install --upgrade pip
  pip3 install --user --upgrade pip	# 或者
  ```
  
- **pip requires Rust>1.41**: 升级pip试试: `pip3 install "pip>=20"`
  
- **`Click will abort further execution because Python 3 was
    configured to use ASCII as encoding for the environment.`**: 错误原理见[click](https://click.palletsprojects.com/en/7.x/python3/)，设置一下系统的语言就好了:

    ```shell
    # 先通过locale -a看当前系统有哪些语言，然后填入正确的语言即可， 例如
    export LC_ALL=en_US.utf8
    export ALL=en_US.utf8
    ```

- **psycopg2安装失败**: 可以尝试`export ARCHFLAGS="-arch x86_64" pip install psycopg2 --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include`

- **#error architecture not supported**: 安装某些包的时候会出现这个，可以尝试`ARCHFLAGS="-arch x86_64" pip install nltk`

- **No such file or directory: 'c++': 'c++'**: `apt install build-essential`

- **no module named bz2: **`sudo apt-get install libbz2-dev`或者`sudo yum install bzip2-devel `

- **no module named cv2**: `pip install opencv-python`

- **urllib3 v2.0 only supports OpenSSL 1.1.1+**: 尝试降级: `pip uninstall urllib3 && pip install urllib3<2.0`

## 推荐Package

- [python-dotenv](https://github.com/theskumar/python-dotenv): 从`.env`文件里面读取环境变量

## 推荐阅读

[Hidden features of Python](http://stackoverflow.com/questions/101268/hidden-features-of-python)

[PyMOTW-3](https://pymotw.com/3/): 由 [Doug Hellmann](http://doughellmann.com/ )所写的Python标准库的示例用法。

[深刻理解Python中的元类(metaclass)](http://blog.jobbole.com/21351/)

[Python项目的配置管理](https://www.keakon.net/2016/10/22/Python%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86)

[Python十大web框架](https://hackernoon.com/top-10-python-web-frameworks-to-learn-in-2018-b2ebab969d1a): 全栈框架(Django/Pyramid/TurboGears/Web2py)、微框架(Flask/Bottle/CherryPy/)、异步框架(Sanic/Tornado)

[Unofficial Windows Binaries for Python Extension Packages 非官方的Python扩展windows平台二进制包](https://www.lfd.uci.edu/~gohlke/pythonlibs/): 对于windows平台总是安装不成功的包可以尝试这样安装

[pyexcel](https://github.com/pyexcel/pyexcel): Python处理Excel表格数据，如果只是读取，可以直接用[pyexcel-xls](https://github.com/pyexcel/pyexcel-xls)

[Python连接FTP/FTPS](https://haofly.net/python-ftp/)