---
title: "CSS教程"
date: 2015-01-11 08:12:39
updated: 2017-08-07 18:50:00
categories: frontend
---
# CSS

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

##### p

- text-indent: 段落缩进设置

## TroubleShooting
#### 元素居中方法
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

