---
title: "BootStrap wiki"
date: 2015-02-20 08:30:39
updated: 2021-07-01 21:39:00
categories: frontend
---
bootstrap是由Twitter退出的一个用于前端开发的开发工具包，其中包含了许多简洁大方的css样式和实用的js插件，当然，它是移动设备优先的响应式开发方式。

## breakpoints

- [bootstrap的响应式breakpoints定义](https://getbootstrap.com/docs/5.0/layout/breakpoints/)
- 一般我们会开发web版，所以在进行移动设备兼容时，需要将默认值修改为移动设备的(这就是为什么叫移动优先)，而为web来添加breakpoint
- 一般都以最小宽度为breakpoint，如果要用最大宽度，一般是少0.02，例如`>=576px`修改为最大宽度就是`<=757.98px`
- 我们开发主要就是兼容这几个: 移动设备(默认值不用加断点)、平板设备(md)，Web(lg)三个即可

| Breakpoint        | Class infix | Grid Breakpoint | Dimensions | Devices                                                 |
| ----------------- | ----------- | --------------- | ---------- | ------------------------------------------------------- |
| X-Small           | none        | xs: 0           | <576px     | iPhone X(375), iPhone 6/7/8 Plus(414), iPhone 5/SE(320) |
| Small             | sm          | sm: 576px       | >=576px    |                                                         |
| Medium            | md          | md: 768px       | >=768px    | iPad(768)                                               |
| Large             | lg          | lg: 992px       | >=992px    | iPad Pro(1024)                                          |
| Extra large       | xl          | xl: 1200px      | >=1200px   |                                                         |
| Extra extra large | xxl         | xxl: 1400px     | >=1440px   | Macbook Pro(1440)                                       |

- bootstrap自定义了一些scss的断点

|            | Bootstrap breakpoing                      | Scss Breakpoint                                      |
| ---------- | ----------------------------------------- | ---------------------------------------------------- |
| 最小值     | @include media-breakpoint-up(sm)          | @media (min-width: 576px)                            |
| 最小值     | @include media-breakpoint-up(md)          | @media (min-width: 768px)                            |
| 最小值     | @include media-breakpoint-up(lg)          | @media (min-width: 992px)                            |
| 最小值     | @include media-breakpoint-up(xl)          | @media (min-width: 1200px)                           |
| 最小值     | @include media-breakpoint-up(xxl)         | @media (min-width: 1400px)                           |
| 最大值     | @include media-breakpoint-down(sm)        | @media (max-width: 575.98px)                         |
| 最大值     | @include media-breakpoint-down(md)        | @media (max-width: 767.98px)                         |
| 最大值     | @include media-breakpoint-down(lg)        | @media (max-width: 991.98px)                         |
| 最大值     | @include media-breakpoint-down(xl)        | @media (max-width: 1199.98px)                        |
| 最大值     | @include media-breakpoint-down(xxl)       | @media (max-width: 1399.98px)                        |
| 两个段之间 | @include media-breakpoint-only(xs)        | @media (min-width: 768px) and (max-width: 991.98px)  |
|            | @include media-breakpoint-only(sm)        |                                                      |
|            | @include media-breakpoint-only(md)        |                                                      |
|            | @include media-breakpoint-only(lg)        |                                                      |
|            | @include media-breakpoint-only(xl)        |                                                      |
|            | @include media-breakpoint-only(xxl)       |                                                      |
| 多个段之间 | @include media-breakpoint-between(md, xl) | @media (min-width: 768px) and (max-width: 1199.98px) |
|            |                                           |                                                      |

## Utilities

- 有几种常见样式并不存在于`utilities`里面，如`font-size/line-height/height` ，建议直接写在html的style里

### Border

- 需要注意的是border不支持breakpoints

  ```shell
  border
  border-top
  border-right
  border-bottom
  border-left
  
  # border: none
  border-0
  border-top-0
  border-right-0
  border-bottom-0
  border-left-0
  
  # border-radius
  rounded
  rounded-top
  rounded-right
  rounded-bottom
  rounded-left
  rounded-circle	# 圆形
  rounded-0	# 没有圆角
  
  # border-color
  border border-primary
  border border-secondary
  border border-success
  border border-danger
  border border-warning
  border border-info
  border border-light
  border border-dark
  border border-white
  ```


### Color

- 设置字体颜色

  ```shell
  .text-primary
  .text-secondary	# 深灰色
  .text-success
  .text-danger # 红色
  .text-warning
  .text-info
  .text-light	# 浅灰色
  .text-dark	# 黑色
  .text-muted
  .text-white
  ```

- 设置背景颜色

  ```shell
  .bg-secondary	# 深灰色
  .bg-light	# 浅灰色
  .bg-dark	# 黑色
  ```

### Cursor

- 只要给元素加上`role="button"`即可增加`cursor: pointer`属性

### Display

- 以d开头
- 可取的值有none、inline、inline-block、block、table、table-cell、table-row、flex、inline-flex

| 屏幕尺寸   | 类                          |
| ---------- | --------------------------- |
| 只在lg隐藏 | d-lg-none d-xl-block        |
| 只在xl隐藏 | d-xl-none                   |
| 只在lg显示 | d-none d-lg-block d-xl-none |
| 只在xl显示 | d-none d-xl-block           |

### Flex

```
.flex-row
.flex-row-reverse
.flex-column
.flex-column-reverse
.flex-sm-row
.flex-sm-row-reverse
.flex-sm-column
.flex-sm-column-reverse
.flex-md-row
.flex-md-row-reverse
.flex-md-column
.flex-md-column-reverse
.flex-lg-row
.flex-lg-row-reverse
.flex-lg-column
.flex-lg-column-reverse
.flex-xl-row
.flex-xl-row-reverse
.flex-xl-column
.flex-xl-column-reverse
```

### Sizing

- 宽度

  ```shell
  w-25
  w-50
  w-75
  w-100	# width: 100%
  ```

- 高度

  ```shell
  h-25
  h-50
  h-75
  h-100	# height: 100%
  ```

### Overflow

```shell
overflow-auto
overflow-hidden
```

### Positoin

```javascript
position-static
position-relative
position-absolute
position-fixed
position-sticky
```

### Spacing

- m表示margin，p表示padding
- t、b、l、r分表表示top、bottom、left、right
- x表示水平方向left和right
- y表示垂直方向top和bottom
- 可以加上响应式参数{property}{sides}-{breakpoint}-{size}
- size的取值有0、1、2、3、4、5、auto

### Text

- align item

  ```shell
  align-item-center
  align-item-start
  align-item-end
  align-item-baseline
  align-item-stretch
  ```

- text alignment

  ```shell
  text-left
  text-center
  text-right
  
  # 添加breakpoint
  text-sm-left
  text-md-left
  ```

- font weight

  ```shell
  font-weight-bolder
  font-weight-bold	# 700
  font-weight-normal	# font-weight: 400
  font-weight-light
  font-italic	# 斜体
  ```

- wrap

  ```shell
  text-nowrap
  text-truncate # 截断，用省略号表示
  ```
  
- justify-content

  ```javascript
  justify-content-center
  justify-content-between
  ```

- vertical-align

  ```shell
  align-middle	# vertical-align: middle
  ```

##  特殊功能(使用Tips)

- **下拉选择列表(需要bootstrap.js)**：

  ```html
  <div class="form-group">
    <label for="sel1">Select list:</label>
    <select class="form-control" id="sel1">
      <option>1</option>
      <option>2</option>
      <option>3</option>
      <option>4</option>
    </select>
  </div>
  ```
  
- input的属性(居然没有哪个地方写了的，我也是醉了，难道只有我没有找到，还是只有我什么基础都没有还来用bootstrap):

  ```html
  <input placeholder="Enter email">   placeholder属性表示在输入框内预先显示的文字
  <input type="email">  type会影响到该输入框的展现形式，它的值可以是checkbox、email、file、password、text(文本输入框)
  <input class="form-control"> input只有加了这个类才会呈现得好看一点，并且默认宽度会变成100\%
  ```
  
- 表单里面点击按钮禁止跳转，不要讲button的type设置为subbmit或者不设置，必须将其设置为`type="button"`才不会强制刷新当前页面

- 使用jquery控制`carousel`跳转:

  ```javascript
  $('.carousel-control').click(function(e){
      e.stopPropagation();
      var goTo = $(this).data('slide');
      if(goTo=="prev") {
          $('#carousel-id').carousel('prev'); 
      } else {
          $('#carousel-id').carousel('next'); 
      }
  });
  ```

## 常用网址

**百度的CDN**： <http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap-theme.min.css> <http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css> [http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js ](http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js)**全局CSS样式**：[http://v3.bootcss.com/css/ ](http://v3.bootcss.com/css/)**组件**：[http://v3.bootcss.com/components/ ](http://v3.bootcss.com/components/)**JavaScript插件**：[http://v3.bootcss.com/javascript/ ](http://v3.bootcss.com/javascript/)**jQuery UI Bootstrap**：[http://www.bootcss.com/p/jquery-ui-bootstrap/ ](http://www.bootcss.com/p/jquery-ui-bootstrap/)**Glyphicons字体图标**：[http://v3.bootcss.com/components/#glyphicons ](http://v3.bootcss.com/components/#glyphicons)**实例精选(几个简单的模板)**：<http://v3.bootcss.com/getting-started/#examples>