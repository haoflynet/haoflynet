- 目前我用到的`react-native`平台对`native`支持最好的表格组件了

## Charts

### VictoryArea

- 每个横坐标都对应两个纵坐标形成一个area，也可以不提供y0，默认就从y最小值开始

```jsx
<VictoryArea
	domain={{x: [minX, maxX], y: [minY, maxY]}}	// 可手动设置x和y轴的边界值
  domain={{y: [minY, maxY]}}	// 也可以单独设置某个轴，和上面的一样，最小值和最大值必须不一样，否则会报一个prop type warning，就只能自己先设置默认值了
  data={[
    { x: 1, y: 2, y0: 0 },
    { x: 2, y: 3, y0: 1 },
    { x: 3, y: 5, y0: 1 },
    { x: 4, y: 4, y0: 2 },
    { x: 5, y: 6, y0: 2 }
  ]}
  dataComponent={<Area />}	// 指那一块区域而不是某个点
/>
```

#### Area颜色渐变

```jsx
import {Defs, LinearGradient, Stop} from 'react-native-svg';

<Defs>
  <LinearGradient
    id="charGradient"
    x1="0.5"
    y1="0"
    x2="0.5"
    y2="1">
    <Stop offset="0" stopColor={appTheme?.colors?.primary} />
    <Stop offset="1" stopColor="#f5fcff" />
  </LinearGradient>
</Defs>

<VictoryArea
	style={{
    data: {
      fill: 'url(#charGradient)',
      fillOpacity: 0.3,
      stroke: '#2C74F6',	// 坐标点线段的颜色
      strokeWidth: 2,	// 坐标点线段的粗细
    },
    parent: {paddingTop: 0},
  }}
/>
```

#### 解决VictoryArea最后一个点的label被截断无法显示完整的问题

- 参考[VictoryArea overflow labels be covered ](https://github.com/FormidableLabs/victory/issues/1725)

```jsx
<VictoryArea
  groupComponent={<G />}	// 只需加一个这个就行
/>
```

### VictoryAxis

- 坐标轴(有些图表自带了的，如果像自定义可以直接用这个)
- 如果要自定义一条看起来像横坐标或者纵坐标的线，可以直接用`VictoryLine`，`data`就是一个开始点一个结束点即可

```jsx
<VictoryAxis
	tickLabelComponent={<></>}	// 这样可以只显示坐标不显示坐标上的值
	offsetY={160}	// 纵向坐标偏移量，单位居然是px
/>
<VictoryAxis
	dependentAxis	// 好像这个就是纵轴
  offsetX={400}	// 横向坐标偏移量
/>
```

### VictoryBoxPlot股票K线图

### VictoryGroup

- 使用它包裹几个内部的charts可以实现隐藏横纵坐标

```jsx
<VictoryGruop
	style={{data: {}}}
  offset={20}	// 子charts之间的距离
  padding={{top: 0, bottom: 0, left: 0, right: 0}}	// padding不能在style里面设置，只能在这里设置
	style={{
		axis: {stroke: 'red'},	// 设置线的颜色，我在VictoryChart可以设置，但是在VictoryGroup下面设置不成功
	}}
>
</VictoryGroup>
```

### VictoryLine折线图/线段

```jsx
<VictoryLine
	style={{data: {
    stroke: '#2C74F6',
    strokeDasharray: '4,4', // 用虚线表示
  }}}	// 设置线的颜色
	labels={['']}
	standalone={false}
	data={data1}
	interpolation={'basis'}	// 默认是linear折线，basis平滑曲线，其他的其实都有差别，但说不上名字了，可以挨个试试：natural/basis/bundle/cardinal/catmullRom/monotoneY/monotoneX/step(电子信号那种)/stepAfter/stepBefore
  dataComponent={<Curve />}	// 指那一条线，而不是某个点
/>
```

### VictoryScatter散点图

- 如果想要展示或者高亮一个单独的点，可以直接用这个来就行了，它还支持丰富的点样式

```jsx
<VictoryScatter
    style={{ data: { fill: "#c43a31" } }}
    size={7}	// 指定点的大小
    labels={({ datum }) => datum.y}
    labelComponent={<VictoryLabel dy={8}/>}
    data={[{x: 1, y: 1, symbol: 'star', size: 5}]}	// 可以针对某个点单独设置其形状和大小，形状包括star星星，square正方形，diamond菱形，circle圆形，triangleUp三角形
/>
```

## Containers

### VictoryChart

```jsx
<VictoryChart
  height={300}	// 高度的默认值就是300
/>
```

#### 隐藏坐标轴

```jsx
<VictoryChart>
  <VictoryAxis
    tickLabelComponent={<></>}	// 如果不加这个，那轴上的坐标也是会显示的
    style={{
           axis: {
           display: 'none',
          },
    }}
  />
  <VictoryAxis
    tickLabelComponent={<></>}
    dependentAxis
    style={{
           axis: {
           display: 'none',
          },
    }}
  />  
</VictoryChart>
```

### VictoryCursorContainer

- 当鼠标或者触摸的时候能够展示一个十字的光标

```jsx
containerComponent={
  <VictoryCursorContainer
  	cursorDimension={'x'}	// 仅展示横轴或者竖轴
  	cursorLabel={(point) => point.x}	// 展示label，不填表示不显示
    cursorLabelComponent={<VictoryLabel
                          	x={300}	// 可以指定label显示在哪个横坐标的位置，可以实现固定在右边
                          />}	// 自定义cusrorLabel组件
  	cursorComponent={
  		<LineSegment	// 可以自定义光标的样式
  			style={{
  				stroke: '#BDBDBD',
  				strokeWidth: '2px',
  				strokeDasharray: '2,4',
				}}
			/>
		}
		events={{
      onTouchMove: (evt: any, targetProps: any): any => {},
    	onTouchEnd: (evt: any, targetProps: any): any => {},
      onTouchStart: (evt: any, targetProps: any): any => {},
		}}
	/>
}
```

## 公共属性

 ### dataComponent

- 是指坐标点的组件

## 其他组件

### VictoryLabel

## TroubleShooting

- **[233, "RNSVGText",71...] is not usable as a native method argument**: 通常是由于表格中有变量没有赋初始值，得到了一个NaN造成的