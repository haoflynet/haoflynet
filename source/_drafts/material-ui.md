---
title: "Material UI 手册"
date: 2019-09-05 14:40:00
categories: Javascript
---

- 样式使用css-in-js风格，得单独学一套
- [官方中文文档](https://material-ui.com/zh/)

## 组件

### Navigation 导航栏

### Bottom Navigation 底部导航栏

#### Link链接

```react
<Link component="button" color="inherit" underline="always">
  This is a button
</Link>
```

### Data Display 数据展示

#### Typography 文字

```react
<Typography variant="h4" color="inherit" align="center" paragraph>
  Content
</Typography>
```

## 样式

- css-in-js

## System 系统(utilities)

- 一些非常实用的内敛样式

- 不过这玩意儿不是每个元素上都可以直接加的，只有自带的`Box`组件可以直接加，所以一般是直接在外面包围一层`Box`，当然如果想要修改子元素的样式，可以用clone方法

  ```jsx
  // 这样在实际生成的DOM元素中就不会有一个多的Box层了，而是直接将样式附加到了子元素上
  <Box color="text.primary" clone>
    <Button />
  </Box>
  ```

- 所有的属性列表(不能实现的常用样式有background-image)

```jsx
<Box 
  // Borders边框
  border={1}
  
  // Color/Palette 颜色
  bgcolor="primary.main"
  bgcolor="secondary.main"
  bgcolor="text.primary"	// 黑色
  
  // Display 位置
  position={'fixed'}
  bottom={0}
  
  // Flexbox
  display="flex"
  flexDirection="row"
  flexWrap="nowrap"
  justifyContent="center"
  justifyContent="space-between"
  
  // Sizing 大小
  width={1/4}
  width={300}
  width="75%"
  width={1}	// 100%
  
  // Spacing 间距
  p={2}
  pt={3}
  px={1}
  py={4}
  
  minWidth="10"
  maxWidth="80"
></Box>
```





