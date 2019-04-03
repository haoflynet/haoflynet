---
title: "我用的IDEs及其配置"
date: 2019-02-26 21:32:00
updated: 2019-04-02 11:10:00
categories: 编程之路
---

多年前，我喜欢用`sublime`，那时候我主要开发的是`Python`这种很简单的脚本语言，后来接触了IDE才发现，对开发者来说，编辑器真的只是暂时的工具，真正能提高大幅度提高开发效率的绝对是功能完整、适配性强的IDE呀😂。

<!--more-->

## Android Studio

- 需要签名的项目，需要先生成JSK文件，在`Build->Build signed APK`里面创建一个即可

- **`Error: Failed to resolve: com.android.support.constraint:constraint-layout-solver:1.0.2`**，只需要在`SDK Manager`中的`SDK Tools`中的`ConstraintLayout for Android`下载或者下载指定的版本即可

- **`/dev/kvm permission denied`**: 原因是当前用户没有在kvm用户组中，需要进行这样的设置:

  ```shell
  sudo apt-get install qemu-kvm -y
  ls -al /dev/kvm	# 查看当前kvm权限，一般是属于root用户，kvm组的
  grep kvm /etc/group	# 查看kvm用户组里面有哪些用户，一般只有kvm:x:数字:
  sudo adduser 用户名 kvm	# 将自己添加到kvm用户组中
  grep kvm /etc/group		# 现在应该变成kvm:x:数字:用户名了
  # 最后注销重新登录即可生效
  ```


## IDEA系列

- 展开左边文件目录树快捷方式设置，默认是`NumPad *`，我真不知道是哪个键，于是统一改成`command +`
- 代码风格设置(直接在Preferences里面搜索设置项)
  - 赋值语句等号对齐: `Align consecutive assignments`
  - 数组内键值对对齐: `Align key-value pairs`
  - 类变量定义等号对齐并且变量也对齐: `Class field/constant groups -> Align fields in columns & Align constatns`
  - 简单的函数直接在一行: `Simple methods in one line`
  - 函数参数多行时自动对齐: `Function/constructor call arguments -> Align when multiline`
  - 函数参数多行时括号和第一个参数换行: `Function/constructor call arguments -> New line after '()'`
  - 函数参数多行时将反括号单独一行: `Function/constructor call arguments ->Place ')' on new line`
  - 函数注释中描述和参数之间空一行`PHPDoc -> Blank line before the first tag`
- 

### Intellij IDEA

- 自动生成`serialVersionUID`的设置：`Preferences->Editor->Inspections->Serialization issues->Serializable class withou 'serialVersionUID'`勾选上
- 使用`tomcat`运行`Maven`项目。在`Run->Configurations`中添加配置，选择`maven`，然后直接在`Command line`中输入`tomcat:run`即可
- 使用`jetty`运行`Maven`项目或者出现`No plugin found for prefix 'jetty' in the current project and in the plugin groups`错误。在`Run->Configurations`中添加配置，选择`maven`，然后`Working directory`中选择项目的`web`目录，最后`Command line`中输入`org.mortbay.jetty:maven-jetty-plugin:run`

### PhpStorm

[EAP 版本下载地址](https://www.jetbrains.com/phpstorm/eap/)

### PyCharm

[EAP 版本下载地址](https://www.jetbrains.com/pycharm/nextversion/)