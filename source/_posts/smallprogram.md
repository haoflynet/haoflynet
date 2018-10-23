---
title: "微信小程序开发手册"
date: 2018-10-17 13:15:00
categories: javascript
---

官方文档非常详细，这里就不复制了，只记录一些自己用到的。

<!--more-->

### [框架文档](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/MINA.htm)

#### 配置

全局配置`app.json`

页面单独配置`页面名.json`

```json
{
  "navigationBarBackgroundColor": "#ffffff",	// 导航栏背景颜色
  "navigationBarTextStyle": "black",	// 导航栏标题颜色
  "navigationBarTitleText": "导航栏标题文字内容",
  "backgroundColor": "#eeeeee",	// 窗口的背景色
  "backgroundTextStyle": "light"	// 下拉 loading 的样式
}
```

#### 框架结构

- 可以将一些全局变量放在`app.js`中，这样全局都是能获取到的

#### 页面跳转

- wx.navigateTo('/pages/index/index?id=123'): 如果要传递参数，可以在query参数中添加，然后在目标页面的`onLoad(options)` 中获取`options.id`即可。需要注意，这个方法不能跳转给`Tab`，相当于是把一个新页面压入栈中，返回的时候就返回到刚才的页面。

- wx.navigateBack()不能直接携带参数，但是可以直接在其他页面获取之前栈中页面的page对象，然后直接进行setData：

  ```javascript
  let pages = getCurrentPages()
  let lastPage = pages[pages.length - 2];
  lastPage.setData({})
  wx.navigateBack({})
  ```

#### 事件

- 事件传参数，例如bindtap事件，不能直接像js那样打个括号把参数传递进去，而应该这样子传递

  ```javascript
  <view id="myId" data-field="自定义字段，不能大写" bindtap="bindtap"> Click me! </view>
  
  // 然后在Page里面这样定义和接收参数
  Page({
      bindtap: function (e) {
          console.log(e)
          console.log(e.target)	// target数据结构和currentTarget一样，不过它表示触发事件的源组件，而currentTarget表示事件绑定的当前组件
          console.log(e.currentTarget)
          console.log(e.currentTarget.id)	// id不用在dataset中获取
          console.log(e.currentTarget.dataset.field)
      }
  })
  ```

### [组件文档](https://mp.weixin.qq.com/debug/wxadoc/dev/component/)

- 目前所有的原生组件都有一些使用限制，比如`z-index`默认为最高，并且无法更改。如果要覆盖，得使用`cover-view`这个原生组件。

#### cover-view

用于覆盖原生组件：`map/video/canvas/camera/live-player/live-pusher`，但是内部只支持嵌套`cover-view/cover-image/button`

#### map

- 最好整个小程序只维护一个`map`组件，不然可能会崩溃，性能很重要

### [API文档](https://mp.weixin.qq.com/debug/wxadoc/dev/api/)

#### 元数据

```javascript
// 动态修改页面标题
wx.setNavigationBarTitle({
    title: '标题1',
}
                         
// 获取屏幕信息
wx.getSystemInfoSync().windowWidth	// 屏幕宽度                         
```

#### 网络

```javascript
wx.request({
  url: 'test.php',
  data: {'x': '', y: ''}
  header: { 'content-type': 'application/json'},
  success (res) { console.log(res.data)}
})
```

#### 位置

```javascript
wx.getLocation(OBJECT)	// 获取当前的地理位置、速度
wx.chooseLocation(OBJECT)	// 打开地图选择位置
wx.openLocation(OBJECT)	// 使用微信内置的地图查看某个位置
```

### [其他工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/devtools.html)

## TroubleShooting

- **无法在开发工具上修改appid，或者修改时出现`修改失败: undefined`**: 直接将当前项目删除，然后新建一个项目，在新建的时候就指定appid即可

- **新功能无法使用，例如map中的enable-zoom等**，首先看文档里面有没有直接写明开发者工具上可否使用，然后可以在在真机上面调试试试。

- **cover-view里面不能放自定义text标签导致不能自定义样式**: 社区给出的意见是[https://developers.weixin.qq.com/community/develop/doc/000a402c99849820f2470d50551000]，给`cover-view`设置样式

- **获取输入框的value值**: 通常我们不会用系统的表单，那么可以通过这种方式像普通的html页面那样获取dom元素的值:

  ```javascript
  <input type="text" value="{{name}}" bindinput="tapInput">
      
  // 然后在js中直接监听输入事件即可
  tapInput: function(e) {
      console.log(e.detail.value)
  }
  ```

- **warning： Now you can provide attr "wx:key" for a "wx:for" to improve performance.**这是因为在使用循环`block`的时候没有给循环的item设置一个唯一的id，可以这样做:

  ```javascript
  <block wx:for-items="{{list}}" wx:key="list.id">
  ```

##### 扩展阅读

- [健壮高效的小程序登录方案](https://mp.weixin.qq.com/s?__biz=MzU0OTExNzYwNg==&mid=2247484421&idx=1&sn=a40c6ca294de39fe502a8d511994da34&chksm=fbb58fccccc206dae8b559365706a8b60f6ce654b46b0414b1a04c7481502d3838c030450dc3&token=1355569705&lang=zh_CN&rd2werd=1#wechat_redirect)

