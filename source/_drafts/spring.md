---
title: "Java Spring手册"
date: 2018-11-01 21:32:00
update: 2019-02-25 09:30:00
categories: 编程之路
---

[Spring Initializr](<https://start.spring.io/>)：Spring项目初始化工具。

### 框架分层结构

调用顺序

> Controller --> Service Interface --> Service Impl --> Dao Interface --> Dao Impl --> Mapper --> DB

#### BIZ层

Service(业务逻辑，可以建立子文件夹来进行分类，这样每个biz就可以更细分)、Schedule(定时任务)、Common(一些中间件认证登录等)。也有Service和BIZ平行的分层方式，这种情况，一般是Service在调用Biz，Biz执行数据库操作，类似于Manager。

#### COMMON层

一些公共的对象，公共的抽象类、公共的异常、公共的帮助方法等

#### DAO层

一般是由MyBatis等工具自动生成的。

PO(持久对象persistant object，与数据表直接对应，也叫Entity层或者Model层)：用于存放实体类，与数据库中的属性值保持一致。

Mapper: 对数据库进行数据持久化操作，它的内部方法就是直接对数据库进行操作的。它类似于manager层。可以封装对数据库的复杂的操作。

VO(value object，类似于将数据库的字段抽象为新的业务相关的字段)。

#### INTEGRATE层

外部系统的一些接口

#### Web层

Controller、Config(一些初始化配置，例如线程池、缓存池等配置的初始化)

### 注解

@Service用于标注业务层组件

@Controller用于标注控制层组件（如struts中的action）

@Repository用于标注数据访问组件，即DAO组件

@Component泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注。

## TroubleShooting

- 



```java
// 控制器
@RestController	// 就是@Controller与@ResponseBody的组合，@ResponseBody表示该方法返回值应绑定到web响应正文。当然这个表示当前控制器支持REST
public class HelloController {
    @RequestMapping("/hello")	    // 路由映射，也可以绑定在类上，还可以使用GetMapping/PostMapping/PutMapping/DeleteMapping/PatchMapping
    public String hello() {
        return "Hello World! Welcome to visit waylau.com!";
    }
}
```







https://mp.weixin.qq.com/s/2dCebIpVjE43xUpx-2YCTg



https://blog.tengshe789.tech/2018/08/04/springboot/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io



