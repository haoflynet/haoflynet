---
title: "Vue实现简单的鼠标拖拽滚动效果"
date: 2020-08-10 00:00:00
categories: javascript
---

在需要这个效果的时候首先在npm仓库找到了`vue-dragscroll`库，但是应用在我们自己项目上的时候拖动起来却非常慢，元素跟不上鼠标的移动速度，无奈，就自己简单的实现了一个拖拽指令:

```javascript
import Vue from 'vue'

Vue.directive('dragscroll', function (el) {
  el.onmousedown = function (ev) {
    const disX = ev.clientX
    const disY = ev.clientY
    const originalScrollLeft = el.scrollLeft
    const originalScrollTop = el.scrollTop
    const originalScrollBehavior = el.style['scroll-behavior']
    const originalPointerEvents = el.style['pointer-events']
    el.style['scroll-behavior'] = 'auto'
    // 鼠标移动事件是监听的整个document，这样可以使鼠标能够在元素外部移动的时候也能实现拖动
    document.onmousemove = function (ev) {
      ev.preventDefault()
      const distanceX = ev.clientX - disX
      const distanceY = ev.clientY - disY
      el.scrollTo(originalScrollLeft - distanceX, originalScrollTop - distanceY)
      // 由于我们的图片本身有点击效果，所以需要在鼠标拖动的时候将点击事件屏蔽掉
      el.style['pointer-events'] = 'none'
    }
    document.onmouseup = function () {
      document.onmousemove = null
      document.onmouseup = null
      el.style['scroll-behavior'] = originalScrollBehavior
      el.style['pointer-events'] = originalPointerEvents
    }
  }
})
```

由于我们项目使用了是`Nuxtjs`，如果完全由后端渲染，是无法在`document`上进行事件监听的，所以在`nuxt.config.js`中这样定义插件:

```javascript
plugins: [
  { src: '@/plugins/dragscroll', ssr: false }
],
```

最后可以在任何元素上应用该指令:

```html
<div dragscroll><img /></div>
```

最终的结果类似这样

![](https://haofly.net/uploads/vue-dragscroll.gif)