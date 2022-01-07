## 通用配置

```javascript
AdminModule.createAdmin({
  adminJsOptions: {
    rootPath: '/admin',
    resources: [User],
  },
  auth: {
    authenticate: async (email, password) => Promise.resolve({ email: 'test' }),
    cookieName: 'auth',
    cookiePassword: 'test',
  }
})
```

## 框架集成

### NestJs

```shell
# 依赖安装
npm install --save adminjs @adminjs/nestjs express-session

# 在app.module.ts中引入
imports: [
	AdminModule.createAdmin({
    adminJsOptions: {
      rootPath: '/admin',
      resources: [User],
    }
  }),
]
```

