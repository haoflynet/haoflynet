## 安装配置

```shell
npx create-next-app --typescript -e with-tailwindcss my-project	# 集成进nextjs
```

## 语法

### Customization

### Layout

- 常用于页面最外层布局

```javascript
class="container mx-auto py-5"
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
```

### Spacing

```shell
p-0	# padding: 0px
p-px # padding: 1px
p-0.5 # padding: 0.125rem
p-1 # padding: 0.25rem，1/2/3/4/5/6/7/8/9/10/11/12/14/16/20/24/28/32/36/40/44/48/52/56/60/64/72/80/96
```

### Sizing

```shell
# width
w-0	# 0px
w-px # 1px
w-1 # 0.25rem
w-3	# 0.75rem

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
```

### Interactivity

```shell
cursor-default
cursor-pointer
cursor-wait
cursor-text
cursor-move
cursor-help
cursor-not-allowed
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
