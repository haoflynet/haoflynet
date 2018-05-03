---
title: "Swift开发MacOS应用"
date: 2016-12-10 12:05:30
updated: 2018-04-24 14:44:00
categories: swift
---

## 基本概念及程序框架

### 主要目录文件

`AppDelegate.swift`: 所有应用开始都有一个AppDelegate，是整个应用程序的一个代理。在应用启动的时候，最先被调用的就是这个AppDelegate中的`applicationDidFinishLaunching`方法，可以在这里做全局初始化，但一般为了保持代码的整洁，具体逻辑并不放在这里。

`Assets.xcasserts`:

`Main.storyboard`: 项目主要的UI文件

`Info.plist`: 项目的基础配置

`*.h`: 头文件。包含类，类型，函数和常量的声明

`*.m`: 源代码文件。可以有`Objective-C`和`C`和`Swift`代码

`*.mm`: 源代码文件。可以有`Objective-C/C/C++/Swift`

`*.cpp`: C++代码

## IB(Interface Builder)

### 组件

#### Labels and Text Field

#### Combo Boxes

#### Popup Buttons

#### Text Views

#### Sliders

#### Date Pickers

#### Buttons

#### Radio Buttons

#### Check Buttons

#### Image Views

### 定位

#### 居中定位

```swif
# 直接选择该Object右下角的Align的Horizontally in Container和Vertically in Container全部设置为0，然后选择Update Frame修改为Items of New Constraints，再点击Add 2 Constraints button.
```









widget也都可以通过代码来设置他们的属性，例如

在applicationDidFinishLaunching函数内部写上

label1.stringValue = "wanghao"
button1.title = "Change Text"
Toolbar 菜单栏
view controller，也就是最开始的那种storyboard
container view，这里应该是可以放其他的view，相当于网页里面的iframe
custom view
vertical Split view/horizontal split view :水平或者垂直分割的view
Collection view：就是将一些列的数据以表格的形式展（包含了Collecotion Item），datasource可以直接outlets到view controller
object：就是一个对象，它可以与类帮顶起来（右上角custom class进行定义），定义了过后，又可以将它与下面的view相联系(control＋拖曳，选择outlets)，
table view：表格

Array Controller：好像是管理一组controller

menu bar：


要连接两个view，也是control拖曳



这个地方可以添加绝对定位或者想对定位 ![绝对定位想对定位](../../../../Downloads/绝对定位想对定位.jpg)

右边那个按钮则是像html里面的margin



上面是Day 2:auto layout



创建新的类的时候也可以同时创建xib文件，上面的collection controller，如果要有一个复杂的item那么久需要自己创建一个类



menu bar

直接在appdelegate里面：要设置application is agent

```swi
let statusItem = NSStatusBar.systemStatusBar().statusItemWithLength(NSVariableStatusItemLength)
//let menu = NSMenu()
let popover = NSPopover()

func applicationDidFinishLaunching(...){
  if let button = statusItem.button {
    button.image = NSImage(named: "图片名称")// 在asets里面添加了的图片
  	//button.action = Selector("showWeatheraaa")
  	
  	button.actoin = Selector("toggleWeather:")
  }
  
  //menu.addItem(NSMenuItem(title: "直接加", action: Selector("showWeather:"), keyEquivalent:"S"))
  //menu.addItem(NSMEnuItem.separatorItem())
  //menu.addItem(NSMenuItem(title:"quit", action: Selector("terminate:"), keyEquivalent:"q"))
  
 // statusItem.menu = menu
 popover.contentViewController = 
}

func showWeather(sender: NSStatusBarButton){
  print("我靠")
}

func toogleWeather(sender: NSStatusBarButton){
  if popover.shown{
    popover.performClose(sender)
  }else{
    if let button = statusItem.button {
      popover.shownRelativeToRect(button.bounds, ofView: button, perferredEdge: .MinY)
    }
  }
}
```

新建了NSOBbject过后，要让它MainMenu .xib加载的时候久被加载，需要把它以object的形式添加到XIB中去

而这个object的Outlets就是相对应的view，比如Status Menu

同理如果创建的是一个NSview，那么一个view泽可以与之关联