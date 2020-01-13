---
title: "我用的IDEs及其配置"
date: 2019-02-26 21:32:00
updated: 2020-01-09 09:08:00
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

- 最好只安装一个`IDEA`，`PhpStrom/PyCharm/WebStorm`可以以插件的方式引入，而且支持都非常不错

- `Intellij IDEA`的[配置文档](https://www.jetbrains.com/help/idea/javascript-specific-guidelines.html)

- 常用快捷键

  ```shell
  Alt+Enter # 万能的快捷键，弹出你用鼠标悬停看到的提示的帮助
  Shift+option	# 多列选择
  ```

- 展开左边文件目录树快捷方式设置，默认是`NumPad *`，我真不知道是哪个键，于是统一改成`command +`

- 手动将一个文件夹变为`resources`目录或者`tests`目录，只需要在左侧目录树右键需要设置的目录，选择`Mark Directory as`，可以选择设置成`Test Sources Root/Resources Root/Test Resources Root/Excluded`等

- 代码风格设置(直接在Preferences里面搜索设置项)
  - 赋值语句等号对齐: `Align consecutive assignments`
  - 数组内键值对对齐: `Align key-value pairs`
  - 类变量定义等号对齐并且变量也对齐: `Class field/constant groups -> Align fields in columns & Align constatns`
  - 简单的函数直接在一行: `Simple methods in one line`
  - 函数参数多行时自动对齐: `Function/constructor call arguments -> Align when multiline`
  - 函数参数多行时括号和第一个参数换行: `Function/constructor call arguments -> New line after '()'`
  - 函数参数多行时将反括号单独一行: `Function/constructor call arguments ->Place ')' on new line`
  - 函数注释中描述和参数之间空一行`PHPDoc -> Blank line before the first tag`
  

### Intellij IDEA

- **自动生成`serialVersionUID`的设置**：`Preferences->Editor->Inspections->Serialization issues->Serializable class withou 'serialVersionUID'`勾选上
- **使用`Tomcat`运行`Maven`项目**。在`Run->Edit Configurations`中添加配置，选择`maven`，然后直接在`Command line`中输入`tomcat:run`即可。如果这种方式有问题，那么可以自己去`Tomcat`[官网](https://tomcat.apache.org/download-90.cgi)下载最新版的`Tomcat`(Mac可以下载`tar.gz`格式的文件，下载后解压即可)，然后在`IDEA`中通过`mav package`将项目打成war包，再添加运行配置`Run->Edit Configurations`添加`Smart Tomcat`(**需要先下载Smart Tomcat插件，自带的Tomcat Server我配置过好几次都没能成功**)，填入以下几个必要配置:
  - Tomcat Server: 选择刚才解压后的目录即可，例如`/Users/name/Downloads/apache-tomcat-9.0.27`
  - Deployment Directory: 填入war包的生成目录，例如`./project-web/src/main/webapp`
  - Context Path: 填入webapp的目录，前缀直接填斜杠即可，例如`/project-web`
- 使用`jetty`运行`Maven`项目或者出现`No plugin found for prefix 'jetty' in the current project and in the plugin groups`错误。在`Run->Configurations`中添加配置，选择`maven`，然后`Working directory`中选择项目的`web`目录，最后`Command line`中输入`org.mortbay.jetty:maven-jetty-plugin:run`。在运行前，需要先`mav install`一下，可以直接在ide中右边侧栏选择`Maven`然后选择根目录`Lifecycle->install`
- 运行`spring`项目直接点击运行`Application.java`即可
- 如果本地有两个项目，其中一个依赖于另外一个作为jar包，可以在另外一个里面先`maven install`然后在本地的仓库目录即可更新该包，这样依赖的那个项目`maven reimport`就能够更新了
- **添加依赖不生效解决方法**
  - 可能是网络问题导致没有拉取到最新的仓库列表，搭梯子试试
- **IDEA运行Tomcat报错 java.lang.NullPointerException**，项目都还没有启动就报这个错，按照如下方法解决:
  - 检查项目目录是否已经生成了`war`包
  - 看[论坛](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360000416199-Error-running-Tomcat-java-lang-NullPointerException)可能是`bug`，可以通过随便修改运行配置的方式恢复`Run->editConfiguration`，选择`Tomcat`配置随便修改其中某个值，然后保存
- **`maven reimport`不起作用**: 可以先后采取以下几种方法:
  - 删除依赖包路径中的源码包
  - `File->Invalidate Caches / Restart`
  - 重启`Idea`
  - 关闭`Idea`，删除项目目录下的`.idea`文件夹，再重新打开`Idea`
- **Could not autowire. No beans of 'xxx' type found**: 这篇文章提供了7个方法，我最终选择了修改检测级别的方法，因为其他的方法都需要对代码有改动。
- **IDEA 运行Django项目提示No module named xxx**: 需要在`File->Project Structure->modules`中将当前`module`删除，然后新建`module`，选择当前项目的根目录，将当前项目设置为一个`Django`项目

### PhpStorm

- 设置PHP版本: `Perferences->Languages->Frameworks`
- 取消注释引入全名的警告: `Perference->搜索Fully qualified name usage`，右边的勾取消

[EAP 版本下载地址](https://www.jetbrains.com/phpstorm/eap/)

### PyCharm

[EAP 版本下载地址](https://www.jetbrains.com/pycharm/nextversion/)

### WebStorm

- 配置`Prettier`

  - 首先需要安装`prettier`，可以全局安装也可以安装在当前项目

  - 在`Preferences->Languages & Frameworks->Javascript->Prettier`中设置`prettier package`的路径，例如`~/.nvm/versions/node/v10.16.2/lib/node_modules/prettier`

  - 然后`Preferences->Keymap`，搜索prettier关键字，设置`Reformat with Prettier`的快捷键，我一般设置成: `Shift + alt + cmd + P`

  - 如果想要保存文件后自动格式化，就需要再配置`watcher`，在`Preferences->Tools->file Watchers`，点击"+"添加一个`prettier`类型的watcher，默认设置，然后保存即可

    