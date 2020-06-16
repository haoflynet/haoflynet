---
title: "Nuxt.js 教程"
date: 2020-06-16 20:09:39
categories: js
---

为什么要用`nuxt.js`，主要就是因为它可以服务端渲染(SSR)，相比于传统的vue单页应用，将渲染放到服务器这边，性能肯定能得到很大提升，并且首次加载无需加载特别大的资源，且对搜索引擎友好，所以没有什么理由不用它。

## 目录结构

`assets`: 资源目录，用于组织未编译的静态资源

`components`: 组件目录

`layouts`: 布局目录

`middleware`: 中间件目录

`pages`: 页面目录

`plugins`: 插件目录

`static`: 插件目录，会被直接映射到根目录下，可以放置`favicon.ico/robots.txt`等文件

`store`: 用于组织应用的`vuex`状态树文件

`nuxt.config.js`: 个性化配置文件

<!--more-->

## 配置

`nuxt.config.js`

```javascript
module.exports = {
  mode: 'spa',

  /*
  ** Headers of the page
  */
  head: {
    title: pkg.name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'description' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' } // 配置favicon.ico，需要将图片放到static目录下
    ]
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [
    {src: '~assets/scss/front.scss'},
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    {src: '~/plugins/test', ssr: false},
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/axios'
  ],

  axios: {
    // proxyHeaders: false
    proxyHeaders: false,
    credentials: false
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  }
}
```

## API

### asyncData

- 渲染组件之前异步获取数据

### fetch

- 渲染页面之前填充应用的状态树(store)数据，与`asyncData`方法类似，不同的是它不会设置组件的数据
- 每次组件加载前被调用(在服务端或切换至目标路由之前)
- `fetch`内部是无法使用`this`获取当前组件实例，因为此时组件还未初始化
- 为了让获取过程可以异步，需要返回一个`Promise`，`Nuxt.js`会等这个`promise`完成后再渲染组件

```javascript
fetch ({ store, params }) {
	return axios.get('http://my-api/stars')
		.then((res) => {
			store.commit('setStars', res.data)
		}
	)
}

// 或者使用async的方式简化一下
async fetch ({ store, params }) {
  let { data } = await axios.get('http://my-api/stars')
  store.commit('setStars', data)
}
```

##### TroubleShooting

- **让组件不在服务端渲染而是在客户端渲染**: 可以给组件加一个`<no-ssr></no-ssr>`包围，但是注意它只能一次包含一个组件，不能多个
- **The client-side rendered virtual DOM tree is not matching server-rendered content. ** 出现这个`error`，解决方法同上
- **<no-ssr>不生效**: 可能是因为其包含的组件里面有槽，例如我在使用`vue-infinite-loading`的时候错误地在组件上加了`slot="append"`属性，导致`<no-ssr>`不生效，导致该组件既没在服务端渲染，也没在客户端渲染。