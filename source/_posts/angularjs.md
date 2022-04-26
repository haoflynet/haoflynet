---
title: "AngularJS"
date: 2016-12-07 09:00:39
updated: 2022-03-31 18:03:00
categories: frontend
---
## 安装与配置

- angular不同的版本对typescript的版本要求是不同的，可以参考[这里](https://stackoverflow.com/questions/57216110/the-angular-compiler-requires-typescript-3-4-0-and-3-5-0-but-3-5-3-was-found)
- angular升级是非常简单的，只要参考[官方升级文档](https://update.angular.io/?v=8.0-10.0)一步一步升即可

```shell
ng serve --host 0.0.0.0 --port 3000	# 启动，指定host，指定port

ng build --aot --optimization	--build-optimizer # 编译项目
	--aot	# 默认为false，是否用提前编译进行构建
	--optimization # 默认为false，使用构建输出优化
	--build-optimizer # 默认为false，使用aot进行优化，推荐加上这个参数
	--extract-css	# 默认为false，从全局样式中提取css到css文件而不是放在js文件
	--source-map	# 默认为true，输出source-map文件
	--vendor-chunk	# 默认为true，将第三方包单独放到一个vendor文件中
	
ng build --deploy-url /app/ --deploy-url /app/	# 如果想要app运行在一个子路由路径下可以这样做
```

## Module

```javascript
@NgModule({
  declarations: [
    UserComponent
  ],
  imports: [
    
  ],
  entryComponents: [
  	DialogComponent, // 对于动态调用的组件，没有在html中调用，而是用js来调用的组件需要在这里声明，例如一些弹框，不声明的话，在动态编译的时候可能发现模板没有引用就不去加载了，但是我发现在lazy loading的时候，如果在child module中声明entryComponents不起作用，只能在app.module中声明才行
  ]
})
```

### Lazy loading延迟加载

- 延迟加载是基于页面路由的，每个路由都可以单独作为一个延迟加载，在进入页面的时候加载该页面所需要的组件
- 如果实现了延迟加载我们在进入对应的页面后会发现新请求一个`1.xxxx.js`的文件，开头是一个数字。这就是当前页面的一些组件，同时我们会发现当前页面的组件在`main.js`中没有了
- 如果我们的页面都是单纯的component而不是module的话需要做这些改造

```javascript
// 在页面组件新建路由文件，例如dashboard.route.ts
export const routes: Routes = [
  {path: '', component: DashboardComponent}
]

// 在页面组件新建module文件，例如dashboard.module.ts
import {routes} from './dashboard.route';
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes)	// 注意这里是forChild不是forRoot
  ],
  declarations: [
    DashboardComponent,
  ]
})
export class DashboardComponent { }

// app-routing.module.ts修改路由方式
const routes: :Routes = [
  {
    path: 'dashboard',
   	loadChildren: () => import('./dashhboard/dashboard.module').then(m => m.DashboardModule)	// 注意这里是Module不是Component
  }
]

// 最后在app.module.ts中，移除DashboardCompoent依赖即可
```

## 模板语法

### 数据绑定

```java
// 变量字符串连接
<img src="https://haofly.net/{{ image.url }}" />

// 动态绑定类
[ngClass]="{'myClass': selected}"
[ngClass]="type='xxx' ? 'mt-1' : 'mt-2'"
  
// 动态绑定样式
[ngStyle]="{'pointer-events': ok ? 'none' : 'auto'}"
```

### 控制语句

```javascript
// for 循环
<ul>
  <li *ngFor="let item of items; let i = index">
  	{{i}}:{{item}}
  </li>
    <li *ngFor="let item of map | mapToIterable">	<!--对于key value的map进行for循环遍历-->
  	{{item.key}}:{{item.value}}
  </li>
</ul>

// switch语句
<div [ngSwitch]="myvalue">
    <div *ngSwitchCase="'aaa'">
    ...
  	</div>
    <div *ngSwitchCase="'bbb'">
    ...
  	</div>
    <div *ngSwitchDefault>
    ...
  	</div>
</div>

// ngShow和ngHide在angular 2+已经不支持了，可以直接这样做
[hidden]="myVar"
```

### get方法/computed方法

- 类似于vuejs中的computed

```javascript
get 字段名() {
  return this.firstname + ' ' + this.lastname;
}
```

### 表单Form

```javascript
// js/ts文件
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';

export class MyComponent implements OnInit {
  myForm: FormGroup;

  constructor(private formBuilder: FormBuilder);
  
	ngOnInit(): void {
    this.myForm = this.formBuilder.group({
    	formFieldName: ['初始值', [Validators.required, this.checkName()]],	// 第一个参数设置初始值，第二个参数是验证方法列表
      字段2: ['', []],
      字段3: new FormControl('', {
        validators: [
          this.aaaaaa.bind(this)	// 自定义验证方法
        ],
        updateOn: 'blur'	// 失去焦点的时候进行验证
      }),
      字段4: [{value: '初始值', disabled: true}]	// 如果要让某个字段disabled需要在这里做，直接在html上面disable可能不生效
  	}, {
      validator: this.checkAll	// 如果不是针对某个字段，而是针对整个表单，比如同时验证多个字段，那么可以在这里做
    })
  }
  
  this.checkName(): any {
    return (control: AbstractControl): { [key: string]: boolean } | null => {
      return control.value >= 0 && control.value <= 2 ? null : {nameValueError: true};	// 如果出错可以返回一个key-value
    };
  }

  this.checkAll(formGroup: FormGroup): any {
    return (formGroup.value.formName !== 'new') ? null : {typeEmpty: true};
  }

  onSubmit(): void {
    this.submitting = true;
    this.myForm.get('field1').setValue(value);	// 手动设置form表单字段的额值
    if (this.myForm.valid) {
      console.log('its ok');
    }
  }
}

// html中这样使用
<form [formGroup]="myForm" (ngSubmit)="onSubmit()">
  <div class="form-group">
    <label>Name</label>
    <input type="text" class="form-control" (input)="inputChange" formControlName="formFieldName" [(ngModel)]="user.name">
    <p class="form-warning" *ngIf="submitting && createForm.get('formName').errors">
      <span *ngIf="createForm.get('formName').errors.nameValueError">	// 这是上面自定义的错误
        Name Should be 1 or 2.
      </span>
    </p>
  </div>
  <button type=submit">Submit</button>
</form>
```

### filter过滤器

```javascript
{{ timestamp * 1000 | date: 'yyyy-MM-dd'}} // 时间格式化
```

###  样式

```javascript
// 如果要覆盖第三方组件的样式，可以用::ng-deep，并且为了防止把其他组件也覆盖了，可以加:host前缀将样式覆盖限制在当前的宿主元素上面去
:host ::ng-deep .xxx {
  
}
```

## 组件通信

### 父组件至子组件通信

- 直接用`@Input`

```javascript
<app-child [field]="value"></app-child>

export class ChildComponent {
  @Input() field: any;	// 根据我的测试，子组件可能无法在contructor或者onInit中获取到这个值，因为这个值可能是动态的，所以最好在子组件创建一个get XXX()方法来获取变化后的值
}
```

### 子组件至父组件通信

- 用`@Output EventEmitter`

```javascript
<app-child (field)="onChildClick($event)"></app-child>

export class ParentComponent {
  onChildClick(field) {
    console.log(field);
  }
}

export class ChildComponent {
  @Output() field = new EventEmitter<String>();
  
  onClick() {
  	this.field.emit('click');
  }
}
```

- 用`@ViewChild`不仅能获取子组件的字段，还能直接使用子组件的方法

 ```javascript
 <app-child></app-child>
 
 export class ParentComponent {
 	@ViewChild(ChildComponent)
   private childComponent: ChildComponent
 	
   onTest () {
     this.childComponent.onTest1();
   }
 }
 
 export class ChildComponent {
   onTest1 () {}
 }
 ```

## 不相关的组件通信

- 创建service来通信，复杂的应用场景这个还是用得比较多

```javascript
// 需要先找个地方新建一个service
@Injectable()
export class MyFieldService {
  private myField: Subject<string> = new Subject<string>();

	setMessage(value: string) {
    this.myField.next(value)
  }

	getMessage() {
    return this.myField.asObservable()
  }
}

export class Component1 {
  constructor(private myFieldService: MyFieldService)
  
  onFieldChange() {
    this.myFieldService.setMessage('new value');
  }
}

export class Component2 {
  constructor(private myFieldService: MyFieldService) {
    // 需要特别注意的是，如果回调函数报错了，之后就不会监听了，造成了只能监听一次的假象
    this.myFieldService.getMessage().subscribe((value) => {
      ...
    }
  }
}
```

## 生命周期

依次是

- ngOnChanges(需implements OnChanges): 当设置或重新设置数据绑定的输入属性时响应，但是当组件没有输入，或者使用它时没有提供任何输入，那么框架就不会调用`ngOnChanges()`
- ngOnInit(需implements OnInit)
- ngDoCheck
- ngAfterContentInit()
- ngAfterContentChecked()
- ngAfterViewInit(需implements AfterViewInit): 当初始化完组件视图以及子视图或包含该指令的视图之后调用，只会调用一次
- ngAfterViewChecked
- ngOnDestroy

## 扩展

- @angular/flex-layout: angular的flex布局组件，能够很方便地实现flex响应式布局

  ```html
  <div fxLayout="row" fxLayoutAlign="space-between"></div>
  ```

## 事件

Angular1里元素绑定点击事件用`ng-click`，但是Angular2里元素绑定点击事件用`(click)`，例如:

```javascript
// click事件
<button (click)="toggleImage()">
  
// input事件是指输入的时候
// change事件是指内容改变以后(离开焦点)
<input (input)="onInput()" (change)="onChange()" 
	(keyup)="onKeyUp(event)"	// 键盘输入事件，event.target.value可以获取input的value
>
  
<!-- select元素点击获取选择的值 -->
<select (change)="onChange($event.target.value)">
    <option *ngFor="let item of devices | keyvalue" value="{{ item.key }}">{{ item.value }}</option>	<!--keyvalue过滤器将字典转换为key value对象的形式-->
</select>

// keydown事件指定键，例如按下回车
<input (keydown.enter)="" />
```

## 网络请求

- angularjs的网络操作由`HttpClient`服务提供，在4.3.x开始使用`HttpClient`代替`Http`
- angular的http请求返回的是一个Observable(可观察对象)，在被消费者subscribe(订阅)之前，不会被执行。subscribe函数返回一个subscription对象，里面有一个unsubscribe函数，可以随时拒绝消息的接收

```javascript
constructor(private http: HttpClient) {}
ngOnInit(): void {
  // 必须使用subscribe才会真的去发送请求。每次调用subscribe可以发送一次请求，也就算是说要发送多个请求，直接在最后那subscribe就可以了。
  
  this.http.get('/').subscribe(
    data => {},
    error => {
      error.json	// 获取json格式的错误相应
    }	// catch error
  );
  this.http.post('', body, {}, {params: new HttpParams().set('id', 3')});	// 添加url参数
  this.http.post('', body).subscribe(...);	// post请求
  this.http.post('', body, {headers: new HttpHeaders().set('Authorization', 'my-auth-token')});    // 设置请求头                               
  this.http.get('').subscribe(
  	data => {}
    err => {'错误处理'}
  );
  this.http.get('').retry(3).subscribe(...);	// 设置重试次数
  this.http.get(''). {responseType: 'text'}.subscribe(...); // 请求非json数据
                    
  // 设置自定义的超时时间
  import { timeout, catchError } from 'rxjs/operators';
	import { of } from 'rxjs/observable/of';

  this.http.get('').pipe(timeout(2000), catchError(e => {
    return of(null);
  }))
                                                      
  await this.http.get('').toPromise();	// 将网络请求转换为promise就可以用promise的await语法了

	// 如果一个函数需要返回一个Observable对象，但是又根据条件来进行http请求，条件满足直接返回结果可以用of来封装一下
	if ([condition]) {
  	return of('result');    
  } else {
    return this.http.get('');
  }
}
```

#### httpclient全局error handler

```javascript
// 新建一个http-interceptor.ts文件，或者其他名字都可
import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { _throw } from 'rxjs/observable/throw';
import 'rxjs/add/operator/catch';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req)
      .catch(errorResponse => {
        if (errorResponse.error && errorResponse.error.msg) {
        	...
        }

        throw errorResponse;
      });
  }
}

export const ErrorInterceptorProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: ErrorInterceptor,
  multi: true,
};

// 然后在app.module.ts中声明这个provider即可
@NgModule({
  providers: [
    ErrorInterceptor
  ]
})

```

### 文件上传

```javascript
<input #photoUpload type="file" accept="image/*" (change)="onInput($event)">
<button class="primaryButton" (click)="uploadImage()">Upload Image</button>

export class MyComponent {
  @ViewChild('photoUpload') adminPhotoUpload: ElementRef;
  
  uploadImage(): {
    const files = this.photoUpload.nativeElement.files;
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'multipart/form-data');
    headers.append('Accept', 'application/json');

    return this.http.post(`${apiURL}/api/storage`, formData, {
      headers
    });
  }

  // 或者这样做
  onInput(event): {
    this.file = event.target.files[0];
  }
}
```

## 单元测试

所有的单元测试文件均以`.spec.ts`结尾，该文件具体语法规则如下:

```javascript
describe('test haofly"s function', () =>{
  it('true is true', () => expect(true).toEqual(true));
  it('null is true', () => exect(null).not.toEqual(true));
});
```

## 推荐扩展包

### ngx-dropzone

- 拖拽上传文件组件

### ngx-socket-io

- Socket-io扩展
- 有一个问题是该第三方包现在是支持`extraHeaders`的(支持自定义header传入后端)，但是却没有发布到npm仓库，参考这个[issue](https://github.com/rodgc/ngx-socket-io/issues/119)，下面有人提出解决办法，参考[这里](https://github.com/ThomasOliver545/real-time-chat-nestjs-angular/blob/main/frontend/src/app/private/sockets/custom-socket.ts)，但是登录的时候还没有token，所以最好是在组件的init里面自己new一个Socket对象吧

## TroubleShooting

- **Cannot read property 'stringify' of undefined**: 在模板中无法直接使用`JSON`等原生对象，可以在`constructor()`中传入:

  ```javascript
  public constructor() {
    this.JSON = JSON;
  }
  ```

- **can't bind to 'ngSwitchWhen' since it isn't a known property of 'template'**: `ngSwitchWhen`已经被`ngSwitchCase`替代了

- **can't bind to 'ngModel' since it isn't a known property of 'input': ** 尝试将`FormsModule`添加到`@NgModule`的`imports`中

- **ng: command not found**: `npm install -g @angular/cli@latest`

- **URLSearchParams is not a constructor**: 通常是因为引用`URLSearchParams`是通过`import { URLSearchParams } from "url"`引入的，但其实它早就内置于`nodejs`中了，可以不用写import语句直接用就可以了

- **相同路由改变query params页面不跳转**: 这是和很多单页框架一样的特性，这个时候可以用`window.location.search`进行页面刷新或者通过监听请求参数的变化来重新获取数据，例如:

  ```javascript
  ngOnInit() {
  	this.route.params.subscribe(params => {
  		this.service.get(params).then(...);
    }
  }
  ```

- **ExpressionChangedAfterItHasBeenCheckedErrord: Expression has changed after it was checked.**：这是因为在子组件里面直接改变了父组件的值，通常是在`ngAfterViewInit`或者`ngOnChanges`中，因为这种改变可能会导致无限循环，所以是禁止的，但是如果确保不会发生无限循环，可以将改变的语句写到`setTimeout`中去

- **给用代码生成的元素绑定事件/addEventListener需要使用.bind方法才能在回调函数内部使用this**: 

  ```javascript
  ngAfterViewInit() {
    document.querySelector('my-element').addEventListener('click', this.onClick.bind(data, this));
  }
  
  onClick(data, event) {
    
  }
  ```
  

## 扩展

- [ngx-emoji-picker](https://www.npmjs.com/package/ngx-emoji-picker): emoji选择扩展