---
title: "AWS 常用配置"
date: 2021-01-22 14:40:00
updated: 2021-02-19 08:40:00
categories: Javascript
---

- Aws的密钥只能下载一次，下载后请小心保存

## EC2

### 如何删除EC2实例

- 先选中要删除的实例，Stop，再Terminate，这个时候虽然实例还在，但其实已经删除了，大概等个10分钟左右就没了

### EC2实例扩容

1. 首先先关机`Actions -> Instance State -> Stop`
2. 进入卷管理: `Elastic Block Store -> Volumes`
3. 选择需要更改的磁盘: `Modify Volume`，然后输入大小
4. 重启实例，并进入终端
5. 使用`df-h`查看当前磁盘容量

### EC2配置Cloudwatch

#### 添加自定义指标

<!--more-->

- 需要在服务器安装aws CLI工具，不同操作系统安装方式见[Installing, updating, and uninstalling the AWS CLI version 2 on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)

- 还需要编写自定以脚本，脚本如下:

```shell
#!/bin/bash
set -x
USEDMEMORY=$(free -m | awk 'NR==2{printf "%.2f\t", $3*100/$2 }')	# 内存监控
DISK_USAGE=$(df -h |grep '/dev/xvda1' |  awk '{ print $5 }' | tr -cd [:digit:])	# 磁盘监控
INSTANCE='i-xxxxxxxx'	# 设置当前instance的id
http_status_code=$(curl --write-out %{http_code} --silent --output /dev/null https://haofly.net)	# HTTP状态监控
mongo_connections_available=$(mongo --eval "printjson(db.serverStatus().connections.available)" | tail -1)	# 监控mongo状态
ssl_expire_day=$(sudo certbot certificates|grep Expiry|awk  '{print $6}')	# 监控let's encrypt ssl证书过期时间

/usr/local/bin/aws cloudwatch put-metric-data --metric-name memory_usage --dimensions Instance=$INSTANCE  --namespace "Custom" --value $USEDMEMORY
/usr/local/bin/aws cloudwatch put-metric-data --metric-name disk_usage --dimensions Instance=$INSTANCE  --namespace "Custom" --value $DISK_USAGE
/usr/local/bin/aws cloudwatch put-metric-data --metric-name staging_500 --dimensions Instance=$INSTANCE  --namespace "Custom" --value $http_status_code
/usr/local/bin/aws cloudwatch put-metric-data --metric-name mongo_available --dimensions Instance=$INSTANCE  --namespace "Custom" --value $mongo_connections_available
/usr/local/bin/aws cloudwatch put-metric-data --metric-name ssl_expire_day --dimensions Instance=$INSTANCE  --namespace "Custom" --value $ssl_expire_day
```

编写完自定义脚本后添加可执行权限`chmod +x watch.sh`，然后可以手动执行一下看看能不能成功，执行完一次过后cloudwatch后台在创建指标的时候就能选择这些指标了。我们可以定时执行这个脚本:

```shell
crontab -e
*/1 * * * * /home/ubuntu/watch.sh	# 设置为每分钟执行一次
```

## S3

### 开放S3桶的公共访问权限

- 需要在Bucket的`Permissions`上进行以下设置

```shell
# Block public access (bucket settings)关闭以下几个权限
Block all public access
	Block public access to buckets and objects granted through new access control lists (ACLs)
	Block public access to buckets and objects granted through any access control lists (ACLs)
	Block public access to buckets and objects granted through new public bucket or access point policies
	Block public and cross-account access to buckets and objects through any public bucket or access point policies

# Bucket policy，编辑Policy，例如:
{
    "Version": "2012-10-17",
    "Id": "Policy1606902711529",
    "Statement": [
        {
            "Sid": "Stmt1606902709971",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mybucketname/path1/*"
        },
        {
            "Sid": "Stmt1606902709972",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mybucketname/path2/*"
        },
        {
            "Sid": "Stmt1606902709973",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mybucketname/path3/*"
        }
    ]
}

# Cross-origin resource sharing (CORS)，这里可以设置跨域请求地址
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "POST"
        ],
        "AllowedOrigins": [
            "https://haofly.net",
            "https://a.haofly.net"
        ],
        "ExposeHeaders": [
            "x-amz-server-side-encryption",
            "x-amz-request-id",
            "x-amz-id-2"
        ],
        "MaxAgeSeconds": 3000
    }
]

```

## CodeDeploy/Pipeline

- CodeDeploy日志位置: `/var/log/aws/codedeploy-agent/codedeploy-agent.log`
- 部署日志位置: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`
- `CodeDeply Agent`安装方式见https://docs.aws.amazon.com/zh_cn/codedeploy/latest/userguide/codedeploy-agent-operations-install-ubuntu.html

## 开发

- [ 官方的js sdk](https://www.npmjs.com/package/aws-sdk)

##### TroubleShooting

- **InstanceAgent::Plugins::CodeDeployPlugin::CommandPoller: Missing credentials** : 需要重启一下agent: `sudo service codedeploy-agent restart`