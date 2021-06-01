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

