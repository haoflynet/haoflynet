

## API

### 位置

 `uni.getLocation(OBJECT)`: 获取位置

- 如果要把获取到的结果给`map`用，那么`type`需要设置为`gcj02`，需要注意的是如果使用浏览器来获取地址，那么可能获取不到准确的地址(例如可能获取到美国的地址)，这时候可以换浏览器试试，实在不行就别用浏览器，直接上其他平台模拟吧。

```javascript
uni.getLocation({
    type: 'wgs84',
    success: function (res) {
        console.log('当前位置的经度：' + res.longitude);
        console.log('当前位置的纬度：' + res.latitude);
    }
});
```







app.cue 配置全局事件监听以及全局样式

main.js 入口文件

manifest.json app 各个平台项目的配置中心 

pages.json 页面配置，condition参数用于开发时候的特殊配置比如指定打开我想要的页面



使用upx作为尺寸单位，相对基准单位。动态的时候还是用px



在unload里面Uni.showloading

发送请求uni.request

跳转页面uni.navigateTo()



<data-news_id>



方法参数就是methods里面的e.currentTarget





