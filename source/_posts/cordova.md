---
title: "Cordova 开发手册"
date: 2021-04-29 08:02:30
updated: 2021-08-13 08:48:00
categories: javascript
---

## 基本命令

- `npm install -g cordova `
- 如果要运行在`xcode`需要用`xcode`打开`项目名.xcworkspace`文件

```shell
# 创建工程
cordova create 目录名 com.haofly.mobile 应用名

# 平台管理
cordova platform add ios
cordova platform add android
cordova platform list	# 列出当前添加了的平台
cordova platform rm android

# 编译运行，如果更新了www目录，可以直接重新build即可
cordova build	# 编译所有平台
cordova build android	# 仅编译指定平台，这条命令相当于cordova prepare android && codova compile android
cordova emulate ios	# 启动模拟器
cordova run browser	# 在指定平台运行

# 插件管理
cordova prepare	# 复制assets中的文件到平台中去
cordova requirements # 检查依赖关系
cordova plugin search facebook	# 搜索插件
cordova plugin ls	# 列出当前已安装的插件
cordova plugin rm cordova-plugin-facebook4	# 移除插件
cordova plugin add cordova-plugin-facebook4 # 添加插件
corodva plugin add https://github.com/myproject#branch_name	# 从github安装指定分支的cordova插件
```

<!--more-->

## 目录结构

- 编译后`*-Info.plist`在`Resources`目录下

- 如果要添加配置到`*-Info.plist`文件里可以在`config.xml`里面的`platform ios`添加，不过添加完成后需要重新`cordova platform remove ios && cordova platform add ios`，否则可能出现错误**doc.find is not a function**

  ```xml
  <platform name="ios">
    <!--下面这个配置可以避免NSURLConnection finished with error - code -1004问题-->
    <edit-config file="*-Info.plist" mode="merge" target="NSAppTransportSecurity">
      <dict>
        <key>NSAllowsArbitraryLoadsInWebContent</key>
        <true/>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
      </dict>
    </edit-config>
  </platform>
  ```

## 使用Vue作前端

### VUE配置步骤

1. 初始化一个`vue`工程，`vue init webpack project-name`

2. 在`vue/index.html`的`head`中添加内容:

   ```html
   <meta http-equiv=”Content-Security-Policy” content="default-src ‘self’ data: gap: https://ssl.gstatic.com ‘unsafe-eval’; style-src ‘self’ ‘unsafe-inline’; media-src *; img-src ‘self’ data: content:; connect-src ‘self’ ws:;">
   
   <script type="text/javascript" src="cordova.js"></script>
   ```

3. 修改build配置，在`config/index.js`中修改如下配置

   ```javascript
   build: {
     index: path.resolve(__dirname, ‘../www/index.html’),	// 指向cordova的www目录
     assetsRoot: path.resolve(__dirname, ‘../www’),
   }
   ```

## 依赖管理Pod

- 转为iOS工程提供的第三方库的依赖管理工具
- **如果发现执行这些命令后仍然缺少依赖，可以去看看fetch.json文件里面有没有缺失那个包，如果缺失了尝试删除fetch.json文件再次安装npm包和pod包试试**

```shell
sudo sudo	# 安装pod管理工具

pod search xxx	# 查找第三方库
cd platforms/ios && pod repo update && pod install	# cordova项目安装第三方库依赖
```

## 移动端常用配置

### 添加App logo

#### Android

- 在`resources`目录中添加logo文件`resources/logo.png`
- 只需要在`config.xml`中添加`<icon src="resources/logo.png" platform="android" width="57" height="57" density="mdpi"/>`即可(与`name`同一级)

#### Ios

- 首先需要生成各个尺寸的logo图片，否则没有的就不会展示自定义的icon，可以在[App Icon Generator](https://appicon.co/)生成对应平台的所有尺寸图片，它会生成一个针对XCode的压缩包，我们可以将所有的图片提取到`resources/ios`目录下

- 在`config.xml`的ios配置中添加如下的icon属性

  ```xml
  <platform name="ios">
      <icon src="resources/ios/180.png" width="180" height="180"/>
      <icon src="resources/ios/20.png" width="20" height="20"/>
      <icon src="resources/ios/60.png" width="60" height="60"/>
      <icon src="resources/ios/120.png" width="120" height="120"/>
      <icon src="resources/ios/76.png" width="76" height="76"/>
      <icon src="resources/ios/152.png" width="152" height="152"/>
      <icon src="resources/ios/40.png" width="40" height="40"/>
      <icon src="resources/ios/80.png" width="80" height="80"/>
      <icon src="resources/ios/57.png" width="57" height="57"/>
      <icon src="resources/ios/114.png" width="114" height="114"/>
      <icon src="resources/ios/72.png" width="72" height="72"/>
      <icon src="resources/ios/144.png" width="144" height="144"/>
      <icon src="resources/ios/167.png" width="167" height="167"/>
      <icon src="resources/ios/29.png" width="29" height="29"/>
      <icon src="resources/ios/58.png" width="58" height="58"/>
      <icon src="resources/ios/87.png" width="87" height="87"/>
      <icon src="resources/ios/50.png" width="50" height="50"/>
      <icon src="resources/ios/100.png" width="100" height="100"/>
      <icon src="resources/ios/167.png" width="167" height="167"/>
      <icon src="resources/ios/1024.png" width="1024" height="1024"/>
  </platform>
  ```

- 然后`cordova prepare`后打开Xcode，在左侧目录`项目名->Resources->Images.xcassets->AppIcon`可以看到我们所有的图标，然后选中整个AppIcon框后，右侧可以勾选对应的平台，选择了后就可以把对应的图片拖到对应尺寸的框里，如果有重复的，可以直接`Cmd + C`进行复制，不能用鼠标复制。需要保证所有的框都装了icon并且没有感叹号

### 异形屏处理

- 现在流行水滴屏、刘海屏、曲面屏、瀑布屏或者其他的异形屏，可能会造成屏幕上下左右出现不规则的区域(或者多出来一块、white bar)

- 我们需要在`App.vue`中添加一个全局的padding使我们的内容全都在中间，目前有四个参数来分别代表上下左右四个地方的安全区域距离边界的距离

  ```javascript
  // 首先需要修改index.html中的viewport，添加vieport-fit=cover
  <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no, viewport-fit=cover">
    
  // 然后需要将app的样式修改一下，将页面主体限定在安全区域内
  #app {
      height:100vh;
      width:100vw;
      padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
  }
  ```

- 如果有`position:absolute; bottom:0`这样的absolute/fixed组件，建议在不同屏幕上看一下，可能需要改为`bottom:env(safe-area-inset-bototm)`，否则可能仍然会跑到异形的地方去(注意背景色的不同)

## 常用插件推荐

### [branch-cordova-sdk](https://github.com/BranchMetrics/cordova-ionic-phonegap-branch-deep-linking-attribution)

- deeplink插件
- [官方集成文档](https://help.branch.io/developers-hub/docs/cordova-phonegap-ionic)
- 如果配置成功后依然不work，可能需要重新`cordova build ios`一下
- 默认情况下，在桌面打开分享地址会是发送SMS的页面，可以在branch后台设置里面的Desktop Redirects中修改的，一种是`Branch-hosted SMS Landing Page`(发送SMS，但是这个发送SMS必须发邮件给他们才会给你开通，否则会报错This app is blocked from sending SMS messages)，一种是`Custom Landing Page`

### [cordova-plugin-console](https://www.npmjs.com/package/cordova-plugin-console)

- 只有很老的版本才需要了，现在可以直接使用`console.log`进行日志的输出，需要注意的是，必须先引入`cordova.js`才行，否则依然无法看到日志输出

### [cordova-plugin-device](https://cordova.apache.org/docs/en/latest/reference/cordova-plugin-device/index.html)

获取平台设备信息

### [cordova-plugin-facebook-connect](https://github.com/cordova-plugin-facebook-connect/cordova-plugin-facebook-connect)

- Facebook登陆插件，安装完成后得去`platforms/ios`目录执行一下`pod repo update && pod install`安装facebook SDK，这样使用:

- 需要注意的是，如果获取不到邮箱地址，可能的原因是邮箱没有认证
- `test user`如果出现`There was a problem logging you in.`错误，不知道为啥，尝试换成添加真实用户为测试用户试试

```javascript
window.facebookConnectPlugin.login(['public_profile', 'email'], userData => {
  const authData = {
    access_token: userData.authResponse.accessToken
  };

  const userId = userData.authResponse.userID;

  window.facebookConnectPlugin.api(`${userId}/?fields=first_name,last_name,email`, null, result => {
    authData.first_name = result.first_name;
    authData.last_name = result.last_name;
    authData.email = result.email;
    resolve(authData);
  },
  error => {
    reject('error getting facebook user info' + error);
  });
},
error => {
  reject('error authenticating with facebook' + error);
});
```

### [cordova-plugin-firebasex](https://github.com/dpa99c/cordova-plugin-firebasex)

firebase插件，包含(cloud messaging等多个firebase的功能)，**如果对firebase的证书配置还不熟悉，可以现在其[example项目](https://github.com/dpa99c/cordova-plugin-firebasex-test)上进行测试，它的example里还有命令行工具，不过它打印的错误信息不够详细，还是用firebase-admin-node好一点，具体的使用方式和证书等配置可以在[firebase手册](https://haofly.net/firebase)中查看**

### [cordova-plugin-geolocation](https://github.com/apache/cordova-plugin-geolocation)

- 如果xcode里面有warning: `No NSLocationAlwaysUsageDescription or NSLocationWhenInUseUsageDescription key is defined in the Info.plist file.`表示没有正确配置`NSLocationWhenInUseUsageDescription`选项

- 下面是两种获取地理信息的声明，需要选择一种在`config.xml`中添加，添加完后记得重新编译(可能需要remove ios再添加才行):

  ```xml
  <edit-config target="NSLocationWhenInUseUsageDescription" file="*-Info.plist" mode="merge">
      <string>need location access to find things nearby</string>
  </edit-config>
  
  <edit-config target="NSLocationAlwaysAndWhenInUseUsageDescription" file="*-Info.plist" mode="merge">
      <string>need location access to find things nearby</string>
  </edit-config>
  ```

### [cordova-plugin-googleplus](https://github.com/EddyVerbruggen/cordova-plugin-googleplus)

Google登陆插件，只不过需要获取很多的账号相关的信息，实际的登陆只需要下面这样做即可。

- `REVERSED_CLIENT_ID`需要在`firebase`的`Project settings`的app中获取，需要下载`GoogleService-Info.plist`，包含在里面的。安装完成后需要确保`REVERSED_CLIENT_ID`被加入到`XCode`中的`Resources/项目名-Info.plist`中的`URL types`中，其中`URL-identifier=REVERSED_CLIENT_ID`，`URL Schemes[0]=com.googleusercontent.apps.xxxxxxx` ，如果没有可以手动添加: ![](https://haofly.net/uploads/cordova_01.png)
- `WEB_APPLICATION_CLIENT_ID`可以在`firebase`里新建一个`web app`取其ID或者直接在上面的`GoogleService-Info.plist`取`GOOGLE_APP_ID`
- `Android`端的`webClientId`参数则是`firebase`的`android app`的`google-services.json`中的`client.oauth_client.client_id`

```javascript
window.plugins.googleplus.isAvailable(avail => {
  if (avail) {
    let params = Platform.isIos() ? {} : {
    	scopes: 'profile email openid',
      webClientId: config.GOOGLE_PLUS_WEB_CLIENT_ID,
      offline: true
    };

    window.plugins.googleplus.login(params, authData => {
      resolve({
        first_name: authData.givenName,
        last_name: authData.familyName,
        email: authData.email,
        access_token: authData.accessToken,
        id_token: authData.idToken
      });
    },
    error => {
      reject('error authenticating with google' + error);
    });
  }
  else {
    reject('google auth not available');
  }
});
```

### [cordova-plugin-qrscanner](https://github.com/haoflynet/cordova-plugin-qrscanner)

 `inoic`[官方推荐](https://ionicframework.com/docs/native/qr-scanner)的一个二维码扫描插件，不过也没找到更好的了，我给改了bug。它默认是全屏的，如果要更改为局部扫描，我觉得得修改源代码，不直接取`body`。还有一个问题是推出扫描时，背景颜色居然没有改过来，我在js代码里改的，所以我是这样用的：

```javascript
mounted() {
 	this.originalBackgroundColor = getComputedStyle(document.getElementsByTagName('body')[0])['background-color'];
  window.QRScanner.scan(displayContents);
  
  function displayContents(err, text) {
  	if (err) {
    		console.log('displayContents, err=', err);
    }
    else {
        if (new Date().getTime() - self.enterTimestamp < 3000) {	// 这里是为了延迟一下，不然扫描实在太快了
          window.QRScanner.scan(displayContents);
        } else {
          console.log('text=' + text);
          self.close(text);
        }
      }
  }
  
  window.QRScanner.show(status => {
      console.log('show scan camera', JSON.stringify(status));
  });
}

close(text) {
  if (typeof text === 'object') {
    text = '';
  }
  const self = this;
  window.QRScanner.destroy(() => {
    self.$navStack.push({name: 'Scan', query: {result: text}});
  });
}

deactivated() {
  document.body.style.backgroundColor = this.originalBackgroundColor;	// 恢复背景色
},

beforeDestroy() {
  document.body.style.backgroundColor = this.originalBackgroundColor;	// 恢复背景色
},

destroyed() {
  document.body.style.backgroundColor = this.originalBackgroundColor;	// 恢复背景色
}
```

### [cordova-plugin-sign-in-with-apple](https://github.com/twogate/cordova-plugin-sign-in-with-apple#readme)

Apple ID登陆插件，需要在apple开发者后台给指定Bundle ID添加`Sign In with Apple`权限，使用同样非常简单，如果要获取email可以使用`jwt-decode`去

```javascript
window.cordova.plugins.SignInWithApple.signin(
  { requestedScopes: [0, 1] },
  result => {
    console.log(result);
		console.log(jwt_decode(result.identityToken));	// 获取email
    alert(JSON.stringify(result));
  },
  error => {
    console.error(error);
    console.log(JSON.stringify(error));
  }
);
```

### [cordova-plugin-splashscreen](https://github.com/apache/cordova-plugin-splashscreen)

启动屏配置插件

## 插件开发Tips

- 我不开发插件，但是很多很小众的插件，经常需要我们修改一下，所以还是需要学习一点插件开发的知识

### IOS开发常用流程

- 方法定义: 需要在`src/ios/*.h`中这样定义:

  ```objective-c
  #import <Cordova/CDV.h>
  
  @interface CordovaAppleMusic : CDVPlugin
  
  - (void) requestToken:(CDVInvokedUrlCommand*)command;
  - (void) requestAuthorization:(CDVInvokedUrlCommand*)command;
  
  @end
  ```

- 方法实现，需要在`src/ios/*.m`中实现

  ```objective-c
  // 此方法来自于CordovaAppleMusic Plugin，是使用OC写的
  - (void)requestToken:(CDVInvokedUrlCommand*)command
  {
      NSString* callbackId = [command callbackId];
      NSString* developerToken = [[command arguments] objectAtIndex:0];	// 如果方法有参数可以这样获取参数
      SKCloudServiceController *serviceController = [[SKCloudServiceController alloc] init];
      [serviceController requestUserTokenForDeveloperToken:developerToken completionHandler:^(NSString * _Nullable userToken, NSError * _Nullable error) {
        if (error != nil) {
          NSLog(@"userToken_Error :%@", error);
          // 返回正确响应
          CDVPluginResult* result = [CDVPluginResult resultWithStatus:CDVCommandStatus_ERROR messageAsString:error.description];
          [self.commandDelegate sendPluginResult:result callbackId:callbackId];
        }
        else{
          // 返回错误响应
          CDVPluginResult* result  = [CDVPluginResult resultWithStatus:CDVCommandStatus_OK messageAsString:userToken];
          [self.commandDelegate sendPluginResult:result callbackId:callbackId];
        }
      }];
}
  ```

- 最后在`www/*.js`中暴露方法给JS

  ```javascript
  var exec = require('cordova/exec');
  module.exports = {
    requestAuthorization: function (successCallback, errorCallback) {	// 无参数的方法
        exec(successCallback, errorCallback, "AppleMusic", "requestAuthorization", []);
    },
    requestToken: function (developerToken, successCallback, errorCallback) {	// 带参数的方法
      exec(successCallback, errorCallback, "AppleMusic", "requestToken", [developerToken]);
    },
  }
  ```

## TroubleShooting

- **应用启动一直白屏**: 网上有很多解决方法，都试过，我最后的解决方法是把系统语言切换成英文解决了

- **pod: Command failed with exit code 31**: 尝试执行一下`pod repo update`，如果是`Apple Silicon`，那么需要使用`arch -x86_64 zsh`

- 删除`node_module`可以解决的一些问题:
  - **Cannot find module './elementtree'**
  
- **Current working directory is not a Cordova-based project.**: 可能是`www`目录不见了

- **new Date('2020-04-29 00:00:00')输出Invalid Date**: 目前我个人只在ios上复现过，vue直接运行没问题，但是真机上却是`Invalid Date`，用moment代替吧

- **'GoogleService-Info.plist' was not found in your Cordova project root folder**: 如果是这样，首先检查是否有该文件，如果确实有还是报错，那么可以在`XCode`中手动添加，右键项目的`Resource->Add Files to "项目名"`选择`GoogleService-Info.plist`即可

  

