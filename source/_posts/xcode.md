---
title: "Xcode / iOS开发手册"
date: 2022-09-16 08:32:00
updated: 2025-05-05 23:57:00
categories: Mac
---

[open-source-ios-apps](https://github.com/dkhamsing/open-source-ios-apps?tab=readme-ov-file#apple-vision): 无论开发什么类型的iOS，刚上手的时候都可以参考这里的example project

## Xcode常用操作

### 模拟器打开keyboard键盘

- 默认是不会弹出键盘的，直接用电脑的键盘进行输入，但是有时候想要调试一下键盘弹出的效果，可以点击顶部菜单`I/O -> Keyboard -> Toggle Software Keyboard`

### 构建hook

- Pre-action和Post-actions，在顶部中间scheme中选择`Edit Scheme`，然后选择Build的`Pre-actions`，即可输入script，另外如果要获取当前的工程目录，可以使用`${PROJECT_DIR}`，但是Provide build settings from需要选择当前的Target

### IAP内购测试

- 需要在App Store Connect后台添加Sandbox Test Accounts
- 只能在真机测试，Settings -> App Store -> SANDBOX ACCOUNT登陆上面创建的account

### TestFlight测试

- 点击XCode -> Product -> Archive创建Archive后点击Distribute App按钮，然后选择TestFlight Internal Only，然后Distibute确定

### 支持构建多个不同的APP

- 例如给开发和测试环境构建不同的APP

1. 首先在XCode中的TARGETS选择当前的TARGET，右键Duplicate

2. 点击顶部中间的Scheme，编辑新的Scheme，可以在新的Scheme的Build Pre-action中通过脚本来自动修改环境变量

3. 选择当前Target，在`Signing & Capabilities`，修改`Bundle Identifier`，这样才能生成不同的APP

4. 修改Info中的Bundle display name，即APP的名称

5. 为了防止pod install的时候仅更新默认的target，其他的target的build phrases被破坏，需要在podfile里面添加配置
   ```shell
   # 下面配置仅针对 flutter，其他的项目，可以根据当前的podfile内容，复制出多个target
   target 'Runner' do
     use_frameworks!
     use_modular_headers!
   
     flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
     target 'RunnerTests' do
       inherit! :search_paths
     end
   end
   
   # 有多个target就写多个target
   target '{TARGET_NAME}' do
     use_frameworks!
     use_modular_headers!
   
     flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
   end
   ```

6. 要运行不同的APP的时候只需要切换顶部中间的schemes即可

### 代码折叠功能

- 这种功能居然不是默认打开的，设置方法： XCode -> Settings -> Text Editing -> 勾选Code folding ribbon

### 格式化代码

- 菜单 -> Editor -> Structure -> Format

## [Apple设计资源](https://developer.apple.com/design/resources/)

## 图标

- [App Icon Generator](https://appicon.co/#app-icon): iOS或者android各种尺寸图标一键生成，生成后直接拖到xcode即可

App需要提供图标的规格为`40/588/60/80/87/120/160/180/1024`，另外，如果最好是将png图片转换为jpg，因为默认会把png不存在的地方背景设置为黑色。准备好图标素材以后，直接在`xcode`里面的`Images.xcassets`将图标拖入即可。

## App 上架流程

1. 注册开发者账号
2. 在[App Store Connect](https://appstoreconnect.apple.com/)新建一个APP
3. 从Xcode上传APP至App Store Connect
   1. 下载P12文件(申请发布(Distribution)证书)
   1. 导入P12文件(我操作的时候是别人直接发给我的，所以这里就没记录步骤了，应该可以[参考这里](https://ask.dcloud.net.cn/article/152))，有一点需要注意的时候，双击P12文件安装成功后，还需要在keychain里点击其`private key`，修改`Access Control`，需要修改配置`Allow all applications to access this item`，否则下面在上传的时候会提示`missing private key`或者让你无限输入电脑用户名密码的问题
   2. 点击`Product->Archive`，完成后会自动弹出一个对话框(当然，这个对话框也可以通过`Window->Organizer`打开，要选择对应的APP)
   3. 选择`Distribute App`，然后选择`App Store Connect`，再`Upload`，一直下一步应该就可以了。(如果打包能成功，但是上传却说认证失败，可能是网络问题)
   4.  上传完成后可以在`App Store Connect`后台的`TestFlight`看到刚才的build了，这时候可以去添加测试用户，点击左侧菜单`App Store Connect User`进行添加，添加方式见页面提示即可，很简单，添加完成后会发送邮件给用户，里面有个兑换码，在ios的testflightapp上点击redeem输入兑换码即可下载，如果下载时提示`the app couldn't be installed because testflight isn't available`，那就等大概五分钟试试

<!--more-->

## App 迁移transfer

- 迁移的条件: https://help.apple.com/app-store-connect/#/devaf27784ff，特别注意必须上架过一个版本才能够直接transfer
- 迁移APP的时候bundle id能一并迁移过去，还是方便

## 删除APP

- 如果删除为提交过的app，那么它仍然会出现在列表中，非常烦，只能等半年后她自己清理了

## Cocoapods/pod

- 升级pod

  ```shell
  pod --version	# 查看pod版本
  sudo gem install cocoapods	# 升级版本
  
  # 清理并重新安装以来
  rm -rf ~/Library/Caches/CocoaPods; 
  rm -rf Pods; 
  rm -rf ~/Library/Developer/Xcode/DerivedData/*; 
  pod deintegrate; 
  pod setup; 
  pod install;
  ```

## Vision APP开发

- [awesome-visionOS](https://github.com/tomkrikorian/awesome-visionOS?tab=readme-ov-file#swiftui)
- [visionOS App Icon Web Preview](https://gnikoloff.github.io/visionos-web-app-icon-maker/): 在线制作和预览vision app的图标

#### 打开预览功能

- Editor -> Canvas选中即可

#### 组件

##### 通用属性

```swift
.hoverEffect()	// 自动响应hover效果
.hoverEffectDisabled() // 禁止响应hover效果
.contentShape(RoundedRectangle(cornerSize: CGSizeMake(20, 20))).hoverEffect() // hover效果默认没有圆角，可以这样设置hover的圆角，但是一定要在hoverEffect前面设置
```

##### VStack、HStack、ZStack

- V代表垂直，H代表从左到右，Z代表从背景到前景

##### TabView

- 就是左侧的tab切换组件，默认是图标，鼠标hover的时候会显示文字
- https://www.rudrank.com/exploring-visionos-tabview/

## TroubleShooting

- **Signing for "xxx" requires a development team. Select a development team in the project editor.**解决方法: 点击项目名->targets->General->Signing，选择自己的Team，选择后重新构建，如果仍然出现该错误，那么可以重启一下xcode或者更新一下xcode多次尝试。

- **打包archive的时候签名报错XXX is automatically signed for development, but a conflicting code signing identity iPhone Distribution has been manually specified. Set the code signing identity value to "Apple Development" in the build settings editor, or switch to manual signing in the Signing & Capabilities editor.**：需要去`PROJECT -> BUILD SETTINGS -> COMBINED`中的`Signing->Code Signing Identity`的值从`iOS Developer`修改为`Apple Development`，还有`TARGETS -> Build Settings -> Combined`中的`Signing->Code Signing Identity->Release`的值从`iOS Developer`修改为Apple `Development`

- **上传archive最后提示Missing private key**

- **Run on device突然报错Errors were encountered while preparing your device for development. Please check the Devices and Simulators Window.**: 重启手机试试吧

- **"XXXX" has 2 Apple Distribution certificates but their private keys are not installed. Contact the creator of one of these certificates to get a copy of the private key**: 可能是key过期了，去apple developer重新生成一个证书吧，下载下来安装上，但是得重启一下`xcode`

- **push app 到appstore一直在processing**: 这个时候确实可以再push一个新版本，可能会更快

- **ios模拟弱网环境**: 设置->开发者选项-> Network LINK CONDITIONER

- **set the code signing identity value to apple development in the build settings editor**: 在`TARGETS -> Build Settings -> All`中搜索`signing` 即可，修改对应的值为`apple development`即可

- **sandbox账户无法登录，提示要进入设置收验证码**: 无论怎样我都收不到验证码， 最后重新建了一个sandbox账户就可以了，sandbox在点击登录按钮登录的时候按理说是不用验证码的，直接就可以登录了。当然，必须得退出本机自身的apple id才行

- **Sandbox沙盒账户在app store中输入密码登陆后无响应，无法登陆**: 尝试在Settings -> App Store中的SANDBOX ACCOUNT中进行登陆

- **添加了测试设备后，Xcode依然无法安装**: 可能是因为Xcode没有及时更新云端的`Provisioning Profile`可以删除目录`~/Library/MobileDevice/Provisioning`，然后打包时候勾选`Automatically manage signing`，Xcode就会重新拉取了

- **python: No such file or directory**: 尝试执行

  ```shell
  # 安装python
  brew install pyenv
  pyenv install 2.7.18
  
  ln -s /opt/local/bin/python2.7 /usr/local/bin/python
  ln -s /opt/local/bin/python2.7 /usr/local/bin/python2
  ```
  
- **Flutter failed to write to a file at ...**: 搜索`ENABLE_USER_SCRIPT_SANDBOXING`配置，将其设置为disabled

- **NSURLConnection SSL error**: 通常只需要在`Info.plist`中添加

  ```shell
  <key>NSAppTransportSecurity</key>
  <dict>
  	<key>NSAllowsArbitraryLoads</key>
  	<true/>
  </dict>
  ```

## 扩展阅读

- [iOS证书(.p12)和描述文件(.mobileprovision)申请](https://ask.dcloud.net.cn/article/152)：关于证书申请的非常详细的一篇文章
