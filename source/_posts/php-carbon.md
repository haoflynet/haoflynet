---
title: "PHP 使用Carbon扩展进行时间处理"
date: 2019-05-31 18:32:00
updated: 2021-03-05 17:47:00
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
Carbon::createFromTimeStamp(1545800000);

# 获取时间字段
$time->timestamp;	// 获取时间戳
$time->year;
$time->month;
$time->format('F');	// 获取月份全称，例如February
$time->day;
$time->hour;
$time->minute;
$time->second;
$time->micro;
$time->dayOfWeek;	// 获取当前时间是一周的第几天
$time->dayOfYear;	// 获取当前时间是一年的第几天
$time->weekOfMonth; // 获取当前时间是当月的第几周
$time->weekOfYear;	// 获取当前时间是当年的第几周
$time->daysInMonth;	// 获取当月有多少天
$time->startOfDay();	 // 今天开始时间
$time->endOfDay();	// 今天结束时间
$time->startOfWeek();	// 这周开始时间
$time->endOfWeek();	// 这周结束时间
$time->startOfMonth();	// 这个月开始时间
$time->endOfMonth();	// 这个月结束时间

# 时间计算
$time->addDays(3);
$time->addWeeks(3);
$time->addHours(24);
$time->subHours(20);
$time->modify('-2 days');
$time->isWeekday();	// 是否是工作日
$time->isWeekend(); // 是否是周末
$time->isYesterday();	// 是否是昨天
$time->isTomorrow();	// 是否是明天

# 时间比较
$first->eq($second);
$first->ne($second);
$first->gt($second);
$first->gte($second);
$first->lt($second);
$first->lte($second);

# 获取指定格式输出
$time->toDateTimeString();
$time->subDays(5)->diffForHumans();	// 5天前
$time->format('m/y') // 指定输出格式: 12/2020
```

## Troubleshooting

- **The timezone could not be found in the database**: 通常是createFromFormat第一个参数格式没有设置