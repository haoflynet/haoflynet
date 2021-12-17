## 项目配置

```shell
# 项目初始化
npm i -g @nestjs/cli
nest new project-name
```

## 路由

```javascript
@Controller()	// 表示这是一个控制器
export class AppController {
  constructor (private readonly appService: AppService) {}	// 依赖注入

  @Get()	// Get方法
  getHello (): string {
    return this.appService.getHello()
  }

	@Post()	// Post方法，应该是不支持一个方法同时有多个HTTP methods的
	test (
    @Query() query: any // @Query指定请求query参数
    @Body() body: any	// @Body指定请求body
  	@Headers() headers: any // @Headers获取header头
  ): string {
    
  }
}
```

