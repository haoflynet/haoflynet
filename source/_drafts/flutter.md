## 安装使用
```shell
# 安装dart sdk
brew tap dart-lang/dart
brew install dart
brew info dart	# 获取dart sdk的安装位置

# 安装flutter：https://docs.flutter.dev/get-started/install/macos#system-requirements
flutter upgrade # 更新flutter SDK
fluter create my_app # 创建一个新项目，名字只能是小写，默认会生成web、android、ios、macos、windows、linux，如果不喜欢可以rm -rf 删除子目录即可

# 安装依赖
flutter doctor	# 查看还有什么依赖没有安装，如果提示sdkmanager没找到，可以在Android Studio -> Settings -> SDK Tools -> SDK Command-line Tools选中它即可
flutter pub get # 安装项目依赖性，同flutter packages get
flutter pub upgrade	# 更新依赖包
flutter pub cache	# 清除缓存
flutter pub deps	# 显示依赖

# 运行
flutter run -d Chrome
flutter run -d ios
flutter run -d emulator-5554 # 运行在指定的安卓设备

# dart命令
dart fix --dry-run # 运行代码诊断
```

## 开发



## 插件推荐

- flutter 插件目录: [pub.dev](https://pub.dev/)

### contentful_rich_text

- Contntful的富文本解析插件

### firebase-messaging

- 集成步骤可以参考[Firebase/Firestore 使用手册](https://haofly.net/firebase)和[Add Flutter push notifications with Firebase Cloud Messaging](https://blog.logrocket.com/add-flutter-push-notifications-firebase-cloud-messaging/)

### flutter_colorpicker

- 解析CSS颜色

### flutter_dotenv

- dotenv支持

### flutter_launcher_icons

- 使用步骤

```shell
dart run flutter_launcher_icons:generate	# 先生成配置文件，这会在根目录创建一个flutter_launcher_icons.yaml文件，然后主要修改image_path设置一下icon的路径即可
flutter pub get
dart run flutter_launcher_icons # 生成对应的icons
```

### flutter_widget_from_html

- flutter_html已经好久没更新了，用这个替代

### http

- 发送http请求

### [in_app_purchase](https://pub.dev/packages/in_app_purchase)

- 同时支持Google billing和Apple in app purchase的库，[官方集成配置文档](https://codelabs.developers.google.com/codelabs/flutter-in-app-purchases#0)

- Android

  - 必须先上传一个build到google play的closed testing(in review后几分钟就能变成Active，然后才能测试)，否则会报错`The item you were attempting to purchase could not be found.`

  - 需要在AndroidManifest.xml中的application标签中添加一个标签来指定billingclient的版本，否则虽然这个插件以来的是最新的版本，但是Google Play Console仍然提示错误: `Google Play Console will throw an error: Your app currently uses Play Billing Library version AIDL and must update to at least version 6.0.1 to make use of the latest monetization features on Google Play`， 具体的billingclient版本号可以查看in_app_purcahse的[changelog](https://github.com/flutter/packages/blob/main/packages/in_app_purchase/in_app_purchase_android/CHANGELOG.md)

    ```xml
    <application>
     ...
     <meta-data android:name="com.google.android.play.billingclient.version" android:value="6.2.0" />
    </application>
    ```
  
  
  - 如果报错`Unhandled Exception: PlatformException(channel-error, Unable to establish connection on channel., null)`，那么可以尝试重新执行一次 `flutter fun --verbose`
  
  
  - 如果`isAvailable`一直返回false，必须在你设备上的`google play`中登陆了才行
  

### path_provider

- 目录、路径相关处理

#### provider

- 状态管理

#### shared_preferences

- 状态管理 

### url_launcher

- 打开链接用

- 如果是安卓需要在AndroidManifest.xml中添加配置:
  ```xml
  <uses-permission android:name="android.permission.INTERNET" />
  
  <application>
    <queries>
      <Intent>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" />
      </intent>
    </queries>
  </application>
  ```

#### video_player / [chewie](https://github.com/fluttercommunity/chewie)

- 视频播放
- chewie用于显示进度条等控件

## TroubleShooting

- **HTTP Host Availability**: 如果`flutter doctor`出现这个错误，需要开启代理才行

- **Xcode出现 Module xxx not found**: 尝试执行:

  ```shell
  flutter clean && flutter pub get && flutter run
  cd ios && pod install
  ```

- **The plugin `flutter_webview_plugin` uses a deprecated version of the Android embedding**: 要么升级该插件，要么使用别人的分支:

  ```yaml
    flutter_webview_plugin:
      git: https://github.com/snoopdoggy322/flutter_webview_plugin
  ```


## 参考项目

- [flutter_twitter_clone](https://github.com/TheAlphamerc/flutter_twitter_clone)