---
title: "HTML 教程"
date: 2014-12-02 22:52:39
updated: 2020-07-19 16:10:00
categories: frontend
---
# Html
## 基本格式

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

##### rel属性

- 用于指定当前文档与被链接文档的关系
- alternate(文档的可选版本)、stylesheet(文档的外部样式表)、start(集合中的第一个文档)、next(集合中的下一个文档)、prev(集合中国呢的前一个文档)、contents(文档目录)、index(文档索引)、glossay(文档中所用字词的术语表或解释)、copyright(包含版权信息的文档)、chapter(文档的章)、section(文档的节)、subsection(文档的字段)、appendix(文档附录)、help(帮助文档)、bookmark(相关文档)、nofloow(指定谷歌搜索引擎不要跟踪链接)、licence、tag、friend

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
  <video>
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

```js
# 获取画布
<canvas id="myCanvas" width="200" height="100"></canvas>
var canvas = document.getElementById('myCanvas')

# 画布属性
canvas.width/canvas.height
ctx.clearRect(0, 0, canvas.width, canvas.height): 清空画布

# 设置图形的组合样式
ctx.globalCompositeOperation = 'source-over';	# 默认source-over表示后画的覆盖先画的，destination-over表示后画的在下面，还有跟多的组合样式

# 画直线
var ctx = c.getContext('2d');
ctx.strokeStyle = '#AAAAAA';
ctx.moveTo(0, 0);
ctx.lineTo(200, 100);
ctx.stroke();

# 画圆
var ctx = c.getContext('2d');
ctx.fillStyle = 'green';
ctx.beginPath();
ctx.arc(15, 15, 30, 0, 2 * Math.PI);
ctx.closePath();
ctx.fill();

# 写字
var ctx = c.getContext('2d');
ctx.font = '30px Arial';
ctx.fillText('Hello World', 10, 50);

# 将canvas内容转换为图片
var dt = canvas.toDataURL('image/png');	# 得到的值是图片的base64编码
```

## TroubleShooting
- **合并单元格**

   <td colspan="2">内容</td>


* **`<a href="..." download></a> `可以直接将a标签的内容进行下载  **

* `&nbsp`html中的空格

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

  
