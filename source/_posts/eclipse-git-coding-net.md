---
title: "项目成员使用eclipse的Git插件进行版本管理的流程(基于coding.net)"
date: 2014-09-13 14:32:19
categories: 编程之路
---
这才是第一个项目，没想到就遇到这么多问题。这次的主要问题就是和小组成员分管不同的模块，但是每次进行迭代的时候都得把代码传过来传过去，而且虽然是不同的模块，但
难免会遇到修改同一个文件的问题，这时候不仅要自习地去寻找哪些文件有改动，还要去判断小组中其它成员改动的意图，还有就是小组中其它成员上网条件堪忧，只能用手机流
量进行上传下载，这样就造成了时间成本和物质成本的浪费。就目前来说，我们没有搭建SVN的条件，而且我本人也是非常推崇Git的，其与SVN的区别在这里就不详解了
，这里主要就是介绍一下eclipse中EGit插件的用法。

# 1.确认安装

最新的Eclipse IDE应该都自带了EGIT插件的，可以在首选项里面查看：  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_0.jpg)  

# 2.全局配置

在这里点击“Add Entry”里面输入在encoding.net申请的帐号的邮箱和用户名(如果是其它网站就换其它网站的帐号就行了)  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_1.jpg)  

### 3.克隆远程分支到本地

菜单栏--窗口-->打开透视图-->Git Repository Exploring，在该视图里选择Clone a Git
repository或者点击上面的克隆按钮都可：  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_2.jpg)  
然后会出现如下设置界面  

![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_3.jpg)  
其中URI就是项目的地址，可以从coding.net网站上该仓库的“代码”选项处获得，输入URI，会自动获得Host和Repository path，而下面
的User和Password则是该网站的用户名和密码，注意Connection的协议设置，git网站一般提供https和ssh两种方式，端口都是默认端口，这
里不用写。

这里点击下一步就会提示选择哪个分支(master就是默认的主分支)，选择你需要的分支点击下一步  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_4.jpg)  
接下来就是项目在本地的一些设置  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_5.jpg)  
这里可以设置保存的目录，远程分支的名字(默认为origin)，因为我们克隆的就是一个工程，所以可以选择“Import all existing
projects after clone finishes”，那么就会在下载完成后直接导入其中的工程(需要注意的是下载的地方不要放在工作空间里，不然不会导入
或导入失败)。最后在工作空间中就有该项目了：  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_6.jpg)  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_7.jpg)  
可以看到git项目和其它项目不一样的是，凡是git会记录更改的文件或文件夹右下角都有一个圆柱体的东西。

# 4.对本地内容进行更改

下面尝试一下对本地内容进行修改然后提交的过程。
当更改了本地内容过后，需要在项目名称上，右键-->team-->commit将当前的更改提交到本地的上传任务中去(此时并没有上传到远程)  
其中，“Commit message”可以写上你本次的提交信息，注意，提交信息也很重要，可以方便以后查看本次提交主要是提交了什么东西，查看你在这次提交中都做
了些什么，还可以让团队中其它成员大致了解其中的更改。 下面的Author和Committer默认即可 在下面的Files列表框里面就是选择本次需要提交的文件
，需要注意的是git会自动列出本次所有更改过的文件，只需要上传更改过的文件就行了。下面点击"Commit and
Push"(也可点击Commit再用push)![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-
coding-net_8.jpg)其中有一串奇怪的数字“6656cfcb”就是本次提交的commit
id(相当于版本号，方便以后进行回退的操作)，此时在coding.net上面就可以看到刚才的提交了，此时还可在“代码”页面查看刚刚的文件是否已经完成了更改  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_9.jpg)  

# 5.提交合并求

当完成一个功能或者模块时，需要进行项目迭代，这时候就要向项目领导人提交合并请求，合并请求可以直接在网页端完成  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_10.jpg)  
先新建合并请求，注意源分支是你更改的分支，目标分支则是你要把你更改的分支合并到哪里去，这里就是master分支，即主分支。 merge
request标题和内容表示你提交本次合并请求的标题和内容，标题就写明你完成了什么，内容可以详细说明一下你做了什么。  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_11.jpg)  
要想看到自己改动的地方，可以通过最下面的改动明细查看，其中改动的地方用红色标识，红色的在本次提交中被替换成了绿色部分的内容  
![](http://7xnc86.com1.z0.glb.clouddn.com/eclipse-git-coding-net_12.jpg)  
最后点击“提交”

此时，项目负责人那里会收到一封邮件(这功能挺贴心的)提示有了新的提交请求，OK，我只要点击同意合并就算完成了。
