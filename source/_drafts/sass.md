http://www.ruanyifeng.com/blog/2012/06/sass.html

弥补css的不足

给css加入编程元素，css与处理器



### 基础语法

#### 变量

```scss
$blue: #1875e7;
div {
  color: $blue;
}
```

#### 表达式

```scss
body {
  margin: (14px/2);
  top: 50px + 100px;
  right: $var * 10%;
}
```

#### 嵌套

```scss
// 选择器嵌套
div {
  hi {
    color:red;
  }
  &:hover {	// 嵌套中使用&引用父元素
    color: blue;
  }
}

// 属性嵌套
p {
  border: {	// 这里有冒号
    color: red;
  }
}
```

#### 控制语句

```scss
// if else 语句
@if lightness($color) > 30% {
  background-color: #000;
} @else {
  background-color: #fff;
}

// for 循环
@for $i from 1 to 10 {
  .border-#{$i} {
    border: #{$i}px solid blue;
  }
}
@each $member in a, b, c, d {
  .#{$member} {
    background-image: url("/image/#{$member}.jpg");
  }
}

// while循环
$i: 6;
@while $i > 0 {
  .item-#{$i} { width: 2em * $i; }
  $i: $i - 2;
}
```

#### 继承extend与重用mixin

```scss
// extend继承
.class2 {
  @extend .class1;
  font-size:120%;
}

// 使用mixin定义一个可重用的代码块
@mixin left {
  float: left;
  margin-left: 10px;
}
@mixin left($value: 10px) {	// 可以指定参数和缺省值
　　　　float: left;
　　　　margin-right: $value;
　　}
div {
  @include left;	// 在需要的地方进行引入
  @include left(20px);
}
```

#### 文件模块

```scss
@import "path/filename.scss"; // 引入文件
@import "foo.css";
```

