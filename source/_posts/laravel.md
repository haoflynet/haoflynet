---
title: "Laravel 手册"
date: 2014-12-12 11:02:39
updated: 2021-03-09 13:58:00
categories: php
---
# Laravel指南
[Laravel项目基本结构](https://github.com/haoflynet/project-structure/blob/master/Laravel/README.md)

十分推荐安装[laravel-ide-helper](https://github.com/barryvdh/laravel-ide-helper)

### 配置

- `.env`文件中，如果有空格，那么值需要用双引号包围，并且里面如果用`\n`，那么必须转义`\\n`
- laravel可以根据不同的系统环境自动选择不同的配置文件，例如，如果`APP_ENV=testing`，那么会自动选择读取`.env.testing`中的配置，如果有`.env`则会被覆盖，特别是单元测试和`artisan`命令中

Laravel的主配置文件将经常用到的文件集中到了根目录下的`.env`目录下，这样更高效更安全。其内容如下：

<!--more-->

```tex
# 这里配置
APP_ENV=local

APP_DEBUG=true
APP_KEY=YboBwsQ0ymhwABoeRgtlPE6ScqSzeWZG

# 这里配置数据库
DB_HOST=localhost
DB_DATABASE=test
DB_USERNAME=root
DB_PASSWORD=mysql

CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_DRIVER=sync

MAIL_DRIVER=smtp
MAIL_HOST=mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null

EXAMPLE_PUBLIC_KEY=abc\ndef	# 要在配置里面换行，目前只有这种方式了，在读取的时候这样子读取: str_replace("\\n", "\n", env('MSGCENTER_PUBLIC_KEY'))

ARRAY={"slave":[{"host":"127.0.0.1","port":3306},{"host":"127.0.0.1","port":3307}]}	# 目前配置文件也不支持数据，也只能这样，然后在使用的时候用json转换一下了json_decode($a, true)['slave']
```

还可以在该文件里配置其它的变量，然后在其它地方使用`env(name, default)`即可访问。例如，读取数据库可以用`config('database.redis.default.timeout', -1)`来。
全局配置文件`.env`仅仅是一些常量的配置，而真正具体到哪个模块的配置则是在`config`目录之下.同样，也可以动态改变配置:`Config::set('database.redis.default.timeout')`

另外，可以通过帮助函数来获取当前的应用环境:

```php
# 获取的是.env里面APP_ENV的值
$environment = App::environment();
App::environment('local')	// true/false
app()->environment()
```

### 控制器

- laravel可以直接通过命令创建一个控制器:
  `php artisan make:controller HomeController`，然后就会有这么一个控制器文件了:`app/Http/Controllers/HomeController.php`

- 重定向到控制器方法中

  ```php
  return redirect()->action('HomeController@index', ['page' => 123])
  ```


#### [Laravel 数据校验/验证Validation](https://haofly.net/laravel-validation)

#### Restful资源控制器

- 资源控制器可以让你快捷的创建 RESTful 控制器

- 通过命令`php artisan make:controller PhotoController --resource`创建一个资源控制器，这样会在控制器`PhotoController.php`里面包含预定义的一些Restful的方法
  `Route::resource('photo', 'PhotoController')`;
- 通过命令`php artisan make:controller PhotoController --resource --model=Photo`可以直接将其与Model绑定

```php
Route::resource('photo', 'PhotoController', ['only' => ['index', 'show']]);	// 仅暴露某几个路由
Route::resource('photo', 'PhotoController', ['except' => ['create', 'store']]); // 排除指定路由
Route::apiResource('photo', 'PhotoController');	// API路由，和resource差不多，只是少了create和edit几个和HTML有关的路由
Route::resource('photo', 'PhotoController', ['names' => [
  'create' => 'photo.createa'	// 资源路由命名
]])


# 嵌套资源控制器
Route::resource('photos.comments', 'PhotoCommentController');
# 这样可以直接通过这样的URL进行访问photos/{photos}/comments/{comments}
# 控制器只需要这样子定义即可
public function show($photoId, $commentId)
```

##### 资源控制器对应的路由

| Verb      | URI                  | Action  | Route Name     |
| --------- | -------------------- | ------- | -------------- |
| GET       | /photos              | index   | photos.index   |
| GET       | /photos/create       | create  | photos.create  |
| POST      | /photos              | store   | photos.store   |
| GET       | /photos/{photo}      | show    | photos.show    |
| GET       | /photos/{photo}/edit | edit    | photos.edit    |
| PUT/PATCH | /photos/{photo}      | update  | photos.update  |
| DELETE    | /photos/{photo}      | destroy | photos.destroy |

## Resources目录

`resource`目录包含了视图`views`和未编译的资源文件(如LESS、SASS或javascript)，还包括语言文件`lang`

### 路由url

路由缓存：laravel里面使用`route:cache Artisan`，可以加速控制器的路由表，而且性能提升非常显著。

```php
# 路由分组，第一个属性则是下面所有路由共有的属性
Route::group(['namespace' => 'Cron', 'middleware' => ['foo', 'bar']], function()
{
    Route::get('/', function()
    {
        // App\Http\Controllers\Cron
    });

    Route::get('user/profile', function()
    {
        // Has Foo And Bar Middleware
    });

});

# 通过url向控制器传递参数
Route::resource('wei/{who}', 'WeixinController');
#然后在控制器里这样定义
public function index($who){}

# 嵌套资源控制器
# 例如
Route::resource('photos.comments', 'PhotoCommentController');
# 这样可以直接通过这样的URL进行访问photos/{photos}/comments/{comments}
# 控制器只需要这样子定义即可
public function show($photoId, $commentId)
# 如果要获取嵌套资源的url，可以这样子:
route('post.comment.store', ['id'=> 12]) # 这样子就获取到id为12的post的comment的创建接口地址
  
# 通配路由
Route::get('/{abc}', 'TestController@test');	// 会匹配所有之前路由匹配不到的路由，但是这样做可能会将nova等路由包含进来，如果想让这样的通配路由排除某些路由可以在app/Providers/RouteServiceProvider.php中添加排除
public function boot() {
  Route::pattern('abc', '^(?backend|nova-api|nova|nova-vendor).[a-zA-Z0-9-_\/]+$]');
  parent::route();
}
```

#### 路由相关方法

```php
# 获取当前页面的地址
URL::full();
url()->full();	// https://haofly.net/laravel?test=1
URL::current();	// https://haofly.net/laravel
url()->current();
Request::url();	// https://haofly.net/laravel
$request->url();
Request::path();	// laravel
$request->path();
Request::getRequestUri();	// /laravel
$request->getRequestUri();
Request::getUri();	// https://haofly.net/laravel
$request->getUri();

# 获取当前页面的路由名称(即使带参数也没问题)
Route::currentRouteName() === 'businessEditView'

# 获取前一个页面的地址
URL::previous()
url()->previous();

Request::url();
```

### [Laravel Blade模板引擎](https://haofly.net/laravel-blade)

#### 分页

Larvel的分页主要靠Eloquent来实现，如果要获取所有的，那么直接把参数写成`PHP_INT_MAX`就行了嘛

```php
# 动态设置页
$request->merge(['page' => 2]);	// 最方便的
Paginator::currentPagesolver(function () use ($currentPage) {return $currentPage}); # 动态改变paginator获取page的方式，全局搜索可以发现它就是从request参数获取的page
$users = User::where('age', 20)->paginate(20);	// 表示每页为20条，不用去获取页面是第几页，laravel会自动在url后面添加page参数，并且paginate能自动获取，最后的结果，用json格式显示就是
{
  'total': 50,
  'per_page': 20,
  'current_page': 1,
  'last_page': 3,
  'next_page_url': '...',
  'prev_page_url': null,
  'from': 1,
  'to': 15,
  'data': [{}, {}]
}

# 如果是在数据库关系中进行分页可以直接在Model里面鞋
public function ...(){
  return $this->posts()->paginate(20);
}

# 获取all的分页数据，不用::all()，而是
User::paginate(20) # 直接用paginate
```

### 数据库Model

Laravel提供了migration和seeding为数据库的迁移和填充提供了方便，可以让团队在修改数据库的同时，保持彼此的进度，将建表语句及填充操作写在laravel框架文件里面并，使用migration来控制数据库版本，再配合Artisan命令，比单独管理数据库要方便得多。

#### 配置文件

`config/database.php`里面进行数据库引擎的选择，数据库能通过`prefix`变量统一进行前缀的配置

数据库读写分离的配置(Laravel的读写分离仅仅是读写分离，在主库故障以后，程序无论是读写都会报连接错误，因为在程序启动的时候建立数据库连接默认都会建立一个写连接，又是一个坑)，如果要解决这个问题，可以使用`zara-4/laravel-lazy-mysql`，它原本是为解决主库连接慢而创造的，但是也能填这个坑。不过，另一方面，DBA必须保证主库的高可用，开发人员是可以不用考虑这一层面的，这是DBA的责任，而不是开发人员的责任，主库挂了，DBA应该立马用新的主库代替。

对于多`slave`的配置，网上的教程感觉都有问题，看了下源码，正确的配置多读库并且几个读库的配置不一样，那么需要这样配置

```php
'mysql' => [
  'driver'    => 'mysql',
  'database'  => 'test',
  'username'  => 'root',
  'password'  => 'password',
  'charset'   => 'utf8',
  'collation' => 'utf8_unicode_ci',
  'strict' => false,	// MySQL数据库严格模式，开启后，如果没有默认值会报错，不开启会自动填充一个默认值
  'read' => [
    [
      'host' => '127.0.0.2',
      'port' => 3307
    ],
    [
      'host' => '127.0.0.3',
      'port' => 3308
    ]
  ],
  'write' => [
    'host' => '127.0.0.1',
    'port' => 3306,
  ]
],
```

#### 建表操作

生成一个model: `php artisan make:model user -m`，这样会在`app`目录下新建一个和user表对应的model文件

```php
<?php
namespace App;
use Illuminate\Database\Eloquent\Model;
class Flight extends Model
{
    //
}
```
加上`-m`参数是为了直接在`database/migrations`目录下生成其迁移文件，对数据库表结构的修改都在此文件里面，命名类似`2016_07_04_051936_create_users_table`，对数据表的定义也在这个地方，默认会按照复数来定义表名:


```php
<?php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateApplicationsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('applications', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
        });
        DB::statement('ALTER TABLE `'.DB::getTablePrefix().'applications` comment "这里写表的备注"');
      DB::table('users'->insert([]));	// 可以直接在migrate的时候进行插入操作
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('applications');
    }
}
```

当数据表定义完成过后，执行`php artisan migrate`即可在真的数据库建表了

```shell
php artisan make:migration 操作名	# 生成迁移文件
php artisan schema:dump	# 从数据库已有的表生成迁移文件
php artisan migrate				# 建表操作，运行未提交的迁移
php artisan migrate --path=databases/migrations/				# 运行指定目录下的迁移，这里无法指定具体文件，只能指定文件夹
php artisan migrate:rollback 	# 回滚最后一次的迁移
php artisan migrate:reset		# 回滚所有迁移
php artisan migrate:refresh   	# 回滚所有迁移并重新运行所有迁移
```

如果要修改原有model，不能直接在原来的migrate文件上面改动，而是应该新建修改migration，例如，执行`php artisan make:migration add_abc_to_user_table`这样会新建一个迁移文件，修改语句写在up函数里面:

```php
public function up()
{
    Schema::table('users', function (Blueprint $table) {
        $table->string('mobile', 20)
          ->nullable()
          ->after('user_face')
          ->comment('电话号码')
          ->default('')
          ->change();  // 将mobile字段修改为nullable并且放在user_face字段后面，主要就是在后面加上change()方法
      	$table->renameColumn('from', 'to');	// 重命名字段
      	$table->dropColumn('votes');		// 删除字段
      	$table->dropColumn(['votes', 'from']);// 删除多个字段
      	$table->string('email')->unique();	// 创建索引字段
      	$table->unique('email');			// 创建唯一索引
      	$table->unique('email', 'nickname');	// 联合唯一索引
      	$table->index(['email', 'name']);		// 创建复合索引
      	$table->dropPrimary('users_id_primary');	// 移除主键
      	$table->dropUnique('users_email_unique');	// 移除唯一索引
      	$table->dropIndex('geo_state_index');		// 移除基本索引
      	$table->json('movies')->default(new Expression('(JSON_ARRAY())')); // 使用表达式
      	$table->timestamp('created_at')->useCurrent();	// 使用当前时间
        $table->timestamp('updated_at')->useCurrentOnUpdate(); // 更新时间
      	$table->timestamp('deleted_at')->nullable();
    });
  
  # 其他相关语法
  Schema::hasTable('users'); // 是否存在某个表
  Schema::hasColumn('users', 'email');	// 是否存在某个列
  Shcema::rename($from, $to);	// 重命名表
  Schema::drop('users');	// drop 表
  Schema::dropIfExists('users');	// drop表
}
```

#### 表/Model的定义

```php
class User extends Model{
  public $timestamps = false;			// 设置该表不需要使用时间戳，updated_at和created_at字段。deleted_at是用use SoftDeletes去控制的
  protected $primaryKey = 'typeid'		// 不以id为主键的时候需要单独设置，需要注意的是laravel以及其他很多orm都不支持复合主键，可能会出现"Segment Fault"
  protected $primaryKey = null;			// 没有主键的情况
  public $incrementing	= false;	// 不使用自增主键，特别注意有非自增的id列，如果没写这个获取到的id会不一样
  protected $connection = 'second';		// 设置为非默认的那个数据库连接
  protected $fillable = ['id', 'name']; // 设置可直接通过->访问或者直接提交保存的字段
  protected $table = 'my_flights';		// 自定义表明，默认的表明会以model的复数形式，需要注意的是，英语单词复数的变化有所不同，如果取错了表明活着以中文拼音作为表明，有时候就需要明确表的名称了
  protected $appends = ['id2'];	// 有时候在转换模型到数组时，希望增加一个数据库不存在的字段，可以用这种方式增加，例如 ->toArray方法，->attributesToArray()方法，->toJson()方法
  protected $visible = ['id']; // 转换为数组的时候限制某些字段可见
  protected $hidden = ['password'];
}
```

#### 字段的定义

```php
# 字段定义
$table->increments('id')	# 默认都有的自增的主键
$table->string('name', 45)->comment('名字') # 字符串类型,添加注释，长度可指明也可不指名
$table->boolean('type') 	# 相当于tinyint(1)
$table->softDeletes()    # 软删除，名为deleted_at类型为timestamp的软删除字段
$table->bigInteger('')	# bigint(20),加不加sign都是20
$table->integer()	# int(10)
$table->integer()->uninsign()	# int(11)
$table->integer()->unsigned()	# int(10)
$table->mediumInteger('')	# int(9)
$table->mediumInteger('')->unsign()	# int(9)
$table->mediumInteger('')->unsigned()
# 相当于int(8)
$table->smallInteger('') # smallint(6)
$table->smallInteger('')->unsign() # smallint(6)
$table->smallInteger('')->unsigned() # smallint(5)
$table->tinyInteger('') # tinyint(4)
$table->tinyInteger('')->unsign() # tinyint(4)
$table->tinyInteger('')->unsigned() # tinyint(1)

$table->float('')	# 相当于DOUBLE

$table->text('')	# text()

$table->dateTime('created_at')  # DATETIME类型

# 字段属性
->nullable()	# 允许null
->unsigned()	# 无符号，如果是integer就是int(10)
->unsign()	# 无符号，如果是integer就是int(11)
->default('')	# 默认值
	
# 索引定义
$table->index('user_id')

# 主键定义
$table->primary('id')  # 默认不用写这个
$table->primary(array('id', 'name')) # 多个主键的情况

# 外键定义
$table->integer('user_id')->unsigned();	# 先要有一个字段，而且必须是unsigned的integer
$table->foreign('user_id')->references('id')->on('users');	# 关联到users表的id字段
```

#### 定义表之间的关系

- 直接在ORM里面进行表关系的定义，可以方便查询操作
- 5.4开始新增了`withDefault`方法，在定义关系的时候，如果对象找不到那么返回一个空对象，而不是一个null

##### 一对多hasMany

```php
public function posts(){
	return $this->hasMany('App\Post');
}
# 可以这样使用
Users::find(1)->posts

# 指定外键
$this->hasMany('App\Post', 'foreign_key', 'local_key')
```
##### 一对一hasOne

```php
public function father(){
	return $this->hasOne('App\Father');
}

$this->hasOne('App\Father', 'id', 'father');	# 表示father的id对应本表的father
```
##### 相对关联belongsTo(多对一)

```php
public function user(){
	return $this->belongsTo('App\User');
	// return $this->belongsTo('App\User')->withDefault();	// 这样子如果找不到关联对象，则会返回一个空对象
	// return $this->belongsTo('App\User')->withDefault(['name' => '不知道'] ); // 还可以给这个空对象赋予默认值
}
Posts::find(1)->user  # 可以找到作者
```
##### 多对多关系belongsToMany

如果有三张表，users,roles,role_user其中，role_user表示users和roles之间的多对多关系。如果要通过user直接查出来其roles，那么可以这样子

```php
class User extends Model {
  public funciton roles()
  {
    return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'foo_id');	# 其中user_roles是自定义的关联表表名，user_id是关联表里面的user_id，foo_id是关联表里面的role_id
  }
}

$roles = User::find(1)->roles;	# 这样可以直接查出来，如果想查出来roles也需要在roles里面进行定义

# 使用pivot查询中间表的信息
foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}

# 不过，如果中间表包含了额外的属性，在定义关系的时候需要使用withPivot显式指定，如果需要中间表自动维护时间字段需要加withTimestamps
return $this->belongsToMany(Role::class)->withPivot('field1', 'field2')->withTimestamps();


# 同步关联对象
$user->posts()->sync([1, 2, 3])	# 这样可以对关联表进行同步，多的关联会进行删除，没有的关联会进行添加，这样就不用在关联表进行先删除再插入的操作了
```
##### 多态关联

一个模型同时与多种模型相关联，可以一对多(morphMany)、一对一(morphOne)、多对多(mar)

例如: 三个实例，文章、评论、点赞，其中点赞可以针对文章和评论，点赞表里面有两个特殊的字段`target_id`、`target_type`，其中`target_type`表示对应的表的Model，`target_id`表示对应的表的主键值

```php
# 点赞Model
class Like extends Model {
  public function target() {
    return $this->morphTo(); // 如果主键不叫id，那么可以指定morphTo(null, null, 'target_uuid')最后这个参数是字段名哟
  }
}
// 文章Model
class Post extends Model {
  public function likes(){	# 获取文章所有的点赞
    return $this->morphMany('App\Like', 'target');
  }
}
// 评论Model
class Comment extends Model {
  public function likes() {	# 获取评论所有的点赞
    return $this->morphMany('App\Like', 'target');
  }
}

$comment->likes;
$comment->likes;


$this->morphedByMany('App\Models\Posts', 'target', 'table_name'); // 一种多对多关联的morphedby

```

#### 数据库填充

Laravel使用数据填充类来填充数据，在`app/database/seeds/DatabaseSeeder.php`中定义。可以在其中自定义一个填充类，但最
好以形式命名，如(默认填充类为DatabaseSeeder，只需要在该文件新建类即可，不是新建文件):

```php
class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run()
    {
        $this->call(UsersTableSeeder::class);
    }
}

class UsersTableSeeder extends Seeder
{
    /**
     * Run the user seeds.
     */
    public function run()
    {
        DB::table('users')->delete();

        App\User::create([
            'email' => 'admin@haofly.net',
            'name' => '系统管理员',
        ]);
    }
}
```

然后在Composer的命令行里执行填充命令

```shell
php artisan db:seed
php artisan db:seed --class=UserTableSeeder	# 执行指定的seed
php artisan migrate:refresh --seed    # 回滚数据库并重新运行所有的填充
```

#### ORM操作

Laravel 查询构建器使用 PDO 参数绑定来避免 SQL 注入攻击，不再需要过滤以绑定方式传递的字符串。但是需要注意的是**当使用`whereRaw/selectRaw`等能嵌入原生语句的时候，要么用bind的方式(即将用户输入作为第二个参数传入)要么就对输入的字符进行严格的过滤**

```php
DB::statement('drop table xxx');	# 直接执行原生sql语句
DB::select('select xxx');	# 如果要获取结果的原生语句可以这样

# 数据库信息获取
## 获取查询SQL
DB::connection('default')->enableQueryLog(); # 如果不指定连接可以直接DB::enableQueryLog()
... # ORM操作
dd(DB::connection('statistics')->getQueryLog()); # 打印sql

DB::getTablePrefix();		# 获取数据表前缀
$user->getTable();			# 获取数据表名称，不带前缀的

# 查询
User::all();						# 取出所有记录
User::all(array('id', 'name'));  # 取出某几个字段
User::find(1);					# 根据主键取出一条数据
User::find([1,2,3]);			# 能一次查询多个
optional(User::find(1))->id;		# 如果user未找到，那么这条语句不会报错，同样返回null，5.5
User::findOrFail(1);				# 根据主键取出一条数据或者抛出异常
User::where([
  ['id', 1],
  ['name', 'haofly']
);			# where语句能够传递一个数组
User::where();					# 如果不加->get()或者其他的是不会真正查询数据库的，所以可以用这种方式来拼接，例如$a_where=User::where();$result =$a_where->where()->get();
User::where('field', 'like', '%test%');	# 模糊搜索
User::where('field', 'like', '%{$keyword}%');	# 直接传入变量
User::where('field', 'regexp', 'abc');	# 正则搜索
User::where()->limit(2);				# limit限制
User::whereIn('name', ['hao', 'fly']);	# in查询
User::whereNull('name');			# is null
User::whereNotNull('name');		# is not null
User::whereBetween('score', [1, 100]);	# where between
User::whereNotBetween('score', [1, 100]);	# where not between
User::whereDate('created_at', '2017-05-17');
User::whereMonth('created_at', '5');
User::whereDay('created_at', '17');
User::whereYear('created_at', '2017');
User::whereRaw('name="wang" and LENGT(name) > 1'); # 当有复杂点的where语句或者想直接写在mysql里面的那样的where语句，可以直接这样写
User::whereColumn('first_field', 'second_field');	# 判断两个字段是否相等
User::where(...)->orWhere();		# or where，需要注意的是这里是和前面所有的where相or，并且后面的不会去判断deleted_at is null了
User::where('...')->orWhere(['a'=>1, 'b'=>2]);	# 同时添加多个
User::where()->firstOrFail()	# 查找第一个，找不到就抛异常
User::where('user_id', 1)->get()# 返回一个Collection对象
User::where(...)->first()		# 只取出第一个model对象
User::find(1)->logs->where(...)	# 关系中的结果也能用where等字句
User::->where('updated_at', '>=', date('Y-m-d H:i').':00')->where('updated_at', '<=', date('Y-m-d H:i').':59') 					# 按分钟数查询
User::find(1)->sum('money')		# 求和SUM
User::where(...)->get()->pluck('name')	# 只取某个字段的值，而不是每条记录取那一个字段，这是平铺的,这里的pluck针对的是一个Collection，注意，这里只能针对Collection，千万不要直接针对一个Model，这样只会取出那张表的第一条数据的那一列，需要注意的是这里是先get除了所有的记录，然后在Collection上面进行的pluck操作，如果想少去一点数据可以先用select()再用pluck
User::where(DB::raw('YEAR(created_at)'), $year); # 嵌套原生函数语句
User::modelKeys()	# 直接获取模型的主键集合(不是'id'为名字的主键都可以)
User::select('name')->where()	# 也是只取出某个字段，但是这里不是平铺的
User::where()->get(['id', 'name'])# 更简单的方法
User::where(...)->pluck('name')	# 这是取出单独的一个行的一个列，不再需要first
User::withTrashed()->where()	# 包括软删除了的一起查询
User::onlyTrashed()->where()	# 仅查找软删除了的
User::find(1)->posts			# 取出一对多关联，返回值为Collection
User::find(1)->posts()			# 取出一对多关联，返回值为hasMany
User::find(1)->posts->count()	# 判断关联属性是否存在stackoverflow上面用的这种方法  
User::all()->orderBy('name', 'desc')	# 按降序排序
User::all()->latest()					# 按created_at排序
User::all()->oldest()					# 按created_at排序
User::all()->inRandomOrder()->first();	# 随机顺序
User::select('name')->distinct()->get()	# 去重
  
## 关联查询(这里的关联查询比较sql化，如果两张表有相同的字段，那么必须在前后的查询中都加上表名才能不发生错误，所以推荐使用has方法)
User::select('name')->join('posts', 'users.id', '=', 'posts.user_id')->where(...);	# Inner Join语法
User::select('name')->leftJoin('posts', 'users.id', '=', 'posts.user_id')->where(...);
User::select('name')->leftJoin('posts', 'users.id', '=', DB::raw('posts.user_id AND users.type=xxx'))->where(...);	# LEFT JOIN ON ... AND ...语法的简便写法
User::select('name')->leftJoin('posts', function($join) {
	$join->on('users.id', '=', 'posts.user_id')
        ->on('users.type', '=', 'xxx')
})	# LEFT JOIN ON ... AND ...语法的标准写法
    
# has语法，不会与Post的字段相冲突
$posts = Post::has('comments')->get();	# 获取所有有评论的posts
$posts = Post::has('comments', '>=', 3)->get();	# 获取评论数量大于3的
$posts = Post::has('comments.votes.user')->get();	# 嵌套has
$posts = Post::whereHas('comments', function($query) {
  $query->where('content', 'like', 'foo%')->whereHas('user');	# 比较复杂的has语法，whereHas也可以不带第二个参数
});  

# 访问器，如果在Model里面有定义这样的方法
public function getNameAttribute(){
  return $this->firstname.$this->lastname;
}
那么在外部可以直接$user->name进行访问

# 新增
Model::firstOrCreate()	# firstOrCreate的第二个参数是5.3才开始的
Model::firstOrNew()		# 与上面一句不同的是不会立马添加到数据库里，可以通过$object->new来判断是否是新添加的，如果该方法不存在那就用$object->exists判断是否已经存在于数据库中，这个方法是没有第二个参数的
Model::updateOrCreate(array(), array())
$User::find(1)->phones()->create([]) # 存在着关联的model可以直接新建，而且可以不指定那个字段，比如这里创建phone的时候不用指定user_id
$author->posts()->save($post);	# 添加hasone或者hasmany，不过这是针对新建的
$author->posts()->associate($post);	# 这是直接将外键设置为已经存在的一个posts
$author->posts()->saveMany([$post1, $post2])	# 添加hasmany
$post->author()->save(Author::find(1))	# 设置外键
$author->posts()->detach([1,2,3])
$author->posts()->attach([1,2,3=>['expires'=>$expires]])
$datas = [
  ['field1' => 'value1', 'field2' => 'value2'],
  ['field1' => 'value3', 'field2' => 'value4'],
];
Post::insert($datas);	// 批量创建并插入

# 修改
$user->restore();		# 恢复软删的数据
$user->fill(['name' => 'wang'])->save()	# fill必须save过后才会更新到数据库
$user->update(['name' => 'wang'])	# update会立即更新数据库
$user->increment('age', 5)	# 如果是数字类型，可以直接相加，不带5就表示之内加1
$user->decrement('age', 5)	# 或者减
$user->save(['timestamps'=>false]);	# save的参数可以阻止一些默认行为，比如这里阻止更新时间戳，就可以手动更改了
    
# 删除
$user->delete()	# 删除，如果设置了软删除则是软删除
$user->forceDelete()	# 无论是否设置软删除都物理删除
  
# 事务，注意数据库的连接问题
DB::beginTransaction();
DB::connection('another')->begintransaction();
DB::rollback();		# 5.1之前用的都是rollBack
DB::commit();
    
# 复制
$newUser = $user->replicate();$newUser->save();
  
# 特殊查询
User::whereRaw('FIND_IN_SET(region_id, abc)')	# 实现FIND_IN_SET
```

#### 查询缓存

##### With/load(预加载/渴求式加载/eager load)

- with/load在laravel的ORM中被称为预加载，作用与关联查询上，能有效缓解N+1查询问题
- 通常的做法是在一次请求开始处理的时候一次性把所有需要用到的关联关系取出来，例如: `Auth::user()->load('detail', 'posts:name', 'posts.comments')`

```php
# 例如要查询所有文章的作者的名字，以前是这样做的，总共查询了1+N次数据库
$posts = App\Post::all();
foreach($posts as $post) {
  var_dump($post->user->name);
}

# 如果使用with的话，就只需要查询两次，一次查询所有的文章，一次查询所有的书
# SELECT * FROM posts;
# SELECT * FROM books WHERE id in (...);
$posts = App\Post::with('user')->get();
foreach ( $books as $book) {
  var_dump($post->user->name);
}

# with还可以一次多加几张关联表
App\Post::with('user', 'author')->get();
# 嵌套使用
App\Post::with('user.phone')->get(); # 去除文章关联的用户信息，并取出用户关联的电话信息
# 预加载指定的列
App\Post::with('user:name,nickname')->get();
# 带条件的预加载
$users = User::with(['posts' => function ($query) {
  $query->where('title', '=', 'test')->orderBy('id', 'desc');	// eager load的orderby
}])->get();

# 而如果父模型已经被获取后，想要再使用预加载，就需要用load了
$posts = Post::all();
$posts->laod('user', 'category');
```

##### Cache

缓存的是结果

#### ORM对象方法

```php
# hasMany对象的查询
$posts = User::find(1)->posts()	# 返回hasMany对象，并未真正查询数据库
$posts = User::find(1)->posts	# 返回Collection对象，数据库的查询结果集
$posts->get()					# 返回Collection对象，数据库的查询结果集
```

##### Collection对象

```php
$obj->count()	# 计数
$obj->first()	# 取出第一个对象
$obj->last()	# 取出最后一个对象
$obj->isEmpty()	# 是否为空
```

#### Model对象的事件

可以在任何的`ServiceProvinder`的`boot`方法中针对`model`级别进行类似事件的回调，例如

```php
Post::updated(function ($post) {})	# 表示Post对象在updated以后需要做什么，例如forget一个缓存等
```

可供监听的事件有`updating/created/updating/updated/deleting/deleted/saving/saved/restoring/restored`。其中`updated`仅仅是字段的值真的变化了才会去更新。

#### DatabaseServiceProvider

Laravel自带一个特殊的`DatabaseServiceProvider`，用于管理数据库的连接，在`config/app.php`里面进行声明。

```php
Model::setConnectionResolver($this->app['db']);	// 这句话用于给模型设置connection resolver，传入一个DatabaseManager，用于管理数据库连接
```

### 认证相关

#### 授权Policy

Policy主要用于对用户的某个动作添加权限控制，这里的`Policy`并不是对`Controller`的权限控制.

权限的注册在`app/Providers/AuthServiceProvider.php`里面，权限的注册有两种:

```php
# 一种是直接在boot方法里面进行定义
class AuthServiceProvider extends ServiceProvider{
  public function boot(GateContract $gate) {
    $this->registerPolicies($gate);
    
    $gate->define('update-post', function($user, $post) {
      return $user->id === $post->user_id;		# 这样就添加了一个名为update-post的权限
    } )
      
    $gate->define('update-post', 'Class@method');	# 也可以这样指定回调函数
    
    $gate->before(function ($user, $ability) {		# before方法可以凌驾于所有的权限判断之上，如果它说可以就可以
      if ($user->isSuperAdmin())
        return true;
    });
    
    $gate->after(function() {})
  }
}

# 第二种是创建Policy类，可以用命令php artisan make:policy PostPolicy进行创建，会在Policies里面生成对应的权限类，当然，权限类创建完了后同样也需要将该类注册到AuthServiceProvider里面去，只需要在其$policies属性中定义就好了，例如
protected $policies = [
  Post::class => PostPolicy::class,		# 将权限类绑定到某个Model
];
# 权限类的定义:
class PostPolicy{
  public function before($user, $ability){		// 类似的before方法
    if ($user->isSuperAdmin()) {return true}
  }
  
  public function update(User $user, Post $post){
    return true;
  }
}
```

权限的使用

```php
# 控制器中使用
use Gate;
if (Gate::denies('update-post', $post)) {abort(403, 'Unauthorized action')}
Gate::forUser($user)->allows('update-post', $post) {}
Gate::define('delete-comment', function($user, $post, $comment){})	# 传递多个参数
Gate::allows('delete-comment', [$post, $comment])	# 也可这样传递多个参数
$user->cannot('update-post', $post)
$user->can('update-post', $post)
$user->can('update', $post)		# 无论你有好多个Policy，因为权限类是根据Model创建的，系统会自动定位到PostPolicy的update中去判断
$user->can('create', Post::class)	# 自动定位到某个model
@can('update-post', $post)		# 在模版中使用，如果是create可以这样@can('create', \App\Post::class)
  <html>
@endcan
@can('update-post', $post)
  <html1>
@else
  <html2>
@endcan
@can('create', \App\Post::class)				# Post的创建，针对PostPolicy
@can('create', [\App\Comment::class, $post])	# Comment的创建，针对CommentPolicy，并且应该这样子定义:public function create(User $user, $commentClassName, Project $project)
```

### Session/Cookie

```php
# 设置cookie
public function index()
{
  // 自动将cookie添加到响应
  Cookie::queue('test', 'value', 10);	
  return view('index');	
  
  // 或者在响应时带上cookie
  return view('index')->withCookie(
  	cookie('test', 'value', 10);	// 或者Cookie::make('test', 'value', 10)
  );
  // withCookies([cookie(...), cookie(...)])	或者直接添加多个cookie
}

# 设置未加密的cookie，需要用到EncryptCookies中间件，在app/Http/Middleware/EncryptCookies.php中添加如下内容
use Illuminate\Cookie\Middleware\EncryptCookies as BaseEncrypter;
class EncryptCookies extends BaseEncrypter
{
    protected $except = [
        'userid',
    ];
}

# 获取cookie
public function index(Request $request)
{
  $cookie = $request->cookie('test');
  $cookies = $request->cookie();
}

# 清除cookie
$cookie = Cookie::forget('test');
return view('index')->withCookie($cookie); # 其实是将该cookie的过期时间进行了更新，成为了过去时
```

### 任务队列Job

- 通过`php artisan make:job CronJob`新建队列任务，会在`app/Jobs`下新建一个任务
- 队列超时自动重试的配置在`config->queue.php->retry_after`中，最好设置成300，否则设置小了即使会成功也可能会超时生成一个失败的任务
- 失败的job默认会保存在数据库中的`failed_jobs`中

```php
# 队列里能够直接在构造函数进行注入，例如
public function __construct(ResourceService $resourceService){
  $this->resourceService = $resourceService;
}

# 任意地方使用队列
dispatch(new App\Jobs\PerformTask);

# 指定队列名称
$jog = (new App\Jobs\..)->onQueue('name');
dispatch($jog);

# 指定延迟时间
$job = (new App\Jobs\..)->delay(60);

Redis::zcard(sprintf('queues:%s:delayed', JobClass::NAME));	// 获取延迟队列任务数量

# 任务出错执行
public function failed()
{
	echo '失败了';
}

# 其他队列命令
php artisan queue:retry all	# 重试所有错误jobs
php artisan queue:retry 5	# 重试指定错误job
php artisan queue:forget 5	# 将某个job从错误表中移除
php artisan queue:flush		# 移除所有错误jobs    
```
#### 队列消费

- `queue:work`: 最推荐使用这种方式，它比`queue:listen`占用的资源少得多，不需要每次启动框架。但是代码如果更新就需要用`queue:restart`来重启

需要注意的是  

1. 不要在`Jobs`的构造函数里面使用数据库操作，最多在那里面定义一些传递过来的常量，否则队列会出错或者无响应  
2. job如果有异常，是不能被catch的，job只会重新尝试执行该任务，并且默认会不断尝试，可以在监听的时候指定最大尝试次数`--tries=3`
3. 不要将太大的对象放到队列里面去，否则会超占内存，有的对象本身就有几兆大小
4. 一个很大的坑是在5.4及以前，由于`queue:work`没有timeout参数，所以当它超过了队列配置中的`expire`时间后，会自动重试，但是不会销毁以前的进程，默认是60s，所以如果有耗时任务超过60s，那么队列很有可能在刚好1分钟的时候自动新建一条一模一样的任务，这就导致数据重复的情况。
5. 如果是使用redis作为队列，那么队列任务默认是是Job的NAME命名，例如
6. `queues:NAME`，是一个列表，过期时间为-1，没有消费者的情况是会一直存在于队列中。而如果是延迟执行的任务，则是单独放在一个有序集合中，其key为`queues:NAME:delayed`，其`score`值就是其执行的时间点。另外，`queues:NAME`存储的是未处理的任务，`queue:default:reserved`存储的是正在处理的任务，这是个有序集合，用`ZRANGE queues:NAME:reserved 0 -1 WITHSCORES`查看其元素。


### 缓存Cache

`Laravel`虽然默认也是用的`redis`，但是和`redis`直接存取相比，方便多了。`Cache`能够直接将一个对象序列化后直接以`key-value`的形式存放到`redis`中。缓存的配置文件在`config/cache.php`，可以指定`redis`的连接。

用到缓存，我的建议是，从`model`层入手，仅仅基于`model`的增删该查进行缓存，而不是直接缓存最上层控制器的结果，如果缓存控制器结果，那么下面相关的所有`model`在变化的时候都得进行改变，这样就会相当复杂。当然具体业务具体分析，如果你仅仅是返回一个静态的页面呢。

```php
Cache::remember('redis-key', 10, function () {
  return User::find(1);
});

Cache::get('key', 'default');
Cache::put('key', 'value', $minutes);
```

如果想在`Model`进行什么更改以后让缓存消失或者更新缓存，那么可以用`Model`的事件去监听。

#### 如何缓存关联关系

由于关系的定义函数并没有直接查询数据库而是一个pdo对象，所以不能直接对关系进行缓存，折衷方法是可以添加一个方法，例如

```php
class User extends Model {}
  public function post() {
	return $this->hasMany(...);
  }
  public function getPost() {
    Cache::remember(..., 10, funciton () {
      return $this->post;
    }))
  }
}
```

#### 数据库为null的时候的缓存问题以及数据库事务的处理方法。

在5.4以前，`remember`和`get`在获取的时候，无论是没有该`key`还是`value`为`null`，得到的结果都是一样的，这样`remember`在每次都会先从`redis`读一次，没找到再在回调函数里面读数据库，然后把null值返回，最后再把null值写入缓存。虽然缓存多次读写没毛病，但是这里数据库也执行了很多次无效查询。我的解决办法用`Redis`去查询key是否真的存在。

如果当前在数据库的事务里面，并且事务进行了回滚，那么依赖于`Redis`的`Cache`并不会自动回滚，可能导致数据不一致。我的解决办法是当有事务发生的时候，不进行缓存的读操作，并且在查询的时候直接将该key进行删除，无论事务里面对该model进行了什么操作，保证数据一致性。

两个问题的解决办法是这样的:

```php
static public function remember($key, $minute, Closure $callback)
{
  if (DB::transactionLevel() === 0) {
    // cache本身的取值方式见vendor/laravel/framework/src/Illuminate/Cache/RedisStore.php
      $value = Redis::connection(self::REDIS_CACHE)->get($key);
      if ($value == 'N;') return null;
      if (is_null($value)) return Cache::remember($key, $minute, $callback);
      return is_numeric($value) ? $value : unserialize($value);
  } else {
    Cache::forget($key);
    return $callback();
  }
}

static public function existsInCache($key)
{
  return Redis::connection(self::REDIS_CACHE)->exists(
    sprintf('%s:' . $key, config('cache.prefix'))
  );
}
```

### 事件

就是实现了简单的观察者模式，允许订阅和监听应用中的事件。用法基本上和队列一致，并且如果用上队列，那么代码执行上也和队列一致了。

#### 事件的注册

#### 事件的定义

#### 事件监听器

#### 事件的触发 

### 服务容器

Laravel核心有个非常非常高级的功能，那就是服务容器，用于管理类的依赖，可实现自动的依赖注入。比如，经常会在laravel的控制器的构造函数中看到这样的代码:

```php
function function __construct(Mailer $mailer){
  $this->mailer = $mailer	
}
```

但是我们却从来不用自己写代码去实例化Mailer，其实是由Laravel的服务容器自动去提供类的实例化了。

```php
# 注册进容器
$this->app->bind('Mailer', function($app){
  return new Mailer('一些构造参数')
});
$this->app->singleton('Mailer', function($app){		# 直接返回的是单例
  return new Mailer('一些构造参数')
})
$this->app->instance('Mailer', $mailer)		# 如果已经有一个实例化了的对象，那么可以通过这种方式将它绑定到服务容器中去
  
# 从容器解析出来
$mailer = $this->app->make('Mailer')	# 返回一个实例
$this->app['Mailer']					# 这样也可以
public function __construct(Mailer $mailer)	# 在控制器、事件监听器、队列任务、过滤器中进行注册
```

### 事件Event

应用场景: 

1.缓存机制的松散耦合，比如在获取一个资源时先看是否有缓存，有则直接读缓存，没有则走后端数据库，此时，通常做法是在原代码里面直接用`if...else...`进行判断，但有了缓存后，我们可以用事件来进行触发。

2.`Illuminate\\Database\\Events\\QueryExecuted`监听数据库相关事件来进行后续处理

### Service Provider

Laravel提供了很方便的注入服务的方法，那就是`service provider`，当写完一个`service provider`以后，在`config/app.php`的provider里面添加该类名称即可实现注入。最重要的两个方法:`绑定(Binding)`和`解析(Resolving)`。

```php
 App()->getLoadedProviders();	// 查看当前已经加载了哪些providers，程序刚启动的时候，懒加载的service provider是不会loaded的。通过个方法或者非懒加载的直接App()->isBooted就可以看到provider有没有加载了

# 对象的解析
$this->app->make('Foo');
$foo = $this->app['Foo'];

# resolving方法用于监听对象被容器解析事件
$this->app->resolving(function ($object, $container) {});	// 解析所有的对象都会别调用
$this->app->resolving('db', function () {});		// 当解析db类型的对象时会被调用
```

这样就可以给laravel编写第三方扩展包了，例如

```php
<?php
use Illuminate\Support\Facades\Config;
use Illuminate\Support\ServiceProvider;

class TestServiceProvider extends ServiceProvider
{
    protected $defer = true;	// 如果需要延迟加载(用的时候才加载)，那么需要定义这个属性并且需要定义下面的provides方法
    
    public function boot()
    {
        // 这里面可以将自己的配置文件push到laravel的config目录中区
        $this->publishes([realpath(__DIR__.'/../../config/api.php') => config_path('api.php')]);
      	$this->mergeConfigFrom(__DIR__.'/config/test.php', 'database');	// 将配置文件合并到已经存在的config下面里面去，动态合并的，并没有写入到文件中去
    }

  	// 这里面可以做一些初始化操作，程序启动的时候执行
    public function register()
    {
      Config::set('database.redis', []);	// 设置可以在这里面修改config下的其他一些配置
    }
    
    // 一般懒加载的时候才需要
    public function provides()
    {
        return [Connection::class];
    }
}
```

### Facades外观

使用外观模式提供静态的接口去访问注册到IoC容器中的类，并且配以别名，这样的好处是，使用起来简单一些，不用写很长的类名。

```php
// 外观定义

```

### 重要对象

#### Route

```php
$route->parameters()	# 获取路由上的参数，即不是GET和POST之外的，定义在路由上面的参数
```

#### Mail

- 发送邮件相关功能
- `to`: 邮件接收人，`cc`: 抄送对象，`bcc`: 暗抄送对象

```php
Mail::to($email)
    ->cc(['admin@haofly.net','admin1@haofly.net'])
    ->send('document');
```

### [Laravel helpers帮助方法以及Collection集合](https://haofly.net/laravel-helpers)


#### Crypt

`Laravel`通过`Mcrypt PHP`扩展提供AES加密功能。一定要设置`config/app.php`中的`key`

```php
$encrypted = Crypt::encrypt('password');
$decrypted = Crypt::decrypt($encrypted);
```

### 错误和日志

- 日志模式: `single`表示输出到`storage/log/laravel.log`中，`daily`表示按天输出到`storage/log/`目录下，`syslog`会输出到系统日志中`/var/log/message`，`errorlog`跟PHP的`error_log`函数一样输出到php的错误日志中
- `logger`用于直接输出`DEBUG`级别的日志，更好的是使用`use Illuminate\Support\Facades\Log;`，如果`storage/laravel.log`下面找不到日志，那么可能是重定向到`apache`或者`nginx`下面去了

```php
# 日志的用法
Log::useFiles(storage_path().'/logs/laravel.log')	# 如果发现无论什么都不输入到日志里面去，一是检查日志文件的权限，而是添加这个，直接指名日志文件

Log::emergency('紧急情况');
Log::alert('警惕');
Log::critical('严重');
Log::error('错误');
Log::warning('警告');
Log::notice('注意');
Log::info('This is some useful information.');
Log::debug();

# 日志分割，使日志按天分割
Log::useDailyFiles('路径', 30, 'debug')	# 30表示保存最近多少天的日志文件
$monolog = Log::getMonolog();		 	# 获取monolog实例
$monogo->getHandlers();					# 获取处理handlers
$handler->setFormatter(new CustomFormatter());	# 自定义handler的输出格式

# 定义日志输出格式
class CustomFormatter extends Monolog\Formatter\LineFOrmatter
{
  /*重写这个方法就好了*/
  public function format(array $record)
  {
	$msg = [
	$record['datetime']->format('Y-m-d H:m:s.u'),
            '[TxId : ' . '' . ' , SpanId : ' . '' . ']',
            '[' . $record['level_name'] .']',
            $record['message'],
            "\n",
        ];

    return implode(' ', $msg);
  }
}

# 新建处理方法
$logStreamHandler = new StreamHandler('路径', Logger::DEBUG);
$logStreamHandler->setFormatter(new CustomFormatter());
Log::getMonolog()->pushHandler($logStreamHandler);
```

#### 自定义错误处理类

Laravel里面所有的异常默认都由`App\Exceptions\Handler`类处理，这个类包含`report`(用于记录异常或将其发送到外部服务)和`render`(负责将异常转换成HTTP响应发送给浏览器)方法。render是不会处理非HTTP异常的，这点要十分注意。

##### 自定义未认证/未登陆的错误信息或重定向

```php
# App\Exceptions\Handler
class Handler extends ExceptionHandler
{
  // 复写该方法即可
  protected function unauthenticated($request, AuthenticationException $exception)
  {
    return $request->expectsJson()
      ? response()->json(['message' => 'Unauthenticated.'], 401)
      : redirect()->guest(route('authentication.index'));
  }
```

#### 统一的异常处理

Laravel可以在`app/Exceptions/Handler.php`里面自定义统一处理异常，需要注意的是，验证异常是不会到这个Handler里面的，验证失败的时候，会抛出`HttpResponseException`，它并不继承于`HttpException`。

```php
public function report(Exception $e)
{
  if ($e instanceoof NotFoundException) {
    throw new NotFoundHttpException;
  }
  
  // HTTP Exception按正常流程处理
  if ($e instanceof HttpException) return parent::report($e);

  $request = request();
  $log = [
    'msg'           => $e->getMessage(),
    'file'          => $e->getFile(),
    'line'          => $e->getLine(),
    'request_path'  => $request->getPathInfo(),
    'request_body'  => $request->all(),
  ];
  Log::error(json_encode($log));
  throw new ResourceException('System Exception');
}
```

### Artisan Console

- `php artisan serve --port=80`: 运行内置的服务器

- `php artisna config:cache`: 把所有的配置文件组合成一个单一的文件，让框架能够更快地去加载。

- `queue:work`从5.3开始默认就是`daemon`，不需要加`—daemon`参数了

- `queue:work`和`queue:listen`的区别是，前者不用每次消费都重启整个框架，但是代码变更后前者必须手动重启命令

- 使用命令的方式执行脚本，这时候如果要打印一些日志信息，可以直接用预定义的方法，还能显示特定的颜色:

  ```shell
  $this->info('')	# 绿色
  $this->line('')	# 黑色
  $this->comment('')	# 黄色
  $this->question('') # 绿色背景
  $this->error('')	# 红色背景
  ```

- Command添加参数

  ```php
  protected $signature = 'test:test {field?} {--debug}';	# 添加参数，问号表示非必填。以--开头的参数叫option，option是布尔值，默认是false，当命令执行时带上该参数则值会为true
  $this->argument('field');					# 获取参数，只能在handle里面，不能在__constructor里面
  $this->option('debug');		# 获取option的参数
  ```

- 命令行直接调用

  ```php
  $exitCode = Artisan::call('email:send', [
      'user' => 1, '--queue' => 'default'
  ]);
  
  # 或者直接在shell里面执行
  php artisan test:test 
  ```


#### 定时任务

```php
# 如果将命令添加到定时任务中去，首先要在www用户下新建crontab
crontab -u www -e	# 添加如下一行
* * * * * php /data/www/html/furion/artisan schedule:run >> /dev/null 2>&1	# 需要注意的是laravel会将程序的错误输出重定向到/dev/null，即直接抛弃。这里的schedule:run只是所有任务的一个总的进程。它负责调度kernel.php里面定义的所有定时任务。而其他定时任务的错误输出同样会重定向到/dev/null


# 在kernel.php中定义定时任务
class Kernel extends ConsoleKernel
{
    protected $commands = [
        //
    ];

    protected function schedule(Schedule $schedule)
    {
      $schedule->command('test')
        ->everyMinute()	// 每分钟执行
        ->days([0, 3])	// 每周日和周三
        ->days([Schedule::SUNDAY, Schedule::WEDNESDAY])	// 每周日和周三
        ->between('7:00', '22:00')	// 仅在7:00至22:00之间执行
        ->unlessBetween('23:00', '4:00')	// 在23:00至4:00之间执行
        ->when(function () {return true;})	// 满足某个条件才执行
        ->skip(function () {return true;})	// 满足某个条件就不执行
        ->environments(['staging', 'production'])	// 传入环境变量
        ->at('2:00')	// 在2:00执行
        ->onOneServer()	// 仅在一台服务器执行
        ->before(function(){})	// 任务执行前触发
        ->after(function () {})	// 任务执行后触发
        ->onSuccess(function () {})	// 任务成功后触发
        ->onFailure(function () {}) // 任务失败后触发
        ->pingBefore($url)	// 任务执行前ping指定url
        ->thenPing($url)	// 任务执行后ping指定url
        ->pingBeforeIf($condition, $url)
        ->thenPingIf($condition, $url)
        ->pingOnSuccess($url)
        ->pingOnFailure()
        ->emailOutputTo('haoflynet@gmail.com')	// 将输出日志传送至指定email
        ->sendOutputTo($filePath)	// 输入日志
        ->appendOutputTo($fileCronLog);	// append方式输出日志
     
      
      // 直接定义简单的定时任务
      $schedule->call(function () {
        DB::table('recent_users')->delete();
      })->daily();
      

      
      $schedule->job(new Heartbeat)->everyFiveMinutes();	// 添加队列的定时任务
      $shcedule->exec('node /home/forge/script.js')->daily();	// 添加命令行定时任务
      $schedule->call('App\Http\Controllers\MyController@test')->everyMinute();	// 将控制器方法作为定时任务
    }
}
```

#### 缓存清理

```shell
php artisan cache:clear
php artisan route:clear
php artisan config:clear
php artisan view:clear
```

### 框架扩展/管理者/工厂

Laravel有几个"Manager"类，用于管理一些基本的驱动组件，例如数据库管理类、缓存管理类、会话管理类、用户验证管理、队列管理。这种类负责根据配置来创建一个驱动。

```php
# 所有的Manager都有个extend方法，可以将新的或者说自己写的驱动注入到manager中去。例如
$this->app->resolving('db', function ($db) {
  return new Connection($config);
});
```

### 测试

PHP的phpunit提供了很好的测试方式，Laravel对其进行了封装，使得易用性更高更方便。

```php
# 访问页面
$this->visit('/')->click('About')->seePageIs('/about-us') # 直接点击按钮并察看页面
$this->seePageIs('/next')	# 验证当前url的后缀是不是这个
$this->visit('/')->see('Laravel 5')->dontSee('Rails')	# 查看页面是否存在某个字符串或者不存在
  
# 用户登录
$user = User::find(1)
$this->be($user)		# 直接在测试用例添加这个即可
Auth::check()			# 用户是否登录，如果已经登录返回true
  
# 表单填写
$this->type($text, $elementName)	# 输入文本
$this->select($value, $elementName)	# 选择一个单选框或者下拉式菜单的区域
$this->check($elementName)			# 勾选复选框
$this->attach($pathtofile, $elementName)	# 添加一个文件
$this->press($buttonTextOrElementName)	# 按下按钮
# 如果是复杂的表单，特别是包含了数组的表单，可以这样子
<input name="multi[]" type="checkbox" value="1">
<input name="multi[]" type="checkbox" value="2">
这种的，就不能直接使用上面的方法了，只能怪上面的方法不够智能呀，解决方法是直接提交一个数组
$this->submitForm('提交按钮', [
  'name' => 'name',
  'multi' => [1, 2]
]);

# 测试
$this->seeInDatabase('users', ['email' => 'hehe@example.com']) # 断言数据库中存在
  
# 模型工厂Model Factories,database/factories/ModelFactory.php，可以不用插入数据库，就能直接得到一个完整的Model对象，define指定一个模型，然后把字段拿出来填上想要生成的数据，例如
$factory->define(App\User::class, function (Faker\Generator $faker) {
  return [
    'name' => $faker->name,
    'password' => bcrypt(str_random(10)),
    'remember_token' => str_random(10),
  ]
});
// 使用的时候，直接这样，50表示生成50个模型对象
factory(App\User::class, 50)->create()->each(function($u) {
  $u->posts()->save(factory(App\Post::class)->make());
});

# 直接对控制器进行测试可以这样做
public function setUp(){
  $this->xxxController = new xxxController()
}

public function testIndex{
  $re = $this->xxxController->index(new Request([]));
  var_dump($re->content);
  var_dump($re->isSuccessful());
}

# 测试命令这样执行
./vendor/bin/phpunit tests/xxxTest.php
```

在实际的测试过程中，我有这样的几点体会:

- 测试类本身就不应该继承的，因为单元测试本身就应该独立开来
- 直接对控制器测试是一种简单直接有效的测试方法，而无需再单独给service或者model层进行测试


### 性能优化

```shell
php artisan clear-compiled && php artisan cache:clear && php artisan config:clear && php artisan route:clear

php artisan optimize --force && php artisan config:cache && php artisan api:cache
```

## [Laravel TroubleShooting/Laravel相关故障解决](https://haofly.net/laravel-troubleshooting)

**相关文章**

[用Laravel拥抱异常](https://laravel-china.org/topics/2460)

[将SQL语句直接转换成Laravel的语法](http://www.midnightcowboycoder.com/)

[Laravel请求生命周期](https://laravel-china.org/articles/10642/laravel-request-life-cycle)

[如何少写PHP"烂"代码](https://juejin.im/post/5b4ecffef265da0fa1221f45): 更好的MVC分层实践

[打造 Laravel 优美架构 谈可维护性与弹性设计](https://juejin.im/post/5be4475c518825170559c044)

[laravelio/portal](https://github.com/laravelio/portal): 一个很好的参考项目，连测试都写得非常好

[octobercms](https://github.com/octobercms/october): laravel写的cms系统

[[Laravel 从学徒到工匠系列] 目录结构篇](https://laravelacademy.org/post/9711.html#toc_2): 详细解释了laravel为何没有Model目录

[老司机带你深入理解 Laravel 之 Facade](https://learnku.com/articles/37493)

[Laravel项目深度优化指南](https://learnku.com/articles/35470)

[如何在Laravel中使用PHP的装饰器模式](https://learnku.com/laravel/t/41757): 这篇文章中的仓库模式也是十分有用的

