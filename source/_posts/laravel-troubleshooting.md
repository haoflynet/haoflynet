---
title: "Laravel 相关故障解决"
date: 2020-08-15 16:02:39
updated: 2022-06-10 14:18:00
categories: php
---

#### 禁用csrf认证

##### 全局禁用csrf

在`app/Http/Kernel.php`中，`$middleware`表示全局中间件，而`$routeMiddleware`表示针对某个路由的中间件，所以只需要把csrf在`$middleware`中注释掉，然后在`$routeMiddleware`中添加`'csrf' => 'App\Http\Middleware\VerifyCsrfToken'`
如果要在某个路由上使用就这样：

```php
Route::group(['middleware' => 'csrf'], function(){     // csrf保护的接口
	Route::get('/', 'HomeController@index');
}
```

##### 针对某几个接口单独禁用csrf

可以在`app/Http/Middleware/VerifyCsrfToken`的`$except`添加，但是这里的添加只能以正则的方式来匹配，不能使用路由别名，如果路由中有参数可以用星号代替

```php
protected $except = [
 	'webhook/*',
  'users/*/profile'
];
```

####  一个页面调用多个接口如何传递CSRF Token

由于`csrf`的`_token`是存储于session的，依照`laravel`的实现机制，同一时间只能有一个`_token`，所以无法实现一个页面设置多个`csrf token`，要解决这个问题要么将非必要的接口忽略`csrf`，要么每次请求`api`后从后台生成并返回一个新的`token`

<!--more-->

#### 处理上传文件

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

#### 存储base64图片

```php
$format = '.png';
if (Str::startsWith($base64, 'data:image/jpeg')) {
  $format = '.jpg';
} else if (Str::startsWith($base64, 'data:image/x-icon')) {
  $format = '.ico';
} else if (Str::startsWith($base64, 'data:image/gif')) {
  $format = '.gif';
}

$safeName = Str::random(10) . '_' . time() . $format;
Storage::disk($disk)->put($path . $safeName, base64_decode(explode(',', $base64)[1]));
$url = Storage::disk('s3-public')->url($path . $safeName);
```

#### 手动清理配置缓存 

`php artisan config:cache`

#### 插入数据的时候出现`MassAssignmentException in Laravel`错误

需要给数据表设置可访问的字段，在Model里面

```php
protected $fillable = array('字段1', '字段2');
```

#### php artisan db:seed出现`[ReflectionException] Claxx XXXTableSeeder dows not exist`错误
这是因为新增加了文件但是composer没有感知到，需要先执行`composer dump-autoload`

#### 定义/修改字段类型为timestamp时出现错误:"Unknown column type "timestamp" requested."
按照[[How do I make doctrine support timestamp columns?](http://stackoverflow.com/questions/34774628/how-do-i-make-doctrine-support-timestamp-columns)]的做法，目前最简单的方式是直接用`DB::statement()`来写SQL语句

#### POST数据的时候出现`The payload is invalid`

我遇到这个情况是因为在做复杂的表单提交，直接提取`X-XSRF-TOKEN`的值，但是由于没有转移，导致后端token揭秘失败

#### 保存model的时候出现错误：`Missing argument 2 for Illuminate\Database\Eloquent\Model::setAttribute()`

一般是`Model`的几个属性没有设正确，检查这几个值`incrementing/timestamps/primarykey/fillable`

#### 队列出现Cannot initialize a MULTI\/EXEC transaction over aggregate connections

升级到最新版laravel吧，然后将redis的扩展切换到phpredis，`laravel5.3`之前自带的`predis`不支持redis的sentinel，并且有些redis操作强依赖于predis的事务操作，各种纠结，最后都不能成功。或者自己[写类似的中间件](https://github.com/cooperaj/laravel-redis-sentinel)

#### Class 'Symfony\Bridge\PsrHttpMessage\Factory\HttpFoundationFactory' not found

偶尔安装了某些个第三方库会出现这种幺蛾子，可以用这种方式解决`composer require symfony/psr-http-message-bridge`

#### 更新表时出现`AH00052: child pid 71 exit signal Segmentation fault (11)`

原因可能是没有设置主键而直接在该表上面更新数据，导致ORM不知道到底该更新谁。并且Laravel不支持复合主键(https://github.com/laravel/framework/issues/5517，作者不支持这种做法)。这种情况，要么给该表添加唯一主键，要么只能用where直接更新了。

#### Error while reading line from server

 `Predis`需要设置`read_write_timeout=0`或者-1，特别是daemon任务，最好设置不超时

#### `PHP Fatal error:  Uncaught exception 'ReflectionException' with message 'Class log does not exist' in /Users/freek/dev/laravel/vendor/laravel/framework/src/Illuminate/Container/Container.php`

出现于5.2版本中，原因是`.env`文件中的配置的值，中间存在空格，如果中间有空格，需要将值用双引号包起来

#### Class env does not exist / Class request does not exist

通常出现在框架还未加载完成就报错，但是在处理错误的时候却使用了`env()/request()`这个功能，导致没有打印真实的错误。处理方式，一是不要使用`app()->environment('...')`，而是检查`.env`文件中是否有错误，例如包含空格的值，必须用双引号包围。我在自定义`ExceptionHandler`中遇到过几次

#### env('xxxx') 总是返回空

原因是缓存了配置，需要注意的是，如果使用了`config:cache`，那么配置必须是在配置文件夹`config`中使用`env`才能调用，如果里面没有定义，在外面直接使用，那么总是返回`null`

#### The given data failed to pass validation

认证出错却不知道具体错在哪里并且状态码是500，如果有用`Dingo API`，那么注意`Request`不要继承`use Illuminate\Foundation\Http\FormRequest`而应该是`use Dingo\Api\Http\FormRequest`

#### Call to undefined method setHidden

注意command的主逻辑不是`fire`而应该是`handle`

#### 启动时报错Unknown: failed to open stream: No such file or directory in Unknown on line 0

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

#### composer install时报错: Please provide a valid cache path

需要手动创建缓存目录，在`storage/framwork`下面新建`sessions`、`views`、`cache`文件夹即可

#### Larave 413 Request Entity Too Large

如果有用web服务器，那么查看nginx或者apache的文件上传限制，如果直接用的`php artisan serve`，那么修改`php.ini`的`upload_max_filesize`和`post_max_size`值

#### Laravel强制开启HTTPS，强制更换设置APP_URL

目前有个需求是为本地`localhost`开启`https`支持，用`nginx`支持`ssl`，但是程序依然用`php artisan serve`启动。首先我的`nginx`是在容器中的，所以在`nginx`的`proxy_pass`应该设置为主机内网IP的地址，然后`php artisan serve --host=0.0.0.0`，程序中的`APP_URL`虽然设置为了`https://localhost`，但是程序中的`URL/ASSET`函数依然会将`url`设置为`http://192.168.1.2`开头的形式，这时候需要在`AppServiceProvider`的`boot`方法中添加如下设置进行强制更换:

```php
\Illuminate\Support\Facades\URL::forceScheme('https');
\Illuminate\Support\Facades\URL::forceRootUrl('https://localhost');
```

#### Laravel migrate出现错误: No such file or directory (SQL: create table `migrations`)

可以尝试清除一下配置，`php artisan config:clear && php artisan migrate:install`

#### 改变默认的asset函数行为

默认的asset函数为框架的内置函数，无法直接改变，可以在`app/Http/helpers.php`中自定义另外一个函数来封装一下，这样也可以全局使用了，例如:

```php
function my_asset($path, $secure = null){
    return 'https://cloudinary.com/' . asset($path, $secure);
}
```

#### oauth-private.key does not exist or is not readable

重新生成一下密钥文件: `php artisan passport:keys`，如果这种方法仍然不行，需要在`storage`目录下新建`oauth-private.key`和`oauth-public.key`文件，内容为空就行，然后执行` php artisan passport:install --force`重新生成

#### PackageManifest.php: Undefined index: name

尝试删除`vendor`和`composer.lock`，然后重新`composer install`

#### No Application Encryption Key Has Been Specified

尝试执行`php artisan key:generate`

#### Invalid request (Unsupported SSL request)

出现这种情况是因为开启了强制HTTPS，要么取消这个限制(搜索'HTTPS'字符串即可找到位置)，要么启用HTTPS

#### Replicating claims as headers is deprecated and will removed from v4.0. Please manually set the header if you need it replicated.

具体原因不知道为啥，反正应该是`laravel/passport`和新版本的`lcobucci/jwt`有冲突，降级后者的版本可以解决: `composer require lcobucci/jwt=3.3.3`

#### 从url保存文件到文件系统

- 只能先下载下来

```php
$info = pathinfo($request->get('url'));
$url = explode('/', $request->get('url'));
$url[count($url) - 1] = urlencode($url[count($url) - 1]);	// 可能需要对url后面文件部分做一下urlencode
$contents = file_get_contents(implode('/', $url));
$file = '/tmp/' . $info['basename'];
file_put_contents($file, $contents);
$uploaded_file = new UploadedFile($file, $info['basename']);
$path = $uploaded_file->storeAs('mypath', $info['basename']);
```

#### throttle的设置在passport /oauth/token不起作用

原因是throttle如果在`kernel.php`中设置的，那他只作用于自己写的API，对于passport中的api不起作用，可以在`AuthServiceProvider.php -> boot` 注册Passport的时候覆盖其设置:

```php
public function boot()
{
  ...
    Passport::routes(function ($router) {
      $router->all();
      Route::post('/token', [
        'uses' => 'AccessTokenController@issueToken',
        'as' => 'passport.token',
        'middleware' => 'throttle:3000,1'
      ]);
    });
}
```

#### Illegal operator and value combination

一般是因为在where条件中比较时间字段的时候传入了一个null值
