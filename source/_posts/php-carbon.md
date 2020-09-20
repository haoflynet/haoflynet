---
title: "PHP 使用Carbon扩展进行时间处理"
date: 2019-05-31 18:32:00
updated: 2020-09-19 09:21:00
categories: php
---

PHP上最好的时间处理工具。

```php
# 以下都是获得一个时间对象
Carbon::now();		// 获取当前时间，2018-01-01 11:11:11
Carbon::today();	// 获取今天的开始时间，2018-01-01 00:00:00
Carbon::tomorrow(); // 获取明天的开始时间，2018-01-02 00:00:00
Carbon::yesterday();// 获取昨天的开始时间，2017-12-31 00:00:00

# 解析时间，这个功能可以说是非常强大了，需要特别注意的是如果parse的字符串内部有带时区，那么解析后的对象也是自带时区的，可能跟当前时区是不一样的
Carbon::parse('2018-01-01');
Carbon::parse('2018-01-01 12:00:00');
Carbon::parse('today');
Carbon::parse('2 days ago');
Carbon::parse('+3 weeks');
Carbon::parse('last friday');
Carbon::parse('Fri May 31 2019 06:50:14 GMT+0000 (UTC)')->toDateTimeString();	// 这个会得到2019-05-31 06:50:14，而不是东8区的时间
Carbon::createFromFormat('Y-m-d H', '1975-05-21 22')->toDateTimeString(); // 1975-05-21 22:00:00


# 时间计算
Carbon::now()->addDays(3);
Carbon::now()->subHours(20);
Carbon::now()->modify('-2 days');

# 获取指定格式输出
Carbon::now()->toDateTimeString();
Carbon::now()->subDays(5)->diffForHumans();	// 5天前
Carbon::now()->dayOfWeek	// 获取今天是星期几，直接返回一个数字
Carbon::now()->format('m/y') // 指定输出格式: 12/2020
```