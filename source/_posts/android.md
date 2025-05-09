---
title: "Android开发手册"
date: 2015-03-18 09:12:39
updated: 2024-11-05 15:37:00
categories: system
---
## [Android API Levels版本](https://apilevels.com/)

## Android Studio 的使用

### [Gradle和Gradle Plugin对应关系](https://developer.android.com/studio/releases/gradle-plugin)

### 生成APK/ABB文件

- 生成APK文件: `Build -> Build Bundles/APK(s) -> Build APK(s)`

- 生成能上传到google playstore的签名了的bundle文件(.abb格式)

  - `Build -> Generate Signed Bundle/APK`，生成的时候记得勾选`Export encrypted key for enrolling published apps in Google Play App Signing`(导出的key的格式是pepk)

  - 如果是第一次上传，可以点击`Create new`生成一个新的keystore文件(一般会以.keystore或者.jks结尾)

  - 一个keystore可能包含多个alias的key，可以多次点击`Create new`来生成即可

  - 如果之前没有上传过google play console，那么在console里面直接新建一个release即可，不用先上传key这些

  - 如果之前已经上传了**upload key certificate**到google play console里面，那么必须用之前的来生成才行，否则上传会提示SHA-1指纹不一致。可以在后台查看`Setup -> App Integrity -> Upload key certificate`看是否有了，注意这里的`Download certificate`只是下载公钥，没啥用的。

  - 如果已经有上传证书并且丢失了的话，只能联系google重新生成一个了(注意是**Upload key certificate**，而不是`App signing key certificate`)，在[这里提交](https://support.google.com/googleplay/android-developer/contact/key)或者页面的`contact our support team`，下面有一些问题
  
    - Is your app enrolled in Play App Signing by Google Play? 选择Yes，然后选择I have an upload key-related issue，然后选择I lost my upload key，选这个。会提示你生成一个新的.pem格式的文件，并且会直接给你生成的命令
  
      ```shell
      keytool -genkeypair -alias upload -keyalg RSA -keysize 2048 -validity 9125 -keystore keystore.jks # 这条命令其实就是在Android studio里面Create new的功能
      keytool -export -rfc -alias upload -file upload_certificate.pem -keystore keystore.jks	# 会生成PEM文件的
      ```
  
    - ~~Is your app enrolled in Play App Signing by Google Play? 选择No，然后选择I lost my upload key，不要选这个，google说它不能重置，你必须创建新的app~~
  
  
  - 获取keystore的sha-1指纹: `keytool -list -v -keystore {keystore_name} -alias {alias_name}`

### 物理设备镜像到电脑

`Settings -> Tools -> Device mirroring -> Enable mirroring of physical Android devices`

### 模拟器里面实现震动

- 目前能找到能行的方法只有在模拟器设置里面选择Virtual sensors -> Move，然后拖动X、Y、Z三个轴移动，不能太快也不能太慢

### 模拟器里面使用代理

```shell
# 执行下面命令然后重启模拟器即可
adb shell settings put global http_proxy $(ipconfig getifaddr en0):7890
```

### 支持同时构建不同的APP

- 常用于同时生成测试和生产环境的APP

- 在build.gradle (:app)中添加如下配置:
  ```java
  // 通过构建hook自动切换.env文件
  applicationVariants.all { variant ->
          variant.preBuild.doFirst {
              def flavorName = variant.flavorName
              def envFileName = ".env"
  
              def flutterRootDir = rootProject.projectDir.parent
  
              if (flavorName == "app1") {
                  envFileName = "$flutterRootDir/env/app1.env"
              } else if (flavorName == "app2") {
                  envFileName = "$flutterRootDir/env/app2.env"
              }
  
              def envFile = new File(envFileName)
              def destinationFile = new File("$flutterRootDir/.env")
  
              if (envFile.exists()) {
                  println "Copying ${envFile.toPath()} to ${destinationFile.toPath()}"
                  Files.copy(envFile.toPath(), destinationFile.toPath(), StandardCopyOption.REPLACE_EXISTING)
              } else {
                  println "Error: ${envFileName} does not exist."
                  throw new GradleException("Missing environment file: ${envFileName}. Build terminated.")
              }
          }
      }
  
      productFlavors {
          app1 {
              dimension "app"
              applicationId "com.example.app1"
              resValue "string", "app_name", "App 1"
              buildConfigField "String", "ENV_FILE", "\"app1.env\""
          }
          app2 {
              dimension "app"
              applicationId "com.example.app2"
              resValue "string", "app_name", "App 2"
              buildConfigField "String", "ENV_FILE", "\"app2.env\""
          }
      }
  ```

  

## Google Play Console的使用

- **即使google play console审核通过了，且也被邀请加入测试了，也要等很久才能在app store里面搜索得到并且下载，可以直接搜索的**
- 在`Activity log`中可以查看最近的操作日志
- **审核被拒: Please provide login credentials**: 需要在`Policy -> App content -> App access -> Manage` 中添加Login Credentials  

<!--more-->

## Android开发常见需求

### [In-App Purchase，app内购](https://haofly.net/react-native)

### Activity生命周期

**onStart()**：可以被用户看到的时候调用的方法
**onRestart()**：从第二个返回第一个，因为第一个没被销毁  
**onResume()**：可以获得用户焦点的时候调用
**onPause()**：从一个Activity换向另一个Activity时第一个会调用这个
**onStop()**：当调完第二个时，第一个就调用这个，该Activity处于不可见时，而如果没有全部遮挡起来就不会调用第一个的onStop()方法了  
**onDestroy()**：如果点击返回，可能会调用这个，把第二个摧毁了 

### 打印日志

```java
Log.v(String tag, String msg);  //verbose类型日志，颜色为黑色
Log.d(String tag, String msg);  //debug日志，颜色为蓝色
Log.i(String tag, String msg);  //information日志，颜色为绿色
Log.w(String tag, String msg); //warn告警日志，颜色为橙色
Log.e(String tag, String msg); //error错误日志，颜色肯定为红色

String deviceId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);	// 获取设备的deviceid
```

### Toast提示框展示日志

```java
import android.widget.Toast;
Toast.makeText(this,"显示内容", Toast.LENGTH_SHORT).show();

// 如果报错Can't toast on a thread that has not called Looper.prepare()，可以这样包装一下
Looper.prepare(); // 准备Looper
Toast.makeText(getApplicationContext(), "Toast message", Toast.LENGTH_SHORT).show();
Looper.loop(); // 启动Looper循环
```

### 时间处理

```java
import java.text.SimpleDateFormat;    
SimpleDateFOrmat formatter = new SimpleDateFormat("yyyy年MM月日 HH:mm:ss");
Date curDate = new Date(System.currentTimeMillis()); // 获取当前时间
String str = formatter.formate(curDate);
```

### 地理位置

```java
public Location getLocation() {
LocationManager locManger = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
Location loc = locManger.getLastKnownLocation(LocationManager.GPS_PROVIDER);
if (loc == null) \{
    loc = locManger.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
}
return loc;
```

## TroubleShooting

- **构建成功，但是运行按钮仍然是灰色**: 没有项目的运行配置`Run->edit configurations`中选择配置module

- **configurations中没有module可以配置**: 选择`File->Sync Project with Gradle Fiels`，然后重新构建，选择

- **gradle build running一直卡住**: 网上有很多的原因，但是我的原因是代理设置错误(我并不知道什么时候设置过代理了)，在mac上，`vim ~/.gradle/gradle.properties`修改代理配置即可

- **org.gradle.api.UncheckedIOException: Failed to capture snapshot of input**: 在`Settings->Build, Execution, Deployment->Gradle->Android Studio`勾选`Enable embedded Maven repository`

- **Field to find 'JAVA_HOME' environment variable. Try setting it manully**: 需要下载对应的[jdk](https://www.azul.com/downloads/?package=jdk)，这个网站下载的jdk非常好安装且非常好卸载，直接下载dmg格式的即可，且有直接的apple m1/silicon版本

- **Duplicate class问题**: 如果错误中是googleservice的问题，可以尝试更新`*-build.gradle`中的google-service版本到最新的`classpath 'com.google.gms:google-services:4.3.10'`，android studio会提示你升级到最新的

- **Could not resolve all dependencies for configuration ':app:debugRuntimeClasspath'. 或者 No such property: logger for class: org.gradle.initialization.DefaultProjectDescriptor**: 可能是ide没有找到node环境，尝试从命令行启动: ` open -a /Applications/Android\ Studio.app`

- **Failed to find platform sdk with path: platforms;android-31或者dependency's AAR metadata (META-INF/com/android/build/gradle/aar-metadata.properties)**需要下载compileSdkVersion中指定的sdk版本

- **Android Studio的sdk manager没有显示未下载的sdk**: 重启android studio试试

- **Failed to load WebView provider: No WebView installed**: 我这边把模拟器的系统升级到android 10就可以了

- **cannot find symbol android.suppport.v4.app.ActivityCompat**：直接替换即可，将`import android.support.v4.app.ActivityCompat`替换为`import androidx.core.app.ActivityCompat`即可，这种到androidx的替换，出现一个替换一个就行，没其他问题，我遇到的还有:

  ```shell
  android.support.v4.app.NotificationCompat -> import androidx.core.app.NotificationCompat; 
  ```

- **MacOs安装指定版本的jdk: ** https://www.azul.com/downloads/?package=jdk

- **模拟器无法访问网络**： 可以尝试在AVD的管理面板上选择`Cold Boot Now`试试

- **adb command not found**: 如果安装了`Android Studio`可以直接这样:

  ```shell
  export PATH=~/Library/Android/sdk/tools:$PATH
  export PATH=~/Library/Android/sdk/platform-tools:$PATH
  ```

- **React Native build的APK居然还是需要metro在运行**： 直接build签名的release的apk

- **error: package com.android.annotations does not exist**: 

  ```shell
  npm install --save-dev jetifier
  npx jetify
  
  # 最后在package.json的scripts中添加
  "postinstall": "npx jetify"
  ```

- **Type 'GoogleServicesTask' field 'intermediateDir' without corresponding getter has been annotated with @OutputDirectory**: 需要更新`com.google.gms:google-services`的版本，在Android Studio中打开`build.gradle`，修改如下代码:

  ```java
  dependencies {
      classpath 'com.google.gms:google-services:4.3.10' // 在修改版本的时候编辑器会自动提示你最新的版本号的
  }
  ```

- **Gradle sync failed: Syncfailed: reason unknown**: 尝试在SDK Manager中把29到33的SDK都安装上

- **获取BSSID总是返回02:00:00:00:00:00**:  这是因为高版本的android限制了的，就是无解

- **class butterknife.compiler.ButterKnifeProcessor$RScanner**: 可以尝试在gradle.properties中添加参数

  ```properties
  org.gradle.jvmargs=-Xmx2048M -Dkotlin.daemon.jvm.options\="-Xmx2048M" \
  --add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED \
  --add-exports=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED \
  --add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED
  ```

##### 扩展阅读

[仿B站](https://github.com/TeamNB/FakeBiliBili)