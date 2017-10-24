---
title: "ShadowSocks 教程"
date: 2015-10-06 11:02:30
updated: 2017-10-24 23:45:00
categories: tools
---
## 服务器
1. 安装服务(pypi)已经没怎么维护了，这里直接从github拉取源码)

    ```shell
    git clone -b master https://github.com/shadowsocks/shadowsocks.git
    cd shadowsocks
    python3.6 setup.py install
    ```

    安装完成后使用`ssserver -p 443 -k password -m aes-256-gcm`(完整daemon命令`ssserver -p 443 -k password -m aes-256-gcm --log-file /var/log/ssserver -d start`)进行测试(不再推荐其他协议)，从客户端发起连接，发现能科学上网了。

2. 设置开机启动

    `mkdir /etc/shadowsocks`
    ```shell
    vim /etc/shadowsocks/config.json
    # 在config.json中复制入以下配置：
    {
        "server":"0.0.0.0",
        "server_port":8388,
        "local_address": "127.0.0.1",
        "local_port":1080,
        "password":"yourpassword",
        "timeout":300,
        "method":"aes-256-gcm"
    }
    ```
    其中端口和密码可按需进行修改

3. 启动服务

    ssserver -c /etc/shadowsocks/config.json

## 客户端
1. 安装必要的软件

        yum install -y epel-release
        yum install -y python
        yum install python-pip privoxy
        pip install shadowsocks
2. 修改相应的配置

   ```shell
   #vim /etc/shadowsocks.json
   {
     "server": "250.250.250.250",
     "server_port": "2333",
     "local_address": "0.0.0.0",
     "local_port": 1086,
     "password": "",
     "method": "rc4-md5"
   }
   ```
3. 启动服务

   ```shell
   nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &	# 后台执行
   echo " nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &" >> /etc/rc.local	# 开机自动启动
   ```

## Socks5代理转换为HTTP代理

使用的软件叫做`privoxy`

```shell
sudo apt-get install privoxy
# sudo vim /etc/privoxy/config，将ss代理的配置设置进去
forward-socks5 / 127.0.0.1:1086 .
# 然后重启，sudo /etc/init.d/privoxy restart即可
export HTTP_RPOXY=127.0.0.1:8118	# 默认代理端口是8118
```

