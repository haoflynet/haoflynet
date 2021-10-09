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

