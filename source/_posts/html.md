---
title: "HTML 教程"
date: 2014-12-02 22:52:39
updated: 2018-09-05 23:10:00
categories: frontend
---
# Html
## 基本格式

```html
<!DOCTYPE html>                   <!--文档声明-->
<html lang="zh-CN">               <!--指定页面语言-->
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">    <!--兼容IE-->
    <title>标题信息</title>
    <link href="styles.css" rel="stylesheet" ><!--添加样式表-->
    <link rel="icon" href="favicon.ico" type="image/gif" sizes="16x16">	<!--设置favicon-->
      
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

## 常用控件

```html
  # 单行文本框
  <input type="text" value="默认值">或<input type="password">
  # 多行文本框
  <textarea>默认值</textarea>
  # 复选框
  <input type="checkbox">
  # 单选按钮
  <input type="radio">
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
