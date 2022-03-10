---
title: "AWS 常用配置"
date: 2021-01-22 14:40:00
updated: 2021-11-24 08:42:00
categories: Javascript
---

- Aws的密钥只能下载一次，下载后请小心保存

## EC2

### 如何删除EC2实例

- 先选中要删除的实例，Stop，再Terminate(终止实例)，这个时候虽然实例还在，但其实已经删除了，大概等个10分钟左右就没了

### EC2实例升级/修改实例类型

- IP会变更，请注意是否启用弹性IP或者负载均衡器

- 关机，需要接近一分钟
- `操作->实例设置->更改实例类型`

### EC2实例扩容

#### 关机扩容

1. 关机扩容很简单，但是IP会变更，请注意是否启用弹性IP或者负载均衡器
2. 首先关机`Actions -> Instance State -> Stop`
3. 进入卷管理: `Elastic Block Store -> Volumes`
4. 选择需要更改的磁盘: `Modify Volume`，然后输入大小
5. 重启实例，并进入终端
6. 使用`df -h`查看当前磁盘容量

#### 不关机扩容

1. 在实例详里面找到root volumn，进入volumn详情

2. `Actions -> Modify Volume`，输入扩容后的大小点击确定

3. 进入实例，此时用`df -h`查看依然是原来的大小，使用`lsblk`命令可以查看有新的大小，该命令用于查看是否具有必须扩展的分区，例如:

   ```shell
   xvda    202:0    0   30G  0 disk
   └─xvda1 202:1    0   20G  0 part /	# df -h只能看到这个分区
   ```

4. 执行扩容命令

   ```shell
   # 有时候lsblk看到的磁盘名称和df -h显示的磁盘名称不一致，没关系，下面的命令按照lsblk的来就行
   
   sudo growpart /dev/xvda 1
   lsblk	# 验证xvda1的大小是否已经变化，不过此时用df -h依然看不出变化
   
   sudo resize2fs /dev/xvda1	# 此时用df -h就能看到变化了，扩容过程也完成了
   ```

### EC2增加磁盘

- 步骤

  1. 创建卷

  2. `操作->连接卷`，默认会挂载到`/dev/sdf`

  3. 进入实例，执行`lsblk`可以看到附加的卷(磁盘)

  4. 新卷默认是没有文件系统的，可以这样确定:

     ```shell
     sudo file -s /dev/xvdf # 如果输出是/dev/xvdf: data表示没有文件系统
     sudo mkfs -t xfs /dev/xvdf	# 创建文件系统，如果找不到mkfs命令，可以安装xfsprogs
     ```

  5. 挂载

     ```shell
     sudo mkdir /data	# 创建挂载点
     sudo mount /dev/xvdf /data	# 挂载
     df -h	# 确认是否挂载成功
     ```

### Ec2绑定Elastic IP弹性IP

- 弹性IP只要是绑定在运行中的ec2实例上就是免费的，所以如果仅仅是要一个不会随着机器状态变化的IP那么推荐用弹性IP而不是用负载均衡器

- 当一个新建的弹性IP被关联到一个实例上的时候，该实例的公有IP地址也会变成一样的，不过之后如果实例重启公有IP会改变，弹性IP则不会了

### EC2配置Cloudwatch

#### 添加自定义指标

<!--more-->

- 需要在服务器安装aws CLI工具，不同操作系统安装方式见[Installing, updating, and uninstalling the AWS CLI version 2 on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
- 对于服务的监控，ELB自带了监控指标的，不需要使用下面脚本中的`http_status_code`，可以在创建监控的时候搜索`5xx`即可看到
- 还需要编写自定一个脚本实现自定义的监控，例如服务健康状态检测，脚本如下:

```shell
#!/bin/bash
set -x
USEDMEMORY=$(free -m | awk 'NR==2{printf "%.2f\t", $3*100/$2 }')	# 内存监控
DISK_USAGE=$(df -h |grep '/dev/xvda1' |  awk '{ print $5 }' | tr -cd [:digit:])	# 磁盘监控
INSTANCE='i-xxxxxxxx'	# 设置当前instance的id
#http_status_code=$(curl --write-out %{http_code} --silent --output /dev/null https://haofly.net)	# HTTP状态监控
mongo_connections_available=$(mongo --eval "printjson(db.serverStatus().connections.available)" | tail -1)	# 监控mongo状态
ssl_expire_day=$(sudo certbot certificates|grep Expiry|awk  '{print $6}')	# 监控let's encrypt ssl证书过期时间

/usr/local/bin/aws cloudwatch put-metric-data --metric-name memory_usage --dimensions Instance=$INSTANCE  --namespace "Custom" --value $USEDMEMORY
/usr/local/bin/aws cloudwatch put-metric-data --metric-name disk_usage --dimensions Instance=$INSTANCE  --namespace "Custom" --value $DISK_USAGE
#/usr/local/bin/aws cloudwatch put-metric-data --metric-name staging_500 --dimensions Instance=$INSTANCE  --namespace "Custom" --value $http_status_code
/usr/local/bin/aws cloudwatch put-metric-data --metric-name mongo_available --dimensions Instance=$INSTANCE  --namespace "Custom" --value $mongo_connections_available
/usr/local/bin/aws cloudwatch put-metric-data --metric-name ssl_expire_day --dimensions Instance=$INSTANCE  --namespace "Custom" --value $ssl_expire_day
```

- 编写完自定义脚本后添加可执行权限`chmod +x watch.sh`，然后可以手动执行一下看看能不能成功，执行完一次过后cloudwatch后台在创建指标的时候就能选择这些指标了。如果执行过程中提示需要`cloudwatch:putMetricData`权限，那么需要去`AWS IAM`里面去分配`cloudwatch`相关的策略，错误信息里面有指定哪个`IAM`用户
- 我们可以定时执行这个脚本:

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
- 只能用于集成了ACM服务的EC2实例，例如(ElasticLoad Balancing [ELB]或Amazon CloudFront分配)，也只有满足这些条件才能自动续订

## Route 53

- AWS的域名管理
- 第一次添加DNS的时候默认时间是`1h`，最好设置成`1m`，否则缓存更新太慢了
- 可以为同一个域名设置多个托管区域(hosted zone)，例如针对同一个域名在测试环境和生产环境分别配置不同的DNS，只需要更改本地的名称服务器就能切换到不同的DNS上去，这样使用感觉有点复杂了
- 如果要用`Route 53`去管理域名的DNS，需要新建托管区域(hosted zone)，然后在域名购买地设置NS记录指向`hosted zone`的四个`NS`记录即可

## ELB/Elastic Load Balancing负载均衡器

- ELB支持多种负载均衡器
  - 应用负载均衡器(Application Load Balancer)：对HTTP/HTTPS请求进行负载均衡
  - 网络负载均衡器(Network Load Balancer)：对网络/传输协议(第4层-TCP、UDP、TLS)以及极端性能/低延迟的应用程序进行负载均衡
  - 网关负载均衡器(Gateway Load Balancer)：IP层
  - ~~(Classic Load Balancer~~)：应用程序在EC2 Classic网络中构建而成，AWS上已经变成灰色了，看来已经放弃了
- 可以直接在EC2管理页面创建负载均衡器，点击`Load Balancer`即可进行创建，如果需要选择ACM管理的SSL证书，可以直接在第二步选择
- 需要注意的是，创建后需要将域名的DNS记录指向负载均衡器的DNS名称，这样才能正确到负载均衡器上
- **负载均衡器默认超时时间是60秒**，如果出现504网关超时错误可能是这个引起的
- 负载均衡器的目标组可以只选择80端口，服务器上也可以只开启80端口，只有在负载均衡器的监听器上面需要监听443，转发到目标组就行了
- 如果是非`Route 53`管理的域名需要指向`elb`需要设置的是CNAME记录
- [价格表](https://aws.amazon.com/cn/elasticloadbalancing/pricing/): 0.0225美元/小时，差不多3.5元/天，简单的还是用弹性IP吧，毕竟是免费的

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

## Lambda

- 通过`process.env.MY_ENV`获取环境变量

- 如果需要安装依赖，要么创建`层`，要么就将`node_modules`一起压缩为`.zip`文件然后上传，可以使用`adm-zip`等方式压缩，但是这样会因为程序包太大而无法使用在线的内联编辑器

  ```javascript
  import AdmZip from 'adm-zip';
  
  const zip = new AdmZip();
  
  zip.addLocalFolder('./dist');
  zip.writeZip('./lambda.zip');
  ```

- 使用`cloudwatch`触发`lambda`，需要在`CloudWatch`控制台创建规则`Events -> Create rule`，`Event Source`可以定时或者选择警告，目标`target`则选择我们创建的`Lambda`函数

实例

```javascript
exports.handler = async (event, context) => {
  // event: 就是测试时间中的key1 value1这些，相当于调用者传入的入参
  // context: 包含有关调用、函数和执行环境的信息，例如logStream,functionVersion,memoryLimitInMB,awsRequestId, logGroupName, logStreamName等
	console.log('xxx') // 可以直接用标准输出输出日志
}
```

## RDS

### MySQL

- [开启创建存储过程的功能](https://aws.amazon.com/premiumsupport/knowledge-center/rds-mysql-functions/?nc1=h_ls)

## DocumentDB (MongoDB)

- 默认启用了tls安全登录设置的，必须下载他们的pem文件才能进行连接，可以在`Amazon DocumentDB -> 参数组`中新建参数组，因为default开头的参数组无法修改，然后在新建的参数组里面将tls给disabled掉，然后再修改集群的参数组即可
- 它是创建在VPC之上的，目前居然不支持公网访问，不同的region之间要访问得给VPC创建对等连接，并且还不支持us-west-1 region，所以最简单的方法是在另外的region创建ec2和documentdb
- 居然不支持`Capped Collections`，可能之后会支持，其他不支持的可以参考[这里](https://docs.aws.amazon.com/documentdb/latest/developerguide/mongo-apis.html)

## Amazon MemoryDB for Redis

- 

## SES/Simple Email Service电子邮件发送和接收服务

## AWS Systems Manager(SSM)

- 管理ec2系统内部的东西，例如通过api或cli向服务器发送命令并执行
- **SSM未发现管理的ec2实例**: 可能是因为`ssm agent`在实例内部未安装或者未安装成功(即使在运行中也可能没有安装成功，还是得看其日志/var/log/amazon/ssm下)，[ssm agent安装文档](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html)，当然`ssm agent`默认是安装了的，可以通过这些命令[查看ssm运行状态](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-status-and-restart.html)

## CodeDeploy/Pipeline

- CodeDeploy日志位置: `/var/log/aws/codedeploy-agent/codedeploy-agent.log`
- 部署日志位置: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`
- `CodeDeply Agent`安装方式见https://docs.aws.amazon.com/zh_cn/codedeploy/latest/userguide/codedeploy-agent-operations-install-ubuntu.html
- 服务器上保留的副本的数量设置`/etc/codedeploy-agent/conf/codedeployagent.yml`里面的`max_revisions`，默认是10，服务器总共才8G，保留不了那么多副本
- `CodeDeploy`拉取的源码和构建后的代码都会自动存储到S3上面去，这些文件可能占用很大的存储，我暂时还不清楚其费用和自动清理的方式，网上有人说用S3的生命周期管理，可是那样不能保证至少保留N个副本

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

## Cron表达式

- 很多地方都会用到cron表达式，比如cloudwatch、ebs生命周期管理器(lifecycle)
- 和我们常规的linux的用法有点不一样，没有隔几天执行的方法，如果要实现只能在日期那里把一个月的写上
- 使用的是UTC时间
- 对于EBS的生命周期管理，最小精度只能是小时，第一位没有用，且可能发生在那个小时里面的任意一分钟

```shell
分钟 小时 日期 月 星期几 年份
0 12 * * ? *	# 每天上午12:00(UTC)运行，相当于我们这边的下午8点
```

## 开发

- [ 官方的js sdk](https://www.npmjs.com/package/aws-sdk)

- 权限验证方式

  -  设置环境变量`export AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=xxx`
  - Lambda，参考下一条tips

- 如果是在aws lambda中运行，可以不需要`access key`和`access id`，只需要在`lambda`的配置中给角色`role`分配权限即可，默认就有一个`CloudWatch`的权限，有一点需要注意的是在`lambda`中需要提前`new instance`然后将函数转换为`promise`的方式，否则函数不会被执行，很奇怪的问题

  ```javascript
  const AWS = require('aws-sdk');
  const ec2 = new AWS.EC2({apiVersion: '2016-11-15'});
  
  exports.handler = async () => {
   	const re = await ec2.describeInstances({DryRun: false}).promise();
  }
  ```

### APIs

```javascript
// 获取实例列表
ec2.describeInstances({
  InstanceIds: ['xxxx']	// 可传入instance id筛选
})

// 获取snapshots列表，包含了所有的snapshots，甚至包括公有的，所以这个接口返回相当大，最好加上筛选参数
ec2.describeSnapshots({
  OwnerIds: ['xxx'],	// 筛选OwnerId，可以找一个自己的snapshots搭上tag，然后筛选tag来找到OwnerId，因为文档说这里可以设置self，但是我就是不行
  Filters: [{
    Name: 'status',
    Values: ['completed']
  }, {
    Name: 'progress',
    Values: ['100%']
  }, {
    Name: 'tag:Name',	// 筛选tag的时候Name=tag:名
    Values: ['myinstance']
  }]
})

// 获取volumes列表
ec2.describeVolumes({
  VolumeIds: ['xxx']	// 可以筛选指定id
})

// 创建卷，创建完成返回的State为creating，等它变成available状态就能用了
ec2.createVolume({
  AvailabilityZone: 'us-east-1a', // 可用区
  SnapshotId: 'xxx',	// 如果是从快照创建卷需要提供这个参数
  TagSpecifications: [{
    ResourceType: 'volume',
    Tags: [{
      Key: 'Name',	// 设置卷名称
      Value: 'myCustomName'
    }]
  }]
})

// 连接卷到实例
ec2.attachVolume({
  InstanceId: '',
  VolumeId: '',
  Device: '/dev/xvdf'	// 这也是必填的，并且必须遵循命名规则https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html
})

ec2.createTags({
  Resources: ['vol-xxxx'],
})

cron(*/10 * * * * *)

ssm.describeInstanceInformation(params)	// 获取ssm管理的设备列表

// 发送命令到服务器执行
ssm.sendCommand({
  DocumentName: 'AWS-RunnShellScript',
  Parameters: {
    commands: [	// command应该是并行执行，前一个出错不会影响后面的，所以如果有需要并行的任务最好写成一条用&&连接
      'systemctl stop mysql && touch /abc'
    ]
  }
})

// 获取sendCommand的执行结果
ssm.listCommandInvocations({
  CommandId: 'xxx',
  Details: true	// 这能返回输出结果
})
```

##### TroubleShooting

- **InstanceAgent::Plugins::CodeDeployPlugin::CommandPoller: Missing credentials** : 需要重启一下agent: `sudo service codedeploy-agent restart`

- **connect EHOSTUNREACH 169.254.169.254:80**: 可能的原因:
  - 网络问题
  - 没有设置`AWS_ACCESS_KEY_ID`和`AWS_SECRET_ACCESS_KEY`环境变量
  
- **wordpress无限重定向**: 可能是在aws的elb中只发了http请求到后端，但是url访问的却是https，导致wordpress搞不清楚了，可以在nginx这边加上一个fastcgi配置:
  
  ```shell
  fastcgi_param HTTPS on;
  ```






我的安全凭证，但是只能创建两个访问密钥，lambda函数不需要创建凭据https://docs.aws.amazon.com/zh_cn/sdk-for-javascript/v3/developer-guide/loading-node-credentials-lambda.html