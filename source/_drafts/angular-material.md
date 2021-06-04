## 组件

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
