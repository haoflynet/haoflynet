---
title: "uniapp 开发手册"
date: 2020-02-05 21:02:30
updated: 2020-04-28 11:41:00
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

### nvue

- 如果不开发App，那么不需要使用nvue
- 在app端，如果使用vue页面，则使用webview渲染；如果使用nvue(native vue)页面，则使用原生渲染，一个app可以同时使用两种

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

## [组件](https://uniapp.dcloud.io/component/)

- `uni-app`可以使用第三方的UI组件，但是如果跨端使用最好使用自带的组件，会有一些自带的优化、适应，风格也和`uni-app`一致
- `uni-ui`是一个跨端ui库，它是基于vue组件的、flex布局的、无dom的跨全端ui框架
- `uni-ui`不包括基础组件，它是`uni-app`基础组件的补充

### [list/uni-list](https://ext.dcloud.net.cn/plugin?id=24)

- 这是app端nvue专用组件，在`nvue`下，如果是长列表，使用list组件的性能高于使用view或scroll-view的滚动，因为list在不可见部分的渲染资源回收有特殊的优化处理
- 但是如果需要跨端，官方还是建议使用uni-ui的uni-list组件，它会自动处理webview渲染和原生渲染的情况，自动在app-nvue下使用list组件，而在其他平台使用页面滚动
- 综上，不如直接使用uni-list就行了
- 

## uniCloud

- 需要先创建云服务空间，然后关联云服务空间
- 但是论坛上还是大部分人持怀疑态度，毕竟长期的项目迭代，不应该绑定到一个商业平台上面来

### 云函数

- 自带uni-id的token，不用自己管理token了
- 默认不需要使用url，如果云函数需要URL化(如微信回调地址)，需要在后台配置url

```javascript
uniCloud.callFunction({
  name: 'test',
  success: (res) => {
    this.title = res
  }
})
```

### 云数据库

- 是一种clientDB，客户端可以直接调用，和firestore一样，可以设置权限，如果在云函数里面进行操作那么是管理员权限
- 云端居然有那么多的表模板，而且还有`schema2code`功能，然后直接导入hbuildx，这样在pages目录下会自动生成增删改查的vue文件，牛逼
- 可以直接写到模版中，不用写js

```vue
<unicloud-db ref="udb" v-slog:default="{data, loading, error, options }" collection="contacts">	<!--这里的contacts就是表名-->
  <view v-if="error">{{error.message}}</view>
  <view v-else>
    <uni-list>
      <uni-list-item v-for="item in items" @longpress.native="rmItem(item._id)"></uni-list-item>
    </uni-list>
  </view>
</unicloud-db>

// 删除云数据，当然要设置权限
rmItem(id) {
	this.$refs.udb.remove(id);	<!--我靠可以直接删除云数据库里面的东西，并且还自带确认删除弹窗，当然要设置权限啦-->
}

// 添加云数据，当然要设置权限
addItem() {
	const db = uniCloud.database();
	db.collection('contacts').add({}).then()
}
```

#### 权限控制

```json
// user表的schema
{
  "bsonType": "object",
  "required": [],
  "permission": {
    "read": true, // 任何用户都可以读
    "create": false, // 禁止新增数据记录（admin权限用户不受限）
    "update": false, // 禁止更新数据（admin权限用户不受限）
    "delete": false, // 禁止删除数据（admin权限用户不受限）
    "count": false // 禁止查询数据条数（admin权限用户不受限），新增于HBuilderX 3.1.0
  },
  "properties": {
    "_id":{},
    "name":{},
    "pwd": {}
  }
}
```

## 扩展阅读

- [uni-app 全局变量的几种实现方式](https://ask.dcloud.net.cn/article/35021)
- [完整的 uni-App+Laravel+jwt-auth 小程序权限认证](https://learnku.com/articles/43682)