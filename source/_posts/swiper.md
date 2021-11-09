---
title: "Swiper 插件使用"
date: 2021-03-28 14:40:00
updated: 2021-10-20 15:16:00
categories: Javascript
---

[官方文档](https://swiperjs.com/get-started/)

## 使用方法

```javascript
var swiper = new Swiper('.swiper-container', {
  slidesPerView: 'auto',	// 每一页的slide数量自动确定，这样可以做到不用整数个显示，也不会导致左右空白
  spaceBetween: 10,	// 每两个slide之间的间隔
  centeredSlides: false,	// 不用从居中开始，否则左边是空白的
  pagination: {
    el: '.swiper-pagination',	// 分页元素位置
    clickable: true,
  },
  direction: 'vertical', // horizontal滚动方向
  width: 500,	// 设置slide的高度和宽度，单位职能是px
  height: 500,
  breakpoints: { // 可以自定义不同的breakpoints里面的不同参数
    1280: {	// 屏幕宽度>=1280时候的breakpoings
      width: 1000,
      height: 1000,
      direction: 'vertical', // 任何参数都可以breakpoint
    }
  }
  scrollbar: {
    el: '.swiper-scrollbar',	// scrollbar的位置
    clickable: true,
    hide: true
  },
  navigation: {			// 指定翻页按钮
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  on: {	// 使用对应的事件
    afterInit: function () {}
    activeIndexChange: function () {}, // 这个事件触发时active图片还没改变
    slideChange: function() {},	// 这个事件触发时图片就改变了
    slideChangeTransitionEnd: function() {}, // 感觉这个方法才是真正的改变完成了
  }
});
```

<!--more-->

- **Lazy Load Images**: 

```java
var swiper = new Swiper('.swiper-container', {
  lazy: true,
  lazy: {
    preloaderClass: 'my-preloader'	// 默认lazy=true即可，但如果需要自定义preloader类名需要这样做
  }
})
```

##### Troubleshooting

- **swiper不能滑动**，可以参考https://segmentfault.com/a/1190000013044682，其实可以在watch里面监听props，然后nexttick里面再次渲染



