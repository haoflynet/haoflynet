---
title: "ThinkPHP 手册"
date: 2016-10-28 00:08:39
updated: 2019-04-23 10:33:00
categories: php
---
垃圾框架，用了`Laravel`过后感觉其他的PHP框架都是垃圾。但是由于生活所迫，不得不研究一下ThinkPHP框架了，哎。

## 配置

数据库配置放在`database.php`

## 帮助函数

```php
$this->redirect('')	# 重定向
Log::record('');	# 记录日志信息到内存
Log::save('');	# 手动将保存在内存中的日志信息写入日志
Log::write('');	# 实时写入一条日志信息，不受配置的允许日志级别影响，可以实时写入任意级别的日志信息
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
  
# 创建数据
$model->create(['name' => 'test']);
  
# 更新数据
$model->where('id=5')->save(['name' => 'test']);	// 根据条件更新记录
$model->name = 'test' && $model->where('id=5')->save();	// 使用对象的方式来操作

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

