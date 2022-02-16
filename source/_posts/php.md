---
title: "PHP 手册"
date: 2013-08-07 02:02:30
updated: 2021-12-23 08:50:21
categories: php
---
# PHP

- 貌似基本上的语言都不会像PHP这样，每次一个HTTP请求过来都去重启初始化全部资源(重启整个框架)，要解决这个问题，`swoole`是目前最可行的解决方案
- PHP还有一种输出内容模式是直接echo或者直接重定向，在return之前就返回，有些古老的框架是这样的，需要特别注意
- [LEMP(Linux + Nginx + MySQL + PHP)环境安装](https://haofly.net/lemp)

## 基本语法

- 判断两个变量是否相等，如果`==`和`===`都能用的情况，那么尽量用`===`，因为它仅检查闭合范围。

- `??`: null合并运算符。如果遍历那个存在且值不为NULL，就返回本身，否则返回它的第二个操作数。三元运算符可以这样用`$a = $a ? : 1`，表示如果为真则直接使用`$a`的值，7里面可以写成`$a = $a ?? 1`

  ```php
  $username = isset($_GET['user']) ? $_GET['user'] : 'nobody';
  $username = $_GET['user'] ?? 'nobody';	// 和上面语句等价
  $username = $_GET['user'] ?? $_POST['user'] ?? 'nobody'; // 甚至可以连接多个
  ```

- `??=`(7.4): 运算符表示有key则赋值，例如`$array['key'] ??= 1`表示数组中有`key`这个key才会被赋值

- `compact`函数，能够创建一个包含变量和它们的值的数组，例如

  ```php
  $a = 123;
  $b = 'abc';
  compact("a", "b");	// ['a' => 123, 'b' => 'abc']
  ```

<!--more-->

### 数组

- 7.4支持数组展开操作: `['banana', 'orange', ...$parts, 'watermelon']`，其中`$parts`为一个数组

```php
array_column($array, $column_key);	// 返回字典型数组里面指定key的那一列组成一个新的数组，取数组指定key组成一个新的数组，例如[['a' => 1], ['a' => 2]], array_column($arr, 'a')得到[1, 2]
array_search(); // 搜索一个key的索引，如果是二维的数组，那么就是通过value搜索key
array_search(strtolower($search), array_map('strtolower', $array)); // array_search忽略大小写
array_search('haofly', array_column($users, 'name')); // 搜索数组的某个字段，如果能找到则返回索引，找不到返回false

array_fill(0, $size, NULL);	// 新建一个固定长度的数组
array_chunk($array, $size);	// 将数组按size大小分为多个数组
array_diff($a, $b); // 比较数组的不同，可以用来判断两个数组是否相等，需要注意的是这里返回的是在array1中但是不在array2中的值，而不是两个的交集
array_flip($array);	// 反转数组的key和value，value作为key，key作为value
array_key_exists("key",$a);  # 查看key是否存在于某个字典
array_intersect($array1, $array2[,$array $...]);	# 返回一个数组，该数组包含了所有在array1同时也出现在其他参数数组中的值
array_map($callback, $array);	// 为数组中每一个元素应用回调函数，如果是类的静态方法，可以这样调用：array_map('myclass::myMethod' , $value);或者array_map( array('myclass','myMethod') , $value);
array_merge((array)arr1, (array)arr2);			# 合并数组，相同的key直接覆盖(前面的被后面的覆盖)，需要特别注意的是如果其中有一个数组为null那么结果就为null，所以最好加上array强制转换一下
array_merge_recursive();	# 合并数组，相同的key不覆盖
['a' => 1] + ['b' => 2]; # 合并数组，数组能够直接相加
array_push($source, "red", "gree");	# 给数组添加元素
array_unshift($arr, $value);	# 在数组开头插入一个或多个元素
array_rand();	// 从数组中随机取出一个或多个元素
array_reverse();// 逆序数组

array_slice($arr, 0, 1); # 数组分片
array_sum($arr); //计算数组中所有值的和
array_unique();	// 数组去重
array_values($arr); //获取数组所有的value值
array_walk(); // 利用回调函数对数组中每一个元素做回调处理
array_keys();	// 获取所有的key
array_values(); // 获取所有的value

count()函数：输出数组的长度
empty()函数：判断数组是否为空
end()		// 返回当前数组的最后一个值，需要注意的是这个函数不仅仅是返回最后一个值，还会把数组当前的指针指向最后一个数据
implode(',', $arr)	# 将数组拼接成字符串
in_array('a', $a, false)				# contain, 查看数组是否存在某个元素。第三个参数表示严格模式，默认为false，最好为true，否则像这种in_array('aa', [0])居然是true
json_encode($arr)	# 数组转换城字符串
list($a, $b) = [1, 2]	# 分别赋值
rsort(); # 以降序对数组排序
sort();		# 排序，可以给数组排序，会修改原来数组的值
uasort($array, $cmp_function)	# 定义对比函数进行排序
unset(arr[1]); // 删除数组元素，需要注意的是，一维数组，在unset以后，索引不会变，比如unset($a[1])，过后，该数组里面就没有1这个索引，而不是把2这个索引提到前面来，使用的时候需要特别注意，delete one item，delete元素
array_splice($a, $index, 1);	# 用这种方式删除数组的元素，索引会改变

# 排序，需要注意的是，php的排序都不会改变索引，只是改变了迭代的顺序，如果是一维数组，序号只是没有在自己的位置上，本质上index是没有变的，需要特别注意，在json_encode或者在转换为其他对象时可能不会出现预期的结果
sort($arr, function($item1, $item2){return $item1 > $item2});

# 数组遍历
foreach($array as $value); //数组遍历
foreach($array as $key => $value); // 数组(字典)遍历，如果是数组，$key表示索引
  
# 数组用于函数
func(*list); // 将数组作为函数的输入
  
# 在数组里面添加数组元素，在不确定key的情况下
$arr = [];
$arr['a'][] = 'a';
$arr['a'][] = 'b';

# 通过数组元素值删除元素
if (($key = array_search($del_val, $messages)) !== false) {
    unset($messages[$key]);
}
```

### 字符串

- 7.1开始支持负数作为偏移: `"abcdefg"[-2] == 'f'`

PHP里面单引号和双引号确实有些地方的用法是不同的，比如匹配换行符的时候。我们应该尽量使用单引号，因为如果是双引号，那么程序会去检测其中的变量。

```php
json_decode(string, $assoc=false);	# 将字符串转换为json对象,$assoc=true时返回array而不是object
lcfirst($str)			# 将字符串首字母转换为小写
mb_strlen($str, 'utf-8') # 求中文字符串长度
mb_substr($str, $start, $length, 'utf-8'); // 字符串分割，字符串截取，可以分割中文哟，如果要获得所有右边的，那么$length不用填或者填上NULL，如果版本不行那就是用功能弱一点的substr
substr($str, $start, $length);	// 字符串分割/字符串截取
substr('abcdefg', -1); // 获取字符串最后一个字符
nl2br() # 将字符串中的\n转换成网页的换行符<br>
sprintf()	# 字符串格式化，需要注意的是，它不是用\转义，而是用的%来转义
strlen() # 求字符串长度
strpos('abc', 'a'); 	# 在字符串中查找第一次出现位置，没找到返回false
str_contains('abc', 'a');# 查找字符串是否出现在指定字符串中，php8.x开始的
str_repeat('abc', n)	# 将字符串重复n次
str_replace(搜索值，替换值，目标)	# 字符串替换，需要注意的是原字符串不会变化，返回的结果才是替换后的字符串
str_replace_first()	# 替换第一个
str_replace_last()	# 替换最后一个
str_replace(array("\r\n", "\r", "\n"), '', $content);	# 去除换行符
strval(5);	# 数字转字符串
substr_count($haystack, $needle, [$offset, $length]);	# 计算子字符串needle在字符串haystack中出现的次数
trim($string);	# 去除字符串前后的空白字符，如果要去除所有的字符只能使用preg_replace('/\s+/', '', $string)，这是stackoverflow上面给出的答案
$a . $b . 'abc' 	# 字符串连接直接用点号
explode(',', $str, [,$limit])	# 字符串分割，第三个参数大于0表示限制分组数量，limit规定所返回的数组元素的个数，小于0时，返回包含除了最后的-limit个元素以外的所有元素的数组；0表示返回包含一个元素的数组
array_map('strrev', explode('-', strrev($a), 2))	# 字符串分割，逆向
iconv('utf-8', 'GBK', $data): 将字符编码从utf-8转换为GBK
join("&", $arr)	# 拼接字符串
parse_str('name=wang&age=18'): 从查询字符串中解析到变量，可以得到$name和$age两个变量
parse_url($url): 解析url成数组，与http_build_query()功能相反
preg_replace('/user_id=\d+&name=/', 'user_id=' . 1048 . '&name=', $code); // 正则替换
preg_replace('/user_id=(\d+)', '/user_id=${1}', $code);	// 获取分组，${1}、${2}...
preg_replace_callback('//', function($matches){return strtolower($matchs[0])}, $text); 执行一个正则表达式搜索并且使用一个回调函数进行替换
preg_split('/a/', $subject); // 通过一个正则表达式分隔给定字符串
preg_match('/Chongqing(?<right>.*)/', $string, $matches): 正则匹配，pattern参数前后必须加斜杠，匹配成功返回1，匹配结果在$matches中，匹配失败，返回0
sprintf("sahgoiahg%s", $a): 格式化输出
strtolower($str)/strtoupper($str): 大小写字符串
ucfirst($str): 将字符串首字母大写
ucwords($str): 将字符串每个单词首字母大写
                      
str_replace(' ', '', lcfirst(ucwords(str_replace(['-', '_'], ' ', $str))));	# 字符串转换为驼峰命名法
                      
$long_str = <<<EOT
abcdefg
EOT;		# 定义长字符串
                      
addslashes($str);		// 使用反斜线引用字符串
pack(format, args+);	// 将数据装入一个二进制字符串，通常用户低级socket编程中，需要注意的是format的可选值和其他语言的可选值可能不一样，多语言交互的时候对照一下
                      
ctype_alnum($string);	# 检查字符串是否由字符和数字组成，等同于preg_match('/[a-zA-Z0-9]+/', $string);
                      
// php7.1新增短数组语法
$data = [[1, 'tom'], [2, 'fred']];
list($id1, $name1) = $data[0]; // 和python有点像
[$id2, $name2] = $data[1];
foreach ($data as [$id, $name]) {	// 循环中也能直接用
    // logic here with $id and $name
}
                      
urlencode($str);	// url encode编码
```
### 数字

- PHP_INT_MAX: 最大整数
- PHP_INT_MIN: 最小整数

```php
ceil()函数：向上取整
rand(min, max)：产生随机数，不需要给初始值了现在
intval($val): 字符串转整数，如果不是数字型字符串，那么转换会失败，失败后返回0，没错是0，mmp
int ip2long(string $ip_address)：IP转换成整数值
string long2ip(string $proper_address)：整数值转换成IP
number_format(float $number)	// 以千位分隔符方式格式化一个数字，返回字符串
sprintf('%04d', 2)	// 数字前补零
10 % 3 = 1;	// 求余操作
str_pad($nu, 4, "0", STR_PAD_LEFT);	// 数字前面补0
round($num, 2);	// 四舍五入，保留两位小数
base_convert(number,frombase,tobase);	// 进制转换
bcsub($left, $right, 2); // 将两个高精度的数字相见，第三个参数表示结果的小数点位数

3 / 2 = 1; // 除法取商
3 % 2 = 1; // 除法取余

bin2hex("test");	// 字符串转16进制
hex2bin('843769807'); // 16进制转字符串
```

### 时间

```php
time(): 获取当前时间戳，秒，10位数
microtime(); # 获取毫秒时间
strtotime('2021-12-16 00:00:00'): 字符串转换为时间戳
gmdate("Y-m-d\TH:i:s\Z"): 获取GMT时区的时间

$beginToday=mktime(0,0,0,date('m'),date('d'),date('Y')):获取今天开始时的时间戳
$endToday=mktime(0,0,0,date('m'),date('d')+1,date('Y'))-1:获取今天结束时的时间戳
$beginYesterday=mktime(0,0,0,date('m'),date('d')-1,date('Y'))：获取昨天开始时的时间戳
$endYesterday=mktime(0,0,0,date('m'),date('d'),date('Y'))-1：获取昨天结束时的时间戳
$beginLastweek=mktime(0,0,0,date('m'),date('d')-date('w')+1-7,date('Y'))：获取上周开始时的时间戳
$endLastweek=mktime(23,59,59,date('m'),date('d')-date('w')+7-7,date('Y'))：获取上周结束时的时间戳
$beginThismonth=mktime(0,0,0,date('m'),1,date('Y'))：获取本月开始时的时间戳
$endThismonth=mktime(23,59,59,date('m'),date('t'),date('Y'))：获取本月结束时的时间戳
# 单独获取当前的年、月、日、时、分、秒等
date('Y-m-d H:i:s'); // 如果要单独获取或者修改格式，那么直接按照里面的格式修改即可
# 输出指定格式
date('Y-m-d H:i', time())

# 时间的表示
d: 月份中的第几天，有前导零的2位数字，01到31
D: 星期中的第几天，文本表示，3个字母，Mon 到 Sun
j: 月份中的第几天，没有前导零，1 到 31
l:（“L”的小写字母），星期几，完整的文本格式	Sunday 到 Saturday
N: ISO-8601 格式数字表示的星期中的第几天（PHP 5.1.0 新加），1（表示星期一）到 7（表示星期天）
S: 每月天数后面的英文后缀，2 个字符，st，nd，rd 或者 th。可以和 j 一起用
w: 星期中的第几天，数字表示	0（表示星期天）到 6（表示星期六）
z: 年份中的第几天	0 到 365
星期	---	---
W	ISO-8601 格式年份中的第几周，每周从星期一开始（PHP 4.1.0 新加的）	例如：42（当年的第 42 周）
月	---	---
F	月份，完整的文本格式，例如 January 或者 March	January 到 December
m	数字表示的月份，有前导零	01 到 12
M	三个字母缩写表示的月份	Jan 到 Dec
n	数字表示的月份，没有前导零	1 到 12
t	指定的月份有几天	28 到 31
年	---	---
L	是否为闰年	如果是闰年为 1，否则为 0
o	ISO-8601 格式年份数字。这和 Y 的值相同，只除了如果 ISO 的星期数（W）属于前一年或下一年，则用那一年。（PHP 5.1.0 新加）	Examples: 1999 or 2003
Y	4 位数字完整表示的年份	例如：1999 或 2003
y	2 位数字表示的年份	例如：99 或 03
时间	---	---
a	小写的上午和下午值	am 或 pm
A	大写的上午和下午值	AM 或 PM
B	Swatch Internet 标准时	000 到 999
g	小时，12 小时格式，没有前导零	1 到 12
G	小时，24 小时格式，没有前导零	0 到 23
h	小时，12 小时格式，有前导零	01 到 12
H	小时，24 小时格式，有前导零	00 到 23
i	有前导零的分钟数	00 到 59>
s	秒数，有前导零	00 到 59>
u	毫秒 （PHP 5.2.2 新加）。需要注意的是 date() 函数总是返回 000000 因为它只接受 integer 参数， 而 DateTime::format() 才支持毫秒。	示例: 654321
时区	---	---
e	时区标识（PHP 5.1.0 新加）	例如：UTC，GMT，Atlantic/Azores
I	是否为夏令时	如果是夏令时为 1，否则为 0
O	与格林威治时间相差的小时数	例如：+0200
P	与格林威治时间（GMT）的差别，小时和分钟之间有冒号分隔（PHP 5.1.3 新加）	例如：+02:00
T	本机所在的时区	例如：EST，MDT（【译者注】在 Windows 下为完整文本格式，例如“Eastern Standard Time”，中文版会显示“中国标准时间”）。
Z	时差偏移量的秒数。UTC 西边的时区偏移量总是负的，UTC 东边的时区偏移量总是正的。	-43200 到 43200
完整的日期／时间	---	---
c	ISO 8601 格式的日期（PHP 5 新加）	2004-02-12T15:19:21+00:00
r	RFC 822 格式的日期	例如：Thu, 21 Dec 2000 16:01:07 +0200
U	从 Unix 纪元（January 1 1970 00:00:00 GMT）开始至今的秒数	参见 time()
```

##### [Carbon时间处理第三方库](https://haofly.net/php-carbon)

### 文件/文件夹/目录操作

```php
$fp = fopen("test", "r") or die("Unable to open file!");	# 打开文件
$fp = fopen('test', 'w')	# 写入
fread($fp,filesize("webdictionary.txt"));	# 读取指定大小的内容
fgetc($fp)		# 读取一个字符
fgets($fp)		# 读取一行
feof($fp)		# 判断指针是否指向文件尾了
fwrite($fp, 'haofly')	# 写入字符串到文件
fclose($fp);	# 关闭文件
file_exists($filename);	# 检查文件或目录是否存在
is_writable($name);	# 检查文件或者目录是否有写入权限

dirname(__FILE__);	# 获取上级目录所在的绝对路径
  
// 遍历目录下的文件
$handler = opendir($dir);
while ($filename = readdir($handler)) {
  if ($filename != '.' && $filename !='..' && is_file($dir . '/'. $filename)) {
    $files[] = $filename;
  }
}
closedir($handler);
```

### 函数/类/对象

- `(array) myobj`对象可强制转换为数组
- 创建空对象: `new stdClass()`
- 对象转数组: `(array) myClass`
- 类的静态常量使用`const`关键字定义
- 7.2开始允许重写抽象方法
- 7.4开始可以给类属性指定类型了，例如:`private int $id;`
- 7.4开始支持直接用箭头的简写的匿名函数，例如: `$nums = array_map(fn($n) => $n * $factor, [1, 2, 3, 4]);`

```php
# public, private, projtected的区别:
public # 权限最多，可以内部调用，实例调用
protected	# 受保护类型，用于本类和继承类调用
private		# 私有类型，只有在本类中使用
  
# PHP7终于支持lambda了，使用的是fn关键字
array_map(fn($n) => $n * 2, [1, 2, 3]);

# PHP7支持类属性指定类型
class Post {
  public int $id;
  public string $name;
  // 指定方法的返回类型
  public function test(): A {
    return a;
  }
}
  
# 对象的序列化和反序列化
serialize()
unserialize()
  
# 一些自省(反射)方法
func_get_args()					# 获取当前方法所有的参数
get_class(className)			# 取得当前语句所在的类名
get_class_methods(className)	# 取得相应class所包含的所有的方法名
get_class_vars(clasName)		# 取得相应class所包含的所有的变量名
get_object_vars($object)		# 获取类或者对象的属性，返回数组
property_exists($object, $key)	# 类或者对象是否存在某个属性
setAttribute($name, $value)		# 设置函数的属性或者直接设置函数的内部变量
$this->{$key} = $value			# 给类动态添加属性
$this->{$key}					# 返回对象指定的属性

# 根据类名知道类的定义文件
$reflector = new ReflectionClass('className');
echo $reflector->getFileName();

# 标准嘞StdClass
$obj->value # 直接获取其内部的变量
  
# trait: 一种代码复用机制，从基类继承的成员会被trait插入的成员所覆盖，优先顺序是来自当前类的成员覆盖了trait的方法，而trait则覆盖了被继承的方法。这是为了弥补PHP单继承的局限。trait虽然不能继承trait，但是可以组合使用，跟继承类似，两个trait里面的方法都会有，并且可以用insteadof方法选择重名的方法该使用哪一个，如果有重名不选择的话则会出现致命错误
# 例如可以写一个单例:
trait SingleInstance
{
  static private $instance = null;
  static public function getInstance(){
    if (!self::$instance) {
      self::$instance = new static();
    }
    return self::$instance;
  }
}
# 在其他类里面只需要use SingleInstance就行了。再比如，文档里面的例子
<?php
class Base {
    public function sayHello() {
        echo 'Hello ';
    }
}

trait SayWorld {
    public function sayHello() {
        parent::sayHello();
        echo 'World!';
    }
}

class MyHelloWorld extends Base {
    use SayWorld;
}

$o = new MyHelloWorld();
$o->sayHello();		// 输出的是Hello World
```

#### 类的继承

```php
class ChildClass extends ParentClass {
  public function __contruct() {
    parent::__construct();	// 调用父类的构造函数
  }
}
```

### Type hint

```php
function foo(?Type $a, 	// 声明参数$a的类型，问号表示可以为null
             Type|null $b // 同上
) {}

/* @var @objs Test[] */	// 这样可以声明一个数组内部元素的类型
foreach ($objs as $obj) {}
```

### 发送CURL请求

- 注意使用CURL之前一定要先确定服务器是否已经安装php的curl扩展，如果没有，可能会报奇怪的错误，安装完扩展后记得重启php进程。
- PHP curl中的每一个设置项都有一个唯一的数值与其对应，如果要`var_dump`一个`curl`对象，打印出来的就是这些数值，数值都应可以参考`https://www.kancloud.cn/baibaoyun/developer/312099`

```php
$ch = curl_init();								// 初始化curl
curl_setopt($ch, CURLOPT_URL, 'url');			// 设置URL
curl_setop($ch, CURLOPT_POST, true);			// 发送POST请求
curl_setop($ch, CURLOPT_POSTFIELDS, $data);		// POST的数据
curl_setop($ch, CURLOPT_RETURNTRANSFER, true);	// 获取返回结果，如果不加这个，那么$result=true
$result = curl_exec($ch);						// 执行curl请求
curl_getinfo($ch, CURLINFO_HTTP_CODE)			// 获取http_code
  
curl_setopt($curlHandle, CURLOPT_HTTPHEADER, ['Accept: application/json']);	// 添加HTTP头
curl_close($ch);								// 关闭连接

# 如果要通过CURL 上传文件，那么需要这样对$data进行处理
if (function_exists('curl_file_create')) { // php 5.6+
  $cFile = curl_file_create($scriptPath);
} else { //
  $cFile = '@' . realpath($scriptPath);
}
$data = ['file' => $cFile];

# 获取curl所有参数所代表的常量值
$arr = get_defined_constants(true);
var_dump($arr['curl']);
```

项目中，强烈推荐使用第三方库`Guzzle`，来实现http请求。该库不仅支持curl，而且支持socket等多种底层实现，在没有curl的情况下也可以发送请求，并且实现了发送文件、同步异步等多种方式。

### WEB程序

```php
$_SERVER['REQUEST_METHOD']	# 返回数据提交的方式，GET、POST等
$_SERVER["SERVER_PORT"] 	# 获取端口
$_SERVER['HTTP_HOST']		# 获取域名或主机地址
$_SERVER['SERVER_NAME']		# 获取域名或主机名
$_SERVER["REQUEST_URI"]		# 获取域名后的详细地址
$_SERVER['PHP_SELF']		# 获取PHP文件名
$_SERVER["QUERY_STRING"]	# 获取网址后的参数
$_SERVER['HTTP_REFERER']	# 获取来源url
parse_str(file_get_contents("php://input"),$post_vars); # 获取PUT数据
getallheaders		# 获取请求头
error_log('message')	# 把错误信息发送到web服务器的错误日志，或者到一个文件里，有长度限制

ob_start();		# 打开输入输出缓冲，打开后，脚本会将输出缓冲起来直到ob_flush()
session_save_path("/var/lib/php/session");	# 更改session路径
session_save_path();	# 获取session路径

header('Content-Type: text/css'); // 直接设置响应的header头
```
### MySQL
```php
mysql_errno();	# 打印SQL出错信息
```

### 异常处理

- 有时候，我们会发现`catch`不到`Exception`或者`Error`，可能的原因是使用了`set_error_handler`等函数进行了错误的单独捕获，还可以使用`register_shutdown_function`注册程序退出时候的回调函数

- 7.1开始能够同时捕获多个异常

  ```php
  try {
      // some code
  } catch (FirstException | SecondException $e) {
      // handle first and second exceptions
  }
  ```

- `error_log`打印日志到php的错误日志中去，配置在`php.ini`中的路径

```php
var_dump(debug_backtrace());	# 随时打印当前的调用栈

try{
	throw new Exception('soahg');
}catch(Exception $e){
	echo $e->getMessage();
}
```

### PHP命令行

```shell
php --ini		# 查看php的配置文件
php --ri xhprof	# --ri可以显示php当前加载的扩展的信息
php -r "var_dump('abc');"	# 直接在命令行执行php语句
```

### 帮助函数

```php
gettype(): 获取变量类型
$obj instanceof A # 判断对象是否属于某个类，不过判断是不是数组只能用is_array()	# 判断是否是数组
is_string()	# 判断是否是字符串
is_object()	# 判断是否是object
is_bool()	# 是否是布尔值
is_int()	# 是否是整数
is_integer()# 是否是整数
is_float()	# 是否是浮点数
is_real()	# 是否是实数
is_numeric	# 是否是数字或者数字字符串

$_ENV	# 获取环境变量
    
interface_exists()	# 检查接口是否已经定义
class_exists()		# 检查类是否已经定义
  
PHP_INT_MAX	# 最大整数
PHP_INT_MIN	# 最小整数
min($value1, $value2...)	# 选出最小值，最大值max同理
min([$value1, $value2,...])	# 选出最小值，最大值max同理
  
hash_hmac(算法名, 明文, 盐)	# hash加密函数，可以选定加密算法，例如hash_hmac('sha1', 'mingwen', 'salt')
```
- **@操作符**: 错误控制运算符，写在一行的前面，可以控制改行不输出warning信息或错误信息
- **var_dump(变量名)**：打印变量，这个函数还会打印变量的类型可以把一个变量的各个部分全部信息输出，包括每个部分的数据类型和长度等信息，但是默认情况下，输出有限制，如果层数深了或者数据长了可能会表示成省略号，可以在`C:\wamp\bin\apache\\apache2.4.9\bin\php.ini`里面修改xdebug节点，添加如下内容

   xdebug.var_display_max_children=128
   ​	xdebug.var_display_max_data=512
   ​	xdebug.var_display_max_depth=5
   另外，将var_dump的输出转换为一个字符串以便web前端显示，可以这样用：
   ​	ob_start();
   ​	var_dump($data);
   ​	$result = ob_get_clean();
   ​	# 或者用另外的函数
   ​	var_export: 输出或返回一个变量的字符串表示
- **file_get_contents**：获取文件或http内容，如果要从http获得json数据可以直接使用它
- **isset()**：查看某个变量或者多个变量是否已经被定义，未赋值或赋NULL都会返回false。没错，可以直接检查多个变量，当所有变量都为true时返回true
- **@header('Content-type: text/html;charset=UTF-8');**PHP文件中添加中文支持，在脚本开始的地方添加给行即可
- **多行输出**：其中最后一个EOF必须写在一行的开头，且里面如果要用变量这样用{ $php_var }
   echo <<<EOF
   ​	内容
   ​	EOF;
- **print_r**:打印关于变量的易于理解的信息。如果给出的是 string、integer 或 float，将打印变量值本身。如果给出的是 array，将会按照一定格式显示键和元素。这点在调试的时候很有用
- **类的方法尽量写成static，速度比public快**

## composer包管理

[Composer中文文档](https://docs.phpcomposer.com/)

- `--prefer-dist`会下载.zip压缩包，并缓存到本地。`--prefer-source`会下载源代码，不会缓存到本地，适合需要修改源代码的时候。
- `--ignore-platform-reqs`表示忽略平台某些依赖的限制，例如`ext-zip`的依赖，如果真的不需要就直接在`install`的时候加上这个参数吧
- 如果`composer`频繁出现`.json 404 not found`，那么可以考虑不再使用国内的这个镜像`https://packagist.phpcomposer.com`，可以修改镜像地址为:`composer config -g repo.packagist composer https://packagist.laravel-china.org`，或者干脆不用国内镜像

`require`是指在生产环境中必须的包，而`require-dev`则是开发的时候要用而生产环境无需用的包，常用命令:

```shell
composer config --list	# 列出当前所有的配置
composer show 	# 获取所有安装的包的列表
composer require package_name --dev	# 安装包，并将其写入composer.json的require-dev中去
composer required package_name ~1.2.0	# 指定版本
composer remove package_name	# 移除包
composer config -g repo.packagist composer https://packagist.phpcomposer.com	# 更换为国内的源
composer config repositories.mypkg composer https://ppkg.haofly.net	# 增加源，并写入composer文件中的repositories字段
composer config -g --unset repos.packagist	# 删除指定仓库

# 忽略ssl证书验证
composer config --global disable-tls true
composer config --global secure-http false
"package/ppkg": "2.7.*@beta"	# 安装beta版

rm -rf ~/.composer/cache	# 清除缓存

# 版本约束符号
~1.2.3	# ~表示定义了最小的小版本号，并且允许最后以为版本号进行升级，相当于>=1.2.3并且<1.3.0
^1.2.3	# ^表示允许升级到安全的版本，相当于>=1.2.3并且<2.0.0

# composer太慢解决方法
composer self-update	# 首先更新composer本身
composer global require hirak/prestissimo	# 然后安装平行安装工具，但是效果感觉不是很明显
composer clear-cache
composer -vvv	# 这句话要单独执行一次
composer update --no-dev --prefer-dist -vvv	# 加入这个看看日志

# 对于需要使用git拉取私有composer包的，可以这样设置github access token，访问https://github.com/settings/tokens生成一个
composer config -g github-oauth.github.com XXXXX
```

### composer事件脚本

composer在执行的时候会在时间点上都会抛出相应的事件，可以添加脚本在事件触发后自动执行。例如:`pre-install-cmd/post-update-cmd(update命令执行后触发)`，而脚本的定义，可以直接放在`composer.json`中，例如一个典型的`Laravel`项目的脚本

```json
"scripts": {
    "post-root-package-install": [
        "php -r \"copy('.env.example', '.env');\""	// 复制文件命令
    ],
    "post-create-project-cmd": [
        "php artisan key:generate"
    ],
    "post-install-cmd": [	// composer install命令执行后触发
        "Illuminate\\Foundation\\ComposerScripts::postInstall",
        "php artisan optimize"
    ],
    "post-update-cmd": [	// composer update命令执行后触发
        "Illuminate\\Foundation\\ComposerScripts::postUpdate",
        "php artisan optimize"
    ]
}
```

### autoload

`autoload`，可以预加载类，自动索引所有的类，能够加快依赖的索引速度。但是autoload并不是实时更新的，如果发现`vendor/composer/autoload_classmap.php`中的类与你预想的有冲突，那么就需要更新一下了：`composer dump-autoload`。

在`composer.json`中有四种自动加载类型。PSR的各个规范可以参考[PizzaLiu/PHP-FIG](https://github.com/PizzaLiu/PHP-FIG):

- classmap: `development`相关的

  ```php
  {
    "classmap": ["src/"]	# 这样composer就会读取这个文件夹下所有的文件，然后再vendor/composer/autoload_classmap.php中将所有的class的namespace+classname生成一个key=>value的数组
  }
  ```

- psr-0: 已经被弃用

- psr-4: 一般用于项目代码的自动加载。需要注意的是除去命名空间前缀的其他子命名空间必须和文件目录相对应。子目录里面的命名空间，就把子目录一同写到命名空间中去。

- files: `helper`相关的

### Extension扩展管理

php的扩展大多可以通过`pecl install packagename`直接进行安装(有些库还是需要先安装源文件，再用pecl进行链接)，可以使用`yum install php-pear`命令安装`pecl`工具

```shell
var_dump(extension_loaded('curl'));		// 查看是否安装某个模块
var_dump(get_loaded_extensions());		// 查看安装了哪些模块

apt-get install php7.4-mbstring	# 安装ext-mbstring扩展
apt-get install php7.4-xmlprc php7.4-xmo 	# 安装ext-dom扩展
apt-get install php-bcmeth # 安装bcmath扩展
```

## 线程/协程/进程

### 迭代器

PHP的迭代器和其他语言的迭代器用法基本相同。

```php
// 迭代器的while循环
while ($it->valid())
{
    $key = $it->key();
    $value = $it->current();
    // ...
    $it->next();
}
```

## PHP配置

配置文件主要放置在`php.ini`，在mac上面，php的默认配置在`/etc/php.ini.default`，如果需要修改，可以自己新建`/etc/php.ini`将需要修改的配置写入其中即可。下面是常见的配置

```shell
upload_max_filesize	= 2M 	# 允许上传的文件最大大小
post_max_size = 8M # 允许发送POST数据的最大大小
```

另外，在PHP代码中可以这样设置和获取配置

```shell
ini_get('upload_max_filesize'); // 但是该属性只能获取，不能在代码里进行设置
```

## 非常好用的第三方库

## TroubleShooting

- **Call to undefined function getallheaders()**  

  版本问题，如果是老版本可以使用如下代码代替

  	if (!function_exists('getallheaders')) { 
  		function getallheaders() { 
  			foreach($_SERVER as $key=>$value) { 
  				if (substr($key,0,5)=="HTTP_") { 
  					$key=str_replace(" ","-",ucwords(strtolower(str_replace("_"," ",substr($key,5))))); 
  					$out[$key]=$value; 
  				}else{ 
  					$out[$key]=$value; 
  				} 
  			} 
  			return $out; 
  		} 
  	}

- **回掉函数中访问外部变量**

  方法一：使用类的静态变量

  方法二：使用use语法

  ```php
  $dt->each(function() use($bianliang) {
    echo $bianliang;
  });
  ```

- **Error while reading line from server**

  这是在使用predis时报的错误，原因是没有设置`read_write_timeout=－1`使redis保持永久连接，否则会在一定时间后断开连接

- `isset`和`empty`判断变量是否存在的问题。都不能用于静态数组变量的判断，最好用`array_key_exists`

- **PHP调用Dubbo服务**: 按照这个教程一步一步来http://www.huangxiaobai.com/archives/1437。

- **PHP Fatal error:  Allowed memory size of 268435456 bytes exhausted (tried to allocate 130968 bytes) in …**: PHP作为daemon程序运行时候经常性出现内存溢出问题，并且这种错误程序是不会退出的，只会卡在那里，supervisor也不会发现程序的异常。首先检查为什么内存溢出，如果是有大量的curl请求，那么有可能是请求未释放或者curl本身的问题(curl 7.19.7在网上有说是有ssl内存溢出漏洞的)。如果实在想不到，那么可以这样做，使用`memory_get_peak_usage(true)`函数判断当前的内存使用量，当快达到阈值(php.ini中有设置，一般为256MB，top出来显示的内存比这个高一点)的时候，主动退出程序或者退出循环，销毁变量，重新开启循环。可以通过`valgrind`来辅助调试内存泄漏问题。
  另外在执行`composer`的时候也会出现类似的错误，可以这样子执行`php -d memory_limit=-1 composer update`直接不限制

- **从数据库取出的整型数据变成了字符串**: php5.3之前，php连接mysql的驱动是`libmysqlclient`，5.3开始`mysqlnd`内置于PHP中了，新的驱动就不会出现这种情况了

- **Cannot find autoconf. Please check your autoconf installation and the $PHP_AUTOCONF environment variable. Then, rerun this script.** `yum install autoconf`

- **fatal error: pcre.h: No such file or directory**: `yum install pcre-devel/sudo apt-get install libpcre3-dev`

- **PDOException "could not find driver"**: 安装`php-mysql/php5-mysql/php7-mysql`扩展

- **Composer报错`Failed to decode response: zlib_decode(): data error`**: 出现在更换源之后，这时候应该先执行`composer clear-cache`

- **Class 'Maatwebsite\Excel\Excel' not found**: 尝试升级该依赖`composer require maatwebsite/excel:^3.0.1`

- **PHP实现startsWith和endsWith功能**: 不过`Laravel`框架自带了这两个函数的

  ```php
  function startsWith( $haystack, $needle ) {
       $length = strlen( $needle );
       return substr( $haystack, 0, $length ) === $needle;
  }
  
  function endsWith( $haystack, $needle ) {
      $length = strlen( $needle );
      if( !$length ) {
          return true;
      }
      return substr( $haystack, -$length ) === $needle;
  }
  ```

- **pecl安装扩展出现Please reinstall the libzip distribution**: `apt-get install libzip-dev / yum install libzip-devel`

- **zlib.h: no such file or directory**: 需要先安装: `apt-get install libz-dev -y`

- **Could not scan for classes inside “vendor/google/apiclient/src/Google” which does not appear to be a file nor a folde**: 看起来是[googleapis/google-api-php-client](https://github.com/googleapis/google-api-php-client)库升级导致的，有这个路径的最高版本为2.7.2，2.8之后就没有src/Goolge了

- **class not found**: 如果是自己写的某个类没找到可能是没有require进来，我们在使用namespace的时候光用namespace是不够的，namespace只是表明其名称空间，require才能把代码引入进来，之所以我们使用框架不会报错，因为我们在框架的入口之行了`require __DIR__.'/../vendor/autoload.php'`的

- **file_get_contents报错505 HTTP Version Not Supported error**: 把请求的url打印出来，多半是`url``没有`encode`

- **Call to undefined function curl_init()**: 需要安装`php_curl`扩展: `apt install php-curl -y`

- **No valid bower.json was found in any branch or tag of**: 尝试给composer添加github access token，上文有提到

- **PHP安装SOAP扩展/docker容器安装php-soap扩展**: 

  ```shell
  yum install php-soap	# centos系统php-soap扩展
  apt-get install php-soap	# debian系统安装php-soap扩展
  apt-get update -y && apt-get install -y libxml2-dev && apt-get clean -y && docker-php-ext-install soap	# docker容器安装php-soap扩展
  php -m | grep soap	# 查看是否安装完成
  ```

- **composer.json丢失**: 目前没有一个简单的方法从`composer.lock`或者`vendor`反向生成`composer.json`，可以尝试这样做:

  ```shell
  composer init	# 初始化一个composer.json出来
  composer show --installed	# 将列出来的包以及版本一个一个粘贴回去
  ```

- **SMTP connect() failed**: 可能是端口不对，现在大部分邮件都只支持ssl协议了，端口号一般是465

- **Call to undefined function imagetypes()**: 没有安装gd扩展: `apt-get install libpng-dev && php7.4-gd -y`

##### 扩展阅读

- [DuckChat](https://github.com/duckchat/gaga): 一款独立部署的聊天系统
- [WSDL转PHP代码](https://www.wsdltophp.com/)