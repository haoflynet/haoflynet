---
title: "electron 手册"
date: 2023-04-19 19:59:00
categories: js
---

- 使用Nodejs编写跨平台桌面应用程序
- Electron Fiddle是官方的沙盒程序

## 安装配置

- 可以使用React脚手架来初始化[electron-react-boilerplate](https://github.com/electron-react-boilerplate/electron-react-boilerplate)

  - 虽然它推荐的是Electron Store来存储状态，但是依然可以用redux或者[mobx](https://haofly.net/mobx/)，并且持久化也可以直接用localStorage，mobx的话就是`mobx-persist-store`


  ```shell
  npm run start 	# 运行APP
  npm run build	 # 编译
  ANALYZE=true npm run build	# 能够直接分析build完成后包的各部分所占的体积
  npm run package	# 打包app，能直接打包成zip或者dmg。可以在package.json中修改package参数，如果添加-mwl表示同时打包--mac, --win, --linux
  ```

- 添加依赖

  ```shell
  ./package.json # 非native的module，或者类型依赖@types/*
  ./release/app/package.json # native modules需要安装在这里，不需要编译
  ```

- package.json配置

  ```json
  {
    "build": {
      "mac": {
        "identity": "Apple Development: xxxx (xxx)"	// 指定签名的identity，否则可能会自动选择到一个无效的identity导致应用打不开，可以用security find-identity -v查看当前所有的identity
      }
    }
  }
  ```

<!--more-->

## 进程

- 主进程 main process：启动应用后就会创建，可以i通过electron中的模块直接与原生GUI交互，在它里面调用BrowserWindow创建应用的窗口
- 渲染进程 renderer process：每个页面都是运行在自己的进程里面，就是渲染进程。渲染进程会在窗口中渲染出web页面，web页面是Chromium渲染的。每个渲染进程都是相互隔离的，并且只知道运行在自己进程里的页面
- 进程有多种通信方式：ipc模块，webContents.send(Main进程主动向Renderer进程发送消息)、remote模块

## 常用功能实现

##### 使用dotenv设置环境变量

尝试了很多方法，最终只找到下面这个方法可用

1. 在渲染进程`preload.ts`中创建一个方法向主进程获取环境变量
   ```javascript
   const electronHandler = {
     ...
     getConfig(config?: string) {
       const configs = ipcRenderer.sendSync('get-env');
       if (config) {
         return configs[config];
       }
       return configs;
     }
   }
   ```

2. 在主进程中`main.ts`监听该事件

   ```java
   ipcMain.on('get-env', async (event) => {
     event.returnValue = {
       BACKEND_API: process.env.BACKEND_API,
     };
   });

3. 在webpack中(`webpack.config.base.ts`)调用`dotenv`获取环境变量

   ```javascript
   module: {
     ...
     plugins: [
         new webpack.EnvironmentPlugin({
         NODE_ENV: 'production',
         ...dotenv.config().parsed
       }),
     ]
   }
   ```

##### [关闭所有窗口时退出应用 (Windows & Linux)](https://www.electronjs.org/zh/docs/latest/tutorial/quick-start#关闭所有窗口时退出应用-windows--linux)

##### [如果没有窗口打开则打开一个窗口 (macOS)](https://www.electronjs.org/zh/docs/latest/tutorial/quick-start#如果没有窗口打开则打开一个窗口-macos)

## TroubleShooting

- **electron v9.4.4-darwin-arm64.zip not found**: 可能原因是使用的apple m1芯片，至少需要将版本提高到`"electron": "^11.0.1"`

## 参考

- [bilimini](https://github.com/chitosai/bilimini): 哔哩哔哩小窗口客户端