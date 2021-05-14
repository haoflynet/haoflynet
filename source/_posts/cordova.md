---
title: "Cordova 开发手册"
date: 2021-04-29 08:02:30
updated: 2021-05-07 08:48:00
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

```shell
sudo sudo	# 安装pod管理工具

pod search xxx	# 查找第三方库
cd platforms/ios && pod repo update && pod install	# cordova项目安装第三方库依赖
```

## 常用插件推荐

- [cordova-plugin-console](https://www.npmjs.com/package/cordova-plugin-console): 只有很老的版本才需要了，现在可以直接使用`console.log`进行日志的输出，需要注意的是，必须先引入`cordova.js`才行，否则依然无法看到日志输出

- [cordova-plugin-device](https://cordova.apache.org/docs/en/latest/reference/cordova-plugin-device/index.html): 获取平台设备信息

- [cordova-plugin-facebook-connect](https://github.com/cordova-plugin-facebook-connect/cordova-plugin-facebook-connect): Facebook登陆插件，安装完成后得去`platforms/ios`目录执行一下`pod repo update && pod install`安装facebook SDK，这样使用:

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

- [cordova-plugin-googleplus](https://github.com/EddyVerbruggen/cordova-plugin-googleplus): Google登陆插件，只不过需要获取很多的账号相关的信息，实际的登陆只需要这样做即可:

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

- [cordova-plugin-qrscanner](https://github.com/haoflynet/cordova-plugin-qrscanner): `inoic`[官方推荐](https://ionicframework.com/docs/native/qr-scanner)的一个二维码扫描插件，不过也没找到更好的了，我给改了bug。它默认是全屏的，如果要更改为局部扫描，我觉得得修改源代码，不直接取`body`。还有一个问题是推出扫描时，背景颜色居然没有改过来，我在js代码里改的，所以我是这样用的：

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

- [cordova-plugin-sign-in-with-apple](https://github.com/twogate/cordova-plugin-sign-in-with-apple#readme): Apple ID登陆插件，需要在apple开发者后台给指定Bundle ID添加`Sign In with Apple`权限，使用同样非常简单，如果要获取email可以使用`jwt-decode`去

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

  

