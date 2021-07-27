## 组件

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
