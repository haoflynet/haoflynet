---
title: "uniapp 开发手册"
date: 2020-02-05 21:02:30
updated: 2020-03-10 11:41:00
categories: uniapp
---

## 项目结构

- 如果是引入的`scss`样式，必须去`components`引入的目录里面去更改其源码或者在`app.vue`文件中定义好样式名进行更改

### 环境判断

可以通过`process.env.NODE_ENV`来判断当前环境是开发环境还是生产环境
  - 在IDE中点击“运行”默认编译出来的是开发环境，点击“发行”默认编译出来的是生产环境
  - 在`package.json`文件中增加节点，可以是心啊自定义条件编译平台

### 页面生命周期

- `onLoad`: 监听页面加载，其参数为上个页面传递的数据
- `onShow`: 监听页面显示。页面每次出现在屏幕上都触发，包括从下级页面点返回露出当前页面
- `onReady`: 监听页面初次渲染完成。注意如果渲染速度快，会在页面进入动画完成前触发
- `onHide`: 监听页面隐藏
- `onUnload`: 监听页面卸载
- `onResize`: 监听窗口尺寸变化
- `onPullDownRefresh`:  监听用户下拉动作，一般用于下拉刷新
- `onReachBottom`:  页面滚动到底部的事件（不是scroll-view滚到底），常用于下拉下一页数据。
- `onTabItemTap`:  点击 tab 时触发
- `onShareAppMessage`: 用户点击右上角分享
- `onPageScroll`: 监听页面滚动，参数为Object
- `onNavigationBarButtonTap`: 监听原生标题栏按钮点击事件，参数为Object
- `onBackPress`: 监听页面返回，返回 event = {from:backbutton、 navigateBack} ，backbutton 表示来源是左上角返回按钮或 android 返回键；navigateBack表示来源是 uni.navigateBack
- `onNavigationBarSearchInputChanged`: 监听原生标题栏搜索输入框输入内容变化事件
- `onNavigationBarSearchInputConfirmed`: 监听原生标题栏搜索输入框搜索事件，用户点击软键盘上的“搜索”按钮时触发。
- `onNavigationBarSearchInputClicked`: 监听原生标题栏搜索输入框点击事件

## 数据绑定

- 与`vue`有相同点也有很多不同点，使用时需要注意

### class/style的属性绑定

```vue
<view v-bind:style="{ color: activeColor, fontSize: fontSize + 'px' }">666</view>
<view v-for="(menu, index) in menus" :class="[index == currentIndex ? 'menuActive' : '']">
```

## API

- `uni-app`对部分API进行了Promise封装，返回数据的第一个参数是错误对象，第二个参数是结果。
  - 异步的方法，如果不传入success、fail、complete等callback参数，将以Promise返回数据

### 数据缓存

```javascript
// 异步设置
uni.setStorage({
    key: 'storage_key',
    data: 'hello',
    success: function () {
        console.log('success');
    }
});

// 同步设置
try {
    uni.setStorageSync('storage_key', 'hello');
} catch (e) {
    // error
}
```

### 请求

`uni.request`

```javascript
// 默认的异步方式
uni.request({
    url: 'https://www.example.com/request',
    success: (res) => {
        console.log(res.data);
    }
});

// Promise方式
uni.request({
        url: 'https://www.example.com/request'
    })
    .then(data => {//data为一个数组，数组第一项为错误信息，第二项为返回数据
        var [error, res]  = data;
        console.log(res.data);
    })

// Await同步方式，page的method方法里是可以将方法定义为async的
function async request () {
    var [error, res] = await uni.request({
        url: 'https://www.example.com/request'
    });
    console.log(res.data);
}
```

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

##### 扩展阅读

- [uni-app 全局变量的几种实现方式](https://ask.dcloud.net.cn/article/35021)