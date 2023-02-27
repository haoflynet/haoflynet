---
title: "Appium "
date: 2017-11-01 21:32:00
categories: 编程之路
---

## React-Native测试

```javascript
// 如果发现找不到我们的元素，可以尝试各种办法，accessible、accessibilityLabel都有可能影响到元素的查找，反正多尝试吧
export function testID(id: string, addAccessibilityLabelonIOS?: boolean) {
  return Platform.OS === 'android' || addAccessibilityLabelonIOS
    ? {
        testID: id,
        accessibilityLabel: id,
        accessible: true,
      }
    : {
        testID: id,
        accessible: false,
      };
}
```

## TroubleShooting

- **运行测试时可以看到重新安装了APP，但是却没有打开执行**: 可能是bundleID不一样
