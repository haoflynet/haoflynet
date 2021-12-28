## 项目配置

```shell
# 项目初始化
npm i -g @nestjs/cli
nest new project-name
```

## Module模块

- 模块用于组织应用程序结构，用于创建controller和provider关系的

```javascript
@Global()	// 一般不需要这个装饰器，除非要让一个模块变成全局模块，其他地方随时能使用，这个一般作用于helpers模块，这样其他模块想用就用，而不用在其他模块一个一个imports了
@Module({
  controllers: [TestController],
  providers: [TestService],	// 这样TestService就能注入到TestController中了
  imports: [],		// 如果需要调用其他模块exports的provider需要在这里声明一下
  exports: [TestService],	// 如果需要其他模块使用当前模块的provider，需要export一下
})
export class TestModule {}
```

## Provider提供者

- 例如service、repository、factory、helper等，都可以用来注入

## 路由与控制器

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

