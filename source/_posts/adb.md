---
title: "ADB: Android调试工具与自动化操作工具"
date: 2018-03-12 21:32:00
updated: 2022-09-06 15:29:00
categories: android
---

ADB(Android Debug Bridge)，即android的一个调试工具，主要用于开发安卓应用时调试与管理手机用，当然，非android程序员的我，主要用来自动化android设备，这一点，类似于web中的selenium。我用它实现了一个**自动发任意短信的功能**，网上的短信发送服务，格式都要求得太严格了，还不如自己用闲置手机发方便。

![](https://haofly.net/uploads/adb.jpeg)

当然，其主要的功能还是这些:

- 管理与电脑连接的android设备
- 管理android模拟器
- 上传/下载文件至android设备或者模拟器

##### Mac安装方式

```shell
brew install android-platform-tools
```

<!--more-->

## 常用命令

### 设备管理

```shell
adb devices	# 列出当前连接的设备(包括连接到电脑的手机以及模拟器)
adb shell netcfg	# 查看手机IP
```

#### 无线连接

要使用无线的方式进行管理，必须得先在手机上打开一个监听端口。方法就是先用usb线连接电脑，然后执行`adb tcpip 5555`命令开启端口，接下来就可以用`adb connect {ip}`的方式管理手机了。(对于root的手机，可以直接在手机上面的terminal类软件上执行`setprop service.adb.tcp.port 5555 && stop adbd && start adbd`即可，当然也有类似的软件可以直接一键开启，不过都得要root权限)

### 信息查看

```shell
# 打印电源相关的信息
adb shell dumpsys power	# mScreenOn=false表示当前为息屏状态或者看mHoldingDisplaySuspendBlocker
```

### 文件管理

```shell
adb push 本地路径 远程路径	# 将电脑上的文件复制到设备
adb pull 远程路径 本地路径	# 将设备上的文件复制到电脑
```

### 包管理

- pm(package manager)

```shell
adb shell pm list packages	# 列出所有的包名
adb shell pm install -r $path/ES.apk	# 安装指定apk包
adb shell am start -n 包名	# 打开指定应用，注意这里的包名不一定能直接打开，可能得再下面的详情里面找到首页的activity component
adb shell dumpsys package 包名	# 查看指定包的详情，Activity等
adb install apk文件	# 安装指定的apk文件到设备
adb uninstall 软件包	# 卸载软件包
adb shell ps	# 查看运行中的进程
```

### 应用内部管理

- am(activity manager)

```shell
am start -n com.estrongs.android.pop/com.estrongs.android.pop.view.FileExplorerActivity	# 
```

### 输入文字

- **adb输入中文的问题：**adb默认是不支持中文字符输入的，不过这里有一个解决方法[ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard)，将其中的apk文件传入手机然后安装上，然后将手机输入法选择为`ADBKeyBoard`即可用命令来输入中文。

```shell
adb shell input text "haofly.net"	# 在安卓设备中输入文字

# 如果打开了ADBKeyBoard键盘，那么应该这样输入中英文:
adb shell am broadcast -a ADB_INPUT_TEXT --es msg '输入中文'
adb shell am broadcast -a ADB_INPUT_CODE --es code 67	# KEYCODE_DEL
```

### 模拟按键

`adb shell input keyevent KEYCODE_HOME`

键码对照表

| 数字表示 | 常量表示               | 功能                 |
| -------- | ---------------------- | -------------------- |
| 1        | KEYCODE_MENU           |                      |
| 2        | KEYCODE_SOFT_RIGHT     |                      |
| 3        | KEYCODE_HOME           | home键               |
| 4        | KEYCODE_BACK           | back键               |
| 5        | KEYCODE_CALL           | 拨号键               |
| 6        | KEYCODE_ENDCALL        | 挂机键               |
| 7至16    | KEYCODE_0 至 KEYCODE_9 | 按键'0'至'9'         |
| 17       | KEYCODE_STAR           | *                    |
| 18       | KEYCODE_POUND          | #                    |
| 19       | KEYCODE_DPAD_UP        | 方向键向上           |
| 20       | KEYCODE_DPAD_DOWN      | 方向键向下           |
| 21       | KEYCODE_DPAD_LEFT      | 光标左移             |
| 22       | KEYCODE_DPAD_RIGHT     | 光标右移             |
| 23       | KEYCODE_DPAD_CENTER    | 导航键 确定键        |
| 24       | KEYCODE_VOLUME_UP      | 音量加键             |
| 25       | KEYCODE_VOLUME_DOWN    | 音量减键             |
| 26       | KEYCODE_POWER          | 电源键(息屏、亮屏)   |
| 27       | KEYCODE_CAMERA         | 拍照键               |
| 28       | KEYCODE_CLEAR          | 清除键               |
| 29-54    | KEYCODE_A 至 KEYCODE_Z | 按键'A' 至'Z'        |
| 55       | KEYCODE_COMMA          | ,                    |
| 56       | KEYCODE_PERIOD         | .                    |
| 57       | KEYCODE_ALT_LEFT       |                      |
| 58       | KEYCODE_ALT_RIGHT      |                      |
| 59       | KEYCODE_SHIFT_LEFT     |                      |
| 60       | KEYCODE_SHIFT_RIGHT    |                      |
| 61       | KEYCODE_TAB            | Tab键                |
| 62       | KEYCODE_SPACE          | 空格键盘             |
| 63       | KEYCODE_SYM            |                      |
| 64       | KEYCODE_EXPLORER       | 资源管理器           |
| 65       | KEYCODE_ENVELOPE       |                      |
| 66       | KEYCODE_ENTER          | 回车                 |
| 67       | KEYCODE_DEL            | 删除、退格           |
| 68       | KEYCODE_GRAVE          | `                    |
| 69       | KEYCODE_MINUS          | -                    |
| 70       | KEYCODE_EQUALS         | =                    |
| 71       | KEYCODE_LEFT_BRACKET   | [                    |
| 72       | KEYCODE_RIGHT_BRACKET  | ]                    |
| 73       | KEYCODE_BACKSLASH      | \                    |
| 74       | KEYCODE_SEMICOLON      | ;                    |
| 75       | KEYCODE_APOSTROPHE     | '                    |
| 76       | KEYCODE_SLASH          | /                    |
| 77       | KEYCODE_AT             | @                    |
| 78       | KEYCODE_NUM            |                      |
| 79       | KEYCODE_HEADSETHOOK    |                      |
| 80       | KEYCODE_FOCUS          | 拍照对焦键           |
| 81       | KEYCODE_PLUS           |                      |
| 82       | KEYCODE_MENU           | menu菜单键           |
| 83       | KEYCODE_NOTIFICATION   | 通知键               |
| 84       | KEYCODE_SEARCH         | 搜索键               |
| 85       | KEYCODE_TAG_LAST       |                      |
| 91       | KEYCODE_MUTE           | 话筒静音键           |
| 92       | KEYCODE_PAGE_UP        | 向上翻页             |
| 93       | KEYCODE_PAGE_DOWN      | 向下翻页             |
| 95       | KEYCODE_SWITCH_CHARSET | 开关符号集(Emoji)    |
| 111      | KEYCODE_ESCAPE         | ESC键                |
| 112      | KEYCODE_FORWARD_DEL    | 删除键               |
| 115      | KEYCODE_CAPS_LOCK      | 大写锁定             |
| 116      | KEYCODE_SCROLL_LOCK    | 滚动锁定键           |
| 121      | KEYCODE_BREAK          | Break/Pause键        |
| 122      | KEYCODE_MOVE_HOME      | 光标移动到开始键     |
| 123      | KEYCODE_MOVE_END       | 光标移动到结尾键     |
| 124      | KEYCODE_INSERT         | 插入键               |
| 143      | KEYCODE_NUM_LOCK       | 小键盘锁             |
| 164      | KEYCODE_VOLUME_MUTE    | 扬声器静音键         |
| 168      | KEYCODE_ZOOM_IN        | 放大键               |
| 169      | KEYCODE_ZOOM_OUT       | 缩小键               |
| 187      | KEYCODE_APP_SWITCH     | 应用程序切换         |
| 223      | KEYCODE_SLEEP          | 睡眠键               |
| 224      | KEYCODE_WAKEUP         | 唤醒键，一般没用     |
| 276      | KEYCODE_SOFT_SLEEP     | 睡眠，除非持有唤醒锁 |
| 277      | KEYCODE_CUT            | 剪切                 |
| 278      | KEYCODE_COPY           | 复制                 |
| 279      | KEYCODE_PASTE          | 粘贴                 |
| 284      | KEYCODE_ALL_APPS       | 显示所有应用程序     |
|          | KEYCODE_ALT_LEFT       | Alt + Left           |
|          | KEYCODE_ALT_RIGHT      | Alt + Right          |
|          | KEYCODE_CTRL_LEFT      | Control + Left       |
|          | KEYCODE_CTRL_RIGHT     | Control + Right      |
|          | KEYCODE_SHIFT_LEFT     | Shift + Left         |
|          | KEYCODE_SHIFT_RIGHT    | Shift + Right        |

### 模拟触摸

想要知道需要触摸的具体位置，可以打开安卓的开发者模式，然后将按键坐标打开。

```shell
adb shell input tap 100 400	# 鼠标触控(100, 400)这个点
adb shell input swipe 10 10 200 200 # 从(10,10)滑动到(200, 200)
adb shell input touchscreen swipe 100 200 100 200 2000	# 在(100, 200)这个点持续按2000ms，应用一般会根据划屏的速度来移动不一样的距离
```

### 其他操作

#### 截图

```shell
adb shell /system/bin/screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png /tmp	# 将截图拷贝到宿主机的/tmp目录
```

#### 事件

```shell
adb shell getevent	# 监听触摸事件，但是只能监听用收点击屏幕，而不能监听用模拟器的事件
```

## ToubleShooting

- **java.lang.SecurityException: Injecting to another application requires INJECT_EVENTS permission**: 对于小米手机，除了打开USB 调试外，还要打开`USB调试（安全设置）`才允许进行操作
