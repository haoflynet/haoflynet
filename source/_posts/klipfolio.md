---
title: "Klipfolio 手册"
date: 2021-10-20 08:02:30
updated: 2022-11-15 15:47:00
categories: system
---
- 这是一个不怎么好用的工具

## Data Sources数据源

- 可以来自系统中已定义好的第三方服务，也可以直接来自于文件上传、API接口、SQL查询、FTP上传、Email附件

- 可以自定义时间去刷新(1h - 24h)，但是如果是文件上传这种是不能自动刷新的

- 可以支持参数，但是必须依赖于klip变量，例如，可以写成`https://haofly.net/{props.pageName}`，这里的`pageName`就是klip的变量，如果是第一次访问一个之前没有请求过的参数，那么可能会比较慢，后续的定时刷新也是可以起作用的，刷新的会把所有请求过的参数都请求一遍

- 由于数据源的接口请求超时时间是80s，对于数据量大的，我们可以创建email形式的数据源，定时往指定的邮箱发送附件即可

- 数据源的大小默认最大是10MB，通过付费计划可以升级到15MB，但是更大就不行了，并且modelled data也不能超过这个限制，所以要想join几张大表，可以在klip面板使用ARRAY(表1, 表2)，或者LOOKUP来查找需要的mapping数据。明明是我自己研究出来的方法，发现官网有文档的: [Managing your data source size](https://support.klipfolio.com/hc/en-us/articles/215548788-Klips-Managing-your-data-source-size)

- 如果要在`dashboard`上手动请求刷新data sources，可以直接data sources的请求刷新接口:

  ```javascript
  // 使用html component做一个刷新按钮，然后手动POST接口
  xmlHttp.open('POST', 'https://app.klipfolio.com/datasources/ajax_refresh_datasource', true);
  xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xmlHttp.send('di=&dsid=' + data source的id); // 这里加上di表示直接等待它完成，如果不加则是把它放入了刷新队列里面去
  ```

<!--more-->

## klip UI设计

### Component

#### Table

- 如果想要table中的某个列可以作为group用(多层级)，可以在table的`Drill Down`来进行`Group By`

#### HTML Component

- 只有这个component能够自己写html和js

### Functions

```shell
Array("All", @Column)	# 给数组增加一个元素

CONCAT("Test - ", @Column)	# 字符串连接/连接字符串
CONCAT(@Column, "|", "https://google.com/id/")	# 给内容加上一个链接

IF(@Country="Canada",@Company Name, BLANK())	# 没匹配上的也会有值

SELECT(@Product, $customVariable=@Name)	# 这个没匹配上的就没有值了


REPLACE(@Column, "查找值", "替换值")	# 这居然是完全匹配
SUBSTITUTE_REGEX(@Column, "查找值", "替换值")	# 这个才和js中的replace类似，且支持正则

SWITCH(data, case1, field, case2, field2, _default_, "默认值")	# 右边条件和结果两个两个成对

LOOKUP(&Column: userId, @Table1_Column1, @Table1_Column2);
LOOKUP(
	CONCAT(@Table1_Column1, @Table1_Column2),
	CONCAT(@Table2_Column1, @Table2_Column2),
	CONCAT(@Table2_Column3)
)	# 相当于连表查询了，两张表join，然后取最后那个字段的值，这里的CONCAT就相当于多个ON条件了，没匹配上的也会有值
```
