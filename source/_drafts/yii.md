## 安装与配置

### 数据库配置

在`common/config/main-local.php`中进行配置

```php
'db' => [
  'class' => 'yii\db\Connection',
  'dsn' => 'mysql:host=localhost;dbname=password',
  'username' => 'username',
  'password' => 'password',
  'charset' => 'utf8',
  'enableSchemaCache' => true,
  'schemaCacheDuration' => 86400,
  'schemaCache' => 'cache',
]
```

### Debug和日志

- 运行日志位置在`frontend/runtime/logs/app.log`

## 路由

- 路由和某难用的框架一样是在`controller`下定义，且开头为`actionXXX`表示`/XXX`路径
