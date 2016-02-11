---
title: "VirtualBox虚拟机(windows系列)与主机共享文件的方法"
date: 2014-10-30 08:36:28
categories: 编程之路
---
在我的印象里，虚拟机在安装增强功能后是可以直接互相拖放文件的，但不知道为什么最近几个月我安装的都不行啊，所以这里记录一下通过映射来共享文件的方法。

# 虚拟Linux Server

  1. 和win一样，点击虚拟机的_设备->安装增强功能_
  2. 不同的是linux_server 上面不会自动弹出安装界面，而是需要挂载在安装，执行如下命令：

        $ sudo mount /dev/cdrom /media/cdrom
    block device /dev/sr0 is write-protected, mounting read-only
    $ cd /media/cdrom
    $ sudo ./VBoxLinuxAdditions.run

  3. 在设置里面添加共享文件夹：   
![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_0.jpg)  

  4. 记住上面的共享的名称，比如company，那么在linux_server里面就可以看到_/media/sf_company_这一个目录。
  5. 如果在linux_server往那个目录添加东西时出现_Read-only_错误，可能是VirtualBox默认禁止在共享目录里建立链接([stackoverflow解答](http://stackoverflow.com/questions/16724543/executing-collectstatic-on-vbox-shared-folder-gives-read-only-error "Link: http://stackoverflow.com/questions/16724543/executing-collectstatic-on-vbox-shared-folder-gives-read-only-error" ))，此时应该执行如下命令，其中，VM_NAME表示你的虚拟机的名称，SHARE_NAME表示共享的名称(不加前缀sf_) 如果是windows主机，在cmd里执行：

        VBoxManage.exe setextradata VM_NAME VBoxInternal2/SharedFoldersEnableSymlinksCreate/SHARE_NAME 1

如果是linux主机，在shell里执行：


        VBoxManage setextradata VM_NAME VBoxInternal2/SharedFoldersEnableSymlinksCreate/SHARE_NAME 1

# 虚拟Windows

### 1.还是要安装增强功能

![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_1.png)  

安装完成后关机，之所以不重启，是因为还有要设置的地方。

### 2.设置共享文件夹

![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_2.png)  
我一般喜欢把共享文件夹设置为固定分配、自动挂载、完全访问权限。

### 3.添加映射

[![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_3.png)  
](http://haofly.net/wp-content/uploads/2014/10/virtualbox-share-
file-4.png)![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-
share-file_4.png)  
![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_5.png)  
点击浏览，找到文件夹，确定


![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_6.png)  
![](http://7xnc86.com1.z0.glb.clouddn.com/virtualbox-guest-host-share-
file_7.png)  
成功！
