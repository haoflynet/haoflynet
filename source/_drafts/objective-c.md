## 数据类型

### 字符串

```objective-c
NSLog(@"test");	// 直接打印字符串

```

### 数组

```objective-c
NSArray *arr = @[@"abc", @"def", @"ghi"];
NSLog(@"arr:%@", arr);	// 打印

for (NSString *str in arr) {	// 遍历数组
  NSLog(@"%@", str);
}
```

### 函数/方法

- 使用中括号来调用方法，例如`[self hello:YES]`([类名 方法名:参数])就相当于其他语言的`this.hello(true);`

```objective-c
- (void)requestUserTokenForDeveloperToken:(NSString *)developerToken completionHandler:(void (^) (NSString * _Nullable userToken, NSError * _Nullable error))completionHandler API_AVAILABLE(ios(11.0), tvos(11.0), watchos(7.0), macos(11.0), macCatalyst(13.0));
```

