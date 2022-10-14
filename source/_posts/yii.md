---
title: "Yii2 开发手册"
date: 2021-11-15 18:02:30
updated: 2022-09-16 08:44:00
categories: php
---

## 安装与配置

### 常用命令

```shell
yii serve 0.0.0.0 --port=8888	# 指定端口，指定host

# 缓存，缓存的文件在frontend/runtime/cache和backend/runtime/cache下面
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

<!--more-->

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

## GridView

- 展示一个数据表格

```php
<?= GridView::widget([
  'dataProvider' => $dataProvider,
  'filterModel' => $searchModel,
  'filterPosition' => '',
  'layout' => '<div class="row"><div class="col-sm-12">{items}</div></div><div class="row"><div class="col-sm-5 text-center-xs text-left-not-xs">{summary}</div><div class="col-sm-7 text-center-xs text-right-not-xs">{pager}</div></div>',
  'columns' => [
    [
      'class' => 'yii\grid\SerialColumn',
      'headerOptions' => ['class' => 'hidden-sm hidden-xs'],
      'contentOptions' => ['class' => 'hidden-sm hidden-xs'],
    ],
    [
      'label' => 'ID',
      'attribute' => 'id',
      'value' => function ($data) {
        return Html::a($data->id, ['upload/view', 'id' => $data->id]);
      },
      'format' => 'raw',
    ],
    [
      'label' => 'Field1',
      'attribute' => 'field1',
      'format' => 'raw',
    ],
    [
      'label' => 'Image',
      'attribute' => 'image',
      'value' => function ($data) {
        return Html::a($data->file_name, Yii::$app->urlManagerFrontEnd->createAbsoluteUrl(['uploads/' . $data->file_name]), ['target' => '_blank']);
      },
      'format' => 'raw',
    ],
    [
      'label' => 'Created',
      'attribute' => 'created',
      'headerOptions' => ['class' => 'hidden-xs'],
      'contentOptions' => ['class' => 'hidden-xs'],
    ],
    [
      'label' => 'Updated',
      'attribute' => 'updated',
      'headerOptions' => ['class' => 'hidden-sm hidden-xs'],
      'contentOptions' => ['class' => 'hidden-sm hidden-xs'],
    ],
    [
      'class' => 'yii\grid\ActionColumn',
     	'template' => '{view} {delete}'	// template能够自定义操作按钮，默认有预览、编辑和删除
    ],
  ],
]); ?>
```

## 数据库

### migrate

- `./yii migrate/create 名称`生成新的`migrations`文件

```php
class m211115_020340_名称 extends Migration {
  public funciotn safeUp () {
    $this->addColumn('user', 'activated', $this->boolean()		// 添加列
                     ->defaultValue(0)
                     ->after('created_at')	// 指定位置，只有after，没有before
                    );
    
    if (Yii::$app->db->getTableSchema('logs', true) === null) {	// 判断表是否存在
      $this->createTable('logs', [
        'id' => $this->primaryKey(),
        'ip' => $this->string()
      ]);
    }
  }
  
  public function safeDown () {
    $this->dropColumn('user', 'activated');	// 删除列

    return false;
  }
}
```

### 增删改查

```php
# 查询
User::find()->where(['activated' => true])->all();
User::find()->where(['and', ['>=', 'created_at', strtotime($from)], ['<', 'created_at', strtotime($to)]])->all(); // and操作
User::find()->select('name')->distinct()->all();	// distinct操作

# 更新
$user->activated = false;
$user->save();
```

## 命令工具

- 可以在`console`下创建控制器，该控制器可以作为命令行工具

```php
<?php
namespace console\controllers;
 
use yii\console\Controller;
 
class TestController extends Controller
{
    public function actionTest()
    {
        echo "test\n";
    }
}

# 如上，就可以执行./yii看到有一个新的命令空间，然后执行./yii test/test就可以执行该控制器的方法了
```

## 帮助方法

```php
Url::base();	// /path
Url::base(true); // http(s)://example.com/path
Yii::$app->urlManagerFrontend->createAbsoluteUrl(...);	// 创建全url路径

// 获取绝对路径
Yii::getAlias('@frontend/web/uploads/images/'.$fileName);

// 生成绝对URL
echo Url::to('@web/images/logo.gif');	// /images/logo.gif

// 生成指定html元素
Html::tag('p', Html::encode($user->name), ['class' => 'username']);	// <p class="username">samdark</p>

// 直接生成a tag
Html::a('Profile', ['user/view', 'id' => $id], ['class' => 'profile-link']);
Html::a('Profile', 'https://google.com', ['target' => '_blank']);

// 直接生成img tag
Html::img('@web/images/logo.png', ['alt' => 'My logo', 'class' => 'myclass1 myclass2']);	# <img src="http://example.com/images/logo.png" alt="My logo" />
```

## 实用插件

- [yii2-lock-form](https://github.com/lichunqiang/yii2-lock-form): 禁止页面中的按钮重复点击

- [~~yii2-cronjob~~](https://www.yiiframework.com/extension/yii2-cronjob): 定时任务插件，但是我`migrate`执行的是这个命令`./yii migrate --migrationPath=@vendor/fedemotta/yii2-cronjob/migrations`，还有其他坑，如果一个任务出错了，数据库居然更新不了

- [~~yii2-cron~~](https://www.yiiframework.com/extension/vasadibt/yii2-cron): 定时任务插件，`migrate`命令为`./yii migrate --migrationPath=@vendor/vasadibt/cron/migrations`

- [Yii2 Cron Log Extension](https://github.com/yii2mod/yii2-cron-log): 定时任务的日志插件，上面两个定时任务插件都不好用，其实要创建定时任务，直接用创建一个命令工具就可以了，可以借助这个插件把执行记录放入数据库即可

  1. 执行`./yii migrate/up --migrationPath=@vendor/yii2mod/yii2-cron-log/migrations`创建命令日志表

  2. 在`console`的配置中添加:

     ```php
     'components' => [
         'errorHandler' => [
             'class' => 'yii2mod\cron\components\ErrorHandler',
         ],
         'mutex' => [
             'class' => 'yii\mutex\FileMutex'
         ],
     ],
     ```

  3. 在我们要执行的console controller里面这样定义:

     ```php
     public function behaviors()
     {
       return [
         'cronLogger' => [
           'class' => 'yii2mod\cron\behaviors\CronLoggerBehavior',
           'actions' => ['index']
         ],
         // Example of usage the `MutexConsoleCommandBehavior`
         'mutexBehavior' => [
           'class' => 'yii2mod\cron\behaviors\MutexConsoleCommandBehavior',
           'mutexActions' => ['index'],
           'timeout' => 3600, //default 0
         ]
       ];
     }
     ```

  4. 这样只要执行了`./yii test`，这里的test默认值`console -> TestController.php -> actionIndex` 方法，这样就能记录到日志里面去了，如果要定时执行，直接借助unix的crontab即可

  
