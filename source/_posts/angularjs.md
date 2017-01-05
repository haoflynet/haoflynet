---
title: "AngularJS"
date: 2016-12-07 09:00:39
categories: frontend
---
# AngularJS

## 语法

**循环语句**

```javascript
<ul>
  <li *ngFor="let item of items; let i = index">
  	{{i}}:{{item}}
  </li>
</ul>
```

## 事件

Angular1里元素绑定点击事件用`ng-click`，但是Angular2里元素绑定点击事件用`(click)`，例如:

```bu
<button ng-click="vm.toggleImage()">
<button (click)="toggleImage()">
```

## 单元测试

所有的单元测试文件均以`.spec.ts`结尾，该文件具体语法规则如下:

```javascript
describe('test haofly"s function', () =>{
  it('true is true', () => expect(true).toEqual(true));
  it('null is true', () => exect(null).not.toEqual(true));
});
```

