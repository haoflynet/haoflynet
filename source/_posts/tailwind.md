---
title: "Tailwind 开发手册"
date: 2021-11-16 00:00:00
updated: 2021-11-16 18:00:00
categories: nodejs
---
- 基本上是我现在开发新旧项目的必备工具了

## 安装配置

## 基础

### 配置文件tailwind.config.js

- 如果项目之前已经有大量的存在的css，为了防止冲突可以使用`prefix`去防止覆盖，对于负数的属性，`prefix`仍然需要写在最前面，例如`tw--mt-10`

```javascript
module.exports = {
  important: false,	// 是否在所有生成的样式加上!important，不推荐这么做
  prefix: 'tw-',	// 添加一个前缀，
  purge: [	// 指定需要从哪些文件中查找我们需要使用的class(这样可以只编译出我们有使用的class)
    '../views/site/*.php'
  ],
  darkMode: false, // or 'media' or 'class'，默认选项
  theme: {
    fontFamily: {	// 直接替换默认字体
      'sans': 'Roboto, sans-serif',
      'serif': 'Roboto, sans-serif',
      'mono': 'Roboto, sans-serif',
      'display': 'Roboto, sans-serif',
      'body': 'Roboto, sans-serif'
    },
    extend: {	// 可以添加一些自定义的样式，或者覆盖之前的样式，在官方文档每一个样式页面下面多有个性化的说明
      backgroundImage: {
        'my-bg': "url('/')"	// 甚至可以这样定义一个背景图片类
        main: 'linear-gradient(225deg, #BD7AE3 0%, #8461C9 100%)'
      },
      boxShadow: {
      	'md-all': '4px 4px 6px -1px rgba(0, 0, 0, 0.1), -2px 2px 4px -1px rgba(0, 0, 0, 0.06)'	// 四周阴影
      }
      height: {
      	'full-vw': '100vw'
    	},
    	minWidth: {
        '36': '9rem'
      },
      spacing: {
        80: '20rem',
        '38': '9.5rem',
        '120': '30rem',
        '128': '32rem',
        '144': '36rem',
        '160': '40rem',
        172: 44rem,
        '192': '48rem',
        '232': '58rem',
        240: '60rem',
        272: '68rem',
        280: '70rem',
        288: '72rem',
        '320': '80rem',
      },
			width: {
        232: '58rem'
      },
    	zIndex: {
        '-10': '-10',
      }
    },
  },
  variants: {
    extend: {
      borderRadius: ['hover']	// 给rounded添加hover效果
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false,	// 添加这个配置可以让tailwind不覆盖默认的基础元素的样式，例如html、body、h1等https://tailwindcss.com/docs/preflight
  }
}
```

<!--more-->

### 响应式

```shell
# 断点
sm	# @media (min-width: 640px) { ... }, mobile
md	# @media (min-width: 768px) { ... }, iPad, iPad Mini
lg	# @media (min-width: 1024px) { ... }, 小屏Web, iPad Pro, Next Hub
xl	# @media (min-width: 1280px) { ... }, 正常Web, Macbook
2xl # @media (min-width: 1536px) { ... }, 大屏Web

# 使用时只需加前缀即可，例如
md:w-full
```

### JIT(Just-in-Time模式)

- 2.1开始才有，虽然是下一代的标准，但仍然是一个`Preview feature`
- 就非常方便了，以前可能需要写`extend`的样式，现在直接开搞

### 样式!important

给样式添加!important有几种方法:

- 在配置里面添加`important: true`，会在所有生成的样式前加上`!important`

- 在配置里面添加`important: '#app'`，会给所有`#app`前缀的样式下添加`!importnat`
- 使用JIT(Just-In-Time)，目前还只是测试版

## 语法

### Customization

### Layout

- 常用于页面最外层布局

```shell
# container
class="container mx-auto py-5"

# display
block
inline-block
inline
flex
inline-flex
table
grid
hidden
table-cell

# Overflow
overflow-hidden	# 可选auto、hidden、visible、scroll
overflow-x-scroll	# 可设置水平和垂直方向

# Position
static
fixed
absolute
relative
sticky

# Top / Right /Bottom /Left
top-0
-top-0	# 负数
left-1/2	# 可选1/2、1/3、2/3、1/4、2/4、3/4，没有12分的

# Z-Index
z-0	# z-10 20 30 40 50 auto
```

### Flexbox & Grid

```shell
# flex
flex-1 # flex: 1 1 0%;
flex-auto # flex: 1 1 auto;
flex-initial	# flex: 0 1 auto;
flex-none	# flex: none

# flex-direction
flex-row / flex-row-reverse / flex-col / flex-col-reverse

# flex wrap
flex-wrap	/ flex-wrap-reverse	/ flex-nowrap

# flex grow
flex-grow-0	# flex-grow: 0
flex-grow	# flex-grow: 1

# flex shrink
flex-shrink-0	# flex-shrink: 0
flex-shrink	# flex-shrink: 1

# justify content
justify-center	# justify-content: center，可选start、end、center、between、around、evenly

# align items
items-center	# align-items: center，可选start、end、center、baseline、stretch

# grid template columns
grid-cols-3	# 定义有多少列，可选1、2、3、4、5、6、7、8、9、10、11、12、none

# grid auto flow
grid-flow-row	# grid-auto-flow，可选row、column、row dense、column dense

# gap
gap-0	# 可选0、0.5、1、1.5、2、2.5、3、3.5、4、5、6、7、8、9、10、11、12、14、16等，并且可以按上下左右来区分
```

### Spacing

```shell
p-0	# padding: 0px
p-px # padding: 1px
p-0.5 # padding: 0.125rem
p-1 # padding: 0.25rem，1/2/3/4/5/6(1.5rem)/7/8/9/10/11/12(3rem=30px)/14(3.5rem)/16(4rem)/20(5rem)/24/28/32(8rem)/36/40(10rem)/44/48/52/56/60/64/72/80(20rem)/96(24rem)
```

### Sizing

```shell
# width
w-0	# 0px
w-px # 1px
w-1 # 0.25rem，可选、1、1.5、2、2.5、3、3.5、4、5、6、7、8(2rem)、9(2.25rem)、10(2.5rem)、1112、14、16、20、24、28、32、36、40、44、48、52、56、60、64、72、80、96(24rem)
w-full # 100%
w-screen # 100vw
w-min	# min-content
w-max	# max-content

# min width
min-w-full	# 可选min-w-0、min-w-full、min-w-min、min-w-max，但是没有上面width那么多数字，如果要用到需要自己来定义，注意extend minWidth而不是width

# height
h-1/2	# height: 50%
h-3/4	# height: 75%
h-5/12	# height: 41.666%
```

### Text/Typography/Font

```shell
# font size
text-2xl # 可选xs(0.75rem=12px)、sm(0.875rem=14px)、base(1rem=16px)、lg(1.125rem=18px)、xl(1.25rem=20px)、2xl(1.5rem=24px)、3xl、4xl(2.25rem=36px)、5xl(3rem=48px)、6xl、7xl、8xl、9xl

# font weight
font-thin # font-weight，可选thin(100)、extralight(200)、light(300)、normal(400)、medium(500)、semibold(600)、bold(700)、extrabold(800)、black(900)

# line height
leading-3	# line-height: .75rem, 可选3(0.75rem=12px)/4/5、6(1.5rem=24px)、7、8(2rem=32px)、9/10

# text color
text-white
text-black
text-current
text-transparent

# text align
text-center # text-align: center

# text decoration
underline	# text-decoration: underline，可选underline(下横线)、line-through(删除线)、no-underline

# text overflow
truncate	# overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
overflow-ellipsis
overflow-clip

# vertical align
align-middle	# vertical-align: middle

# word break
break-normal	# overflow-wrap: normal; word-break: normal
break-words # overflow-wrap: break-word
break-all	# word-break: break-all
```

### Backgrounds

```shell
# background color
bg-white	# 可选gray、red、yellow、green、blue、indigo、purple紫色、pink
bg-gray-50
bg-blue-100

# background position
bg-bottom # 可选bottom、center、left、left-bottom、left-top、right、right-bottom、right-top、top

# background repeat
bg-repeat
bg-no-repeat
bg-repeat-x
bg-repeat-y
bg-repeat-round
bg-repeat-space

# background size
bg-auto	# 可选auto、cover、contain
```

### Borders

```shell
# border radius，默认不支持hover，可以自定义
rounded-none	# border-radius: 0px
rounded-sm	# border-radius: 0.125rem
rounded-lg	# border-radius: 0.5rem
rounded-2xl	# border-radius: 1.5rem
rounded-3xl
rounded-full	# border-radius: 9999px，圆形

# border width
border	# border-width: 1px
border-0	# 可选0、2、4、8
border-t-0	# 可指定方向

# border color
border-transparent
border-current
border-black
border-white
border-gray-50	# 所有颜色都可

# border style
border-solid	# border-style: solid, 可选solid、dashed、dotted、double、none

# ring是tailwind预先定义的一种border类型，就是一圈
# ring width
ring
ring-0	# 可选0、1、2、4、8、inset

# ring color
ring-transparent
ring-current
ring-black
ring-white
ring-gray-50	# 可选所有颜色
```

### Effects

```shell
# box shadow
shadow
shadow-sm	# 可选sm、md、lg、xl、2xl、inner、none

# opacity 透明度
opacity-0	# 可选0、5、10、20、25、30、40、50、60、70、75、80、90、95、100
```

### [Transitions & animation](https://tailwindcss.com/docs/transition-property)

- `transition-{properities}`可以实现指定属性的动画过渡效果效果
- 例如按钮hover放大]

```shell
transition-top

# transition duration
duration-75	# 可选75、100、150、200、300、500、700、1000，单位为毫秒
```

### Interactivity

```shell
# Appearance
appearance-none		# 隐藏input或者select的选择按钮等，但是我用起来没效果，还是得自己写css，参考https://haofly.net/css

# cursor
cursor-pointer	# 可选default、pointer、wait、text、move、help、not-allowed

# user select
select-none	# user-select:none，可选none、text、all、auto
```

## 扩展

- [tailwindo](https://github.com/awssat/tailwindo): Laravel的blade模板转tailwind的工具，不大好用，但也将就了
- [wickedblocks](https://wickedblocks.dev/): 免费的tailwindcss组件模板
