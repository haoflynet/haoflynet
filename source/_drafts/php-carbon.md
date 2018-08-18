---
title: "PHP 使用Carbon扩展进行时间处理"
date: 2018-08-03 16:32:00
categories: php
---

PHP上最好的时间处理工具。

```php
# 以下都是获得一个时间对象
Carbon::now();		// 获取当前时间，2018-01-01 11:11:11
Carbon::today();	// 获取今天的开始时间，2018-01-01 00:00:00
Carbon::tomorrow(); // 获取明天的开始时间，2018-01-02 00:00:00
Carbon::yesterday();// 获取昨天的开始时间，2017-12-31 00:00:00

# 解析时间，这个功能可以说是非常强大了
Carbon::parse('2018-01-01');
Carbon::parse('2018-01-01 12:00:00');
Carbon::parse('today');
Carbon::parse('2 days ago');
Carbon::parse('+3 weeks');
Carbon:::parse('last friday');

# 时间计算
Carbon::now()->addDays(3);
Carbon::now()->subHours(20);
Carbon::now()->modify('-2 days');

# 获取指定格式输出
Carbon::now()->toDateTimeString();
Carbon::now()->subDays(5)->diffForHumans();	// 5天前
```