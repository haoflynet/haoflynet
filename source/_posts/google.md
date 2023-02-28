---
title: "Google Cloud 相关服务"
date: 2021-07-23 07:52:39
updated: 2023-02-21 18:07:00
categories: frontend
---

- [Install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk): google cloud cli工具安装方式

## Cloud Function

- [不同配置的价格表](https://cloud.google.com/functions/pricing?hl=zh-cn)
- 最大超时时间只能设置为540s=9min，实在不行可以用`Cloud Tasks` 队列，或者在时间快完的时候直接再调用一下url参数组织一下
- [其他限制](https://cloud.google.com/functions/quotas): 常用的会有未压缩HTTP请求或响应的大小为10 MB
- 为了减少函数的执行时间，我们需要尽量提升程序的启动时间，默认都是冷启动的，但是如果间隔时间很小，谷歌可能并没有销毁，这个间隔是谷歌自己控制的，并且是不一定的，所以你会发现如果启动时间长的函数，有时候处理得快有时候处理得慢。当然，谷歌也提供付费服务保证至少有几个实例在运行，如果不想用，还可以自己弄个定时任务去定时请求一次，不过当然那也算运行时间呀。

```javascript
req.headers['x-forwarded-for'] || req.connection.remoteAddress || req.headers['fastly-client-ip']	// 可以通过这种方式获取客户端IP地址
```

## Cloud Scheduler

- 定时任务
- 配置说明：
  - Max retry attempts: 失败重试的次数
  - Max retry duration: 失败后的最长重试时间，看次数和时间哪个先到就停止
  - Min/Max backoff duration: 两次重复间隔最短/最长时间
  - Attempt deadline config：验证一个请求是否成功的最长等待时间，如果超过这个时间会显示失败，并得到一个UNKNOWN的错误
- 居然遇到了trigger两次的bug，就一个任务在一个时间点居然trigger了两次，别人也遇到过https://stackoverflow.com/questions/71594174/cloud-scheduler-invokes-cloud-function-more-than-once-during-schedule，可能不能用http来trigger cloud function了

## Cloud Tasks

- 任务队列，[官方文档](https://cloud.google.com/tasks/docs/creating-http-target-tasks?hl=zh-cn)用起来非常简单实用，可用于多消费者，或者减少第三方接口的并发速率限制

- 速率控制(队列使用令牌桶来控制任务执行速率，每个命令的队列都有一个用于存储令牌的存储分区，应用每执行一个任务，就会从桶中移除一个令牌，会按照max_dispatches_per_second速率不断向令牌桶中补充填充新令牌)
  - Max dispatches: 每秒钟任务分配的速率，每秒将任务分配给多少个worker
  - Max concurrent dispatches: 并发执行的数量，同时运行的任务的最大数量
  
- 重试控制：
  - MAX ATTEMPTS：任务可以尝试的最大次数，包括第一次尝试，-1表示不限制?，但是不能设置为0，所以如果说只想执行一次，应该是设置为1
  - MAX INTERVAL：重试尝试之间的最短等待时间
  
- 一些限制

  - 任务大小上限：100KB(超过会报错task size too large)
  - 队列执行速率：每个队列每秒500次任务调度
  - 人物的最大倒计时/ETA：30天
  - 可以批量添加的最大任务数：100个
  - 在一项事务中可以添加的最大任务数：5个
  - 默认的最大任务队列数：100个

- 官方文档给的例子是发送一个字符串，但是如果要发送json格式的payload，可以这样做：

  ```javascript
  const task = {
    httpRequest: {
      httpMethod: 'POST',
      url: `${config.baseUrl}?${searchParams.toString()}`,
      body: Buffer.from(JSON.stringify(params)).toString('base64'),
      headers: {
        'Content-Type': 'application/json',
      },
    },
  };
  
  const request = { parent: this.queue, task };
  await client.createTask(request);
  
  // 在接口这边不用做其他处理，就像平常的json请求那样即可
  app.post('/endpoint', (req, res) => {
    const {foo} = req.body;
    console.log(foo); // "bar"
    res.send('ok');
  });
  ```

- **The queue cannot be created because a queue with this name existed too recently**: 队列删除7天后才能创建同名的队列

<!--more-->

## [firebase/firestore](https://haofly.net/firebase)

## Google Drive

- 无论是用`google-drive-ocamlfuse`还是`rclone`的方式挂载都需要在web端授权，不如就用[rclone](https://haofly.net/rclone)，主要是mac上面好安装点而且功能更多

## Google Fonts

- 谷歌字体服务

```shell
# 支持多种字体可以加多个family参数
https://fonts.googleapis.com/css2?family=Crimson+Pro&family=Literata

# 支持设置字体的weight
https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@200..900
https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@1,200..900
https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,200..900;1,700
```

## Google Tag Manager(GTM)

- 谷歌代码管理系统
- 如果要在前端代码里面集成多种跟踪或者网站分析代码，以前的话就得添加多个代码片段，有了google tag manager，只需要添加一次，在google后台配置即可添加多个

## Logging

- 谷歌的日志查询起来非常方便，就像是查询json字段一样

- 日志最大为256kb，其实非常小，而且很难debug，出现的时候程序会直接crash。如果经常出现，可以尝试用[object-sizeof](https://www.npmjs.com/package/object-sizeof)来查看一下内存

- 常用的查询语法

  ```shell
  jsonPayload.message =~ "regular expression pattern"	# 模糊查询
  jsonPayload.message !~ "regular expression pattern"	# 模糊查询，不等于
  
  (jsonPayload.message = "abc" OR jsonPayload.message = "dd")	# 或者or查询
  
  m = NULL_VALUE	# 某个字段是否为null需要用这个特殊值，而不能直接用null
  
  # 查询数组内的字段，例如m=[{abc: 123}]，可以直接当对象来查
  m.abc=123
  # 普通的数组，可以直接查询，例如m=["abc" , "def"]
  m = "abc"
  
  # 如果某个字段可能存在也可能不存在，可以这样查询
  operation.id:* # 如果该字段存在
  NOT operation.id:* # 如果该字段不存在
  ```

## Map地图服务

- vue推荐使用[vue-google-autocomplete](https://github.com/olefirenko/vue-google-autocomplete)做地址的自动完成，只需要按照其`README`开通对应的API，然后在`Credentials`拿到`API KEY`即可，它主要是用的是`AutocompletionService`，该组件支持这样几个自定义搜索参数:
  - types: 默认值为`address`还支持`geocode/establishment/address/(regions)/(cities)`
  - country: 限制搜索国家
  - getAddressData会返回addressData(administrative_area_level_1, country, latitude, locality, longitude), placeResultData(address_components(包含行政区层级), place_id), id(这只是map组件的id)
  - 可以通过inputChange事件和update方法来修改自动填充的内容

## GTM(Google Tag Manager)

- 有了它就不用每次添加一个新的服务(tag)都去修改代码了，因此服务添加多了也不会影响网站的首次加载速度
- 在新建了账号后，就可以选择`Tags->New`，例如可以添加`Google Analytics 4`

## Colab

- Variables不是环境变量，是tensorflow的变量，可以参考[这里](https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/guide/variable.ipynb)
- Colab可以[连接不同的文件服务](https://neptune.ai/blog/google-colab-dealing-with-files): Github, Google Drive, Local File System, Google Sheets, Google Cloud Storage(GCS), AWS S3, Kaggle datasets, MySQL
  - Google Drive: 注意无法直接链接别人分享给你的文件夹，必须将分享的文件夹添加快捷方式(Add shortcut to drive)到你自己的文件夹才行


## TroubleShooting

- **Error: Cannot find module './middleware/cloudevent_to_background_event'**: 给我的感觉就是新版的sdk发布后老的只要是重新安装的就不能用，必须升级到最新版才可以
- **Google Cloud Function出现错误Error: memory limit exceeded或者503 HTTP UNAVAILABLE**: 可能真的是内存超了，默认内存是128MB
