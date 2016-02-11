---
title: "SSL各种格式证书的转换(JKS to PEM, KEY, CRT)"
date: 2015-08-04 11:05:06
categories: 编程之路
---
原文链接：<http://ju.outofmemory.cn/entry/108566>

_fuck，最讨厌java了，有同事说JKS是Java特有的东西，所以必须调用Java才能使用，but，I use Python，nothing is im
possible，发现使用requests来直接调用其它格式的证书文件就行，当然，Python也可以用pyjks包来将jks转换为其它格式，但没必要那样做，
因为直接用ssl工具转换就可以一劳永逸了。_

JKS(Java
KeyStore)是Java的一个证书仓库，包括授权整数和公钥整数等。JDK提供了一个工具keytool用于管理keystore。转换步骤：

  1. 使用keytool导出成PKCS12格式：

        # keytool -importkeystore -srckeystore server.jks -destkeystore server.p12 -srcstoretype jks -deststoretype pkcs12
    输入目标密钥库口令:  

    再次输入新口令:
    输入源密钥库口令:  

    已成功导入别名 ca_root 的条目。
    已完成导入命令: 1 个条目成功导入, 0 个条目失败或取消

  2. 生成pem证书(包含了key，server证书和ca证书)：

        # 生成key 加密的pem证书
    $ openssl pkcs12 -in server.p12 -out server.pem
    Enter Import Password:
    MAC verified OK
    Enter PEM pass phrase:
    Verifying - Enter PEM pass phrase:




    # 生成key 非加密的pem证书




    $ openssl pkcs12 -nodes -in server.p12 -out server.pem
    Enter Import Password:
    MAC verified OK

  3. 单独导出key：

        # 生成加密的key
    $ openssl pkcs12 -in tankywoo.p12  -nocerts -out server.key
    Enter Import Password:
    MAC verified OK
    Enter PEM pass phrase:
    Verifying - Enter PEM pass phrase:




    # 生成非加密的key




    $ openssl pkcs12 -in tankywoo.p12 -nocerts -nodes -out server.key
    Enter Import Password:
    MAC verified OK

  4. 单独导出server证书：

        $ openssl pkcs12 -in server.p12  -nokeys -clcerts -out server.crt
    Enter Import Password:
    MAC verified OK

  5. 单独导出ca证书：

        $ openssl pkcs12 -in server.p12  -nokeys -cacerts -out ca.crt
    Enter Import Password:
    MAC verified OK

# TroubleShooting：

1.至于原文中出现的导入ca_root证书出现错误，它那个方法貌似不管用，这里建议将Java升级到Java8即可成功导入。

2.在Python中使用ssl时(无论是用httplib、ssl还是requests)，可能出现以下错误：



    Traceback (most recent call last):
      File "client.py", line 10, in <module>
        ssl_sock.connect(('', 9000))
      File "/Users/amk/source/p/python/Lib/ssl.py", line 204, in connect
        self.ca_certs)
    ssl.SSLError: [Errno 0] _ssl.c:327: error:00000000:lib(0):func(0):reason(0)

根本原因就是提供的证书是错误的
