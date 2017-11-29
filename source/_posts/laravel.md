---
title: "Laravel"
date: 2014-12-12 11:02:39
updated: 2017-11-29 10:21:00
categories: php
---
# Laravel指南
[Laravel项目基本结构](https://github.com/haoflynet/project-structure/blob/master/Laravel/README.md)

### 配置

Laravel的主配置文件将经常用到的文件集中到了根目录下的`.env`目录下，这样更高效更安全。其内容如下：

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

配置文件中使用变量:

```shell
DOMAIN=
```

### 控制器

laravel可以直接通过命令创建一个控制器:
`php artisan make:controller HomeController`，然后就会有这么一个控制器文件了:`app/Http/Controllers/HomeController.php`

#### 数据校验Validation

```
# 通过Validator进行校验，第一个参数是一个key-value的数组
$validation = Validator::make($request->all(), [
  'ip' => 'required|ip'			# 校验key=ip的值是否真的是ip
  'arr.arr.field' => 'required'	# 验证多级数组内部字段，其实都是字典
  'arr.*.field'	=> 'required'	# 验证数组内部的字段，数组下面是一个数组的情况，5.1不支持
])

# 常用框架自带的认证类型
active_url			# 该url一定能访问
array				# 仅允许为数组
between:min,max		# 介于最小值和最大值之间，两边都是闭区间，如果是数字，一定要先声明当前字段为integer
boolean				# 必须是true,false,1,0,"1","0"
date				# 必须是时间类型
exists:table,column	# 判断字段的值是否存在于某张表的某一列里面
exists:table,column1,column2,value	# 判断字段的值是否存在于某张表的某一列里面，并且另一列的值为多少
exists:table,column1,column2,!value	# 判断字段的值是否存在于某张表的某一列里面，并且另一列的值不为多少
exists:table,column1,column2,{$field}# 判断字段的值是否存在于某张表的某一列里面，并且另一列的值和前面的某个字段提供的值一样
in:value1,value2,...# 字段值必须是这些值中的一个，枚举值
not_in:value1,value2,...	# 字段值不为这其中的任何一个
integer				# 必须是整数
ip					# 必须是IP字符串
json				# 必须是JSON字符串
max:value			# 规定最大值
min:value			# 规定最小值
numeric				# 是数字
required			# 必填
required_if:anotherfield,value1,value2	# 当指定的anotherfield字段等于任何一个value时，此字段必填
required_unless:anotherfield,value1,value2 # 当指定的anotherfield字段等于任何一个value时，此字段不用必填
required_with:foo,bar,...  # 当指定的字段中任何一个有值时，此字段为必填
required_with_all:foo,bar,...	# 当指定的所有字段都有值时，此字段为必填
required_without:foo,bar,...	# 如果缺少任意一个指定的字段，则自此字段为必填
required_with_out_all:foo,bar,...	# 如果所有指定的字段你都没有值，则此字段为必填
same:foo			# 必须和指定字段的值保持一致
string				# 必须是字符串
url					# 必须是合法的url
regex				# 必须符合这个正则表达式，例如regex:/^[a-z]{1}[a-z0-9-]+$/，需要注意的是，如果正则表达式中用了|符号，必须用数组的方式来写正则表达式，否则会报错，例如['required', 'regex:/[0-9]([0-9]|-(?!-))+/']

# 自定义错误提示的消息，可以通过传递进去，不过也可以直接在语言包文件resources/lang/xx/validation.php文件的的custom数组中进行设置

# 验证数组里面的字段用这样的方式
'person.email' => 'email|unique:users'
'person.first_name' => 'required_with:person.*.last_name'

# 将表单的验证提取出来作为单独的表单请求验证Form Request Validation
# 使用php artisan make:request BlogPostRequest创建一个表单请求验证类，会在app/Http/Requests里面生成相应的类，之后表单验证逻辑就只需要在这里写上就行了，例如
<?php
namespace App\Http\Requests;
use Route;
use Illuminate\Support\Facades\Auth;
class BlogPost extends Request{
	// 这个方法验证用户是否有权限访问当前的控制器
    public function authorize()    {
        $id = Route::current()->getParameter('post');	// 如果是resource的东西，要获取id，在这里是这样子获取，不能直接用id，而是相对应的资源名
        switch($this->method()){	# 我这里，姑且卸载一起
            case 'POST':{
                return Auth::user()->can('create', Project::class);
            }
            case 'PUT':{
                return Auth::user()->can('update', Project::find($id));
            }
        }
    }

    /**
     * 这里则是返回验证规则
     */
    public function rules(){
        switch($this->method()){
            case 'POST': {
                return [
                    'name'              => 'required|string|max:100',
                ];
            }
            case 'PUT':{
                return [
                    'name'              => 'required|string|max:100',

                ];
            }
        }
    }

	// 自定义返回格式
    public function response(array $errors){
        return redirect()->back()->withInput()->withErrors($errors);
    }
}
```

#### Restful资源控制器

资源控制器可以让你快捷的创建 RESTful 控制器。通过命令`php artisan make:controller PhotoController`创建一个资源控制器，这样会在控制器`PhotoController.php`里面包含预定义的一些Restful的方法
Route::resource('photo', 'PhotoController');

```php
# 嵌套资源控制器
# 例如
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
这样定义url
Route::resource('wei/{who}', 'WeixinController');
然后在控制器里这样定义
public function index($who)

# 嵌套资源控制器
# 例如
Route::resource('photos.comments', 'PhotoCommentController');
# 这样可以直接通过这样的URL进行访问photos/{photos}/comments/{comments}
# 控制器只需要这样子定义即可
public function show($photoId, $commentId)
# 如果要获取嵌套资源的url，可以这样子:
route('post.comment.store', ['id'=> 12]) # 这样子就获取到id为12的post的comment的创建接口地址
```

### 视图/静态资源

#### 提供文件下载

```php
return response()->download($pathToFile);	# 直接提供文件下载
return response()->download($pathToFile, $name, $headers);	# 设置文件名和响应头
return response()->download($pathToFile)->deleteFileAfterSend(true); # 设置为下载后删除
```

### 模板Template

#### 标签

```tex
# 转义
{!! $name !!}

# if else
@if()
@else
@endif
# 需要注意的是，if else是不能写在一行的如果非要写在同一行，建议使用这样的方法
{!! isset($a) && $a['a'] == 'a' ? 'disabled': '' !!}
```

#### 分页

Larval的分页主要靠Eloquent来实现，如果要获取所有的，那么直接把参数写成`PHP_INT_MAX`就行了嘛

```php
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

#### 建表操作

生成一个model: `php artisan make:model user -m`，这样会在`app`目录下新建一个和user表对应的model文件

	<?php
	namespace App;
	use Illuminate\Database\Eloquent\Model;
	class Flight extends Model
	{
	    //
	}
加上`-m`参数是为了直接在`database/migrations`目录下生成其迁移文件，对数据库表结构的修改都在此文件里面，命名类似`2016_07_04_051936_create_users_table`，对数据表的定义也在这个地方，默认会按照复数来定义表名:


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

当数据表定义完成过后，执行`php artisan migrate`即可在真的数据库建表了

	php artisan migrate				// 建表操作，运行未提交的迁移
	php artisan migrate:rollback 	// 回滚最后一次的迁移
	php artisan migrate:reset		// 回滚所有迁移
	php artisan migrate:refresh   	// 回滚所有迁移并重新运行所有迁移

如果要修改原有model，不能直接在原来的migrate文件上面改动，而是应该新建修改migration，例如，执行`php artisan make:migration add_abc_to_user_table`这样会新建一个迁移文件，修改语句写在up函数里面:

```php
public function up()
{
    Schema::table('users', function (Blueprint $table) {
        $table->string('mobile', 20)->nullable()->after('user_face')->comment('电话号码')->change();  // 将mobile字段修改为nullable并且放在user_face字段后面，主要就是在后面加上change()方法
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
    });
}
```

#### 表/Model的定义

```php
class User extends Model{
  public $timestamps = false;			// 设置该表不需要使用时间戳，updated_at和created_at字段
  protected $primaryKey = 'typeid'		// 不以id为主键的时候需要单独设置，需要注意的是laravel以及其他很多orm都不支持复合主键，可能会出现"Segment Fault"
  protected $primaryKey = null;			// 没有主键的情况
  protected $incrementing	= false;	// 不使用自增主键
  protected $connection = 'second';		// 设置为非默认的那个数据库连接
  protected $fillable = ['id', 'name']; // 设置可直接通过->访问或者直接提交保存的字段
  protected $table = 'my_flights';		// 自定义表明，默认的表明会以model的复数形式，需要注意的是，英语单词复数的变化有所不同，如果取错了表明活着以中文拼音作为表明，有时候就需要明确表的名称了
}
```

#### 字段的定义

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

#### 定义表之间的关系

直接在ORM里面进行表关系的定义，可以方便查询操作。

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

	public function father(){
		return $this->hasOne('App\Father');
	}
	
	$this->hasOne('App\Father', 'id', 'father');	# 表示father的id对应本表的father
##### 相对关联belongsTo(多对一)

	public function user(){
		return $this->belongsTo('App\User');
		// return $this->belongsTo('App\User')->withDefault();	// 这样子如果找不到关联对象，则会返回一个空对象
		// return $this->belongsTo('App\User')->withDefault(['name' => '不知道'] ); // 还可以给这个空对象赋予默认值
	}
	Posts::find(1)->user  # 可以找到作者
##### 多对多关系belongsToMany

如果有三张表，users,roles,role_user其中，role_user表示users和roles之间的多对多关系。如果要通过user直接查出来其roles，那么可以这样子

	class User extends Model {
	  public funciton roles()
	  {
	    return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'foo_id');	# 其中user_roles是自定义的关联表表名，user_id是关联表里面的user_id，foo_id是关联表里面的role_id
	  }
	}
	
	$roles = User::find(1)->roles;	# 这样可以直接查出来，如果想查出来roles也需要在roles里面进行定义
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

然后在Composer的命令行里执行填充命令

	php artisan db:seed
	php artisan migrate:refresh --seed    //回滚数据库并重新运行所有的填充

#### ORM操作

```php
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
User::findOrFail(1);				# 根据主键取出一条数据或者抛出异常
User::where([
  ['id', 1],
  ['name', 'haofly']
);			# where语句能够传递一个数组
User::where();					# 如果不加->get()或者其他的是不会真正查询数据库的，所以可以用这种方式来拼接，例如$a_where=User::where();$result =$a_where->where()->get();
User::where('field', 'like', '%test%');	# 模糊搜索
User::where('field', 'regexp', 'abc');	# 正则搜索
User::where()->limit(2)				# limit限制
User::whereIn('name', ['hao', 'fly']);	# in查询
User::whereNull('name');			# is null
User::whereNotNull('name');		# is not null
User::whereBetween('score', [1, 100]);	# where between
User::whereNotBetween('score', [1, 100]);	# where not between
User::whereDate('created_at', '2017-05-17');
User::whereMonth('created_at', '5');
User::whereDay('created_at', '17');
User::whereYear('created_at', '2017');
User::whereRaw('name="wang" and LENGT(name) > 1');				# 当有复杂点的where语句或者想直接写在mysql里面的那样的where语句，可以直接这样写
User::whereColumn('first_field', 'second_field');	# 判断两个字段是否相等
User::where(...)->orWhere()		# or where
User::where()->firstOrFail()	# 查找第一个，找不到就抛异常
User::where('user_id', 1)->get()# 返回一个Collection对象
User::where(...)->first()		# 只取出第一个model对象
User::find(1)->logs->where(...)	# 关系中的结果也能用where等字句
User::->where('updated_at', '>=', date('Y-m-d H:i').':00')->where('updated_at', '<=', date('Y-m-d H:i').':59') 					# 按分钟数查询
User::find(1)->sum('money')		# 求和SUM
User::where(...)->get()->pluck('name')	# 只取某个字段的值，而不是每条记录取那一个字段，这是平铺的,这里的pluck针对的是一个Collection，注意，这里只能针对Collection，千万不要直接针对一个Model，这样只会取出那张表的第一条数据的那一列，需要注意的是这里是先get除了所有的记录，然后在Collection上面进行的pluck操作，如果想少去一点数据可以先用select()再用pluck
User::select('name')->where()	# 也是只取出某个字段，但是这里不是平铺的
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
User::select('name')->leftJoin('posts', 'users.id', '=', 'posts.user_id')->where(...);	# Left Join语法
# has语法，不会与Post的字段相冲突
$posts = Post::has('comments')->get();	# 获取所有有评论的posts
$posts = Post::has('comments', '>=', 3)->get();	# 获取评论数量大于3的
$posts = Post::has('comments.votes')->get();	# 嵌套has
  $posts = Post::whereHas('comments', function($query) {
    $query->where('content', 'like', 'foo%');	# 比较复杂的has语法
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

# 修改
$user->fill(['name' => 'wang'])->save()	# fill必须save过后才会更新到数据库
$user->update(['name' => 'wang'])	# update会立即更新数据库
$user->increment('age', 5)	# 如果是数字类型，可以直接相加，不带5就表示之内加1
$user->decrement('age', 5)	# 或者减
# 删除
$user->delete()	# 删除，如果设置了软删除则是软删除
$user->forceDelete()	# 无论是否设置软删除都物理删除
  
# 事务，注意数据库的连接问题
DB::beginTransaction();
DB::connection('another')->begintransaction();
DB::rollback();		# 5.1之前用的都是rollBack
DB::commit();
```

#### 查询缓存

##### With(预加载)

with在laravel的ORM中被称为预加载，作用与关联查询上

```php
# 例如要查询所有文章的作者的名字，可以这样子做
$posts = App\Post::all();
foreach($posts as $post) {
  var_dump($post->user->name);
}
# 但是，这样做的话，每一篇文章都会查询一次用户，而如果这些文章的用户都是一个人，那岂不是要查询n次了。这时候预加载就有用了。
$posts = App\Post::with('user')->get();
foreach ( $books as $book) {
  var_dump($post->user->name);
}
# 这样子做，所有的数据在foreach前就都读取出来了，后面循环的时候并没有查询数据库，总共只需要查询2次数据库。

# with还可以一次多加几张关联表
App\Post::wth('user', 'author')->get();
# 嵌套使用
App\Post::with('user.phone')->get(); # 取出用户并且取出其电话

# 也可以不用全部取出来
$users = User::with(['posts' => function ($query) {
  $query->where('title', '=', 'test');
}])->get();
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

通过`php artisan make:job CronJob`新建队列任务，会在`app/Jobs`下新建一个任务.

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

# 任务出错执行
public function failed()
{
	echo '失败了';
}
```
#### 队列消费

- `queue:work`: 最推荐使用这种方式，它比`queue:listen`占用的资源少得多，不需要每次启动框架。但是代码如果更新就需要用`queue:restart`来重启

需要注意的是  

1. 不要在`Jobs`的构造函数里面使用数据库操作，最多在那里面定义一些传递过来的常量，否则队列会出错或者无响应  
2. job如果有异常，是不能被catch的，job只会重新尝试执行该任务，并且默认会不断尝试，可以在监听的时候指定最大尝试次数`--tries=3`
3. 不要将太大的对象放到队列里面去，否则会超占内存，有的对象本身就有几兆大小
4. 一个很大的坑是在5.4及以前，由于`queue:work`没有timeout参数，所以当它超过了队列配置中的`expire`时间后，会自动重试，但是不会销毁以前的进程，默认是60s，所以如果有耗时任务超过60s，那么队列很有可能在刚好1分钟的时候自动新建一条一模一样的任务，这就导致数据重复的情况。
5. 如果是使用redis作为队列，那么队列任务默认是是Job的NAME命名，例如
6. `queues:NAME`，是一个列表，过期时间为-1，没有消费者的情况是会一直存在于队列中。而如果是延迟执行的任务，则是单独放在一个有序集合中，其key为`queues:NAME:delayed`，其`score`值就是其执行的时间点


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

应用场景: 1.缓存机制的松散耦合，比如在获取一个资源时先看是否有缓存，有则直接读缓存，没有则走后短数据库，此时，通常做法是在原代码里面直接用`if...else...`进行判断，但有了缓存后，我们可以用事件来进行触发

### Service Provider

Laravel提供了很方便的注入服务的方法，那就是`service provider`，当写完一个`service provider`以后，在`config/app.php`的provider里面添加该类名称即可实现注入。这样就可以给laravel编写第三方扩展包了。

```php
<?php
use Illuminate\Support\Facades\Config;
use Illuminate\Support\ServiceProvider;

class TestServiceProvider extends ServiceProvider
{
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
}
```

### 重要对象

#### Request

```php
$request->route()	# 通过request获取Route对象
```

#### Route

```php
$route->parameters()	# 获取路由上的参数，即不是GET和POST之外的，定义在路由上面的参数
```

### 帮助类

#### Collection Laravel的集合

`Illuminate\Support\Collection`类提供了一个非常方便的操作来操作数组

```php
$collection = collect([1, 2, 3]);		// 创建一个集合类
User::where('name', 'wang')->get();		// 操作数据库经常会返回一个Collection

all();					// 返回该集合所代表的底层数组[1, 2, 3]
avg();					// 返回集合中所有项目的平均值
avg('field');			// 指定键值的平均值
chunk(n);				// 拆分集合
collapse([1,2], [2,3])	// 合并数组为一个集合
contains('key');		// 判断集合是否含有某个key
count();				// 返回集合总数
diff(arr2);				// 返回在第一个集合中存在而在第二个集合中不存在的值
each(function ($item, $key) {return false;});	// 遍历集合，回调函数返回false的时候会中断循环
every(function ($value, $key) {return 1>2;});	// 判断集合中的每个元素是否都满足条件
except(['field']);		// 返回集合中除了制定键以外的所有项目
filter(function ($value, $key) {return 1>2;});	// 在回调函数中筛选集合，只留下return true的项目
filter();				// 不提供参数的时候，集合中为false的元素都被移除
first(function ($value, $key) {return 1>2;});	// 返回第一个return true的项目
first();				// 不提供参数则返回第一个项目
forget('key');			// 根据key移除某个项目，如果是数组，应该输入序号
forPage();				// 集合分页
groupBy('field');		// 根据键值分组
implode('field', ',');	// 合并集合中指定键的值为字符串，如果不提供field，则表示直接将项目进行合并
map(function ($value, $key) {return 'a';});		// 遍历修改集合中的值
random(n=0);				// 随机返回一个项目，n可以不填，如果n>1则会返回一个集合，注意为1的时候返回的不是集合而是里面的项目
reject(function($item){return true;});			// 从集合中移除元素，当返回true的时候，该元素会被移除
unique(function ($item) {return $item;} );		// 仅仅返回唯一的值，相当于去重
```

#### Crypt

`Laravel`通过`Mcrypt PHP`扩展提供AES加密功能。一定要设置`config/app.php`中的`key`

```php
$encrypted = Crypt::encrypt('password');
$decrypted = Crypt::decrypt($encrypted);
```

### 帮助函数

```php
# intersect 获取request的字段来更新字段
$record->update($request->intersect([
    'title',
    'label',
    'year',
    'type'
]));

$re = request();	// 任何地方获取请求对象，5.1开始
$re = response();	// 任何地方获取响应对象，5.1开始

str_contains('Hello foo bar.', 'foo');	# 判断给定字符串是否包含指定内容
str_random(25);			# 产生给定长度的随机字符串
```

### 错误和日志

`logger`用于直接输出`DEBUG`级别的日志，更好的是使用`use Illuminate\Support\Facades\Log;`，如果`storage/laravel.log`下面找不到日志，那么可能是重定向到`apache`或者`nginx`下面去了

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

- `php artisna config:cache`: 把所有的配置文件组合成一个单一的文件，让框架能够更快地去加载。

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
  protected $signature = 'test:test {field?}'	# 添加参数，问号表示非必填
  $this->argument('field')					# 获取参数
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
```

在实际的测试过程中，我有这样的几点体会:

- 测试类本身就不应该继承的，因为单元测试本身就应该独立开来
- 直接对控制器测试是一种简单直接有效的测试方法，而无需再单独给service或者model层进行测试



## TroubleShooting

- **禁止全局csrf认证**：在`app/Http/Kernel.php`中，`$middleware`表示全局中间件，而`$routeMiddleware`表示针对某个路由的中间件，所以只需要把csrf在`$middleware`中注释掉，然后在`$routeMiddleware`中添加`'csrf' => 'App\Http\Middleware\VerifyCsrfToken'`
  如果要在某个路由上使用就这样：

  	Route::group(['middleware' => 'csrf'], function(){     // csrf保护的接口
  		Route::get('/', 'HomeController@index');
  	}

- **处理上传文件**：

   $file = Input::file('upload_file");// 获取上传文件对象
   	$file->isValid()                   // 检验文件是否有效
   	$file->getClientOriginalName();    // 获取文件原名
   	$file->getFileName();              // 获取上传后缓存的文件的名字
   	$file->getRealPath();              // 获取缓存文件的绝对路径
   	$file->getClientOriginalExtension();// 获取上传文件的后缀
   	$file->getMimeType();              // 获取上传文件的MIME类型
   	$file->getSize();                  // 获取上传文件的大小

- **获取输入信息**
   $id = Input::get('id');
   	$id = Input::get('id', 2);  // 还可以指定默认值

- **获取请求信息**：
   Request::url();      // 获取请求url
   	$request = new Request;
   	$request->get('id'); // 同样实现获取数据的功能

- **手动清理配置缓存 **

   php artisan config:cache

- **插入数据的时候出现`MassAssignmentException in Laravel`错误**  

   需要给数据表设置可访问的字段，在Model里面

   	protected $fillable = array('字段1', '字段2');

- **php artisan db:seed出现`[ReflectionException] Claxx XXXTableSeeder dows not exist`错误**
  这是因为新增加了文件但是composer没有感知到，需要先执行`composer dump-autoload`

- **定义/修改字段类型为timestamp时出现错误:"Unknown column type "timestamp" requested."**
  按照[[How do I make doctrine support timestamp columns?](http://stackoverflow.com/questions/34774628/how-do-i-make-doctrine-support-timestamp-columns)]的做法，目前最简单的方式是直接用`DB::statement()`来写SQL语句

- **POST数据的时候出现`The payload is invalid`**，我遇到这个情况是因为在做复杂的表单提交，直接提取`X-XSRF-TOKEN`的值，但是由于没有转移，导致后端token揭秘失败

- **保存model的时候出现错误：`Missing argument 2 for Illuminate\Database\Eloquent\Model::setAttribute()`**，一般是`Model`的几个属性没有设正确，检查这几个值`incrementing/timestamps/primarykey/fillable`

- **队列出现Cannot initialize a MULTI\/EXEC transaction over aggregate connections**: 升级到最新版laravel吧，然后将redis的扩展切换到phpredis，`laravel5.3`之前自带的`predis`不支持redis的sentinel，并且有些redis操作强依赖于predis的事务操作，各种纠结，最后都不能成功。

- **Class 'Symfony\Bridge\PsrHttpMessage\Factory\HttpFoundationFactory' not found**，偶尔安装了某些个第三方库会出现这种幺蛾子，可以用这种方式解决`composer require symfony/psr-http-message-bridge`

- **更新表时出现`AH00052: child pid 71 exit signal Segmentation fault (11)`**: 原因可能是没有设置主键而直接在该表上面更新数据，导致ORM不知道到底该更新谁。并且Laravel不支持复合主键(https://github.com/laravel/framework/issues/5517，作者不支持这种做法)。这种情况，要么给该表添加唯一主键，要么只能用where直接更新了。

## 相关文章

[用Laravel拥抱异常](https://laravel-china.org/topics/2460)