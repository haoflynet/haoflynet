---
title: "Charles Mac下的抓包工具"
date: 2017-08-27 22:52:39
categories: tools
---

相比于强大的`wireshark`来说，`Charles`的功能算是十分局限了，因为`Charles`只能用于http/https的抓包。但是术业有专攻，`Charles`的体验比`wiresharek`好了好多倍。之所以最近要用到`Charles`，是因为`wireshark`的https抓包比较鸡肋，设置复杂，不同的电脑可能抓取不到想要的结果。所以我选择了`Charles`，当然是试用版啦，能试用30天，试用期以后能正常使用，不过每次试用不超过半小时，超过后不保存就退出了，有点儿恶心。`WireShark`的原理是监听网卡，而`Charles`的原理则是非常简单的设置代理。其主要的特点有:

- 抓取https和http，外观展示类似postman，十分详细并且结构化
- 能改变请求的内容
- 能改变响应的内容
- 能模拟弱网环境
- 能做压力测试

### Charles的基本设置

1. 点击设置按钮然后进入`Proxy Setting`，设置Http代理
   ![Http代理设置](https://haofly.net/uploads/charles_1.png)
2. 系统代理设置
   ![](https://haofly.net/uploads/charles_2.png)
3. 安装Charles的证书: Help -> SSL Proxying -> Install Charles Root Certificate，安装证书，并完全信任该证书
   ![Mac 钥匙串管理](https://haofly.net/uploads/charles_3.png)
4. 虽然设置了ssl证书，但是默认并没有对每个请求开启https的抓取，还需要针对单独的请求进行选择，在请求上面右键选择`SSL Proxy: Enabled`
   ![](https://haofly.net/uploads/charles_4.png)



###Charles抓取移动端设备iPhone过程

1. Mac上开启Wifi热点

2. 手机连接Mac的Wifi，在wifi详情的最下面设置http代理，代理地址即使路由地址，也即mac的地址

   ![](https://haofly.net/uploads/charles_6.png)

3. 选择Help -> SSL Proxying -> Instanll Charles Root Certificate on a Mobile Device or Remote Browse。在移动端上面安装
   ![](https://haofly.net/uploads/charles_5.png)

4. 这样和mac端一样进行抓取。抓取示例:
   ![](https://haofly.net/uploads/charles_7.png)

##### TroubleShooting

- **Charles的网络出现不可描述的问题**: 关闭系统的其他代理，例如vpn和ss。
- **想要解开所有的HTTP/HTTPS请求？不可能的。**:移动端不像web端，能够看到所有的源码。如果对post的data进行加密，即使是HTTP也不能解开。当然移动端也有apk包反编译的工具，但并不是每次都能成功，所以和web端爬虫更相似的一种万能方法是模拟真机操作。我的想法是使用安卓模拟器，然后在上面进行点击操作，这一点我正在试验。


##### 相关文章

[Charles 从入门到精通](http://blog.devtang.com/2015/11/14/charles-introduction/)