## OCI(Oracle Cloud Infrasturcture)

- Oracle的命令行工具

### 安装

- 安装非常方便，这是[不同系统的安装文档](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- 配置

```shell
oci setup config
Enter a location for your config [/home/ubuntu/.oci/config]:	# 默认即可
Enter a user OCID:	# 这里的user OCID来自于user profile里面的OCID
Enter a tenancy OCID: # 来自于右上角头像里面的Tenancy里面的OCID
# 其他默认即可
```

- 上传Public Key(`/home/ubuntu/.oci/oci_api_key_public.pem`)到API Keys(`My Profile -> API keys -> Paste a public key`)中，上传后可能需要等几分钟才生效

### 常用命令

```shell
# 用户管理iam
oci iam compartment list --all	# 列出所有的compartment，可以获取到compartment id，下面很多命令都需要的

# 计算资源compute
oci compute instance list --compartment-id=ocidxxxxx	# 列出所有的实例
oci compute instance get --instance-id=ocid1.xxxxx	# 获取实例详情，但是这里不会返回IP，要获取IP还是得用vinc来弄

# 公网IP，public-ip
oci network public-ip list --compartment-id=ocidxxxxx --scope=REGION	# 列出所有的公网IP
oci network public-ip update --public-ip-id=ocid1.publicip.xxxxxxx --private-ip-id= # 将公网IP与私有IP解绑，解绑后服务器内部kennel
oci network public-ip update --public-ip-id=ocid1.publicip.xxxxxxx --private-ip-id=ocid1.privateip.xxxxxx # 将公网IP绑定到指定的私有IP

# 私网IP，private-ip来自于VNIC Details里面的Private IP Address
oci network private-ip get --private-ip-id=ocid1.privateip.xxxxxxx

# 获取VNIC详情, VNIC的OCID在VPIC Details里面获取，注意不是那个FQDN
oci network vnic get --vnic-id=ocid1.vnic.xxxxx
```

