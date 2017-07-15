---
title: "设计模式-php实现"
date: 2016-08-30 11:40:30
updated: 2017-07-14 14:27:00
categories: code
---
即使我写了这样的文章，我依然坚信设计模式只是某些垃圾语言用来规避其语言本身弊端的规范而已，不然，就只能写出糟糕的代码了。

# 创建型

### Factory Method(工厂方法模式/工厂模式)

工厂模式是一种类，提供了创建对象的某些方法，可以直接使用工厂类创建对象，而不是直接使用new。

优点：如果要改变所创建对象的类型，只需要修改该工厂即可。比如有个类需要读取用户数据来创建，原本是读取的数据库，现在要从文本读取，就得把那个类及其所有依赖都更改一遍。

php示例

```php
<?php
interface IPost{
  function getName();
}

class Post implements IPost{
  public function __construct($id){}
  
  public static function Load($id){
    return new Post($id);
  }
  
  public static function Create(){
    return new Post(null);
  }
  
  public function getName(){
    return "haofly";
  }
}

$post = Post::Load(1);
echo $post->getName();
?>
```

### AbstractFactory(抽象工厂模式)

抽象工厂模式提供了一种方式，可以将一组具有同一主题的单独的工厂封装起来。客户端程序不需要知道（或关心）它从这些内部的工厂方法中获得对象的具体类型，因为客户端程序仅使用这些对象的通用接口。抽象工厂模式将一组对象的实现细节与他们的一般使用分离开来。

php示例，代码来自[维基百科](https://zh.wikipedia.org/wiki/%E6%8A%BD%E8%B1%A1%E5%B7%A5%E5%8E%82#PHP)

```php
<?php
abstract class AbstractFactory {
	abstract public function CreateButton();
	abstract public function CreateBorder();
}

class MacFactory extends AbstractFactory{
	public function CreateButton()
	{
		
		return new MacButton();
	}
	public function CreateBorder()
	{
		return new MacBorder();
	}
}
class WinFactory extends AbstractFactory{
	public function CreateButton()
	{
		return new WinButton();
	}
	public function CreateBorder()
	{
		return new WinBorder();
	}
}
class Button{}
class Border{}

class MacButton extends Button{
	function __construct()
	{
		echo 'MacButton is created' . "\n";
	}
}
class MacBorder extends Border{
	function __construct()
	{
		echo 'MacBorder is created' . "\n";
	}
}


class WinButton extends Button{
	function __construct()
	{
		echo 'WinButton is created' . "\n";
	}
}
class WinBorder extends Border{
	function __construct()
	{
		echo 'WinBorder is created' . "\n";
	}
}
?>
# 客户端使用
<?
$type = 'Mac'; //value by user.
if(!in_array($type, array('Win','Mac')))
    die('Type Error');
$factoryClass = $type.'Factory';
$factory=new $factoryClass;
$factory->CreateButton();
$factory->CreateBorder();
?>
```

### Prototype(原型模式)

通过复制一个已经存在的实例来返回新的实例，而不是新建实例。

优点: 多用于创建复杂的或者耗时的实例，这种情况，复制一个已经存在的实例使程序运行更高效，活着创建值相等，只是命名不一样的同类数据。

### Singleton(单例模式)

php示例，代码来自[IBM](https://www.ibm.com/developerworks/cn/opensource/os-php-designptrns/)

```php
<?php
require_once("DB.php");

class DatabaseConnectiono{
  private $_handle = null;
  
  private function __construct(){
    $dsn = 'mysql://root:password@localhost/photos';
    $this->_handle = & DB::Connect($dsn, array());
  }
  
  public static function get(){
    static $db = null;
    if($db == null)
      $db = new DatabaseConnectioni();
    return $db;
  }
  
  public function handle(){
    return $this->_handle;
  }
}

print("Handle=".DatabaseConnection::get()->handle()."\n");
print("Handle=".DatabaseConnection::get()->handle()."\n");
```

## 结构型

### Adapter Class/Object(适配器/转换器)

介绍: 把一个类的接口变换成客户端所期待的另一种接口，Adapter模式使原本因接口不匹配或不兼容而无法在一起工作的两个类能够在一起工作。外部请求方式一样，内部实现方式不一样。

应用场景: 

1. 想使用一个已经存在的类，但是它的接口并不完全符合需求
2. 适用于第三方库的API会发生改变而选择不直接把第三方API给用户使用的情况下，在前面封装一层。

php实例，代码来自[真实的归宿](http://blog.csdn.net/hguisu/article/details/7527842)

```php
<?php  
/** 
 * 目标角色
 */  
interface Target {  
    /** 
     * 源类的方法：这个方法将来有可能继续改进 
     */  
    public function hello();  
   
    /** 
     * 目标点 
     */  
    public function world();  
}  
   
/** 
 * 源角色：修改后的方法
 */  
class Adapter {  
    /** 
     * 源类含有的方法 
     */  
    public function world() {  
        echo ' world <br />';  
    }  
   
    /** 
     * 将hello方法改为了greet方法
     */  
    public function greet() {  
        echo ' Greet ';  
    }  
}  
   
/** 
 * 类适配器角色 
 */  
class Adapter  implements Target {  
    private $_adaptee;  

    public function __construct(Adaptee $adaptee) {  
        $this->_adaptee = $adaptee;  
    }  
   
    /** 
     * 源类中没有hello方法，在此补充 
     */  
    public function hello() {  
       $this->_adaptee->greet();  
    }  
}  
/** 
 * 客户端程序 
 */  
class Client {  
    public static function main() {  
        $adaptee = new Adaptee();  
        $adapter = new Adapter($adaptee);  
        $adapter->hello();  	// 无论内部怎么变，外部都用hello来引用
        $adapter->world();  
    }  
}  
  
Client::main();  
?>  
```



### Bridge(桥接模式)

把事务对象和其具体行为、具体特征分离开来，使它们可以各自独立的变化。

python实例，代码来自[维基百科](https://zh.wikipedia.org/wiki/%E6%A9%8B%E6%8E%A5%E6%A8%A1%E5%BC%8F#Python)

```python
"""圆形、三角形归于抽象的形状，而画圆、画三角形归于抽象的画图"""

# Implementor
class DrawingAPI:
	def drawCircle(x, y, radius):
		pass

# ConcreteImplementor 1/2
class DrawingAPI1(DrawingAPI):
	def drawCircle(self, x, y, radius):
		print "API1.circle at %f:%f radius %f" % (x, y, radius)

# ConcreteImplementor 2/2
class DrawingAPI2(DrawingAPI):
	def drawCircle(self, x, y, radius):
		print "API2.circle at %f:%f radius %f" % (x, y, radius)

# Abstraction
class Shape:
	# low-level
	def draw(self):
		pass

	# high-level
	def resizeByPercentage(self, pct):
		pass

# Refined Abstraction
class CircleShape(Shape):
	def __init__(self, x, y, radius, drawingAPI):
		self.__x = x
		self.__y = y
		self.__radius = radius
		self.__drawingAPI = drawingAPI

	# low-level i.e. Implementation specific
	def draw(self):
		self.__drawingAPI.drawCircle(self.__x, self.__y, self.__radius)

	# high-level i.e. Abstraction specific
	def resizeByPercentage(self, pct):
		self.__radius *= pct

def main():
	shapes = [
		CircleShape(1, 2, 3, DrawingAPI1()),
		CircleShape(5, 7, 11, DrawingAPI2())
	]

	for shape in shapes:
		shape.resizeByPercentage(2.5)
		shape.draw()

if __name__ == "__main__":
	main()
```



### Composite(组合模式)

### Decorator(装饰模式)

### Facade(外观)

### Flywight(享元)

### Proxy(代理)

## 行为型

### Interpreter(解释器)

### Template Method(模板方法)

### Observer(观察者模式)

优点: 被观察对象不用具体了解观察者具体实现，而是由观察者去实现。被观察者忽略了依赖它的对象，它要关注在事件发生时触发该事件并发送消息给观察者即可。这个和依赖注入有点相近的地方。

php示例，代码来自[IBM](https://www.ibm.com/developerworks/cn/opensource/os-php-designptrns/)

```php
<?php
/**
 * 测试代码创建 UserList，并将 UserListLogger 观察者添加到其中。然后添加一个消费者，并将这一更改通知 UserListLogger
 */
  
# 定义要通过怎样的方法才能成为观察者
interface IObserver{
  function onChanged($sender, $args);
}
# 定义可以被观察的对象
interface IObservable{
  function addObserver($observer);
}
# 实现IOBbservable，以便将本身注册为可观察
class UserList implements IObservable{
  private $_observers = array();
  
  public function addCustomer($name){
    foreach($this->_observers as $obs){
      $obs->onChanged($this, $name);	# 通知观察者
    }
  }
  
  public function addObserver($observer){
    $this->_observers[] = $observer;
  }
}

class UserListLogger implements IOBserver{
  public function onChanged($sender, $args){
    echo("'$args' added to user list\n");
  }
}

$ul = new UserList();
$ul->addObserver(new UserListLogger());
$ul->addCustomer("Jack");
```

### Command(命令)

### Chain of Respopnsibility(责任链)

包含了一些命令对象和一系列的处理对象，每一个处理对象决定它能处理哪些命令对象，它也知道如何将它不能处理的命令对象传递给该链中的下一个处理对象。

php示例，代码来自[维基百科](https://zh.wikipedia.org/wiki/%E8%B4%A3%E4%BB%BB%E9%93%BE%E6%A8%A1%E5%BC%8F#PHP)

```php
<?php
abstract class Logger {
	const ERR = 3;
	const NOTICE = 5;
	const DEBUG = 7;

	protected $mask;
	protected $next; // The next element in the chain of responsibility

	public function setNext(Logger $l) {
		$this->next = $l;
		return $this;
	}

	abstract public function message($msg, $priority);
}

class DebugLogger extends Logger {
	public function __construct($mask) {
		$this->mask = $mask;
	}

	public function message($msg, $priority) {
		if ($priority <= $this->mask) {
			echo "Writing to debug output: {$msg}\n";
		}

		if (false == is_null($this->next)) {
			$this->next->message($msg, $priority);
		}
	}
}

class EmailLogger extends Logger {
	public function __construct($mask) {
		$this->mask = $mask;
	}

	public function message($msg, $priority) {
		if ($priority <= $this->mask) {
			echo "Sending via email: {$msg}\n";
		}

		if (false == is_null($this->next)) {
			$this->next->message($msg, $priority);
		}
	}
}

class StderrLogger extends Logger {
	public function __construct($mask) {
		$this->mask = $mask;
	}

	public function message($msg, $priority) {
		if ($priority <= $this->mask) {
			echo "Writing to stderr: {$msg}\n";
		}

		if (false == is_null($this->next)) {
			$this->next->message($msg, $priority);
		}
	}
}

class ChainOfResponsibilityExample {
	public function __construct() {
		// build the chain of responsibility
		$l = new DebugLogger(Logger::DEBUG);
		$e = new EmailLogger(Logger::NOTICE);
		$s = new StderrLogger(Logger::ERR);
		
		$e->setNext($s);
		$l->setNext($e);

		$l->message("Entering function y.",		Logger::DEBUG);		// handled by DebugLogger
		$l->message("Step1 completed.",			Logger::NOTICE);	// handled by DebugLogger and EmailLogger
		$l->message("An error has occurred.",	Logger::ERR);		// handled by all three Loggers
	}
}

new ChainOfResponsibilityExample();
?>
```

### Iterator(迭代器)
### Mediator(中介者)
### Memento(备忘录)
### State(状态)
### Strategy(策略模式)

指对象有某种行为，但是在不同的场景中，该行为有不同的实现算法。

抽象工厂与策略模式不同的地方在于，工厂是创建型模式，关注的是对象的创建，而策略是行为型模式，关注的是对行为的封装，对于工厂来说无论返回的对象内部是怎样的，只要是我想要的对象就行，而对于策略模式来说返回的对象即使不同也会有相同的方法/行为。

php示例，代码来自[维基百科](https://zh.wikipedia.org/wiki/%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F#PHP)

```php
<?php
class StrategyExample {
    public function __construct() {
        $context = new Context(new ConcreteStrategyA());
        $context->execute();

        $context = new Context(new ConcreteStrategyB());
        $context->execute();

        $context = new Context(new ConcreteStrategyC());
        $context->execute();
    }
}

interface IStrategy {
    public function execute();
}

class ConcreteStrategyA implements IStrategy {
    public function execute() {
        echo "Called ConcreteStrategyA execute method\n";
    }
}

class ConcreteStrategyB implements IStrategy {
    public function execute() {
        echo "Called ConcreteStrategyB execute method\n";
    }
}

class ConcreteStrategyC implements IStrategy {
    public function execute() {
        echo "Called ConcreteStrategyC execute method\n";
    }
}

class Context {
    var $strategy;

    public function __construct(IStrategy $strategy) {
        $this->strategy = $strategy;
    }

    public function execute() {
        $this->strategy->execute();
    }
}

new StrategyExample;
?>
```

### Visitor(放问者)



## TroubleShooting

- **工厂模式和策略模式的区别**
  如大多数网上的解释一样，工厂模式更注重对象的创建，策略模式更注重行为的不同。根据我的理解工厂模式更适用于创建不同的对象，这些对象拥有不同的方法。而策略模式则更多是针对有相同方法的对象。例如网上的文章经常举的例子一样，数据库的操作，其实每个数据库的操作都不一样，所以这里更适用于工厂模式。但是如果有后端一样的场景，那么策略模式就更方便了。例如

  ```php
  # 工厂模式
  DBFactory::create(Redis::class)->record()->add();

  # 策略模式(不同的公有云相同的create方法)
  abstract class CloudContext
  {
    protected $cloud;
    public function __construct(Cloud $cloud) {
      $this->cloud = $cloud;
    }
  }
  class HostContext extends CLoudContext
  {
    public function create(
    	$this->cloud->create();
    );
  }
  $host new HostContext(CloudFactory::create(AliyunCloud::class));
  $host->create();
  ```

  ​

- ​