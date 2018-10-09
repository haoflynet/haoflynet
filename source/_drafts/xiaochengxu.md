---
title: "微信小程序开发手册"
date: 2017-03-15 21:35:00
categories: javascript
---

## 微信小程序开发教程

官方文档非常详细，这里就不复制了。

### [框架文档](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/MINA.html)

#### 页面跳转

- wx.navigateTo('/pages/index/index?id=123'): 如果要传递参数，可以在query参数中添加，然后在目标页面的`onLoad(options)` 中获取`options.id`即可。需要注意，这个方法不能跳转给`Tab`，相当于是把一个新页面压入栈中，返回的时候就返回到刚才的页面。

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



### [API文档](https://mp.weixin.qq.com/debug/wxadoc/dev/api/)









## TroubleShooting

- **无法在开发工具上修改appid，或者修改时出现`修改失败: undefined`**: 直接将当前项目删除，然后新建一个项目，在新建的时候就指定appid即可

- **新功能无法使用，例如map中的enable-zoom等**，首先看文档里面有没有直接写明开发者工具上可否使用，然后可以在在真机上面调试试试。

- **warning： Now you can provide attr "wx:key" for a "wx:for" to improve performance.**这是因为在使用循环`block`的时候没有给循环的item设置一个唯一的id，可以这样做:

  ```javascript
  <block wx:for-items="{{list}}" wx:key="list.id">
  ```

##### 扩展阅读



https://github.com/CH563/TodoList-wechat



https://github.com/yangzaiwangzi/KM-MiniProgram



https://github.com/kesixin/MP_MambaBlog_Online

https://github.com/ningge123/wonderfully