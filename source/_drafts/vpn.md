## L2TP over IPsec
- 一键搭建：https://github.com/hwdsl2/setup-ipsec-vpn/blob/master/README-zh.md
- linux服务器无桌面环境连接Ipsec服务端，修改自[ubuntu 终端里如何连接vpnd](https://github.com/hwdsl2/setup-ipsec-vpn/issues/960，下面是部分Dockerfile内容

```shell
FROM ubuntu:20.04

RUN echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
RUN echo "resolvconf resolvconf/linkify-resolvconf boolean false" | debconf-set-selections
RUN sysctl -p
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y apt-utils debconf-utils dialog init libreswan resolvconf wget vim expect && apt-get clean all
RUN ln -s $(which ipsec) /usr/local/sbin/ipsec
RUN wget https://git.io/vpnupgrade -O vpnupgrade.sh && sudo sh vpnupgrade.sh
RUN rm /usr/local/sbin/ipsec~ && rm /usr/sbin/ipsec
RUN ipsec initnss
RUN sed -i "s/#logfile/logfile/" /etc/ipsec.conf && touch /var/log/pluto.log


# 启动容器
docker build -t vpn:check .
docker run --name vpn --privileged=true -dit vpn:check /sbin/init
docker exec -it vpn bash

# 容器里需要这样做
ipsec import vpnclient.p12	# 倒入ipsec服务端在一键安装脚本安装后生成的vpnclient.p12文件
certutil -L -d /etc/ipsec.d	# 如果有vpnclient表示导入成功了
vim /etc/ipsec.d/vpnclient.conf # 如下内容，除了下面中文地方需要修改，其他地方不用修改
conn VPN服务的IP
        left=%defaultroute
        leftcert=vpnclient
        leftid=%fromcert
        leftrsasigkey=%cert
        leftsubnet=0.0.0.0/0
        leftmodecfgclient=yes
        right=VPN服务的IP
        rightsubnet=0.0.0.0/0
        rightid=vpnclient.p12文件里面的那个IP，是服务器最初的IP
        rightrsasigkey=%cert
        narrowing=yes
        ikev2=insist
        rekey=no
        fragmentation=yes
        mobike=no
        auto=add

# 启动客户端
ipsec addconn vpn.example.com
ipsec restart
ipsec auto --up vpn.example.com
tail -f /var/log/pluto.log	# 日志
curl -L ip.gs # 检查IP
```

