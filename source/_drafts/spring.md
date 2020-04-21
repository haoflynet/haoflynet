---
title: "Java Spring手册"
date: 2018-11-01 21:32:00
update: 2020-04-13 15:30:00
categories: 编程之路
---

[Spring Initializr](<https://start.spring.io/>)：Spring项目初始化工具。

### 框架分层结构

调用顺序

> Controller --> Service Interface --> Service Impl --> Dao Interface --> Dao Impl --> Mapper --> DB

#### BIZ层

Service(业务逻辑，可以建立子文件夹来进行分类，这样每个biz就可以更细分，如果Biz和Servic都单独作为一层，那么Biz的粒度更细，`Service`则是提供给别人的接口)、Schedule(定时任务)、Common(一些中间件认证登录等)、Manager、RPC Service、MQTask、JobTask。也有Service和BIZ平行的分层方式，这种情况，一般是Service在调用Biz，Biz执行数据库操作，类似于Manager。

BO(Business Object)

#### COMMON层

一些公共的对象，公共的抽象类、公共的异常、公共的帮助方法等

#### DAO层

一般是由MyBatis等工具自动生成的。

DO/PO(Data Object/Persistant Object，与数据表直接对应，也叫Entity层或者Model层)：用于存放实体类，与数据库中的属性值保持一致。

Mapper: 对数据库进行数据持久化操作，它的内部方法就是直接对数据库进行操作的。它类似于manager层。可以封装对数据库的复杂的操作。

VO(value object，类似于将数据库的字段抽象为新的业务相关的字段): VO往往用于请求处理层，即Controller。

#### INTEGRATE层

外部系统的一些接口

#### Web层

Controller、Config(一些初始化配置，例如线程池、缓存池等配置的初始化)

### 注解

#### @Async

- 必须用在`public`方法上，同一个类的其他方法调用此方法无法实现异步
- `Spring`使用的是`SimpleAsyncTaskExecutor`来处理`@Async`注解的任务

```java
@EnableAsync
public class MyClass {
  @Async
  public void testMethod() {
    	System.out.println("Currently Executing thread name - " + Thread.currentThread().getName());
  }
}
```

#### Autowired

- 自动注入，默认按照类型去匹配`bean`

#### @Resource

- 和`Autowired`类似，默认按照`name`去匹配`bean`

```java
public class Post {
  @Resource(name = "author")
  private Author author;
}
```

@Service用于标注业务层组件

@Controller用于标注控制层组件（如struts中的action）

@Repository用于标注数据访问组件，即DAO组件

@Component泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注。

### 重要概念

#### bean

- `bean`有两种初始化方法:
  - 在`applicationContext.xml`中直接添加指定的类`<bean id="myBean" class="com.MyBean" init-method="initMethod"></bean>`
  - 实现`InitializingBean`接口，并实现`afterPropertiesSet`方法，这样可以在所有其他的属性设置完成后才初始化该类，如果用上面的方式，则无法实现依赖注入(其他的依赖都还没有初始化)。可以在里面新建一个线程实现启动完成后添加监听线程的功能。
  
- 在任意地方获取指定的`bean`，可以有效解决循环依赖的问题，如下，建立一个方法类:

  ```java
  package com.haofly.net.common.utils;
  
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.ApplicationContextAware;
  import org.springframework.stereotype.Component;
  
  @Component	// 一定要加这个
  public class SpringContextUtil implements ApplicationContextAware {
      /**
       * Spring应用上下文环境
       */
      private static ApplicationContext applicationContext;
      /**
       * 实现ApplicationContextAware接口的回调方法，设置上下文环境
       */
      @Override
      public void setApplicationContext(ApplicationContext applicationContext) {
          SpringContextUtil.applicationContext = applicationContext;
      }
  
      public static ApplicationContext getApplicationContext() {
          return applicationContext;
      }
  
      /**
       * 获取bean对象
       *
       * @param name bean名称
       * @return Object 一个以所给名字注册的bean的实例
       */
      public static Object getBean(String name) {
          return applicationContext.getBean(name);
      }
  }
  
  
  // 在其他地方可以这样子直接获取指定的bean
  BusniessServiceImpl businessServiceImpl = (BusinessServiceImpl) SpringContextUtil.get("businessServiceImpl");	// 需要注意的是，如果放在应用初始化的过程中，那么该类中的applicationContext可能还没有初始化，可以sleep以下或者其他方式
  ```

#### AOP切片

- 切片的功能类似于中间件，或者说插件

在`applicationContext.xml`中定义切片:

```xml
<bean id="myLogAspect" class="net.haofly.commons.util.LogAspect"></bean>
<aop:config>
  <!-- 设置切入点 -->
  <aop:pointcut expression="execution(* net.haofly.cloud.service.*.impl.*.*Impl.*(..)) and !execution(* net.haofly.service.tt.impl.ServerImpl.createServer(..))" id="myPointcut"/>	<!-- 排除某个方法直接用! -->
  
  <!-- 设置切面: 将指定bean对象中的某个方法切入到某个切入点，这里是把日志里面的validate方法切入到上面那些切入点中 -->
  <aop:aspect ref="myLogAspect">
    <aop:around method="validate" pointcut-ref="myPointcut"/>
  </aop:aspect>
</aop:config>
```

## TroubleShooting

- 启动时在`Initializing Spring FrameworkServlet 'spring'`这一句日志时候，可能是以下原因之一
  - `Mybatis`的`xml`文件的id可能重复了



##### 扩展阅读

- [Aliyun Java Initializr](https://start.aliyun.com/): Spring的国内的脚手架



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



kafka

https://spring.io/projects/spring-kafka#overview

https://juejin.im/entry/5b5ac2aff265da0f6263877c