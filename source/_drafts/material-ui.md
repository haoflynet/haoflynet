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

- 所有的属性列表(不能实现的常用样式有background-image/background-position)

```jsx
<Box 
  // Borders边框
  border={1}
  borderRadius={"50%"}	// border-radius
  
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
  alignContent="flex-start"
  alignContent="flex-end"
  
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
  
  // Typography 文字，对于Typography如果改不了内部的样式，那么直接把标签去掉，直接<Bod>文字</Box>
  textAlign="left"	// text-align，可选left、center、right
  fontWeight="fontWeightLight" // font-weight，可选fontWeightLight、fontWeightRegular、fontWeightMedium、fontWeightBold或者直接数字{500}
  fontSize="fontSize"	// font-size，可选fontSize，其他元素的size：h6.fontSize，或者直接数字{16}
  fontStyle="normal" // font-style，可选normal、italic、poblique
  fontFamily="fontFamily" // font-family
  letterSpacing={6} // letter-space
  lineHeight={10}	// line-height
  
  minWidth="10"
  maxWidth="80"
></Box>
```





