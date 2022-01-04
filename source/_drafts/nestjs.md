## 项目配置

```shell
# 项目初始化
npm i -g @nestjs/cli
nest new project-name
```

### .env配置文件支持

```javascript
npm i --save @nestjs/config

// 然后在app.module.ts中引入即可
@Module({
  imports: [ConfigModule.forRoot()], // 如果像要所有modules都能使用可以设置{isGlobal: true}参数
})

process.env.TEST	// 使用
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

## 资源Resource

- 使用`nest g resource`能够直接生成一个资源对应的文件Module、Controller等，当然数据库model不会自动生成

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

@Controller('users')	// 定义路由路径
export class UserController {}

@Controller('users/:userId') // 嵌套资源，子资源，可以这样定义路由
export class PostController {
  @Get('/posts/:id')
  getUserPostDetail(@Param('userId') userId, @Param('id') id) {}
}
```

## 数据库

### NestJs +Sequelize

- 安装:

  ```shell
  npm install --save @nestjs/sequelize sequelize sequelize-typescript mysql2
  npm install --save-dev @types/sequelize
  ```

- 配置，具体的数据表定义和用法可以参考[sequelize-typescript文档](https://github.com/RobinBuschmann/sequelize-typescript#readme)

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
        models: [],
      }),
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
    imports: [SequelizeModule.forFeature([UserModel])],
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
