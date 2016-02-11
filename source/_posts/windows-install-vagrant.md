---
title: "windows环境下Vagrant(Docker)的安装、打包以及Vagrant Manager的安"
date: 2014-12-29 19:08:00
categories: 编程之路
---
_Docker：是一个开放源代码软件专案，在软件容器下自动布署应用程序，借此在Linux操作系统上，提供了一个额外的软件抽象层，以及操作系统层虚拟化的自动管
理机制[2]。Docker利用Linux内核中的资源分离机制，例如cgroups，以及Linux内核名称空间，来建立独立的软件容器（containers）。
这可以在单一Linux实体下运作，避免启动一个虚拟机器造成的额外负担。(维基百科)_

Docker无疑是2014年人们谈论最多的虚拟开发环境构建工具，在我看来它是VirtualBox虚拟机最佳的替代方案，使用它的理由有三点：
1.轻量级，一个box只需要几百兆(Vagrant) 2.部署方便，有现成的[base
boxes可供下载](http://www.vagrantbox.es/)(Vagrant)，并且可以自己制作Image
3.运行流畅，几秒开机，占用内存十分的少(在我的电脑上，它甚至比Chrome占用的内存还要少)

而本文所要说的Vagrant这是其在Windows上的替代方案，它是使用VirtualBox动态创建和配置虚拟环境。它基于Ruby，但必须依赖其他的虚拟环境
构建工具，比如VirtualBox或者VM等。下面主要介绍其安装部署过程。

**注：有一个快速的生成Vagrantfile的网站：<https://puphpet.com，可以选择不同的操作系统，不同的开发环境(lamp,lnmp)，如果设置了apache的域名，那么需要修改主机的host文>件**

**基础环境：Windows 7 + Git for Windows**

  1. ## 下载并安装基本工具

Oracle VM VirtualBox：<https://www.virtualbox.org/wiki/Downloads>
Vagrant：<https://www.vagrantup.com/downloads.html>
安装完Vargrant后，可以直接在bash里查看是否安装成功


        $vagrant -v
    Vagrant 1.7.1

  2. ## 下载box

Vagrant提供了一些常用的人们已经打包好了的box镜像，当然可以使用vargrant命令进行下载，但是总没有迅雷快吧，所以直接去官网下载：<http:/
/www.vagrantbox.es/> 其中，我选择的是Ubuntu Server Trusty 14.04 amd64：<https://oss-bin
aries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box>[
](https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-
amd64-vmwarefusion.box)注意是virtualbox版本还是vmware版本，大小只有399M

  3. ## 初始化工作目录

`vagrant init`  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_1.jpg)  
此时会生成一个Vagrantfile文件，它就是该虚拟机的配置文件，可在里面配置端口或者文件的映射规则。
**注**：其实添加box可以在任意位置添加，vagrant应该只是记录了其路径，然后`vagrant init +
name`才是初始化的时候指定所需要的box，而默认的`vagrant init`会默认去寻找名为base的镜像。  

  4. ## 添加镜像

`vagrant box add`  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_2.jpg)  
其中"base"就是你给镜像取的名字，`vagrant box
list`可以列出当前所有的box(不仅仅是该目录)，需要注意的是，由于我之前添加了一个同名的镜像，并且没删除干净，所以这里添加了一个`--force`参数

  5. ## 启动

![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_3.jpg)  
这就是其启动过程，可以发现它的一些基本设置：如SSH端口为2222，用户名密码均是vagrant，/vagrant映射到本地的F:/docker/ubunt
u-server

  6. ## 连接进入

当虚拟机启动后，可以使用SSH连接工具XShell或者putty进行登录： 地址：127.0.0.1 端口：2222(虚拟机不同，端口会变的)
用户名：vagrant 密码：vagrant 或者直接使用vagrant命令登录：`vagrant ssh`  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_4.jpg)  
到这里，就可以确定安装完成了。 PS：所有创建了的box也都可以通过VirtualBox进行查看和配置：  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_5.jpg)  

# Vagrant box的打包

通常，官网的list列表并不能提供我们自己所需要的运行环境，比如我有时候需要14.04的LAMP环境或者LNAMP环境，但又不想每次都重新安装一下，这时候就
可以去官网下载一个干净的base，对其修改后打包成自己的box，以后谁要用就直接取，里面已经安装好了所需要的环境了，打包很简单，使用的是`vagrant
package`命令，但首先得启动该虚拟机：  
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_5.png)  
注意我在该虚拟机的root用户目录里新建了一个名为`haofly`的文件，待会儿方便证明其确实是我修改后的box，下面只需要将`package.box`添加
到vagrant即可使用它来创建新的虚拟机了，为了方便管理，我将其复制了出来并重命名为`ubuntu-14.04-amd64-lamp-20141225.b
ox`：  

![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_6.jpg)  

# Vagrant Manager的安装

vagrant
manager是一个正在开发中的vagrant的管理工具，主页在[https://github.com/lanayotech/vagrant-
manager-windows ](https://github.com/lanayotech/vagrant-manager-windows "Link:
https://github.com/lanayotech/vagrant-manager-windows" )

安装步骤：

  1. 下载安装 到其releases列表进行下载：<https://github.com/lanayotech/vagrant-manager-windows/releases> 然后直接运行安装即可。不过要是出现以下错误   
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_7.jpg)  
[ ](http://haofly.net/wp-content/uploads/2014/12/windows-install-
vagrant5.jpg)表示你的电脑没有安装`.NETFramwork 4.5`那么就去安装，但如果这里点击“是”那么会跳到4.5.2去，我没安装上，所以
之后直接下载了4.5([下载地址](http://www.microsoft.com/zh-
cn/download/details.aspx?id=30653))安装上了

  2. 界面   
![](http://7xnc86.com1.z0.glb.clouddn.com/windows-install-vagrant_8.jpg)  
它没什么单独的界面，就是在右下角的一个控制图表，点击就可以了。

  3. 需要注意的是：vagrant manager目前存在一个很大的缺陷就是只能操作C盘下的box，不然什么操作都会出现错误 _A Vagrant environment or target machine is required to run this command. Run `vagrant init` to create a new Vagrant environment. Or, get an ID of a target machine from `vagrant global-status` to run this command on. A final option is to change to a directory with a Vagrantfile and to try again. _其实，开发人员也一直在关注着这个问题：<https://github.com/lanayotech/vagrant-manager-windows/issues/8>

# 附

Vagrant常用命令：

vagrant box add name：添加box vagrant box list：列出当前所有的box vagrant box remove
name：列出某个box(名字就是自己给取的，比如上面的base) vagrant box repackage name：对某个box重新打包
vagrant init [name]：初始化当前目录为工作目录 vagrant up [name]：启动虚拟机 vagrant destroy
[name]：删除虚拟机 vagrant suspend [name]：暂停某个box vagrant reload [name]：重新加载 vagrant
resume [name]：恢复虚拟机 vagrant halt [name]：关闭虚拟机 vagrant ssh：连接虚拟机 vagrant
package --output name：如果对虚拟机的配置进行修改过后，如果想把当前环境打包，可使用这个命令 vagrant
status：查看虚拟机状态

## TroubleShooting

  1. 在linux环境下，共享目录的权限无权限问题： `Vagrant Synced Folders Permissions` 解决方法是在Vagrantfile里面进行如下配置：

        config.vm.synced_folder "/docker/ubuntu/", "/var/www/html",
        id: "vagrant-root",
        owner: "nobody",
        group: "nobody",
        mount_options: ["dmode=775,fmode=664"]

  2. 连接mysql数据库出现如下错误：

        Lost connection to MySQL server at 'reading initial communication packet', system error: 0

那么应该是mysql的bind-address未配置正确，应该将其改为eth0的地址，而不是该虚拟机的IP地址，当然，改为0.0.0.0也行

  3. 集群(同时开启多个虚拟机，虚拟机之间通过IP访问)，vagrantfile可以这样配置，例如：

        # -_- mode: ruby -_-




    # vi: set ft=ruby :




    Vagrant.configure(2) do |config|
        config.vm.define :master do |master|
            master.vm.provider "virtualbox" do |v|
                v.memory = "1024"
                #v.gui = true
            end
            master.vm.box = "django"
            master.vm.hostname = "master"
            master.vm.network "private_network", ip: "192.168.111.10"
            master.vm.network "forwarded_port", guest: 8000, host: 8000
            master.vm.network "forwarded_port", guest: 3306, host: 3307
            master.vm.synced_folder "F:/workspace/wh_operation", "/django"
        end




        config.vm.define :slave do |slave|
        slave.vm.provider "virtualbox" do |v|
            v.memory = "1024"
            #v.gui = true
        end
        slave.vm.box = "django"
        slave.vm.hostname = "slave"
        slave.vm.network "private_network", ip: "192.168.111.11"
    end


end
