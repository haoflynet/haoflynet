---
title: "Material UI 手册"
date: 2019-09-05 14:40:00
categories: Javascript
---

- 样式使用css-in-js风格，得单独学一套
- [官方中文文档](https://material-ui.com/zh/)

## 组件

- 动态调用组件的方式

  ```react
  const components = {
    a: AComponent,
    b: BComponent
  }
  
  const MyComponent = components['a']
  return <MyComponent />	// 调用的时候必须大写
  ```

### Layout 布局

#### Box 分组

- 非常实用的一个组件，类似于bootstrap中的utilities，可以非常方便地通过props来设置样式

- 这就是`material-ui`中的`System 系统`，不过system系统包含一些非常实用的内联样式，不过这玩意儿不是每个元素上都可以直接加的，只有自带的`Box`组件可以直接加，所以一般是直接在外面包围一层`Box`，当然如果想要修改子元素的样式，可以用clone方法

  ```react
  // 这样在实际生成的DOM元素中就不会有一个多的Box层了，而是直接将样式附加到了子元素上
  <Box color="text.primary" clone>
    <Button />
  </Box>
  ```

- 支持的所有的属性(其中不包含的常用的属性包括background-image/background-position)

  ```react
  <Box 
    // Borders边框
    border={1}
    borderRadius={"50%"}	// border-radius
    borderColor="primary.main" // secondary.main, error.main, grey.500, text.primary
    
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

#### Container 容器

- 简单的页面主要内容的wapper，自带居中、padding-x和maxWidth等实用的属性

#### Grid 栅格

- 响应式布局

```jsx
<Grid 
  container	// 加了container就是flex布局
  alignItems={"center"}
></Grid>
```



### Navigation 导航栏

### Bottom Navigation 底部导航栏

#### Link链接

```react
<Link component="button" color="inherit" underline="always">
  This is a button
</Link>
```

### Data Display 数据展示

#### Icons 图标

- 我们可以用`SvgIcon`来封装自己的图标，如果有自己的图标并且数量多且用的地方多，最好用这个来封装每一个svg，就能让他们统一起来

- 还有种借助webpack的svgr进行封装的方式可以让svg仍然以svg的形式存在，但是没有试过，先就不写了

- 封装只需要这样做即可:

  ```react
  function HomeIcon(props) {
    return (
      <SvgIcon {...props} 
        aria-label="home"	<!--语意话-->
        viewBox="0 0 36.997 35.901"<!--通常我们从设计得到的svg不是统一24的尺寸，通常有自己的尺寸，需要将该viewBox写到这里，否则可能会缺少一部分-->
      >	
        <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />	<!--这一块是svg的内容(svg tag的内容部分)-->
      </SvgIcon>
    );
  }
  ```

- 实用起来就方便得多了

  - 注意如果svg的color修改不成功，可能是因为svg中某些样式直接写在了path的`fill`属性中，可以直接在`path`元素上面加上`fill={props.color || "white"}`

  ```react
  <HomeIcon
  	fontSize={"large"}	// fontSize=2.1875rem/35px，还可选small
    style={{ fontSize: 40 }}
    
    color="paimary"	// paimary, secondary, action, disabled
    style={{ color: green[500] }}
    
  />
  ```

#### Tooltip 提示

- 遇到一个很奇怪的问题，所有的tooltip都只固定在页面的左上角，而不是元素的上方，结果发现是有程序员给所有div添加了`width: 100%;height:100%`的属性，我去

```react
<Tooltip
  leaveDelay={200000}	// 显示时长，调试的时候可以把这个增大
  placement={"top"}
  title={	// 自定义弹出框内容
    <React.Fragment>
      <Typography color="inherit">Tooltip with HTML</Typography>
      <em>{"And here's"}</em> <b>{'some'}</b> <u>{'amazing content'}</u>.{' '}
      {"It's very engaging. Right?"}
    </React.Fragment>
  }
  >
  <Button>
    <Avatar src={avatar} />
  </Button>
</Tooltip>
```

#### Typography 文字

```react
<Typography 
  component="h4" // 使用component能让他直接变成h4元素
  color="inherit" align="center" paragraph>
  Content
</Typography>
```

## 样式

- css-in-js

```react
const useStyles = makeStyles({
  root: {
    color: 'red',
    '& p': {
      color: 'green',
      '& span': {
        color: 'blue'
      }
    }
  },
});
```



