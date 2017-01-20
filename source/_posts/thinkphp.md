---
title: "ThinkPHP教程"
date: 2016-10-28 00:08:39
updated: 2016-11-21 14:33:00
categories: php
---
## ThinkPHP

垃圾框架，用了`Laravel`过后感觉其他的PHP框架都是垃圾。但是由于生活所迫，不得不研究一下ThinkPHP框架了，哎。

## 帮助函数

```php
$this->redirect('')	# 重定向
```

## 数据库

```php
# 定义model对象
$model = M('Product')
  
# 直接执行sql语句
$Model = new Model()
$Model->query(sql)

# 获取上一次执行的sql语句
M()->getLastSql();

# 查询数据
$model->select()	# findall功能
$model->where('name="haofly"')->find()	# 查找满足条件的第一条数据
$model->where('name="haofly"')->select()# 查找满足条件的所有数据
  
# 删除数据
$model->where('id=5')->delete()
```

## 模板引擎

```php
# volist: 用于在模版中循环输出数据集
# 首先有$this->assign('list, $list)
# 然后在模版中这样写循环
<volist name="list" id="vo">
  {$vo['name']}<br>
  {$vo['pass']}<br>
</volist>
```

