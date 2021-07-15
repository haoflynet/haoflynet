---
title: "Google Cloud 相关服务"
date: 2021-08-01 11:52:39
categories: frontend
---

## Cloud Function

- 最大超时时间只能设置为540s=9min，实在不行可以用`Cloud Tasks` 队列，或者在时间快完的时候直接再调用一下url参数组织一下

## Cloud Tasks

- 任务队列，[官方文档](https://cloud.google.com/tasks/docs/creating-http-target-tasks?hl=zh-cn)用起来非常简单实用，可用于多消费者，或者减少第三方接口的并发速率限制
- 速率控制(队列使用令牌桶来控制任务执行速率，每个命令的队列都有一个用于存储令牌的存储分区，应用没执行一个任务，就会从桶中移除一个令牌，会按照max_dispatches_per_second速率不断向令牌桶中补充填充新令牌)
  - Max dispatches: 每秒钟任务分配的速率，每秒将任务分配给多少个worker
  - Max concurrent dispatches: 并发执行的数量，同时运行的任务的最大数量
- 重试控制：
  - MAX ATTEMPTS：任务可以尝试的最大次数，包括第一次尝试
  - MAX INTERVAL：重试尝试之间的最短等待时间

## [firebase/firestore](https://haofly.net/firebase)

## Logging

- 谷歌的日志查询起来非常方便，就像是查询json字段一样

## Map地图服务

- vue推荐使用[vue-google-autocomplete](https://github.com/olefirenko/vue-google-autocomplete)做地址的自动完成，只需要按照其`README`开通对应的API，然后在`Credentials`拿到`API KEY`即可，它主要是用的是`AutocompletionService`，该组件支持这样几个自定义搜索参数:
  - types: 默认值为`address`还支持`geocode/establishment/address/(regions)/(cities)`
  - country: 限制搜索国家
  - getAddressData会返回addressData(administrative_area_level_1, country, latitude, locality, longitude), placeResultData(address_components(包含行政区层级), place_id), id(这只是map组件的id)
  - 可以通过inputChange事件和update方法来修改自动填充的内容

## GTM(Google Tag Manager)

- 有了它就不用每次添加一个新的服务(tag)都去修改代码了，因此服务添加多了也不会影响网站的首次加载速度
- 在新建了账号后，就可以选择`Tags->New`，例如可以添加`Google Analytics 4`

