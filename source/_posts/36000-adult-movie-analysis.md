---
title: "对三万六千部大电影的分析"
date: 2017-09-21 22:52:39
categories: 程序人生
---

最近年轻气盛、心血来潮、突发奇想地决定去分析一下特定类型电影的数据，我的爬虫技术自我感觉还算不错，但是爬取数据来具体该如何分析，我只能算是个新手。

练手的具体网站就不说了，总共有`36956.avi`条数据，总共发送约4000个请求，切换了上百个代理，不得不说，在同类型网站里面，该网站的的反爬策略算是中规中矩的。以下是我对本次爬取数据的基本描述与简单分析:

##### 基本数据

|               | statistics    |
| ------------- | ------------- |
| 总数量           | 36956         |
| 总大小(G，我可不会下载) | 940           |
| 总时长(hour)     | 9688.56       |
| 总观看量          | 2,418,738,994 |

##### 排行数据

观看量排名前十的影片:

![观看量排名前十的影片](https://haofly.net/uploads/36000-adult-movie-analysis_0.png)

观看量排名后十的影片: 

![](http://ojccjqhmb.bkt.clouddn.com/36000-adult-movie-analysis_1.png)

好评率排名前十的影片(这个指标基本上不能代表什么，该网站没人评分少的基本上都能很高，评分算法有问题):

![](http://ojccjqhmb.bkt.clouddn.com/36000-adult-movie-analysis_2.png)

时长排名前十的影片(强撸灰飞烟灭，应该没人看完):

![](http://ojccjqhmb.bkt.clouddn.com/36000-adult-movie-analysis_3.png)

##### 词云

最后来一个词云(分析就不言而喻了，重口味，绝对的重口味)

![](http://ojccjqhmb.bkt.clouddn.com/36000-adult-movie-analysis_4.png)

##### 总结

1. 此次爬虫所使用的技术比较简单，`Python3.6`做主要的程序语言，`requests`做curl请求，`jieba中文分词`做标题分词提取，`skydark/nstools`的繁简转换，`amueller/word_cloud`做词云图片。
2. 有些东西确实看得越多，越重口
3. 我终于知道网上这类网站的分析为什么那么少了，我得去补补了。