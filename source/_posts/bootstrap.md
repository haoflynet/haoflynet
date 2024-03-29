---
title: "BootStrap wiki"
date: 2015-02-20 08:30:39
updated: 2021-06-02 21:39:00
categories: frontend
---
bootstrap是由Twitter退出的一个用于前端开发的开发工具包，其中包含了许多简洁大方的css样式和实用的js插件，当然，它是移动设备优先的响应式开发方式。

## breakpoints断点定义

- [bootstrap的响应式breakpoints定义](https://getbootstrap.com/docs/5.0/layout/breakpoints/)
- 首先是移动设备有限，所以默认情况的样式是针对移动设备的，往上主要就是两个断点： md(>=768px iPad)、lg(>=992px正常的Web尺寸)

##  栅格系统

```html
<div class="row">
  <div class="col-md-1"></div>
  <div class="col-md-1"></div>
</div>
```

## Utilities

- 从`4.x`才开始的

- 有几种常见样式并不存在于`utilities`里面，如`font-size/line-height/height` ，建议直接写在html的style里

### Border

- 需要注意的是border不支持breakpoints

  ```shell
  border
  border-top
  border-right
  border-bottom
  border-left
  border-bottom-0
  
  # border-radius
  rounded
  rounded-top
  rounded-right
  rounded-bottom
  rounded-left
  rounded-circle	# 圆形
  rounded-0	# 没有圆角
  
  # border-color
  border-primary
  border-secondary
  border-success
  border-danger
  border-warning
  border-info
  border-light
  border-dark
  border-white
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

| 屏幕尺寸     | 类                           |
| ------------ | ---------------------------- |
| 只在lg隐藏   | d-lg-none d-xl-block         |
| 在lg和xl隐藏 | d-lg-none d-xl-none          |
| 只在xl隐藏   | d-xl-none                    |
| 只在lg显示   | d-none d-lg-block d-xl-none  |
| 在lg和xl显示 | d-none d-lg-block d-xl-block |
| 只在xl显示   | d-none d-xl-block            |

### Flex

```shell
d-flex	# flex布局

# 排列方向
flex-row
flex-row-reverse
flex-column
flex-column-reverse
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

# 内容布局
justify-content-start
justify-content-end
justify-content-center
justify-content-between
justify-content-around
```

### Sizing

- 不支持breakpoint

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
overflow-visible
overflow-scroll
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