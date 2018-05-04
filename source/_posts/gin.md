---
title: "Go Web框架gin"
date: 2018-05-04 23:25:00
categories: Go
---

目前，基于Go的web框架也可谓是百花齐放了，之所以选择`gin`，没其他原因，就只是因为其在github上的star数是最多的，而且仅仅从README看，其文档也是相当丰富的。

## 安装gin

直接使用`go get github.com/gin-gonic/gin`即可。

官方README中提供了非常多的例子。例如最简单的实例代码:

```go
package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.Run() // listen and serve on 0.0.0.0:8080
}
```

## 路由

```go
router := gin.Default()	// 默认是带有Logger和Recovery中间件的
router := gin.New()	// 不带中间件的路由
router.Use(gin.Logger()) // 可以使用这种方式来指明中间件
router.GET("/test", MyMiddleware(), testEndpoint)	// 也可以用这种方式给指定路由添加中间件
router.GET("/someGet", getting)	// 支持所有Restful的操作

// 带参数的路由
router.GET("/user/:name", func(c *gin.Context) {
		name := c.Param("name")
})

// 参数可选/通配符功能
router.GET("/user/:name/*action", ...)

// 路由分组
v1 := router.Group("/v1")
{
    v1.POST("/login", loginEndpoint)
    v1.POST("/submit", submitEndpoint)
}

v1.Use(AuthRequired()) {}	// 路由分组单独指定中间件
```

## 请求与响应

### 请求

```go
// 获取路由参数，假设有路由为"/user/:name"
c.Params.ByName("name")

// 获取query参数
c.Query("name")
c.DefaultQuery("name", "Guest")

// 获取表单参数
c.PostForm("name")
c.DefaultPostForm("name")
```

#### 参数绑定

#### 请求验证

### 响应

```go
// 返回简单的字符串
c.String(200, "pong")

// 返回JSON数据
c.JSON(200, gin.H{
    "message": "pong",
})

// 重定向
c.Redirect(http.StatusMovedPermanently, "https://google.com")

```

## 中间件

### 自定义中间件

### BasicAuth中间件

## 异步协程

gin可以借助协程来实现异步任务，但是这时候得手动copy上下文，并且只能是可读取的。

```go
router.GET("/async", func(c *gin.Context) {
    cCp := c.Copy()
    go func() {
        time.Sleep(5 * time.Second)
        log.Println("Done! in path" + cCp.Request.URL.Path)
    }()
})
```



 

