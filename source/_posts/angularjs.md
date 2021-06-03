---
title: "AngularJS"
date: 2016-12-07 09:00:39
updated: 2021-06-02 22:53:00
categories: frontend
---
## 语法

### 数据绑定

```java
// 动态绑定类
[ngClass]="{'myClass': selected}"
[ngClass]="type='xxx' ? 'mt-1' : 'mt-2'"
```

### 控制语句

```html
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
```

### get方法/computed方法

- 类似于vuejs中的computed

```javascript
get 字段名() {
  return this.firstname + ' ' + this.lastname;
}
```

### 表单

## 事件

Angular1里元素绑定点击事件用`ng-click`，但是Angular2里元素绑定点击事件用`(click)`，例如:

```javascript
// click事件
<button (click)="toggleImage()">
  
// input事件是指输入的时候
// change事件是指内容改变以后(离开焦点)
<input (input)="onInput()" (change)="onChange()">
  
<!-- select元素点击获取选择的值 -->
<select (change)="onChange($event.target.value)">
    <option *ngFor="let item of devices | keyvalue" value="{{ item.key }}">{{ item.value }}</option>	<!--keyvalue过滤器将字典转换为key value对象的形式-->
</select>
```

## 网络请求

angularjs的网络操作由`HttpClient`服务提供，在4.3.x开始使用`HttpClient`代替`Http`

```javascript
constructor(private http: HttpClient) {}
ngOnInit(): void {
  // 必须使用subscribe才会真的去发送请求。每次调用subscribe可以发送一次请求，也就算是说要发送多个请求，直接在最后那subscribe就可以了。
  this.http.get('/').subscribe(data => {
    // Read the result field from the JSON response.
    this.results = data['results'];
  });
  this.http.post('', body, {}, {params: new HttpParams().set('id', 3')});	// 添加url参数
  this.http.post('', body).subscribe(...);	// post请求
  this.http.post('', body, {headers: new HttpHeaders().set('Authorization', 'my-auth-token')});    // 设置请求头                               
  this.http.get('').subscribe(
  	data => {}
    err => {'错误处理'}
  );
  this.http.get('').retry(3).subscribe(...);	// 设置重试次数
  this.http.get(''). {responseType: 'text'}.subscribe(...); // 请求非json数据                                     
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

##### TroubleShooting

- **Cannot read property 'stringify' of undefined**: 在模板中无法直接使用`JSON`等原生对象，可以在`constructor()`中传入:

  ```javascript
  public constructor() {
    this.JSON = JSON;
  }
  ```

- **can't bind to 'ngSwitchWhen' since it isn't a known property of 'template'**: `ngSwitchWhen`已经被`ngSwitchCase`替代了

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

  