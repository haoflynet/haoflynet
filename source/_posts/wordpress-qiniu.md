---
title: "七牛镜像存储之wordpress插件的安装及测试"
date: 2014-08-29 07:52:28
categories: 编程之路
---
七牛镜像存储介绍

镜像存储就是将自己服务器上的静态内容使用七牛云存储作为镜像服务器，这样网站的用户在访问页面的时候访问的其实是七牛云里面的数据，网站本身的服务器可不放置该静态
资源，这样不仅可以大大减少自己网站的所用空间，还能显著提升访问速度。(本文所有图片均已使用七牛插件做镜像工具，可以查看图片链接，显示的是qiniu.com)
。下面是用户类别以及各种优惠：  
![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_0.jpg)  
简单操作过程

1.注册并新建一个空间：[官网操作指南](https://portal.qiniu.com/tutorial/index "Link:
https://portal.qiniu.com/tutorial/index" )

2.对空间进行设置：  
![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_1.jpg)  
在镜像存储中设置自己的域名，域名设置可以绑定自己的域名，但是只能标准用户使用，我们可以直接使用七牛提供的二级域名

3.wordpress获取插件并安装，插件名称为：WPJAM 七牛镜像存储

4.设置七牛镜像存储插件  
![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_2.jpg)  
![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_3.jpg)  
其中，ACCESS KEY和SECRET KEY在七牛网站的帐号设置里面的密钥处获取

本地设置：主要设置的是要保存文件的后缀  

![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_4.jpg)其它地方均不用设置，但写完博
客并发布后，可以看到七牛空间上已经有刚才上传在wordpress的图片等了，此时就可以在wordpress多媒体里删除该图片，图片依然可以访问。  
![](http://7xnc86.com1.z0.glb.clouddn.com/wordpress-qiniu_5.jpg)  
