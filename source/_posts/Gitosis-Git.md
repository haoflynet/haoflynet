---
title: "使用Gitosis搭建Git服务器的过程"
date: 2014-09-23 22:39:35
categories: 编程之路
---
参考文章：<http://blog.csdn.net/davidsky11/article/details/23023729>

**环境：Ubuntu14.04_server(Virtualbox虚拟机里面) + windows7 其中，windows7里面已经安装好了[git for windows](http://msysgit.github.io/)，且ubuntu里已经用apt-get方式安 装了git这个软件，还有就是已经能通过ssh访问虚拟机了。**

具体步骤：

# Step1：安装与配置几个软件



    sudo apt-get install git git-core openssh-server python-setuptools


添加git用户



    sudo groupadd git
    sudo useradd git -g git -m
    sudo passwd git


全局配置，这里的name和email可以随便设置不影响，因为生成key的时候是按照当前的linux登录帐号生成的



    git config --global user.name "haofly"
    git config --global user.email "haofly@server-pc"

安装gitosis，随便在哪个目录都行



    git clone https://github.com/res0nat0r/gitosis.git
    cd gitosis
    sudo python setup.py install

#  Step2：服务器的配置

虽然是服务器的配置，但这里需要在主机windows上面配置一下(当然可以在同一台电脑上配置，但是为了不搞混，建议最好服务器和客户端分开)
在客户端，即git管理员的PC上，要先安装上git软件，windows就装上git for
windows即可，linux上git即可，在gitbash中，生成密钥：



    ssh-keygen -t rsa

置于密钥保存在哪儿和密码的设置，默认即可。要记住路径，在我的PC上生成的密钥在**_C:\\Users\\haofly.ssh_**里面，该文件夹内有三个文件：
id_rsa, id_rsa.pub, known_hosts其中id_rsa.pub就是公钥，现在要把公钥上传到git服务器上(注意：如果PC与虚拟机必须
要有网络端口转发，那么git的端口是9418)。在gitbash输入(其中的IP地址是PC访问虚拟机里面服务的地址)



    scp C:\\Users\\haofly.ssh\\rsa.pub git@169.254.217.173:/tmp/id_rsa.pub

然后，回到服务器里：



    sudo chmod a+r /tmp/id_rsa.pub
    sudo -H -u git gitosis-init < /tmp/id_rsa.pub


此时会提示(额，我电脑上是中文，忘了是什么了)： Initialized empty Git repository in
/home/repo/gitosis-admin.git/ Reinitialized existing Git repository in
/home/repo/gitosis-admin.git/ 然后再改变权限



    sudo chown git:git /home/git/repositories
    sudo chmod 755 /home/git/repositories
    sudo chmod 755 /home/git/repositories/gitosis-admin.git/hooks/post-update

#  Step3：建立测试仓库

在服务器上新建一个裸仓库



    su git
    cd
    cd repositories
    git init --bare test.git

此时虽然新建了一个仓库，但是是个裸仓库，不能被clone下来，需要让管理员为其分配权限。 在test.git文件夹内有如下重要文件：
HEAD文件：存放根节点的信息，Git采用这种树形结构来存储版本信息。 refs目录：存储当前版本控制目录下的各种不同引用，即各个分支树的信息，其下有hea
ds/remotes/stash/tags四个子目录，分别存储对不同的根、远程版本库、Git栈和标签的四种引用。
logs目录：根据不同的引用存储了日志信息。 test.git/object/pack：这里存放的就是我们上传的东西，但是被打包成了idx和pack结尾的文
件。所以如果上传了后发现找不到，其实是在这里面的。

# Step4：修改gitosis配置文件

现在在管理员的PC上(就是刚刚上传公钥的那台机器上，我这里就是windows主机)，把管理的仓库clone下来，找个地方，然后在gitbash里执行(如果不
行，试试全路径/home/git/repositories/gitosis-admin.git)：



    mkdir admin
    cd admin
    git clone git@169.254.217.173:gitosis-admin.git
    cd gitosis-admin
    vim gitosis.conf

clone下来会有两个东西，一个是keydir文件夹，里面存储了所有需要访问git服务器的用户的ssh公钥，比如我的keydir/haofly@HAOFLY
_PC.pub，另一个文件就是gitosis.conf，里面配置了各个仓库的访问权限，例如：



    [gitosis]
        [group gitosis-admin]
            writable = gitosis-admin
            members = haofly@HAOFLY-PC
        [group team]
            writable = test
            members = haofly@ubuntu  haofly@HAOFLY-PC  pitter@PITTER-PC

这个配置文件很直白，有多个组，每个组的writable代表一个仓库，members表示具有读写权限的用户，用户的公钥必须在keydir文件夹内。
然后把配置文件push到服务器上去



    git add .
    git commit -m "add test and someusers"
    git push origin master

#  Step5：测试

空仓库是不能clone的，需要一个具有write权限的人初始化一个版本，在客户端执行：



    mkdir test
    cd test
    git init
    echo "hehe" > hello
    git add .
    git commit -m "initial vesion"
    git remote add origin git@169.254.217.173:test.git
    git push origin master

如果push成功了，那么可以去服务器上看看，但千万不要妄图去找你库里面的文件，因为你上传的东西，git服务器会把它弄成idx和pack文件，我不大清楚git
的原理，反正是这里面的_**/home/git/repositories/test.git/objects/pack/ **_

原文中其它配置我还没试过。。。
