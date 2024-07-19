---
title: "proxychains 手册"
date: 2024-06-16 23:02:30
categories: system
---

Proxychains是一个强大的工具，可以帮助用户在各种网络环境中实现代理访问，能够动态地将程序的套接字重定向到指定的代理。通过正确的配置和使用，能够大大提升网络操作的灵活性和便利性。clash的代理通常只能用于http或者https以及socks5，相当于设置了`https_proxy`, `http_proxy`, `all_proxy`，但不是所有的程序都会自动读取这几个环境变量，这个时候可以使用Proxychains直接更改套接字层。

## 安装使用

- Github地址: [proxychains-ng](https://github.com/rofl0r/proxychains-ng)

```shell
brew install proxychains-ng	# For Mac

vim ~/.proxychains/proxychains.conf # 创建配置文件，内容如下：
[ProxyList]
socks5 127.0.0.1 7890	# 这就是我实际代理的地址，clash默认就是7890端口
```

## 使用场景

之前不能使用代理的很多场景现在都能通过代理了：

- Firebase
  ```shell
  proxychains4 node main.js
  ```

- Android Studio模拟器:
  ```shell
  proxychains4 ~/Library/Android/sdk/emulator/emulator -avd Medium_Tablet_API_26
  ```

  