---
title: "Java Spring-boot手册"
date: 2017-11-01 21:32:00
categories: 编程之路
---

https://start.spring.io/

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