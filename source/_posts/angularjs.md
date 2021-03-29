---
title: "AngularJS"
date: 2016-12-07 09:00:39
updated: 2021-03-29 22:53:00
categories: frontend
---
## 语法

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

## 事件

Angular1里元素绑定点击事件用`ng-click`，但是Angular2里元素绑定点击事件用`(click)`，例如:

```html
<button ng-click="vm.toggleImage()">
<button (click)="toggleImage()">
  
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