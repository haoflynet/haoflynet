---
title: "米家智能家居玩儿法"
date: 2019-01-22 22:29:00
categories: 智能家居
---

盼望着盼望着，米家的智能家居终于能用苹果的`Siri`直接控制了，终于不用自己去搭`homebridge`了。我至今没有买小米家的智能音箱，是因为我相信有一天绝对能用`Siri`直接控制的，这一天居然真的来了。小米音箱和`siri`虽然都是通过语音控制，但却是两种不同的媒介，一种必须拿起手机先喊siri，一种必须依赖音箱。我更喜欢前者，因为我能做到哪儿都拿着手机，但不能做到每个房间一个音箱。这个音箱拿来录录抖音倒还可以。

### 夏洛克智能贴锁M1

299的价格实现每天不带钥匙出门，比动不动就上千的指纹锁性价比高多了。其原理就是将钥匙插入锁孔，然后由手机连接蓝牙，蓝牙控制贴锁，贴锁转动钥匙实现开门。因为必须用蓝牙，所以不必担心远程误开。但是有些人质疑其实用性，这样出门虽然不带钥匙了，但是必须带手机呀。我想说的是，很多人买指纹锁、智能锁的主要目的不就是不带钥匙吗，又不是不带手机，谁出门不带手机的，并且即使哪天手机没电或者手机真没带，也能通过别人的手机登录自己的帐号，或者让已经被分配钥匙的人来开门就好了。这是除路由器以外我现在实用最高频率的米家产品了。

### 小米万能遥控器

我通过它实现了控制家中的乐视电视、松下吸顶灯和艾美特风扇。其中电视和灯在遥控器里面都有现成的红外线模板，风扇没有，但是提供了学习功能。遥控器放在客厅，主要控制客厅的红外家电，非常实用。

### 小米路由器

路由器普遍内存和硬盘比较小，能少折腾就少折腾。

<!--more-->

#### 开启SSH功能

路由器本质上都是linux，所以基本上的路由器都是带有SSH功能的。但是根据我的尝试(仅针对小米路由器3)，新版本的系统貌似把SSH登录的功能给关闭了，在不刷第三方系统的情况下，只有刷入老版本系统才能开启该功能。

#### 外网通过Ssh登录路由器

通过`frp`工具，无需安装额外的东西即可实现内网穿透，教程在[这里](https://haofly.net/frp)，小米路由器3只有`/userdisk`目录有写权限

#### 路由器实现局域网唤醒WOL(Wake On Lan)

我使用这个功能主要是为了能通过路由器远程唤醒家里的nas或者树莓派，因为路由器一直运行且能远程登录，自然就可以让nas或者树莓派在空闲的时候自己休息了。但是小米路由器3没有自带`wol`相关工具，我没有找到别人交叉编译的版本，自己也懒得折腾，最后找到了别人编译好的`opkg`工具，[教程在这里](http://bbs.xiaomi.cn/t-13865126-4-o1)，有了包管理工具，就能为所欲为了。	

首先要通过作者提供的网盘地址下载二进制`opkg`到`/userdisk`，接着执行以下命令修改源：

```shell
echo "src/gz attitude_adjustment_base http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/base
src/gz attitude_adjustment_packages http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/packages/
src/gz attitude_adjustment_luci http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/luci/
src/gz attitude_adjustment_management http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/management/
src/gz attitude_adjustment_oldpackages http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/oldpackages/
src/gz attitude_adjustment_routing http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/routing/
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/releases/ramips/packages
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/releases/luci/packages
dest root /data
dest ram /tmp
lists_dir ext /data/var/opkg-lists
option overlay_root /data
arch all 100
arch ramips 200
arch ramips_24kec 300" > /etc/opkg.conf
```

然后就可以正常安装软件了:

```shell
cd /userdisk
./opkg update
wget  http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/base/libc_0.9.33.2-1_ramips_24kec.ipk 
./opkg install libc_*.ipk	# 安装缺失的依赖
./opkg install wol			# 安装wol软件

wol -i [IP][MAC]		# 执行WOL命令
```

### 小米米家智能摄像机

小米的第一代摄像机产品，买得较早，功能很少，如今只是放在门口做威慑用。

### 米家智能插座(ZigBee版)

这个对于我来说用处真的不大，因为我家里大部分的电器原生就能用手机控制。不过有一个很实用的功能就是点亮统计了，空调不能统计因为空调插座规格不一样。比如:

```shell
移动摄像头：白天1.4w，夜间2.25w
小米摄像头：白天1.9w，夜间2.66w
海尔冰箱：速冻模式130w，稳定后78w
热水器：开关都是3w-4w
LG洗衣机：待机时0w-0.3w，洗衣服时30w-370w，波动比较大因为有时候会将水加热滚动的频率也实时变化
小米空气净化器：待机1.55w，最大档26.47w，自动4.2w
艾美特风扇：强风47w，弱风41w，待机0.9w
微波炉：高火1250w
```

### 米家恒温电水壶

热水很快，缺点是白色太不经脏了。智能恒温、定时热水等十分有用的功能在我这儿变成了鸡肋，因为我根本用不到呀，我在家里喝冷的矿泉水就行。

### 空气净化器

纯粹心理作用比较大，用了一年半后滤芯到期了取出来发现里面并不怎么脏。晚上建议关闭，虽然声音很小但真不是静音。

### 小米插线板1代

这个得批评，做工差，每次插入都感觉里面有碎片，另一个用了一年多，USB孔全坏了。