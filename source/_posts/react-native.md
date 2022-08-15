---
title: "React Native手册"
date: 2017-05-27 14:59:00
updated: 2022-08-15 12:24:00
categories: js
---

## 基础概念

**特别注意: **

- `React-Native`是基于`React`实现的，更多语法可以参考[React 开发手册](https://haofly.net/react)
- 如果是自己开发新产品，那么希望每次都把各个基础组件升级到最新稳定版。

`React Native`开发的优点

- 拥有系统级别的通知或提醒
- 可以访问本地通讯录、相册等资源
- 可以针对不同的平台提供不同的体验

`React Native`采用的是`ES2015`(即ES6)的语法标准，模板上使用了自己的`JSX`语法(在代码中嵌入结构标记)。

### 环境搭建

```shell
# 初始化项目
npm uninstall -g react-native-cli	# 官方说不要用这个来初始化了，并且得卸载了，否则可能出现奇怪的问题
npx react-native init testProject	--verbose # 新建项目目录，并初始化项目。命令会执行很久，且--verbose像没用似的，像卡死了一样
npx react-native init testProject --version 0.68.2 --verbose	# 创建指定版本的项目
npx react-native init aegis_app --template react-native-template-typescript --verbose	# 创建一个typescript的项目
npx react-native init oai --template "react-native-template-typescript@6.10.*" --verbose	# 创建一个typescript的项目，指定版本

## 运行项目
cd testProject
npx react-native start
npx pod-install
npx react-native run-ios	# 第一次启动会很慢。等模拟器运行起来后可以直接Cmd+R刷新应用，Cmd+D打开调试菜单
npx react-native run-android	# 安卓开发最好安装上android studio，这不仅会帮你安装java、jdk，而且还能直接管理安卓模拟器，把android studio配置好了以后，android的开发环境也好了

npm install --save react-native@X.Y	# 直接指定版本号的更新升级，手动升级更爽。我不喜欢用react-native-git-upgrade来升级，需要注意的是，升级以后一定要顺便升级一下命令行工具react-native-cli，否则会可能会出现不预期的错误
```

### prop&&state

两者可以说是大同小异，在大多数情况下，两者没什么很大的差别。两者的改变的时候，渲染的地方都会重新渲染。

**prop**: 一个组件的设置参数，可以理解为初始化参数或者对象的静态变量，并且可以在父组件中设置，在子组件中不可改变，但是可以一直往下传递至子子孙孙。

**state**: 更像是对象的一些变量，并且确实是经常改变的，只是父子之间不能传递。

```javascript
// 动态设置某个状态值
this.setState({
    results: value,
});
```

## 布局

不用css，但是类似css。所有的组件都有`style`属性。样式名是将默认的css的命名更改为了驼峰命名。一般使用`StyleSheet.create`在组件外面集中定义组件的样式。例如:

```js
// 指定固定的高度和宽度用width和height，React Native中的尺寸都是无单位的。
<View style={{width: 50, height: '50%', backgroundColor: 'powderblue'}} />

// 弹性的高度和宽度用flex。flex为1的时候表示撑满所有的剩余空间，如果多个并列子组件一起使用，则他们会平分空间，并且值越大所占比例就越大。例如
<View style={{flex: 2, backgroundColor: 'skyblue'}} />

<View style={[styles.css1, styles.css2]} /> // 包含多个样式

// 这样还能直接看出来层级关系。例如<Text style={styles.red}>test</Text>
const styles = StyleSheet.create({
  bigblue: {
    color: 'blue',
    fontWeight: 'bold',
    fontSize: 30,
  },
  red: {
    color: 'red',
  },
});
```

#### Flexbox布局

规定某个组件的子元素的布局。`flex`的值就类似于栅栏布局中的row宽度，一个2一个1，那么画面总共可以分成三份这种，如果直接`flex:1`，那么就表示直接占据整个。

```javascript
// 父视图属性
<View style={{
	flex: 1, 
    flexDirection: 'row', 	// 规定布局方向，默认是column垂直方向布局，row表示水平方向布局
    flexWrap:'wrap', // 默认为nowrap，表示子元素是否允许多行排列
    justifyContent: 'flex-start', // 规定子元素沿着主轴的排列方式。可选项有flex-start、center、flex-end、space-around以及space-between
    alignItems: 'stretch', //规定子元素沿着次轴(与主元素垂直的轴)的排列方式。可选项有flex-start、center、flex-end、stretch
}}>

// 子视图属性
<View style={{
	alignSelf: 'auto', // 定义了flex容器内被选中项目的对齐方式，可选auto, flex-start, flex-end, center, stretch	             
}}>

// flexGrow与flex有些类似，但是flex会使子元素的空间大小限定在父元素空间范围内，而flexGrow会使子元素起码维持其本身大小，再根据父元素是否有剩余空间进行空间分配。
```

#### 居中问题

```javascript
// 图标悬浮与图片的正中间，两者均居中对齐
<View style={{
		justifyContent: 'center',
        alignItems: 'center',
}}>
    <Icon name="microphone" size={70} style={{
        position: 'absolute',
        zIndex: 1,
        justifyContent: 'center',
		alignItems: 'center'
    }}/>      
	<Image source={require('../img/test.png')} style={{
       width: 250, 
       height: 250,
       alignItems: 'center',
       justifyContent:'center',
      }}
    />
</View>
```

#### 定位问题

```javascript
// 获取屏幕尺寸
import Dimensions from 'Dimensions';
Dimensions.get('window');

// 获取元素的位置: https://stackoverflow.com/questions/30096038/react-native-getting-the-position-of-an-element
class MyComponent extends React.Component {
    render() {
        return <View ref={view => { this.myComponent = view; }} />
    }
    componentDidMount() {
        // Print component dimensions to console
        this.myComponent.measure( (fx, fy, width, height, px, py) => {
            console.log('Component width is: ' + width)
            console.log('Component height is: ' + height)
            console.log('X offset to frame: ' + fx)
            console.log('Y offset to frame: ' + fy)
            console.log('X offset to page: ' + px)
            console.log('Y offset to page: ' + py)
        })        
    }
}
```

## 组件

### Animated动画

第三方库里面那些酷炫的效果均是通过动画来实现的

```javascript
const top = useRef(new Animated.Value(100)).current;	// 将一个属性变为可以执行动画的属性

<Animated.View>
  <View style={{top}}></View>
</Animated.View>

top.setValue(1000);	// 当改变值的时候用setValue来执行，就能让改变变得平滑
Animated.timing(top, {	// 也可以自定义执行时间
  toValue: 1000,
  duration: 500,	// 默认500
  delay: 100,	// 默认为0
}).start()
```

### Button基础按钮

这个组件的样式是固定的，如果需要自定义，那么高级的按钮参考`Touchable`系列

```javascript
<Button
	onPress={() => this._func()}
	title="按钮标题必填"
/>
```

### Image

图片组件，如果我们在同一个目录里面同时包含`a.png/a@2x.png,a@3x.png`那么`react native`就能通过屏幕的分辨率自动选择不同尺寸的图片，并且在代码里面仅需要`require(./img/check.png)`就行了。

### Navigation/Component导航组件/路由/route

[Navigation文档](https://reactnavigation.org/docs/getting-started)，Navigation已经单独成为一个模块，强烈建议不再使用老的导航器，[导航器对比](https://www.jianshu.com/p/98db12a6afec)，在这里有其更详细的文档。在`0.44`版本移除了[`Navigator`](https://facebook.github.io/react-native/docs/navigator.html)，该模块被移动到[react-native-custom-components](https://github.com/facebookarchive/react-native-custom-components)现在也仅用于兼容老版本。使用前得先安装`npm install --save react-navigation`。有如下三种类型的导航器

```shell
# 看官网的意思就是要安装这些东西
npm install --save @react-navigation/native react-native-screens react-native-safe-area-context @react-navigation/native-stack

# ios需要执行
npx pod-install ios

# android需要再MainActivity中添加一个方法
import android.os.Bundle;

@Override
protected void onCreate(Bundle savedInstanceState) {
  super.onCreate(null);
}

# 然后需要全局使用NavigationContainer包裹app，在app.js中
import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';

export default function App() {
  return (
    <NavigationContainer>{/* Rest of your app code */}</NavigationContainer>
  );
}
```

#### StackNavigator

类似于普通的Navigator，体现在屏幕上方的导航栏

```javascript
// StackNavigator用于创建多页面应用。其中每一个都是一个Component
import React from 'react';
import { View, Text } from 'react-native';
import { StackNavigator } from 'react-navigation';

class HomeScreen extends React.Component {
  static navigationOptions = ({navigation}) => {return ()}; // 可以使用return的方法，这样可以在上面写一些逻辑
  static navigationOptions = ({navigation}) => ({
    title: '头部标题',
    headerStyle: {
    	backgroundColor: '#ffffff',	// 设置头部样式      
    },
    headerTintColor: '#fff',
    headerTitleStyle: {	// 设置头部字体样式
      fontWeight: 'bold'      
    },
    headerRight: (			// 设置header bar的左右按钮
      <Button
        onPress={() => alert('This is a button!')}
        title="Info"
        color="#fff"
      />
    ),
    // header头中直接进行页面跳转
    headerRight: (<Button onPress={() => navigation.navigate('Setting')} title={'设置'}  />),

  });

  componentWillMount() {}	// render之前执行，并且永远只执行一次
  render() {}		// 渲染页面
  componentDidMount() {}	// 组件加载完成后执行，在render之后，已经有了DOM结构，不要把其他逻辑写在render，以防阻塞UI
  componentWillReceiveProps() {} // 组件接收到一个新的prop时执行，这个方法在初始化render时不会被调用
  shouldComponentUpdate() {}  // 返回一个布尔值
  componentWillUpdate() {}	// 在组件接收到新的props或者state但还没有render时执行，初始化时不会执行
  componentDidUpdate() {}	// 组件更新完成后

  render() {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Home Screen</Text>
      </View>
    );
  }
}

// 可以在App.js中声明所有的页面，默认放在第一个的为首页
export default StackNavigator({
  Home: {
    screen: HomeScreen,
  },
});

// 组件之间跳转方式
this.props.navigation.push('Home');	// 跳转至新的场景，并且将场景入栈
this.props.navigation.navigate('Home', {param1: '...'})	// 将新路由推送到堆栈导航器，如果它不在堆栈中，那么跳转到该页面
this.props.navigation.goBack()
```

#### TabNavigator

类似于ios的`TabBarController`，屏幕下方的标签栏

#### DrawerNavigator

侧边弹出的抽屉效果

### SafeAreaView

- 使用改组件包裹可以自动实现异形屏的padding，也不用考虑android还是iOS

```javascript
import { SafeAreaView } from 'react-native'	// 如果不工作，就使用下面的方式
import { SafeAreaView } from 'react-native-safe-area-context'
```

### ScrollView滚动

可以在该组件下面添加任意组件，能轻松实现几个组件的共同滑动

```javascript
<ScrollView
	scrollEnabled={false}		// 禁用滚动
></ScrollView>
```

### StatusBar状态栏

### TextInput输入框

TextInput默认宽度与父节点相同。如果想要其在没有文字的时候也能占据宽度，可以设置`flex:1`并且父`View`也得设置`flex:1`

```javascript
<TextInput
	style={{
           height: 40, 
           alignSelf: 'center',	// 输入框文字居中
           alignItem: 'center',
           textAlign: 'center',	// 这个才是输入框里面的文字居中
    }}
    onChangeText={(text) => this.setState({text})}
    clearTextOnFocus={true}
    placeholder='请输入'	// 默认是灰色的
    value={this.state.text}
/>
```

### Touchable*系列

包括了触摸的相关事件(触摸、点击、长按、反馈等):

**onPressIn**: 触摸开始

**onPressOut**: 触摸离开

**onPress**: 单击事件

**onLongPress**: 长按事件

#### TouchableHighlight

触摸点击高亮效果。点击的时候，不透明度会降低，同时会看到变暗或者变量。只支持一个子节点，如果要多个子视图组件，可以用View进行包装。

```javascript
<TouchableHighlight onPress={this._onPressButton.bind(this)} underlayColor="white">
    <View style={styles.button}>
        <Text style={styles.buttonText}>TouchableHighlight</Text>
	</View>
</TouchableHighlight>

// 可点击的图片
<TouchableHighlight onPress={this._onPressButton}>
    <Image
		style={styles.button}
		source={require('./myButton.png')}
	/>
</TouchableHighlight>
```

#### TouchableNativeFeedback

仅限android。

#### TouchableOpacity

透明度变化。

#### TouchableWithoutFeedback

不带反馈效果的。

## API

### Share分享功能

```javascript
import { Share } from 'react-native';
Share.share({	// 官方文档说android用message、ios用url，但经过我的测试最好都用url，因为分享到不同的app，获取的字段并不相同
	title: url,
  message: url,
  url: url,
})
```


## JSX语法

```jsx
// 使用循环
<View>
    {this.state.voices.map((voice, index) => {
        return (
        <Text key={`voice-${voice.id}`}>
			{voice.text}
		</Text>
		)
	})}
</View>

// 定义模板(自定义标签)
const InfoText = ({ text }) => (		// 其中text是模板的参数
  <View style={styles.container}>
    <Text style={styles.infoText}>{text}</Text>
  </View>
)
<InfoText text="haofly"/>	// 使用模板
```

### 样式stylesheet

- [官方建议](https://reactnative.dev/docs/stylesheet)不要将stylesheet放在render函数中
- 最好不同的组件使用不同的名称，不要全都用`styles`命名
- 原生不支持scss那样的嵌套语法，好像也没有啥好用的嵌套方式，就是感觉原生就是不支持什么复杂的样式

```jsx
const page = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    alignItems: "center"
  }
})

const typography = StyleSheet.create({
  header: {
    color: "#61dafb",
    fontSize: 30,
    marginBottom: 36
  }
})
```

## 网络请求

`React Native`使用的网络请求是[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)，但是，统治js的http请求库明显是`axios`，所以我还是喜欢用`axios`，另外，网络请求天生就应该是异步的，这两个库都是不支持同步的。

```javascript
// 安装npm install --save axios
import axios from 'axios';
axios.get('...').then((response)=>(console.log(response.data))); // 得到响应结果，不用像fetch那样responseJson了
```

## Debug

- 如果是真机，可以通过摇一摇弹出debug菜单，但是基本上没啥用，最有用的可能就是Chrome里面调试了，至少能看到打印出来的object的详情

- `LogBox`在`release/production`中是自动禁用的

## 常用插件推荐

### [Awesome React Native](https://github.com/jondot/awesome-react-native)

- 包含很多的react native的插件扩展

### [customauth-react-native-sdk](https://github.com/torusresearch/customauth-react-native-sdk)

- torus sdk

- 如果运行不起来可以试试它项目里面的example，虽然文档少了，但是那个example还是更新的挺及时的，照着看有没有遗漏的，我在1.0.1版本上发现有这些需要额外配置:

  ```javascript
  // ios/Podfile，具体行数参考example中的配置
  use_modular_headers
  pod 'glog', :podspec => '../node_modules/react-native/third-party-podspecs/glog.podspec', :modular_headers => false
      installer.pods_project.build_configurations.each do |config|
  #       config.build_settings["EXCLUDED_ARCHS[sdk=iphonesimulator*]"] = "arm64"
      end
  
      installer.pods_project.targets.each do |target|
        if target.name == "web3.swift"
  target.build_configurations.each do |config|
    config.build_settings["SWIFT_INCLUDE_PATHS[sdk=iphonesimulator*]"] = "$(inherited) $(PODS_CONFIGURATION_BUILD_DIR)/BigInt $(PODS_CONFIGURATION_BUILD_DIR)/GenericJSON $(PODS_TARGET_SRCROOT)/web3swift/lib/**"
  config.build_settings["SWIFT_INCLUDE_PATHS[sdk=iphoneos*]"] = "$(inherited) $(PODS_CONFIGURATION_BUILD_DIR)/BigInt $(PODS_CONFIGURATION_BUILD_DIR)/GenericJSON $(PODS_TARGET_SRCROOT)/web3swift/lib/**"
  end
  end
  end
  
  // AppDelegate.m，我最开始就是点了登录后没反应，后来发现是它根本没有监听openURL
  - (BOOL)application:(UIApplication *)app
              openURL:(NSURL *)url
              options:(NSDictionary<NSString *, id> *)options {
  
    NSString *myString = url.absoluteString;
  
    NSLog(@"String to handle : %@ ", myString);
    if (@available(iOS 10.0, *)) {
      [RNCustomAuthSdk handle:myString];
    } else {
      // Fallback on earlier versions
    }
  
    // Your additional URL handling (if any) goes here.
    return NO;
  }
  
  
  // ios/xxx/Info.plist，添加url scheme
  		<dict>
              <key>CFBundleTypeRole</key>
              <string>Editor</string>
  			<key>CFBundleURLSchemes</key>
  			<array>
  				<string>torusapp</string>
  			</array>
  		</dict>
  
  ```

### [react-native-geolocation-service](https://github.com/Agontuk/react-native-geolocation-service)

- 谷歌定位插件，能够获取当前的定位

- 如果出现获取不到地理位置，经常提示`timed out`并且time out设置为很大依然报错，可以参考这个issue[Location request timed out most of the time](https://github.com/Agontuk/react-native-geolocation-service/issues/174)，下载谷歌地图然后定位一下，再重新安装一下应用试试

- 如果出现**Location settings are not satisfied**: 根据我的尝试，可能是因为国内或者说是因为小米手机的问题，ios和android得不同的设置才行:

  ```javascript
  Geolocation.getCurrentPosition(
  	(position) => {console.log(position)},
  	(error) => {console.log(error)},
  	Platform.OS === 'ios' ? { enableHighAccuracy: true, timeout: 25000, maximumAge: 20000 } : { enableHighAccuracy: false, maximumAge: 20000, forceRequestLocation: true, forceLocationManager: true, distanceFilter: 250, accuracy: { android: 'balanced', ios: 'threeKilometers' } }
      );
  ```

### [react-native-async-storage](https://github.com/react-native-async-storage/async-storage)

- 能够用来持久化mobx等的状态，在应用退出后不会清空
- `React-native iOS, Async storage error: "Invalid key - must be at least one character. Key: `出现这个错误是因为在getItem/setItem的时候key的值为空，需要修改一下，注意如果key的值修改后可能需要重新build才能生效

### [react-native-bottom-sheet](https://www.npmjs.com/package/@gorhom/bottom-sheet)

- 一个比较好用的底部弹出功能，drawer，抽屉
- snapPoints: 定义弹出的区域的高度，这之外的地方不能点击
- `enablePanDownToClose`: 向下滑自动关闭
- 如果是多个sheet叠加显示，好像DOM后面的就是最上层

### [react-native-dotenv](https://github.com/goatandsheep/react-native-dotenv)

-  使用`.env`文件来加载环境变量
- 需要注意的是，它是有缓存的，如果变量更改了记得参考文档清理cache
- 如果使用的是typescript，最好参考文档使用`Option 2: specify types manually`

### [react-native-iap](https://github.com/dooboolab/react-native-iap)

- 用于google play和apple store的内购组件
- **Android平台能够通过getProducts获取产品列表，但是购买的时候却报错That item is unavailable**: 具体原因还未知，在github提交了[discussion](https://github.com/dooboolab/react-native-iap/discussions/1378)，但目前没有回复。最后不知道怎么就解决了，尝试过这些方法:
  1. 上传一个signed release到internal testing和closed testing，但是第一次上传审核时间有点久，且审核通过后可能也要等几小时才可以
  2. Google Play Console -> Setup -> API access: 打开了`Play Android Developer API`，应该和这个无关
  3. License testing得添加设备登录的google账号
  4. `App -> Setup -> Advanced settings -> App availability`设置为`Published`
  5. `App ->  Setup -> Advanced settings -> Managed Google Play`设置为`Turn on`下面的留空就行

### [react-native-paper](https://callstack.github.io/react-native-paper/index.html)

- material-ui在react-native平台的替代品，同样遵循material design
- 在使用Menu.Item的时候，如果要自定义menu和整个container的高度，需要设置minHeight和maxHeight才行，不知道为啥container会默认设置为100，源码里没看到哪个地方有设置
- `ActivityIndicator`就是一个loading图标，非常好用

## 开发原生相关问题

#### 在真实设备上调试以及打包到真实设备

在真实设备上调试，只需要在`Xcode`中`Run`到你自己连接的设备即可，这时候安装在手机上面的，是和电脑上面模拟器出来的一模一样，也能进行调试，但是断开usb后应用不能使用。如果要将应用直接整体打包到设备上面，看看真实使用的效果，可以按照这个教程进行设置`https://facebook.github.io/react-native/docs/running-on-device.html`，主要就是修改`AppDelegate.m`中的`jsCodeLocation`的值，将其改变成如下状态即可。

```swift
jsCodeLocation = [[NSBundle mainBundle] URLForResource:@"main" withExtension:@"jsbundle"];
```

#### APP图标设置

参考`Xcode`中的图标设置，也只能在`xcode`中设置，即直接将图标拖如`Images.xcassets`

#### 原生库

开发者会将很多原生库打包成一些静态库，或者由js直接封装好了的静态库。一般比较好的静态库都能够使用命令自动链接:`react-native link 某已安装的具体库名`，如果手动链接可以参考文档[linking-libraries-ios](https://facebook.github.io/react-native/docs/linking-libraries-ios.html)

## TroubleShooting

- **":CFBundleIdentifier" Does Not Exist**: 可能是因为你的代码依赖的是老的`react native`或者`node`版本或者`xcode`版本，可以执行以下命令升级依赖:`react nativeupgrade `

- **undefined is not an object evaluating React.PropTypes.string**: 仍然是版本的问题，新版的已经将`React.PropTypes`移到单独的库了([prop-types](https://reactjs.org/blog/2017/04/07/react-v15.5.0.html))。需要注意的是`React.PropTypes.func`更改成了`PropTypes.function`了，其他的名字没有改，只是位置变了。

- **undefined is not an object(evalauating 'WeChat.registerApp')**: 引入`react-native-wechat`之后[手动去link](https://github.com/yorkie/react-native-wechat/blob/master/docs/build-setup-ios.md)

- **No bundle url present**: 启动的时候报错，有以下几种解决方案:

  - 全部关了以后，看看8081端口是否被占用，然后重新`react-native run-ios`
  - 上面方法多次尝试不行以后直接删除`node_modules`目录，重新安装依赖

- **isMounted(...) is deprecated warning**: [目前来看](https://github.com/react-navigation/react-navigation/issues/3956)，并没有什么解决方案。

- **闪退**: 有如下几种情况

  - 没有给API添加对应的权限，具体权限列表可以参见: [Swift开发MacOS应用](https://haofly.net/swift-macos)

- **_this._registerevents is not a function**: 升级的时候没有顺便升级`react-native-cli`

- **cross-env: command not found**: `npm install cross-env`

- **unable to load script from assets index.android.bundle**: 这样做能够解决(来自于Stackoverflow):

  ```shell
  mkdir android/app/src/main/assets
  react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res
  react-native run-android
  
  # 可以将上面的命令放到package.json的scripts中去，这样以后直接npm run android-linux即可
  "android-linux": "react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res && react-native run-android"
  ```

- **`SDK location not found. Define location with sdk.dir in the local.properties file or with an ANDROID_HOME environment variable.`**原因是没有定义android sdk的位置，首先下载android sdk或者安装android studio(会自动下载sdk)，最后将地址写在`local.properties`文件或者直接设置为环境变量`ANDROID_HOME`

- **com.android.builder.testing.api.DeviceException: No connected devices! **得去android studio把安卓模拟器打开

- **`react-native run-android`命令提示`Android project not found. Maybe run react-native android first`，但是执行`react-native android`却说命令没找到**: 首先看当前目录有没有`android`文件夹，如果没有，那么使用`react-native eject`命令生成，如果有，那么就用`android studio`来运行一次，看看是不是有哪些基础环境没有安装

- **Invalid YGDirection 'row' should be one of: (inherit, ltr, rtl)**: 需要将`<Flex direction="row"`修改为`<Flex flexDirection="row"`

- **`Print: Entry, ":CFBundleIdentifier", Does Not Exist`** [解决方法如下](https://stackoverflow.com/questions/37461703/print-entry-cfbundleidentifier-does-not-exist)

  ```shell
  # 首先关闭XCode
  cd node_modules/react-native/third-party/glog-{X}.{X}.{X}/
  ./configure
  # 然后重新打开xcdoe即可
  ```

- **Text strings must be rendered within a <Text> component**: 首先最基本的，文字必须在text组件里面，但这还是比较容易排查，而不好排查的情况一般是我们在做判断的时候没有使用布尔值，例如

  ```javascript
  {icon && {icon}} // 这样会报错
  {!!icon && {icon}} // 将对象转换为布尔值即可
  ```

- **输入框键盘挡住了部分视图**: 这时候需要使用`KeyboardAvoidingView`来包装一下`view`，该组件可以自动根据键盘的高度，调整自身的height或底部的padding来避免遮挡，有时候也需要再配合`ScrollView`来使用，注意它可以不需要在整个页面外层包装，可以只包裹住form那部分即可

  ```javascript
  <KeyboardAvoidingView
  behavior={Platform.OS == "ios" ? "padding" : "height"}
  style={styles.container}
  >
    ...
  </KeyboardAvoidingView>
  ```

- **ARCHS[@]: unbound variable in Xcode 12或者YogaKit.modulemap not found**: 需要把`Build Settings -> Architectures -> Excluded Architecture`设置成这样(来自[Stackoverflow](https://stackoverflow.com/questions/64474801/archs-unbound-variable-in-xcode-12)): ![](https://i.stack.imgur.com/4RFTI.png)

- **You must have a keystore.properties file in the <rn-root-folder>/android/ folder or set the environments variables**: Android目录下新建文件`keystore.properities`，内容如下即可:

  ```shell
  STORE_FILE=app.keystore
  KEY_ALIAS=app_alias
  STORE_PASSWORD=your_password
  KEY_PASSWORD=your_password
  ```

##### 扩展阅读

- 浅谈前端移动开发[(Ionic与React Native)](http://bbs.reactnative.cn/topic/420/%E6%B5%85%E8%B0%88%E5%89%8D%E7%AB%AF%E7%A7%BB%E5%8A%A8%E5%BC%80%E5%8F%91-ionic-%E4%B8%8E-react-native)
- [30天React Native学习](https://github.com/fangwei716/30-days-of-react-native)


- [仿美团示例项目]( https://github.com/huanxsd/MeiTuan)
- [低仿映客直播](https://github.com/tion126/RNLive?utm_medium=email&utm_source=gank.io)
- [双生——情侣应用](https://github.com/oh-bear/2life)
- [基于 React Native 的跨三端应用架构实践](https://www.infoq.cn/article/vXkNh*HVrW7HUeiNdlsk)

