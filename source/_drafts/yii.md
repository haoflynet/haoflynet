## 安装与配置

### 常用命令

```shell
yii serve 0.0.0.0 --port=8888	# 指定端口，指定host

# 缓存，缓存的文件在frontend/runtime/cache下面
yii cache 	# li
yii cache/flush-schema db	# 清除db缓存
```

### 常用配置

```php
# index.php
defined('YII_DEBUG') or define('YII_DEBUG', true);	# 打开debug模式

# common/config/main-local.php
'db' => [	# 数据库配置
  'class' => 'yii\db\Connection',
  'dsn' => 'mysql:host=localhost;dbname=password',
  'username' => 'username',
  'password' => 'password',
  'charset' => 'utf8',
  'enableSchemaCache' => true,
  'schemaCacheDuration' => 86400,
  'schemaCache' => 'cache',
]
  
// backend/config/main-local.php
$config = [
  'components' => [
    'request' => [
      'enableCsrfValidation' => false,	// 可以全局关闭csrf验证
    ]
  ]
]
```

### Debug和日志

- 运行日志位置在`frontend/runtime/logs/app.log`

## 控制器与路由

- 路由和某难用的框架一样是在`controller`下定义，且开头为`actionXXX`表示`/XXX`路径

```php
// 控制器的behaviors方法能够控制访问权限
public function behaviors() {
  return [
    'class' => AccessControl::className(),
    'rules' => [
      [
        'actions' => ['login', 'error'],
        'allow' => true,
      ],
      [
        'allow' => true,
        'roles' => ['@']	// 表示任何角色都能访问
      ]
    ]
  ]
}
```

## View视图

```php
public function viewIndex() {
  $this->view->title = 'abc';	// 这样可以动态设置title
  return render('viewname', ['key1' => 'value1'])
}

<?php
  use Yii;

	$this->title = 'xxx';	# 可以设置title

	$this->registerJsFile('/js/xxx.js');	// 单个页面引入js和css文件，注意yii2不能用Yii::app()来引入了
  $this->registerCssFile('/css/xxx.css');
?>
```

## 帮助方法

```php
// 生成绝对URL
echo Url::to('@web/images/logo.gif');	// /images/logo.gif


// 生成指定html元素
Html::tag('p', Html::encode($user->name), ['class' => 'username']);	// <p class="username">samdark</p>

// 直接生成img tag
Html::img('@web/images/logo.png', ['alt' => 'My logo', 'class' => 'myclass1 myclass2']);	# <img src="http://example.com/images/logo.png" alt="My logo" />
```

## 实用插件

- [yii2-lock-form](https://github.com/lichunqiang/yii2-lock-form): 禁止页面中的按钮重复点击
