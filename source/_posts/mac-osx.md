---
title: "MacOS教程"
date: 2016-09-06 01:02:30
updated: 2020-08-16 22:11:00
categories: system
---
## Mac自带截图功能

- `Command + Shift + 4` 普通截图
- `Command + Shift + 4`，然后按`空格`，对指定窗口截图
- `Command + Shift + 3` 全屏截图

## Mac瘦身

- `~/Library/Application Support/Code/User/workspaceStorage`: VS COde的工作区文件夹唉，但是所有的扩展都会重建这个文件夹，把年代久远的删除了

## Shell配置使用

### Mac使用Iterm2的Profile功能实现类似ssh标签/xshell登录的功能

在`Preferences`中不仅可以设置默认`Profile`的窗口样式等，还是通过新建不同的`Profile`来实现自动登录。例如: ![](https://haofly.net/uploads/macos_01.png)

这样如果想要进入某个服务器，只需要在`iterm2`中点击顶部菜单`Profiles->aliyun`即可直接进入服务器。对于复杂的输入密码的场景，可以参考[Linux 手册](https://haofly.net/linux)的`expect`进行配置

### mac shell使用rz、sz直接上传或者下载服务器文件

- 需要注意的是在使用`except`登录服务器的情况下，使用`lrzsz`不会起作用

首先使用`brew install lrzsz`安装命令行工具

然后保存iterm2-send-zmodem.sh 和iterm2-recv-zmodem.sh[两个脚本](https://github.com/aikuyun/iterm2-zmodem)到`/usr/local/bin`目录下

打开`iterm2`，`Perferences->Profiles->Advanced->Triggers->Edit`，添加如下`trigger`

```shell
\*\*B0100			Run Silent Coprocess	/usr/local/bin/iterm2-send-zmodem.sh
\*\*B00000000000000	Run Silent Coprocess	/usr/local/bin/iterm2-recv-zmodem.sh
```

### Homebrew配置使用

```shell
export ALL_PROXY=socks5://127.0.0.1:1080	# homebrew走ss代理
```

### 查看每个CPU的负载/GPU负载

`活动监视器->窗口->CPU使用率/CPU历史记录/GPU历史记录`

### 修改终端欢迎字符

```shell
vim /private/etc/motd	# 直接输入即可
```

## 系统管理命令

```shell
dscacheutil -q group	# 查看所有用户和组
```

## 更换文件图标

http://www.cnblogs.com/wormday/archive/2011/05/06/2038703.html

## 与Android联动

- `brew cask install android-file-transfer`可以管理小米手机上的文件

## 自制iPhone铃声

[iTunes 簡單自製 iPhone 鈴聲不求人](http://applefans.today/blog/1266100502)

### Mackup配置备份

```shell
brew install mackup

vim ~/.mackup.cfg进行配置
[storage]
engine = file_system	# 表示用文件系统进行存储
path = /Users/haofly/OneDrive	# 指定路径

mackup backup	# 备份命令
mackup restore	# 数据恢复
mackup uninstall# 将配置文件拷回原来的系统目录
```

## ios safari移动端真机调试

https://www.jianshu.com/p/ed4b1bfb57dc

## TroubleShooting

- **磁盘空间爆了，重启后spotlight一直显示正在索引**: 原因可能是误删了索引的文件(索引文件确实有哦几个G)，修复需要执行以下几个命令：

   ```shell
   sudo mdutil -i off /
   sudo mdutil -E /
   sudo mdutil -i on /
   ```

- **Library not loaded: /usr/local/opt/readline/lib/libreadline.6.2.dylib Referenced from: /usr/local/bin/gawk Reason: image not found**: 执行下面这个命令更新所有`brew`安装的包可以修复

  ```shell
  brew upgrade
  ```
  
- **明明安装了xcode命令行工具却还是提示找不到**，可以用这个命令重装一下: 

  ```shell
  xcode-select --print-path	# 一般会打印/Library/Developer/CommandLineTools
  sudo rm -r -f /Library/Developer/CommandLineTools
  xcode-select --install	# 重新安装
  ```

- **Macos使用ssh登陆linux服务器无法显示中文**，需要设置终端的字符集:

   ```shell
   # vim ~/.zshrc，在底部输入如下内容，然后保存重启终端
   export LC_ALL=en_US.UTF-8  
   export LANG=en_US.UTF-8
   ```

   

   

   
