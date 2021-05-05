---
title: "AWS 常用配置"
date: 2021-01-22 14:40:00
updated: 2021-03-12 08:42:00
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

- S3的[生命周期管理](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html#glacier-pricing-considerations)，有点绕，还没搞懂
- 通过`Bucket`的`Metrics`可以查看桶的总容量和总的文件数量
- 通过文件夹的`Actions->Calculate total size`可以查看指定文件夹的容量和文件数量

### 使用js sdk操作AWS3

```javascript
import AWS = require('aws-sdk')

const config = {
    accessKeyId: '',
    secretAccessKey: '',
    bucket: 'bucketName'
}

const s3Client = new AWS.S3(config)
s3Client.getObject({
  Bucket: config.bucket,
  Key: 'object path'
}).promise().then(result => {
  console.log(result.Body)
})
```

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

## ACM/AWS Certificate Manager

- AWS的公有SSL/TLS证书是免费的，不过因为ACM管理私钥，所以只能在AWS上面使用。获取步骤还算简单，添加一个CNAME记录，一会儿就好了
- 只能用于集成了ACM服务的EC2实例，例如(ElasticLoad Balancing [ELB]或Amazon CloudFront分配)

## Route 53

- AWS的域名管理
- 可以为同一个域名设置多个托管区域(hosted zone)，例如针对同一个域名在测试环境和生产环境分别配置不同的DNS，只需要更改本地的名称服务器就能切换到不同的DNS上去，这样使用感觉有点复杂了

## ELB/Elastic Load Balancing

- ELB支持多种负载均衡器
  - 应用负载均衡器(Application Load Balancer)：对HTTP/HTTPS请求进行负载均衡
  - 网络负载均衡器(Network Load Balancer)：对网络/传输协议(第4层-TCP、UDP、TLS)以及极端性能/低延迟的应用程序进行负载均衡
  - 网关负载均衡器(Gateway Load Balancer)：IP层
  - ~~(Classic Load Balancer~~)：应用程序在EC2 Classic网络中构建而成，AWS上已经变成灰色了，看来已经放弃了
- 可以直接在EC2管理页面创建负载均衡器，点击`Load Balancer`即可进行创建，如果需要选择ACM管理的SSL证书，可以直接在第二步选择
- 需要注意的是，创建后需要将域名的DNS记录指向负载均衡器的DNS名称，这样才能正确到负载均衡器上
- 负载均衡器的目标组可以只选择80端口，服务器上也可以只开启80端口，只有在负载均衡器的监听器上面需要监听443，转发到目标组就行了

## API Gateway

- [Creating a Serverless Contact Form on AWS](https://levelup.gitconnected.com/creating-a-serverless-contact-form-on-aws-ff339ad1fa60): 使用API Gateway + SES服务创建一个serverless API用于网页的用户表单搜集
- [如何启用 CloudWatch Logs 以对 API Gateway REST API 或 WebSocket API 进行问题排查](https://aws.amazon.com/cn/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/): 

### 映射模板语法

- [文档在这里](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference-programming-guide.html)

```shell
# 这是一个使用EMS发送email的模板
Action=SendEmail&Message.Body.Text.Data=$util.urlEncode("
#set($name = $input.path('$.name'))		# 从POST JSON中获取指定字段的数据，并分配一个变量，不要用$input.json('$.name')去获取那样字符串会默认在前后加上双引号
#if($name && $name.length() != 0)	# if条件语句
Name: $name
#end

#set($index = 1)
#set($emails=$stageVariables.sendEmails.split(','))	# $stageVariables可以从阶段变量取值
#foreach($email in $emails)
email: $email
#set($index = $index+1)
#end
")&Message.Subject.Data=Contact+form+submission&Destination.ToAddresses.member.1=haoflynet%gmail.com&Source=no_reply%40haofly.net
```

### API Gateway权限设置/Resource Policy

- 有多种访问策略：AWS Account Allowlist/IP Range Denylist/Source VPC Allowlist
- [如何排查API Gateway中的HTTP 403禁止访问错误](https://aws.amazon.com/cn/premiumsupport/knowledge-center/api-gateway-troubleshoot-403-forbidden/)
- [如何排查与 API Gateway 私有 API 终端节点的连接问题？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/api-gateway-private-endpoint-connection/)
- [我从 VPC 连接到 API Gateway API 时，为什么会收到 HTTP 403 禁止错误？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/api-gateway-vpc-connections/)

##### 实现仅自己的EC2(指定的VPC)能访问接口其他地方不能访问接口

1. Resource Policy添加如下策略:

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": "*",
               "Action": "execute-api:Invoke",
               "Resource": "arn:aws:execute-api:us-west-2:账户ID:API的ID/APi的Stage/*/*"
           }
       ]
   }
   ```

2. 进入我们想配置的EC2绑定的VPC的配置页面选择左侧菜单栏的`Endpoints(终端节点)`，创建一个新的终端节点。服务类别选择AWS服务，服务名称选择API Gateway的执行服务`com.amazonaws.us-west-2.execute-api`，终端节点类型为`Interface`，然后VPC就是我们需要的VPC，子网可以全选，取消选择`Enable DNS name`禁用私有DNS，其他默认。创建完成后需要等几分钟才能生效

## RDS

### MySQL

- [开启创建存储过程的功能](https://aws.amazon.com/premiumsupport/knowledge-center/rds-mysql-functions/?nc1=h_ls)

## SES/Simple Email Service电子邮件发送和接收服务

## CodeDeploy/Pipeline

- CodeDeploy日志位置: `/var/log/aws/codedeploy-agent/codedeploy-agent.log`
- 部署日志位置: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`
- `CodeDeply Agent`安装方式见https://docs.aws.amazon.com/zh_cn/codedeploy/latest/userguide/codedeploy-agent-operations-install-ubuntu.html
- 服务器上保留的副本的数量设置`/etc/codedeploy-agent/conf/codedeployagent.yml`里面的`max_revisions`，默认是10，服务器总共才8G，保留不了那么多副本
- `CodeDeploy`拉去的源码和构建后的代码都会自动存储到S3上面去，这些文件可能占用很大的存储，我暂时还不清楚其费用和自动清理的方式，网上有人说用S3的生命周期管理，可是那样不能保证至少保留N个副本

需要在项目根目录添加这些文件

```yml
# buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 10
    commands:
      - echo Installing Web App...
  pre_build:
    commands:
      - echo Installing source NPM dependencies...
      - npm install
  build:
    commands:
      - echo Build started on `date`
      - npm run build
  post_build:
    commands:
      - echo Build completed on `date`
artifacts:
  files:
    - app/**/*
    - config/**/*
    - lib/**/*
    - node_modules/**/*
    - public/**/*
    - scripts/*
    - views/**/*
    - .babelrc
    - appspec.yml
    - buildspec.yml
    - package.json
    - package-lock.json
    - pm2.config.js
    - server.js
  discard-paths: no
```

以及

```yml
# appspec.yml
version: 0.0
os: linux
files:
  - source: /
    destination: /home/ubuntu/myproject
permissions:
  - object: ./scripts/
    pattern: "*"
    mode: 755
    type:
      - file
hooks:
  ApplicationStop:
    - location: ./scripts/stop_service.sh
      mode: 755
      runas: root
  ApplicationStart:
    - location: ./scripts/start_service.sh
      mode: 755
      runas: root
  ValidateService:
    - location: ./scripts/validate_service.sh
      mode: 755
      timeout: 30
      runas: root
```

对应的脚本可以这样

```shell
# scripts/start_service.sh
#!/bin/bash
cd /home/ubuntu/myprojct
if [ "$APPLICATION_NAME" == "MyProject-Staging-Application" ]
then
  pm2 reload pm2.config.js --env staging
else
	pm2 reload pm2.config.js --env production
fi

exit

# scripts/stop_service.sh
#!/usr/bin/env bash
isExistApp=`pgrep node`
if [[ -n  $isExistApp ]]; then
sudo kill ${isExistApp}
fi

exit

# scripts/validate_service.sh
#!/bin/bash
echo "service codedeploy-agent restart" | at -M now + 2 minute;
```

## 开发

- [ 官方的js sdk](https://www.npmjs.com/package/aws-sdk)

##### TroubleShooting

- **InstanceAgent::Plugins::CodeDeployPlugin::CommandPoller: Missing credentials** : 需要重启一下agent: `sudo service codedeploy-agent restart`