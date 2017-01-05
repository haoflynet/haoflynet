---
title: "Python字符串"
date: 2016-08-07 11:06:30
updated: 2016-12-28 19:48:00
categories: python
---
# Python字符串

## 编码问题

- **2中打印str显示前面加了个u且中文类似\u8be5\u9879**：这是十六进制的Unicode编码，使用`string.encode('utf-8')`进行转换

- **2中类似\uiahd\u9483这样的字符串**：需要注意的是，该字符串本来就是这样，而不是编码成这样的，这时候需要反编码：`string.decode('unicode_escape'))`

- **无法解析\u2c这样的unicode字符，出现错误`UnicodeDecodeError: 'unicodeescape' codec can't decode bytes in position 0-3:truncated \uXXXX escape`**: 原因是unicode默认是\uxxxx这样的形式来解析字符串的，但是如果出现`\u2c`这种，是解析不了的，应该写成`\u002c`这种形式，前面需要补全

- **url编码** Python3中，url编码放在了url lib.parse中了

  ```python
  from urllib import parse
  parse.quote(str)
  parse.quote_plus(str)
  ```

- **bytes to string**

  ```pythohn
  b"abcde".decode('utf-8')
  ```

- **将字符串输出为16进制字节**:

  ```python
  ":".join("\{:02x\}".format(ord(x) for x in 字符串))
  # 或
  ":".join("\{0:x\}".format(ord(x) for x in 字符串))
  # 输出类似于: 12:45:45
  ```

- **16进制转换为utf-8** :类似 `\xe5\x94\xae\`这种，使用如下方式进行转换

  ```python
  unicode(string, 'utf-8')
  ```

- **查看字符编码**

  ```python
  import chardet
  chardet.detect(string)
  ```


## 常用操作

```python
# 字符判断
string.isalpha()	# 是否为字母
string.isdigit()	# 是否为数字

# 格式化字符串
'abcdef %s' % (123)	# 特别适合长字符串不用加号来拼接字符串的情况
"my name is {name}".format(name=name)	# 这种方式好处是可以直接定义名字
f'my name is {变量名}'	# Python3.6里面新增的特性，可用这种方式直接格式化字符串

# 指定列宽格式化字符串
import textwrap
print(textwrap,fill(s, 70)) # 将s字符串已70列显示，多的换行
os.get_terminal_size().columns # 可以使用这个方法获得终端的大小和尺寸

# 字符串填充
a = 'abc'
print(a.zfill(5)) # 输出'00abc'

# 去掉空格
s.strip()          # 去掉两端空格
s.lstrip()         # 去掉左边空格，加参数可以
s.rstrip()         # 去掉右边空格
s.replace(' ', '') # 去掉所有空格

# 大小写转换
s.upper()    # 全部转为大写
s.lower()    # 全部转为小写
```

### 查找与替换

```python
# 字符串替换
import re
text = 'Today is 11/27/2016'
pat = re.compile(r'(\d+)/(\d+)/(\d+)')
pat.sub(r'\3-\1-\2', text)
'Today is 2016-11-27'

# 带命名组的替换
re.sub(r'<a.*?>(.*?)</a>','\g<1>', text) # 替换a标签，但保留a标签里面的内容，需要注意的是.*表示最长匹配，而.*?表示最短匹配

# 对替换做特殊处理
print(re.sub('(?P<value>\d+)', lambda matched: str(int(matched.group('value')) * 2), s))

# 使用正则方式查找  
import re  
url = 'http://haofly.net/note.html'  
match = re.search('(.*)/(.*?).html', a)  
print(match.group(1), match.group(2))

# 基本查找，返回第一个出现该字符串的位置  
text.find(',')   

# 查找某字符串出现的所有位置的一个列表  
[m.start() for m in re.finditer(',', text)]  # 输出[4, 11]  

# 忽略大小写的查找
re.findall('python', 'text, flags=re.IGNORECASE)  
           
# 查找所有匹配的
matches = re.findall('pattern', string)   # 返回所有匹配的列表  

# 最短匹配  
str_pat = re.compile(r'\\"(.*?)\\"')  
str_pat.findall(text2)  	# 输出['no.', 'yes.']

# 查找时中文编码问题
re.search('中文(.*?)呵呵'.decode('utf8'), string)
           
# 字符串分割-正则方式
line = 'asdf fjdk; afed, fjek, asdf, foo'
import re
re.split(r'[;,\\s]\\s_', line) # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
re.split(r'(;|,|\\s)\\s_', line) # 这样连分隔符都能分割出来
```

## 时间处理

```python
# 简单的获取时间：
import datetime
a = str(datetime.date.today())
print(a)  # 格式为2015-07-17
a = time.strftime('%H:%M:%S')  # 格式为11:20:00
time.strftime('%Y-%m-%d %H:%M:%S')

# 字符串转时间：
time_str='Tue, 11 Nov 2014 06:37:20 +0000'
date = datetime.datetime.strptime(time_str, '\%a, \%d \%b \%Y \%H:\%M:\%S \%z')
print(date)  # 输出'2014-11-11 06:37:20+00:00'
print(date.timestamp()) # 输出时间戳'1415687840.0'
# 或者
date = datetime.datetime(2006, 12, 12, 12, 12, 12)

# 获取当天开始和结束的时间(即00:00:00到23:59:59)
today = datetime.date.today()
datetime.datetime.combine(today, datetime.time.min)
# 得到datetime.datetime(2015, 7, 24, 0, 0)
datetime.datetime.combine(today, datetime.time.max)
# 得到datetime.datetime(2015, 7, 24, 23, 59, 59, 999999)

# 时间加一天，加一分钟，昨天，明天，前面几天，后面几天
now = datetime.datetime.now()
date = now + datetime.timedelta(days = 1)
date = now + datetime.timedelta(seconds = 3)

# 关于时间占位符总结：
%d：日
%b：简写的月份，如Oct
%Y：年份
%H：小时
%m：月
%M：分钟
%S：秒
%z：与时区相关，在标准时间上加时间，例如'+00:00'

# 各种格式举例
time.strftime('%Y-%m-%dT%H:%M:%S%z')  # 2015-11-11T02:49:03+00:00

# 转换时间为UTC／GMT时间
time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.mktime(time.strptime("2008-09-17 14:04:00",                   "%Y-%m-%d %H:%M:%S"))))

# 时间戳的转换：
ltime=time.localtime(1395025933)
timeStr=time.strftime("\%Y-\%m-\%d \%H:\%M:\%S", ltime)

string = '2015年09月18日 00:01:00'
date = time.strptime(string, '\%Y年\%m月\%d日 \%H:\%M:\%S')
b = time.mktime(date)   # 获取时间戳

# datetime转时间戳
time.mktime(the_date.timetuple()

# 获取本月有多少天，以及最后一天的计算方法
import calendar
today = datetime.date.today()
_, last_day_num = calendar.monthrange(today.year, today.month)
last_day = datetime.date(today.year, today.month, last_day_num)
```

## TroubleShooting

- **"TypeError: Unicode-objects must be encoded before hashing"**

  原因是在3.x中，md5方法仅接受unicode编码过后的字符串:

  ```python
  hashlib.md5(string.encode('utf-8')).hexdigest()
  ```
