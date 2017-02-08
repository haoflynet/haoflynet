---
title: "PHP 教程"
date: 2013-08-07 02:02:30
updated: 2017-02-02 10:21:21
categories: php
---
# PHP

## 基本语法
### 数组
```php
array_chunk($array, $size): 将数组按size大小分为多个数组
array_diff($a, $b): 比较数组的不同，可以用来判断两个数组是否相等，需要注意的是这里返回的是在array1中但是不在array2中的值，而不是两个的交集
array_key_exists("key",$a)  # 查看key是否存在于某个字典
array_merge()			# 合并数组，相同的key直接覆盖
array_merge_recursive()	# 合并数组，相同的key不覆盖
array_push($source, "red", "gree")	# 给数组添加元素
array_search(): 搜索一个key的索引
array_search(strtolower($search), array_map('strtolower', $array)): array_search忽略大小写
array_slice($arr, 0, 1) # 数组分片
array_sum($arr): 计算数组中所有值的和
count()函数：输出数组的长度
empty()函数：判断数组是否为空
end()		// 返回当前数组的最后一个值，需要注意的是这个函数不仅仅是返回最后一个值，还会把数组当前的指针指向最后一个数据
implode(',', $arr)	# 将数组拼接成字符串
in_array('a', $a)				# 查看数组是否存在某个元素
json_encode($arr)	# 数组转换城字符串
rsort(): 以降序对数组排序
sort()：排序，可以给数组排序
uasort($array, $cmp_function)	# 定义对比函数进行排序
unset(arr[1]): 删除数组元素

foreach($array as $value): 数组遍历
foreach($array as $key => $value): 数组(字典)遍历
func(*list): 将数组作为函数的输入
  
# 在数组里面添加数组元素，在不确定key的情况下
$arr = [];
$arr['a'][] = 'a';
$arr['a'][] = 'b';
```

### 字符串
```php
json_decode(string, $assoc=false)	# 将字符串转换为json对象,$assoc=true时返回array而不是object
mb_strlen($str, 'utf-8') # 求中文字符串长度
mb_substr($str, $start, $length, 'utf-8'): 字符串分割，可以分割中文哟，如果要获得所有右边的，那么$length不用填或者填上NULL，如果版本不行那就是用功能弱一点的substr
nl2br() # 将字符串中的\n转换成网页的换行符<br>
strlen() # 求字符串长度
str_replace(搜索值，替换值，目标)	# 字符串替换

strpos('abc', 'a'): 在字符串中查找第一次出现位置，没找到返回false
$a . $b . 'abc':字符串连接直接用点号
explode(',', $str)	# 字符串分割，第三个参数大于0表示限制分组数量
array_map('strrev', explode('-', strrev($a), 2))	# 字符串分割，逆向
iconv('utf-8', 'GBK', $data): 将字符编码从utf-8转换为GBK
join("&", $arr)	# 拼接字符串
parse_str('name=wang&age=18'): 从查询字符串中解析到变量，可以得到$name和$age两个变量
preg_replace('/user_id=\d+&name=/', 'user_id=' . 1048 . '&name=', $code): 正则替换
preg_replace_callback('//', function($matches){return strtolower($matchs[0])}: 执行一个正则表达式搜索并且使用一个回调函数进行替换
preg_match('/Chongqing(?<right>.*)/', $string, $matches): 正则匹配，pattern参数前后必须加斜杠
sprintf("sahgoiahg%s", $a): 格式化输出
strtolower($str)/strtoupper($str): 大小写字符串
ucfirst($str): 将字符串首字母大写
ucwords($str): 将字符串每个单词首字母大写
```
### 数字
```php
ceil()函数：向上取整
rand(min, max)：产生随机数，不需要给初始值了现在
intval($val): 字符串转整数
int ip2long(string $ip_address)：IP转换成整数值
string long2ip(string $proper_address)：整数值转换成IP
number_format(float $number)	// 以千位分隔符方式格式化一个数字，返回字符串
sprintf('%04d', 2)	// 数字前补零
```

### 时间
	time(): 获取当前时间戳
	strtotime(''): 字符串转换为时间戳
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

### 函数/类/对象

```php
# public, private, projtected的区别:
public # 权限最多，可以内部调用，实例调用
protected	# 受保护类型，用于本类和继承类调用
private		# 私有类型，只有在本类中使用
  
# 对象的序列化和反序列化
serialize()
unserialize()
  
# 一些自省(反射)方法
get_class(className)			# 取得当前语句所在的类名
get_class_methods(className)	# 取得相应class所包含的所有的方法名
get_class_vars(clasName)		# 取得相应class所包含的所有的变量名
func_get_args()					# 获取当前方法所有的参数
setAttribute($name, $value)		# 设置函数的属性或者直接设置函数的内部变量

# 根据类名知道类的定义文件
$reflector = new ReflectionClass('className');
echo $reflector->getFileName();

# 标准嘞StdClass
$obj->value # 直接获取其内部的变量
  
# trait: 一种代码复用机制，从基类继承的成员会被trait插入的成员所覆盖，优先顺序是来自当前类的成员覆盖了trait的方法，而trait则覆盖了被继承的方法。这是为了弥补PHP单继承的局限
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
?>
```

### 发送CURL请求

[字段参考](http://php.net/manual/zh/function.curl-setopt.php): 可实现各种action操作，以及异步等操作

### WEB程序

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
### MySQL
	mysql_errno():	# 打印SQL出错信息

### 异常处理
	try{
		throw new Exception('soahg');
	}catch(Exception $e){
		echo $e->getMessage();
	}

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

interface_exists()	# 检查接口是否已经定义
class_exists()		# 检查类是否已经定义
  
PHP_INT_MAX	# 最大整数
PHP_INT_MIN	# 最小整数
```
- **@操作符**: 错误控制运算符，写在一行的前面，可以控制改行不输出warning信息或错误信息
- **var_dump(变量名)**：打印变量，这个函数还会打印变量的类型可以把一个变量的各个部分全部信息输出，包括每个部分的数据类型和长度等信息，但是默认情况下，输出有限制，如果层数深了或者数据长了可能会表示成省略号，可以在`C:\wamp\bin\apache\\apache2.4.9\bin\php.ini`里面修改xdebug节点，添加如下内容

  	xdebug.var_display_max_children=128
  	xdebug.var_display_max_data=512
  	xdebug.var_display_max_depth=5
  另外，将var_dump的输出转换为一个字符串以便web前端显示，可以这样用：
  	ob_start();
  	var_dump($data);
  	$result = ob_get_clean();
  	# 或者用另外的函数
  	var_export: 输出或返回一个变量的字符串表示
- **file_get_contents**：获取文件或http内容，如果要从http获得json数据可以直接使用它
- **isset()**：查看某个变量是否已经被定义，未赋值或赋NULL都会返回false
- **@header('Content-type: text/html;charset=UTF-8');**PHP文件中添加中文支持，在脚本开始的地方添加给行即可
- **多行输出**：其中最后一个EOF必须写在一行的开头，且里面如果要用变量这样用{ $php_var }
  	echo <<<EOF
  	内容
  	EOF;
- **print_r**:打印关于变量的易于理解的信息。如果给出的是 string、integer 或 float，将打印变量值本身。如果给出的是 array，将会按照一定格式显示键和元素。这点在调试的时候很有用
- **类的方法尽量写成static，速度比public快**


## composer包管理
`require`是指在生产环境中必须的包，而`require-dev`则是开发的时候要用而生产环境无需用的包，常用命令:

```php
composer config --list	# 列出当前所有的配置
composer show 	# 获取所有安装的包的列表
composer require package_name --dev	# 安装包，并将其写入composer.json的require-dev中去
```

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

  ​