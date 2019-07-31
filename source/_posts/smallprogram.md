---
title: "微信小程序开发手册"
date: 2018-10-17 13:15:00
updated: 2019-07-31 18:12:00
categories: javascript
---

官方文档非常详细，这里就不复制了，只记录一些自己用到的。

<!--more-->

### [框架文档](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/MINA.htm)

#### 配置

全局配置`app.json`

```json
{
	"tabBar": {		// 底部导航配置
    	"color": "#a9b7b7",			// 未选择时底部导航的文字颜色
    	"selectedColor": "#11cd6e",	// 选择时底部导航的文字颜色
    	"borderStyle":"white",		// 底部导航边框的颜色
    	"list": [{
      		"selectedIconPath": "images/home_selected.png",	// 底部导航被选择时的图片
      		"iconPath": "images/home.png",					// 底部导航未选择时的图片
      		"pagePath": "pages/index/index",
      		"text": "首页"
    	}]
  },
}
```

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

#### 页面生命周期

```javascript
onShow			// 监听页面显示，如果是第一次，它发生在onLoad之前
onLoad			// 监听页面加载
onReady			// 监听页面初次渲染完成
onHide			// 监听页面隐藏
onUnload		// 监听页面卸载
onPullRefresh	// 监听用户下拉动作
onReachBottom	// 页面上拉触底事件的处理函数
```

#### 页面跳转

- wx.navigateTo('/pages/index/index?id=123'): 如果要传递参数，可以在query参数中添加，然后在目标页面的`onLoad(options)` 中获取`options.id`即可。需要注意，这个方法不能跳转给`Tab`，相当于是把一个新页面压入栈中，返回的时候就返回到刚才的页面。

- wx.navigateBack()不能直接携带参数，但是可以直接在其他页面获取之前栈中页面的page对象，然后直接进行setData：

  ```javascript
  let pages = getCurrentPages()
  let lastPage = pages[pages.length - 2];
  lastPage.setData({})
  wx.navigateBack({})
  ```

- wx.reload(options): 直接刷新当前页面

#### 用户信息

##### 登录功能

- 需要注意的是，可以不经用户统一直接调用登录接口，但是只能获取到其`OpenId`和`session_key`

登录逻辑，官方这张图片很简单了

![](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/image/api-login.jpg)

##### 获取用户信息

- 敏感信息包含`openId/unionId`

```javascript
// 需要自己写一个button让用户主动触发，例如
<button open-type="getUserInfo" bindgetuserinfo="bindGetUserInfo"
>登录</button>

// 在js中这样获取
bindGetUserInfo: function(res) {
    res.userInfo	// 用户信息对象，不包含openid等敏感信息
    res.rawData		// 不包括敏感想你洗的原始字符串，用于计算签名
    res.signature	// 签名数据
    res.encryptedData	// 包含敏感数据在内的完整用户信息的加密数据
    res.iv				// 加密算法的初始向量
}

// 查看是否授权
wx.getSetting({
    success(res) {
        if (res.authSetting['scope.userInfo']) {
            // 已经授权，可以直接调用 getUserInfo 获取头像昵称
            wx.getUserInfo({
                success(res) {
                    console.log(res.userInfo)
                }
            })
        }
    }
})
```

#### 事件

- 常用事件有tap(点击)、longtap(长按)

- 阻止事件冒泡：将`bindtap`修改为`catchtap`即可

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

#### text

#### textarea

多行输入框

### [API文档](https://mp.weixin.qq.com/debug/wxadoc/dev/api/)

#### setData页面数据

```javascript
this.setData({
    'array[0].field': 'value',	// 可以用这种方式直接设置列表里面某个元素的值，而不用取出来再放回去set
})

new_array = this.data.array.splice(index, 1)	// 但是删除元素还是有点麻烦
this.setData({
    'array': new_array
})
```

#### 数据存储

- 同一个微信用户，同一个小程序storage上限未10MB，用户纬度隔离
- 单个`key`允许存储的最大数据长度未1MB
- 数据存储生命周期跟小程序本身一致，即除用户主动删除或超过一定时间被自动清理，否则数据都一致可用。如果用户储存空间不足，会自动清空最近最久未使用的小程序的本地缓存。
- 后面加`Sync`的表示同步方法，异步一般有`success/fail/complete`回调函数，而同步则需要自己去`catch`异常

```javascript
wx.clearStorage()	// 异步清理本地数据缓存
wx.getStorage({key:'key', success(res){}})	// 异步从本地缓存中获取指定key的内容
wx.getStorageInfo({success(res) {
    console.log(res.keys)	// 当前storage中所有的key
    console.log(res.currentSize)	// 当前占用的空间大小，单位KB
    console.log(res.limitSize)}		// 限制的空间大小，单位KB
})	// 异步获取当前storage的相关信息
wx.removeStorage({key: 'key'})	// 从本地缓存中移除指定的key
wx.setStorage({key: 'key', data: data})	// 设置缓存
wx.setStorageSync('key', 'value')
```

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
  success: function(res) { console.log(res.data)},
  complete: function() {console.log('无论成功与否都会执行')},
})
```

#### 分享/转发

```javascript
// 添加该元素，打开页面之后就能在右上角点击分享了
onShareAppMessage: function () {
    return {
      path: '/pages/index/index
      title: 'name',
    }
}

// 如果同一个页面有些能分享有些不能分享，可以在load里面调用这个方法，隐藏分享
wx.hideShareMenu()
```

#### 位置

```javascript
wx.getLocation(OBJECT)	// 获取当前的地理位置、速度
wx.chooseLocation(OBJECT)	// 打开地图选择位置
wx.openLocation(OBJECT)	// 使用微信内置的地图查看某个位置
```

### 性能优化

- this.setData()的优化，如果是不必要的字段，完全可以不用该字段进行set，可以自己另外设置一个字段例如`this._data`去更新值

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

- **元素水平垂直居中对齐**

  ```css
  .parent {
      text-align:center;
      align-items:center;
      justify-content: center;
      margin: auto;
      
      display: flex;
      align-items: center;
  }
  ```

- **开发时分享出去的链接用户打开提示“暂无开发权限”**: 原因是没有将对方设置为开发者或者体验者，需要在后台的开发设置中进行设置，或者在微信“小程序助手”中进行成员管理

- **warning： Now you can provide attr "wx:key" for a "wx:for" to improve performance.**这是因为在使用循环`block`的时候没有给循环的item设置一个唯一的id，可以这样做:

  ```javascript
  <block wx:for-items="{{list}}" wx:key="list.id">
  ```

##### 扩展阅读

- [健壮高效的小程序登录方案](https://mp.weixin.qq.com/s?__biz=MzU0OTExNzYwNg==&mid=2247484421&idx=1&sn=a40c6ca294de39fe502a8d511994da34&chksm=fbb58fccccc206dae8b559365706a8b60f6ce654b46b0414b1a04c7481502d3838c030450dc3&token=1355569705&lang=zh_CN&rd2werd=1#wechat_redirect)
- [小程序登录、微信网页授权](https://juejin.im/post/5c125b5f6fb9a049b13e1404): 介绍了微信各个种类帐号的区别
- [微信小程序跨页面通信解决思路](https://aotu.io/notes/2017/01/19/wxapp-event/index.html)
- [Gitter for GitHub](https://github.com/huangjianke/Gitter): 小程序版的Github客户端
- [小程序云开发实战 - 口袋工具之“历史上的今天”](https://juejin.im/post/5d3eaa3af265da039a285fa3)

##### 推荐UI扩展

[weui-wxss](https://github.com/Tencent/weui-wxss)

##### 框架扩展

[wepy](https://github.com/Tencent/wepy): 腾讯官方的小程序组件化开发框架