## 组件

### Dialog

- 默认情况`dialog`组件会自动focus第一个可以focus的元素(如果第一个元素在最下面，可能会造成打开就滑动到了最下面的问题)，可以修改其`autoFocus`从参数

### Input

```javascript
// 验证功能
emailFormControl = new FormControl('', [
    Validators.pattern('abc')
]);

<input type="text" class="form-control" [formControl]="emailFormControl">
<mat-error *ngIf="emailFormControl.hasError('pattern')">
  Please enter a valid email address
</mat-error>
```



### Selection

```react
<mat-form-field appearance="fill">
  <mat-label>Icons</mat-label>
  <mat-select [(value)]="myIds" multiple>
    <mat-option value="0">Option1</mat-option>
    <mat-option value="1">Option2</mat-option>
    <mat-option value="2">Option3</mat-option>
  </mat-select>
</mat-form-field>
```

### Tooltip

```javascript
// 手动调用tooltip
<button md-mini-fab color="primary" #tooltip="mdTooltip" [mdTooltip]="'Menu'" [mdMenuTriggerFor]="menu" class="remove-record">Button</button>

@ViewChild('tooltip') tooltip:MdTooltip;

ngOnInit() {
    this.tooltip.show();
}
```

### [tree](https://material.angular.io/components/tree/examples)

- 这是我见过最难用最难看的`tree`组件了
