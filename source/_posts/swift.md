---
title: "Swift教程"
date: 2016-09-28 16:05:30
updated: 2016-09-28 16:44:00
categories: apple
---
## 数据类型
##### 基本变量使用

```swift
let a = 1	// 声明常量
var b = 2	// 声明变量
var c: String	// 声明变量类型

// 可选类型表示允许常量或者变量没有值，即nil，可选类型用？表明
var d: String?	// 可选变量，会自动将其值设置为nil
var e: Int? = 404 // 可选变量，这样可以把nil赋值给该变量
println(e!)	// 需要!来获取值
// 隐式解析可选类型，用!声明，表明强制要求该变量一定有值。一个隐式解析可选类型其实就是一个普通的可选类型，只是可以被当作非可选类型来使用，如果该变量没有值，那么去获取的时候就会报错
let f: String? = "test"
println(f)	// 不需要!

// 三木运算符
?:  // 和php一样吧

// 空合运算符
a ?? b	// 如果a包含一个值则是a，否则就是b

// 闭区间运算符
for index in 1...5 {}	// 返回一个a到b区间的所有的值
// 半开区间运算符
for index in 0..<5 {}
```

##### 字符串

```swift
string.isEmpty    	// 判断字符串是否为空
count(string)		// 求长度
let g = "\(var1) 呵呵"	// 直接将变量的值插入字符串，用反斜线为前缀的括号中
string.hasPrefix("abc")		// 判断前缀
string.hasSuffix("def")		// 判断后缀
string.uppercaseString		// 转换为大写
string.lowercaseString		// 转换为小写
```

##### 数组

```swift
var strList = ["A", "B"]	// 直接定义
var strList: [String] = ["A", "B"]	// 定义
var strList = [Int](count: 10, repeatedValue: 0)// 定一个一个包含10个零的数组
var StrList = Array(count: 10, repeatedValue: 1)
strList.count	// 数组长度
strList.isEmpty	// 是否为零
strList += ["C"]	// 可以直接加
strList[5...7] = ["E", "F"]		// 能这样插入 
strList.insert("G", atIndex: 0)	// 也能这样插
strList.removeAtIndex(0)		// 删除一个元素
strList.removeLast()			// 删除最后一个元素
for item in strList {}			// 数组遍历
for (index, value) in enumerate(strList) {} // 遍历的同时获取到当前索引
```

##### 集合

```swift
var h = Set<Character>()	// 定义
h.insert("B")				// 插入
h.count						// 数量
h.isEmpty					// 是否为空
h.remove("B")				// 删除一个元素，返回值为该函数本身
h.contains("B")				// 集合是否包含一个特定的值
for item in h {}			// 遍历
for item in sorted(h) {}	// 有序遍历
h.intersection(i)			// 求两个集合的交集
h.symmetricDifference(b)	// 求两个集合不同的
h.union(b)					// 求两个集合的并集
h.subtracting(b)			// 求在h集合但不在b集合的
h.isSubsetOf(b)				// h是否为b的子集
h.isSupersetOf(b)			// h是否为b的父集
h.isDisjointWith(b)			// h和b是否完全不一样
```

##### 字典

```swift
var z: [String:String] = ["A": "a", "B": "b"]
z.count		// 字典元素数量
z.isEmpty	// 是否为空
z["C"] = "c"// 添加值
z.updateValue("C", forKey:"C") // 更新值，返回老值
z["C"] = nil	// 移除值
z.removeValueForKey("C")	// 移除值
for (key, value) in z {}	// 字典遍历
for key in z.keys {}		// 遍历key
for value in z.values {}	// 遍历value
let a = Array(z.keys)	
let b = Array(z.values) 
```

##### 函数

```swift
// 简单定义，函数的参数默认是常量，如果在函数题中更改参数值居然会编译错误，如果要传入一个变量参数，可以在参数名前加var，加了var，就可以在函数内部进行修改，但修改后的值并不能影响函数外部该值的原来的值，如果真的要修改外部的，那么要将参数定义为inout，表示是输入输出参数
func sayHello(userName: String, second: String = "默认值") -> String {
  let a = "B" + userName
  return a
}

// 多返回值定义
func count(string: String) -> (a: Int, b: Int) {
  return (a, b)
}

// 提供外部参数名的，在调用时必须提供外部的参数名
func function(externalParamterName localParameterName: int) {}
// 调用时
func(外部变量名: "abc")

// 好吧，这样就不用单独定义外部参数名了，外部参数名和内部参数名一样
func function(#string: String) {}

// 可变参数
func function(numbers: Double...) {}
```

##### 结构体/类

```swift
// getter/setter
struct Point {
    var x = 0.0, y = 0.0
}
struct Size {
    var width = 0.0, height = 0.0
}
struct Rect {
    var origin = Point()
    var size = Size()
    var center: Point {
      get {
          let centerX = origin.x + (size.width / 2)
          let centerY = origin.y + (size.height / 2)
          return Point(x: centerX, y: centerY)
      }
      set(newCenter) {
          origin.x = newCenter.x - (size.width / 2)
          origin.y = newCenter.y - (size.height / 2)
      }
    }
}
var square = Rect(origin: Point(x: 0.0, y: 0.0),
    size: Size(width: 10.0, height: 10.0))
let initialSquareCenter = square.center
square.center = Point(x: 15.0, y: 15.0)

// 属性观察器，每次属性被设置的时候都会调用属性观察器，有两种
willSet: 在设置新的值之前调用
didSet: 在新的值呗设置之后调用
// 直接在定义结构体或类内部变量时使用
class Example {
  var test: Int = 0 {
    willSet(newValue) {
      println("hehe")
    }
    didSet {
      println("haha")
    }
  }
}

// 下标脚本
// 构造器
struct teset {
  var a: Double
  init() {
    a = 12.0
  }
}
```























