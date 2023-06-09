## 通用配置

```javascript
AdminModule.createAdmin({
  adminJsOptions: {
    rootPath: '/admin',
    resources: [User, Project],
    resources: [User, Project].map((model) => {	// 或者可以这样子自定义各种字段
      const options: any = {
        resource: model,
        options: {
          sort: { direction: 'desc', sortBy: 'id' },
          properties: {
            createdAt: { isVisible: { edit: false } },
            updatedAt: { isVisible: { edit: false } },
            deletedAt: { isVisible: { edit: false } }
          }
        }
      }

      if (model === ProjectModuleModel) {
        options.options.listProperties = ['id', 'projectId', 'moduleId', 'name', 'worker', 'cron', 'nextAt', 'logs']
        options.options.editProperties = ['projectId', 'moduleId', 'name', 'description', 'worker', 'cron', 'nextAt', 'logs']
        options.options.showProperties = ['projectId', 'moduleId', 'name', 'description', 'cron', 'nextAt', 'created_at', 'logs']
      }
      return options
    })
  },
  auth: {
    authenticate: async (email: string, password: string) => {	// 设置自定义后台验证，如果没有这个那就是免登录的，非常危险
      if (email === DEFAULT_ADMIN.email && password === DEFAULT_ADMIN.password) {
        return Promise.resolve(DEFAULT_ADMIN);
      }
      return null;
    },
    cookieName: 'adminjs',
    cookiePassword: 'secret',
  }
})
```

## 框架集成

### NestJs

- 2023年6月：由于AdminJS现在只支持ESM，并且NestJS还不支持，所以安装后可能会有Bug(我根本运行不起来)，所以我只有将下面这些依赖固定到低版本

```javascript
// 依赖安装
yarn add --save @adminjs/express@^5.1.0 @adminjs/nestjs@^5.1.1 @adminjs/sequelize@^3.0.0 @tiptap/pm adminjs@^6.8.7 express-session express-formidable

// 在app.module.ts中引入
import { AdminModule } from '@adminjs/nestjs';
import * as AdminJSSequelize from '@adminjs/sequelize';
import AdminJS from 'adminjs';

AdminJS.registerAdapter({
  Resource: AdminJSSequelize.Resource,
  Database: AdminJSSequelize.Database,
});

imports: [
  AdminModule.createAdminAsync({
    useFactory: () => ({
      adminJsOptions: {
        rootPath: '/admin',
        resources: [UserModel],
      },
    }),
  }),
]
```

