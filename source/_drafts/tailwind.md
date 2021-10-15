## 安装配置

## 基础

### 配置文件tailwind.config.js

```javascript
module.exports = {
  prefix: 'tw-',	// 添加一个前缀，如果项目之前已经有大量的存在的css，为了防止冲突可以使用这个方式去防止覆盖
  purge: [	// 指定需要从哪些文件中查找我们需要使用的class(这样可以只编译出我们有使用的class)
    '../views/site/*.php'
  ],
  darkMode: false, // or 'media' or 'class'，默认选项
  theme: {
    extend: {	// 可以添加一些自定义的样式，或者覆盖之前的样式，在官方文档每一个样式页面下面多有个性化的说明
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
        '120': '30rem',
        '192': '48rem',
        '232': '58rem',
        '240': '60rem',
        '320': '80rem',
      },

    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: false,	// 添加这个配置可以让tailwind不覆盖默认的基础元素的样式，例如html、body、h1等https://tailwindcss.com/docs/preflight
  }
}
```

### 响应式

```shell
# 断点
sm	# @media (min-width: 640px) { ... }, mobile
md	# @media (min-width: 768px) { ... }, iPad
lg	# @media (min-width: 1024px) { ... }, 小屏Web, iPad Pro
xl	# @media (min-width: 1280px) { ... }, 正常Web, Macbook
2xl # @media (min-width: 1536px) { ... }, 大屏Web

# 使用时只需加前缀即可，例如
md:w-full
```

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
flex-row
flex-row-reverse
flex-col
flex-col-reverse

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
```

### Spacing

```shell
p-0	# padding: 0px
p-px # padding: 1px
p-0.5 # padding: 0.125rem
p-1 # padding: 0.25rem，1/2/3/4/5/6/7/8/9/10/11/12/14/16/20(5rem)/24/28/32/36/40(10rem)/44/48/52/56/60/64/72/80(20rem)/96(24rem	)
```

### Sizing

```shell
# width
w-0	# 0px
w-px # 1px
w-1 # 0.25rem，可选、1、1.5、2、2.5、3、3.5、4到12、14、16、20、24、28、32、36、40、44、48、52、56、60、64、72、80
96
w-full # 100%
w-screen # 100vw

# min width
min-w-full	# 可选min-w-0、min-w-full、min-w-min、min-w-max，但是没有上面width那么多数字，如果要用到需要自己来定义

# height
h-1/2	# height: 50%
h-3/4	# height: 75%
h-5/12	# height: 41.666%
```

### Text/Typography

```shell
# font size
text-xs
text-sm
text-base
text-lg
text-xl
text-2xl # 一直到text-9xl

# line height
leading-3	# line-height: .75rem, leading-3/4/5/6/7/8/9/10

# text color
text-white
text-black
text-current
text-transparent

# text align
text-center # text-align: center

# vertical align
align-middle	# vertical-align: middle
```

### Backgrounds

```shell
# background color
bg-white
bg-gray-50
bg-blue-100

# background position
bg-bottom
bg-center
bg-left
bg-left-bottom
bg-left-top
bg-right
bg-right-bottom
bg-right-top
bg-top

# background repeat
bg-repeat
bg-no-repeat
bg-repeat-x
bg-repeat-y
bg-repeat-round
bg-repeat-space
```

### Borders

```shell
# border radius
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

### Transitions & animation

- `transition-{properities}`可以实现指定属性的动画过渡效果效果

```shell
transition-top

# transition duration
duration-75	# 可选75、100、150、200、300、500、700、1000，单位为毫秒
```

### Interactivity

```shell
# cursor
cursor-pointer	# 可选default、pointer、wait、text、move、help、not-allowed

# user select
select-none	# user-select:none，可选none、text、all、auto
```





laravel转tailwind的工具https://github.com/awssat/tailwindo，不大好用



Important: true最好设置上



添加自定义的类

```css
@layer utilities {
  .filter-grayscale {
    filter: grayscale(100%);
  }
  
  @variants dark {
    .filter-none {
      filter: none;
    }
		.filter-grayscale(100%);
  }
}

可以这样使用
<div class="filter-grayscale dark:filter-none"></div>
```



免费的tailwindcss组件模版：https://wickedblocks.dev/z
