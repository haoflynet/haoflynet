---
title: "JavaScript & Ajax & jQuery教程"
date: 2015-02-07 11:52:39
updated: 2017-03-07 17:08:00
categories: frontend
---
# JavaScript & Ajax & jQuery
## 基本语法

### 变量

```javascript
var $a;	// es6以前定义变量，if (true) {var a = 1;} console.log(a); 输出为1
let $b;	// es6用于定义跨级作用域本地变量，if (true) {let b = 1;} console.log(b);输出为undefined
const $c;	// 定义常量
```

### 数组

```javascript
arr.indexOf('元素')			// 获取某个元素在数组中的下表，没有在返回－11
JSON.stringify(Array)		// 将数组转换为JSON格式的字符串
arr.toString(): 数组转字符串，中间会自动加上逗号
arr.join(''): 数组转字符串，分隔符可自定义
arr.push(obj): 给数组添加元素
arr.slice(start, end): 数组分片
$.each($array, function(k, v){});	# 遍历数组
$.inArray('a', $arr): 判断数组是否包含某个元素
```
### 字符串
	JSON.parse(text)	# 将字符串转换为JSON
	str.replace(reg, function(s, value){})	# 替换字符串，reg可以是正则表达式
	str.indexOf(substring)	# 查找子字符串出现的位置，-1表示没找到
	str.split('#')	# 字符串分割，返回分割后的列表
	 parseInt(数字)  # 将数字取整

## DOM操作
### 元素查找
```javascript
// 元素选择
$('p')  		// 选取标签<p>的所有元素
$('p#intro')  	// id为intro的所有p元素
$('p.intro')  	// class为intro的所有p元素
$('p:first')  	// 选取第一个<p>元素
$('p a:first')	// 选取p元素下的第一个a元素
$('p[name=abc]')
$('*')        	// 所有元素
$(this)       	// 当前元素
$(this).next()  // 获取下一个同级元素
$(this).nextAll('cl')	// 获取指定元素的所有指定的同级元素
$('p').find('input')	// 查找input下的所有input元素
$('input:checked') 		// 查找所有checked为true的checkbox的input元素
document.getElementById('test:abc')	// 有特殊字符的元素的查找，jquery往往无法处理过来
```

### 获取元素内容

```javascript
$('#check').prop('checked')	// 获取checkbox是否被check了，不用给你用attr
```

### 编辑元素

```javascript
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
```

### 元素事件
```javascript
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
resize() 	// 大小调整，一般是$(window).resize(function()\{\})

# 事件的触发
$('a').trigger('click')  // 触发a标签的click事件
$('#myModal').modal('show')  // bootstrap中modal的触发
```
### 页面属性
```javascript
window.location.href 			// 获取当前的url
window.lcoation.href = 'url'	// 跳转到某个url
location.reload()				// 刷新当前页面
```
### 特殊函数
```javascript
t = setInterval("show()",3000)	// 每隔3秒执行该函数
clearInterval(t)				// 清楚计时器
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

* Ajax请求总是执行error部分代码，原因可能是返回数据的格式不对，一定要返回dataType所规定的数据格式
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

    如果是通过一个button而不是input提交的话，那么可以这样使用.需要注意的是，只能一个文件一个文件地append，后台才能通过request.FILES看到

  ```javascript
    $('button#uploadFile').on('click',function(){ 
      var f = $('input#uploadFile')[0].files;
      var formadata = new FormData();
      formdata.append('image', f[0]);
    });
  ```

    如果要在Ajax中读取其它Json文件，可以使用$.getJson方法，但是由于这个方法使用的是同步ajax的方式，而且即使是在其回调函数中也无法将返回值赋值到外部变量去，所以可以直接用ajax请求来取代它：

  ```javascript
    var data = [];
    $.ajax({
        url: 'port.json',
    	async: false,
    	dataType: 'json',
    	success: function (json) {
      	data = json.一个结点名称;
          alert(data);
    	}
    });
  ```


* **获取当前元素的父元素**，使用target，但有时候也可以不用target...我也是醉了 获取同级的元素：prev()和next()

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
     });


*   在ajax的url里面，默认是相对于当前地址的url，例如

        当前地址是http://localhost/a，那么url: 'publish'表示http://localhost/publish
        当前地址是http://localhost/a/b，那么url: 'publish'表示http://localhost/hehe/publish
        只有写为url: '/publish'才表示相对于根域名，即http://localhost/publish

* **给生成的元素动态绑定事件**：SegmentFault说直接用.on方法可以实现1.7之前.live的动态绑定功能，但是我就是不行，这里使用.on的另外一种方法，绑定到document上去就行了，原理就是将事件委托给父元素，然后由父元素绑定给子元素：

         $(document).on('click', 'button', function(){
         	alert('dg');
         });

* 绑定回车事件：

         $(document).on('keypress', 'input', function(event){
         if(event.keyCode == '13'){
             alert('success');
         });



* 提交表单时，如果想增加额外的参数，可以添加动态添加一个隐藏标签： 

  ```javascript
  var input = $("<input>").attr("type", "hidden").attr("name", "字段名").val("value");
  $('#form1').append($(input));
  ```

* `<select>`元素的选择`<option>`事件是`change`，而获得所选择元素使用的是`val()`，默认被选择：`<option selected="true" value="xxx">xxx</option>`，获取文本内容用`text()`

* **避免表单回车自动提交**：有时候想在表单提交前进行一些操作，但又不想在回车时自动提交表单(当只有input的时候，会强制提交)，这时候只需要在button的回车事件中添加`return false`即可

