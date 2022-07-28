## Charts

### VictoryArea

- 每个横坐标都对应两个纵坐标形成一个area，也可以不提供y0，默认就从y最小值开始

```jsx
<VictoryArea
	domain={{x: [minX, maxX], y: [minY, maxY]}}	// 可手动设置x和y轴的边界值
  data={[
    { x: 1, y: 2, y0: 0 },
    { x: 2, y: 3, y0: 1 },
    { x: 3, y: 5, y0: 1 },
    { x: 4, y: 4, y0: 2 },
    { x: 5, y: 6, y0: 2 }
  ]}
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

### VictoryAxis

- 坐标轴(有些图表自带了的，如果像自定义可以直接用这个)

```jsx
<VictoryAxis
	tickLabelComponent={<></>}	// 这样可以只显示坐标不显示坐标上的值
	offsetY={160}	// 纵向坐标偏移量
/>
<VictoryAxis
	dependentAxis	// 好像这个就是纵轴
  offsetX={400}	// 横向坐标便宜量
/>
```

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

### VictoryLine

- 折线图

```jsx
<VictoryLine
	style={{data: {stroke: '#2C74F6'}}}	// 设置线的颜色
	labels={['']}
	standalone={false}
	data={data1}
	interpolation={'natural'}
/>
```

## Containers

### VictoryChart

#### 隐藏坐标轴

```jsx
<VictoryChart>
  <VictoryAxis
    style={{
           axis: {
           display: 'none',
          },
    }}
  />
  <VictoryAxis
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

## 其他组件

### VictoryLabel