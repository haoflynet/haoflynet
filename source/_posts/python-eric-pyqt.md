---
title: "Python3+Eric5+PyQt4环境搭建"
date: 2014-08-13 00:10:00
categories: 编程之路
---
Eric是Python语言的一个IDE，它支持Python+PyQt(Python的一个图形库)进行可视化图形界面的开发。目前最新版本Eric5支持到Pyt
hon3.4和PyQt4，目测Eric6马上就要出来了，并且Eric6支持PyQt5。当然，Eric还支持其它的一些开发语言，不过主要还是用来开发Pytho
n的图形界面。Python为数不多的IDE中Eric算是很好的了，不仅支持多语言，而且界面好看，调试功能强大，对于熟悉QT的人就更得心应手了，因为PyQt是
完全把C++的QT库拿来改成了Python自己的库，类和函数的用法几乎一致，再加上Python语言本身的简洁和强大，是我很喜欢的一套工具。这里就简要介绍一下
其环境的搭建过程。

1.下载必要的几个文件(在下载的时候一定要注意64位还是32位，必须一致)：

Python3：[下载页面](https://www.python.org/downloads/windows/) 可以下载最新的版本

PyQt4：[下载页面](http://www.riverbankcomputing.co.uk/software/pyqt/download)
注意Eric目前只支持到PyQt5，不过Qt的版本可以到5，我下载的就是PyQt4-4.11.1-gpl-Py3.4-Qt5.3.1-x64.exe

Eric5：[下载页面](http://sourceforge.net/projects/eric-ide/files/eric5/stable/) ，选择
一个最新稳定版，进入后记得把语言包一起下载，我下载的就是eric5-5.4.6.zip和eric5-i18n-tr-5.4.6.zip，注意windows版
本是zip压缩文件tar.gz是针对linux的

2.安装Python3：点击msi文件默认安装就行，千万不要修改路径，不然之后所有东西都要修改路径

3.安装PyQt4：点击exe文件默认安装，勿改路径，安装完后，打开Python
IDLE(Python安装完后开始菜单中会有这么一个选项)，输入import PyQt4看是否已经成功安装该模块

4.安装Eric5：将下载后的两个zip同时解压，然后将解压后的文件夹直接放到C盘下，点进去后点击install.py进行安装，一会儿就安装好了

5.验证安装：最后在C:\\Python34目录里面找到eric5.bat(这就是Eric的启动文件，可以在桌面建立一个快捷方式方便以后打开)

6.初始化配置：第一次进入会提示进行初始化配置，此时界面还是英文的，不过没关系，下次打开就是中文了，我们先来进行如下简单配置：

首先是Editor->AutoCompletion->QScintilla勾选上Show single(显示单条)和Use fill-up
characters(使用填充符号)和from Document and API files(源文件来自文档和API文件)

然后是Editor->API勾上Compile APIs
automatically(自动编译API)，在下面的language选择Python3，然后在下面选择Add from installed
APIs(从已安装的API添加)选择eric5.API

最后，确定，重启，就可以了

7.Hello World：下面开始尝试第一个Python GUI程序

项目->新建：

![](http://7xnc86.com1.z0.glb.clouddn.com/python-eric-pyqt_1.jpg)  

项目名称：test，然后在项目文件夹里新建一个文件夹test，点击OK即可新建项目

新建窗体：在窗体标签栏里点击右键新建窗体，然后会提示选择窗体类型，直接选择对话框，然后OK，然后会叫你输入ui文件的名称，之后就会进入QtDesigner(
Qt设计师)设计界面

![](http://7xnc86.com1.z0.glb.clouddn.com/python-eric-pyqt_2.jpg)  

直接将左边的按钮控件拖到主界面，然后双击该按钮可以修改其显示的文字

![](http://7xnc86.com1.z0.glb.clouddn.com/python-eric-pyqt_3.jpg)  

保存后，返回Eric界面，会发现刚才新建的ui文件，然后对着它右键->编译窗体，再切换到源代码标签可看到编译生成的py文件，这就是Python可执行的文件了
，右边就是自动生成的代码，此时就可以直接按F5运行，就会出现那个Hello World!对话框了

![](http://7xnc86.com1.z0.glb.clouddn.com/python-eric-pyqt_4.jpg)  

现在就踏上你的PyQt之旅吧，不过PyQt没有多少的中文资料，如果对QT熟悉，可以直接到网上找找“PyQt_精彩实例分析”(也可以联系我)



封面图片来自Pixebay
