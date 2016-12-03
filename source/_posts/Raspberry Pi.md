---
title: "Linux Server(Raspberry Pi)安装运行浏览器"
date: 2015-12-21 02:17:38
categories: system
---
原打算使用Splinter模拟真人访问浏览器的动作，但它必须有浏览器支持，而且仅支持Firefox和Chrome浏览器或者远程浏览器，最先是想使用Chrom
eDriver，但是无论怎么折腾也安装不上，于是用Firefox，发现一篇很好的教程，[原文地址](http://www.installationpage.
com/selenium/how-to-run-selenium-headless-firefox-in-ubuntu/)。它这个版本被称作Selenium
headless firefox(无头？)  

步骤如下：  

  1. 首先，添加repository，并安装firefox：  


    sudo add-apt-repository ppa:mozillateam/firefox-stable
    sudo apt-get update
    sudo apt-get install firefox

  1. 安装Xvfb：是用来虚拟X服务程序，是用来实现X11显示的协议  


        sudo apt-get install xvfb
    sudo Xvfb :10 -ac  # 10表示编号

  1. 设置环境变量  


        export DISPLAY=:10
    firefox

  1. 现在可以使用firefox了
