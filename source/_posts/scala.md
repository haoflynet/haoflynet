---
title: "scala 开发手册"
date: 2019-06-27 21:32:00
categories: scala
---

由于之前用`pyspark`写出来的`spark`程序在运行一段时间后会突然卡住，导致任务堆积，最终内存溢出。所以最近又决定直接用`spark`原生的`scala`语言来重写程序，`scala`大体上和`java`语言的语法是兼容的。

## 基本变量

- `val`用于声明常量，`var`用于声明变量

<!--more-->

### 列表/数组

- 不可变

```scala
val arr:Array[String] = new Array[String](3)	// 数组定义
val arr = new Array[String](3)
val arr = Array("a", "b", "c")
arr.contains("b")	// 检查列表是否存在指定的元素
```

### 元组

- 不可变对象

```scala
val t = new Tuple3(1, "2")
t._1	// 元组下标从1开始，并且是用下划线访问
t.productIterator.foreach{ i => println("value="+i)}	// 元组迭代遍历
t.toString()	// 以字符串的方式输出元组所有的元素

// 数组遍历方式
for (element <- arr) {}
for (i <- 0 until arr.length)
for (i <- 0 until (arr.length, 2))	// 遍历步长
for (i <- (0 until arr.length).reverse) // 反向遍历
```

### 字符串

```scala
val a = """定义长字符串"""
val a = "a=%s=%s".format("val1", "val2")	// 字符串格式化
```

#### 时间处理

```scala
System.currentTimeMillis()	// 获取当前时间戳(毫秒)
new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date)	// 得到格式化的当前日期时间

val now = Calendar.getInstance()
now.get(Calendar.HOUR_OF_DAY)	// 获取当前的小时数
```

### Map映射

```scala
val a = Map("a" -> 1, "b" -> 2)
```

## 条件控制

```scala
if () {} else if {} else {}
```

## 类/函数/方法/对象

```scala
def addInt( a:Int, b:Int ) : Int = {	// 需要指定参数列表及其类型，返回值及其类型
  a + b	// 可以用return，但是scala并不建议这样做，并且在很多情况这样做有问题
}

def addInt(a: Int=123) : Int = {}	// 定义默认值
def addInt(args: Int*) : Int = {} // 定义可变长度参数
def addInt(a: Int): Option[Int] = {none}	// 定义可选值，该函数可以返回Int也可以返回None

// 类没有构造函数，类本身就是一个构造函数，例如
class Post(val title: String, var content: String) {	// 参数可以是val或var
  def this(title: String) {			// 辅助构造函数以this命名，提供不同的函数签名定义不同的构造方法
    this(title, "the content")
  }
  
  def this(content: String) {}	// 可以定义多个不同签名的辅助构造函数
}
val post = new Post("the title", "the content")


// 偏函数的定义
val originalFunc = (a: int, b: String) => {}
val newFunc = (b: String) => Boolean = originalFunc(123, _)	// 下划线_是占位符，这个函数将originalFunc的参数a进行了固定，在调用时只需要调用newFunc(b)即可
```

## 网络请求

#### [scalaj库](https://github.com/scalaj/scalaj-http)

首先需要在`pom.xml`中添加如下依赖:

```xml
<dependency>
  <groupId>org.scalaj</groupId>
  <artifactId>scalaj-http_2.11</artifactId>
  <version>2.4.1</version>
</dependency>
```

这样发送http请求

```scala
val result = Http(url)
						.postData("{'a':123}")
						.header("content-type", "application/json")
						.asString
result.code	// 状态码
result.body // String格式的响应内容
```
