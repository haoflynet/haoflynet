## 安装与配置

### 常用命令

```shell
yii cache 	# li
yii cache/flush-schema db	# 清除db缓存
```

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

## 控制器与路由

- 路由和某难用的框架一样是在`controller`下定义，且开头为`actionXXX`表示`/XXX`路径

## 帮助方法

```php
// 生成绝对URL
echo Url::to('@web/images/logo.gif');	// /images/logo.gif


// 生成指定html元素
Html::tag('p', Html::encode($user->name), ['class' => 'username']);	// <p class="username">samdark</p>

// 直接生成img tag
Html::img('@web/images/logo.png', ['alt' => 'My logo', 'class' => 'myclass1 myclass2']);	# <img src="http://example.com/images/logo.png" alt="My logo" />
```

