---
title: "ionic 教程"
date: 2017-10-17 22:22:39
updated: 2017-10-26 12:34:39
categories: frontend
---
基于AngularJS进行的封装，性能中等。

## ionic开发环境部署

`ionic`app主要使用命令行进行构建并使用`Cordova`用来构建和打包。首先安装[NodeJs](https://haofly.net/nodejs)，然后在[ionic官网](https://dashboard.ionicjs.com)注册一个账号

```shell
npm install -g inoic cordova	# 安装命令行工具
ionic start test				# 创建一个测试项目，期间会提示你登录你的账号
ionic start test tutorial		# 最后一个参数可以新建默认的模板项目，例如tabs表示3个tab的layout(默认选项)，sidemenu、blank、super、tutorial
cd test
git push ionic master			# 初始化项目完成后按照提示进行push操作，push到ionic的控制台里面去
ionic serve						# 自动打开网页，第一个项目能跑起来了
```

此时可以去ionic的控制台查看该项目的信息以及设置一些自动构建相关配置了。但是目前只能在web端访问，如果想要生成ios或者android平台的项目还需要安装单独的工具:

#### for ios

```shell
xcode-select --install	# 安装xcode命令行工具
npm install -g ios-deploy	# 安装ios部署工具
ionic cordova run ios	# 即可自动打开模拟器
```

![ionic ios](http://ojccjqhmb.bkt.clouddn.com/ionic_0.png)

###项目基本结构

```shell
.
├── README.md
├── config		# 个性化配置文件
│   ├── index.ts
├── config.xml
├── hooks
│   └── README.md
├── ionic.config.json
├── node_modules
├── package-lock.json
├── package.json
├── resources
│   ├── README.md
│   ├── android
│   ├── icon.png
│   ├── ios
│   └── splash.png
├── src					# 项目主要源文件
│   ├── app
│   │ 	├── app.component.ts# 定义rootPage，第一个被载入的page，默认是HelloIonicPage,pages表示所有的页面
│   │ 	├── app.html		# app的主模板
│   │ 	├── app.module.ts	# 当前app入口
│   │ 	├── app.scss
│   │ 	└── main.ts
│   ├── assets
│   ├── index.html		# 主入口文件
│   ├── manifest.json
│   ├── pages			# 一个一个的page，这就是最基本的页面
│   │   ├── hello-ionic
│   │   │   ├── hello-ionic.html	# 模板文件
│   │   │   ├── hello-ionic.scss
│   │   │   └── hello-ionic.ts	# 定义该页面的主类HelloIonicPage
│   │   ├── item-details
│   │   │   ├── item-details.html
│   │   │   ├── item-details.scss
│   │   │   └── item-details.ts
│   │   └── list
│   │   │   ├── list.html
│   │   │   ├── list.scss
│   │   │   └── list.ts		# 初始化navCtrl，定义navigation栈，push页面进去
│   ├── service-worker.js
│   └── theme
├── tsconfig.json
├── tslint.json
└── www
    └── manifest.json
```

### 基本配置

可以自己创建一个全局的配置文件，类似`koa2`：

```shell
# vim config/index.ts
export default {
    "option1" : "option1 value"
};

# 使用方法
import Config from '../../../config';
console.log(Config.options1);
```

## API

`Controller`可以直接在`page`的构造函数中自动注入，例如

```javascript
import { ModalController } from "ionic-angular";

constructor(public modalCtrl: ModalController) {}

createModal() {
    let searchPageModal = self.modalCtrl.create(myPage, {origin: self.origin});
	searchPageModal.present();
}
```

### [ModalController](https://ionicframework.com/docs/api/components/modal/ModalController/)

模态框，弹出层。

```javascript
const profileModal = this.modalCtrl.create(Profile, { userId: 8675309 });
profileModal.present();	// 展示出来，一般从下方往上滑动

@Component(...)
class Profile {
	constructor(params: NavParams) {	// page之间传递参数
    	console.log('UserId', params.get('usreId'));	// 获取参数
	}             
}
```

### NavController

主要负责导航的controller。包含有如下一些属性

```shell
# 生命周期函数
ionViewWillEnter: 进入整个页面将要激活的时候触发
ionViewDidEnter: 当整个页面都载入完成过后并且激活后触发
```

### ViewChild

可以使用@ViewChild获取Nav组件的一个实例。例如

```js
// html中有<div #container class="post_container"></div>，定义了一个container，可以在ts中这样获取，定义该元素为ElementRef元素。
@ViewChild('container') postContainer: ElementRef;	// ElementRef是Angular的知识，主要用于封装不同平台下视图层中的native元素。ElementRef.nativeElement就可以获取元素本身，之后就可以进行操作了，例如postContainer.naiveElement.style.backgroundColor。可以拿来当做jQuery中的$(this)了
```

### ViewController

视图控制器。可以控制当前页面的显示。

```javascript
this.viewCtrl.dismiss();	// 关闭当前page
```

## [UI组件](https://ionicframework.com/docs//components/#alert-prompt)

### [Button](https://ionicframework.com/docs/components/#buttons)

按钮组件。

### Content

#### ion-content

最基本的内容组件。

[SearchBar]()

搜索框。

```javascript
<ion-searchbar (ionInput)="getItems($event)"></ion-searchbar>
<ion-list>
  <ion-item *ngFor="let item of items">
    {{ item }}
  </ion-item>
</ion-list>
```

[SearchBar](https://ionicframework.com/docs/components/#searchbar)

搜索框。

### [Tab/Tabs](https://ionicframework.com/docs/components/#select)

标签页，一般是位于页面底部，Tabs内部的元素就是Tab。需要注意的是，只有在控制器里面定义了ion-tab的root页面，页面才会显示，否则不会显示tabs。**默认的tab的`[root]`属性至少填写一个，不然会空白或者全黑**

如果每一页都有底部的tab，最好让app的`rootPage`直接设置为`BasicPage`。

## AngularJS组件

### HttpClient网络请求

要发起网络请求，首先去要添加对应的module，在`app.module.ts`里添加

```javascript
import { HttpClientModule } from "@angular/common/http";
@NgModule({
  declarations: [
    MyApp,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,	// 这里添加该Module
    IonicModule.forRoot(MyApp)
  ],
})
```

## TroubleShooting

- **ion-tabs 不显示，显示空白或者黑色，或者ion-tabs empty blank**:默认的`ion-tab`的 `[root]`属性必须填写，而且不能设置为`null`

- **SearchBar无法自动设置setFocus()，setFocus() not working临时解决方案**: 

  ```javascript
  setTimeout(()=>{
    self.searchBar.setFocus();
  },100);
  ```

  ​

- ​

