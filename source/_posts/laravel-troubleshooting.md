---
title: "Laravel 相关故障解决"
date: 2020-08-15 16:02:39
categories: php
---

##### 禁止全局csrf认证

在`app/Http/Kernel.php`中，`$middleware`表示全局中间件，而`$routeMiddleware`表示针对某个路由的中间件，所以只需要把csrf在`$middleware`中注释掉，然后在`$routeMiddleware`中添加`'csrf' => 'App\Http\Middleware\VerifyCsrfToken'`
如果要在某个路由上使用就这样：

	Route::group(['middleware' => 'csrf'], function(){     // csrf保护的接口
		Route::get('/', 'HomeController@index');
	}

<!--more-->

##### 处理上传文件

```php
$file = Input::file('upload_file");// 获取上传文件对象
$file->isValid()                   // 检验文件是否有效
$file->getClientOriginalName();    // 获取文件原名
$file->getFileName();              // 获取上传后缓存的文件的名字
$file->getRealPath();              // 获取缓存文件的绝对路径
$file->getClientOriginalExtension();// 获取上传文件的后缀
$file->getMimeType();              // 获取上传文件的MIME类型
$file->getSize();                  // 获取上传文件的大小
```

##### 手动清理配置缓存 

`php artisan config:cache`

##### 插入数据的时候出现`MassAssignmentException in Laravel`错误

需要给数据表设置可访问的字段，在Model里面

	protected $fillable = array('字段1', '字段2');

##### php artisan db:seed出现`[ReflectionException] Claxx XXXTableSeeder dows not exist`错误
这是因为新增加了文件但是composer没有感知到，需要先执行`composer dump-autoload`

##### 定义/修改字段类型为timestamp时出现错误:"Unknown column type "timestamp" requested."
按照[[How do I make doctrine support timestamp columns?](http://stackoverflow.com/questions/34774628/how-do-i-make-doctrine-support-timestamp-columns)]的做法，目前最简单的方式是直接用`DB::statement()`来写SQL语句

##### POST数据的时候出现`The payload is invalid`

我遇到这个情况是因为在做复杂的表单提交，直接提取`X-XSRF-TOKEN`的值，但是由于没有转移，导致后端token揭秘失败

##### 保存model的时候出现错误：`Missing argument 2 for Illuminate\Database\Eloquent\Model::setAttribute()`

一般是`Model`的几个属性没有设正确，检查这几个值`incrementing/timestamps/primarykey/fillable`

##### 队列出现Cannot initialize a MULTI\/EXEC transaction over aggregate connections

升级到最新版laravel吧，然后将redis的扩展切换到phpredis，`laravel5.3`之前自带的`predis`不支持redis的sentinel，并且有些redis操作强依赖于predis的事务操作，各种纠结，最后都不能成功。或者自己[写类似的中间件](https://github.com/cooperaj/laravel-redis-sentinel)

##### Class 'Symfony\Bridge\PsrHttpMessage\Factory\HttpFoundationFactory' not found

偶尔安装了某些个第三方库会出现这种幺蛾子，可以用这种方式解决`composer require symfony/psr-http-message-bridge`

##### 更新表时出现`AH00052: child pid 71 exit signal Segmentation fault (11)`

原因可能是没有设置主键而直接在该表上面更新数据，导致ORM不知道到底该更新谁。并且Laravel不支持复合主键(https://github.com/laravel/framework/issues/5517，作者不支持这种做法)。这种情况，要么给该表添加唯一主键，要么只能用where直接更新了。

##### Error while reading line from server

 `Predis`需要设置`read_write_timeout=0`或者-1，特别是daemon任务，最好设置不超时

##### `PHP Fatal error:  Uncaught exception 'ReflectionException' with message 'Class log does not exist' in /Users/freek/dev/laravel/vendor/laravel/framework/src/Illuminate/Container/Container.php`

出现于5.2版本中，原因是`.env`文件中的配置的值，中间存在空格，如果中间有空格，需要将值用双引号包起来

##### Class env does not exist / Class request does not exist

通常出现在框架还未加载完成就报错，但是在处理错误的时候却使用了`env()/request()`这个功能，导致没有打印真实的错误。处理方式，一是不要使用`app()->environment('...')`，而是检查`.env`文件中是否有错误，例如包含空格的值，必须用双引号包围。我在自定义`ExceptionHandler`中遇到过几次

##### The given data failed to pass validation

认证出错却不知道具体错在哪里并且状态码是500，如果有用`Dingo API`，那么注意`Request`不要继承`use Illuminate\Foundation\Http\FormRequest`而应该是`use Dingo\Api\Http\FormRequest`

##### Call to undefined method setHidden

注意command的主逻辑不是`fire`而应该是`handle`

##### 启动时报错Unknown: failed to open stream: No such file or directory in Unknown on line 0

可能是错误地删除了`server.php`文件，可以直接自己写一个:

```php
<?php
/**
 * Laravel - A PHP Framework For Web Artisans
 *
 * @package  Laravel
 * @author   Taylor Otwell <taylor@laravel.com>
 */

$uri = urldecode(
    parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)
);

// This file allows us to emulate Apache's "mod_rewrite" functionality from the
// built-in PHP web server. This provides a convenient way to test a Laravel
// application without having installed a "real" web server software here.
if ($uri !== '/' && file_exists(__DIR__.'/public'.$uri)) {
    return false;
}

require_once __DIR__.'/public/index.php';

```

##### composer install时报错: Please provide a valid cache path

需要手动创建缓存目录，在`storage/framwork`下面新建`sessions`、`views`、`cache`文件夹即可