---
title: "CSS教程"
date: 2015-01-11 08:12:39
updated: 2021-02-01 11:30:00
categories: frontend
---
## 浏览器兼容

- 首行的`<!DOCTYPE html>`很关键

- 谷歌浏览器或者新的浏览器支持在十六进制颜色后面加两位数来表示透明度，但是其他浏览器不支持，会直接不显示颜色

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

## 特殊函数

##### Calc

- 非常棒的函数，能够借助css直接对属性进行计算，例如`width: cacl(50% - 4px)`，表示宽度为父组件宽度的一半减4px，需要注意的时候中间计算符号的两边必须有空格，否则会被浏览器认为是一个错误的属性而被忽略
- 可以用于控制字体的缩放，例如`font-size: calc(1.5rem + 3vw)`，这样字体能跟随页面一同缩放
- 可以通过它实现简单的固定顶部和底部，而中间刚好撑满浏览器的布局:
  ![](https://haofly.net/uploads/css_01.jpg)

## 各种属性

##### a链接

a:link：表示一个正常的未被点击过的a标签的属性

a:visited: 表示一个已经被点击过的a标签的属性

a:hover: 鼠标移动到a标签上面

a:active: a标签被点击的时候

##### background

- 可以同时设置背景图像的color、image、repeat、attachment、position属性，如`.style1{background:beige url(mypic.png) no-repeat top center}`

##### background-color

- 设置透明
- transparent: 直接设置
- rgba(255, 255, 255, 0.5): 前三个是颜色，最后一个是透明度

##### background-image

- 设置背景图片，如`background-iamge: url(mypic.png)`
- 需要注意的是背景图片并不会撑起元素的高度，如果想要这种效果，可以参考[图片做背景撑开div](https://blog.csdn.net/u013205165/article/details/99000978)或者[css背景图撑开盒子高度](https://blog.csdn.net/qq_34812257/article/details/84867616)还有[响应式背景图片]([http://www.topcss.org/tag/%E5%93%8D%E5%BA%94%E5%BC%8F%E8%83%8C%E6%99%AF%E5%9B%BE%E7%89%87/](http://www.topcss.org/tag/响应式背景图片/))

##### background-repeat

- 设置是否及如何重复背景图像
- repeat(默认值，背景图像在摧之方向和水平方向重复)、repeate-x(水平方向重复)、repeat-y(垂直方向重复)、no-repeat(不重复)、inherit(继承父元素)

##### background-size

- 设置背景图片的大小
- 可选值：auto(以背景图片的比例缩放背景图片)、cover(缩放背景图片以完全覆盖背景区，可能背景图片部分看不见，宽高比例不变)、contain(缩放背景图片以完全转入背景区，可能背景区部分空白，宽高比例不变)、直接指定宽度(如50%、3em、12px、auto等)、指定宽度和高度(如50% auto、100% 100%等)

##### border边框

- border-color: 设置4个边框的颜色
- border-radius: 设置边框圆角大小
- border-style: 设置4个边框的样式。可能的值有none(无边框)、hidden(对于表，用于解决边框冲突，和none一样)、dotted(点状边框)、dashed(虚线)、solid(实线)、double(双线)、groove(3D凹槽边框)、ridge(3D垄状边框)、inset(3D inset边框)、outset(3D outset边框)、inherit(从父元素继承)
- border-width: 边框宽度
- 可以将三个属性一起定义:`border: width style color`，例如`border-right: 10px solid black`

##### box-shadow

- 给框添加阴影
- `box-shadow: h-shadow v-shadow blur spread color inset;`，例如`box-shadow: 10px 10px 5px #888888;`

##### cursor

- 设置鼠标悬停效果
- default(默认光标，一个箭头)、auto(默认值，浏览器自己设置)、crosshair(十字光标)、pointer(一只手、拖拽光标)、move(可被移动的光标)、e-resize/ne-resize/nw-resize/n-resize/se-resize/sw-resize/s-resize/w-resize(光标指示矩形框的边缘可往哪个方向移动，常用于往8个方向改变窗口大小)、text(文本)、wait(在忙，一只表或沙漏)、help(帮助，问号或气球)、no-drop/not-allowed(禁止，红色的圈加一个斜杠)
- `cursor:pointer`在`input type="file"`的情况下可能会不生效，可以给`input`标签添加`font-size: 0`，这样就能实现鼠标移到input元素上变成手形了

##### display

- 规定元素应该生成的显示框的类型
- none(不显示)、block(块级元素，前后会带有换行符)、inline(默认，内联元素，前后没有换行符)、inline-block(行内块元素)、list-item(会作为列表显示)、inherit(继承父元素display属性)
- 值为`flex`表示弹性布局

##### font-weight

- 设置字体粗细

- 如果值为`bold`，表示直接加粗，相当于值为`700`

- 如果想要字体超过900，可以尝试这些方法

  - 更换字体

  - 尝试给字加阴影，加少一点也有一定的加粗字体的效果

    ```css
    text-shadow: 0px 1px, 1px 0px, 1px 0px;
    
    // 或者几个属性配合
    text-shadow: 1px 0;
    letter-spacing:1px;
    font-weight:bold;
    letter-spacing: 0.5px;
    ```

##### input

- text-align: 内容显示方式，`center`表示居中显示
- 如果direction属性是ltr，则默认值是left；如果direction是rtl，则为right

##### justify-content

- 用于设置弹性盒子元素在主轴(横轴)方向上的对齐方式，`align-content`用于设置垂直轴
- flex-start: 默认值，项目位于容器的开头
- flex-end: 项目位于容器的结尾
- center: 项目位于容器的中心
- Space-between: 项目位于各行之间留有空白的容器内
- space-around: 项目位于各行之前、之间、之后都留有空白的容器内
- initial: 设置该属性为它的默认值
- Inherit: 从父元素继承该属性

##### line-height

- 设置行间距

##### list-style

- 把图像设置为列表中的列表项目标记(就是每一行的头那个地方设置为圆点显示还是数字显示)
- 包括三个属性: `list-style-type list-style-position list-style-image`，默认值为`disc outside none`
- `list-style-type`就是左边的样式，可选值有none(无标记)、disc(实心圆，默认)、circle(空心圆)、square(实心方块)、decimal(数字)、decimal-leading-zero(0开头的数字)等

##### margin

```css
margin: 10px 5px 15px 20px;	/*上 右 下 左*/
```

##### outline

- 如果想要`Button`等点击后不出现蓝色的边框，可以把该属性设置为`none`

##### overflow

- 当水平或垂直方向溢出时添加滚动条

- `visible`: 内容不会被截断，且可以显示在内容盒之外

- `hidden`: 内容会被截断，且不会显示滚动条

- `scroll`: 总是显示滚动条，无论内容是否发生溢出

- `auto`: 取决于浏览器本身

- **既要有滚动效果，又要隐藏滚动条**，可以使用这种方法:

  ```css
  .hide-scrollbar{
    -ms-overflow-style: none;
    overflow: -moz-scrollbars-none;
  
    &::-webkit-scrollbar {
      width: 0 !important
    }
  }
  ```

##### overflow-x

- 当水平方向溢出时添加滚动条

##### overflow-y

- 当垂直方向溢出时添加滚动条
- scroll: 可以用这个属性给单独的两列创建单独的滚动条

##### pointer-events

- 指定在什么情况下某个特定的图形元素可以成为鼠标事件的target

- `none`: 可以实现某个元素仅仅能看，但是无法触发其事件。屏蔽掉某个元素上的所有的事件
- 这个属性的其他值都只适用于`SVG`

##### position

- absolute: 绝对定位，相对于static定位以外的第一个父元素进行定位
- fixed: 绝对定位，相对于浏览器窗口进行定位
- relative: 相对定位，相对于其正常位置进行定位
- static: 默认值。没有定位ie，元素出现在正常的流中
- inherit: 从父元素继承position属性
- 如果**父元素设置了margin auto且overflow-x:none，子元素如果想单独撑开(而不是所有子元素撑开)父元素且横屏占满，可以采取修改position的值为fixed然后width：200%，然后left一点到左边去即可**

##### table

- overflow:scroll：如果表格超宽，让页面自动出现滚动条
- word-wrap:break-word，超过宽度自动换行
- word-break: break-all，超过宽度，无论是不是一个单词都换行

##### scroll-behavior

- smooth: 使滚动变为平滑滚动，如果想要自己通过手动控制滚动，如`scrollTo`等，一定要加该参数，这样才能使滚动看起来平顺一点
- auto: 滚动框立即滚动

##### text

- text-indent: 段落缩进设置

##### text-overflow

- 设置当文本溢出包含元素时怎么做
- clip(直接截断文本)、ellipsis(截断文本并显示省略号)

##### top

- 如果`top`属性不起作用，可以尝试修改当前元素或者父元素或兄弟元素的`position`值试试

##### white-space

- nowrap: 强制不换行

##### user-select

- none(文本不能被选择)、text(可以选择文本)

##### vertical-align

- 设置元素的垂直对齐方式，定义行内元素的基线相对于该元素所在行的基线的垂直对齐
- 参考值：baseline(默认，元素放置在父元素的基线上)、sub(垂直对齐文本的下标)、super(垂直对齐文本的上标)、top(把元素的顶端与行中最高元素的顶端对齐)、text-top(把元素的顶端与父元素字体的顶端对齐)、middle(把此元素放置在父元素的中部)、bottom(把元素的顶端与行中最低的元素的顶端对齐)、text-bottom(把元素的底端与父元素字体的底端对齐)、%(使用line-height属性的百分比值来排列此元素，允许为负)、inherit(继承父元素的值)

##### -webkit-text-fill-color

- 检索或设置对象中的文字填充颜色。如果同时设置了text-fill-color和color，text-fill-color定义的颜色将覆盖color属性；通常-webkit-text-fill-color与-webkit-text-stroke一起使用，能实现一些例如渐变文字和镂空文字的效果。

- 可以使用该参数来解决safari和firefoxinput框在disabled时[颜色不一样的问题](https://stackoverflow.com/questions/262158/disabled-input-text-color):

  ```css
  -webkit-text-fill-color: #880000;
  opacity: 1; /* required on iOS */
  ```

##### white-space

- nowrap: 强制不换行

##### width元素宽度 

- max-width设置最大宽度，默认为none

##### word-wrap

- break-word: 强制换行(a标签太长强制换行)

##### @media

- 媒体查询，可以定义当满足某个条件时的css，例如

  ```css
  @media (max-width: 600px) {	// 当屏幕最大宽度小于600px的时候
    .tag {
      display: none;
    }
  }
  
  @media (min-width: 700px) and (orientation: landscape) {}	// 仅在横屏并且宽度大于700px的时候
  @media tv and (min-width: 700px) and (orientation: landscape){}// 仅在电视上
  ```

## CSS选择器

##### .class1.class2

- 表示既包含class1又包含class2的元素

##### .class1 .class2

- 表示class1下的class2的元素

##### element > element

- 例如`div > p`表示选择所有父节点为`div` 的`p`元素

##### element + element

- 例如`div + p`表示选择所有前面是`div`标签的`p`标签

##### element ～ element

- 例如`p ~ ul`表示选择所有`p`标签后的`ul`标签

##### [attribute]

- 例如`a[target]`表示选择所有含有`target`属性的`a`标签

##### [attribute=value]

- 例如`a[target=_blank]`表示选择所有`target`属性为`_blank`的`a`标签

##### [attribute~=value]

- 例如`[title~=flower]`表示选择所有`title`属性里面包含`flower`的标签

##### [attribute|=value]

- 例如`[lang|=en]`表示选择所有`lang`属性以`en`开头的标签

##### [attribute^=value]

- 例如`a[href^="https"]`表示选择所有`href`属性以`https`开头的`a`标签

##### [attribute$=value]

- 例如`a[href$=".pdf"]`表示所有`href`属性以`.pdf`结尾的`a`标签

##### [attribute*=value]

- 例如`a[href*="test"]`表示所有`href`包含`test`的`a`标签

##### :active

- 例如`a:active`表示`a`标签被激活

##### ::after

- 例如`p::after`表示在`p`标签后插入一些内容

```css
// 这样每一个p标签后面都会跟上这个内容了
p::after { 
  content: " - Remember this";
}
```

##### ::before

- 例如`p::before`表示在`p`标签前插入一些内容，和`::after`用法类似
- `::before/::after`可组合实现一些[绚丽的效果](https://juejin.im/post/6854573204011221000#heading-13): 伪类光圈、伪类括号效果、丝带效果、几何图形(三角形、五角星)、水滴、流动边框、Tooltip提示、伪类盒子阴影、Tabs当前激活状态、伪元素模糊背景、蓝湖文字、主要标题、鼠标浮层、遮罩浮层、伪类美化文字、照片堆叠效果

##### :checked

- 例如`input:checked`表示选择所有`checked`了的`input`

##### :default

- 例如`input:default`表示选择所有默认状态下的`input`

##### :disabled

- 例如`input:disabled`表示选择所有禁用了的`input`

##### :empty

- 例如`p:empty`表示选择没有子元素的`p`标签

##### :enabled

- 例如`input:enabled`表示选择所有可用的`input`标签

##### :first-child

- 第一个子元素

##### ::first-lettter

- 第一个字母

##### ::first-line

- 第一行

##### :first-of-type

- 例如`p:first-of-type`表示全局所有的`p`标签里面的第一个

##### :focus

- 表示获得焦点的时候

##### :hover

- 鼠标浮动的时候

##### :in-range

- 当值在某个范围内的时候

```css
<style>
input:in-range {
  border: 2px solid yellow;
}
</style>
// 下面的7在input的范围内，当值为7的时候就应用上面的样式
<input type="number" min="5" max="10" value="7">
```

##### :indeterminate

- 元素为不确定状态时

##### :invalid

- 当输入为不合法的时候`input:invalid`

##### :lang(language)

- `p:lang(it)`表示选择所有`lang`属性为`it`的`p`标签

##### :last-child

- 最后一个子元素
- **慎用这几个相关的伪类选择器，因为不总是能达到预期的效果**，可以参考[选择某类的最后一个元素——CSS3伪类选择器走过的坑](https://juejin.im/post/6844904072206614535)

##### :last-of-type

- 全局最后一个指定元素

##### :link

- `a:link`表示所有为访问的`a`标签

##### :not(selector)

- `:not(p)`表示所有不是`p`标签的标签

##### nth-child(n)

- 前n个子元素

##### nth-last-child(n)

- 表示倒数n个子元素
- 参数除了数字，还可以填入`odd`和`even`表示奇偶

```css
// 表示该div标签下的最后2个元素的属性
div:nth-last-child(2) {
  background: red;
}
```

##### :nth-last-of-type(n)

- 最后n个元素

##### :nth-of0type(n)

- 前n个元素

##### :only-of-type

- `p:only-of-type`选择所有的`p`标签为父元素的`p`标签

##### :only-child

- `p:only-child`选择`p`标签为唯一子元素的父元素

- 例如

  ```css
  p:only-child
  {
  background:#ff0000;
  }
  
  <div> <!--这里选择到的是div元素-->
  	<p>这是一个段落。</p>
  </div>
  
  <div> <!--不唯一，不选择该元素-->
  <p>这是一个 span。</p>
  <p>这是一个段落。</p>
  </div>
  ```

##### :optional

- `input:optional`表示输入框为非必选的时候

##### out-of-range

- 和`in-range`相反

##### ::placeholder

- `input::placeholder`

##### :read-only

- `input:read-only`表示只读的`input`标签

##### :read-write

- `input:read-write`表示可读写的`input`标签

##### :required

- `input:required`表示必填的`input`标签

##### :root

- 选择文档的跟元素

##### ::selection

- 用户当前选择的元素

##### :target

- 

##### :valid

- 合法的输入框

##### :visited

- 访问过的连接

## Flex布局

- 注意flex是无法给容器设置`height`的，但是可以通过设置内部元素的`height/max-height/min-height`来间接控制其高度

- 如果`flex`的宽度较长，明明有剩余空间却自动换行了可能需要这样设置(flex布局的内容超出了盒子的宽度):

  ```css
  .content {
      flex: 1;
      width: 0;
  }
  // 或者
  .content {
      flex: 1;
      overflow: hidden；
  }
  ```

参考
[Flex 布局教程：语法篇](https://www.ruanyifeng.com/blog/2015/07/flex-grammar.html) 

[Flex 布局教程：实例篇](http://www.ruanyifeng.com/blog/2015/07/flex-examples.html): 这里面可以看到居中对齐、右对齐、左对齐、上部居中对齐、下部居中对齐、右下对齐等，以及网格布局、圣杯布局(传统网页的布局方式)、输入框的布局、悬挂式布局、固定的底栏、流式布局

#### flex容器的属性

| 属性名          | 含义                                                         | 可选值                                                       | 默认值     |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------- |
| flex-direction  | 决定主轴的方向（即项目的排列方向）                           | row \| row-reverse \| column \| column-reverse               | row        |
| flex-wrap       | 定义换行方式                                                 | nowrap \| wrap(第一行在上方) \| wrap-reverse(第一行在下方)   | nowrap     |
| flex-flow       | flex-direction和flex-wrap属性的简写形式                      |                                                              | row nowrap |
| justify-content | 定义了项目在主轴上的对齐方式                                 | flex-start(左对齐) \| flex-end(右对齐) \| center(居中) \| space-between(两端对齐，项目之间的间隔都相等) \| space-around(每个项目两侧的间隔相等) |            |
| align-items     | 定义项目在交叉轴上如何对齐                                   | flex-start(交叉轴的起点对齐，上对齐) \| flex-end(交叉轴的终点对齐，下对齐) \| center(交叉轴的中点对齐，居中对齐) \| baseline(项目的第一行文字的基线对齐) \| stretch(如果项目未设置高度或设为auto，将占满整个容器的高度) | stretch    |
| align-content   | 定义了多根轴线的对齐方式.如果项目只有一根轴线，该属性不起作用 | flex-start(与交叉轴的起点对齐) \| flex-end(与交叉轴的终点对齐) \| center(与交叉轴的中点对齐) \| space-between(与交叉轴两端对齐，轴线之间的间隔平均分布) \| space-around(每根轴线两侧的间隔都相等) \| stretch(轴线占满整个交叉轴) | stretch    |

#### flex容器下项目的属性

| 属性名      | 含义                                                         | 可选值                                                       | 默认值                                                       |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| order       | 定义项目的排列顺序，数值越小，排列越靠前，默认为0            |                                                              | 0                                                            |
| flex-grow   | 项目的放大比例                                               | 如果所有项目的`flex-grow`属性都为1，则它们将等分剩余空间（如果有的话）。如果一个项目的`flex-grow`属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍。这个就类似于element里面的xs了 | 0(如果存在剩余空间也不放大)                                  |
| flex-shrink | 项目的缩小比例                                               | 如果所有项目的`flex-shrink`属性都为1，当空间不足时，都将等比例缩小。如果一个项目的`flex-shrink`属性为0，其他项目都为1，则空间不足时，前者不缩小。 | 1(即如果空间不足，该项目将缩小)                              |
| flex-basis  | 在分配多余空间之前，项目占据的主轴空间.浏览器根据这个属性，计算主轴是否有多余空间 | 可以设为跟`width`或`height`属性一样的值（比如350px），则项目将占据固定空间 | Auto                                                         |
| flex        | 是`flex-grow`, `flex-shrink` 和 `flex-basis`的简写           |                                                              | 0 1 auto                                                     |
| align-self  | 允许单个项目有与其他项目不一样的对齐方式，可覆盖`align-items`属性 | auto \| flex-start \| flex-end \| center \| baseline \| stretch | auto(继承父元素的`align-items`属性，如果没有父元素，则等同于`stretch`) |

## Grid布局

- 参考底部推荐文章

## 动画transitions

- `transitions`允许我们平滑地改变属性值(而不是立马变更到某个值)

  ```css
  // 最简单的例子，当鼠标移动到div上面的时候div的宽度由100px平滑变更为300px，总共耗时2秒
  div {
    width: 100px;
    transition: width 2s;
  }
  div:hover {
    width: 300px;
  }
  ```

- transition-property表示绑定的属性名称，transition-duration表示属性变更的时间，transition-timing-function表示属性变更方式，transition-delay表示变更延迟，可以简写为

  ```css
  div {
    transition: width 2s linear 1s;
  }
  ```

- transition-timing-function变更方式默认为linear表示匀速(cubiz-bezier(0,0,1,1))，ease表示中间快两头慢(cubiz-bezier(0.25,0.1,0.25,1))，ease-in表示先慢后快(0.42, 0, 1, 1)，ease-out表示先快后慢(0, 0, 0.58, 1)，ease-in-out表示中间慢两头快(0.42, 0, 0.58, 1)，cubiz-bezier(n, n, n, n)自定义快慢

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
# 方法五，css3里面超级简单
.div {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: traslate(-50%, -50%);
}
# 方法六：让容器内部的元素垂直居中
.parent {
  display: flex; 
  align-items: center;
}
# 方法六：让标签中的文字剧中
div {
  text-align: center;
}
# 方法七：绝对定位元素的居中对齐
<div style="position: absolute; left: 50%;">
<div style="position: relative; left: -50%;>
content
</div>
</div>
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

#### 底部居中对齐

```css
.class {
  position:absolute;
  bottom: 30px;
  margin: auto;
  left: 0;
  right: 0;
} 
```

#### 在Chrome显示小于12px的字体

- 需要注意的是这个方法只是单纯地缩小了显示的字，并不是将字体变小了，换行那个地方可能有问题

```css
.item {
	-webkit-transform: scale(.5);
  -moz-transform: scale(.5);
  transform: scale(.5);
}
```

#### 让两个Div或其它元素始终并排显示

- UI中可能会有将两个元素合并成一个元素，并且无论响应式如何改变，两个元素始终按原来的样式在一起
- 可以先调整两个元素的样式，让他们挨在一起，然后新建一个父类将他们包裹

```css
.parent {
  min-width: 150px; // 父组件设置最小宽度，这样即使是响应式也不会影响父组件内部的元素了。剩下的就是让外部无论如何也不能让parent元素的宽度变小了
}
.leftElement {
  position: relative;
  display: inline-block;
  width: 100px;
}
.rightElement {
  position: relative;
  display: inline-block;
  left: -4px;	// 微调右边的元素
  top: 1px;
  border: 1px solid #e1e4e6;
  border-left: none;
  width: 50px;
}
```

#### 子元素位于父元素底部

```css
.parent{
  position: relative;
  height: 300px;
  width: 300px;
  margin:0 auto;
}
.child{
  position: absolute;
  bottom: 0;
  height: 80px;
}
```

#### 多行文字截断/仅显示3行/实现see more/read more功能

```css
// 方法一：文本设置固定高度，超过某个高度就隐藏
div {
  line-height: 20px;
  overflow: hidden;
  max-height: 60px; // 3行文本的高度
  
  .read-more {	// 当点击read more后最大高度就变大
    max-height: 9999px;
    transition: max-height 0.2s ease;
  }
}

// 方法二：使用-webkit-line-clamps，但是可能存在浏览器兼容问题，例如Firefox和IE浏览器不支持该属性，移动端浏览器一般都基于webkit内核，兼容性还行
div {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

// 方法三：通过伪元素绝对定位到行尾并遮住文字
p {
    position: relative;
    line-height: 20px;
    height: 40px;
    overflow: hidden;
}
p::after {
    content:"...";
    font-weight:bold;
    position:absolute;
    bottom:0;
    right:0;
    padding:0 20px 1px 45px;
    
    background: -webkit-gradient(linear, left top, right top, from(rgba(255, 255, 255, 0)), to(white), color-stop(50%, white));
    background: -moz-linear-gradient(to right, rgba(255, 255, 255, 0), white 50%, white);
    background: -o-linear-gradient(to right, rgba(255, 255, 255, 0), white 50%, white);
    background: -ms-linear-gradient(to right, rgba(255, 255, 255, 0), white 50%, white);
    background: linear-gradient(to right, rgba(255, 255, 255, 0), white 50%, white);
}
```

#### 两个并排inline-block的元素一样的高度却不在同一水平线上，但又不是多余的属性导致的上下空白

- 这是一个比较奇怪的问题，甚至有时候在不同的浏览器里面会有不同的表现
- 这涉及到基准线的对齐方式，可以将两个元素都设置`vertical-align: top;`解决，具体的可以参考上文`vertical-align`属性的设置

#### 火狐浏览器input的placeholder不再同一水平线上

尝试设置如下伪类，[来源](https://stackoverflow.com/questions/36421637/input-placeholder-not-vertically-aligned-in-firefox)

```css
::-webkit-input-placeholder {
   color: brand-blue;
}

:-moz-placeholder { /* Firefox 18- */
   color: brand-blue;  
   line-height 60px;
}

::-moz-placeholder {  /* Firefox 19+ */
   color: brand-blue;  
   line-height 60px;
}

:-ms-input-placeholder {  
   color: brand-blue;
}
```

#### 设置密码输入框的显示于隐藏

- 通过修改`type`属性

```javascript
const password = document.querySelector('#password');

$('input#password').on('click', function(e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // 通过修改右边小眼睛的类来切换眼睛的展示
    this.classList.toggle('fa-eye-slash');
})
```

#### 实现图片的等比例自动缩放

```css
img{
	width: auto;
	height: auto;
	max-width: 100%;
	max-height: 100%;	
}
```

**扩展阅读**

[Flex 布局教程](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)

[CSS Viewport 视口单位](https://juejin.im/post/5efd21f2f265da2307399020#heading-19): 一种新的单位`vw/vh/vmin/vmax`，这篇文章中有很多应用案例，例如: 响应式字体大小、全屏、粘性布局、响应式元素、垂直和水平间距、模态框、页面头部、纵横比、顶部边框、移动端滚动等

[最强大的 CSS 布局 —— Grid 布局](https://juejin.im/post/6854573220306255880)