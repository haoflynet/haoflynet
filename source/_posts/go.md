---
title: "Go 手册"
date: 2018-04-13 19:02:30
updated: 2018-04-16 00:52:00
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

## 基本语法

### 变量

基本的变量类型有`bool/string/int/int8/int16/int32/int64/uint/uint8/uint16/uint32/uint64/unitptr/float32/float64/complex64/complex128`(其中`uint8`=`byte`，`int32`=`rune`)

```go
var a, b bool	// var声明变量，必须在后面指定类型。而且会给一个默认值
var c, d int = 1, 2
e := 3	// 不用var直接声明并赋值
const f = 4 // 声明常量

// 数组
var g [10]int	// 声明g为一个包含10个int的数组
h := [3]int{1,2,3}	// 这个定义语法也是...唉
i := []int{1,2,3}
h[low : high]	// 居然能切片，需要注意的是，切片之后并不是新建变量，而只是原数组的部分引用，修改切片后的值会影响原数组
len(h)	// 切片的元素数量
cap(h)	// 切片的容量。从切片的第一个元素到底层数组的末尾元素的元素数量
j := make([]int, 5)	// make 函数会分配一个元素为零值的数组并返回一个引用了它的切片
k := make([]int, 0, 5) // len(k)=0, cap(k)=5
k = append(k, 1)	// 向切片增加元素

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

### 控制语句

```go
// if语句
if x < 0 {}
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
// defer语句会将语句推迟到外层函数返回之后执行，相当于finally，例如
defer resp.Body.Close()

// return后面不跟参数可以直接返回定义了的变量名
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}
```

### 错误处理

通常函数都会返回一个error值

```go
re, err := Abs()
if err != nil {}
```

### go协程-go程

Go的协程居然就叫go。`select`语句让go可以等待多个通信操作

```go
go f(x,y,z)	// 这样会启动一个新的协程去处理f函数

// 信道: 带有类型的管道，你可以通过它用信道操作符 <- 来发送或者接收值。看起来非常有用。信道的发送和接收操作在另一端准备好之前都会阻塞。如果在go之后，相当于等待协程完成
ch := make(chan int)	// 定义一个信道，其中的值类型为int
ch := make(chan int, 100)	// 带缓冲区的信道，仅当信道的缓冲区填满后，向其发送数据时才会阻塞。当缓冲区为空时，接受方会阻塞
close(ch)	// 主动关闭信道
for i: = range ch	// 这样可以不断从信道取数据，信道关闭后自动退出
ch <- v	// 将v发送到信道ch
v := <-ch // 从ch接收值

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

### 包管理

引用包里面的变量，必须是已经导出的，只有大写开头的才是导出的，例如`math.Pi`

```go
// 定义当前包名
package main
// 导入包
import (
	"fmt
    "math""
)
```

## 标准库

### 网络请求

```go
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
```

### 时间处理

```go
import time
start := time.Now()	// 获取当前时间，格式虽然不大懂，但是时间运算是相当强的
start - time.Now()	// 计算时间差，自带单位换算，而且非常精准
```

