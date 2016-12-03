---
title: "JavaScript & Ajax & jQuery教程"
date: 2016-08-07 11:52:39
updated: 2016-11-21 17:08:00
categories: frontend
---
# JavaScript & Ajax & jQuery
## 基本语法
### 数组

	arr.indexOf('元素'): 获取某个元素在数组中的下表，没有在返回－11
	JSON.stringify(Array):	将数组转换为JSON格式的字符串
	arr.toString(): 数组转字符串，中间会自动加上逗号
	arr.join(''): 数组转字符串，分隔符可自定义
	arr.push(obj): 给数组添加元素
	arr.slice(start, end): 数组分片
	$.each($array, function(k, v){});	# 遍历数组
	$.inArray('a', $arr): 判断数组是否包含某个元素
### 字符串
	JSON.parse(text)	# 将字符串转换为JSON
	str.replace(reg, function(s, value){})	# 替换字符串，reg可以是正则表达式
	str.indexOf(substring)	# 查找子字符串出现的位置，-1表示没找到
	str.split('#')	# 字符串分割，返回分割后的列表

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

// 属性更改
addClass('')	// 给元素添加类
removeClass('')	// 给元素移除某个类
$('p').css('color', 'red')			// 修改CSS属性
$('button').prop('disabled', true)	// 设置按钮不可点击disabled
```

### 元素事件
```javascript
change()	// 当元素发生改变时触发，常用于input、select
focus()		// 元素获得焦点时触发
blur()		// 元素失去焦点时触发
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

## TroubleShooting
- **根据select的选项不同跳转到不同的页面**:

  <select onchange="location.href=this.options[this.selectedIndex].value;">

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

- 禁用radion标签

  ```javascript
  <input type="radio" name="foo" value="Y" checked>
  <input type="radio" name="foo" value="N" disabled>
  ```

  ​





#### load()

通过Ajax请求加载服务器中的数据，可直接把获取到的数据放置到指定的元素中去，其调用格式为： `load(url, [data], [callback]`
其中，url为服务器的地址，后面两个为可选参数，data为请求时所发送的数据，callback为回调函数。例如：



    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
      <meta charset="utf-8">
      <script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js"></script>
      <script type="text/javascript">
        $(function()\{
          $('#btn').bind('click', function()\{
            $(".content").load('a.txt');
          \});
        \});
      </script>
    </head>
    <body>
      <p class="content">以前的内容</p>
      <button id="btn">测试</button>
    </body>
    </html>

#### getJSON()

通过Ajax获取服务器中的数组，并对获取的数据进行解析，显示在页面中，其调用格式为： `$.getJSON(url, [data], [callback])`

#### getScript()

通过Ajax获取并执行服务器中的JavaScript文件，其调用格式为： `$.getScript(url, [callback])`

#### get()

使用Ajax的GET请求方式向服务器请求数据，请求所获得的数据保存在回调函数的参数中，其调用格式为： `$.get(url, [callback])`

回调函数要是用获取到的数据就定义为function(data)\{\}，其中data即使获取到的数据。

#### post()

使用Ajax的POST请求方式向服务器发送数据，其调用格式为： `$.post(url,[data],[callback])`

#### serialize()

序列化表单元素值，将表单中有name属性的元素值进行序列化，生成标准URL编码文本字符串，直接可用于ajax请求，其调用格式为
`$(selector).serialize()`

#### ajaxStart()和ajaxStop()

分别用于在该Ajax请求出发前和出发后所执行的函数，其调用格式为： `$(selector).ajaxStart(function()\{\}) &nbsp;
和 &nbsp;$(selector).ajaxStop(function()\{\}`

###  jQuery Ajax参数

| 参数名      | 类型     | 描述                                      |
| -------- | ------ | --------------------------------------- |
| data     | String | 发送到服务器的数据，将自动转换成请求字符串格式。 GET请求中附加在URL后。 |
| dataType | String | 预期服务器返回的数据类型，如下几种：                      |
"xml""html""script""json""jsonp""text"  
error |  Function |  请求失败时调用此函数  
success |  Function |  请求成功时调用此函数  
type |  String |  指定请求方式，默认为“GET”，可设置为“POST”或其它 例如“PUT”、“DELETE”等  
url |  String |  发送请求的地址，默认为当前页的地址  
如需传递数据只需要如下：



    $('button#publish').bind('click', function()\{
        var $data = {};
        $data.id = '----------------------';
        $.ajax(\{
        url: "\{\{ url('publish') \}\}",
        type: "POST",
        data: $data,     // 可以使用Input::get('id')来获取该数据
        dataType: "html",
        error: function()\{
            $('.message').html("出错啦");
            \},
        success: function(data)\{
            $('.message').html(data + $('.message').html())
        \}
        \});
    \});

## TroubleShooting：

* 在Laravel中如果出现TokenMismatchException，有可能是Laravel的CSRF机制造成的，解决办法参见<http://www.golaravel.com/laravel/docs/5.0/routing/>，即 首先在meta中添加

        <meta name="csrf-token" content="\{\{ csrf_token() \}\}" />

然后设置ajaxSetup：


        <script type="text/javascript">
        $(function()\{
        $.ajaxSetup(\{
            headers: \{
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            \}
        \});
            $('#publish').bind('click', function()\{        // ajax事件
                $.ajax(\{
                    。。。
               \});
    </script>

*   Laravel 5 要使用Input获取输入的信息，必须先`use Input`，看来Laravel 5 对命名空间的管理更加严格了
*   Ajax请求总是执行error部分代码，原因可能是返回数据的格式不对，一定要返回dataType所规定的数据格式
    * 上传文件，需要特殊的几个参数和变量

          $('input#uploadh').bind('change', function()\{  

          var f = this.files;
          var formdata = new FormData();
          formdata.append('image', f[0]);




        $.ajax(\{
        url: "\{\{ url('uploadimg') \}\}",
        type: "POST",
        data: formdata,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function(data)\{
        alert('成功');
         \}
    \});


\});

如果是通过一个button而不是input提交的话，那么可以这样使用： $('button#uploadFile').on('click',
function()\{ var f = $('input#uploadFile')[0].files; var formadata = new
FormData(); formdata.append('image', f[0]);
需要注意的是，只能一个文件一个文件地append，后台才能通过request.FILES看到

* 如果要在Ajax中读取其它Json文件，可以使用$.getJson方法，但是由于这个方法使用的是同步ajax的方式，而且即使是在其回调函数中也无法将返回值赋值到外部变量去，所以可以直接用ajax请求来取代它：

        var data = [];
    $.ajax(\{
      url: 'port.json',
      async: false,
      dataType: 'json',
      success: function (json) \{
        data = json.一个结点名称;
      \}
    \});
    alert(data);

* 获取当前元素的父元素，使用target，但有时候也可以不用target...我也是醉了 获取同级的元素：prev()和next()

          $('button#post').bind('click', function(ele)\{
          $.ajax(\{
              url: port,
              type: "POST",
              dataType: "json",
              error: function(error)\{
                  alert('出错啦');
              \},
              success: function(data)\{
                  alert($(ele.target).parent().parent().attr('id'));
              \}
          \});
      \});




*   在ajax的url里面，默认是相对于当前地址的url，例如

              当前地址是http://localhost/a，那么url: 'publish'表示http://localhost/publish
          当前地址是http://localhost/a/b，那么url: 'publish'表示http://localhost/hehe/publish
          只有写为url: '/publish'才表示相对于根域名，即http://localhost/publish

*   获取当前页面的URL信息：

                                window.location.pathname   # 获取当前url的后缀(域名后面的部分)
                            window.location.href       # 获取整个URL
                            window.location.port       # 获取端口号
                            window.location.protocol   # 获取URL的协议
                            window.location.host       # 域名加端口号
                            window.location.search     # 问号后面的部分

    * 判断是否存在某个节点

          if( $(this).length >= 1)\{
           alert('存在');
      \} else \{
          alert('不存在');
      \}

    * 给生成的元素动态绑定事件：SegmentFault说直接用.on方法可以实现1.7之前.live的动态绑定功能，但是我就是不行，这里使用.on的另外一种方法，绑定到document上去就行了，原理就是将事件委托给父元素，然后由父元素绑定给子元素：

          $(document).on('click', 'button', function()\{
          alert('dg');
      \});

    * 绑定回车事件：

          $(document).on('keypress', 'input', function(event)\{
          if(event.keyCode == '13')\{
              alert('success');
      \});

    * 查找元素： find可以查找所有子孙元素，children只查找第一级的元素，如果要在查找到的元素上继续查找，那么要使用括号将它变成一个jquery元素，例如：

          trs = $('tbody').children('tr');
      ths = $(trs[0]).children('th');

    * 序列化表单数据，然后通过ajax直接提交：

          $("button").click(function()\{
        $("div").text($("form").serialize());
      \});




    // 同样可以通过数组的方式来传递
    $("button").click(function()\{
      $("div").text($("form").serializeArray());
    \});  


* 提交表单时，如果想增加额外的参数，可以添加动态添加一个隐藏标签：  


        var input = $("<input>").attr("type", "hidden").attr("name", "字段名").val("value");
    $('#form1').append($(input));

*   


  ---
  title: "jQuery、JavaScript奇淫技巧"
  date: 2015-03-21 18:36:35
  categories: jquery
  ---
    * 基本运算  


          parseInt(数字)  # 将数字取整

    * 选择器  


          # 元素选择

      # 属性选择
      $('p[name=abc]') # name为abc的p元素，其中不等于用!=，$=表示以什么结束的元素
    
      # CSS选择
      $('p').css('background-color', 'red') # background-color为red的p元素
    
    * 元素事件  


          resize() # 大小调整，一般是$(window).resize(function()\{\})
      click    # 鼠标点击
      dbclick  # 鼠标双击
      mouseenter # 鼠标穿过元素
      mousesleave # 鼠标离开元素
      mousedown  # 鼠标移动到元素上方，并按下鼠标按键
      mouseup    # 在元素上松开鼠标按钮
      hover      # 模拟光标悬停事件
      focus      # 元素获得焦点
      blur       # 元素失去焦点
    
      # 触发事件
      $('a').trigger('click')  # 触发a标签的click事件
      $('#myModal').modal('show')  # bootstrap中modal的触发
    
    * 元素操作  


          $(selector).removeClass(class)  # 移除某个元素指定的类
      $('#image').attr('src', 'image...')  # 修改image元素的src属性

  今天在写代码的时候居然想着用POST请求来传递大段大段的html内容，后来一想，jQuery怎么可能没有直接操作网页元素的方法呢，果然，jQuery是可以直
  接操作DOM的。

  DOM(Document Object Model文档对象模型)，定义了访问HTML和XML文档的标准。

  ## 获取内容

  **text()**：设置或返回所选元素的文本内容

  **html()**：设置或返回所选元素的内容(包括HTML标记)

  **val()**：设置或返回表单字段的值

  一些不常用的获取方法：





  ## CRUD

  ### 删除

  remove()：

  detach()：会保留其所绑定的事件及附加的数据

  empty()：保留本身，删除所有子节点

  例如：



      $("div").remove("#3");   // 删除div标签里面id为3的标签

  ###  添加

  clone()：复制节点，如果带一个参数true，则表示会把该节点的所有绑定的事件一起复制

  replaceAll() / replaceWith()：替换节点

  append() / appendTo() / append(function(index,
  html)\{\})：在所选元素的最后的前面插入，其中index表示索引，而html表示其内容

  prepend() / prependTo() prepend(function(index, html)\{\})：在所选元素内部的最前面插入

  after() / insertAfter()：插入到所选节点的后面

  before() / insertBefore()：插入到所选节点的前面

  例如：这是一个ajax请求的success部分



      success: function(data)\{
          var $new_item = '<div class="item col-md-1">'+                                    '    <div class="panel panel-default">'+
                          '        <div class="panel-heading">' + data + '</div>' +                   '        <div class="panel-body">耶耶耶耶耶"</div>'+                 '    </div>'+                                     '</div>';
          $('.message').prepend(function(html)\{
              return $new_item;
          \});
      \}

  ### 修改

  直接将内容text修改即可

  ## TroubleShooting

    * <select>元素的选择<option>事件是change，而获得所选择元素使用的是val()，默认被选择：<option selected="true" value="xxx">xxx</option>
    * <input>元素，输入一个字符立马出发事件的event是：  


          $('#myinput').on('input', function()\{
          alert('aaaaaaaa');
      \});
    
    * 设置checkbox的属性，设置其它属性与此类似：  


          $("#checkbox_id3").attr("checked", true)    

      $("#checkbox_id3").attr("cdhecked", 'checked')
      $("#checkbox_id3").attr("checked", false)
      $"#checkbox_id3").attr("checked", '')
    
    * 判断是否有某个class：  


          $("button").click(function()\{
        alert($("p:first").hasClass("intro"));
      \});
    
    * jquery设置元素的CSS属性  


            $("p").css("color","red");

    * a标签href不跳转的方法  


          <a href="javascript:void(0);">呵呵</a>

    * 避免表单回车自动提交：有时候想在表单提交前进行一些操作，但又不想在回车时自动提交表单(当只有input的时候，会强制提交)，这时候只需要在button的回车事件中添加return false即可
    *   
