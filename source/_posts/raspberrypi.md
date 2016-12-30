---
title: "玩转树莓派2"
date: 2015-12-08 02:58:50
updated: 2016-12-30 11:03:00
categories: 就是爱玩
---
想在家里做NAS、DNS等私有云服务，但是无奈家里淘汰下来的电脑已无力承担如此重任。没办法了，就只能试试树莓派。不试不知道，一试吓一跳，完全就是一手掌大小的电脑，听说desktop版本还能使用word等软件，虽然只有1GB内存，但是200多块(淘宝店)就能买到这个东西，那是非常值了。当然，作为一个技术爱好者，别人是完全无法体会这种快乐的。要是其功耗再低点或者能采用其它的供电方式(比如无线供电、电池供电)，感觉完全能颠覆智能市场。  

## **制作启动镜像**

镜像下载：<https://www.raspberrypi.org/downloads/>，我下载的是RASPBIAN分支，因为其是官方提供且基于Debian，和Ubuntu操作一样.
**Mac环境**：  
```shell
df  # 查看当前已经挂载的卷,一般sd卡在最后，Filesystem是/dev/disk2s1，Mounted on /Volumes/No Name，可以在Finder里面将sd卡的名字改为Pi(我那个默认是No Name)
diskutil unmount /dev/disk2s1   #将sd卡卸载
>> Volume Pi on disk2s1 unmounted
diskutil list # 查看是否有sd卡设备
dd bs=4m if=pi.img of=/dev/rdisk2   #将镜像文件pi.img写入sd卡，需要注意这条命令使用的是rdisk2，这是原始字符设备
diskutil unmountDisk /dev/disk2  # 再卸载sd卡，此时可以拔出来插入树莓派的sd卡槽了  
```

## **启动操作系统**

收到货的那天，发现其有一个DC接口，还以为是通过DC接口供电，出门走了一圈都没发现有卖这货的，于是回家，自习已看，发现可以用Android的电源为期供电的，那接口名字忘了。和网上建议的一样，我采用的是5V 2A的供电设备(其实是直接插到小米插线板上的)  

然后，我又发现，我家里没多的网线，那怎么办，我装的不是desktop版本，没有网线就不能SSH进去。不过还好，它支持HDMI，于是我把它功过HDMI连接上了家里40英寸的电视，(HDMI高清显示，真他妈爽)就像这样，还通过USB插了外置键盘。  

![](http://7xnc86.com1.z0.glb.clouddn.com/raspberrypi_1.jpg)  

默认是通电自动启动的，所以插上电就会进入系统了，默认用户名pi，默认密码是raspberry，接着就做一些基本的配置，通过`sudo raspi-config`来运行设置工具：

- 第一项将sd卡的剩余空间全部用来使用

- 然后修改`Internationalisaton Options`里面的时区及默认字符编码`zh_CN GB2312/zh_CN.UTF-8 UTF-8`

- 接着修改源，这个国度没办法的事  

  ```shell
  # sudo nano /etc/apt/sources.list.d/raspi.list，修改如下
  deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ jessie main

  # sudo nano /etc/apt/sources.list，修改为如下：
  deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ jessie main non-free contrib  
  deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ jessie main non-free contrib
  ```


- 最后，安装必要的软件
  ```	shell
  sudo apt-get update && sudo apt-get upgrade 
  sudo apt-get install vim tree ttf-wqy-microhei git
  sudo rpi-update	# 如果想要升级固件，可以这样升级，如果提示命令找不到可以先install rpi-update
  ```

- WIFI设置

  ```shell
  # 当然，我不可能一直用电视作显示器吧，这时候我买的无线设备就有用场了，直接通过USB插到树莓派上，然后设置wifi  
  $ ifconfig # 可以看到wlan0，表示已经识别无线网卡
  $ sudo vim /etc/network/interfaces添加或修改关于wlan0的配置
  auto wlan0
  allow-hotplug wlan0
  iface wlan0 inet dhcp
  wpa-ssid WIFI名称
  wpa-psk WIFI密码

  # 然后通过如下命令重启网卡
  sudo ifdown wlan0 && sudo ifup wlan0
  ```

- 搭建ownCloud私有云

  ```shell
  作为私有云方案，我选择的ownCloud，而不是Samba，因为Samba功能仅仅算是ftp的共享，而不是一个私有云方案，当然ownCloud也有为人诟病的地方，比如内存占用高(树莓派2上占用100多MB)，另一个是因为它本身是基于Apache的，树莓派内存总共就1G，我可不想既有Apache又有Nginx，所以直接用的是Nginx+php5-fpm的方案，不过这样子，配置过程就有点麻烦了。  
  # 首先，安装基本服务
  sudo apt-get install php5-common php5-cli php5-fpm
  sudo apt-get install nginx
  sudo apt-get install mysql-server mysql-client

  # 配置MySQL，ownCloud需要提前创建用户、数据库和分配权限
  > create database 库名 character set utf8 collate utf8_general_ci;  
  > grant ALL on 库名.* 用户名@localhost identified by "密码"   # 注意，ownCloud是不允许root用户的，因为权限太多

  # 配置文件权限
  chmod 775 -R owncloud/        # 不要分配777，分配了也不能用
  chown -R www-data:www-data owncloud/

  # 配置php5-fpm
  $ printenv PATH 获取系统环境变量
  vim /etc/php5/fpm/pool.d/www.conf，将下面几行前面的注释去掉
  ;env[HOSTNAME] = $HOSTNAME  
  ;env[PATH] = /usr/local/bin:/usr/bin:/bin      # 这里还要修改为刚才获取到的环境变量  
  ;env[TMP] = /tmp  
  ;env[TMPDIR] = /tmp  
  ;env[TEMP] = /tmp

  # 配置nginx，按照官网的教程配置Nginx conf：https://doc.owncloud.org/server/7.0/admin_manual/installation/nginx_configuration.html

  对于官网的配置，我做了如下几项修改：
  location ~ .php(?:$|/)$这里面修改为：
  location ~ ^(.+?.php)(/.*)?$ \{  
    fastcgi_split_path_info ^(.+.php)(/.+)$;  
    include fastcgi_params;  
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;  
    fastcgi_param PATH_INFO $fastcgi_path_info;  
    fastcgi_pass unix:/var/run/php5-fpm.sock;  
    fastcgi_index index.php;  
    include fastcgi_params;  
    fastcgi_param PHP_VALUE "post_max_size=10G \\n upload_max_filesize=10G";   # 上传默认居然为513MB，这里可以修改大，不然在owncloud无法调整到更大  
  \}
  检查配置文件是否正确用# nginx -t nginx.conf  
  ```


### TroubleShooting

```

## TroubleShooting
- **中文设置**:

```
    sudo raspi-config
    去掉en_GB.UTF-8 UTF-8
    选择“en_US.UTF-8 UTF-8”、“zh_CN.UTF-8 UTF-8”、“zh_CN.GBK GBK”
    然后第二个页面默认语言选择en_GB.UTF-8 UTF-8
```

参考：  
[http://blog.akarin.xyz/raspberry-init/  
https://github.com/ccforward/cc/issues/25?utm_source=tuicool](http://blog.akar
in.xyz/raspberry-
init/https://github.com/ccforward/cc/issues/25?utm_source=tuicool "Link:
http://blog.akarin.xyz/raspberry-
init/https://github.com/ccforward/cc/issues/25?utm_source=tuicool" )  

```