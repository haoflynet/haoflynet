---
title: "ADB: Android调试工具与自动化操作工具"
date: 2018-03-12 21:32:00
updated: 2018-12-12 17:29:00
categories: android
---

ADB(Android Debug Bridge)，即android的一个调试工具，主要用于开发安卓应用时调试与管理手机用，当然，非android程序员的我，主要用来自动化android设备，这一点，类似于web中的selenium。我用它实现了一个**自动发任意短信的功能**，网上的短信发送服务，格式都要求得太严格了，还不如自己用闲置手机发方便。

![](https://haofly.net/uploads/adb.jpeg)

当然，其主要的功能还是这些:

- 管理与电脑连接的android设备
- 管理android模拟器
- 上传/下载文件至android设备或者模拟器

<!--more-->

## 常用命令

```shell
adb devices	# 列出当前连接的设备(包括连接到电脑的手机以及模拟器)

adb install apk文件	# 安装指定的apk文件到设备
adb uninstall 软件包	# 卸载软件包

adb shell	# 登录设备的shell
adb push 本地路径 远程路径	# 将电脑上的文件复制到设备
adb pull 远程路径 本地路径	# 将设备上的文件复制到电脑

# 包管理命令pm，package manager
pm install -r $path/ES.apk	# 安装指定apk包

# 命令am，activity manager
am start -n com.estrongs.android.pop/com.estrongs.android.pop.view.FileExplorerActivity
	# 启动指定activity
```

## 控制安卓设备

### 模拟输入文字

**adb输入中文的问题：**adb默认是不支持中文字符输入的，不过这里有一个解决方法[ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard)，将其中的apk文件传入手机然后安装上，然后将手机输入法选择为`ADBKeyBoard`即可用`adb shell input`命令来输入中文。

```shell
adb shell input text "haofly.net"	# 在安卓设备中输入文字
```

### 模拟输入按键

```shell
adb shell input keyevent 67

# 常用键码对照
1(KEYCODE_MENU): menu键
3(KEYCODE_HOME): home键
4(KEYCODE_BACK): back键
21(KEYCODE_DPAD_LEFT): 光标左移
22(KEYCODE_DPAD_RIGHT): 光标右移
```

### 模拟触摸

想要知道需要触摸的具体位置，可以打开安卓的开发者模式，然后将按键坐标打开。

```shell
adb shell input tap 100 400	# 鼠标触控(100, 400)这个点
adb shell input swipe 10 10 200 200 # 从(10,10)滑动到(200, 200)
adb shell input touchscreen swipe 100 200 100 200 2000	# 在(100, 200)这个点持续按2000ms
```