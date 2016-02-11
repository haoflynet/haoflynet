---
title: "Linux+goagent+Chrome配置教程"
date: 2014-05-16 23:13:29
categories: 编程之路
---
本教程来源于[goagent项目](https://code.google.com/p/goagent)  
具体步骤如下：

1.申请Google App Engine并创建appid，由于我早已经申请好，所以就不再赘述，详细申请过程上面那个网站上有的

2.下载最新版的goagent并解压，就在刚才那网站上面下载

3.编辑local/proxy.ini，把其中的appid = goagent，password = 你的密码
中的goagent改成你之前申请的应用的appid


4.安装依赖：

sudo apt-get install python-dev python-greenlet python-gevent python-vte
python-openssl python-crypto python-appindicator  
网站上说要安装gevent1.0其实用apt安装已经是1.0了，所以不用做那一步了5.上传  
在解压后的server目录下执行python uploader.zip

6.运行客户端  
在local目录下赋予proxy.py可执行权限`chmod +x proxy.py`，然后就可以双击执行了，运行过程中请不要关闭

7.设置为开机启动  
就在这个local目录下执行  
`python addto-startup.py`

8.安装浏览器插件  
在谷歌应用中心搜索`Proxy SwitchySharp`并安装

9.配置Proxy SwitchySharp插件：  
选项 -> 导入/导出 -> 从文件恢复 -> local目录下的SwitchyOptions.bak -> 确认

10.安装证书：进入谷歌浏览器的设置 -> 高级设置 -> HTTPS/SSL的管理证书选项 -> 进到授权中心 -> 点击导入 ->
选择local文件夹里面的CA.crt -> 此时会弹出一个选项框，将该框的三种信任方式都勾选上然后确定

10.终于完成了，现在在浏览器上面的switchsharp插件选择GoaGent代理，然后推特和facebook等应该都能正常访问了，别忘了关注我的twit
ter：[豪翔天下](<https://twitter.com/haofly>)



封面图片来自Pixebay
