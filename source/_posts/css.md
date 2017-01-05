---
title: "CSS教程"
date: 2015-01-11 08:12:39
categories: frontend
---
# CSS
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




判断屏幕宽度
@media (min-width: 400px) {

}

