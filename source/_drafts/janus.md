```shell
# 这里官方文档写的libsrtp-dev，但我这边得安装libsrtp2-dev
apt install make meson libmicrohttpd-dev libjansson-dev \
	libssl-dev libsrtp2-dev libsofia-sip-ua-dev libglib2.0-dev \
	libopus-dev libogg-dev libcurl4-openssl-dev liblua5.3-dev \
	libconfig-dev pkg-config gengetopt libtool automake
	
pip3 install ninja

# 安装完成后需要生成配置文件
make configs
```

