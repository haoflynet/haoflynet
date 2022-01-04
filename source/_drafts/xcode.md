---
title: "Xcode / iOS开发手册"
date: 2018-06-05 21:32:00
updated: 2021-12-31 09:36
categories: Mac
---

## [Apple设计资源](https://developer.apple.com/design/resources/)

## 图标

App需要提供图标的规格为`40/588/60/80/87/120/160/180/1024`，另外，如果最好是将png图片转换为jpg，因为默认会把png不存在的地方背景设置为黑色。准备好图标素材以后，直接在`xcode`里面的`Images.xcassets`将图标拖入即可。

## App 上架流程

1. 注册开发者账号
2. 在[App Store Connect](https://appstoreconnect.apple.com/)新建一个APP
3. 从Xcode上传APP至App Store Connect
   1. 导入P12文件(我操作的时候是别人直接发给我的，所以这里就没记录步骤了，应该可以[参考这里](https://ask.dcloud.net.cn/article/152))，有一点需要注意的时候，双击P12文件安装成功后，还需要在keychain里点击其`private key`，修改`Access Control`，需要修改配置`Allow all applications to access this item`，否则下面在上传的时候会提示`missing private key`或者让你无限输入电脑用户名密码的问题
   2. 点击`Product->Archive`，完成后会自动弹出一个对话框(当然，这个对话框也可以通过`Window->Organizer`打开，要选择对应的APP)
   3. 选择`Distribute App`，然后选择`App Store Connect`，再`Upload`，一直下一步应该就可以了。(如果打包能成功，但是上传却说认证失败，可能是网络问题)
   4.  上传完成后可以在`App Store Connect`后台的`TestFlight`看到刚才的build了，这时候可以去添加测试用户，点击左侧菜单`App Store Connect User`进行添加，添加方式见页面提示即可，很简单，添加完成后会发送邮件给用户，里面有个兑换码，在ios的testflightapp上点击redeem输入兑换码即可下载，如果下载时提示`the app couldn't be installed because testflight isn't available`，那就等大概五分钟试试

## App 迁移transfer

- 迁移的条件: https://help.apple.com/app-store-connect/#/devaf27784ff，特别注意必须上架过一个版本才能够直接transfer
- 迁移APP的时候bundle id能一并迁移过去，还是方便

## 删除APP

- 如果删除为提交过的app，那么它仍然会出现在列表中，非常烦，只能等半年后她自己清理了

## TroubleShooting

- **Signing for "xxx" requires a development team. Select a development team in the project editor.**解决方法: 点击项目名->targets->General->Signing，选择自己的Team，选择后重新构建，如果仍然出现该错误，那么可以重启一下xcode或者更新一下xcode多次尝试。
- **打包archive的时候签名报错XXX is automatically signed for development, but a conflicting code signing identity iPhone Distribution has been manually specified. Set the code signing identity value to "Apple Development" in the build settings editor, or switch to manual signing in the Signing & Capabilities editor.**：需要去`PROJECT -> BUILD SETTINGS -> COMBINED`中的`Signing->Code Signing Identity`的值从`iOS Developer`修改为`Apple Development`，还有`TARGETS -> Build Settings -> Combined`中的`Signing->Code Signing Identity->Release`的值从`iOS Developer`修改为Apple `Development`
- **上传archive最后提示Missing private key**
- **Run on device突然报错Errors were encountered while preparing your device for development. Please check the Devices and Simulators Window.**: 重启手机试试吧
- **"XXXX" has 2 Apple Distribution certificates but their private keys are not installed. Contact the creator of one of these certificates to get a copy of the private key**: 可能是key过期了，去apple developer重新生成一个证书吧，下载下来安装上，但是得重启一下`xcode`
- **push app 到appstore一直在processing**: 这个时候确实可以再push一个新版本，可能会更快
- **ios模拟弱网环境**: 设置->开发者选项-> Network LINK CONDITIONER
