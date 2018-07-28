---
title: "Go 手册"
date: 2018-04-13 19:02:30
updated: 2018-07-28 11:49:00
categories: go
---

终于有应用场景需要用到Go了，这次算是正式开始学了。其实在我眼里，Go的应用场景主要有以下几点

- 超高并发/超高性能
- 多核CPU充分利用
- 系统底层应用开发

其实自己的项目或者现在公司的项目，都配不上"超高"两字，所以也就没考虑过用`Go`语言，而是用能快速开发的`Python`和`PHP`。

<!--more-->

## 安装Go

需要注意的是，在使用go之前，必须设置GOPATH这个环境变量，并且该环境变量不允许和`GOROOT`一样，该目录是用来存放第三方包的源码的地方。

## 编译与构建

如果是一个单独的文件运行程序，那么该文件的package必须是`package main`，否则会出现`go run: cannot run non-main package`错误

## 基本语法

### 变量

- 基本的变量类型有`bool/string/int/int8/int16/int32/int64/uint/uint8/uint16/uint32/uint64/unitptr/float32/float64/complex64/complex128`(其中`uint8`=`byte`，`int32`=`rune`)
- 如果是在块中定义的变量(例如if for等)，作用于仅仅在块中

```go
var a, b bool	// var声明变量，必须在后面指定类型。而且会给一个默认值
var c, d int = 1, 2
e := 3	// 不用var直接声明并赋值
const f = 4 // 声明常量
_, err := function()	// 表示第一个返回值后面不会被使用，这样可以防止出现"declared and not used"提示

reflect.TypeOf(b)	// 获取变量类型

// 指针
var p *int	// 定义p是一个指向int类型值的指针，默认值为nil
p = &a		// 取a的指针
*p			// 取值

// 结构体
type Vertex struct {
    x int
    y int
}
v = Vertex{1, 2}
v.x

// 给结构体定义方法，类似于类
func (v Vertex) Abs() float64{
    return math.Sqrt(v.X*v.Y)
}
v.Abs()	// 就可以这样调用了

// 变量映射，额，跟字典超级像呀
var m map[string]Vertex
m = make(map[string]Vertex)
m["test"] = Vertex{10, 20}
delete(m, key)	// 删除元素

// 接口，就是由一组方法签名定义的集合
type Abser interface {
    Abs() float64
}
```

#### 数字/整型/布尔值

- 布尔值的默认值为false
- 由于`int`类型的范围，与平台有关，所以在长度不确定的时候，最好使用`int64`

```go
string:=strconv.Itoa(int)	// 整型转换为字符串
string:=strconv.FormatInt(int64,10)	// int64转换为字符串
myInt := int64(normalInt)	// int转换为int64

// 产生随机数
rand.Seed(time.Now().Unix())	// 初始化随机种子
rand.Intn(len(proxies))
```

#### 数组slice

```go
var g [10]int	// 声明g为一个包含10个int的数组
h := [3]int{1,2,3}	// 这个定义语法也是...唉
i := []int{1,2,3}
h[low : high]	// 居然能切片，需要注意的是，切片之后并不是新建变量，而只是原数组的部分引用，修改切片后的值会影响原数组
len(h)	// 切片的元素数量
cap(h)	// 切片的容量。从切片的第一个元素到底层数组的末尾元素的元素数量
j := make([]int, 5)	// make 函数会分配一个元素为零值的数组并返回一个引用了它的切片
l := make([]int, len(...))
k := make([]int, 0, 5) // len(k)=0, cap(k)=5
k = append(k, 1)	// 向切片增加元素

// 动态数组/不定长数组
var arr []string
newArr = append(arr, "one")
```

#### 字符串/json

```go
str = `定义超长的字符串`
if str == "" {}	// 判断字符串是否为空
fmt.Sprintf("%s %d", "abc", 1)	// 字符串格式化

int,err:=strconv.Atoi(string)	// 字符串转换为int类型
int64, err := strconv.ParseInt(string, 10, 64)	// 字符串转换为指定类型指定进制的整型
arr := []byte(str)	// 将字符串直接转换为字节数组

// 字符串查找
strings.Contains("seafood", "foo")	// 字符串是否包含某个子字符串
strings.Count("abc", "a")	// 子字符串在字符串中出现的次数
strings.HasPrefix("Gopher", "Go")	// 字符串开头
strings.HasSuffix("Amigo", "go")	// 字符串结尾

// 字符串分割
strings.Split("foo,bar,baz", ",")	// ["foo" "bar" "baz"]
strings.SplitAfter("foo,bar,baz", ",") // ["foo," "bar," "baz"]
strings.SplitN("foo,bar,baz", ",", 2)	// ["foo", "bar,baz"]

// 正则表达式
reg := regexp.MustCompile(`"page":(\d)`)	// 定义规则
match := reg.FindStringSubmatch(text)	// 获取满足条件的子字符串，match[1]表示括号中的，这里只匹配第一次，FindAllStringSubmatch表示查找所有
```

#### 结构体/类/接口

- go语言本身没有类的概念，但是可以用结构体来实现一个类。

- 判断结构体是否为空，可以直接判断里面的某个字段是否为空，或者，新建一个空结构体，例如`(Option{})  == option`

- 结构体中属性开头字母如果大写，表示可以在其他包中访问，否则只能在本包中访问。这个地方需要特别注意的是，像使用`json.Marshal`类似的操作，也是访问不到小写开头属性的，因为`json`算是另外一个包了

- 接口`interface`类似于基类或者接口类，定义一些公有的方法然后继承者去实现

- 空接口类型`interface{}`可以存储任意数据类型的实例，如果用于函数参数表示该函数接收任意的数据类型

- 由于有些函数确定了入参类型，但是接口又代表的是所有类型，所以如果要把一个接口传入一个明确类型的函数中，就需要特别指明其类型。例如`function(var.(string)`。不过这不能作用于接口数组，否则会出现`invalid type assertion non-interface type []... on left`这样的错误，如果要传入一个数组，需要我们构建一下[参考](https://stackoverflow.com/questions/27689058/convert-string-to-interface):

  ```go
  var face []interface{}
  for i, book := range books{
      face[i] = book
  }
  function(face)	// function([] interface{})
  ```

- 

```go
// 创建匿名结构体
var book struct{Name string}
json.Marshal(struct{Name string, year int}{"name", 2018})	// 这种方式可以在创建的时候初始化值

// 结构体转json格式字符串
b, err := json
if err != nil {}
str := string(b)

// json格式字符串转结构体使用tag来定义序列化时的字符串名称，例如
type Book struct{
    Name string `json:"name" bson:"NAME"`
}
var book Book
jsonStr := `{"Name": "haofly"}`
json.Unmarshal([]byte(jsonStr), &book)
fmt.Println(book)

// 继承/组合结构体
type Option2 struct {
    Option
    ip string
}

// 可以自己在当前package里面写一个函数来当作构造函数，例如
func NewOption(arg Args) (Option, error) {
    return Option{}
}

// 实例化的几种方法
var opt Option;	// 变量声明
opt.proxy = ""	// 给字段复制
opt := Option{}
opt := &Option{}
opt := &Option{proxy: ""}
opt := Option{proxy: ""}
opt := new(Option)

// 在定义完结构提后，可以这样声明类的方法
func (option *Option) get() {...}
```

### 控制语句

```go
// if语句
if x < 0 {}
if x <0 && y > 0 {}
if v := match.Pow(x, n); v < lim {}	// 一边if一边声明变量，该变量只有在该作用域有效

// for 循环
for i := 0; i < 10; i++ {}
for ; sum < 1000; {}	// 可以直接不写前后条件
for sum < 1000 {}	// while循环
for {}	// while true循环
for i,v := range pow {}	// pow是一个切片，for循环遍历切片时，每次迭代都会返回两个值，第一个是下标，第二个是元素

// switch，不需要在case后面加break
switch os := os; os {
    case "darwin":
    	...
    default:
    	...
}
switch {
    case t.Hour() < 12:	// 没错，可以这样写条件。反正都是从上往下，匹配到第一个就终止。其他语言为啥不这样
    	...
}
```

### 函数

```go
// defer语句会将语句推迟到外层函数返回之后执行，相当于finally，类似析构函数，例如
defer resp.Body.Close()

// return后面不跟参数可以直接返回定义了的变量名
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

// 定义返回带异常的函数，相当于将内部的err抛出来
func my(a int) (string, error) {
    return "123", nil	
}

// 定义不确定变量数量的函数/可选参数
func test(v ...interface{}) {
    fmt.Println(v)	// 是一个切片/数组
    fmt.Println(v[0])
    fmt.Println(v[1].(string))	// 在使用的时候声明该变量类型
}
```

### 错误处理

通常函数都会返回一个error值

```go
re, err := Abs()
if err != nil {}

if re, err := Abs(); err != nil {}	// 直接在一行进行错误处理

errors.New("redis not connectetd")	// 新建一个error

// 聚合处理error
var err error
defer func() {
    if err != nil {
        handle()
    }
}()
//这样当有错误出现的时候不用单独写handle函数，所有错误同样处理
err = doSomeThing()
if err != nil {return}
```

### go协程-go程

Go的协程居然就叫go。`select`语句让go可以等待多个通信操作。

```go
go f(x,y,z)	// 这样会启动一个新的协程去处理f函数

// select使一个Go程可以等待多个通信操作。select 会阻塞到某个分支可以继续执行为止，这时就会执行该分支。当多个分支都准备好时会随机选择一个执行。
func fibonacci(c, quit chan int) {
	x, y := 0, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}
c := make(chan int)
quit := make(chan int)
go func() {
    for i := 0; i < 10; i++ {
        fmt.Println(<-c)
    }
    quit <- 0
}()
fibonacci(c, quit)

// 锁sync.Mutex
```

#### 信道

信道是带有类型的管道，你可以通过它用信道操作符 <- 来发送或者接收值。看起来非常有用。信道的发送和接收操作在另一端准备好之前都会阻塞，相当于发送信道方在其他协程从信道读取数据之前会被阻塞，而接收信道方在其他协程发送之前会被阻塞。可用于在其他协程结束之前，阻塞Go主协程。

```go
ch := make(chan int)	// 定义一个信道，其中的值类型为int
ch := make(chan int, 100)	// 带缓冲区的信道，仅当信道的缓冲区填满后，向其发送数据时才会阻塞。当缓冲区为空时，接受方会阻塞
close(ch)	// 主动关闭信道
ch <- v	// 将v发送到信道ch
v := <-ch // 从ch接收值

// 这样可以不断从信道取数据，信道关闭后自动退出，但是信道如果没有主动关闭，会一直等待，其中i就是信道发送过来的值
for i: = range ch {
    // 虽然不能直接在这里面close(ch)，但是可以通过判断来break，在循环break之后close信道呀
}	
```

### 文件操作

```go
b, err := ioutil.ReadFile("test.json")	// 直接读取文件内容
if err != nil {}
str := string(b)	// 将文件内容转换为字符串
```

### 包管理

引用包里面的变量，必须是已经导出的，只有大写开头的才是导出的，例如`math.Pi`

```go
// 定义当前包名
package main
// 导入包
import (
	"fmt"
    "math"
)
```

## 标准库

### 网络请求

```go
import "net/http"
// GET请求
resp, err := http.Get("https://haofly.net")
if err != nil {}
defer resp.Body.Close()		// 必须关闭连接
body, err := ioutil.ReadAll(resp.Body)
if err != nil {}
fmt.Println(string(body))

// POST请求
http.Post('url', "application/x-www-form-urlencoded", strings.NewReader("name=test"))
http.PostForm('url', url.Values{"key": {"value"}})

// 复杂的http请求用client，例如设置header头以及cookie
client := &http.Client{}
req, err := http.NewRequest("POST", "url")
if err != nil {}
req.Header.Set("Content-Type", "")
req.Header.Set("Cookie", "name=test")
resp, err := client.Do(req)

// http编码转换(gbk转utf8)，使用标准库golang.org/x/net/html/charset
contentType := resp.Header.Get("Content-Type")
utf8reader, err := charset.NewReader(resp.Body, contentType)
if err != nil {}
text, err := ioutil.ReadAll(utf8reader)
if err != nil {}
return string(text), nil
```

### 时间处理

```go
import time
start := time.Now()	// 获取当前时间，格式虽然不大懂，但是时间运算是相当强的
start - time.Now()	// 计算时间差，自带单位换算，而且非常精准
```

## 扩展库推荐

基本上可以理解为`gopkg.in`才是Go官方推荐的库网站，地址与github中的地址其实是相对应的，不过这个好处是可以在后面加一个版本号做到版本控制

- **gjson**: 非常好用的redis数据读取库(仅仅是读)
- **logrus**: 日志库，默认日志级别为`Info`，`Debug`级别需要主动设置
- **[mgo](https://godoc.org/gopkg.in/mgo.v2#Bulk.Insert)**: mongo驱动
- **redigo**: redis驱动

## TroubleShooting

- **should have comment or be unexported**，这只是VSCode的语法Warning，它希望暴露的结构体等有一个明确的注释，这时候只需要在需要注释的结构体上面加上这样的注释即可:

  ```go
  // test is ...
  type test struct {}
  ```


##### 扩展阅读

[官方FAQ](https://golang.org/doc/faq): 我见过写得最详细的编程语言官方FAQ