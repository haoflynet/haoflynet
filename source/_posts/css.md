---
title: "CSS教程"
date: 2015-01-11 08:12:39
updated: 2018-08-25 20:50:00
categories: frontend
---
## 浏览器兼容

- 首行的`<!DOCTYPE html>`很关键

- IE9以下需要专门调用这几个js

  ```html
  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
    <script src="http://apps.bdimg.com/libs/html5shiv/3.7/html5shiv.min.js"></script>
    <script src="http://apps.bdimg.com/libs/respond.js/1.4.2/respond.min.js"></script>
  <![endif]-->
  ```

- IE浏览器兼容模式，并且针对IE浏览器首先使用edge内核，对于多核浏览器，首先使用Chrome内核

  ```html
  <meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1" />
  ```

## 各种属性

##### a链接

a:link：表示一个正常的未被点击过的a标签的属性

a:visited: 表示一个已经被点击过的a标签的属性

a:hover: 鼠标移动到a标签上面

a:active: a标签被点击的时候

##### border边框

- border-color: 设置4个边框的颜色
- border-radius: 设置边框圆角大小
- border-style: 设置4个边框的样式。可能的值有none(无边框)、hidden(对于表，用于解决边框冲突，和none一样)、dotted(点状边框)、dashed(虚线)、solid(实线)、double(双线)、groove(3D凹槽边框)、ridge(3D垄状边框)、inset(3D inset边框)、outset(3D outset边框)、inherit(从父元素继承)
- border-width: 边框宽度

##### input

- text-align: 内容显示方式，`center`表示居中显示

##### margin

```css
margin: 10px 5px 15px 20px;	/*上 右 下 左*/
```

##### table

- overflow:scroll：如果表格超宽，让页面自动出现滚动条

##### text

- text-indent: 段落缩进设置

##### width元素宽度 

- max-width设置最大宽度，默认为none

##### word

- white-space: nowrap 强制不换行

##### user-select

- none(文本不能被选择)、text(可以选择文本)

## TroubleShooting
#### 元素居中方法
```css
方法一：
<center>...</center>
方法二：
div {margin:0 auto}
方法三：
.Absolute-Center {
	margin: auto;
	position: absolute;
	top: 0; left: 0; bottom: 0; right: 0;
}
# 方法四
.test {  
    float: none;  
    display: block;  
    margin-left: auto;  
    margin-right: auto;  
}  
```

#### 将某元素置于底层，使用z-index属性，例如：
	div {
		z-index; -100;   # 值越小，越底层，默认应该为0
	}

#### 文字模糊、阴影效果，使用text-shadow属性，例如：
	.menu a:hover{
		text-shadow: 0 0 10px gray;
	}

#### 控制元素的隐藏：
	# 这样不会占用位置
	<div id="div1" style="display:block;">DIV 1</div>

#### 文字环绕图片效果
	<div class="wrap">
		文字的前半部分
		<img src="test.png" style="float: left; padding: 0; margin: 3px 5px 0px 0px;">
		文字的后半部分
	</div>

#### 固定网站底部信息栏，使得无论内容多少都始终正好显示在底部
	html, body {
		height: 100%;
	}
	.wrapper {
		min-height: 100%;
		height: auto !important;
		height: 100%;
		margin: 0 auto -100px; // 这里负的是footer的高度
	}
	.footer {
		height: 100px;
	}
	# 然后，网页主体由以下部分组成：
	<html>
		<head></head>
		<body>
			<div class="wrapper"></div>
			<div class="footer"><div>       // 这里也可以用footer代替
		</body>
	</html>

以上，我的直觉告诉我会有更方便的方法，但是我居然没找到，谷歌上搜索出来几乎都是这个答案。

#### 判断屏幕宽度

```css
@media (min-width: 400px) {

}
```

#### 各种情况的颜色渐变实现

http://www.w3cplus.com/content/css3-gradient

#### 让任意的标签可点击

```html
<div onclick="location.href='https://haofly.net'" style="cursor:pointer"></div>
```

