---
title: "Element"
date: 2019-01-05 10:00:00
updated: 2020-06-10 16:40:00
categories: java
---

如果要自定义非全局的css属性，可以直接在当前页面添加`<style>`标签像普通的html文件那样添加即可



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