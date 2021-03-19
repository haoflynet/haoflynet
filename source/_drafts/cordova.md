cordova

`npm install -g cordova `

## 基本命令

```shell
# 平台管理
cordova platform add ios
cordova platform add android
cordova platform list	# 列出当前添加了的平台
cordova platform rm android

# 编译运行，如果更新了www目录，可以直接重新build即可
cordova build	# 编译所有平台
cordova build android	# 仅编译指定平台，这条命令相当于cordova prepare android && codova compile android
cordova emulate ios	# 启动模拟器

# 插件管理
cordova plugin search facebook	# 搜索插件
cordova plugin ls	# 列出当前已安装的插件
cordova plugin rm cordova-plugin-facebook4	# 移除插件
cordova plugin add cordova-plugin-facebook4 # 添加插件
corodva plugin add https://git.github.com/myproject#branch_name	# 从github安装指定分支的cordova插件
```

<!--more-->

## 依赖管理Pod

- 转为iOS工程提供的第三方库的依赖管理工具

```shell
sudo sudo	# 安装pod管理工具

pod search xxx	# 查找第三方库
cd platforms/ios && pod repo update && pod install	# cordova项目安装第三方库依赖
```

## 常用插件推荐

- [cordova-plugin-facebook-connect](https://github.com/cordova-plugin-facebook-connect/cordova-plugin-facebook-connect): Facebook登陆插件，安装完成后得去`platforms/ios`目录执行一下`pod repo update && pod install`安装facebook SDK，这样使用:

  ```javascript
  window.facebookConnectPlugin.login(['public_profile'], userData => {
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

- [cordova-plugin-sign-in-with-apple](https://github.com/twogate/cordova-plugin-sign-in-with-apple#readme): Apple ID登陆插件，需要在apple开发者后台给指定Bundle ID添加`Sign In with Apple`权限，使用同样非常简单:

  ```javascript
  window.cordova.plugins.SignInWithApple.signin(
    { requestedScopes: [0, 1] },
    result => {
      console.log(result);
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
