---
title: "Material UI / MUI手册"
date: 2021-08-10 08:40:00
updated: 2021-10-21 08:48:00
categories: Javascript
---

- 样式使用css-in-js风格，得单独学一套
- [官方中文文档](https://material-ui.com/zh/)
- 从5.x开始`material-ui`更名为`mui`了，网上搜到不要奇怪

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

### Inputs

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
  interactive // 交互式，当鼠标移动到弹出框上时不会因为leaveDelay时间到了而关闭，如果没有它，弹出框将不能被点击，鼠标的点击事件都是下层元素的
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

- fontWeight/fontSize这些都不能直接设置，只能外面套一层Box

```react
<Typography 
  component="h4" // 使用component能让他直接变成h4元素
  color="inherit" align="center" paragraph>
  Content
</Typography>
```

### Feedback

### Surfaces

#### [Accordion/Expand手风琴](https://mui.com/components/accordion/)

- 可以伸缩展开的手风琴效果

```javascript
const [expanded, setExpanded] = useState(false)

<Accordion
	defaultExpanded={false}	// 默认是否展开
  onChange={() => setExpanded(!expanded)}
  elevation={0}>	// evevation参数可以不显示子元素外层的border
  <AccordionSummary
    expandIcon={expanded ? <FaMinus /> : <FaPlus />}	// 可以通过事件来使用不同的icon
    aria-controls="panel1a-content"
    id="panel1a-header"
    >
    <Typography>Accordion 1</Typography>
  </AccordionSummary>
  <AccordionDetails>
    <Typography>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
      malesuada lacus ex, sit amet blandit leo lobortis eget.
    </Typography>
  </AccordionDetails>
</Accordion>
```

### Navigation 导航栏

#### Bottom Navigation 底部导航栏

#### Link链接

```react
<Link component="button" color="inherit" underline="always">
  This is a button
</Link>
```

### Layout 布局

#### Box 分组

- 非常实用的一个组件，类似于bootstrap中的utilities，可以非常方便地通过props来设置样式

- 这就是`material-ui`中的`System 系统`，不过system系统包含一些非常实用的内联样式，不过这玩意儿不是每个元素上都可以直接加的，只有自带的`Box`组件可以直接加，所以一般是直接在外面包围一层`Box`，当然如果想要修改子元素的样式，可以用clone方法

  ```react
  // 这样在实际生成的DOM元素中就不会有一个多的Box层了，而是直接将样式附加到了子元素上
  // 当clone不work的时候，可以尝试调换Box组件和被clone的组件的引入顺序
  <Box color="text.primary" clone>
    <Button />
  </Box>
  ```

- 支持的所有的属性(其中不包含的常用的属性包括background-image/background-position)

  ```react
  <Box 
    component="span"	// box默认是一个div元素，也可以通过这个属性置顶其为特定的元素
    
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

<!--more-->

#### Container 容器

- 简单的页面主要内容的wapper，自带居中、padding-x和maxWidth等实用的属性

#### Grid 栅格

- 响应式布局
- 默认情况flex元素的默认属性值为`min-width: auto`，当子元素设置`white-space: nowrap`的时候会超出元素，这时候可以给容器加上`zeroMinWidth` 属性，即`Grid item xs zeroMinWidth`

```jsx
<Grid 
  container	// 加了container就是flex布局
  alignItems={"center"}
  direction="row"
  justifyContent="center"
  spacing={1}	// item之间的间距=spacing * 8px
>
	<Grid item xs={12} sm={6}></Grid>
  <Grid item xs={12} sm={6}></Grid>
</Grid>

// 自适应布局，可以让子项平均地利用空间，可以显示设置一个子项的宽度，而使其他项的大小根据其宽度自动进行调整
<Grid container>
	<grid item xs></grid>
  <grid item xs={6}></grid>
  <grid item xs></grid>
</Grid>
<Grid container>
	<grid item></grid>
  <grid item xs={12} sm container>	// 子项也可以是container
  </grid>
</Grid>
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

## 服务端渲染SSR

- `material-ui`通常会与`next.js`配合作为服务端渲染工程

- 当使用`useMediaQuery`去判断屏幕宽度的时候，`mui`会将当前组件渲染两次。第一次什么也不渲染，第二次则会与子组件一起渲染。这个双向渲染有个缺点就是UI会有闪烁。当然，如果不进行服务器端渲染，可以将其`options`参数的`noSSR`设置为`true`

  ```javascript
  const isWeb = useMediaQuery(theme.breakpoints.up("sm"), {
    defaultMatches: true,	// 默认值为false，因为在服务器端无法获取服务器宽度，默认会渲染一个空的组件，但是设置为true后当获取不到宽度的时候就会仍然会返回true，默认会返回一个渲染了的页面
  })
  ```

- 除了上面会render两次以外，我发现`next.js`的配置中只要有`rewrites`，就会又多渲染一次，无论访问的是不是`rewrites`里面的路由。可以参考`https://github.com/vercel/next.js/discussions/27985`

