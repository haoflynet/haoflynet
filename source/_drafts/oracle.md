## OCI(Oracle Cloud Infrasturcture)

- Oracle的命令行工具

### 安装

- 安装非常方便，这是[不同系统的安装文档](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)，安装过程会问得很详细，基本上默认选项就可以了，安装完成后执行命令会说没有config文件，参考其提示一步一步设置即可，最后还需要把Public Key上传到API Keys中。上传后可能要等几分钟才生效。

### 常用命令

```shell
# 用户管理iam
oci iam compartment list --all	# 列出所有的compartment，可以获取到compartment id，下面很多命令都需要的

# 计算资源compute
oci compute instance list --compartment-id=ocidxxxxx	# 列出所有的实例

# 公网IP，public-ip
oci network public-ip list --compartment-id=ocidxxxxx --scope=REGION	# 列出所有的公网IP
oci network public-ip update --public-ip-id=ocid1.publicip.xxxxxxx --private-ip-id= # 将公网IP与私有IP解绑
oci network public-ip update --public-ip-id=ocid1.publicip.xxxxxxx --private-ip-id=ocid1.privateip.xxxxxx # 将公网IP绑定到指定的私有IP

# 私网IP，private-ip
oci network private-ip get --private-ip-id=ocid1.privateip.xxxxxxx

# 获取VNIC详情
oci network vnic get --vnic-id=ocid1.vnic.xxxxx
```

