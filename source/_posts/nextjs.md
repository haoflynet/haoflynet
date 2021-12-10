---
title: "Next.js 手册"
date: 2021-05-19 08:00:00
updated: 2021-11-16 08:37:00
categories: js
---

- `React`的`SSR`框架
- 需要注意的是如果页面中有用js控制的部分(例如条件渲染)，在SSR的时候不会直接渲染成DOM元素，虽然也能导出成静态HTML，但是仍然是前端js来控制的

## 基础配置

```shell
npx create-next-app@latest	# 初始化项目
npx create-next-app@latest --typescript	# 使用typescript初始化

# 如果要使用tailwindcss，不推荐tailwindcss官方的脚手架，-e with-tailwindcss安装完成后typescript和eslint都没有，还是自己集成吧，也挺简单的。
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init -p
# 根据文档https://tailwindcss.com/docs/guides/nextjs，替换tailwindcss中的purge和globals.css

npm install sass	# 增加对sass、scss的支持

next -p 3001	# 指定启动端口
```

### next.config.js

- 每次修改必须重启应用
- 在`.env`中设置的环境变量默认不会在后端渲染中被前端看到，但是如果以`NEXT_PUBLIC_`开头的环境变量，是能看到也能被前端直接使用的

```javascript
module.exports = {
  env: {	// 设置环境变量，设置后可以在jsx中直接用{process.env.customKey}获取值，环境变量还能设置在.env中
    customKey: 'my-value',
  },
  images: {
    domains: ['example.com']	// 定义哪些image允许展示
    loader: 'imgix',	// 如果图片存储在第三方，需要加这个设置
    path: '',	// 如果图片存储在第三方且使用相对路径需要添加域名在这里，但是如果是绝对路径，留空字符串即可
  },
  async redirects() {	// 设置重定向规则
    return [{
      source: '/home',
      destination: '/',
      permanent: true	// true表示永久重定向302，false表示暂时的，301
    }]
  },
  async rewrites() {	// 设置rewrites规则，将原来的路径进行重写以此来屏蔽实际的路径，浏览器url不会变化，但是该规则不适用于导出为纯静态的站点，如果是纯静态站点可能需要nginx等来配合
    return [{
        source: '/',
        source: '/old-blog/:slug',	// 也可以匹配参数
        source: '/blog/:slug*',	// 也可以模糊匹配
        source: '/post/:slug(\\d{1,})',	// 正则匹配
        destination: '/signin',
        permanent: true, // 重定向是否是permanent
        has: [{
          type: 'header',	// 可以匹配header中是否有某个key
          key: 'x-redirect-me'
        }, {
          type: 'query',	// 可以匹配query参数
          key: 'page',
          value: 'home'
        }, {
          type: 'cookie',	// 匹配cookie
          key: 'authorized',
          value: 'true'
        }, {
           type: 'header',
           key: 'x-authorized',
           value: '(?<authorized>yes|true)', // 可以提取value作为destination的值destination: '/home?authorized=:authorized',
        }]
      }]
  }
}
```

## 路由

### 路由定义

- 路由定义默认是根据pages文件夹下的文件名来的

```javascript
pages/blog/first-post.js → /blog/first-post
pages/dashboard/settings/username.js → /dashboard/settings/username

pages/blog/[slug].js → /blog/:slug (/blog/hello-world)
pages/[username]/settings.js → /:username/settings (/foo/settings)
pages/post/[...all].js → /post/* (/post/2020/id/title)

// 可以通过context获取路由参数
export async function getServerSideProps (context: NextPageContext): Promise<any> {
  console.log(context.query.all)	// all得到的是一个数组，按每一级来
  return {
    props: {}
  }
}
```

### 路由常用方法

```javascript
import { useRouter } from 'next/router';

const router = useRouter()		// 等同于window.location
router.query.search	// 获取query参数
router.push('/signin');	// 路由跳转
router.replace('/signin');	// 路由跳转
router.push({pathname: '/post/[pid]', query: {pid: post.id}})	// 指定参数
router.pathname;	// 获取当前的pathname，例如/signin
router.back();	// 返回上一页，即window.history.back()
router.reload();	// 刷新页面，即window.location.reload()
router.locale	// 当前的locale
router.locales	// 所有的locales
router.defaultLocale	// 默认的locale
```

### 路由事件

包括：routeChangeStart、routeChangeComplete、routeChangeError、beforeHistoryChange、hashChangeStart、hashChangeComplete

## 页面组件

- 通过变量渲染html，需要用`<div dangerouslySetInnerHTML={{__html = '<div></div>'}}`

### [Layouts](https://nextjs.org/docs/basic-features/layouts)

- 全局定义页面的layout

- 所有页面都相同的layout可以这样做

  ```javascript
  // pages/_app.js
  import Layout from '../components/layout'
  
  export default function MyApp({ Component, pageProps }) {
    return (
      <Layout>
        <Component {...pageProps} />
      </Layout>
    )
  }
  ```

- 如果不是所有页面的layout都相同，可以在单独的page里面这样做

  ```javascript
  // pages/_app.js，在_app.js中声明使用getLayout方法来获取Layout
  export default function MyApp({ Component, pageProps }) {
    // Use the layout defined at the page level, if available
    const getLayout = Component.getLayout || ((page) => page)
    return getLayout(<Component {...pageProps} />)
  }
  
  // pages/_app.tsx，如果是typescript需要这样声明
  type NextPageWithLayout = NextPage & {
    getLayout?: (page: ReactElement) => ReactNode
  }
  type AppPropsWithLayout = AppProps & {
    Component: NextPageWithLayout
  }
  export default function MyApp ({ Component, pageProps }: AppPropsWithLayout): ReactNode {
    // 我这里和官网不一样，如果有getLayout就用getLayout，否则就用全局的
    if (Component.getLayout) {
      return Component.getLayout(<Component {...pageProps} />)
    }
    return (<Layout><Component {...pageProps} /></Layout>)
  }
  
  // components/layout.js，自定义一个layout
  import Navbar from './navbar'
  import Footer from './footer'
  export default function CustomLayout({ children }) {
    return (
      <>
        <Navbar />
        <main>{children}</main>
        <Footer />
      </>
    )
  }
  // components/layout.tsx, typescript版本
  import React, { ReactElement } from 'react'
  interface LayoutProps {
    children: ReactElement
  }
  export default function Layout (props: LayoutProps): JSX.Element {
    return (
      <>
        <div>header</div>
        <main>{props.children}</main>
      </>
    )
  }
  
  
  
  // pages/index.js
  import Layout from '../components/layout'
  import NestedLayout from '../components/nested-layout'
  
  export default function Page() {}
  
  // 通过getLayout方法来定义
  Page.getLayout = CustomLayout
  ```

### Head

- 可以在`Head`里面插入全局的js，例如google analytics代码:

  ```javascript
  <Head>
    <script
  		dangerouslySetInnerHTML={{
      	__html: `[google analytics tracking code here]`
      }}
    />
  	<link
    	href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
  		rel="stylesheet"
  	/> // 字体优化，能够在编译阶段就优化字体，这样在打开页面不会因为要获取字体文件而闪一下
  </Head>
  ```

### Image

- 需要在`next.config.js`中配置图片域名`images.domains`
- 可以设置width、height、quality、priority、responsive自动修改图片显示大小
- 但是毕竟是后端js程序在进行转换，不如直接使用`cloudinary`这样的服务速度快功能多
- 如果图片存储在第三方需要添加配置`images: loader: 'imgix'`
- width和height必填，除非`layout=fill`

```javascript
import Image from 'next/image'

<Image
  loader={myLoader}
  src="me.png"	// 要么是本地静态文件，要么用绝对路径，不能用//开头的路径
  alt="Picture of the author"
  width={500}
  height={500}
/>
```

#### 使用svg作为component

- 和其他框架一样，都是用`npm install @svgr/webpack --save-dev`
- 需要做如下配置:

```javascript
// next.config.js 添加如下配置
module.exports = {
  webpack(config) {
    config.module.rules.push({
      test: /\.svg$/,
      use: ["@svgr/webpack"]
    });

    return config;
  }
};
```

### Link

```javascript
<Link href=''>
  <a>title</a>
</Link>

<Link href=''>
  <a><Image ... /></a> // 如果link下需要包含image，不能直接image，外面得加一层a标签
</Link>
```

## 后端渲染SSR

- 在组件加载前就从接口获取数据，才能实现后端渲染，而不是前端去调用API
- 需要注意的是通过服务端获取的props，必须直接传递到html中去，不要用useEffect等去传递给另外一个变量，那样就不会直接渲染到HTML中去了，浏览网页源代码发现他们只是在一个变量上，对SEO十分不友好
- `getServerSideProps`和`getInitialProps`都无法用在404页面上，如果是404页面只能在`componentDidMount`或者`useEffect(() => {}, [])`里面去请求获取数据了，[官方说明](https://nextjs.org/docs/messages/404-get-initial-props)

<!--more-->

```javascript
class MyComponent extends React.Components {
  static getInitialProps() {
    return fetch('').then(response => response.json())	// 需要返回一个字典
  }
  
  render() {
    return (<div>aaa</div>)
  }
}

// 如果是函数式组件可以这样做
function MyComponent() {
  return (<div>aaa</div>)
}
MyComponent.getInitialProps = async () => {
  return fetch('').then(response => response.json())
}

// 官方推荐的是getServerSideProps，需要注意的是它不能做用于纯component，必须是page
export async function getServerSideProps(){
  const data = await myAPI('/api/resource')
  return {
    props: { data }
  }
}

// 如果是不会改变的数据可以用getStaticProps，它会在编译的时候就静态的props传入组件，所以如果接口返回的数据有变化，也只有重新编译才行
export async function getStaticProps() {
  const data = await myAPI('/api/resource')
  return {
    props: { data }
  }
}

// 用于在使用动态路由时生成静态文件，他是配合getStaticProps使用的，getStaticProps根据url生成不同的页面
export async function getStatisPaths() {
  const res = await myAPI('/api/resource')
  const paths = res.data.map(resource => `/resource/${resource.id}`)
  return {
    paths, // 有多个path就会生成多个静态页面
    fallback: false
  }
}

export default MyComponent
```

## Hook

### 获取window size

```javascript
// hooks/useWindowResize.js
import React, { useLayoutEffect, useState } from 'react';

export default function useWindowResize() {
    const [size, setSize] = useState([0, 0]);
    
    useLayoutEffect(() => {
        function updateSize() {
            setSize([window.innerWidth, window.innerHeight]);
        }
        
        window.addEventListener('resize', updateSize);
        
        updateSize();
        
        return () => window.removeEventListener('resize', updateSize);
    }, []);
    return size;
}

// 其他组件就能这样引用了
const [windowWidth, windowHeight] = useWindowResize();
```

## 其他特性

### 动态引入模块

```javascript
const DynamicComponent = dynamic(() => import('../components/hello'))

<DynamicComponent />
```

### 国际化i18N

- nextjs的国际化支持很棒，只要设定好需要哪些语言，就只要在切换语言的时候指定语言，而不需要更改页面中其他的地方
- 支持通过域名来切换语言，或者通过path前缀来切换语言

```javascript
// next.config.js
module.exports = {
  i18n: {
    locales: ['en-US', 'fr', 'nl-NL'],	// 声明支持哪些语言
    defaultLocale: 'en-US',	// 声明默认的语言
    domains: [	// 如果想通过域名来确定语言，需要在这里设置域名，如果不设置这个，那么默认是通过path来确定的，例如，默认是/blog，带语言就是/fr/blog，nl-nl/blog
      {
        domain: 'example.com',
        defaultLocale: 'en-US',
      },
      {
        domain: 'example.nl',
        defaultLocale: 'nl-NL',
      },
      {
        domain: 'example.fr',
        defaultLocale: 'fr',
      },
    ],
  },
}
```

## TroubleShooting

- **pages with `getServerSideProps` can not be exported.** 需要将`package.json`中的`build`命令中的`next export`去掉，它和`getServerSideProps`不兼容
- **getServerSideProps不起作用**: 它只能做用于page，不能直接作用于component
- **初始进入admin太慢**: 是因为js太大，尝试给nginx加上gzip试试
- **rewrites会render两次**: 我也不清楚原因，目前正在论坛上问https://github.com/vercel/next.js/discussions/27985
- **生成的静态页面会有__next_data__字段存储着所有的props信息**：这样页面上其实就有两份数据了，但是看作者的意思是所有的后端渲染都会这样做的，无法去掉https://github.com/vercel/next.js/discussions/13418，所以最好用graphql等或者其他方式只保留需要的字段

