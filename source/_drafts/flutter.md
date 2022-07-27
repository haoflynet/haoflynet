```shell
# 安装dart sdk
brew tap dart-lang/dart
brew install dart
brew info dart	# 获取dart sdk的安装位置

# 安装flutter：https://docs.flutter.dev/get-started/install/macos#system-requirements

# 安装依赖
flutter doctor	# 查看还有什么依赖没有安装
flutter pub get # 安装项目依赖性，同flutter packages get
flutter pub upgrade	# 更新依赖包
flutter pub cache	# 清除缓存
flutter pub deps	# 显示依赖

	
	Flutter是基于Dart语言的移动UI框架
	
	下载sdk，得自己找地方放，放了后加入PATH
```

## TroubleShooting

- **HTTP Host Availability**: 如果`flutter doctor`出现这个错误，需要开启代理才行