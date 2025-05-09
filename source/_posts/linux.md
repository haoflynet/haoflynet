---
title: "Linux 手册"
date: 2013-09-08 11:02:30
updated: 2023-09-11 17:52:30
categories: system
---
# Linux手册

## 系统安装

CentOS版本说明

- BinDVD: 最完整的版本，可以选择安装所有的软件
- LiveDVD: 光盘安装版
- LiveCD:比LiveDVD体积小而已
- minimal: 精简版，连基本软件都没带，最好不要安装这个
- netinstall: 网络安装版

## 基础安装

```shell
# CentOS
sudo yum install epel-release
sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm	# EC2的Centos7上执行这个才能使用安装EPEL

yum groupinstall "Development Tools"	# 安装gcc等基本开发工具
## vim /etc/sysconfig/network-scripts/ifcfg-eth0把ONBOOT=no改成yes即可让网卡开机自动启动
```

## 命令行Tips

<!--more-->

#### shell

- 一次执行多条命令可以使用`&&`连接，但是如果要使后面的命令即使报错也执行可以使用`||`

```shell
# shell配置文件的区别
~/.bash_profile: 用户登录时被读取执行
~/.bashrc: 启动新的shell时被读取执行
~/.bash_logout: shell退出时被读取执行

# shell登录过程
/etc/profile -> ~/.bash_profile -> ~/.bash_login -> ~/.profile

# 常见环境变量
PATH: 指定shell在这些目录里面寻找命令，添加环境变量: PATH="$PATH:$HOME/bin"
HOME: 当前用户住目录
MAIL: 当前用户存放邮件的目录
SHELL: 当前用户使用的shell种类
LOGNAME: 当前用户的登录名
HOSTMANE: 当前主机名
LANG/LANGUAGE: 语言

# 输入输出，shell参数
2>&1 	# 输出重定向，1代表标准输出，2代表标准错误输出，这个表示将标准错误输出也输入到标准输出中
echo $0	# shell本身的文件名
echo $1	# 得到shell的第一个参数
echo $#	# 得到最后一个参数的序号，相当于打印有多少个参数
echo $@	# 得到shell所有的参数
echo $$	# Shell本身的PID

# 并发执行shell命令，不是串行，是并行。并且所有命令的输出都能看得到
#!/bin/sh
/usr/bin/my-process-1 --args1 &
/usr/bin/my-process-2 --args2 &
/usr/bin/my-process-3 --args3 &
wait
echo all processes complete

# 忽略上一句的错误
mkdir /abc/def || echo 'hello'
```

#### 进程及端口

```shell
# 查看端口占用情况
netstat -ap | grep 端口号   # 查看某一个端口
netstat -ntlp
netstat -tunpl | grep 端口号	# 查看某个端口到底被哪个进程占用
top -p 进程ID：查看进程的实时情况，包括内存大小，内存占用率、CPU占用率，运行时间
gtop: 命令行式的活动监视器
htop: 比top更好看的进程监视，还支持查看进程的每个子进程
cat /proc/进程ID/status：查看进程详细信息，包括线程数，线程名称，线程状态，占用内存大小
ps aux	# 列出目前所有进程的内存用量
pstree -p 进程ID # 查看线程的进程数以及进程ID，需要安装psmisc
lsof	# 能看到所有进程打开的文件
lsof -i :端口号   # 查看端口占用情况，不仅能看到哪个进程开启的端口，还能查看谁在使用该端口
lsof -i -n -P | egrep ':8000.+ESTABLISHED'   # 查看8000端口的连接列表
lsof -i -n -P | egrep -c ':8000.+ESTABLISHED' # 查看8000端口的连接数字
time 命令	# 查看命令的执行时间

# 结束进程
kill -s 9 进程ID
kill -TERM 进程ID		# 杀死进程及其所有的子进程，但有时候不起作用
ps -aef|grep "run.js" | awk '{print $2}' | xargs sudo kill -TERM	# 批量关闭指定的进程
pkill -f cycle_cleaner	# 批量关闭自定关键字的进程

# 监控每个进程的网络带宽，类似的还有iftop，但是都只能监听TCP，iptraf工具能监听UDP流量
sudo apt-get install nethogs -y
sudo nethogs

# 监控内存占用
top: 常用的命令，按1可以查看每个CPU的负载情况
gtop: 功能十分强大的系统监视器

# /var/run/*.pid文件，pidfile文件一般用于daemon程序，主要作用是保证在系统中只存在该daemon的一个进程，同时也便于系统统一管理这些daemon程序。

# timeout设置进程最大运行时间(秒)，超时后自动退出
timeout 3 top	# 仅运行3秒
```

#### 查找、统计、替换

```shell
ls -lR | grep "^-" | wc -l # 递归统计文件夹下所有文件的个数
ls -lt	# ls的时候按时间排序
ls -Slh	# 按文件从大到小排序，大小排序
ls -Slrh # 按文件从小到大排序
ls -1 # 按文件名排序
ls -1r	# 按文件名倒序排序
wc -l: 统计行数
fdupes -r /home		# 快速查找重复文件
fdupes -f /home | xargs rm -f	# fdupes居然没有直接删除的功能，-d参数必须询问，这样子就能直接进行删除了，-f参数表示忽略第一个文件，这样出来的就都是重复的了
find / -name filename	# 精确查找某个文件
find / -name '*.txt'	# 模糊查找某个文件
find / -mmin -60    # 查找60分钟内修改的文章
find / -type d -mtime -1 # 查找1天内修改过的文件夹(好吧，我用了rm -rf / 命令才知道的)
find ./ -ctime -10 # 查找最近10天修改过的文件，atime表示最后一次访问时间，ctime表示最后一次状态修改时间，mtime表示最后一次内容修改时间
cat /proc/cpuinfo | grep "model name" | wc -l	# 获取服务器核心数
cat -E filename	# 显示每行末尾的结束字符$，可以用来排查有些配置文件被多输入了字符
cat filename|tr -s '\n'	# cat命令不输出空行
free -h | sed -n '2p' | awk '{print $2}'		# 获取服务器内存大小
df -h | sed -n '2p' | awk '{print $2}'			# 获取服务器磁盘大小
sort filename | uniq -c	# 去除文件中重复的行

cat file.json | jq -r '.user.name'	# 命令行直接解析json可以使用sudo apt-get install jq -y
```

##### awk

以行为单位将输入进行处理，貌似这里的处理只能进行print

```shell
-F 参数将行做分割，例如：ps | awk -F ':' {'print $1'}  # 按:分割字符串，将ps的第二列输出
cat file | awk {system($0)}	# 执行文件中的每一行命令
```

##### grep

```shell
grep -c "词语"   # 统计出现的次数
grep -i ""	# 忽略大小写
grep -n ""		# 把匹配到的行号也打印出来
grep -v "Java"	# 查找没有该词的行
grep -v ^$		# 排除空白行
grep -5 ""		# 打印匹配的前后5行
grep -A5 # 打印匹配的后5行
grep -B5 # 打印匹配的前5行
grep -E "a|b"	# grep支持正则，多个关键字
grep 字符串 文件名  # 在文件中查找某个字符串
grep ^字符串 文件名 # 在文件中查找以某字符串开始的行
grep [0-9] 文件名  # 在文件中查找包含数字的行
grep 字符串 -r 目录 # 在特定目录及其子目录中的文件查找str，-d参数能进行删除操作，保留一个副本
grep xxx -b10		# 查找指定字符串并且把它前面的10行一起显示出来
grep xxx --color=auto	# 高亮显示查找到的字符串
grep --exclude-dir=node_modules	# grep的时候忽略指定目录/忽略目录
```

##### sed

##### 同样以行为单位将输入进行处理

```shell
# 参数 
-n 输出第几行，例如：ps | sed -n '1p'  # 将ps的第一行输出

# 功能
a 新增
c 取代
d 删除
s 替代

# 常用命令
sed '/^$/d' file > outputfile	# 去除文件中的空白行
sed '5s/^.*$/xxxxx/'  file		#　替换一整行
sed '5s/^.*$/xxxxx/' filename	# 替换某个文件的第五行，并输出结果，不写入
sed -i 's/^abc$/xxxxx/g' filename 	# 替换某个文件的abc字符串，并写入指定文件
sed -i "s/localhost:8000/127.0.0.1:8000/g" `grep localhost:8000 -rl ./`	# 批量替换一个文件夹下所有文件的内容
perl -i -pe 's/abc/def/g' Options\ AI.xcodeproj	# 如果文件名中有空格，我用sed一直不成功，只能用perl命令来代替
```
##### xargs

给其他命令传递参数的过滤器，能够用于组合多个输入，将标准输入转换成命令行参数。

```shell
cat url-list.txt | xargs wget -c	# 下载一个文件中所有的链接
cat folder-list.txt | xargs ls		# 列出一个文件夹文件中的所有文件
```

##### watch

周期性地执行指定的命令

```shell
watch -n 3 'cat /proc/loadavg'	# 每3秒执行一次
```

##### while

循环语句，可以直接在shell中单行写，例如

```shell
ls | while read line; do xargs zip $line.zip $line;done
```

#### 文件操作

```shell
# 压缩，7zip需要安装工具yum install p7zip
tar -czvf --exclude=.git --exclude=*.jar 结果.tar.gz 目标/    # 打包并使用gzip压缩，exclude命令用于排除某些目录或文件
tar -cjvf 结果.tar.bz2 目标/   # 打包并使用bzip2压缩
zip *.zip file          # 压缩file为zip格式
zip -r *.zip file dir   # 压缩文件或目录一起为zip格式
zip -e 结果.zip 目标     # 压缩并加密(OSX可用)
zip -P 密码 结果.zip 目标	# 压缩并加密，直接把密码写在命令行
7z x 目标.7z			# 解压.7z文件
unrar -e *.rar	# 解压.rar文件

# 压缩格式对比
# 压缩比率: tar.bz2=tar.bz>tgz>tar
# 占用空间: tar.bz2=tar.bz<tgz<tar
# 压缩时间: tar.bz>tar.bz2>tgz>tar
# 解压时间: tar.bz2>tar.bz>tar>tgz

# 解压
xz -d *.tar.xz
tar xvf *.tar
tar zxvf *.tgz
tar -xjf tar.bz2   # 解压bz2文件
gunzip *.gz     # 解压gz文件
tar -xzf *.tar.gz

# 复制
cp 文件1 文件2
cp -r 目录1 目录2  # 递归复制
cp -a 目录1 目录2  # 递归复制目录，同时将文件属性也复制过去，包括文件权限所有者全都复制

# 文件分割
split -b 1024m targetfile prefix  # 文件分隔-b表示按大小分隔，-l表示按行数分隔,prefix是分割后每个文件的前缀
cat prefix* > newtarget	# 将分割后的文件又合并在一起

# 查看文件内容
cat filename | more  # 表示分页查看文件内容

# 输出内容到文件
cat ./test.conf >> /etc/supervisord.conf
sudo bash -c 'cat ./test.conf >> /etc/supervisord.conf'  # 上一句如果出现权限问题可以尝试使用这条命令
file 文件名	# 查看文件基本类型
stat 文件名	# 查看文件的属性，例如最近访问时间、最近更改时间、最近改动时间等

# 建立链接，最好都用绝对路径
## 软连接，就是快捷方式
软连接：ln -s 源 目的地
软连接可以给目录创建
对源文件修改能影响目的文件，目的文件的修改也会影响源文件
如果删除了目的地文件对源文件不会有影响，但是如果删除源文件，两边都会删除
如果是目录，那么删除了目的地的一个子文件，这边也会删除的
## 硬连接
硬连接：ln -d 源 目的地
硬连接不能给目录创建，对连接做的更改会影响源文件，只能在同一文件系统中创建
为了弥补软硬连接的不足，可以使用mount --bind命令进行挂载
unlink /xxx # 删除连接

# 文件创建
mkdir -m 777 path	# 创建时赋予权限
mkdir -p path/2 # 创建目录树，并且如果存在，不会报错
mkdir -pv path/{path1,path2} # 建立子目录
mkdir -v a+wt path	# 创建一个粘滞模式的文件，其他用户可以修改，但是只有该文件的owner才能进行删除操作，这条命令即使把0755(rwxr-xr-x)改为1777(rwxrwxrwt)

# 找不同
diff 文件1 文件2   # 找出两个文件的不同
diff -x '*log' ...	# -x 参数排除指定文件
sdiff 文件1 文件2  # 以对比的方式找文件的不同

# 批量转换文件编码
find *.txt -exec sh -c "iconv -f GBK -t UTF8 {} > change.{}" \;	# 这里将GBK转换为UTF8

# 删除文件，强烈建议安装trash-cli命令，因为rm的文件不会在回收站，到时候找都找不回来

ls *.txt	# 直接使用通配符
ls -l # 列出文件详细信息
ls -ld # 列出文件夹详细信息

\cp -rf file1 file2	# cp命令不弹出确认Y/N的解决方法是在前面加上斜杠

# 更改文件或文件夹权限
chmod g+x filename	# 给group增加可执行权限
chmod g+xw filename
chmod o+w filename	# 给其他用户增加可写权限
chmod g-x filename	# 给group移除可执行权限
```

#### ssh

```shell
# 配置免密码登录
ssh-keygen -t dsa # 生成自己的ssh，然后将~/.ssh/id_dsa.pub的内容添加到主机的~/.ssh/authorized_keys里面面去

ssh -i key.pem root@127.0.0.1	# 通过pem认证登录服务器
ssh -vvv # ssh的debug模式
ssh-keygen -lf ~/.ssh/id_rsa.pub	# mac下计算ssh key的sha256指纹
ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub	# linux上计算ssh key的指纹
ssh-keygen -p -f ~/.ssh/id_rsa.pub		# 修改key密码

# SSH使用代理
ssh -o ProxyCommand='nc -X 5 -x 127.0.0.1:1080 %h %p' host

# ssh-add命令，将专用密钥添加到ssh-agent的高速缓存中。转发ssh key，常用于跳板机
## ssh代理git可以参考https://docs.github.com/zh/developers/overview/using-ssh-agent-forwarding，但是排查问题还得加一个可能，如果服务器磁盘满了，也是代理不成功的
ssh-add -L	# 列出ssh-agent的公钥
ssh-add -l	# 列出ssh-agent的密钥
ssh-add -k -i ~/.ssh/my.pub	# 将指定ssh key添加到当前用户的key列表中去，之后的ssh命令都会自动带上该key
ssh-add -A	# 将当前所有的key都带上

# ssh直接执行命令
ssh IP "ls"
ssh IP "echo \`uname -a | awk '{print \$3}'\`"	# 特殊符号

# ssh config设置，可以修改~/.ssh/config来设置简单的ssh配置，例如，如果设置了下面这几行，那么就可以直接ssh ali来进行指定服务器的登录了
Host ali
  HostName 233.233.233.233
  User root
  Port 22

# SSH自动把host加入到known_hosts
ssh -o StrictHostKeyChecking=no root@ip

# 命令行直接输入密码，使用sshpass，当然，这样子在history就会记录下你的密码了，可以使用history的相关功能屏暂时屏蔽掉记录密码的功能
sshpass -ppassword ssh

# expect: 交互式SHELL自动输入，需要先安装apt install expect -y, 然后可以这样写一个可执行文件
#!/usr/bin/expect -f	# 可以加入-d参数进行调试
set timeout 10 # 注意超时也是会自动向下继续执行的
spawn target.sh		# 需要执行的脚本
expect "Select group"	# 期望出现的字符
expect "aaa" {send "1\n"}	# 一组语句
send "1\n"	# 当出现上面字符的时候输入指定字符
interact	# 保持交互状态，这样不会退出交互
expect "Success"	# 注意最好在后面判断一下成功信息的出现，这样才能保证程序执行完成了后退出，不然会以为回车没有用哟，此时不要用interact。但是我仍然遇到过send后一直不执行下面语句的情况，不知道怎么解决了

# CentOS下的安装
yum install openssh-client openssh-server

# 传输文件
scp 用户名@地址:远程路径 本地路径  # 获取/下载远程服务器的文件，目录加-r参数
scp 本地路径 用户名@地址:远程路径  # 将本地文件上传到远程目录，目录加-r
## 使用finder直接选择文件进行上传和下载
apt-get install lrzsz -y	# 安装rz和sz命令工具

# 仅允许SSH登录，vim /etc/ssh/sshd_conf
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication no

# 允许普通用户使用SSH登录，默认开启UsePam的，普通用户只能用账户密码登录不能用KEY登录
# vim /etc/security/access.conf，找到-:ALL EXCEPT root :ALL在root后面添加你需要的用户，比如-:ALL EXCEPT root haofly:ALL,然后，重启SSHD

#保存，然后重启ssh服务
service sshd restart

# 进制特定IP登录，vim /etc/hosts.deny
sshd:IP

# 登录shell和非登录shell的区别: 加载的文件不同，登录式shell加载/etc/profile、/.bash_profile和~/.profile，而非登录式shell加载/etc/bashrc或者/etc/bash.bashrc、~/.bash_rc，所以在切换用户是最好加上-，即su - haofly就切换到那个心的地方了
```

##### ssl证书

```shell
openssl x509 -in cert.pem -noout -text	# 打印出证书的内容
```

#### 包管理

```shell
# RPM管理工具
rpm -qa					# 列出当前系统所有安装的包
rpm -ql 包名			   # 查询已经安装的包的文件路径或者查询是否安装某个包
rpm -ivh *.rpm			# 安装指定rpm包
rpm -ivh --test *.rpm	# 检查指定rpm包的依赖关系是否完全满足，并不真正安装
rpm -vhU https://nmap.org/dist/nmap-7.80-1.x86_64.rpm	# 下载并安装包
rpm -qpf *.rpm			# 查询指定rpm包都有哪些依赖
rpm -qpi *.rpm			# 查询指定rpm包的元信息
rpm -qpl *.rpm			# 查询指定rpm包的下都有哪些文件
rpm -qpl -c *.rpm		# 查询指定rpm包的下都有哪些配置文件
rpm -e 包名			   # 卸载软件包
rpm -qf 文件名		      # 查询指定文件属于哪个包
yum --showduplicates list 软件名	# 查询源里面指定软件都有哪些版本并标明当前所使用的版本
yum -y downgrade mysql-0.2.2-1536136655.el7	# 将软件降级到指定版本
yum update 报名	# 更新软件包

# dpkg管理工具
dpkg -i *.deb # 安装deb包，但是它不会自动解决依赖，安装完成后还要使用apt-get -f install这条命令来安装没有安装好的依赖
dpkg -l			# 查看已经安装的包及其版本

# Debian
apt-cache search 包名		# 搜索源里面是否有指定的包
apt-cache show 包名 	   # 显示apt库里面的软件的版本号
apt-get clean 			# 自动清理安装程序时缓存的deb包
apt-get autoclean  		# 清理已卸载软件的无用的依赖包
apt list --installed	# 查看已经安装的包列表
apt-get install 包名	# 安装或者更新指定的软件包
apt-get install vim=2:7.3.547-1 # 安装指定版本的包
apt-get upgrade	# 更新所有已安装的软件包
```

#### 磁盘管理

```shell
sudo fdisk -lu   # 显示硬盘及分区情况
sudo fdisk /dev/sdb # 对某一硬盘进行分区(千万不要在当前硬盘进行分区)
sudo mkfs -t ext4 /dev/sdb   # 将硬盘格式化为ext4文件系统
sudo df -lh   # 显示硬盘挂载情况
sudo mount -t ext4 /dev/sdb /mydata  # 挂载某个分区文件为ext4
sudo mount -t tmpfs -o size=12m tmpfs storage/framework/cache	# tmpfs允许将文件作为一个目录存储在RAM中，这样既能用文件保存，又能因为是内存中得到性能的提升
sudo umount /dev/sdb	# 卸载磁盘
sudo mount -o remount,rw /mydata	# 重新按照指定的读写权限挂载磁盘

# vim /etc/fstab中添加，特别注意，修改完该文件后需要执行mount -a测试一下语法是否有错误，以免无法启动
UUID=硬盘的UUID  /挂载位置   ext4 defaults 0  0   # 在系统启动时自动挂载硬盘blkid /dev/sda1  查看硬盘UUID用sudo blkid

sudo du -h -d 1 /path	# 获取指定目录下一级的各个目录的大小

# Linux读写windows的NTFS磁盘分区，使用微软开源的NTFS-3G
yum install ntfs-3g
mkdir /mnt/test				# 创建一个挂在目录
ntfs-3g /dev/sda5 /mnt/test	# 将windows的分区挂载到/mnt/test目录下面去

# ncdu: 统计并查看磁盘空间使用量，可以按时间以及大小排序
yum install ncdu
du -h --max-depth=1	# 当ncdu统计出来的容量明显不对的时候只能用这个了

# 查看磁盘读写情况，iostat
sudo apt-get install sysstat -y
iostat

# 磁盘空间不足
sudo apt-get clean && sudo apt-get autoremove	# 可以删除一些不必要的linux-headers-* 和 linux-headers-*-generic文件

sudo journalctl --vacuum-size=500M # 可以将journal的日子限制到指定大小，会自动删除多余的日志

```

#### 用户管理

```shell
w # 查看当前登录的所有的用户
who # 查看当前登录的用户及启动的进程

sudo -i # 切换为root用户
sudo -u postgres psql xxx # 以指定用户身份执行命令

# 添加用户
sudo useradd -s /bin/bash -d /home/username -m username
sudo userdel -r username	# -r参数表示同时删除主目录和邮件池

# 修改用户密码
sudo passwd username

# 批量修改用户密码
chpasswd < user.txt	# 其中user.txt是用户名和密码的对应文件，格式为username:password

# 给用户添加sudo权限，以下这种方法不可采取，因为改错了以后就不能使用sudo命令了，只能通过单用户模式去修改正确，最好的方式是使用`pkexec visudo`命令进行修改。
vim /etc/sudoers 修改如下内容(同时，可以像nginx那样将配置分开/etc/sudoers.d/针对某个用户)
# User privilege specification  
root    ALL=(ALL:ALL) ALL      # 在这一行下面写  
username1 ALL=(ALL:ALL) ALL    # 该用户可以执行所有sudo操作
username2 ALL=NOPASSWD:/usr/bin/git # 该用户可以执行'sudo git'的操作

cat /etc/passwd  	# 查看所有用户
cat /etc/group		# 查看所有用户组
cat /etc/shadow	# 通过看是否有加密穿来判断是否给用户设置了密码

# 将用户添加到组，注意可能需要重新登录才能生效
sudo usermod -a -G groupName userName
sudo usermod -a -G www-data ubuntu	# 将ubuntu添加到www-data组


# ACL权限分配: 可以给指定的用户指定目录分配指定的权限

su - www -c "php artisan"	# 以指定用户执行命令

# 清空登录日志
echo > /var/log/wtmp	# 成功登录的用户
echo > /var/log/btmp	# 尝试登录的用户信息
echo > /var/log/lastlog	# 最近登录的用户信息
```

#### 系统相关

```shell
lsb_release -a      # 查看系统信息
echo $HOSTTYPE     	# 查看系统位数
cat /proc/cpuinfo    # 查看CPU信息
cat /etc/issue     # Debian系列查看系统版本
cat /etc/redhat-release # redhat系列查看系统版本
cat /proc/version	# 更详细的系统版本
rpm -q centos-release|cut -d- -f3	# 查看centos是6还是7
lspci				# 显示当前主机的所有PCI总线信息、vga/navidia表示的是显卡GPU信息
lspci -v -s 00:0f.2	# 显示指定硬件信息的详情，例如查看GPU大小等
who -b	# 查看最后一次系统启动时间
who -r # 查看当前系统运行时间
lastlog # 查询所有用户最近一次的登陆时间
last # 列出当前和最近登陆的用户的信息

# 环境变量
env	# 查看环境变量
export A=b	# 设置环境变量

# 更新系统
sudo apt-get install update-manager-core
sudo do-release-upgrade

# 系统开关
shutdown -h now # 关机
shutdown -r now # 重启

# 查看某个命令的系统调用
strace + 命令: 这条命令十分强大，可以定位你程序到底是哪个地方出了问题

# 增加虚拟内存
sudo dd if=/dev/zero of=/swapfile bs=1024 count=500000  # 500MB，这两行是连在一起的，我日
sudo mkswap /swapfile && sudo chown root:root /swapfile && sudo chmod 0600 /swapfile && sudo swapon /swapfile
sudo echo "/swapfile          swap            swap    defaults        0 0" >> /etc/fatab	# 开机时挂载

/sbin/swapoff /swapfile	# 停止交换分区
rm -rf /swapfile		# 删除交换分区

sudo service lightdm start	# Linux Mint关闭GUI，重启gui
```

#### systemctl/service

- service定义在`/etc/systemd/system/`或者`/usr/lib/systemd/system/`下的

```shell
systemctl list-unit-files --type=service	# 查看系统所有安装的服务项，enabled的表示设置为了开机自启动
systemctl list-units --type=service	# 查看系统所有运行的服务项(如果某个服务显示为红色表示有问题)
systemctl list-units --type=service --state=failed	# 仅查看当前运行的出错的服务
systemctl list-dependencies nginx	# 查看服务项的依赖关系
systemctl daemon-reload	# 修改添加或删除服务项目后执行这个命令
systemctl get-default	# 查看系统的默认启动级别
systemctl isolate graphical.target	# 切换系统的默认启动级别到图形界面

systemd-analyze	# 查看系统启动耗时
systemd-analyze blame | grep .service	# 查看各项服务的启动耗时

systemctl status nginx # 查看服务状态，是否启动、是否激活及日志
systemctl start docker	# 开启服务
systemctl restart teamviewerd	# 重启
systemctl stop teamviewerd	# 停止服务
systemctl reload nginx	# 重新读取配置文件

systemctl is-enabled mongodb # 验证是否开启了开机启动
systemctl enable docker.service	# 开机启动服务
systemctl enable --now docker.service 	# 设置为启动服务并且现在就启动一下
systemctl disable docker.service	# 禁用开机启动

service httpd status	# 检查服务状态
systemctl list-units --type=service	# 显示所有已启动的服务

journalctl --follow -u myown.service 	# 查看某个系统服务的日志
```

如果要将自己的程序变成系统的一项服务，那么可以在`/etc/systemd/system/`下新建一个以`.service`后缀 的文件，内容格式如下，新建完成执行`systemctl daemon-reload`:

```shell
[Unit]
Description=这里是服务的描述
Documentation=http://nginx.org/en/docs/	# 这里服务的文档地址
After=newtork-online.target			# 表示在哪些服务(模块)之后启动，多个的以空格分隔

[Service]
Type=<simple|forking|oneshot>	# simple命令前台持续运行，forking命令后台持续运行，oneshot命令只执行一次
PIDFile=/var/run/nginx.pid	# pid文件所在位置
ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf	# 表示启动参数
ExecReload=/bin/kill -s HUP $MAINPID	# 重新读取配置文件的命令
ExecStop=/bin/kill -s TERM $MAINPID	# 服务退出命令

[Install]
WantedBy=multi-user.target
```

#### 网络/防火墙

```shell
# 安装ping命令
apt-get install iputils-ping

# 查看进程的网速
nethogs

# 使用curl查看出口IP及服务商
curl ipinfo.io

# 关闭几种防火墙
sudo apt remove iptables-persistent -y && sudo ufw disable && sudo iptables -F

# ufw防火墙
sudo ufw status	# 查看当前的规则列表
sudo ufw allow from 192.168.1.100 to any port 3005	# 添加新规则

# CentOS6
/etc/init.d/iptables status     # 查询防火墙状态
/etc/init.d/iptables save		# 下面这些语句都是暂时的，并不会写入配置文件，使用save则会写入

## -A: 添加一条规则
## -p: 指定协议
## -dport: 目标端口
## -sport: 源端口
## -j: ACCEPT接收，DROP拒绝。DROP动作会简单的直接丢弃数据，并不反馈任何回应，客户端会超时。REJECT则会礼貌地返回一个拒绝数据包，客户端会马上断开
## -s: 指定IP
iptables -D INPUT 5	# 参考上面的status，指定删除某个规则下面某个序号的规则
iptables -A OUTPUT -p tcp --dport 6379 -j DROP	# 禁止访问外部的6379端口
iptables -A INPUT -p tcp --dport 6379 -j DROP	# 进制外部访问内部的6379端口

# CentOS7 用firewall代替了iptables
firewalld		# 启动服务，启动的时候需要注意，默认不会开启任何端口
systemctl disable firewalld && systemctl stop firewalld	# 关闭服务
firewall-cmd --state	# 查看firewall运行状态
firewall-cmd --add-port=3306/tcp --permanent	# 添加端口，需要注意的是，很多时候需要重启firewall才能生效
firewall-cmd --remove-port=3306/tcp --permanent	# 将某个端口从zone删除
firewall-cmd --reload			# 重启服务
firewall-cmd --list-ports		# 列出开放的端口
firewall-cmd --list-all-zones	# 查看都有哪些区域，默认有下面这些区域。如果客户端的源地址匹配了zone的sources，那么就直接使用该zone的规则。
## block，阻塞区域，会拒绝进入的网络连接，返回icmp-host-prohibited
## dmz，隔离区域，
## drop，丢弃区域，任何进入的数据包将被丢弃
## external，外部区域，只有指定的连接会被接受
## home，家庭区域，只接受被选中的连接，默认未ssh,samba-client和dhcpv6-client
## internal，内部区域
## public，公共区域，只接受那些被选中的连接，默认只允许ssh和dhcpv6-client，默认的区域
## trusted，信任区域，允许所有网络通信通过
## work，工作区域，只能定义内部网络

# 扫描无线网络
ifconfig wlan0 up
iwlist wlan0 scanning
```

##### 命令行获取自己的公网IP地址

```shell
# IPv4地址
curl ipinfo.io/ip
curl api.ipify.org
curl ipecho.net/plain

# 获取IPv6地址
curl -6 icanhazip.com
curl bot.whatismyipaddress.com
```

##### Dns设置及常用DNS

```shell
nslookup -q=A haofly.net	# 查询域名的DNS记录

# 设置DNS, vim /etc/resolv.conf
nameserver 114.114.114.114	# 114.114.115.115
nameserver 223.5.5.5	# 阿里的DNS，223.6.6.6
nameserver 1.2.4.8	# SDNS,210.2.4.8
nameserver 202.38.64.1	# 中科大dns，202.38.64.1
```

#### 软件源管理

Debian的软件源分为`stable/testing/unstable/experimental`。默认大家平时使用的都是stable，unstable的开发代号是sid。如果我们需要更新的软件，那么将sid源加入到软件源中:

```tex
deb http://ftp.debian.org/debian sid main
```

然后就可以这样子安装软件`sudo apt-get -t sid install ...`

##### 推荐的软件源

```shell
# CentOS 软件源位置/etc/yum.repos.d
```

##### 创建自己的yum源

通过简单的`createrepo --update /data/mypath/`命令即可在指定路径创建自己的源仓库。然后再启动一个http服务将该目录暴露出来即可，最简单的可以直接`python3 -m http.server`即可。最后在需要安装该仓库软件的机器上新建一个源文件即可:

```shell
# vim /etc/yum.repos.d/myrepo.conf，输入以下内容
[my_test_repo]	# 指定仓库的名称
name=my test repo
baseurl=http://127.0.0.2:8000
enabled=1	# 是否启用这个更新库
gpgcheck=0	# 是否使用gpg文件来检查软件包的签名
gpgkey=...	# 表示gpg文件存放位置，如果gpgcheck为0可以不用写
```

## 其它工具

#### chokconfig系统服务

更新和查看系统服务的运行级信息(可以设置开机启动服务)，各个服务的配置文件在`/etc/init.d/`。

level总共有6级，分别表示关机、单用户模式、无网络连接的多用户命令行模式、有网络连接的多用户命令行模式、不可用、带图形界面的多用户模式、重新启动。

```shell
chkconfig --list	# 查看全部服务状态
chkconfig --add 服务名	# 将某项服务设置为自动启动，该名字必须是/etc/init.d/文件夹下面的文件名
chkconfig --del 服务名	# 禁止某项服务自动启动
```

需要注意的是，`/etc/init.d/服务名`文件的编写方式必须这样写:

```shell
#!/bin/sh
#
# my-agent
#
# chkconfig: 3 99 01		# 这一行必须有，第一个数字表示运行级别，第二个表示启动时的执行顺序，第三个表示系统退出时候的执行顺序，例如3，345等
# description: Starts and stops the my-agent daemon.	# 这一行必须有
#
/usr/share/my-agent/bin/my-agent $@	# 下面即是需要执行的命令
```

#### Crontab/at定时任务

要使用`cron`服务，首先要安装启动`cron`: `sudo apt-get install cron -y && crond`。at命令可用于只执行一次的任务

```shell
crontab -e # 直接打开定时任务文件进行编辑
格式如下：
第1列：分钟
第2列：小时
第3列：日
第4列：月
第5列：星期
第6列：命令
其中，每一列可以逗号和小横线表示特殊的意义，比如
3,15 8-11 * * * 命令   # 表示在上午8点到11点的第3和15分钟执行
* 23 * * * 命令			# 注意这个表示的是23点的每分钟都执行
0 */1 * * * 命令			# 每隔一小时
*/2 * * * * 命令 			# 每隔两分钟
需要注意的是coontab是不会自动加载环境变量的哟，所以有时候发现命令没有被执行，可能是这个原因

# crontab日志，默认是关闭的，如果要打开可以在配置文件里面进行打开,vim /etc/rsyslog.d/50-defaullt.conf，当然要看日志首先也得有日志服务apt-get install rsyslog
cron.*	/var/log/cron.log	# 将cron前面的注释去掉
service rsyslog restart		# 重启rsyslog

# crontab跑GUI任务
30 23 * * * DISPLAY=:0 /usr/bin/pygui-macro run	# 每晚十一点半跑一个定时任务

# 不用管理员用户而是直接当前用户用sudo执行(管理员用户可以直接sudo crontab -l查看任务)
20 * * * * echo "password" | sudo -S rm /etc/xxx	# 缺点是只能将密码写在这里了

# 查看所有用户的定时任务信息
/var/spool/cron/

# 查看最近的定时任务执行列表
systemctl list-timers

20 23 * * * command >> /tmp/crontab 2>&1	# 将输出重定向

select-editor # 重新选择crontab等应用的默认编辑器为vim
```

#### CURL

```shell
curl -o a.txt url	# 将文件下载到本地并命名为a.txt
curl -O url			# 将文件下载到本地用它本来的命名
```

#### FTP/SFTP/VSFTPD

ftp: 很普通的文件传输协议

sftp: 基于ssh协议的加密ftp传输协议

vsftpd: ftp服务器，支持ftp协议，不支持sftp协议

```shell
# sftp配置方法
## 日志配置，配置了日志就有登录相关的日志了，甚至有操作相关的日志
## 参考https://access.redhat.com/articles/1374633，可能程序名会不一样
## sftp的登录日志不会出现在last等系统登录日志中
echo "Subsystem   sftp    /usr/libexec/openssh/sftp-server -l VERBOSE -f LOCAL3" >> /etc/ssh/sshd_config
echo "local3.*  /var/log/sftp.log" >> /etc/syslog.conf

# vsftp安装方法
yum install vsftpd	# centos
apt install vsftpd	# ubuntu
# sudo vim /etc/vsftpd/vsftpd.conf，ubuntu在/etc/vsftpd.conf 修改如下几项：
anonymous_enable=NO
local_enable=YES
chroot_local_user=YES
write_enable=YES	# 可以写数据，如果没有加这个权限去写入的话会报FTP 550错误
local_root=/	# 这个选项可以修改默认的登录目录，设置默认目录为/，该选项默认没在配置文件里
allow_writeable_chroot=YES	# 是否允许在local_root目录进行写操作

service vsftpd restart
chkconfig vsftpd on 	# 开机启动

# sftp修改默认登录目录，vim /etc/ssh/sshd_config，注意ChrootDirectory必须是root:root owner，权限必须是755

# 创建用户
adduser ftpuser	# ubuntu需要用命令useradd -m testuser
passwd ftpuser
usermod -d /path/to/location ftpuser	# 将该用户的登录目录设置为指定的目录，如果设置了local_root当然就不行了
usermod -s /usr/sbin/nologin ftpuser && echo "/usr/sbin/nologin" >> /etc/shells	# 禁止该用户登录shell但允许登录ftp，有人说有安全问题，但么有其他方法，也没人说具体啥安全问题，就这样吧

# 常用命令
ftp domain ip	# 连接目标ftp服务器
sftp user@ip # 连接目标sftp服务器
sftp -i /path/to/your/private-key.pem username@hostname_or_ip # 使用pem文件登录目标sftp服务器
put a.txt		# 上传当前目录的一个文件
mput ./*		# 同时上传多个文件
dir	# 列出当前目录下的文件
mkdir test	# 创建目录
rmdir test	# 删除目录
# 如果要在ftp server删除非空的目录，可以这样做，安装lftp
#lftp user,password server登录服务器，然后直接执行rm -rf directory即可
```

#### logrotate日志轮转

可以设置自动轮转日志，日志超过指定大小，自动压缩，有些系统默认开启，有些则没有，可以通过包管理直接安装。其主配置文件在`/etc/logrotate.conf`，针对不同应用的日志存放在不同的单独的配置文件中`/etc/logrotate.d/`目录下，例如，下面就是一个标准的`nginx`应用的日志轮转配置

- 另外可以通过`logrotate /etc/logrotate.conf `手动运行轮转

```shell
/var/log/nginx/*log {	# 针对指定目录下所有的*log文件
    su root root			# 如果轮转用户没权限，则可以指定用户
    create 0644 nginx nginx	# 以指定的权限创建全新的日志文件
    daily					# 轮转频率，可以有monthly/daily/weekly/yearly
    rotate 10				# 最多保留多少个备份
    missingok				# 忽略轮转过程中出现的错误
    notifempty				# 如果日志为空则不进行轮转
    compress				# 对备份进行gzip压缩
    sharedscripts
    postrotate				# 指定备份完成后执行什么命令，一般就是重启应用，这样应用才会将日志打印到新的文件中去
        /bin/kill -USR1 `cat /run/nginx.pid 2>/dev/null` 2>/dev/null || true
    endscript
}
```

#### nmap

端口扫描工具，为了使`banner`信息更加准确，建议将`nmap`的版本升级到最新

```shell
nmap -Pn 8.8.8.8			# 扫描一个禁ping的机器
nmap -Pn 8.8.8.8 -p 2333	# 指定扫描某个端口
```

#### Rsync文件/文件夹同步工具

```shell
# -a 表示递归同步，且同元信息(修改时间、权限等)
# -n/--dry-run，不会实际同步，只是模拟执行看看哪些文件会被同步
# --exclude="*.txt" 忽略文件，如果多个需要写多个--exclude
rsync -avpP root@server:/path ./ # 从服务器下载文件 

rsync -avpP --rsync-path="sudo rsync"	...	# 如果服务器上需要sudo权限可以这样执行
rsync -avpP --exclude "*.png" --exclude filename # 排除某些文件
```

#### Tmux

相比于Mac下的iTerm2，其优势主要在于能够保存和恢复session。

```shell
# tmux的快捷键都是在先按下control+b键以后再按的

## 窗口操作
c 新建窗口
d 退出当前窗口
p 切换至上一个窗口
n 切换至下一个窗口
s 列出当前所有的会话，并且可以通过上下键直接选择，这个就十分方便了
w 窗口列表选择，mac下使用ctrl+p和ctrl+n进行上下选择
& 关闭当前窗口
0 切换至0号窗口
f 根据窗口min搜索选择窗口

## 窗格操作
% 左右平分两个窗格
" 上下平分两个窗格
x 关闭当前窗格
o 切换窗格
[ 可以用PgUp和PgDn等滚屏，按q可以退出滚屏

## 会话操作
tmux a 恢复至上一次的会话
tmux nes -s test 新建名称为test的会话
tmux ls  列出所有的tmux会话
tmux a -t test 恢复名称为test的会话
tmux rename -t 1 test	# 修改窗口1的会话名称
tmux kill-session -t test 删除名为test的会话
tmux kill-server 删除所有会话
```

#### samba

```shell
# 安装与配置
sudo apt-get update && sudo apt-get install samba samba-commonj
vim /etc/samba/smb.conf	# 修改配置文件，添加如下内容，其中smbashare是远程用户需要输入的路径，path是实际的目录路径
[sambashare]
    comment = Samba on Ubuntu
    path = /home/username/sambashare
    read only = no
    writable = yes
    public = no
    browsable = yes
sudo service smbd restart	# 重启smdb
sudo smbpasswd -a username	# 添加一个用户，之后就可以用这个用户登录了

smbclient //host/path	# 进入共享文件夹中
> get filename	# 下载文件，无法递归下载
> ls		# 列出文件

smbget -R smb://host/path	# 如果要递归下载文件夹，可以这样子使用
```

#### [supervisor](https://haofly.net/supervisor)

**其他命令**

```shell
cd -	# 返回上一次的目录，真他妈实用
history	# 查看历史命令，如果需要查看命令执行时间，需要先export HISTTIMEFORMAT='\%F \%T '。如果要直接执行某个序号的命令，直接!n就好了
history -c	# 清除所有的命令历史
history -d 123	# 删除某一条命令的执行记录
!233	# 根据history的序号执行指定的命令

tzselect	# 更改时区
timedatectl | grep "Time zone"	# 获取时区地区
dpkg-reconfigure tzdata	# 上面那个不行的时候可以用这个
ntpdate	# 如果连时间戳都不对，那么用这个工具来同步时间

# 命令命名，例如如果想通过python命令调用python3而不是默认的python2，那么可以这样子：
alias python=python3
alias pip=pip3
alias run8000='python manage.py runserver 0.0.0.0:8000'

# yes命令：重复输出字符串，不带参数则默认输出y。例如 `yes | apt-get install xxx`会默认输出y

# 网络相关
ifdown eth0 # 禁用eth网卡
ifup eth0

# 随机数
echo $RANDOM

# 除法
echo $RANDOM / 28 | bc
echo $RANDOM % 28 | bc
```

## Shell Script

- 最好用`/bin/bash`来执行，不要直接用`/bin/sh`来执行，bash会有很多高级点的功能，且也经常用到

#### 变量

```shell
a=$(command)	# 将命令的结果赋给变量
echo "abdc$a"	# 双引号内部的语句可以直接引用变量，但是变量名后面不能有多的字符
echo "abc"$a"def"	# 可以这样字符串和变量直接相加

VAR2=${VAR:-haofly}	# 如果变量VAR不存在，后面就是它的默认值
VAR2=${VAR/.tar.gz}	# 如果VAR的值为haofly.tar.gz，那么VAR2=haofly，一种替换
length=$(#array[@]}或者length=$(#array[*]} # 获取数组长度
```

#### 流程控制

```shell
command A && command B || command C	# 这才是最简单的if else语句
command A || (command C) && command D # 注意，如果打了括号，那么该语句会

if语句：
	-z：为空
	-n：不为空
	-gt：大于
	-lt: 小于
	-le: 小于等于
	-ge: 大于等于
	-eq: 等于，仅针对数字
	==: 等于，针对字符串
	
# 判断文件是否存在
if [ ! -f "$filename" ]; then	# 文件夹有-d
touch "$filename"
fi

# 判断文件是否为空
if [[ ! -s filename ]]; then
echo 'a'
fi

# 判断当前是否有sudo权限
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo: sudo $0 $*"
    exit 1
fi

# 多个if判断
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]; then
    echo "it's not ok"
fi

# if...elif...else...fi
if []; then
	...
elif []; then
	...
else
	...
fi

if [ ! `which vim` ]; then yum install vim; fi

或且非
# -a 与
# -o 或
# ！非
```

#### 特殊符号

```shell
[[]]：双中括号，之间的字符不会发生文件名扩展或者单词分割
(())：双小括号，整数扩展，其中的变量可以不适用$符号前缀
$?：获取上一条命令的退出码，0表示成功，其他则是失败 exit code
$@: 获取所有参数
```

#### 日期/时间处理

```shell
date +"%s"	# 按照时间戳来显示
date +"%m-%d-%y"	# mm-dd-yy格式
date +"%T"	# 仅显示时间，比如10:44:00
time1=$((($(date +%s ) - $(date +%s -d '20210101'))/86400)) # 日期相减，计算间隔日期
```

#### 随机数
​	$RANDOM	# 生成一个随机数

#### 特殊操作

```shell
. /etc/*.conf		# 导入配置文件，这样配置文件里面的变量就可以直接使用了
find ./ -name "*.log" -mtime -1 | which read line; do tail -n 5 "$line" > ~/bak/"$line"; done # 查找，然后按行进行执行
while read line do 语句 done  # 一行一行地进行处理，真正的处理
	
# xargs：将上一个管道的输出直接作为这个管道的输入
ps | grep python | awk -F ' ' '\{print $1\}' | xargs kill

date+\%Y-\%m-\%d   # 获取今天的日期

/sbin/ifconfig eth0 | grep 'inet ' | cut -d: -f2 | awk '{ print $2 }	# 获取网卡的IP地址

echo -e '\035\nquit' | telnet 192.168.1.1 23 && echo "success" || echo "failed"	# shell判断telnet端口是否能够访问，并能自动退出

if [ "$(stat -c '%a' /usr/local/src)" == "777" ]	# 判断文件夹权限

# 使用shell来判断ftp server是否能够连接，是否有权限
ftp -n $ftp_host $ftp_port << EOF
quote USER ${ftp_user}
quote pass ${ftp_pass}
mkdir test
rmdir test
EOF
if [[ "${PIPESTATUS[2]}" != 1 ]]; then
  echo "Error"
  exit 1
fi
```

## 域名解析

- 泛域名证书，例如`*.haofly.net`仅支持通配符当前级别的域名，不支持更高一级域名，例如`a.b.haofly.net`三级域名，如果要三级域名也通配符需要单独申请另外一个证书才行
- MX记录后面是需要加小数点的

# TroubleShooting

- **Linux下笔记本触摸板无法使用的问题**
  我的电脑是宏碁E1-471G, ubuntu13.04，以下几个方法依次尝试

  ```shell
  # 方法一
  Fn + F7 
  # 方法二
  Ctrl + Fn + F7 
  # 方法三
  执行命令sudo modprobe -r psmouse然后sudo modprobe psmouse proto=imps同时，为了开机有效，新建文件/etc/modprobe.d/options，添加代码options psmouse proto=imps
  ```

- **Ubuntu无法调节屏幕亮度** 

  ```shell
  # 方法一 
  ## vim/etc/default/grub文件，将GRUB_CMDLINE_LINUX=""修改为
  GRUB_CMDLINE_LINUX="acpi_backlight=vendor" 
  ## 然后执行sudo update-grub更新grub 
  ## vim /etc/rc.local文件，在exit 0这行代码之前加上
  echo 100 > /sys/class/backlight/intel_backlight/brightness 
  ## 再重启  

  # 方法二 
  ## vim /usr/share/X11/xorg.conf.d/20-intel.conf添加如下代码：
  Section "Device"
  Identifier "card0"
  Driver "intel"
  Option "Backlight" "intel_backlight"
  BusID "PCI:0:2:0"
  EndSection
  ## 重启
  ```

- **Linux内核的更新** 
  **CentOS**：[CentOS 6.5 升级内核到 3.10.28](http://cn.soulmachine.me/blog/20140123/)
  **Ubuntu**：[使用dpkg安装ubuntu内核](http://blog.skyx.in/archives/216/)

- **Deepin升级时出现"这种情况的原因可能是本地依赖已经损坏"** 
  刚装上Deepin(2014.2)发现在应用商店升级时，有3个安装包无法升级(使用apt-get也提示无法升级)，原因可能是下载的包的依赖关系发生改变而引起的，解决方法如下： 

  ```shell
  sudo apt-get clean    # 清除已经下载的安装包
  sudo apt-get update   # 重新更新软件列表
  sudo apt-get dist-upgrade	# 与upgrade不同，dist-upgrade能够忽略Packages中的相关性问题进行强制升级，在依赖关系前后发生改变后也仍然会进行升级。
  ```


- **XShell连接FTP出现`The data connection could not be established: ETIMEDOUT - Connection attempt timed out`错误**

  在连接管理里面讲当前ftp连接类型设置为普通ftp`only use plain FTP (insecure)`

- **Linux网卡设置**  

  - 有些系统使用`ip`命令来代替`ifconfig`

  ```shell
  # ifconfig或者ip addr show
  enp2s0    Link encap:以太网  硬件地址 fc:aa:14:4e:ed:18    
            inet 地址:192.168.1.41  广播:192.168.1.255  掩码:255.255.255.0  
            inet6 地址: fe80::feaa:14ff:fe4e:ed18/64 Scope:Link  
            UP BROADCAST RUNNING MULTICAST  MTU:1500  跃点数:1  
            接收数据包:182927 错误:0 丢弃:0 过载:0 帧数:0  
            发送数据包:89825 错误:0 丢弃:0 过载:0 载波:0  
            碰撞:0 发送队列长度:1000   
            接收字节:203392327 (203.3 MB)  发送字节:7662359 (7.6 MB)  
  
  lo        Link encap:本地环回    
            inet 地址:127.0.0.1  掩码:255.0.0.0  
            inet6 地址: ::1/128 Scope:Host  
            UP LOOPBACK RUNNING  MTU:65536  跃点数:1  
            接收数据包:7423 错误:0 丢弃:0 过载:0 帧数:0  
            发送数据包:7423 错误:0 丢弃:0 过载:0 载波:0  
            碰撞:0 发送队列长度:0   
            接收字节:628267 (628.2 KB)  发送字节:628267 (628.2 KB)  
  ```

  一般lo表示本地还回，eth0表示以太网卡，wlan0表示无线网，但是有时候非常奇葩，比如我这里这台服务器的以太网卡叫enp2s0，我树莓派上的网卡叫什么`wl0`
  静态网络设置:

  ```shell
  ## vim /etc/network/interfaces  # 这里仅设置eth0网卡  
  auto eth0  
  iface eth0 inet static  
  address 192.168.1.100  
  netmask 255.255.255.0  
  gateway 192.168.1.1 
  ## vim /etc/resolv.conf  # 不知道为什么有次设置了上面的还是无法联网，再修改DNS设置就行
  nameserver 192.168.1.1  # 这里加一行，这里的IP是我路由的IP，如果重启后又不能联网了，可能是这个文件又复原了。。。  
  # 重启网卡  
  /etc/init.d/networking restart**
  ```

  WiFi网络设置

  ```shell
  **$ vim /etc/network/interfaces  # 这里设置wlan0我那个卡
  auto wlan0
  allow-hotplug wlan0
  iface wlan0 inet dhcp
  wpa-ssid WIFI名称
  wpa-psk WIFI密码  
  
  # 重启网卡  
  sudo ifdown wlan0 && sudo ifup wlan0
  ```


- **Virtualbox虚拟机网卡丢失**
  一般发生在采用以前的vdi新建虚拟机之后，发现只有lo网卡，eth0网卡丢失，修复过程如下：

  ```shell
  # 首先使用如下命令查看可用的网卡
  ifconfig -a  # 这不仅会显示lo网卡，还会显示其它可用的网卡，如eth0，名字不固定，比如我这次是eth1
  
  # 记住上面以太网卡的名字，然后执行
  sudo dhclient eth0   # 将该网卡打开
  
  # 当然很有可能在网络设置里面没有该网卡，导致重启后依然无法联网的情况，我的网卡设置里就是eth0但现在应该变为eth1了，参考上面的/etc/network/interfaces文件
  ```

- **apt-get update时出现Unknown error executing gpgv等问题** 

  ```shell
  cd /usr/local/lib/
  mv libreadline* /temp
  ldconfig
  apt-get update
  ```

- **CentOS安装Nginx/Tengine出现"configure: error: the HTTP rewrite requires the PCRE library"**

     `yum -y install pcre-devel openssl openssl-devel`

- **全局中文utf8环境**

  ```shell
  # CentOS
  localedef -i zh_CN -c -f UTF-8 zh_CN.utf-8
  export LANG=zh_CN.UTF-8
  然后全局生效,vim /etc/locale.conf
  LANG=zh_CN.UTF-8
  LC_COLLATE=zh_CN.UTF-8
  
  # Ubuntu
  sudo locale-gen zh_CN.UTF-8
  sudo update-locale
  sudo vim /etc/environment # 添加如下两行
  LC_ALL=zh_CN.UTF-8
  LC_CTYPE=zh_CN.UTF-8
  sudo vim ~/.bashrc # 添加如下两行
  export LC_ALL=zh_CN.UTF-8
  export LC_CTYPE=zh_CN.UTF-8
  # 最后重新登录终端即可
  ```

- **免密码登录仍然要求输入密码**

  ```shell
  # 权限问题
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/authorized_keys
  ```

- **CentOS7 无法使用命令netstat，nmap**
  原因是CentOS7抛弃了这几个老旧的命令，使用新的命令进行[替代](https://dougvitale.wordpress.com/2011/12/21/deprecated-linux-networking-commands-and-their-replacements/#netstat)了，如果要使用那几条命令，可以`yum install net-tools / apt install net-tools`

- **CentOS出现:"cannot find a valid baseurl for repo"** 
  CentOS minimal默认是没有开启网卡的，需要将`vim /etc/sysconfig/network-scripts/ifcfg-eth0
  `中的`ONBOOT=no`修改为`ONBOOT=yes`，然后执行`dhclient`，再重启就可以了

- **make: yacc: Command not found**  

   ```shell
   sudo apt-get install bison -y
   sudo apt-get install bison -y
   ```

- **/bin/bash: line 9: makeinfo: command not found**

   `sudo apt-get install texinfo`

- **g++: command not found**

   `yum install gcc-c++`


- `Too many levels of symbolic links `

  出现这个错误是由于在创建软链接的时候使用的是相对路径，重新用绝对路径创建链接即可

- **ssh 出现"Too many authentication for "root""**
  连接的时候加一个参数:`ssh -o PubkeyAuthentication=no root@...`

- **ssh 出现“SSH Too Many Authentication Failures”**: 如果自己确实没有太多的认证失败，那么可能是因为.ssh下的认证文件太多，登陆的时候全都尝试了一遍，可以添加一个参数`ssh -o IdentitiesOnly=yes root@...`来表明只使用identity文件来尝试登陆
  
- **在server上面安装Teamviewer的时候提示`framebuffer not available,Please make sure that /dev/fb0 is accessible and it is configured to 32-bit depth.`相关问题**：需要安装相关的显示依赖:

  ```shell
  yum install centos-release-xen
  yum update
  reboot
  ```

- **切换用户出现`This account is currently not available`的问题**，原因是要切换的用户没有bash登录的权限，`cat /etc/passwd`可以看到该用户的shell是`/sbin/nologin`，应该直接把它改成`/bin/bash`，当然，安全着想，有些用户不建议使用bash shell

- **`sudo echo > file`出现`Permission denied`错误**，没错，用sudo居然也会出现权限错误，因为重定向符号`>`也是bash的命令，也需要给它单独的root权限，所以这里一般这样子解决

  ```shell
  # 方法一
  sudo sh -c "echo abc > target"
  # 方法二
  echo abc | sudo tee target
  echo abc | sudo tee -a target	# 追加>>
  ```

- **`add-apt-repository`的时候居然Python的错误:`Python error: UnicodeDecodeError: 'ascii' codec can't decode byte 0xc5`**，需要在add前设置语言编码
  `LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php`

- **`add-apt-repository: command not found`**，需要安装基本的工具`apt-get install software-properties-common`

- **`aptitude: command not found`**: `sudo apt-get install aptitude`

- **`sudo`命令出现`sudoers`错误，错误详情如下**。这种情况，只能进单用户模式去修改了。

  ```shell
  　　sudo： >>> /etc/sudoers：syntax error 在行 21 附近<<<
  　　sudo： /etc/sudoers 中第 21 行附近有解析错误
  　　sudo： 没有找到有效的 sudoers 资源，退出
  　　sudo： 无法初始化策略插件
  ```

- **Linux进入单用户模式**: 常用于权限错误或者root密码的修改。进入方法:

  1. 重启系统，一直按着上下键，以等到切换启动内核的界面
  2. 选择高级选项里面的`recovery mode`，但是现在不要点击回车，选中后按`e`进行编辑
  3. 将`ro recovery nomodeset`改为`rw single init=/bin/bash`
  4. 按下`F10`进入单用户模式。当前用户就是`root`，把不正常的配置或者密码都修改掉以后，重启系统

- **更新时候提示`由于没有公钥，无法验证下列签名 **: 原因是加入了不被信任的源，这时候，要么把该源删除掉，要么从认证服务器导入该公钥。例如

  ```shell
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ABCDEFG # ABCDEFG就是刚才错误提到的key
  ```

- **Connecting to ftp.debian.org (2001:67c:2564:a119::148:12) Connecting to hwraid.le-vert.net (2001:bc8:357c::1)**，该错误是因为apt在访问该源地址的时候自动使用了`IPv6`，而你的机器却不支持`IPv6`，所以需要强制开启一下

  ```shell
  apt-get -o Acquire::ForceIPv4=true update	# 临时使用IPv4
  # sudo vim /etc/apt/apt.conf.d/99force-ipv4，加入如下内容以后都使用IPv4
  Acquire::ForceIPv4 "true";
  ```

- **升级时出现大量`下列软件包的版本将保持不变`**: 执行`sudo apt-get dist-upgrade`，该命令会强制更新

- **`E: Invalid message from method gpgv: NO_PUBKEY 04EE7237B7D453EC`**，可以采用以下方式进行恢复

  ```shell
  sudo add-apt-repository ppa:webupd8team/y-ppa-manager
  sudo apt-get update
  sudo apt-get install y-ppa-manager
  sudo y-ppa-manager
  # 然后点击Advanced->Try to import all missing GPG keys
  ```

- `sudo apt-get update出现`如下错误:

  ```shell
  正准备解包 .../xxxxxxxxxxx.deb  ...
  正在将 xxxxxxxxxxx:i386 (linux mint) 解包到 (linux mint) 上 ...
  dpkg: 处理归档 /var/cache/apt/archives/xxxxxxxxx.deb (--unpack)时出错：
  尝试覆盖共享的 'xxxxx', 它与软件包 xxxxx 中的其他实例不同
  由于已经达到 MaxReports 限制，没有写入 apport 报告。
  ```

  可以这样修复

  ```shell
  sudo mv /var/lib/dpkg/info /var/lib/dpkg/info_back
  sudo mkdir /var/lib/dpkg/info
  sudo apt-get update
  sudo apt-get install -f 
  ```

- `root`用户可以直接执行，`sudo`却提示命令没找到`command not found`，这是因为使用`sudo`执行的时候，环境变量会默认设置为`/etc/sudoers`文件中`secure_path`所指定的值

- **SSH KEY公钥添加成功，但依然无法登录**: 一般是认证文件权限的问题，权限过高和过低都不行，`~/.ssh`文件夹的权限是700，`~/.ssh/*`的权限是600.

- **`rm -rf`删除目录的时候报错: 目录非空**: 检查一下是否有进程在占用目录，或者目录下是否有一些隐藏的状态文件

- **spawn command not found**: `spawn`命令必须在安装`except`之后，并且不能在`/bin/bash`中使用，只能在`!/usr/bin/expect`中使用

- **vsftpd出现refusing to run with writable root inside chroot()**: 需要在`/etc/vsftpd/vsftpd.conf`设置`allow_writeable_chroot=YES`

- **Linux mint20安装向日葵报错`grep: /etc/upstream-release: 是一个目录 `**: 这是因为`sunlogin`没有获取到正确的系统版本，可以这样做:

  ```shell
  # 想将判断版本的几个文件做个备份
  sudo mv /etc/os-release /etc/os-release.bak
  sudo mv /etc/issue /etc/issue.bak
  sudo mv /etc/upstream-release/ /etc/bak
  
  # vim /etc/os-release，写入如下信息
  NAME="Linux Mint"
  VERSION="20 (Ulyana)"
  ID=linuxmint
  ID_LIKE=ubuntu
  PRETTY_NAME="Linux Mint 20"
  VERSION_ID="20"
  HOME_URL="https://www.linuxmint.com/"
  SUPPORT_URL="https://forums.ubuntu.com/"
  BUG_REPORT_URL="http://linuxmint-troubleshooting-guide.readthedocs.io/en/latest/"
  PRIVACY_POLICY_URL="https://www.linuxmint.com/"
  VERSION_CODENAME=ulyana
  UBUNTU_CODENAME=foca
  
  # /etc/issue，写入如下信息
  Ubuntu 18.04 LTS \n \l
  ```

- **linux系统变为了只读**

  ```shell
  mount	# 查看当前挂载了哪些磁盘，找到只读盘，例如/dev/sda1
  umount /dev/sda1
  mount /dev/sda1 /boot
  remouont -o rw,remount /boot
  ```

- **卸载磁盘`umount target is busy`**: 可以这样来卸载busy中的磁盘

  ```shell
  umount -lf /dev/sda1	# f指force，l指lazy
  ```
  
- **AWS mount磁盘报错: Filesystem xvdg has duplicate UUID - can't mount**: 可以忽略uuid: `mount -o nouuid /dev/xvdg /data`

- **Failed to fetch xxx 404 Not Found [IP: ]**: 可能需要更一下包列表`apt-get update`

- `chmod和chown不起作用`，发生在挂载的磁盘上面的问题，试试重新挂载的时候设置umask为000，如果不行的话，就用`mount`命令看看那个磁盘的格式，如果是windows的格式，例如vfat、ntfs，那么可能不支持，那么办法了

- **查看linux服务器莫名其妙重启/关机的原因**: 主要还是查看`/var/log/syslog`，可以使用下面的命令:

  ```shell
  sudo grep -iv ': starting\|kernel: .*: Power Button\|watching system buttons\|Stopped Cleaning Up\|Started Crash recovery kernel' \
    /var/log/messages /var/log/syslog /var/log/apcupsd* \
    | grep -iw 'recover[a-z]*\|power[a-z]*\|shut[a-z ]*down\|rsyslogd\|ups'
  ```

- **ssh输入密码后就挂起了无法登陆**：可能是路由器的问题，可以加一个参数试试: `ssh -o IPQoS=0x00 ubuntu@...`

- **Ubuntu系统升级后apache或者nginx服务器不再解析PHP**: 应该是在升级系统后apache的php模块掉了，而且我的mysql模块也没了，可以尝试`sudo apt install libapache2-mod-php && sudo apt-get install php-mysql && sudo systemctl restart apache2`

- **检测TLSv1.2，TLSv1.1、ssl是否工作正常**: 可以用curl调用这个网址https://badssl.com/
