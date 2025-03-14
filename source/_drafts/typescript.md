## 常用声明

### Record键值对

```javascript
Record<string, {key: string; value: string}[]> 
// 等价于:
{
  [key: string]: { key: string; label: string }[];
}
```








```
TS7031: Binding element label implicitly has an any type.

{
  "compilerOptions": {
    "noImplicitAny": false // 禁用任何any类型的错误提示
  }
}



禁用TS2571: Object is of type unknown

```

