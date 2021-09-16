---
title: "Antd "
date: 2019-09-05 14:40:00
updated: 2021-09-16 18:00:00
categories: Javascript
---

## 组件

### General

#### Icon图标

- 如果要直接用自定义的svg作为icon图标可以这样做: 

```javascript
// 安装vue-svg-loader: npm i -D vue-svg-loader vue-template-compiler

// 添加编译时配置，在vue.config.js中添加
chainWebpack: (config) => {
    const svgRule = config.module.rule('svg')
    svgRule.uses.clear()
    svgRule
      .use('vue-loader')
      .loader('vue-loader') // or `vue-loader-v16` if you are using a preview support of Vue 3 in Vue CLI
      .end()
      .use('vue-svg-loader')
      .loader('vue-svg-loader')
  }

// 直接使用svg文件
import MessageSvg from 'path/to/message.svg';

<a-icon :component="MessageSvg" />
```

### Feedback
#### Notification 通知提醒框

- 

## TroubleShooting

- ****

