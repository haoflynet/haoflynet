---
title: "Nestjs 使用手册"
date: 2022-04-29 08:00:00
updated: 2022-08-25 15:40:00
categories: Javascript
---

## 项目配置

- 默认端口为3000，如果要修改可以在`src/main.ts`中进行修改

```shell
# 项目初始化
npm i -g @nestjs/cli
nest new project-name
```

### .env/dotenv配置文件支持

```javascript
npm i --save @nestjs/config

// 然后在app.module.ts中引入即可
@Module({
  imports: [ConfigModule.forRoot()], // 如果想要所有modules都能使用可以设置{isGlobal: true}参数
})

process.env.TEST	// 使用
```

<!--more-->

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

## 资源Resource

- restful里面常用的概念
- 使用`nest g resource`能够直接生成一个资源对应的文件Module、Controller等，当然数据库model不会自动生成

### Dto

- 用于前后端交互数据类型的定义，可以这样子将entity(model)转换为dto

```javascript
class MyDto {
  name: string
  
  static fromModel (model: MyModel): MyDto {
    const myDto = new MyDto()
    myDto.name = model.name
    return myDto
  }

	static fromModels (models: MyModel[]): MyDto[] {
    return models.map((model) => MyDto.fromModel(model))
  }
}
```

### Entity

- 我们的model可以作为entity来用，以`*.entity.ts`结尾

## 路由与控制器

- 可以使用`nest g controller`生成控制器，不过最好还是用`nest g resource`生成一个资源，包含了一些其他的逻辑文件

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
    @Query('type') type: string // 只取某一个参数
    @Body() body: any	// @Body指定请求body
  	@Headers() headers: any // @Headers获取header头
  	@Request() req: any,  // import { Request } from '@nestjs/common'
  ): string {
    
  }
}

@Controller('users')	// 定义路由路径
export class UserController {}

@Controller('users/:userId') // 嵌套资源，子资源，可以这样定义路由
export class PostController {
  @Get('/posts/:id')
  getUserPostDetail(@Param('userId') userId, @Param('id') id) {}
}
```

### 异常

```shell
# 常见异常，默认返回的是{"statusCode": 422, "error": "Unprocessable Entity"}格式
NotFoundException: 404
UnprocessableEntityException: 422
InternalServerErrorException: 500

throw new UnprocessableEntityException('field error')	# 如果在异常类上添加一个字符串，会在返回结果中添加一个message字段
```

## 数据库

### NestJs +Sequelize

- 安装:

  ```shell
  yarn add @nestjs/sequelize sequelize sequelize-typescript mysql2
  yarn add -D @types/sequelize
  ```

- Migration: 由于migration和代码无关，也无需依赖注入，可以直接用sequelize-cli命令来创建维护即可，参考[Sequelize 使用手册](https://haofly.net/sequelize)

- 事务：[官方](https://docs.nestjs.com/techniques/database#transactions)不建议直接使用`@transaction`装饰器来包装事务，其实手动写也还好，因为需要用到事务的地方并不多

- 配置，具体的数据表定义和用法可以参考[sequelize-typescript文档](https://github.com/RobinBuschmann/sequelize-typescript#readme)以及我写的[Sequelize 使用手册](https://haofly.net/sequelize)

  ```javascript
  // app.module.ts的imports中进行引入
  @Module({
    imports: [
      SequelizeModule.forRoot({
        dialect: 'mysql',
        host: 'localhost',
        port: 3306,
        username: 'root',
        password: 'root',
        database: 'test',
        loggin: false,	// 是否打印mysql的日志
        models: [],
      }),
      forwardRef(() => AbcModule),	// 如果两个module之间互相依赖，可以使用forwardRef来解决循环依赖的问题, can't resolve dependencies of the ...
    ],
  })
  
  // 通过nest g resource User来生成资源文件夹，然后在其目录下新建model文件，例如user.model.ts
  import { Column, CreatedAt, Model, Table, UpdatedAt } from 'sequelize-typescript'
  
  @Table({ tableName: 'users' })
  export class UserModel extends Model {
    @Column
    username: string;
  
    @CreatedAt
    @Column({ field: 'created_at' })
    createdAt: Date;
  }
  
  // 定义完成后需要在users.module.ts中引入该model
  @Module({
    imports: [
      SequelizeModule.forFeature([UserModel])
    ],
    controllers: [UsersController],
    providers: [UsersService],
    exports: [SequelizeModule]
  })
  export class UsersModule {}
  
  // 然后就能在service注入了
  @Injectable()
  export class UsersService {
    constructor (
      @InjectModel(UserModel)
      private readonly userModel: typeof UserModel
    ) {}
  }
  ```

## [JWT认证Authentication](https://docs.nestjs.com/security/authentication#jwt-functionality)

- 需要注意文档里的[Enable authentication globally](https://docs.nestjs.com/security/authentication#enable-authentication-globally)配置是全局的配置，我们一般不会需要这样做，因为登录注册等接口是不需要token的

- 在控制器获取jwt token的payload，可以这样做

  ```javascript
  import {Request} from '@nestjs/common'
  
  async getInfo(@Request() req: any) {
    console.log(req.user);
    return {
      ...req.user
    };
  }
  ```

- `jwt-auth.guard.ts`中可以在handleRequest中处理错误

  ```javascript
  @Injectable()
  export class JwtAuthGuard extends AuthGuard('jwt') {
    canActivate(context: ExecutionContext) {
      // 程序首先就是在这里验证，如果这里返回false，那么会直接403
      throw new UnauthorizedException()
      
      const request = context.switchToHttp().getRequest()
      request.user = await this.userService.findOne()	// 可以这样，然后就可以在@Request req中使用了
      
      return super.canActivate(context);
    }
  
    handleRequest(err, user, info) {
      if (err || !user) {
        throw err || new UnauthorizedException();
      }
      return user;
    }
  }
  ```

## 开启CORS

```javascript
const app = await NestFactory.create(AppModule, { cors: true });
await app.listen(3000);
```

## OpenAPI/Swagger文档

- [官方文档](https://docs.nestjs.com/openapi/introduction): 按照官方文档安装以来，然后直接替换main.ts即可

```javascript
export class UserController {
  @Post('/signin')
  @ApiCreatedResponse({
    description: 'Signin success',
    type: UserResponseDto,// 响应的类型需要在这里定义
  })
  @ApiResponse({ status: 201, description: 'The record has been successfully created.'})
  @ApiResponse({ status: 403, description: 'Forbidden.' })	// 可以定义多个response
  async signin(@Body() signDto: SigninDto): Promise<UserResponseDto> {}
}

class SignDto {
  @ApiProperty({ // 定义需要在API文档上展示的字段
    default: 'signin',	// 定义默认值
    enum: ['signin', 'signup'],	// 定义枚举值
    description: '', // 字段描述
    required: false,	// 如果是可选参数可以这样设置
  })
  name: string;
}
```

## 部署nestjs到aws lambda Serverless

[官方文档](https://docs.nestjs.com/faq/serverless)虽然提了一下，但是并没有一个方便的包来实现这些步骤，只能按照他提供的步骤摸索着来。要将nestjs转换为serverless模式，最主要的问题就是减少冷启动的时间。所以我们最好在编译阶段就进行优化。

1. 首先安装必要的依赖
   ```shell
   # For npm
   npm i @vendia/serverless-express aws-lambda
   npm i -D @types/aws-lambda serverless-offline
   
   # For yarn
   yarn add @vendia/serverless-express aws-lambda
   yarn add -D @types/aws-lambda serverless-offline
   ```

2. 在根目录创建`serverless.yml`
   ```yaml
   service: serverless-example
   
   plugins:
     - serverless-offline
   
   provider:
     name: aws
     runtime: nodejs20.x
   
   functions:
     main:
       handler: dist/main.handler
       events:
         - http:
             method: ANY
             path: /
         - http:
             method: ANY
             path: '{proxy+}'
   ```

3. 修改main.ts
   ```javascript
   import { NestFactory } from '@nestjs/core'
   import { ValidationPipe, VersioningType } from '@nestjs/common'
   import { AppModule } from './app.module'
   import { CustomExceptionFilter } from './filter/exception.filter'
   import { Callback, Context, Handler } from 'aws-lambda'
   import serverlessExpress from '@vendia/serverless-express'
   
   let server: Handler
   
   async function bootstrap(): Promise<Handler> {
     const app = await NestFactory.create(AppModule)
     app.enableVersioning({
       type: VersioningType.URI
     })
     app.useGlobalPipes(new ValidationPipe())
     app.useGlobalFilters(new CustomExceptionFilter())
   
     await app.init()
   
     const expressApp = app.getHttpAdapter().getInstance()
     return serverlessExpress({ app: expressApp })
   }
   
   export const handler: Handler = async (
     event: any,
     context: Context,
     callback: Callback,
   ) => {
     server = server ?? (await bootstrap())
     return server(event, context, callback)
   }
   ```

4. 在`tsconfig.json`中添加配置:
   ```json
   {
     "compilerOptions": {
       ...
       "esModuleInterop": true
     }
   }
   ```

5. 在根目录创建`webpack.config.js`
   ```javascript
   module.exports = (options, webpack) => {
     const lazyImports = [
       '@nestjs/microservices/microservices-module',
       '@nestjs/websockets/socket-module',
     ]
   
     return {
       ...options,
       externals: [],
       output: {
         ...options.output,
         libraryTarget: 'commonjs2',
       },
       plugins: [
         ...options.plugins,
         new webpack.IgnorePlugin({
           checkResource(resource) {
             if (lazyImports.includes(resource)) {
               try {
                 require.resolve(resource)
               } catch (err) {
                 return true
               }
             }
             return false
           },
         }),
       ],
     }
   }
   ```

6. 测试
   ```shell
   # 这条命令会将整个目录编译为一个单独的js文件,  dist/main.js
   nest build --webpack
   
   # 本地测试
   npx serverless offline

7. 部署，将该js文件压缩为zip包上传到aws lambda即可

## 常用扩展

### [nestjs-command](https://www.npmjs.com/package/nestjs-command)

- 可用于编写命令行工具或者写一个daemon进程都可以，集成非常方便，直接复制文档中的例子即可

## 扩展文章

- [NestJS Microservice 的微服务架构初探](https://juejin.cn/post/6844904178200870920)
- [NestJS 微服务示例](https://zhuanlan.zhihu.com/p/372338721)

## TroubleShooting

- **测试的时候报错Use jest.setTimeout(newTimeout) to increase the timeout value, if this is a long-running test.** 其他方法我试过不行，只能在`package.json`的`jest`下添加`"testTimeout": 60000`
