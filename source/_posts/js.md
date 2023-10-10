---
title: "JavaScript & Ajax & jQuery & NodeJS 教程"
date: 2015-02-07 11:52:39
updated: 2023-08-24 08:18:00
categories: frontend
---
# JavaScript & Ajax & jQuery

TODO: 逐步用原生方法替换jQuery，参考[You-Dont-Need-jQuery](https://github.com/oneuijs/You-Dont-Need-jQuery#query-selector)

- 判断是否是非数字: `isNaN(a)`
- 生产环境直接全局屏蔽掉`console.log`的输出，只需要复写即可:`console.log=()=>{}`
- 包含关系(超集): TypeScript > ES2016 > ES2015 > ES5
- 常用CDN
  - [cdnjs](https://cdnjs.com/)

## 基本语法

- `?.`可选链`optionalChaining`，`a?.b`，表示如果a对象存在那么取`a.b`属性，否则直接返回`null`，而不会因为找不到属性报错，但是这个语法在`vue2`的`template`中无法使用。这居然是14.x才开始能用的
- `??`双问号，`a ?? b`，如果左边的值为`null`或者`undefined`，那么就返回右边的值，需要注意的是左边为`false`的时候依然是左边的值
- js也是有switch语句的
- `if`条件语句如果有逗号，其实是按照最后一个值作为判断的: `if (a = '123', b = '234', a > b)`

### 变量

- 获取变量所占用的内存大小可以使用[object-sizeof](https://www.npmjs.com/package/object-sizeof)

```javascript
var $a;	// es6以前定义变量，if (true) {var a = 1;} console.log(a); 输出为1
let $b;	// es6用于定义跨级作用域本地变量，if (true) {let b = 1;} console.log(b);输出为undefined
const $c;	// 定义常量
window.test = 123;	// 声明全局变量
a = {...b}	// 变量克隆

const [a, ...b]	= [1, 2, 3, 4]	// a=1, b=4	解构赋值
```

<!--more-->

### 对象/字典

```javascript
object instanceof constructor	// 判断某个对象是否属于某个类
var copyObj = Object.assign({}, original_obj);	// 对象的深拷贝，直接用等于赋值是浅拷贝
var copyObj = Object.assign({}, new Obj); // 直接将字典赋值给对象，或者叫拷贝对象
Object.keys(obj);	// 获取对象所有的key，返回一个数组
Object.values(obj); // 获取对象所有的value，返回一个数组
Object.entries(obj); // 获取对象所有的键值对，返回一个数组，例如{a:123,b:233}, 会返回['a':123], ['b': 233]
Object.keys(obj).length == 0; // 判断对象是否为空
Object.assign({}, {}); // 合并两个对象/合并两个字典
"key" in obj	// 判断对象是否包含某个key

var a = {}
a[abc] = 'def';	// 变量作为字典名
var a = {
  [abc]: 'def',	// 或者这样将变量做为字典名，变量作为key
  [`${a}`]: 'def',
}
```

### 数组

```javascript
Array.from('abc')	// 会得到['a', 'b', 'c']
Array.from(['abc', 'def']) // 会得到['abc', 'def']
Array.from([1, 2], x => x+ x) // 会得到[2, 4]
Array.from({length:10},(item, index)=> index+1)	// 快速生成指定长度的数组
let myArr: number[] = []	// typescript中定义一个number数组
arr = [...arr1]	// 克隆/复制数组
arr = [...arr1, arr2]	// 合并数组
arr = [...'hello']	// 把字符串作为数组

arrA.concat(arrB)			// 合并两个数组，会生成一个新的数组
arr.indexOf('元素')			// 获取某个元素在数组中的下标，查看某个元素是否存在于数组中，没有在返回－1
arr.includes('元素');		// 判断数组是否包含某元素
JSON.stringify(Array)		// 将数组转换为JSON格式的字符串
arr.toString(): 数组转字符串，中间会自动加上逗号
arr.join(''): 数组转字符串，分隔符可自定义
arr.push(obj)		// 在数组尾部添加元素
arr.push(...arr2)	// 合并两个数组，追加到数组尾部
arr.pop(obj)		// 去除数组尾部元素
arr.unshift(obj)	// 在数组头添加元素
arr.shift(obj)		// 去除数组头部元素
arr.slice(start, end) // 数组分片
arr.slice(-1)[0] // 获取数组最后一个元素，还可以这样定义[ , lastItem] = arr
arr.sort()	// 自动对数组进行排序(从小到大)，可以提供一个比较函数arr.sort(function (a, b) {return a > b ? 1 : -1})，特别需要注意的是这里只能返回1,-1和0，不能返回布尔值，否则会有意料之外的结果
arr instance of Array	// 判断是否是数组
arr.filter(Boolean)	// 快速移除所有"false"类型(false、null、undefined等)的元素

// 遍历数组方法
for (var index in arr) {}	// 注意这里的循环变量不是数组元素而是索引
a.forEach(function(value, key, arr) {}); 
arr.map((value) => {console.log(value); return newValue;}) // 返回值为一个新的数组，原数组不会改变
arr.filter(function(value, key, arr) {return true}); // 返回新数组，如果元素返回true则保留，返回false则抛弃
arr.some(function(value, key, arr){});	// 筛选数组，如果返回true则停止循环。返回布尔值，表示是否有满足条件的
arr.every(function(value, key, arr){});	// 筛选数组，是否每个元素都返回true
arr.slice(0).reverse().map(function(){});	// 反向遍历数组，加个slice作用是防止原数组的顺序被更改

// for jQuery
$.each($array, function(k, v){});	// 遍历数组
$.inArray('a', $arr): 判断数组是否包含某个元素
delete a['a']	// 删除字典元素，如果用它来删除数组中的元素，删除完以后，数组总的长度不变，元素会被换成undefined，和php一样的坑
delete a.b	// 同上

Array.isArray(arr)	// 判断是否是数组，类似于其他语言的is_array
Array.isArray(arr) && arr.length === 0	// 判断是否是空数组
```
### 数字/布尔

- `!!{}`的值为`true`，`!!''`的值为false

```javascript
Math.floor(0.2);	// 向下取整
Math.ceil(0.2);		// 向上取整
Math.round(0.2);	// 四舍五入
Math.abs(-1);		// 取绝对值
Math.trunc()	// 去掉小数部分
Math.sign（）	// 判断一个数字是正数、负数还是0
Math.random()	// 产生0-1之间的随机数

var a = 100;
a.toString();	// 数字转字符串
num.toString(8);	// 把数字转换为指定进制的字符串
num.toFixed(2);	// 保留两位小数，我去会变成字符串，这个才是四舍五入，但是最好用lodash.floor

obj%1 === 0	// 判断是否是数字
```
### 字符串

```javascript
// 正则
var re = new RegExp("a|b", "i");	// 通过字符串来生成正则表达式，相当于/a|b/i，这种方式的好处是可以使用变量来写正则表达式
text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');	// 如果源字符串里有特殊字符需要加斜杠先转义一次

// 搜索
str.startsWith("hello");	// 类似beginWith
str.endsWith("world"); // 类似endWith
a.toUpperCase() === b.toUpperCase()	// 验证字符串是否相等大小写不敏感
str.match(/<title>(.*?)<\/title>/)	// 正则提取
str.match(/<title>(.*?)<\/title>/g)	// 全局搜索，不加g默认只取找到的第一个嘛，但是global不支持分组，会把前后的都给返回到结果中去。这种情况，要么匹配后，循环对结果进行前后去除；要么用exec对先行获取每一个结果的match[1]
str.match(/<title>(<abc>.*?)<\/title>/)	// 正则提取，带命名组的正则提取
str.matchAll()	// 直接全局搜索，ES2019+

// 去除空格，需要注意的是js的replace如果不用正则/g，则默认只会替换第一个匹配
str.replace(/\s+/g, "")    		// 去除所有的空格
str.replaceAll('abc', 'd')	// 替换所有，es2021+，对于npm run build的代码如果es版本选择较低也会报错
str.trim() / str.replace(/^\s+|\s+$/g, "");	// 去除两端的空格, 类似于trip，strip
str.trimLeft() / str.replace( /^\s*/, '')		// 去除左边的空格
str.trimRight() / str.replace(/(\s*$)/g, "")		// 去除右边的空格
str.replace(/[\r\n]/g, ' ')	// 去掉换行

JSON.parse(text)	// 将字符串转换为JSON
str.replace(reg, function(s, value){})	// 替换字符串，reg可以是正则表达式
str.replace('/abc(.*?)def/', function (a, b) {	// 分组正则替换
  return 'newstring';
})
// 需要注意的是上下两种方法的第二个参数都是指整个字符串，而不光是分组里面的串，如果要想只替换中间部分，可以将前后都用小括号进行分组，然后用$1$2来表示
str.replace(/_(.*?)_/g, "<div>$1</div>")	// 或者直接这样分组正则替换
str.indexOf(substring)	// 查找子字符串出现的位置，-1表示没找到
str.includes(substring)	// 查看是否存在某个子字符串
str.repeat(n)	// 将字符串重复n次
string.slice(start, end);	// 字符串分片
str.split('#')	// 字符串分割，返回分割后的列表
str.split(/\s+/) // 也可以用正则分割
str.split('...', n)	// n表示返回数组的最大长度，分割还是会分割成所有，只是返回前n个
str.toUpperCase()	// 转换为大写
str.toLowerCase()	// 转换为小写
parseInt(数字)  // 将数字取整，字符串转整数，字符串转数字
parseInt(num, 10) // 转整数，传入基数
parseFloat(num) // 字符串转浮点数

btoa(str);	// 字符串转换为base64
atob(str);	// base64转换为字符串

str.padStart(3, '0')	// 在字符串前面补0,ES8
str.padEnd(3, '0')	// 在字符串后面补0,ES8

a = encodeURI(uri);	// 会自动识别url中需要编码的地方
b = decodeURI(uri); // url解码
a = encodeURIComponent(uri);	// url编码，会对整个字符串编码，比如http://也会被编码
b = decodeURIComponent(uri);	// url解码

// 字符串格式化
`我是${name}`;

util.format('this is %s', 'foo');	// nodejs的util模块格式化字符串

// 判断字符串是否为数字
var str = "123";
var n = Number(str);
if (!isNaN(n))
{
    alert("it is");
}

name.charAt(0).toUpperCase() + name.slice(1); // 原生js让首字母大写
```

#### 时间处理moment/luxon/dayjs

- [时区列表](https://jp.cybozu.help/general/zh/admin/list_systemadmin/list_localization/timezone.html)
- moment作者已经不推荐使用`moment.js`，他自己又搞了个`luxon`，但我更推荐使用`dayjs`
- 需要注意的是`moment.date(12)`等方法会更改对象本身，所以在函数之间传递的时候最好克隆一个新的对象`moment(moment())`
- [format格式](https://day.js.org/docs/en/display/format)
- [moment在线测试](http://jsfiddle.net/brandonscript/rLjQx/)

```javascript
// 原生方法
new Date().getTime() // 获取当前时间戳，毫秒
new Date().toLoczaleTimeString('en-US', {
  timeZone: 'Eurrpo/American',
  hourCycle: 'h23',	// 以24小时制显示hour
  year: 'numeric',
  month: '2-digit',	// 几位数字，比如01，02等
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit'
})	// 转换为指定时区的时间
date.toISOString()	// 输出2022-05-24T14:18:13.046Z的格式
var today = Date.parse(new Date());	// 获取时间戳timestamp，单位为毫秒
Date.parse(1234567890000);	// 时间戳直接转换为Date
today.setTime(today.getTime() - 24*60*60*1000); // 获取昨天的时间
today.setDate(today.getDate() - 1);	// 也可以直接对年月日时分秒进行加减操作，这也是获取昨天的时间
today.getYear();	// 21
today.getFullYear(); // 2021
today.getMonth() + 1; //获取月份
String(today.getMonth() + 1).padStart(2, '0'); // 获取月，前面补零
today.Day() + 1;	// 获取星期几
today.getDate();	// 获取日
String(today.getDate()).padStart(2, '0');	// 获取天，前面补零
today.getHours();
today.getMinutes();
today.getSeconds();
today.getMilliseconds();

// dayjs
dayjs.unix(1318781876)	// 从时间戳解析时间
dayjs('2021-03-02T04:00:00.000Z').format('MMM D, YYYY')	// 时间解析和格式化
dayjs().format('YYYY-MM-DD')	// 获取年月日
dayjs().add(1, 'days')	// 日期加法
dayjs().subtract(7, 'year')	// 日期减法
dayjs('2018-10-1').isBefore('2018-1-1')	// 日期比较
dayjs.extend(utc)
dayjs.extend(timezone)	// 设置timezone需要extend这两个
dayjs("").tz("America/New_York"))
import duration from 'dayjs/plugin/duration';
dayjs.extend(duration)
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime)	// 设置humanize需要extend这两个
dayjs.duration(1, "minutes").humanize(); // a minute, 目前没有找到当1的时候为阿拉伯数字
dayjs.duration(24, "hours").humanize(); // a day
dayjs.duration(1, "minutes").huminize(true);	// in a minute
dayjs.duration(-1, "minutes").huminize(true);	// a minute ago, react可以直接用react-timeago来计算
date1.diff(date2, 'month')	// 计算两个时间的差值

// luxon
DateTime.now();
today.toMillis() // 获取毫秒时间戳
dur().toHuman()	// 1 year, 2 months, 1 week, 3 days, 4 hours, 5 minutes, 6 seconds, 7 milliseconds, luxon的humanize简直不能看

// moment，更详细的操作文档可参见http://momentjs.cn/docs/#/displaying/
moment('2020-04-29 00:00:00');	// 直接解析，需要注意的是它不能解析时间只有一位的情况，例如'2020-04-29 0:0:0'
moment('20200429', 'YYYYMMDD')	// 解析非标准格式的时间需要指定格式
moment(new Date()).add(1, 'days'); // 计算明天的时间
moment(new Date()).add(-1, 'days'); // 计算昨天的时间
moment(new Date()).subtract(2, 'hours');	// 时间相加减
moment().set('hour', 13)	// 设置当前的时间
moment().day()	// 当前日期是一周的第几天(0-6)，星期天是0，星期六是6
moment().weekday()	// 获取当前是星期几
moment().day(10)	// 如果指定的数字超过6，则会冒泡到其他星期
moment().days()	// 星期几0-6
moment().iosWeekday()	// 1-7分别代表星期一到星期天
moment().daysInMonth()	// 获取当前月的天数
moment().date()	// 获取当天是几号1-31
moment().date(30)	// 设置当前是几号
moment().month() + 1 // 获取当前月份
moment().year()	// 获取当前年
moment().dayOfYear()	// 1-366
moment().isSame('2021-04-17', 'day');	// 检查制定日期是不是今天
moment().isSameOrBefore();
moment().format(); // "2014-09-08T08:02:17-05:00"
moment().format("dddd, MMMM Do YYYY, h:mm:ss a"); // "Sunday, February 14th 2010, 3:25:50 pm"
moment().format("YYYY-MM-DD HH:mm:ss");	// 2021-01-06 22:00:00
moment().format("ddd, hA");                       // "Sun, 3PM"
moment().format("[Today is] dddd");               // "Today is Sunday"
moment().format("hh:MM A");		// "06:00 PM"
moment().isoWeekday();	// Sunday获取星期几
moment('gibberish').format('YYYY MM DD');         // "Invalid date"
moment().diff(moment[])	// 比较两个日期的间隔，默认是时间戳的比较
moment().diff(moment[], 'days')	// 比较两个日期的间隔，第二个参数可以设置比较的是年、还是月份等
moment().unix()	// 获取时间戳
moment.max(moment[]); // 获取多个时间里面最大的时间
moment.min(monent[]);	// 获取多个时间里面最小的时间
moment().startOf('weeks')	// 获取一天的开始时间，获取一周的开始时间，获取一个月的开始时间，获取一个季度的开始时间
moment().endOf('weeks') // 获取一天的结束时间，获取一周的结束时间，获取一个月的结束时间，获取一个季度的结束时间
```

#### URL Params处理

```javascript
let searchParams = new URLSearchParams(url.split('?')[1])

// 遍历请求参数
for (const [key, value] of mySearchParams.entries()) {}

let builder = new URLSearchParams()
builder.set('field1', 'value')
builder.set('feild2', JSON.stringify(myObj))
builder.toString()	// 生成URL查询字符串
```

## Buffer

```javascript
Buffer.from('abc', 'utf8') // 从字符串创建Buffer
```

### 函数

```javascript
// 不定参数，会把needles当作一个数组，没有值也是空数组
function containsAll(haystack, ...needles) {
	console.log(haystack, needles);
}

function fn() {
  console.log(arguments)	// 获取参数
}

// 箭头函数
const fn = function () {}
const fn = () => {}
const fn = name => {}	// 如果只有一个参数可以这样简写
const fn = num => num * num	// 如果只有一个返回语句可以这样简写
const fn = name => ({name})	// 如果返回的是一个对象可以这样简写
```

### 类

```javascript
class Person {
  name = 'test';

	// getter方法
	get fullName () {
    return this.name
  }

	// setter方法
	set fullName (name) {
    this.name = name
  }
}
```

### 文件/文件夹

- 主要是使用`Nodejs`中的`fs`模块
- 下面很多方法默认都是异步方法，一般加上`Async`就是其同步的方法，但是同步方法要加上`try...catch...`

```js
fs.statAsync(path); // 同步判断文件或文件夹是否存在，同步方法最好加上try...catch
fs.stat(path, function(exists) {}); // 异步的方式判断文件或文件夹是否存在，文件创建时间

fs.access(path, 权限, function(err){}); // 判断是否拥有指定文件的指定的权限，权限可以有fs.F_OK(文件是否可见，也可用来判断文件是否存在),fs.R_OK(是否可读),fs.W_OK(是否可写),fs.X_OK(是否可执行)

const fileBuffer = fs.readFileSync(path.join(__dirname, "../public/index.html"))	// 读取文件，最好加上__dirname，否则可能会出现找不到路径的问题
fileBuffer.toString()	// 获取文件内容字符串

fs.readdir('目录名', 'utf-8', function (err, data) {	// 获取目录下的文件
  data.forEach(function(item, index)) {	// 遍历目录
    fs.reradFile('文件名', 'utf-8', function(err, content) {	// 读取文件内容
    	fs.writeFile('文件名', "abc", "utf-8", function(err) {	// 向文件写入内容
        
      });
  	});
  }
});

const path = require('path')
path.resolve('../.env')	// 根据相对路径获取绝对路径
```

#### FileList

- web原生的文件对象，是`input[type=file]`的value，是一个只读的对象

  ```javascript
  var fileInput = document.getElementById("myfileinput");
  var files =fileInput.files
  
  // 遍历FileList对象
  for (var i = 0; i < files.length; i++) {
      file = files.item(i);
      file = files[i];
      alert(file.name);	// 获取上传的文件的文件名
  }
  ```
  
- 虽然`FileList`是一个只读对象，但是仍然有办法删除上传的某个文件

  ```javascript
  const input = $('myInput')[0];
  const deletedIndex = 2;
  const dt = new DataTransafer();
  for (var i = 0; i < input.files.length; i++) {
    if (i !== deletedIndex) {
      dt.items.add(files[i]);
    }
  }
  input.files = dt.files;
  ```

### 错误处理

- 有时候dom的一些操作无法用try catch到错误，原因是它可能是异步的，需要在方法后用`.catch`来捕获异常

```javascript
try {
  
} catch (error) {
  // 错误则会执行
  console.log(error.toString()) // 只是message本身
  console.log(error.stack)// 这是我们console.log(e)的字符串，可以用正则从中匹配到一些有用的信息
  throw error // 重新抛出错误
} finally {
  // 无论是否成功都执行
}
```

### 网络请求

```javascript
// 同步方式
var xmlHttp = new XMLHttpRequest();
xmlHttp.open("GET", "https://haofly.net", false);
xmlHttp.send();
console.log(xmlHttp.responseText);

// 异步方式
var xmlHttp = new XMLHttpRequest();
xmlHttp.onload = function(e) {
  console.log(xmlHttp.status, xmlHttp.responseText);	// 这里处理响应结果
}
xmlHttp.onreadystatechange = function() {
  console.log(xmlHttp.readyState)	// 0请求未初始化，1服务器连接已建立，2请求已接受，3请求处理中，4请求已完成，且响应已就绪
};
xmlHttp.open("GET", 'https://haofly.net', true);
xmlHttp.send();

// 如果是POST form数据，需要这样做
const params = 'foo=test&foo1=test1'
xmlHttp.open('POST', url, true);
xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xmlHttp.send(params);
```

### 进程/线程/Shell命令执行

- 使用`child_process`模块
- 可用来执行`shell`命令

```js
var p = require('child_process');
p.exec("ls abc", function (error, stdout, stderr) {});	// 异步执行shell命令
p.execSync("ls abc");	// 同步方式执行SHELL命令
```

## DOM操作

### 元素查找

- 一般`getElements**`方法返回的是一个NodeList，并不是普通的列表对象但是不能用`forEach`来遍历，只能用for循环遍历，因为它是一个`HTMLCollection`对象，也可以转换为列表对象`Array.from(nodeList)`

```javascript
// 原生元素选择
document.querySelector(".myclass");	// 也可以用jQuery的选择起
document.querySelectorAll('div.abc, div.def');
document.getElementById('xxx');
document.getElementByClassName('myclass');
document.getElementByTagName('p');
ele.parentElement;	// 获取父元素
ele.parentNode;		// 获取父节点
ele.children		// 获取子节点
ele.closet('td')	// 查找最近的某个
ele.getElementsByTagName('td');	// 查询子元素
ele.getElementsByClassName('myclass');	// 查询子元素
ele.firstElementChild;
ele.lastElementChild
ele.nextElementSibling;	// 获取下一个兄弟节点
ele.previousElementSibling;

// jQuery元素选择
$('p')  		// 选取标签<p>的所有元素
$('p')[0]	// 获取原生对象
$('p#intro')  	// id为intro的所有p元素
$('p.intro')  	// class为intro的所有p元素
$('p:first')  	// 选取第一个<p>元素
$('p a:first')	// 选取p元素下的第一个a元素
$('p[name=abc]')
$('*[data-abc="22"]');	// 获取data-*元素，按data数据获取元素
$('body >div:first-child') // 查找第一级的第一个元素
$('*')        		// 所有元素
$('[id^="test"]')	// 查找id以test开头的元素
$('[id$="test"]')	// 查找id以test结尾的元素
$('[id*="test"]')	// 通配符查找
$('[id!="test"]')	// 查找id不为test的元素
$(this)       		// 当前元素
$(this).next()  	// 获取下一个同级元素/兄弟节点
$(this).nextAll() // 获取所有之后的兄弟节点
$(this).prev()		// 获取上一个同级元素/兄弟节点
$(this).prevAll() // 获取所有之前的兄弟节点
$(this).siblings() // 返回兄弟姐妹节点，不分前后
$(this).parent()	// 获取父元素
$(this).parents('myclass')	// 查找所有祖先元素
$(this).children('myclass')	// 获取子元素，只会返回直接的子节点
$(this).nextAll('cl')	// 获取指定元素的所有指定的同级元素
$('p').find('input')	// 查找input下的所有input元素
$('p').last()		// 选择最后一个元素
$('input:checked') 		// 查找所有checked为true的checkbox的input元素
$('div:visiable')
document.getElementById('test:abc')	// 有特殊字符的元素的查找，jquery往往无法处理过来

$('img').index($(myImg)) // 可以查找某个元素在一个jquery数组中的索引

$('select option[value="abc"]');	// 通过value获取select的option
```

#### 同步等待元素存在可见

由于有些元素不一定是在`window.load`之后就全部展示的，有时候我们需要通过滚动页面才能让某些元素出现，这个时候就需要一个比较方便的方法用于等待元素出现。如果是异步的需求，可以直接用`setInterval`每隔几秒去检查一次(注意不能用while循环去一直判断，因为会占用计算时间，导致异步任务无法完成)，但是对于复杂的需求，比如等待一个元素出现后需要等待另外的元素出现，或者是需要同步判断一系列的元素，那么就需要另外的方法，目前能找到的最好的方法是这样的:

```javascript
function rafAsync() {
    return new Promise(resolve => {
        requestAnimationFrame(resolve);
    });
}

// 用这种方式去检查元素的效率比setInterval高很多
async function checkElement(selector, index = 0) {
    let querySelector = document.querySelectorAll(selector)[index];
    while (querySelector === null || querySelector === undefined) {
        querySelector = document.querySelectorAll(selector)[index];
        await rafAsync()
    }
    return querySelector;
}

checkElement('#my_tag').then((element) => {	// 当元素可见时会执行then里面的回调逻辑
  console.log(element);
})
```

### 获取元素内容

```javascript
// js原生方法
ele.attributes;	// 一个(name, value)的数组
ele.getAttribute('class');
ele.setAttribute('class', 'highlight');
ele.hasAttribute('class');
ele.removeAttribute('class');
ele.value;		// 获取元素内容
ele.style.fontSize // 获取inline样式
ele.innerText	// 获取元素文字
getComputedStyle(ele)	// 获取元素的所有的样式，包含了所有的css属性
getComputedStyle(ele, '::before')	// 获取指定事件的样式

videoEle.videoHeight / myVideo.videoWidth	// 原视频的分辨率，注意这里并不是视频组件的长宽
videoEle.clientHeight / myVideo.clientWidth	// 视频组件的长款
videoEle.currentTime	// 当前播放到什么时间了
videoEle.ended // video是否播放完毕
videoEle.paused // video是否暂停

// jQuery方法
$('[id=xxx]');	// 如果有重复的id的元素可以这样获取所有的元素
$('#check').prop('checked')	// 获取checkbox是否被check了，不用给你用attr
$('div').prop('classList') // 获取元素类列表
$('div').prop('classList').remove('d-none')	// 移除某个类
$('div').prop('classList').add('d-none')	// 添加某个类
$('div').height()	// 获取元素高度
$('div').height(20)	// 设置元素高度
$('select').val()	// select标签的值
$('select option:selected').text();	// select被选中项的文本
$('div').data('abc'); // 获取元素的data数据，例如<div data-abc="dsiahoaihgio"></div>
$('div').removeAttr('required');	// jquery移除属性
$('div').hasClass('foo');	// 判断元素是否有某个类
$("p").is(":visible");	// 查看元素是否可见
$('div').prop('tagName'); // 获取元素的tag名称
```

### 编辑元素

```javascript
// js原生
option = document.createElement('option');	// 创建元素
option.setAttribute('value', 'value1');		// 设置元素属性
text = document.createTextNode('ppp');		// 创建内容
ele.appendChild(text);					// 添加子元素
ele.removeChild(text);
ele.replaceChild(el1, el2);				// 替换子元素
selection.innerHtml = '<option>a</option>';	// 修改内部html内容
parentElement.insertBefore(newElement, referenceElement);	// 插入子元素
ele.classList.add("mystel", "secondClass");	// 给元素添加类
ele.classList.remove('mystyle', 'secondClass');	// 给元素移除类
ele.classList.toggle("mystle"); // 切换类，如果没有就增加该类，如果有就删除该类
ele.classList.contains('mystyle');	// 判断当前类是否存在
ele.classList.item(0);	// 获取第几个类
ele.style.color = '#fff';	// 直接修改style
document.getElementById("input").value = "test";	// 设置input元素的内容
ele.disabled = true;	// 禁用元素，禁用button

// 添加元素
html('')	// 修改内部的html内容
append()	// 在被选元素的结尾插入内容
prepend()	// 在被选元素的开头插入内容
after()		// 在被选元素之后插入内容
before()	// 在被选元素之前插入内容
remove()	// 删除当前元素
empty()		// 清空当前元素的子元素
clone()		// 克隆/复制一个元素

// jquery属性更改
addClass('')	// 给元素添加类
removeClass('class1 class2')	// 给元素移除某个类
$('p').css('color', 'red')			// 修改CSS属性
$('button').prop('disabled', true)	// 设置按钮不可点击disabled
$('p').hide()	// 隐藏元素
$('p').show()	// 显示元素
$('img').attr('src', 'xxx')	// 改变元素的属性
$('div')[0].scrollIntoView()	// 将页面滚动到某个元素
$('div').animate({scrollTop: $('div').offset().top - 10})	// 将元素滚动到某个位置

// video标签控制(原生js)
myVideo.play()	// 开始播放
myVideo.pause()	// 暂停播放
myVideo.load()	// 重新加载视频

// 创建元素
var a_tag = document.createElement('a');	// 首先创建一个空元素
parent_tag.after(a_tag);	// 然后将元素放到指定的位置
a_tag.outerHTML = '<a class="..." name="">ok</a>'; // 最后将元素html替换成我们想要的

$("#<form_id>").trigger("reset"); // jQuery清空表单字段

canvasEle.getContext("2d").strokeRect(20, 20, 150, 100)	// 在元素上绘制矩形
```

### 元素事件listen event

- 对于动态生成的元素，绑定事件需要绑定在父元素上才能生效，或者直接绑定在document上，`$(document).on('click', '#myButton', function(){})`
- 对于`input`框，当失去焦点的时候才会触发`onchange`，输入事件应该是`oninput`

```javascript
// js原生事件
ele.onchange = function () {};
ele.onchange = funciton () {};
ele.addEventListener('click', func (e) {});	// 原生click事件，注意这里如果用箭头函数，那么获取当前元素不应该用this而是用e.targetsf
ele.removeEventListener('change', func () {});
videoEle.addEventListener('resize', () => {});	// video元素的长宽或者分辨率变化
ele.addEventListener('DOMNodeInserted', func (){});	// 当插入新DOM元素时触发

// 页面事件
window.onload = function () {};	// 页面加载完成后触发
document.onkeyup = function(e) {};	// 用户按键事件
// 监听页面全局异常
window.addEventListener("unhandledrejection", event => {
  console.warn(`UNHANDLED PROMISE REJECTION: ${event.reason}`);
});
window.addEventListener('error', function(event) { ... })

// jQuery事件列表
change()	// 当元素发生改变时触发，常用于input、select
blur()		// 元素失去焦点时触发
click    	// 鼠标点击
dbclick  	// 鼠标双击
focus()		// 元素获得焦点时触发
hover		// 模拟光标悬停事件
mouseenter 	// 鼠标穿过元素
mousedown	// 鼠标移动到元素上方，并按下鼠标按键
mousesleave // 鼠标离开元素
mouseup		// 在元素上松开鼠标按钮
resize() 	// 大小调整，一般是$(window).resize(function(){})

// 事件的触发
document.getElementById('').dispatchEvent(new MouseEvent('mouseenter')) // 原生方式触发事件
$('a').trigger('click')  // 触发a标签的click事件
$('#myModal').modal('show')  // bootstrap中modal的触发

// 事件的订阅
$('p').bind('click', function(){});	// 用bind进行事件的绑定，即使是之后生成的元素也能与事件绑定

// modal模态框显示事件/show                            
$('#myModal').on('shown.bs.modal', function () {});
// modal模态框关闭事件                                           
$('#myModal').on('hidden.bs.modal', function () {});
$('#myModal').on('hidden', function () {});
$('#myModal').on('hide', function () {});
```
### 页面属性
```javascript
document.cookie					// 当前cookie
document.cookie = 'abc=123';		// 添加cookie，注意这是添加，不是设置
document.cookie = 'abc=123; expires=' + date.toGMTString() + ';'	// 设置过期时间
window.location.href 			// 获取当前的url，例如 https://haofly.net/js/index.html?abc=def
window.location.pathname	// 例如 /js/index.html
window.location.origin	// 例如 https://haofly.net
window.location.hostname	// 例如 haofly.net
window.lcoation.href = 'url'	// 跳转到某个url
window.location.back() // 返回上一页
window.history.pushState({"html":test.html,"pageTitle":response.pageTitle},"", urlPath);	// 不刷新页面直接修改url
document.referrer				// 获取当前页面的referer，是一个read only属性，不可以在ajax里面改变，改不了，md。也可用于获取parent document的url
location.reload()				// 刷新当前页面
window.stop() // 停止当前所有的渲染和js执行过程或者正在请求还未完成的请求

window.getSelection().toString();	// 获取选中的文字，但是图片不能toString

// 获取url参数的方法，来自Stack Overflow
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
getUrlParameter('page')

// ready()方法
$(document).ready(function);	// 当DOM已经加载，并且页面已经完全呈现时，会发生ready事件
(function() {
  // 原生的ready方法
})();
```
### Canvas

```javascript
const c = document.getElementById('myCanvas')
const ctx = c.getContext('2D')	// 创建一个可绘制的canvas画布
ctx.font = ''	// 设置字体
ctx.fillText('test', 10, 20)	// 填充文字
ctx.fillStyle = 'red'	// 设置颜色
ctx.textAlign = 'center'	// 文字水平居中
```

### 特殊函数

```javascript
// 定时器
var t = window.setTimeout(func, delay);	// 延迟delay毫秒后执行函数func
var t = window.setInterval(func, delay);	// 每隔delay毫秒就执行函数func
var t = setImmediate(func);					// 在浏览器完全结束当前运行的操作之后立即执行指定的函数
clearInterval(t)				// 清除计时器，setInterval返回的是一个定时器的id，如果不清楚定时器名称，可以直接来个for循环清理所有的Interval：for(var i = 0; i<= 2000; i++) {clearInterval(i);}

debugger;						// 代码加入这一行，浏览器会自动断点进行调试，这对于自动编译的开发环境非常实用
```

## Module 语法

js里面一个模块就是一个独立的文件，文件内部的变量，外部是无法获取到的，需要用`export`使内部的变量暴露给外部，例如:

```js
export var name = 'hao';
export {var1, var2, var3};	// 一次多个
export function myfunc(x, y) {};	// 导出函数
export {var1 as var2};	// 重新命名
export default function () {};	// 这样在import的时候可以自定义name，例如import customName from '...';

exports.myFunc = function () {}
```

## Async/Promise

- 异步执行代码能防止单线程的js被阻塞，但是却让响应的顺序不可预计。
- 如果要同时保证异步函数的顺序，要么就需要一层一层使劲的嵌套，除非使用Promise，它允许将这种回调函数的嵌套改为链式调用，然后将回调放到then中。
- 但是then依然不够直观，所以就有Async和await了。写起来的代码就像是同步的了。async函数内部可以有一个或多个异步操作，一旦遇到await就会立即返回一个pending状态的Promise对象，然后回到主线程执行住线程代码。等到await的异步请求被resolve/reject后，才会继续执行async函数内后面的部分。

```javascript
// 模拟一个异步函数
let asyncFunc = async() => {
  await new Promise((resove, reject) => {
    console.log("actions");
    setTimeout(() => {
      console.log("模拟异步返回结果");
    }, 0);
  });
  return "ok";
}
let promise = asyncFunc();
promise.then(value => {
  console.log(value);
});

// mock一个Promise(比如mockfetch函数)
mockFetch = (url) => {
    return new Promise((resolve, reject) => {
      const code = 200;
      process.nextTick(() =>
        status === 200 ?               
          resolve({
            json: function() {
              return {
                msg: "ok",
              };
            },
          }) : reject({
        		error: "error"
      		}),
      );
    });
  };
mockFetch("https://api.github.com/users/haoflynet/repos");

// 可以用Promise实现sleep，模拟超时，模拟延迟
await new Promise(r => setTimeout(r, 1000));

// 用await Promise实现setInterval
async function waitUntil(condition) {
  return await new Promise(resolve => {
    const interval = setInterval(() => {
      if (condition) {
        resolve('foo');
        clearInterval(interval);
      };
    }, 1000);
  });
}

// 一次性parallel执行多个异步任务
await Promise.all(_.map(arr, async (item) => {
  await ...
}));

// 如果需要依次调用一组Promise，不是parallel的形式，可以这样做
for await (const item of items) {
  await ...
}
```

## Ajax

- 如果要接收stream响应，nginx的location也需要添加配置`proxy_buffering off; fastcgi_buffering off;`

```javascript
$('myForm').serializeArray();	// 将表单数据转换成array然后用ajax提交

$.ajax({
	url: 'url',
	dataType: 'json',
	type: 'POST',
	data: data,
  xhrFields: { // 如果是stream响应，需要这样设置
    responseType: 'stream',
    onprogress: function(e) {
      console.log(e.currentTarget.response);
    }
  }
  beforeSend: function (xhr) {	// 发送请求前需要做什么
    
  },
	error: function(re){
	},
	success: function(re){
	},
  complete: function(re) { 	 // 无论怎样都会执行
    if (re.statusText == "success") { 
      console.log("Sent successfully");
    } else { 
      console.log("Not Sent");
    }
  }
});

// 全局注册一个ajax完成的回调函数
$(document).ajaxComplete(function() {
 $( ".log" ).text( "Triggered ajaxComplete handler." );
});
```

直接发送POST请求

```javascript
$.post('some.php', {name: 'haofly'})
    .done(function(msg){  })
    .fail(function(xhr, status, error) {
        // error handling
    });
```

## jQuery Effects特效

- 能实现一些简单的效果，例如blind(百叶窗特效)、bounce(反弹特效)、clip(剪辑特效)、drop(降落特效)、explode(爆炸特效)、fade(淡入淡出特效)、fode(折叠特效)、highlight(突出特效)、puff(膨胀特效)、pulsate(跳动特效)、scale(缩放特效)、shake(震动特效)

```javascript
$('#mydiv').fadeout();	// 使用方法很简单
$('#mydiv').fadein().delay(1000).fadeout(); // 延迟执行
```

## 调试技巧

- **代码中打断点直接`debugger;`语句，这样浏览器会自动在该处断点，对于会有js压缩的代码调试非常有用**
- **浏览器console.log**打印出来的对象，如果没有点击展开，那么点开的时候会是最后一次该对象的值。

## 第三方库

### lodash/常用帮助函数

- [Online Lodash Tester](https://codepen.io/travist/full/jrBjBz/): 在线测试lodash功能的站点

##### _camelCase

- 将字符串转换为驼峰写法

```javascript
_.camelCase('Foo Bar');	// => 'fooBar'
_.camelCase('--foo-bar--');	// => 'fooBar'
_.camelCase('__FOO_BAR__');	// => 'fooBar'
```

##### _.chain

- lodash中最重要的部件之一
- 可以将普通的对象变为可链式执行的对象
- `_.chain(arr)....value()`也可隐式调用`_(arr)...`就不用`.value()`
- 这里的`.value()`是一个延迟计算操作，但是有些方法是不能加在链条中的，例如`reduce`会被立即计算

```javascript
const arr = [1,2,3,4,5]了
_.chain(arr)
	.filter(n => n % 2 === 0)
	.map(n => n * n)
	.uniq()
	.sum()
	.value()	// 最后要加.value()才能得到真正的结果值

// .value()的延迟计算
a = _.chain(arr).filter(n => n % 2 === 0).map(n => n * n).sum()
a.value()	// 得到20
arr.push(6)
a.value()	// 得到56
```

##### _.cloneDeep

- 深度克隆

```javascript
newObj = _.cloneDeep(oldObj);
```

##### _.countBy

```javascript
_.countBy([6.1, 4.2, 6.3], Math.floor)	// {'4': 1, '6': 2}
```

##### _.chunk

- 对数组按指定数量分片

```javascript
_.chunk([1,2,3,4,5], 2)	// [[1,2], [3,4], [5]]
_.chunk('abcdefg', 2).map(chunk => chunk.join(''))	// 如果用在字符串上的话结果会将每个字符分隔开，所以我们需要join一下
```

##### _.debounce(func, [wait=0])

- 函数防抖，防止函数短时间内重复执行，例如api请求，搜索的查询

```javascript
_.debounce(() => {apicall}, 100)
```

##### every

必须所有回调都返回`true`，最终结果就为`true`，否则就为`false`. 有个妙用就是在实现在forEach中break的功能

##### filter

过滤数组，将返回为`true`(满足条件)的元素组成为一个新数组

```javascript
Array.from([1,2,3]).filter(item => item > 2)	// 得到[3]
Array.from([1,2,3]).filter((item, index) => function({ // 带索引
  return true;
}))	// 得到[3]
```

##### find

返回回调结果为`true`的第一个元素 

##### _.find

返回回调结果为`true`的第一个元素

```javascript
_.find(users, function (item) {item.age > 20})
_.find(users, {'age': 20, 'active': true})	// 如果是等于操作那么可以直接这样
_.find(users, 'active'}	// 如果是布尔值可以更简化
```

##### findIndex

返回回调结果为`true`的第一个元素的索引位置

##### _.flatMap

对数组中的所有值运用函数，函数的返回值即是一个新的数组，如果不返回则是`undefined`

```javascript
function duplicate(n) {
  return [n, n];
}
 
_.flatMap([1, 2], duplicate);
// => [1, 1, 2, 2]
```

##### _.flatMapDeep

- 类似于`flatMap`，但是它会递归将值中的数组全部展开

##### _.floor(number, [precision=0])

- 四舍五入，可以指定保留几位小数，且小数位不足时不会补0，比toFixed好用

```javascript
_.floor(4.006) // 4
_.floor(0.046, 2) // 0.04
_.floor(4) // 4
```

##### forEach

对数组中每一个值运用函数，但是无需返回值，只是单纯的遍历

##### _.forIn

- 遍历对象/遍历字典

```javascript
function Foo() {
  this.a = 1;
  this.b = 2;
}
 
Foo.prototype.c = 3;
 
_.forIn(new Foo, function(value, key) {
  console.log(key);
});

_.forIn('string', function(value, index) {	// 遍历字符串
  
})
```

##### _.get

- 获取对象内部的属性值，一个非常非常实用的方法

```javascript
_get(user, 'name', 'defaultvalue')
_get(user, 'parent.name', 'devaultvalue')

var object = { 'a': [{ 'b': { 'c': 3 } }] }
_.get(object, 'a[0].b.c')	// 可以直接使用数组下标进行访问
_.get(object, ['a', '0', 'b', 'c'])
```

##### _.groupBy

- 根据第二个参数的返回值来进行分组，返回的是一个key=> [item]对象，key为返回值，[item]为对象列表

```javascript
// 返回{ '4': [4.2], '6': [6.1, 6.3] }
_.groupBy([6.1, 4.2, 6.3], function (item) {
  return Math.floor(item);
});
```

##### _.intersection

- 计算几个数组的交集

```javascript
_.intersection([2, 1], [4, 2], [1, 2])	// [2]
```

##### _.invert

- 交换map/json的key和value

```javascript
const obj = {a: 1, b: 2, c: 3}
_.invert(obj)	// {'1': 'a', '2': 'b', '3': 'c'}
```

##### _.isEqual

```javascript
_.isEqual(_.sortBy(a), _.sortBy(b)) // 比较两个数组是否相等(不按顺序)
_.isEqual(a.sort(), b.sort())	// 同上
_.isEqual(a, b) // 可以比较两个Object是否相同
```

##### _.isMatchWith

`isMatchWith(object, source, [customizer])`, 具有基本的isMatch功能，并且能添加`customizer`进行定制化的比较。判断source是否包含在object里，customizer返回true或者false。我fuck，这个函数只要source里面有key没在object，立马就返回false了，都不执行customizer的

##### isNaN

判断value是否是`NaN`

##### _.nth

- 获取数组/字符串指定索引的元素，可以用负数

```javascript
_.nth(arr, -1);	// 获取倒数第一个元素 
_.nth(arr, -2); // 获取倒数第二个元素
_.nth(str, -1);	// 获取字符串最后一个自负
```

##### _.kebabCase

- 将字符串转换为`kebaba`格式，中线分割

```javascript
_.kebabCase('Foo Bar');	// => 'foo-bar'
_.kebabCase('fooBar');	// => 'foo-bar'
_.kebabCase('__FOO_BAR__');	// => 'foo-bar'
```

##### _.last

- 获取数组的最后一个元素

```javascript
_.last(['a', 'b']);
```

##### map

对数组中每一个值运用函数，返回一个新的值作为新数组，没有返回值的位置会被设置为`undefined`

```javascript
myArr.map(Match.sqrt)

myArr.map((item, index) => {})	// 获取遍历的索引

// 在map中使用异步函数
await Promise.all(_.map(['a','b'], async (item) => {
  await ...
}))
```

##### _.map

- 遍历对象/字典时，callback第一个参数是value不是key

```javascript
_.map(users. 'name')	// 提取字段的某一个值作为数组
```

##### _.mapKeys

- 值不变，将每个返回值作为key，可作用于数组和对象上

```javascript
var arr = [1, 2, 3];
_.mapKeys(arr, (item) => item.toString()) // {"1": 1, "2": 2, "3": 3}

var obj = { 'a': 1, 'b': 2, 'c': 3 };
_.mapKeys(obj, (item) => item.toString()) // {"1": 1, "2": 2, "3": 3}
```

##### _.mapValues

- 和`_.mapKeys`类似，不过这个目的是修改value，而不是key

```javascript
var obj = { 'a': 1, 'b': 2, 'c': 3 };
_.MapValues(obj, (value) => item.toString()) // {"a": "1", "b": "2", "c": "3"}

var arr = [1, 2, 3]; // 作用于数组上时，item参数是数组下标
_.mapKeys(arr, (item) => item.toString()) // {"0": "1", "1": "2", "2": "3"}
```

##### _.max

```javascript
_.max([1, 2, 3]) // 3
_.max([])	// undefined
```

##### _.maxBy

```javascript
_.maxBy(objects, 'field')	// 这个返回的是对象，并不是最大的那个值
```

##### _.merge

- 递归合并两个对象

```javascript
var obj1 = { 'a': [{ 'b': 2 }, { 'd': 4 }] }
var obj2 = { 'a': [{ 'c': 3 }, { 'e': 5 }] }
_.merge(obj1, obj2) // { 'a': [{ 'b': 2, 'c': 3 }, { 'd': 4, 'e': 5 }] }
```

##### _.min

- 获取最小值

```javascript
_.min([4, 2, 8, 6])	// 2
_.min([])	// undefined
```

##### _.orderBy

- 排序

```javascript
var users = [
  { 'user': 'fred',   'age': 48 },
  { 'user': 'barney', 'age': 34 },
  { 'user': 'fred',   'age': 40 },
  { 'user': 'barney', 'age': 36 }
];

_.orderBy(users, ['user', 'age'], ['asc', 'desc']);	// 先按user升序，相同的再按age降序
```

##### _.pick

- 最实用函数之一，从对象中获取指定级别的值

```javascript
const obj = {'a': 1, 'b': 2, 'c': 3}
_.pick(obj, ['a', 'c'])	// {'a': 1, 'c': 3}
```

##### _.pickBy

```javascript
const obj = {'a': 1, 'b': '2', 'c': 3}
_.pickBy(obj, _.isNumber)	// {'a': 1, 'c': 3}
```

##### _.random

- 生成随机数

```javascript
_.random(0, 100)	// 生成0-100的整数
_.random(0, 100, true)	// 生成0-100的浮点数
```

##### _.reduce

- 能够将元素一次进行计算，第一个参数为上一次计算的结果

```javascript
var arr = [1,2,3];
_.reduce(arr, function(result, o) {return result + o});	// 这里的result其实是第一个元素，以后的每一个return的结果作为下一次的result

// 如果要累加对象的某个值可以这样做
const users = [
  {num: 1},
  {num: 2}
]
_.reduce(users, (result, user) => {result.num += user.num; return result})
```

##### _.snakeCase

- 将字符串转换为`snake`形式，下划线分割

```javascript
_.snakeCase('Foo Bar');	// => 'foo_bar'
_.snakeCase('fooBar');	// => 'foo_bar'
_.snakeCase('--FOO-BAR--');	// => 'foo_bar'
```

##### some

只要其中一个值返回`true`，那么整个表达式的结果就是`true`

```javascript
Arrays.from([12, 22, 33]).some(item => item > 30)
```

##### _.sortBy

```javascript
_.sortBy([{a: 123}, {a:222}], ['a'])
_.sortBy([{a: 123}, {a:222}], function(o) => o.a)
```

##### _.startCase

- 将字符串转换为每个单词首字母大写的格式，空格分割

```javascript
_.startCase('--foo-bar--');	// => 'Foo Bar'
_.startCase('fooBar');	// => 'Foo Bar'
_.startCase('__FOO_BAR__');	// => 'FOO BAR'
```

##### _.template

创建一个预编译的模板方法来进行字符串的格式化

```javascript
// 默认就能直接解析ES的分隔符
var compiled = _.template('hello ${ user }!');
compiled({ 'user': 'pebbles' });

// 使用自定义的模板分隔符{{ }}
_.templateSettings.interpolate = /{{([\s\S]+?)}}/g;
var compiled = _.template('hello {{ user }}!');
compiled({ 'user': 'mustache' });
```

##### _.take

- 取前n个元素组成一个新的数组

```javascript
_.tak([1, 2, 3], 2) // [1,2]
```

##### _.toPath

转化value为属性路径的数组

```javascript
_.toPath('a.b.c')		// => ['a', 'b', 'c']
_.toPath('a[0].b.c') // => ['a', '0', 'b', 'c']
```

##### _.uniq

创建一个去重后的`array`数组副本

```javascript
_.uniq([1, 2, 2]) // 得到[1, 2]
```

##### _.uniqBy

- 根据指定方法去重

```javascript
_.uniqBy([{}, {}], (item) => item.field)
_.uniqBy([{}, {}], 'field1')	// 根据指定字段去重可以这样简写
```

##### upperFirst

- 首字母大写

```javascript
_.upperFirst('abc') // Abc
```

##### _.xorWith

- 得到在两个数组中都不存在的元素组成的数组，第三个参数是一个比较函数，用于比较是否相等

```js
_.xorWith([3], [1,2], _.isEqual)	// 得到[3,1,2]
_.xorWith([3, 1], [1,2], _.isEqual)	// 得到[3, 2]
```

### 常用帮助方法

```javascript
// 获取query参数
window.getQuery = function(key) {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get(key)
}

// 设置query参数
window.addQuery = function(key, value) {
  var searchParams = new URLSearchParams(window.location.search)
  searchParams.set(key, value)
  // window.location.search = urlParams	// 直接跳转
  return searchParams.toString()
}

// 获取cookie
window.getCookie = function(cname) {
  const name = cname + "="
  const ca = document.cookie.split(';')
  for (let i = 0; i < ca.length; i++) {
    const c = ca[i].trim()
    if (c.indexOf(name) === 0) return c.substring(name.length, c.length)
  }
  return ""
}

// 设置cookie
window.setCookie = function(key, value) {
  document.cookie = `${key}=${value}`
}

// 数字转货币(每三位一个逗号)
window.convertNumberToMoney = function(money){
	if(money && money!=null){
		money = String(money)
		var left=money.split('.')[0],right=money.split('.')[1]
		right = right ? (right.length>=2 ? '.'+right.substr(0,2) : '.'+right+'0') : '.00'
		var temp = left.split('').reverse().join('').match(/(\d{1,3})/g)
		return (Number(money)<0?"-":"") + temp.join(',').split('').reverse().join('')+right
	} else if(money===0) {
		return '0.00';
	}else{
		return "";
}
  
// 简单的retry重试方法
function retry(fn, times, delay=3000) {
  return new Promise(function(resolve, reject) {
    function try() {
      fn()
        .then(res => resolve(res))
        .catch(err => {
        	if (times === 0) {
            reject(err);
					} else {
            times--;
            setTimeout(try(), delay);
          }
      	})
    }
    try();
  })
}
```

## 推荐阅读

- [You-Dont-Need-jQuery](https://github.com/nefe/You-Dont-Need-jQuery/blob/master/README.zh-CN.md)

## TroubleShooting

- **根据select的选项不同跳转到不同的页面**:
  `<select onchange="location.href=this.options[this.selectedIndex].value;">`

- **Ajax请求无论是GET还是POST都突然变成了OPTIONS请求**
  可能是因为把本地代码提交到服务器时，发生了跨域请求错误，url里面写的是本地的端口地址，这时候只需要修改本地的端口地址修改为相对于服务器的本地地址即可

- **停止js的冒泡** 反正就三种方法，随便试
  
  ```javascript
  // 方法一
  event.stopPropagation();
  
  // 方法二
  event.preventDefault();
  
  // 方法三
  return false
  ```
  
- **select标签disabled掉过后表单提交不上去那个字段**: 我也不知道什么原因，但是确实是这样的，可以用[stackoverflow](http://stackoverflow.com/questions/1191113/how-to-ensure-a-select-form-field-is-submitted-when-it-is-disabled)里的方法:

  ```html
  <select name="myselect" disabled="disabled">
      <option value="myselectedvalue" selected="selected">My Value</option>
      ....
  </select>
  <input type="hidden" name="myselect" value="myselectedvalue" />		<!--这里用js来控制或者说我现在的需求就是已经有值过后不然更改，那么直接写死这里的value就行了嘛-->
  ```

- **禁用radion标签**

  ```javascript
  <input type="radio" name="foo" value="Y" checked>
  <input type="radio" name="foo" value="N" disabled>
  ```

* **在Laravel中如果出现TokenMismatchException**，有可能是Laravel的CSRF机制造成的，解决办法参见<http://www.golaravel.com/laravel/docs/5.0/routing/>，即 首先在meta中添加

  ```html
  <meta name="csrf-token" content="{{ csrf_token() }}" />
  ```

  然后设置ajaxSetup:

  ```javascript
  <script type="text/javascript">
      $(function(){
      $.ajaxSetup({
          headers: {
              'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
          }
      });
          $('#publish').bind('click', function(){        // ajax事件
              $.ajax({
                  。。。
             });
  </script>
  ```

* **Laravel 5 要使用Input获取输入的信息**，必须先`use Input`，看来Laravel 5 对命名空间的管理更加严格了

* **Ajax请求总是执行error部分代码/Ajax文件上传**，原因可能是返回数据的格式不对，一定要返回dataType所规定的数据格式
    上传文件，需要特殊的几个参数和变量

    ```javascript
    $('input#uploadh').bind('change', function(){
        var f = this.files;
        var formdata = new FormData();
        formdata.append('image', f[0]);	// 或者$("#uploadh")[0].files[0]);
        $.ajax({
            url: "{{ url('uploadimg') }}",
            type: "POST",
            data: formdata,
            dataType: "json",
            processData: false,
            contentType: false,
            success: function(data){
                alert('成功');
            }
        });
    });
    ```

* 如果是通过一个button而不是input提交的话，那么可以这样使用.需要注意的是，只能一个文件一个文件地append，后台才能通过request.FILES看到

    ```javascript
    $('button#uploadFile').on('click',function(){ 
        var f = $('input#uploadFile')[0].files;
        var formadata = new FormData();
        formdata.append('image', f[0]);
    });
    ```

* **获取当前元素的父元素**，使用target，但有时候也可以不用target...我也是醉了 获取同级的元素：prev()和next()


* ```javascript
     $('button#post').bind('click', function(ele){
     $.ajax({
         url: port,
         type: "POST",
         dataType: "json",
         error: function(error){
             alert('出错啦');
         },
         success: function(data){
             alert($(ele.target).parent().parent().attr('id'));
         }
     });
     ```


* 在ajax的url里面，默认是相对于当前地址的url，例如

  ```tex
  当前地址是http://localhost/a，那么url: 'publish'表示http://localhost/publish
  当前地址是http://localhost/a/b，那么url: 'publish'表示http://localhost/hehe/publish
  只有写为url: '/publish'才表示相对于根域名，即http://localhost/publish
  ```

* **给生成的元素动态绑定事件**：SegmentFault说直接用.on方法可以实现1.7之前.live的动态绑定功能，但是我就是不行，这里使用.on的另外一种方法，绑定到document上去就行了，原理就是将事件委托给父元素，然后由父元素绑定给子元素：

     ```javascript
     $(document).on('click', 'button', function(){
     	alert('dg');
     });
     ```

* **绑定回车事件**：

     ```javascript
     $(document).on('keypress', 'input', function(event){
     if(event.keyCode == '13'){
         alert('success');
     });
     ```

* 提交表单时，如果想增加额外的参数，可以添加动态添加一个隐藏标签： 

  ```javascript
  var input = $("<input>").attr("type", "hidden").attr("name", "字段名").val("value");
  $('#form1').append($(input));
  ```

* `<select>`元素的选择`<option>`事件是`change`，而获得所选择元素使用的是`val()`，默认被选择：`<option selected="true" value="xxx">xxx</option>`，获取文本内容用`text()`

* **避免表单回车自动提交**：有时候想在表单提交前进行一些操作，但又不想在回车时自动提交表单(当只有input的时候，会强制提交)，这时候只需要在button的回车事件中添加`return false`即可

* **无法获取iframe里面的内容**: 一个iframe表示一个窗口，并且还对应不同的域名，默认情况，放任一个网页，脚本都默认在最上层的窗口上面，在谷歌浏览器的`审查元素`视图下的`Console`的左上角可以选择定位到哪个`iframe`，如果是爬虫或者油猴脚本，要注意对应iframe的url。

* **onclick的时候将标签本身作为参数**: `onclick="dothing(this);"`

* **onclick的时候直接阻止冒泡**: `<span onclick="event.stopPropagation(); alert('ok');"></span>`

* **js实现点击自动复制到剪贴板**: 

     ```javascript
     var text_tag = document.getElementById("text");
     text_tag.select();
     document.execCommand("Copy");
     
     // 如果要复制自定义的内容或者在hidden的input上面复制可以创建一个临时的element，来自https://stackoverflow.com/questions/31593297/using-execcommand-javascript-to-copy-hidden-text-to-clipboard
     var tempInput = document.createElement("input");
     tempInput.style = "position: absolute; left: -1000px; top: -1000px";
     tempInput.value = value;
     document.body.appendChild(tempInput);
     tempInput.select();
     document.execCommand("copy");
     document.body.removeChild(tempInput);
     ```

* **打开新标签页**: `window.open(pageURL,name,parameters) / window.open(url, '_blank')`

* **$('form').serialize()表单序列化时无法正确获取`checkbox`的值**: 可以在`checkbox`前添加一个隐藏的`input`，两者使用同样的`name`，这样在表单提交的时候会提交两个值，但是后端都是选择的后面那个值

     ```html
     <input type="hidden" name="option" value="false"/>
     <input type="checkbox" name="option" value="true"/>
     ```

- **隐藏CNZZ“站长统计”四个字**: 直接在添加这行js:

  ```javascript
  $('a').last().hide();
  ```

- **Unexpected token o in JSON at position 1**: 原因是在使用`JSON.parse(str)`的时候，传入的不是字符串而是一个对象，即`[object Object]`，把`[`理解为了数组的开始，但是`o`就无法理解了。

- **Uncaught TypeError: a.indexOf is not a function**: 版本问题。`$(window).load(function(){})`在高版本中已经废弃了，需要用`$(window).on('load', function(){})`替代。如果仍然有问题，可以直接引入一个兼容包`<script src="https://code.jquery.com/jquery-migrate-1.4.1.min.js"></script>`

- **出发表单submit事件但是不想要表单自动提交并刷新网页**: 

  ```javascript
  $('#contactForm').submit(function () {
   sendContactForm();
   return false;
  });
  ```

- **限制input框输入特殊字符**

  ```javascript
  $(".myinput").keypress(function (e) {
  	if ((event.which != 46 || 
         $(this).val().indexOf('.') != -1) && 
        (event.which < 48 || event.which > 57)
       ) {
  		return false;
  	}
  });
  ```
  
- **上传图片后实时预览图片**

  ```javascript
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#file').attr('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  $("#img_preview").change(function() {
    readURL(this);
  });
  ```
  
- **select元素实现重复点击取消选择**

  ```javascript
  $('select option').on('click', function (e) {
    this.selected = !this.selected;
    e.preventDefault();
  });
  ```
  
- **添加英文数字索引前缀**：得到1st 2nd 3rd等

  ```javascript
  function ordinal_suffix_of(i) {
      var j = i % 10,
          k = i % 100;
      if (j == 1 && k != 11) {
          return i + "st";
      }
      if (j == 2 && k != 12) {
          return i + "nd";
      }
      if (j == 3 && k != 13) {
          return i + "rd";
      }
      return i + "th";
  }
  ```

- **JS Input 延时触发/延迟触发**: 常用于autocomplete，不想每次都去查询接口，而是间隔很短时间去查询:

  ```javascript
  const timer = null;
  
  function onInputChange(){
  	const value = document.getElementById("input").value;
    clearTimeout(timer);
    timer = setTimeout(function () {
      console.log(value);
    }, 500);	// 做一个500毫秒的延时
  ```

- **Property 'style' does not exist on type 'Element'**: 需要强制声明其类型: `Array.from(document.getElementsByClassName('test') as HTMLCollectionOf<HTMLElement>)`

- **moment Not in a recognized ISO format**: 这是moment无法自动解析其他格式的时间，这时候需要制定格式，例如`moment('2021-6-28', 'YYYY-M-D')`

- **input输入框仅允许输入数字，去掉字符串中的非数字字符**: 

  ```javascript
  $('input').on('keyup', function() {
    $(this).val($(this).val().repalce(/[^0-9]/g, ''))
  })
  
- **dayjs_1.default is not a function**: 可以尝试在tsconfig中添加配置`esModuleInterop: true`

- **显示精确的实时时间，精确到秒**: 我发现angular的get方法并不能在date变化的时候实时更新，这样还不如直接用interval:

  ```javascript
  setInterval(() => {
    this.now = new Date();
  });
  ```
  
- **Uncaught TypeError: Illegal invocation**: 发生于使用多层调用内置函数的情况，例如:

  ```javascript
  var obj = { alert: alert};
  obj.alert('hello');		// 这样就会报错
  
  var obj = { alert: alert.bind(window) }
  obj.alert('hello');		// 这样就能正常调用了
  ```


##### 扩展阅读

- [一大波JS开发工具函数](https://zhuanlan.zhihu.com/p/113385396?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)
- [blowup.js](https://github.com/paulkr/blowup.js): 一个比较简单好用的类似淘宝图片放大的jQuery插件
