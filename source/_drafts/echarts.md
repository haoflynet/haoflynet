- echarts的`react-native`的wrapper基本上都是基于webview的，集成比较顺手的只有[react-native-echarts-wrapper](https://github.com/tomLadder/react-native-echarts-wrapper)，如果只是展示的话问题不大，但是如果要响应touch event等，可能会有很多的问题的，所以要谨慎

## 配置

## 常用需求

### 隐藏坐标轴/坐标线/坐标刻度/网格线

```javascript
{
  xAxis: {
    show: false,	// 隐藏坐标轴(线和刻度同时隐藏)
    axisLine: {	// 只隐藏坐标线
      show: false
    },
    axisTick: {	// 只隐藏坐标刻度
      show: false
    },
    splitLine: {	// 隐藏网格线
      show: false
    }
  }
}
```

### 多条线段显示不同的颜色

```javascript
visualMap: [{
  show: false,
  dimension: 0, 
  seriesIndex: 0,	// 针对那一个数据集
  pieces: [{
    lte: 6,
    color: 'red'
  }, {
    gte: 6,
    color: 'black'
  }]
}]
```

