---
title: "修改U盘图标"
date: 2014-10-30 12:54:14
categories: 就是爱玩
---
虽然用U盘装过很多次系统了，但昨天突然感觉制作完win7启动盘后，那个图标也太丑了吧。所以毅然决定改了一下，通过这种改动，无论是在什么电脑上都能显示出来的。

# 1.制作图标

U盘的图标其实png, jpg, ico什么类型的都支持的，但是为了美观，最好选择png或ico，我就用的ico，因为这两者会把透明部分真正透明化。至于怎么
制作ico，可以使用Photoshop修改好了过后保存为png图片，然后在线将png转换为ico格式：[图标在线转换工具](http://www.img2i
co.net/)

# 2.在U盘根目录新建文件autorun.inf

内容如下：



    [AutoRun.Amd64]
    icon=haofly.ico




    [AutoRun]
    icon=haofly.ico


# 3.将图片haofly.ico拷贝到U盘根目录

# 4.结果如下

![](http://7xnc86.com1.z0.glb.clouddn.com/modify-u-disk-logo.png)﻿  
