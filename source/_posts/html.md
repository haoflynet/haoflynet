---
title: "HTML 教程"
date: 2014-12-02 22:52:39
updated: 2021-10-15 08:10:00
categories: frontend
---
# Html
## 基本格式

- `defer`和`async`的区别:
  - defer: `<script defer src="myscript.js"></script>`，加载后续文档元素的过程将和该脚本的加载并行进行(异步)，并在最后执行
  - async: `<script async src="script.js"></script>`，加载后续文档元素的过程将和该脚本并行进行，并在最后执行
  - 什么都没有则是立即加载并且立即执行

```html
<!DOCTYPE html>                   <!--文档声明-->
<html lang="zh-CN">               <!--指定页面语言-->
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">    <!--兼容IE-->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">	<!--编码声明-->
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">	<!--将网页中的http请求默认提升到https请求，防止出现mixed-content错误-->
    <title>标题信息</title>
    <link href="styles.css" rel="stylesheet" ><!--添加样式表-->
    <link rel="icon" href="favicon.ico" type="image/gif" sizes="16x16">	<!--设置favicon-->
    <link rel="canonical" href="https://haofly.net/html" />	<!--权威内容标签，SEO有用，可以参考https://ahrefs.com/blog/zh/canonical-tags/-->
		<link rel="alternate" href="https://haofly.net/en/html" hreflang="en" /> <!--网页可选语言-->
    
    <script src="scripts.js"></script> <!--添加Js脚本-->
    <style type="text/css"></style> <!--内嵌CSS-->
  </head>
  <body>
    页面主体
    <p>段落</p>       <!--段落-->
    <br>             <!--换行-->
    <hr>             <!--水平线-->
    <img alt="Horsehead" src="Horse.jpg" />  <!--图片-->
  </body>
</html>
```

<!--more-->

## 语法规范

* **缩进**：缩进设置为2个空格的宽度，嵌套元素都缩进一次
* **引号**：全部使用双引号(虽然html5在很多地方可以使用单引号)
    * **注释**：<!--注释内容-->
    * **字符编码**：全部采用UTF-8
    * **属性顺序**：`class id name src href title alt`

## 标签列表

### a标签

##### href=”javascript:void(0);”

- 当要a标签表现为链接形式又需要用js来执行的时候可以这样写href，而不是直接将href删除
- 如果直接`href="#position"`表示跳转到指定id的元素，俗称"喵点"

##### rel属性

- 用于指定当前文档与被链接文档的关系
- alternate(文档的可选版本)、stylesheet(文档的外部样式表)、start(集合中的第一个文档)、next(集合中的下一个文档)、prev(集合中国呢的前一个文档)、contents(文档目录)、index(文档索引)、glossay(文档中所用字词的术语表或解释)、copyright(包含版权信息的文档)、chapter(文档的章)、section(文档的节)、subsection(文档的字段)、appendix(文档附录)、help(帮助文档)、bookmark(相关文档)、nofloow(指定谷歌搜索引擎不要跟踪链接)、licence、tag、friend

### button

- button的三种type: submit(默认值)/button/reset，如果一个`form`里面有多个未指定`type`的`button`，那么点击他们都会提交`form`，所以需要未非`submit`的`button`制定`type="button"`

### form

- 表单中如何设置数组:

  ```html
  <input type="text" name="users[1]['name']" />
  <input type="text" name="users[2]['name']" />
  ```
  
- 点击`submit`但是阻止`form`表单默认的`submit`行为:

  ```javascript
  $("body").on("submit", "form", function( event ){
      event.preventDefault();
  });
  ```
  
- 原生方法验证表单:

  ```javascript
  const form = document.getElementById(formId);
  form.checkValidity(); // 报错则返回false
  form.reportValidity(); // 以原生的方式显示错误信息
  
  const inputField = document.getElementByName('name');
  name.checkValidity(); name.reportValidity(); // 也可以直接在指定元素上进行校验
  ```

### input

- accept(当为文件上传时，指定上传文件的类型)、alt(当为图片上传时，定义图像输入的替代文本)、autocomplete(是否开启自动完成)、autofocus(页面加载时是否自动获得焦点)、checked(是否被选中)、disabled(是否禁用)、form(规定输入字段所属的一个或多个表单)、formaction(覆盖表单的action属性)、formencrypt(覆盖表单的enctype属性)、formmethod(覆盖表单的method属性)、formnovalidate(覆盖表单的novalidate属性，提交表单时不需要验证)、formtarget(覆盖表单的target属性)、width/height(当为图片上传时定义input字段的高度)、max(规定输入字段的最大值)、maxlength(规定输入字段的字符的最大长度)、min(规定输入字段的最小值)、multiple(可选择多个文件)、pattern(规定输入字段的格式，例如pattern="[0-9]")、readonly、required、size(输入字段的宽度)、src(定义以提交按钮形式显示的图像的URL)

- type=number数字输入框

  ```html
  <input type="number">
  <input type="number" step="10" min="0" max="100">	<!--设置步长、最小值和最大值-->
  <input type="number" step="0.01"> <!--允许小数点-->
  
  <!--提供建议值-->
  <input id="ticketNum" type="number" name="ticketNum" list="defaultNumbers">
  <span class="validity"></span>
  <datalist id="defaultNumbers">
    <option value="10045678">
    <option value="103421">
    <option value="11111111">
    <option value="12345678">
    <option value="12999922">
  </datalist>
  ```

- 隐藏数字输入框的上下箭头:

  ```css
  /* Chrome, Safari, Edge, Opera */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  
  /* Firefox */
  input[type=number] {
    -moz-appearance: textfield;
  }
  ```

### radio

- 当在`radio`中使用`required`时，只需要在第一个`radio`中设置即可

### textarea

- 支持的html属性: rows(文本区域可见的高度)、cols(文本区域可见的宽度)、autofocus(页面加载时是否自动获得焦点)、maxlength(规定文本区域允许的最大字符数)、raadonly(规定文本区域为只读)、required(规定文本区域是否为必填)

```html
<textarea rows="10" cols="30">内容</textarea>
```

## 常用控件

```html
# 单行文本框
<input type="text" value="默认值">或<input type="password">

# 文件上传
<input type="file" accept="image/*" />

# 多文件上传
<input type="file" accept="image/*" multiple />

# 多行文本框
<textarea>默认值</textarea>
  # 复选框
  <input type="checkbox">
  # 单选按钮
  <input type="radio" disabled>	// 单选按钮不能用readonly来禁用
  # 按钮
  <input type="submit">
  # 列表
  <select>...</select>
  # 音频
  <audio src="hehe.mp3" controls></audio>
  # 视频
	<video controls <!--是否展示控制工具栏，播放按钮，播放进度条-->
         preload="metadata">	<!--preload="metadata"能使预先抓取一张图片，这里是0.5秒处的图片作为缩略图--->
		<source src="https://xxx.mp4#t=0.5" type="video/mp4">
  </video>
# 表单
<form>
  <table>
    <tr>
      <td></td>
      <td></td>
    </tr>
  </table>
</form>

# 链接
<a href="url"></a>  # a标签的target属性: 默认为_self表示当前框架中打开网页，_blank表示新窗口中打开网页
<hr>	横线
```


## 语义标签

**time**：用于标注日期和时间 
**nav**：用于标识一组导航链接 
**footer**：用于标识通常放在页面地步的代码 
**header**：可以把各种标题放在里面 
**article**：表示一个完整的内容块，比如博客文章，应该包括标题、作者以及正文 
**hgroup**：用于标注副标题 
**section**：表示一个区块，是一个通用容器  


## Canvas

```javascript
// 获取画布
<canvas id="myCanvas" width="200" height="100"></canvas>
var canvas = document.getElementById('myCanvas')

// 画布属性
canvas.width/canvas.height
ctx.clearRect(0, 0, canvas.width, canvas.height): 清空画布

// 设置图形的组合样式
ctx.globalCompositeOperation = 'source-over';	// 默认source-over表示后画的覆盖先画的，destination-over表示后画的在下面，还有跟多的组合样式

// 画直线
var ctx = c.getContext('2d');
ctx.strokeStyle = '#AAAAAA';
ctx.moveTo(0, 0);
ctx.lineTo(200, 100);
ctx.stroke();

// 画圆
var ctx = c.getContext('2d');
ctx.fillStyle = 'green';
ctx.beginPath();
ctx.arc(15, 15, 30, 0, 2 * Math.PI);
ctx.closePath();
ctx.fill();

// 写字
var ctx = c.getContext('2d');
ctx.font = '30px Arial';
ctx.fillText('Hello World', 10, 50);

// 将canvas内容转换为图片
var dt = canvas.toDataURL('image/png');	// 得到的值是图片的base64编码
```

## TroubleShooting
- **合并单元格**

   <td colspan="2">内容</td>


* **`<a href="..." download></a> `可以直接将a标签的内容进行下载  **

* `&nbsp`html中的空格

* **浏览器无法显示HEIC格式的文件**: 从ios上传图片会自动转换为JPG格式，但是通过airdrop传送给mac，再通过safari从网页上传则是heic格式，浏览器默认不会展示，而是直接下载，导致无法显示HEIC格式的图片，可以在上传完成后进行格式转换，或者在input的accept属性指定哪些image格式允许

* **网页视频或音频无法自动播放的问题**: 新版本的浏览器中，只有静音的网页视频可以自动播放，其他有音频的都无法自动播放(但是在微信或者qq这种应用内部自带的浏览器是允许自动播放的)。不过在[stackoverflow](https://stackoverflow.com/questions/50490304/how-to-make-audio-autoplay-on-chrome)上也找到一种在浏览器里有用的绕过方式(但是在手机浏览器中仍然不行): 

  ```html
  <!--在网页中同时使用这两个标签 -->
  <iframe src="silence.mp3" allow="autoplay" id="audio" style="display:none"></iframe>
  <audio id="player" autoplay loop>
      <source src="audio/source.mp3" type="audio/mp3">
  </audio>
  ```

  还有一种方式是让用户在网页触发一次交互操作，无论什么东西，也不一定要点击音频，只要点击后就能用js去进行播放了。如果在用户没交互操作的情况下用js进行`audio.play()`那么会报错:**`Uncaught (in promise) DOMException: The play() request was interrupted by a new load request.`**，这是因为`play()`在新版本里面变成了一个异步函数，必须主动`catch`这个`promise`，例如:

  ```javascript
  result = video.play();
  result.then().catch(error => {})
  ```


#####  扩展阅读

- [HTTP Content-type列表](https://tool.oschina.net/commons)