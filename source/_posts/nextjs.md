---
title: "Next.js 手册"
date: 2021-05-19 08:00:00
categories: js
---

- `React`的`SSR`框架

## 基础配置

```shell
next -p 3001	# 指定启动端口
```

## 路由

```javascript
import { useRouter } from 'next/router'

const router = useRouter()	// 等同于window.location
router.pathname	// 获取路由路径
router.query.search	// 获取query参数
router.locale	// 当前的locale
router.locales	// 所有的locales
router.defaultLocale	// 默认的locale
```

## 后端渲染SSR

- 在组件加载前就从接口获取数据，才能实现后端渲染，而不是前端去调用API，这就要求我们要在组件的`getInitialProps`方法中获取数据
- 需要注意的是通过服务端获取的props，必须直接传递到html中去，不要用useEffect等去传递给另外一个变量，那样就不会直接渲染到HTML中去了，浏览网页源代码发现他们只是在一个变量上，对SEO十分不友好

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

// 官方推荐的是getServerSideProps
export async function getServerSideProps(){
  const data = await myAPI('/api/resource')
  return {
    props: { data }
  }
}

// 如果是不会改变的数据可以用getStaticProps，它会在编译的时候就静态的props传入组件，所以如果接口返回的数据有变化，也只有重新编译才行
export async function getStaticProps(){
  const data = await myAPI('/api/resource')
  return {
    props: { data }
  }
}

export default MyComponent
```

## Hook

### 一个获取window size的hook

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

## TroubleShooting

- **pages with `getServerSideProps` can not be exported.d** 需要将`package.json`中的`build`命令中的`next export`去掉，它和`getServerSideProps`不兼容

