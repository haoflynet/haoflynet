---
title: "Laravel使用IoC模式(DI、依赖注入)"
date: 2015-05-17 16:19:06
categories: 编程之路
---
参考文章：<https://phphub.org/topics/607> (以下内容基本上都摘自该文章)

IoC这个主题我已经收藏了很久了，直到今天才有空深入地理解了一遍Laravel的IoC模式。

前几天在使用LeanCloud的Python SDK，我就在想，每次连接LeanCloud的存储服务都需要先创建一个连接，如果要执行其它的操作，那又得新建那
个连接了。IoC就是为了解决每次都重复连接的一种编码模式，通过依赖注入减少耦合。

上面引用的参考文章里已经注明了为什么我们在这种情况下一定要使用依赖注入，这里我就只记录下到底该如何使用该模式。

Laravel的依赖注入是使用的“容器”这个概念，是一种全局注册表，使用容器的依赖注入作为一种桥梁来解决依赖可以使我们的代码耦合度耕地，很好的降低了组件的复
杂性。示例代码如下：



    <?php




    class SomeComponent\{      # 组件
        protected $_di;      # 一个私有变量





    public function __construct($di)\{
        $this-&gt;_di = $di;
    \}

    public function someDbTask()\{
        // 通过get获取connection service总是返回一个新的连接
        $connection = $this-&gt;_di-&gt;get('db');
    \}

    public function someOtherDbTask()\{
        // 和上面不同，这里获取的是共享的连接
        $connection = $this-&gt;_di-&gt;getShared('db');

        //This method also requires a input filtering service
        $filter = $this-&gt;_db-&gt;get('filter');
    \}


\}

$di = new Phalcon\\DI(); // 创建一个容器

// 在容器中注册一个名为'db'的服务，用于连接数据库，并返回该连接 $di->set('db', function()\{ return new
Connection(array( "host" => "localhost", "username" => "root", "password" =>
"secret", "dbname" => "invo" )); \});

// 在容器中注册一个名为'filter'的服务 $di->set('filter', function()\{ return new Filter();
\});

// 在容器中注册一个名为'session'的服务 $di->set('session', function()\{ return new
Session(); \});

// 将容器作为一个参数传递到构造函数中去 $some = new SomeComponent($di);

$some->someTask();

现在，该组件只有访问某种service的时候才需要它，如果它不需要，它甚至不会被初始化，以节约资源。Phalcon\\DI是一个实现了服务的依赖注入功能的组件
，它本身就是一个容器。由于Phalcon高度解耦，Phalcon\\DI是框架用来集成其他组件的必不可少的部分，开发人员也可以使用这个组件依赖注入和管理应用程
序中不同类文件的实例。

在容器中注册服务，框架本身或开发人员都可以注册服务。当一个组件A要求调用组件B(或它的类的一个实例)，可以从容器中请求调用组件B，而不是创建组件B的一个实例
。

### 注入方法

服务可以通过以下几种方式注入到容器：



    <?php




    // 首先要创建一个依赖注入容器
    $di = new Phalcon\\DI();




    // 通过类名注入
    $di->set("request", 'Phalcon\\Http\\Request');




    // 通过匿名函数注入Using an anonymous function, the instance will lazy loaded
    $di->set("request", function()\{
        return new Phalcon\\Http\\Request();
    \});




    // 直接用一个实例来注入
    $di->set("request", new Phalcon\\Http\\Request());




    // 通过数组来注入
    $di->set("request", array(
        "className" => 'Phalcon\\Http\\Request',
        "parameters" => array(
                parameter" => array(
                    "host" => "localhost",
                )
            )
        )
    ));

在容器中，通过数组，字符串等方式存储的服务都将被延迟加载，即只有在请求对象的时候才被初始化。

从容器获得服务：



    <?php $request = $di->get("request");
    //或者使用魔术方法
    $request = $di->getRequest();

其它相关文章：

# [PHP程序员如何理解IoC/DI](http://segmentfault.com/a/1190000002411255 "Link:
http://segmentfault.com/a/1190000002411255" )
