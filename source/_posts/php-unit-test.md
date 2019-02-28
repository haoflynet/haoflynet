---
title: "PHP单元测试"
date: 2016-08-08 22:02:30
updated: 2016-09-15 16:09:00
categories: php
---
PHP的单元测试工具比Python好选择，基本上就是PHPUnit了。

### 断言

```php
$this->setExpectedException(Exception class);	// 断言将会出现某个exception	
```

## Mockery mock对象

Mockery默认包含在PHPUnit中，根据我的经验，学会了mock才算真正学会了单元测试，无论是Python还是PHP都是如此。使用它也解决了我之前以为依赖注入对测试来说极大地加大了复杂度的错误思想。使用方法如下: 

```php
# 首先在一个测试类中
$this->object = Mockery:mock('class');

# 模拟方法的返回值
$this->object->shouldReceive('getValue')->andReturn('abc');	
$this->object->getValue()	# 这样就会返回abc
$this->object->shouldReceive('getAttribute')->with('value')->andReturn('def');
$this->value	# 这样会返回属性的值
```

## Xdebug的使用

既然用上了单元测试，那为何不继续深入使用，添加代码覆盖率的测试，以前我认为覆盖率只是用来给我们玩玩儿的，当我真正开始写了后才知道，真的太有用了。首先，他让我了解到一个真相，那就是我自己写的代码，很多地方，我自己都不清楚，有些异常我根本不知道在什么情况下会抛，有好多重复的地方代码根本不应该存在，有好多逻辑没考虑完整。要查看代码覆盖率还需要安装Xdebug。

安装方式：

```shell
sudo apt-get install php-pear php5-dev libcurl3-openssl-dev -y
pecl install xdebug
# 然后分别在/etc/php5/cli/php.ini和/etc/php5/apache2/php.ini 里面分别添加
zend_extension="/usr/local/php/modules/xdebug.so"
```

使用:

`phpunit testfile.php --coverage-html foldername`即可生成html文件

### TroubleShooting

- `Call to a member funciton make() on null`错误

  只需要添加父类构造方法即可:

  ```php
  function __construct(){
    parent::setUp();
  }
  ```

  ​

