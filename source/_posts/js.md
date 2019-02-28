---
title: "JavaScript & Ajax & jQuery教程"
date: 2015-02-07 11:52:39
updated: 2019-02-26 21:12:00
categories: frontend
---
# JavaScript & Ajax & jQuery

TODO: 逐步用原生方法替换jQuery，参考[You-Dont-Need-jQuery](https://github.com/oneuijs/You-Dont-Need-jQuery#query-selector)

## 基本语法

### 变量

```javascript
var $a;	// es6以前定义变量，if (true) {var a = 1;} console.log(a); 输出为1
let $b;	// es6用于定义跨级作用域本地变量，if (true) {let b = 1;} console.log(b);输出为undefined
const $c;	// 定义常量
window.test = 123;	// 声明全局变量
```

<!--more-->

### 对象

```javascript
object instanceof constructor	// 判断某个对象是否属于某个类
var copyObj = Object.assign({}, original_obj);	// 对象的深拷贝，直接用等于赋值是浅拷贝
```

### 数组

```javascript
arrA.concat(arrB)			// 合并两个数组
arr.indexOf('元素')			// 获取某个元素在数组中的下标，查看某个元素是否存在于数组中，没有在返回－1
JSON.stringify(Array)		// 将数组转换为JSON格式的字符串
arr.toString(): 数组转字符串，中间会自动加上逗号
arr.join(''): 数组转字符串，分隔符可自定义
arr.push(obj)		// 在数组尾部添加元素
arr.pop(obj)		// 去除数组尾部元素
arr.unshift(obj)	// 在数组头添加元素
arr.shift(obj)		// 去除数组头部元素
arr.slice(start, end): 数组分片

// 遍历数组方法
for (var index in arr) {}
a.forEach(function(value, key, arr) {}); 
arr.map((value) => {console.log(value); return newValue;}) // 返回值为一个新的数组，原数组不会改变
arr.filter(function(value, key, arr) {return true}); // 返回新数组，如果元素返回true则保留，返回false则抛弃
arr.some(function(value, key, arr){});	// 筛选数组，如果返回true则停止循环。返回布尔值，表示是否有满足条件的
arr.every(function(value, key, arr){});	// 筛选数组，是否每个元素都返回true

// for jQuery
$.each($array, function(k, v){});	// 遍历数组
$.inArray('a', $arr): 判断数组是否包含某个元素
delete a['a']	// 删除字典元素，如果用它来删除数组中的元素，删除完以后，数组总的长度不变，元素会被换成undefined，和php一样的坑
```
### 数字

```javascript
Math.floor(0.2);	// 向下取整
Math.floor(0.2);	// 四舍五入
Math.ceil(0.2);		// 向上取整

num.toString(8);	// 把数字转换为指定进制的字符串
```
### 字符串

```javascript
// 正则
var re = new RegExp("a|b", "i");	// 通过字符串来生成正则表达式，相当于/a|b/i

// 搜索
str.match(/<title>(.*?)<\/title>/)	// 正则提取
str.match(/<title>(.*?)<\/title>/g)	// 全局搜索，不加g默认只取找到的第一个嘛，但是global不支持分组，会把前后的都给返回到结果中去。这种情况，要么匹配后，循环对结果进行前后去除；要么用exec对先行获取每一个结果的match[1]
str.match(/<title>(<abc>.*?)<\/title>/)	// 正则提取，带命名组的正则提取

// 去除空格
str.replace(/\s+/g, "")    		// 去除所有的空格
str.trim() / str.replace(/^\s+|\s+$/g, "")	// 去除两端的空格
str.trimLeft() / str.replace( /^\s*/, '')		// 去除左边的空格
str.trimRight() / str.replace(/(\s*$)/g, "")		// 去除右边的空格
str.replace(/[\r\n]/g, ' ')	// 去掉换行

JSON.parse(text)	// 将字符串转换为JSON
str.replace(reg, function(s, value){})	// 替换字符串，reg可以是正则表达式
str.indexOf(substring)	// 查找子字符串出现的位置，-1表示没找到
string.slice(start, end);	// 字符串分片
str.split('#')	// 字符串分割，返回分割后的列表
str.split(/\s+/) // 也可以用正则分割
str.split('...', n)	// n表示返回数组的最大长度，分割还是会分割成所有，只是返回前n个
parseInt(数字)  // 将数字取整

btoa(str);	// 字符串转换为base64
atob(str);	// base64转换为字符串

a = encodeURIComponent(uri);	// url编码
b = decodeURIComponent(uri);	// url解码
```

#### 时间处理

`XDate`

```javascript
Date.parse(new Date());	// 获取时间戳，单位为毫秒
```

## DOM操作

### 元素查找

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
ele.getElementsByTagName('td');	// 查询子元素
ele.getElementsByClassName('myclass');	// 查询子元素
ele.firstElementChild;
ele.lastElementChild
ele.nextElementSibling;	// 获取下一个兄弟节点
ele.previousElementSibling;

// jQuery元素选择
$('p')  		// 选取标签<p>的所有元素
$('p#intro')  	// id为intro的所有p元素
$('p.intro')  	// class为intro的所有p元素
$('p:first')  	// 选取第一个<p>元素
$('p a:first')	// 选取p元素下的第一个a元素
$('p[name=abc]')
$('*')        		// 所有元素
$(this)       		// 当前元素
$(this).next()  	// 获取下一个同级元素
$(this).prev()		// 获取上一个统计元素
$(this).parent()	// 获取父元素
$(this).children()	// 获取子元素
$(this).nextAll('cl')	// 获取指定元素的所有指定的同级元素
$('p').find('input')	// 查找input下的所有input元素		
$('input:checked') 		// 查找所有checked为true的checkbox的input元素
document.getElementById('test:abc')	// 有特殊字符的元素的查找，jquery往往无法处理过来
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

// jQuery方法
$('#check').prop('checked')	// 获取checkbox是否被check了，不用给你用attr
$('div').height()	// 获取元素高度
$('div').height(20)	// 设置元素高度
$('select').val()	// select标签的值
$('select option:selected').text();	// select被选中项的文本
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
selection.innerHtml = '<option>a</option';	// 修改内部html内容
parentElement.insertBefore(newElement, referenceElement);	// 插入子元素

// 添加元素
html('')	// 修改内部的html内容
append()	// 在被选元素的结尾插入内容
prepend()	// 在被选元素的开头插入内容
after()		// 在被选元素之后插入内容
before()	// 在被选元素之前插入内容
remove()	// 删除当前元素
empty()		// 清空当前元素的子元素

// 属性更改
addClass('')	// 给元素添加类
removeClass('')	// 给元素移除某个类
$('p').css('color', 'red')			// 修改CSS属性
$('button').prop('disabled', true)	// 设置按钮不可点击disabled
$('p').hide()	// 隐藏元素
$('p').show()	// 显示元素
$('img').attr('src', 'xxx')	// 改变元素的属性

// video标签控制
myVideo.play()	// 开始播放
myVideo.pause()	// 暂停播放

// 创建元素
var a_tag = document.createElement('a');	// 首先创建一个空元素
parent_tag.after(a_tag);	// 然后将元素放到指定的位置
a_tag.outerHTML = '<a class="..." name="">ok</a>'; // 最后将元素html替换成我们想要的
```

### 元素事件
```javascript
// js原生事件
ele.onchange = function () {};
ele.onchange = funciton () {};
ele.addEventListener('click', func () {});
ele.removeEventListener('change', func () {});

// 页面事件
window.onload = function () {};	// 页面加载完成后触发
document.onkeyup = function(e) {};	// 用户按键事件

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
$('a').trigger('click')  // 触发a标签的click事件
$('#myModal').modal('show')  // bootstrap中modal的触发

// 事件的订阅
$('p').bind('click', function(){})	// 用bind进行事件的绑定，即使是之后生成的元素也能与事件绑定
```
### 页面属性
```javascript
document.cookie					// 当前cookie
document.cookie = 'abc=123';		// 添加cookie，注意这是添加，不是设置
document.cookie = 'abc=123; expires=' + date.toGMTString() + ';'	// 设置过期时间
window.location.href 			// 获取当前的url
window.lcoation.href = 'url'	// 跳转到某个url
document.referrer				// 获取当前页面的referer，是一个read only属性，不可以在ajax里面改变，改不了，md
location.reload()				// 刷新当前页面

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
$(document).ready(function);	// 当DOM已经加载，并且页面已经完全呈现时，会发生ready事件。
```
### 特殊函数

```javascript
// 定时器
var t = window.setTimeout(func(), delay);	// 延迟delay秒后执行函数func
var t = window.setInterval(func(), delay);	// 每隔delay秒就执行函数func
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
```

## Ajax

最普遍的用法:

```javascript
$.ajax({
	url: 'url',
	dataType: 'json',
	type: 'POST',
	data: data,
	error: function(re){
	},
	success: function(re){
	}
    complete: function(re) { 	 // 无论怎样都会执行
        if (re.statusText == "success") { 
            console.log("Sent successfully");
        } else { 
            console.log("Not Sent");
        }
    }
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

## 调试技巧

- **代码中打断点直接`debugger;`语句，这样浏览器会自动在该处断点，对于会有js压缩的代码调试非常有用**
- **浏览器console.log**打印出来的对象，如果没有点击展开，那么点开的时候会是最后一次该对象的值。

## 推荐阅读

- [You-Dont-Need-jQuery](https://github.com/nefe/You-Dont-Need-jQuery/blob/master/README.zh-CN.md)

## TroubleShooting

- **根据select的选项不同跳转到不同的页面**:
  `<select onchange="location.href=this.options[this.selectedIndex].value;">`

- **Ajax请求无论是GET还是POST都突然变成了OPTIONS请求**
  可能是因为把本地代码提交到服务器时，发生了跨域请求错误，url里面写的是本地的端口地址，这时候只需要修改本地的端口地址修改为相对于服务器的本地地址即可

- **停止js的冒泡** 
  `window.event? window.event.cancelBubble = true : evt.stopPropagation();`

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

* **Ajax请求总是执行error部分代码**，原因可能是返回数据的格式不对，一定要返回dataType所规定的数据格式
    上传文件，需要特殊的几个参数和变量

    ```javascript
    $('input#uploadh').bind('change', function(){
        var f = this.files;
        var formdata = new FormData();
        formdata.append('image', f[0]);
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

* **js实现点击自动复制到剪贴板**: 

     ```javascript
     var text_tag = document.getElementById("text");
     text_tag.select();
     document.execCommand("Copy");
      5 Url2.select(); // 选择对象
     ```

* **打开新标签页**: `window.open(pageURL,name,parameters)  `

* **$('form').serialize()表单序列化时无法正确获取`checkbox`的值**: 可以在`checkbox`前添加一个隐藏的`input`，两者使用同样的`name`，这样在表单提交的时候会提交两个值，但是后端都是选择的后面那个值

     ```html
     <input type="hidden" name="option" value="false"/>
     <input type="checkbox" name="option" value="true"/>
     ```

- **Uncaught TypeError: Illegal invocation**: 发生于使用多层调用内置函数的情况，例如:

  ```javascript
  var obj = { alert: alert};
  obj.alert('hello');		// 这样就会报错
  
  var obj = { alert: alert.bind(window) }
  obj.alert('hello');		// 这样就能正常调用了
  ```
