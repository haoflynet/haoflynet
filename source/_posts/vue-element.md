---
title: "Vue-Element 手册"
date: 2020-08-09 16:00:00
updated: 2020-08-23 16:56:00
categories: javascript
---

## 布局

### 栅格布局

- `el-row`和`el-col`可以搭配实现24格的栅格布局

- `el-row`支持如下属性

| 参数    | 含义                           | 说明   | 可选值                                      | 默认值 |
| ------- | ------------------------------ | ------ | ------------------------------------------- | ------ |
| gutter  | 每两个栅格之间的间隔(单位是px) | number | -                                           | 0      |
| type    | 布局模式                       | string | -                                           | -      |
| justify | flex布局下的水平排列方式       | string | start/end/center/space-around/space-between | start  |
| align   | flex布局下的垂直排列方式       | string | top/middle/bottom                           | top    |
| tag     | 自定义元素标签                 | string | *                                           | div    |

  - `el-col`支持如下属性

| 参数 | 含义 | 说明 | 可选值 | 默认值 |
| ---- | -------------------------------------- | ------------------------------------------- | ---- | ---- |
| span | 栅格占据的列数 | number | - | 24 |
| offset | 栅格左侧的间隔格数 | number | - | 0 |
| push | 栅格向右移动格数 | number | - | 0 |
| pull | 栅格向左移动格数 | number | - | 0 |
| xs   | `<768px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| sm   | `≥768px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| md   | `≥992px` 响应式栅格数或者栅格属性对象  | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| lg   | `≥1200px` 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | —    | —    |
| xl   | `≥1920px` 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | - | - |
| tag | 自定义元素标签 | string | * | Div |

栅格布局一般会根据实际的各个分辨率下的情况来设置每个布局的宽度，如果想要直接换行，也可以某一种分辨率之和超过24，这样只要两个`col`超过24就会换行，例如:

```vuejs
<el-row :gutter="24">
  <el-col :xs="20" :sm="6" :md="4" :lg="3" :xl="1"><div></div></el-col>
  <el-col :xs="20" :sm="6" :md="8" :lg="9" :xl="11"><div></div></el-col>
  <el-col :xs="20" :sm="6" :md="8" :lg="9" :xl="11"><div</div></el-col>
  <el-col :xs="20" :sm="6" :md="4" :lg="3" :xl="1"><div</div></el-col>
</el-row>
```

<!--more-->

### 基于断点的隐藏类

- 如果想要实现在某些显示条件下将元素隐藏可以简单地使用以下的样式
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

```css
<div hidden-xs-only></div>	<!--设置改组件在xs尺寸时隐藏-->
```

## 组件

### form表单

- 表单自定义`label`/自定义空`label`，在使用表单时发现空label不能直接留空，可以在表单内部使用`slot`自定义空`label`或者在空`label`中添加空格:

  ```javascript
  <label slot="label">&nbsp;</label>
  ```

-  一个`el-form-item`下包含多个字段的表单验证或者子组件中包含多个字段，可以在给子组件传递一个可以用于验证的`prop`，但是并不真正验证它，而是在编写自定义`validator`来进行多个字段的自定义验证，传递`prop`只是为了触发验证

  ```javascript
  <el-form-item :prop="`${formModelProp}`" :rules="{validator:customValidator}"></el-form-item>
  ```
  
- 如果想要一个`form-item`的验证错误提示覆盖一排的多个字段而不是超长后换行，可以在`style`里面直接修改错误提示的`css`属性让它不换行即可

- **表单验证相关方法**: 

  - **需要格外注意的是el-form-item的prop值不是简单的formData的字段名，对于数组型的字段，它可能需要定义为`field2[0].name`这样的形式，下标不能错**

  - validate: 对整个表单的所有字段进行验证，回调函数有两个参数，分表表示校验是否成功和未通过校验的字段，例如

    ```javascript
    this.$refs.myFormRef.validate(function (valid, errorObj) {
      console.log(valid)	// 是否成功
      console.log(errorObj) // 错误的字段的信息
    })
    
    // 其中errorObj是一个包含错误名和字段的对象，例如:
    {
      'field1': {
        'field': 'field1',
        'message': 'field 1 is empty'
      },
      'field2[0].name': {
        'field': 'field2[0].name',
        'message': 'field2[0].name is empty'
      }
    }
    ```

  - validateField: 对部分表单字段进行校验`Function(prop: string, callback: Function(errorMessage: string))`

  - resetFields: 对整个表单进行充值，将所有字段值重置为初始值并移除校验结果，常用于用于点击表单的取消按钮

  - clearValidate：移除表单的校验结果，传入的是待移除的表单项的prop属性组成的数组，如果不传则移除整个表单的校验结果。可以用它来在提交的时候取消部分表单的校验，比如有些对象如果所有字段都为空那么就不判断该表单，可以这样做:

    ```javascript
    this.$refs.myFormRef.validate(function (valid, errorObj) {
      if (!valid) {
        Object.keys(errorObj).forEach (field => {
          const splits = field.split('[')
          const fieldName = splits[0]
          const index = parseInt(splits[1])
          if (!AllowdFieldNameArray.includes(fieldName)) {
            return true
          }
          const obj = isNaN(index) ? formData[fieldName] : formData[fieldName][index]
          if (Object.values(obj).some((item) => item)) {	// 如果该对象每个字段都不为空则表示没问题
            console.log('it\'s ok', field)
          } else {
            formRef.clearValidate(Object.keys(errorObj).filter((item) => item.split('.')[0] === field))
          }
        })
      }  
    })
    ```

### dialog对话框

- `el-dialog`多重嵌套的时候，最好在子`dialog`上添加`append-to-body`属性，这样才能保证弹窗正常显示且遮罩层表现正常

## TroubleShooting

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

  