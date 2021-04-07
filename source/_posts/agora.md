---
title: "Agora 声网 使用手册"
date: 2021-04-01 23:00:00
updated: 2021-04-06 10:00:00
categories: Javascript
---

- 每月1万分钟的免费额度，可以说相当不错的了

## [生成token](https://docs.agora.io/cn/cloud-recording/token_server?platform=All%20Platforms)

- 无论是主持人还是用户还是录制UID进入频道前都需要先生成一个token
- token的生成方式点击标题即可，里面有各种语言生成token的方式
- 生成token必须提供一个UID，得自己找办法和数据库中原有的用户关联
- [token相关错误码](https://docs.agora.io/cn/All/faq/token_error)

## 服务端

- 服务端的`Restful API`都有频率限制且阈值并不高，这是[官方提供的超出频率限制解决方法](https://docs.agora.io/cn/All/faq/restful_api_call_frequency)，可以参考一下，之前我以为hook能够帮助我减少很多请求，但发现并不如我的预期，主要是实效和顺序性的问题

### [Channel相关的服务端Restful API](https://docs.agora.io/cn/rtc/restfulapi/#/)

#### 项目管理

#### 踢人规则

#### 查询在线频道信息

##### 获取用户列表

- 可以同时获取主持人和观众的用户列表，但是只有创建token时候的UID

```shell
# 接口地址: /dev/v1/channel/user/{appid}/{channelName}
```

### [云端录制Restful API](https://docs.agora.io/cn/cloud-recording/restfulapi/#/)

- 如果一个频道超过15秒内没有主持人以及观众，那么频道会关闭，下面的接口都会提示找不到该频道
- 云端录制的原理就是添加了一个观众去听
- 目前云端录制无论是自建服务器还是使用官方接口都只支持生成`m3u8`格式的音视频文件，如果需要其他格式需要自己去转换
- [云端录制常见错误码](https://docs.agora.io/cn/cloud-recording/common_errors?platform=RESTful)

#### 获取云端录制资源resource ID

- 后续对云端录制的几个接口都需要该`resource ID`，并且每次调用都能生成一个新的
- ``resource ID`的时效是5分钟，必须5分钟内用它去开始云端录制，但是后续仍然可以用它来`query/stop`

```shell
# 接口地址: /v1/apps/{appid}/cloud_recording/acquire
# 接口参数:
{
	"cname": "频道名称",
	"uid": "1234567890", 	# 可以固定一个与数据库中其他用户uid不会重复的id
	"clientRequest": {
		"resourceExpiredHour": 24
	}
}
```

#### 开始云端录制

- 一般紧接着获取resource ID后进行
  - 需要注意的是，多次对同一个频道调用`start`接口，会开启多个录制，会生成多份录制文件

```shell
# 接口地址: /v1/apps/{appid}/cloud_recording/resourceid/{resourceid}/mode/{mode}/start
# 其中mode=mix的是默认模式，表示将频道哪所有UID的音视频混合录制为一个音视频文件，可选individual/web
# 接口参数:
{
	"cname": "频道名",
	"uid": "录制的用户ID", # 需要和获取resource ID的一致
	"clientRequest": {
		"token": `${this.buildTokenWithUid(uid)}`, # 调用buildTokenWithUid方法生成的token
		"recordingConfig": {
			"channelType": 1,
			"streamTypes": 0,
			"maxIdleTime": 3000,	# 这个一定要注意设置大一点，否则可能出现超过一定时间不出声频道自动销毁的情况
			"videoStreamType": 0,
			"unSubscribeAudioUids": [
				"1234567890"	# 不录制指定uid的音视频，可以直接设置为录制用的那个UID	
			]
		},
		"recordingFileConfig": {
			"avFileType": [
				"hls"
			]
		},
		"storageConfig": {
			"vendor": 1,
			"accessKey": config.aws3.accessKeyId,
			"region": config.aws3.regionNum,
			"bucket": config.aws3.bucket,
			"secretKey": config.aws3.secretAccessKey,
			"fileNamePrefix": [	# 需要注意的是文件夹名称在agora这边不允许下划线
				'directoryPrefix',
				audioPost.id
			]
		}
	}
}
```

#### 查询云端录制状态

- 可以通过该方法获取云端录制生成的m3u8文件名称(如果不使用agora提供的回调服务，就只能自己找个时机去获取了，否则频道销毁后就获取不到该文件了，并且频道在刚调用完start的时候也是获取不到该文件的)

```shell
# 接口地址：/v1/apps/{appid}/cloud_recording/resourceid/{resourceid}/sid/{sid}/mode/{mode}/query
```

#### 停止云端录制

- 当所有用户都离开频道后，云端录制也会自动暂停的
- 云端录制停止不代表频道被销毁

```shell
# 接口地址: /v1/apps/{appid}/cloud_recording/resourceid/{resourceid}/sid/{sid}/mode/{mode}/stop
# 接口参数:
{
	"cname": "频道名称",
  "uid": "录制用的用户ID",
	"clientRequest": {}
}
```

### [回调服务/消息通知服务](https://docs-preprod.agora.io/cn/Agora%20Platform/ncs?platform=Android)

- 要开通回调服务国内必须提交工单，国外必须通过email联系
- 回调服务需要提供接口给他们，否则他们总说你的接口有问题，我都还没接入我怎么提供接口呢，关键改接口地址又得发邮件，所以这里最好先写好一个返回200的接口，并且把body都打印到日志里面去
- 回调服务需要问你是否需要`retry`，之前我觉得加上会比较好，后来看觉得还是取消好一点，他们的回调没发现漏发的，只有不及时的，反正时间顺序完全没有

#### [实时通信回调服务](https://docs-preview.agoralab.co/cn/Agora%20Platform/rtc_eventtype)

#### [云端录制 RESTful API 回调服务](https://docs.agora.io/cn/cloud-recording/cloud_recording_callback_rest?platform=RESTful)

| EventType | Description                                                  | comment                                                      |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 4         | The M3U8 playlist file is generated. M3U8文件生成            | 可以在这时候获取到`m3u8`文件的文件名                         |
| 11        | The cloud recording service has ended its tasks and exited. 云端录制退出 | 退出的时候可以尝试从`m3u8`文件中解析出云端录制的总时长       |
| 33        | 录制文件上传到第三方云存储的进度                             | 个人感觉没多大用，每个分片都会进行上传并回调，再加上retry，这个事件相当多 |

