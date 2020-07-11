---
title: "Element"
date: 2019-01-05 10:00:00
updated: 2020-07-05 16:40:00
categories: java
---

## 布局

| xs   | `<768px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| ---- | -------------------------------------- | ------------------------------------------- | ---- | ---- |
| sm   | `≥768px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| md   | `≥992px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| lg   | `≥1200px` 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| xl   | `≥1920px` 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) |      |      |



如果要自定义非全局的css属性，可以直接在当前页面添加`<style>`标签像普通的html文件那样添加即可

我们可以通过引入单独的 `display.css`：

```
import 'element-ui/lib/theme-chalk/display.css';
复制代码
```

它包含的类名及其含义如下：

- `hidden-xs-only` - 当视口在 xs 尺寸时隐藏
- `hidden-sm-only` - 当视口在 sm 尺寸时隐藏
- `hidden-sm-and-down` - 当视口在 sm 及以下尺寸时隐藏
- `hidden-sm-and-up` - 当视口在 sm 及以上尺寸时隐藏
- `hidden-md-only` - 当视口在 md 尺寸时隐藏
- `hidden-md-and-down` - 当视口在 md 及以下尺寸时隐藏
- `hidden-md-and-up` - 当视口在 md 及以上尺寸时隐藏
- `hidden-lg-only` - 当视口在 lg 尺寸时隐藏
- `hidden-lg-and-down` - 当视口在 lg 及以下尺寸时隐藏
- `hidden-lg-and-up` - 当视口在 lg 及以上尺寸时隐藏
- `hidden-xl-only` - 当视口在 xl 尺寸时隐藏



##### TroubleShooting

- **slider组件在小屏幕上离开焦点后tooltip却不消失**:  这应该是一个已知的[bug](https://github.com/ElemeFE/element/issues/19008)，可以这个`issue`下的解决方案:

  ```javascript
  <el-slider @change="change" ref="timeSlider"> </el-slider>
  
  change(val){
    if (this.$refs["timeSlider"].$refs["button1"]) {
        this.$refs["timeSlider"].$refs["button1"].handleMouseLeave(); 	 
    }
    if (this.$refs["timeSlider"].$refs["button2"]) {
      this.$refs["timeSlider"].$refs["button2"].handleMouseLeave(); 
    }
  }
  ```
  
- **验证函数没有执行**: 检查验证方法里面是否保证调用了`callback`方法的

- **去掉table的第三种状态(升序ascending、降序descending，这里要去掉的是默认无排序的状态null)**： 需要这样设置，不过这样设置后，小箭头上依然会保留`null`的状态，这时候可以用`pointer-event:none`这个css属性将小箭头的事件屏蔽掉即可:

  ```vue
  <el-table :sort-orders="['ascending', 'descending']"></el-table>
  ```

  