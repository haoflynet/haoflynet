---
title: "Django教程"
date: 2015-03-14 08:44:39
updated: 2024-09-04 15:01:00
categories: python
---
# Django教程

[Django常用项目结构](https://github.com/haoflynet/project-structure/blob/master/Django/README.md)以及[cookiecutter-django](https://github.com/pydanny/cookiecutter-django)。

[Django第三方库推荐](https://djangopackages.org/)

[django-extensions](https://github.com/django-extensions/django-extensions): Django扩展库，有很多其他框架有但是Django没有的扩展

Python一直是我最喜欢的语言，在这个寒假打算认真学习一下Python的Web框架。在Django和Tornado之间我选择了前者，没有特别的原因，网上人云亦云的，肯定不会有一方离另一方差很远，我就直接去看了看Github上两个项目的活跃度，所以选择了前者。

应该说Django坚持自己造轮子，确实为开发者节约了不少的时间，我很看重它的扩展功能，packages数量十分丰富。Django采用的是最流行也是我最熟悉的MVC设计模式，虽然在之前的一个PHP(Laravel)项目中也是采用的MVC模式，但一直都没怎么吃透，始终在各层分离的时候不是很清晰，所以也可趁学习Django对MVC的概念进行强化。

Django另一个我特别喜欢的特性就是Application，它与Project的概念不同，一个APP就相当于一个功能模块，一个Project可以包含多个APP，一个APP可以同时被多个Project引用，App增加了代码的复用机会，提高了扩展性和松耦合性，Django中很多的packages都是以APP的形式存在的。

<!--more-->

## 项目搭建

1. [使用Virtualenv搭建Python3的Django环境](http://haofly.net/virtualenv-python-django/)
2. 新建项目 `django-admin startproject 项目名 .` 这样会把当前目录作为一个Django项目，里面已经有一些基本的配置文件：

   ```shell
   django_test
   ├── db.sqlite3
   ├── django_test
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   └── manage.py
   ```
3. 在项目根目录下新建APP `django-admin startapp APP名称` 如果是搭建一个非常简单的应用，那么不使用APP也行，仅需把路由指向目标view就可以了，但是如果要搭建复杂的应用并且需要良好的隔离性，那最好使用APP。同样，使用该命令也会在当前目录下新建一个目录，里面已经包含一些配置文件：

   ```shell
   django_test/testapp
   ├── admin.py	# 注册models，用于admin管理
   ├── __init__.py
   ├── migrations	# 数据库迁移
   ├── models.py	# 定义models
   ├── tests.py	# 单元测试
   ├── apps.py		# App的配置类，AppConfig用于存储应用程序的元数据，可以重载父类的ready()方法，用于在Django启动时执行
   └── views.py	# 视图文件
   ```

   如果添加了APP，那么需要在主配置文件`settings.py`里面的`INSTALLED_APPS`里面添加该APP的名称

4. `Hello World！ `所有入门教程都必须要有一个Hello World! 首先，在APP的视图文件views.py里添加函数，该函数直接返回一个字符串的响应：

   ```python
   from django.shortcuts import render
   from django.http import HttpResponse
   def hello(request):
   	return HttpResponse('Hello World!')
   ```
   然后添加URL，在Project目录里的`urls.py`里进行管理，添加hello的url如下：

   ```python
   from django.conf.urls import patterns, include, url
   from django.contrib import admin
   
   urlpatterns = [
   	url(r'^admin/', include(admin.site.urls)),
   	url(r'^hello/', 'testapp.views.hello'),
   ]
   ```
5. 运行 `python manage.py runserver` 如果要以daemon的方式在后台运行，可以使用nohup命令 `nohup python manage.py runserver 0.0.0.0:8000 &` 使用它可以打开Django自带的默认Web引擎，可以在 `http://127.0.0.1:8000`中查看 在测试的时候可以使用该引擎，它不仅轻量，而且在打开后还会自动检测代码的更改，进行自动更新，这样就不用每次对代码变动了都来重启一次

## 配置项

### 全局配置

需要注意的是，Django官方并没有默认的分离配置文件的方案。我认为最佳的方式是，建立多个配置文件(仅仅把重要的需要个性化更改的配置分离开，基础的配置仍然是一个，其他使用继承覆盖的方式，基础的`settings.py`里面就直接设置为本地的即可)，然后在启动的时候指定不同的配置文件即可。`python manage.py runserver --settings=prod_setting`

配置文件内容

```python
DEBUG = True			# DEBUG模式
TEMPLATE_DEBUG = True	# TEMPLATE的DEBUG模式

ALLOWED_HOSTS = []   	# 设置哪些域名可以访问，当debug为false时必须为其指定一个值，['*']表示允许所有的访问

INSTALLED_APPS = [默认APP+自己的APP]
MIDDLEWARE_CLASSES = [中间件]

ROOT_URLCONF = 'admin.urls'	# 读取的默认的url文件

# Database 数据库的配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',	# MySQL/Mariadb数据库设置
        'NAME': 'admin',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'PORT': 3307,
        'CONN_MAX_AGE': 0,	# 数据库连接最长生存时间，超过该时间后连接自动断开，可以设置为None,表示持久化连接，不主动断开.默认是0，一个请求用完就断开
    }
}

LOGIN_URL = '/login/'	# 设置登录页面，用户未登录自动跳转到这里
LOGIN_REDIRECT_URL = '/'	# 设置登录成功后自动跳转到的页面

LANGUAGE_CODE = 'en-us'  # 语言，中文可用zh-Hans、zh-CN，完整列表见：http://www.i18nguy.com/unicode/language-identifiers.html
TIME_ZONE = 'Asia/Chongqing'        # 时区
USE_TZ = True	# 处理时间的时候会用到，详细看下面的DateTimeField字段介绍

# Static files (CSS, JavaScript, Images) 静态文件目录  
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') # 这个选项默认是没有的，在编码时将静态文件放在APP中的static目录下，部署时用python manage.py collectstatic就可以把静态文件收集到STATIDC_ROOT目录
```

在其他文件访问全局配置项，可以这样访问：

```python
from django.conf import settings
settings.DEBUG
```

### 应用配置

在上面新建的app的目录结构里面又一个`apps.py`文件，它存储了应用的元数据，通过继承`AppConfig`来配置其属性，可配置的选项如下:

```tex
可配置的属性
AppConfig.name			# 应用的完整Python路径，例如django.crontrib.admin，在整个Django项目中必须是唯一的
AppConfig.label			# 应用的缩写，例如admin，
AppConfig.verbose_name	# 应用的适合阅读的名称
AppConfig.path			# 应用目录的文件系统路径，例如/usr/lib/python3.4/dist-packages/django/contrib/admin

可配置的方法
AppConfig.get_models()			# 返回可迭代的Model类
AppConfig.get_model(model_name)	# 返回具体的Model
AppConfig.ready()				# 执行初始化任务
```

## 请求与响应

```python
HttpResponse('字符串', content_type="text/plain") # 指定content_type的响应
    
HttpRequest.method   # 请求种类
HttpRequest.GET      # 获取所有的GET参数(字典)
HttpRequest.POST     # 获取表单POST的参数，这个是获取不到Json格式传送的数据的
HttpRequest.POST.get('field', 'default')
request.body()
json.loads(request.body)	# 获取json格式的请求参数
HttpRequest.scheme   # 表示请求的模式，是http还是https
HttpRequest.cookies  # 包含了所有的cookie信息
HttpRequest.session  # session信息
HttpRequest.FILES    # 包含了上传的文件
HttpRequest.META     # 包含了http请求的各种headers，HTTP_REFERER，其中headers的字段都是大写并且会有个前缀，例如headers中有key，那么request.META.HTTP_KEY，用这种方式获取
HttpRequest.user     # 当前的登录的用户，配合着auth使用

get_host()           # 获取真实地址
get_full_path()      # 获取路径，不包含域名
build_absolute_uri() # 获取完整路径
is_secure()          # 如果是https返回true，否则false
is_ajax()            # 是否是ajax请求

return JsonResponse(error, status = 422)	# 返回指定状态码
ip = request.META.get('REMOTE_ADDR')	# 获取用户IP
return HttpResponseRedirect('/')		# 重定向
```

## 路由与视图

- **url**: web访问请求的入口(相当于Laravel里的路由)
- **view**：应用的逻辑部分，从客户端接收请求，处理并返回数据，一般返回到template模板进行渲染(相当于Laravel里的控制器) 

```python
# 定义路由
from django.urls import include, path, re_path
urlpatterns = [
    path('test/', myapp.views.test),	# 直接指定路由所对应的views方法
    path('test1/', myapp.views.test, APPEND_SLASH=False),	# APPEND_SLASH默认为True，会使用301自动处理末尾的反斜杠，当然如果是API请求是不会自动重定向的，可以这样做re_path('test(\/)+')
    path('db/', include('myapp.urls')),	# 指定某个路由前缀所对应的urls文件，非常适合app。实现了路由分组的功能
    re_path(r'^table/(?P<table_name>[a-zA-Z0-9-_]*)$', views.table),
,	# 正则匹配，url传递参数，接收时只需要def test1(request, name)即可
    path('abc', myapp.views.test2),
    path('aaa', include('myapp.urls'), namespace='myapp')	# 命名路由
]

# myapp.urls.py
app_name='myapp'	# 命名路由
urlpatterns = [
    path('aa', name='a')	# 这样可以{% url 'myapp:aa'  %}
]
```

## 数据库
Django同很多框架一样使用了ORM(Object Relational Mapping，对象关系映射)的方式，每个model类代表一张数据库的表，每一个属性代表其一个字段(这种特性的实现依赖于python的元类)。 

- 多数据库配置，参考[django多数据库配置](https://blog.csdn.net/songfreeman/article/details/70229839)，主要是在Meta里面添加`app_label`进行标识，然后我的建议是app_label直接和数据库名相同，这样就不用单独写配置关系`DATABASE_APPS_MAPPING`了

- 方法二：使用单独的查询语句指定单独的数据库

  ```python
  UserModel.objects.using(dbname).all()
  ```

- 方法三：使用DB Router

  ```python
  # 指定读写规则
  class CasaRouter:
      def db_for_read(self, model, **hints):
          if 'replica1' in settings.DATABASES:
              return random.choice(['replica1'])
          return random.choice(['default'])
  
      def db_for_write(self, model, **hints):
          """ Always return primary """
          return 'default'
  
      def allow_relation(self, obj1, obj2, **hints):
        """Django默认是返回的None，None的话在大多数情况是正确的，表示只有当两个记录在同一个库查询的时候才能进行关联查询"""
          return None
  
      def allow_migrate(self, db, app_label, model_name=None, **hints):
          return True
  ```

### 数据表定义

- Django需要每张表都得有一个`primary_key=True`，如果没有指定，那么会默认假设你的表里面有一个`id`列，并且是`primary_key`
- `ForeignKey`等外键的定义是可以使用model名称字符串的，而不用引入，因为引入经常会因为交叉引入而报错
- 自定义的`manager`封装的是一些动态方法，并不是静态方法，是作用于`objects`上面的

定义model的文件是`project/app/models.py`里面，例如，要定义一张用户表：

```python
fromo django.db import models
class User(models.Model):
	username = models.CharField(max_length = 20, verbose_name="注释")
	create_time = models.DateTimeField(auto_now_add = True)	# 注册日期字段，如果同时有两个字段对应着同一个外键，那么久得重命名字段名了，比如：
	receiver = models.ForeignKey('Users', null=True, related_name='receiver')	# 数据库里面自动就是receiver_id
	poster = models.ForeignKey('self', null=True, related_name='poster')	# self表示关联自己，
	
	def __str__(self):
		'''这个函数可以用于str(obj)函数来输出该对象的信息，默认是表名'''
		return self.username
    
    class Meta:
        db_table = '自定义表名'
        unique_together = ('column_1', 'column_2')	# 联合唯一键
```
当建立好models过后，执行如下命令就可以在数据库中新建或更新数据表了：

```shell
python manage.py makemigrations	# 检测所有的model更改，自动生成相应的migrations文件到migrations目录下面去
python manage.py makemigrations APP名称	# 为指定的APP执行migration
python manage.py migrate	# 应用migration
```

注：如果是有修改的，那么新添加的数据必须要允许null或者设置默认值，否则会报错，这其实是为了保护已经存在了的数据，当然在添加完该字段后把null去掉再更新数据库就可以了。
### 字段类型
注：Django默认为每张表设置了一个int(11)的自增主键，不需要自己去定义了。
#### 字段通用参数

```python
primary_key = False/True   # 是否设置为主键
blank = False/True         # 是否可为空，这其实是用于Field的判断
null = False/True          # 是否可为空，这才是真正的数据库里面是否可以为null
max_length = 3             # 最大长度，对整型无效
default = ''               # 设置默认值
verbose_name =             # 相当于备注，如果没给出那么就是该字段,当然，要指定的话，可以直接第一个参数一个字符串就可以指定了，当然，这里并不会在migrate的时候数据库里面写上备注
editable = False/True      # 是否可编辑
unique = False/True        # 是否唯一
auto_now = False/True      # 用于时间，每次更新记录的时候更新该字段
auto_now_add = False/True  # 用于时间，创建新纪录的时候自动更新该字段
choices # 很实用的一个功能，相当于存储一个枚举列表，其中左边的key是实际存储在数据库中的值，例如，可以这样定义一个字段：
	YEAR_IN_SCHOOL_CHOICES= (
		('FR', 'Freshman'),
		('SO', 'Sophomore'),
		('JR', 'Junior'),
		('SR', 'Senior'),
	)
	然后在定义字段的时候给个参数choices=YEAR_IN_SCHOOL_CHOICES，在插入字段的时候，使用'RF'这样的，在获取字段值的时候这样{{ p.get_year_in_school_display }}即可显示'Freshman'
```
#### 常用类型

```python
# 数字类型：
AutoField		# 自增长字段
IntegerField	# 长度为11的整数
PositiveIntegerField：
SmallIntegerField
PositiveSmallIntegerField
BigIntegerField：
BinaryField：
BooleanField：
NullBooleanField：
DecimalField(max_digits = None, decimal_places = None)
FloatField

# 字符类型
CharField	# 字符串类型，可用max_length指定长度，枚举类型也使用该方式，只需要指定枚举枚举元组即可，例如type = models.CharField('类型', choices=CONTENT_TYPE)，其中CONTENT_TYPE=(('a', 'abc'))
TextField：text类型
CommaSeparatedIntegerField：用逗号分隔的整数，我擦，这有用

# 时间类型
## USE_TZ=True(默认)时，Django内部都使用的是UTC时间，数据库中看起来比当前时间少8小时(DateTime和TIMESTAMP都会这样，因为TIMESTAMP在insert的时候是用的字符串那种形式插进去，所以TIMESTAMP的真实时间也是改变了的)。Django之所以这样做是为了统一内部的转换，这样只有在前端显示的时候需要进行时间转换。当然如果你想使用TIMESTAMP字段，就把USE_TZ=False，这样，在数据库里面存储的才是真实的时间戳，但是其他的地方可能就要自己去转换了，我反正喜欢使用TIMESTAMP，否则数据库里面的时间看起来少8小时，别扭。唉，DateTime不包括时间的时区信息，这也是其一个弊端。
DateField	# DATE类型
TimeField	# datetime.time，时间
DateTimeField()	# DATETIME类型，包括了日期和时间，需要注意的是Django默认的TIME_ZONE是UTC，在初始化的时候，格式如"2015-04-27T15:01:00Z"，它属于python里面的datetime.datetime类型，可分别用year/month/day等获取时间。
unique_for_date属性：比如，如果有一个title字段，其有一个参数unique_for_date = "pub_date"，那么该表就不会出现title和pub_date同时相同的情况，其它的还有unique_for_month,unique_for_year

其它很有用的类型：
EmailField：Email邮箱类型
FileField：文件类型，不过不能设置为primary_key和unique，要使用该字段还有很多需要注意的地方，具体的见官方文档
FilePathField：同上
ImageField
IPAddressField：从1.7开始已经不建议使用了，应该使用下面这个
GenericIPAddressField：
URLField
UUIDField
```

### 数据库SQL操作
要使用model，必须先导入它，例如`from app.models import Blog`，一条记录就是一个model类的实例，要获取其字段值，直接用点号访问即可，例如有Blog对象blog，那么可以直接用blog.userName访问其值。

####  原生SQL

- 任何时候使用`raw`方式查询，都有sql注入的风险，需仔细检查
- 变量使用`%s`的方式进行传递，否则有注入风险。但是这种方式只支持传value，表名、字段名这些都不支持用这种方式传递，否则会在它们两边加上多余的引号等

```python
# 获取原始SQL语句
from django.db import connection
print(Blog.objects.filter(name="").query)	# 这样可以将SQL语句打印出来，但是这种方法只能输出select的语句，写操作的语句无法打印，只能用下面的方法
connection.queries			# 会返回一个所有执行过的SQL的列表，并且每条时一个字典，包含了SQL语句以及SQL所执行的时间

# 执行原生SQL语句
from django.db import connection
with connection.cursor() as cursor:	# connection['my_db_alias'].cursor()指定另外的数据库
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()
    
# 在model对象上执行原生sql
Person.objects.raw('SELECT * FROM mypersontable')	# 这样子的返回结果，依然会像Person.objects.all()一样映射到对象上面去
Person.objects.raw('SELECT * FROM mypersontable', translations={'first': 'first_name'})	# 支持自定义与对象的映射关系

# 执行原生sql语句返回的是记录值，并不能像对象那样在返回值的同时返回字段名，如果想要同时获得字段名，可以通过如下的方式进行获取
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
```

#### 查询记录

- `model`对象转换为json，但是对于特殊的字段，例如文件字段依然不能正常转换，最好还是自己写个`transform`去转换

  ```python
  from django.forms.models import model_to_dict
  
  # 方法一
  model_to_dict(blog)
  model_to_dict(blog, ['id', 'name'])	# 可以只取指定的字段
  
  # 方法二
  result = django.core.serializers.serialize('json', some_queryset)
  ```

- `Blog.objects.all()[3:30]`只取出部分数据，相当于limit，并不会查处全部

- 偶尔使用自定义的查询条件: `Model.objects.extra(where['FIND_IN_SET(1, field)])`

- `get`方法如果找不到默认会报错，可以使用`try except`或者使用`filter(id="").first()`进行不报错处理，效果差不多

```python
Blog.objects.all()   		# 获取该表的所有记录，返回的是记录对象组成的列表
Blog.objects.get(pk=1)      # 根据主键获取数据
Blog.objects.get(name="")  	# 只会找到第一个匹配的数据，找不到就报错
Blog.objects.filter(name="")# 这个就会找到匹配的多个数据
Blog.objects.filter(~Q(name=''))	# 不等于
Blog.objects.all().exclude(id=7)  		# 排除，即不等于，同上
Blog.objects.filter(name__contains="") 	# 模糊查找name字段的值，返回列表
Blog.objects.filter(name__in=[])	# in操作
BLog.objects.filter(id__range=[3, 8])	# between操作
Blog.objects.order_by("字段1", "-字段2")  # 排序，order_by不加任何参数表示不需要排序，前面加减号表示逆序
Blog.objects.all().order_by("字段")
Blog.objects.count()     				# 返回记录总数

Blog.objects.values('id', 'name')  		# 相当于select id name from Blog，返回的事是一个字典
Blog.objects.values('name').distinct()  # distinct在django的mysql引擎中无法对field进行distinct操作，所以需要这样做
Blog.objects.values_list('id', flat=True)# 查询该字段的所有值并且返回的是id的列表，而不是包括了名字的字典
Blog.objects.all().defer('title')		# 不取某个字段，这里返回是一个model对象
Blog.objects.all().only('title', 'field1')		# 仅仅取某个字段，也是返回一个model对象
Blog.objects.all().values_list('title')	# 仅仅取某个字段，这里返回一个元组

Blog.objects.first()	# 获取第一条记录，如果没有使用order by，那么默认是order by主键
Blog.objects.last()	# 和fitst相反
Blog.objects.latest('id', '-expire_data')  				# 根据某个字段查找其最后一条记录，返回的是一个对象，不是id，类似于last()
Blog.objects.earest('id', '-expire_data')	# 和latest正好相反，取最早的一条记录
Blog.objects.filter(time__gte = '2015-07-23', time__lte = '2015-07-24') # 大于等于并且小于等于，不加e表示不能等于
Blog.objects.filter(time__isnull = True)# 判断某个字段是否为空
Blog.objects.filter('time__year': '2015', 'time__month': '08', 'time__day': '17')：按年月日查询日期，可仅查询其中某一个条件

# Q查询，可以对关键字参数进行封装，可以使用&,|,~等操作
from django.db.models import Q
Blog.objects.filter( Q(name__startswith='wang') | ~Q(name__startswith='hao') )
Blog.objects.get( Q(name__startswith='wang'), Q(name__startswith='hao')) # 逗号就可以直接表示and了
        print(People.objects.filter(
        (Q(birth_lunar__month=old_month) & Q(birth_lunar__day=old_day)) |
        (Q(birth_new__month=new_month) & Q(birth_new__day=new_day))
    ).query)
```

#### 新增记录

```python
post = Blog(userName="wanghao", userId=12)
post.save()
# create方法可以一行搞定
post = Blog.objects.create(userName="aaa")

# 批量插入/新增
posts = []
for i in title:
	posts.append(Posts(title = title))
Posts.objects.bulk_create(posts)
```

#### 更新记录

```python
Blog.objects.filter(id=1).update(userName="new")	# 批量更新
Blog.objects.filter(id=1).update(**mydict)	# 字典更新
post.abc = 'test'
post.save()	# 更新一条数据

Blog.objects.all().update(userName="new")  # 还可以批量更新
obj, created = Posts.objects.update_or_create(title='wang', defaults = updated_values)   # 1.7之后可以用这种方法来更新或者创建一个，如果没找到对象，那么就新建，新建或者更新的字典是defaults的值，返回值中，obj表示该对象，created是一个布尔值
get_or_create(title='wang', defaults=\{\})：获取或者新建
```

#### 删除记录

```python
Blog.objects.get(userName="xiao").delete()
Blog.objects.all().delete()
Blog.author.through.objects.filter(author = author.id).delete()  # 删除多对多关系，仅仅是删除关系，而不是删除对象
```

### 数据约束
#### ForeignKey

- 如果是面向用户的数据最好别在数据库层面使用强制的外键约束，如果仅仅是在model中定义倒没啥

  ```shell
  CASCADE # 默认选项，级联删除
  PROTECT	# 保护模式，删除时候会报错ProtectedError
  SET_NULL # 置空，删除的时候，外键字段被设置为空
  SET_DEFAULT	# 删除时设置为默认值
  SET()	# 自定义一个值
  ```

例如：

```python
# modles.py
class System(models.Model):
	name = models.CharField(max_length = 20)

class Server(models.Model):
	ip = models.GenericIPAddressField(default = '127.0.0.1')
	system = models.ForeignKey(System, on_delete=models.DO_NOTHING) # 不使用外键约束的时候这里on_delete直接DO_NOTHING即可
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING)	# self表示关联自己

# views.py里面这样子使用
server = Server.objects.get(id=1)
server_system = server.system.name # 这样就可以获取到那个name了
```
#### OneToMany(hasMany)
一对多关系，同样使用ForeighKey实现，例如

```python
# 在models.py中定义
class Posts(models.Model):
	title = models.CharField('标题', max_length = 50)

class Comments(models.Model):
	post = models.ForeignKey(Posts, related_name = 'comments_set')

# 在views.py中这么用
post = Posts.objects.get(pk = 1)    # 获取一篇文章
comments = post.comments_set.all()  # 获取该文章的所有评论，是一个列表
```
#### ManyToManyField
多对多关系，有一种特殊情况，如果需要对这种关系添加额外的字段，可以使用through，添加额外的表来表示，例如，用户一张表，被使用的物品一张表，用户与物品是多对多的关系，但是有时候我们需要记录下用户使用该物品的一些其他属性，比如使用了多少次什么的，这时候就需要给这个多对多关系添加额外的字段来表示，那就需要添加额外的表了，示例如下：

```python
# 有中间表的情况
class User(models.Model):
	username = models.CharField(max_length = 20)
	goods = models.ManyToManyField(to='Goods', through='user_goods')

class Goods(models.Model):
	goodsname = models.CharField(max_length = 20)

class user_goods(models.Model):
	user = models.ForeignKey(User)
	goods = models.ForeignKey(Goods)
	clicks = models.IntegerField('点击量', default=0)
    
user = User(id=1)
user.goods.all()	# 获取所有的多对多东西
user.goods.filter(user_goods__clicks=123).all()	# 筛选表/筛选中间表的时候，使用类名的全小写加双下划线再加字段名即可
user_goods.objects.create(user=User.objects.create(), goods=Goods.objects.create(), clicks=2)	# 有中间表的情况只能每张表里面的记录单独创建，并且同样不能使用remove方法进行删除，也只能单独删除，或者用clear批量清空
```

#### OneToOneField
必须是一对一，而不是多对一或一对多

```python
# 需要注意的是OneToOneField在反差的时候必须保证有数据存在，如果不存在则会报错RelatedObjectDoesNotExist，可以在使用的时候在封装一下
def the_user(self):
    return user if hasattr(self, 'user') else None
```

#### OneToDifferentModel(Generic relations)

- 类似于`Laravel`种的多态关联，一个对象可以同时与多个不同的model进行关联

```python
# 例如有一张评论表，可以给商家评论，也能给用户评论
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)	# 评论发表者
    comment = models.TextField()	# 评论内容
    
    # 下面是定义关联，其中content_type是与ContentType关联，这是DJango内置的模型，里面包括了表信息；而object_id就是目标model的主键id
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()	# conent_object则是目标对象
    
comment = MediaFile.objects.first()
comment.content_object	# 这样可以获取该评论的目标，如果是商家则返回商家model，如果是用户则是用户model

# 而如果要在评论对象那边反查(反向关联)，则可以在对象那边定义这样一个属性
comments = GenericRelation(Comment)
```

### 分页

- 自带的分页功能有严重的性能问题，是一次性取出所有数据再从中取出某一页的方式，十分不推荐
- 可以自己写分页功能，分两条sql，一条`COUNT`，另外一条则是`LIMIT/OFFSET`，惰性执行可以直接写成`Contacts.objects.all()[0:20]`，这同样没有取出所有


```python
# 自带的分页功能，一次取出所有
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 导入模块
def listing(request):
	contact_list = Contacts.objects.all()   # 获取所有model对象
	paginator = Paginator(contact_list, 25) # 第二个参数是每页显示的数量
	page = request.GET.get('page')          # 获取URL参数中的page number
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:                # 若不是整数则跳到第一页
		contacts = paginator.page(1)
	except EmptyPage:                       # 若超过了则最后一页
		contacts = paginator.page(paginator.num_pages)

	return render_to_response('list.html', {"contacts": contacts})
```

虽然contacts是一个Page对象，但是在模板中仍然可以使用for循环对其进行遍历，它其实是一个对象所组成的list。下面是分页按钮html模板例子：

```html
<nav>
	<ul class="pagination">
		<li class="{% if current_page == 1 %}disabled{% endif %}"><a href="#" aria-label="Previous"><span aria-hidden="true"></span></a></li>
		{% for index in page_index %}
			{% if index == current_page %}class="active"{% endif %}<a href="#";{{ index }}<span class="sr-only"(current)/</span></a></li>
			{% endfor %}
		<li class="{% if current_page == num_pages %}disabled{% endif %}<a href="#" aria-label="Previous"><span aria-hidden="true"></span></a></li>
	</ul>
</nav>
```
### 初始化数据

为了方便迁移,让别人使用你的APP,有时候需要为APP里面的表提供demo数据,这时候就需要预先填充一些数据.这里使用Django的fixtures方式填充(Django提供两种[填充方式](https://docs.djangoproject.com/en/1.8/howto/initial-data/))。使用JSON格式，我们可以首先使用`manage.py dumpdata data.json`方式到处原来数据库中内容看看该格式，类似如下：

```json
[
	{
		"fields": {
		"userName": "小豪",
		"title": "第一篇文章",
		"userId": 1,
		"update": "2015-04-27T15:01:03Z",
		"datetime": "2015-04-27T15:01:00Z",
		"content": "这是文章的内容"
		},
		"model": "digital.blog",
		"pk": 1
	},
	{
		"fields": {
			"userName": "笑总",
			"title": "第二篇文章",
			"userId": 2,
			"update": "2015-04-28T15:01:03Z",
			"datetime": "2015-04-28T15:01:03Z",
			"content": "这是文章的内容吗"
		},
		"model": "digital.blog",
		"pk": 2
	},
]
```
我们可以自己按照这个模板新建填充数据，其中pk指的是主键值。当建立好json文件过后，执行`python manage.py loaddata data.json`即可导入数据。

## Validator验证

- `Django`自带的一些验证工具是可以直接使用的，例如`RegexValidator('^[0-9]*$')(123)`，验证不通过会直接报错`ValidationError`

## 日志

`Django`定义了Python自带的`logging`模块，我们可以在配置里面配置非常个性化的日志处理方式。例如

```python
# 在settings.py里添加如下配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,	# 这里可以设置为不覆盖本来的配置，这样以前的日志，例如访问日志，就能按照以前的方式进行输出
    'formatters': {	# 自定义输出格式
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'handlers': {	# 定义日志处理的方式
        'custom_file': {
            'level':'DEBUG',					# 超过指定的level级别的才会输出
            'class':'logging.handlers.RotatingFileHandler',	# 日志输出到文件并自动轮转
            'filename': '/tmp/uwsgi-app.log',     # 日志输出文件
            'maxBytes': 1024*1024*5,              #文件大小
            'backupCount': 5,                     #备份份数
            'formatter':'standard',               #使用哪种formatters日志格式
        },
        'custom_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',	# 日志输出到控制台
            'formatter': 'standard'
        }
    },
    'loggers': {	# 定义各种logger，可以选择logger需要使用哪些handlers
        'custom': {
            'handlers': ['custom_file', 'custom_console'],
            'level': 'DEBUG',			# 超过该level级别才会进行处理
        }
    }
}
```

使用时，只需要这样做

```python
import logging
logger = logging.getLogger('custom')	# 获取指定的logger
logger.error('error')
logger.exception('error')	# 该方法会同时打印出调用栈
```

## Template: Django模板

和所有的MVC框架一样，模板功能是必须有的。这里介绍一下Django模板的使用方法。

### 模板定义
为了方便管理，最好在app的目录下新建templates文件夹用于存放模板文件，然后在project的配置文件settings.py中指明模板文件夹的位置:

```python
TEMPLATES['DIRS']这个变量中添加即可，比如
'DIRS': [
	os.path.join(BASE_DIR, 'dashboard/templates').replace('\\', '/'),
]
```

这样，在该app的view中就可以这样使用templates下的test.html模板文件了。例如：

```python
def test(request):
	return render(request, 'test.html')
```
### 参数传递
要向模板中传递参数，可以给render添加第三个参数，该参数其实是一个字典，在模板中可以直接使用该字典的key，例如：
```python
return render(request, 'test.html', {'name1': value1, 'name2': value2} )
```
这样，在模板文件test.html中就可以直接`{{ name1 }}`来使用`name1`的值了。

### 继承与引用
模板方便之处就是可以使用继承将代码分块并且将重复的地方都写在一个`base.html`里。当要实现继承的时候在html文件第一行写上

```django
{% extends 'base.html' %}
```

然后分别实现其区块即可。 在base模板中一般这样定义区块：

```django
{% block 块名 %}
	这里直接写html代码
{% endblock %}
```

如果子模块没有定义某个block的内容，那么就采用父模板的，如果需要使用父模板的内容可以用`{{ block.super }}` 
模板也可以通过引用其它模板的代码，例如，在要引用的地方使用：

```django
{% include 'nav.html' %}
{% include 'includes/nav.html' %}
```

### 静态文件css、js、img
静态文件一般当然是要存放在自己的app里面，这时候，就应该指定静态文件的路径在project的配置文件`settings.py`中添加如下配置：

```python
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    'f:/project/app/static', # 无论是windows还是linux都要用左斜杠哟
)
```

在模板中使用静态文件就这样：

```html
{% load staticfiles %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">

{% load static %}
<body data-media-url="{% get_media_prefix %}">	# 获取media前缀路径
```

### 模板标签
Django内置了一些比较常用又实用的标签：

```django
# 变量
{{ names.0 }}	# 通过下标获取列表变量的值
{% request.GET.key %}	# 直接读取request
{% request.get_full_path %}# 模板里面获取当前url路径

# 注释
{# 单行注释 #}
{% comment %}多行注释{% endcomment %}

# url路由
url(r'^blog/', 'myapp.views.blog'), # 博客页面的路由
{% url 'digital.views.blog' %}	# 嵌入路由
url(r'^blog/', 'myapp.views.blog', name='blog')	# 使用命名路由
{% url 'blog' %}	# 嵌入命名路由
url(r'^oauth/', include('oauth.urls', namespace='oauth'))	# 第三方APP的路由
{% url 'oauth:hello' %}

# for循环
{% for <element> in <list> %}{% endfor %}
{% for <element> in <list> reversed%}{% endfor %} 反向迭代列表
{% for <element> in <list> %}{% empty %}{% endfor %} 列表为空时的输出内容
{{ forloop.counter }}	# 获取当前索引，默认从1开始
{{ forloop.counter0 }}	# 获取当前索引，从0开始

# if语句
{% if <element> %}
{% elif <element> %} 
{% else %}
{% endif %}

{% ifequal 变量1 变量2 %}
比较值
{% endifequal %}
##ifnotequal同上
  
# with语句(QuerySet不能用last)
{% with list|last as last_item %}
  {{ last_item }}
{% endwith %}
```

### 过滤器
可以直接格式化输出，是一种最便捷的转换变量输出格式的方式。

```django
{{ today | data: "Y m d" }}	# 格式化输出时间
{{ content | safe}}				# 输出富文本，不对html转义
```
这里是常见的过滤器：

```html
add：将该数字加上一个数字，例如 {{ value|add:"2" }}，如果原来的值为4，那么新的值就为6，不仅进可以作用与int，还能作用与列表，将列表中每个值都加
addslashes：添加反斜杠到需要转义的地方前
capfirst：第一个字母大写
center：在字符串前后加空格，并让该字符串位于中间，例如 `{{ value|center: "5" }}`，那么输出时前后都是5个空格
cut：去除字符串中的指定字符，例如`{{ value|cut:" " }}`，表示去除字符串中的所有空格
date：按指定的格式字符串参数格式化date或者datetime对象，参数太多了，看[文档](https://docs.djangoproject.com/en/1.8/ref/templates/builtins/)
default：参数没赋值的情况下给定默认值，例如`{{ value|default: "nothing" }}`
default_if_none：如果它是none就给定默认值
dictsort：将一个字典组成的列表排序，例如`{{ value|dictsort:"name" }}`意思是将value这个列表里面的字典按照字典里的name的顺序来排序
dictsortreversed：与上面顺序相反
divisibleby：是否能被整除，返回True/False，例如`{{ value|divisibleby:"3" }}`
filesizeformat：-h方式输出文件的大小，例如`{{ value|filesizeformat}}`，如果value=123456789，那么输出将是117.7MB
first：返回列表的第一个值
floatformat：设置浮点数的显示形式
get_digit：获取一个整数的倒数第几个数字，例如`{{ value|get_digit:"2" }}`,那么123456789的值为8
join：将一个列表的值添加一个分隔符并以字符串形式输出，例如`{{ value|join:"//"}}`那么['a', 'b', 'c']输出将是"a//b//c"
last：返回列表的最后yield值，由于QuerySet没有[-1]索引获取元素的方法，所以无法使用with获取最后一个元素。需要这样做: {% for obj in queryset%}{% if forloop.last %}{{ obj.key }}{% endif %}{% endfor %}
length：返回变量的长度，也可以在if语句里面使用，例如 {% if messages|length >= 100%} ...{% endif %}
length_is：判断一长度是否是某个值，例如`{{ vlaue|length_is:"4" }}`如果value长度是4那么就返回True
linebreaks：替换换行符，例如如果value的值是Joel\nis a slug，那么输出就是<<p>Joel<br /> is a slug</p>
linenumbers：在输出的tex前加上标号
ljust：在字符串后面加上指定长度的宽度，例如`{{ value|ljust:"10" }}`
make_list：将整型或字符串转换为单个单个的列表元素组成一个列表
random：在列表里面随机选取一个元素
lower：转换为小写
rjust：在字符串前面加上指定长度的宽度
slice：列表分片，例如`{{ some_list|slice:":2"}}`就表示前面两个元素，可以用它来实现startswith，endwith等功能
slugify：
stringformat：
striptags：取出HTML中的tag，只去内容
time：同date
timesince：
timeuntil
title：将一个字符串转换为title的形式，即一般的第一个字母大写那种标题
truncatewords: "30"：表示只显示前面30个字符
truncatechars_html：
truncatewords：显示前面多少个字符，单位是词，而不是字符
truncatewords_html：
unordered_list：
upper：转换为大写
urlencode：将url进行编码，例如"http://www.example.org/foo?a=b&c=d"被编码为“http\%3A//www.example.org/foo\%3Fa\%3Db\%26c\%3Dd”
urlize：
urlizetrunc：
wordcount：统计字符串中单词的数量
wordwrap：指定特定的长度来分隔字符串
yesno：
```

常用过滤器组合:

```django
{{ user.name.split|join:"_" }}	// 将空格转换为下划线
```

### 其他标签

```django
# autoescape标签
{% autoescape on %}       # 去掉自动转义
{{ body }}
{% endautoescape %}

# cycle标签：每次使用该标签，标签中的值就会变化，比如下面这个，第一次该值为row1，第二次则为row2，第三次又变为了1，感觉可以用于循环里面的奇偶什么的
{% for o in some_list %}
<tr class="{% cycle 'row1' 'row'2 %}"
...
</tr>
{% endfor %}

# now 标签，直接将当前时间按指定格式输出：
{% now "jS F Y H:i" %}

# spaceless标签：移出HTML tags之间的空白
{% spaceless %}
<p>
...
</p>
{% endspaceless %}

# verbatim：停止模版引擎，一般用于在模板里面写Javascript什么的
{% verbatim %}
...
{% endverbatim %}

# with标签：和语法里面的with类似
{% with total=business.employees.count %}
{{ total }} employee{{ total|pluralize }}
{% endwith %}
```

## [DJango Admin后台管理](https://haofly.net/django-admin)

## [Django Form表单系统](https://haofly.net/django-form)

## 用户管理功能

### 扩展/自定义用户表

- 注意扩展用户表必须在项目最开始的时候做，否则在migrate的时候会[报错](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project)

Django默认通过`django.contrib.auth`提供用户认证相关功能，用户表默认为`auth_user`，但是如果我们想要使用给自己的用户表用于认证，但是又能用到django原有的认证功能，那么可以这样扩展用户表：

```python
# 在app的models里面建立一个新的model
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    custom_field = models.CharField(default='custom', null=True)	# 需要注意的是自己新添加的字段必须为NULL或者存在默认值，否则，使用命令创建用户时会报错
    
# 新建model以后，只需在settings.py中指定用户认证MODEL即可
AUTH_USER_MODEL = 'app.User'
```

### 用户登录相关功能

```python
# 创建用户，如果是自建的User，那么应该引入自己的User model
from django.contrib.auth.models import User
user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
user.save()

# 验证用户登录
from django.contrib.auth import authenticate, login
user = authenticate(username='hao', password='test')
if user is not None and user.is_activate:
    print('认证成功')
    login(request, user)	# 写入session，存储用户状态

# 判断用户是否已经登录
request.user.is_authenticated

# 退出登录
from django.contrib.auth import logout
def logout_view(request):
	logout(request)
    
# 给路由添加限制用户登录的功能，这会让未登录用户重定向到settings.LOGIN_URL去
from django.contrib.auth.decorators import login_required
@login_required
def my_view(request):
    ......
```

### 自定义登录验证功能

有时候，我们可能想使用邮箱验证，而不是用户名，那么我们可以自己建立一个认证后台，例如`backends.py`

```python
from django.conf import settings
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(object):
	def authenticate(self, username=None, password=None):
		if '@' in username:
			kwargs = {'email': username}
		else:
			kwargs = {'username': username}
		try:
			user = User.objects.get(**kwargs)
			if user.check_password(password):
				return user
			except User.DoesNotExist:
				return None

def get_user(self, user_id):
	try:
		return User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return None</pre>
```

然后在settings.py中添加如下代码：

```python
# 该字段指定了默认的验证后台，从上到下顺序验证，如果上面验证不成功就验证下面的
AUTHENTICATION_BACKENDS = (
	'myapp.backends.EmailOrUsernameModelBackend',   # 自定义的认证后台
	'django.contrib.auth.backends.ModelBackend',    # 这是默认的认证后台
)
```
这样，就可以依然使用刚才的代码对用户登录进行验证了。

## media文件处理

- 如果要在`template`里使用`MEDIA_URL`变量，那么需要在配置文件的`TEMPLATES->OPTIONS->context_processors`添加`django.template.context_processors.media`
- `media`和`static`一样，都只能在`DEBUG=True`的时候生效，在线上环境，这两者都是使用的服务器进行代理静态文件
- 用户上传的文件一般叫做media，可以在`settings.py`里面添加如下配置定义其目录

```python
MEDIA_URL = '/media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

- 在model里面，可以直接定义某个字段上传到的路径:

```python
class Post(models.Model):
    pic = models.FileField(upload_to='upload/pic')	# 这样在后台的admin里面该字段会变成上传文件并且会自动上传到该目录，数据库里存放的则是其路径，例如'upload/pic/test.png'
```

## Channels

用于与websockets通信

## signal

[参考](http://www.weiguda.com/blog/38/)django中signal与操作系统的signal是完全不一样的.Django的signal是一种同步的消息队列.通常在以下情况进行使用：

- signal的receiver需要同时修改对多个model时
- 将多个app的相同signal引到同一receiver中处理时
- 在某一model保存之后将cache清除时
- 无法使用其他方法, 但需要一个被调函数来处理某些问题时
- 作为网站的通知

## [Django部署](https://haofly.net/django-deploy)

## [自定义存储系统/七牛云存储](https://haofly.net/django-storage)

### Django缓存系统

能够缓存视频或者模板片段或者API。

## Django测试

- 可以使用`python manage.py shell`进入shell终端直接访问项目中的各种对象

- 如果想要在正式的数据库中测试数据，而不是让测试工具自己创建一个新的数据库，可以在`settings.py`中这样指定测试数据库，但是需要注意的是一定要加`--keepdb`选项，否则可能删除掉原来的数据库

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'test',
          'USER': 'root',
          'PASSWORD': 'test',
          'HOST': '127.0.0.1',
          'PORT': 3306,
          'CONN_MAX_AGE': 0,
          'TEST': {
              'NAME': 'test',	# 与上面的数据库名相同
          }
      }
  }
  ```

- `--keepdb`选项只是防止测试数据库被销毁，但是测试时候执行的其他操作依然都会回滚，如果想要操作数据库不回滚，那么可以在测试类上重载`_rollback_atomics`这个方法:

  ```python
  class MyModelTest(TestCase):
      @classmethod
      def _rollback_atomics(cls, atomics):
          """Rollback atomic blocks opened by the previous method."""
          for db_name in reversed(cls._databases_names()):
              # transaction.set_rollback(True, using=db_name)	# 注释掉这一行即可
              atomics[db_name].__exit__(None, None, None)
  
      def test_get_by_id(self):
          print(MyModelTest.get_by_id(1))
  ```

## Django国际化

- `I18N`表示国际化，`L10N`表示本地化。Django使用的是`gettext`工具进行国际化的翻译。
- 如果编译过后依然不生效，那么把`*.po`里面的`fuzzy`删掉，再不行就重启`uwsgi`进程

为了实现国际化我们需要这样做：

1. 将需要翻译的字符串在源码中进行标注

   ```python
   from django.utils.translation import gettext as _
   
   def test(request):
       return HttpResponse(_("test"))
   ```
   如果是在模板中，需要这样标记

   ```django
   {% load i18n %}
   <title>{% trans "test" %}</title>	# 字符串必须加引号
   <title>{% trans 变量 %}</title>
   ```

2. 在`settings.py`中配置并新建国际化文本存放目录，即个目录`locale`目录

   ```python
   LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
   ```

3. 生成指定语言的文件目录，这条命会扫描Django项目源文件，将其中标记为需要翻译的字符串抽取出来，统一放在`locale/zh_hans/LC_MESSAGES/django.po`这个文本文件里面

   ```shell
   # 支持的语言列表：http://www.i18nguy.com/unicode/language-identifiers.html
   python manage.py makemessages -l zh_Hans	# 简体中文，需要注意的是mac上面大小写不敏感，但是linux上面会存在问题，语言文件这里必须大写，并且项目中其他地方用zh-hans
   python manage.py makemessages -l ja		# 日文
   python manage.py makemessages -l ko		# 韩文
   ```

4. 文本文件中会列出我们所有标记了的字符串，你可以在每个字符串下面填上对应的值，例如

   ```shell
   #: web/views.py:15	# 这是字符串抽取的来源
   msgid "test"		# 默认会将字符串放在msgid
   msgstr "测试"			# 这里的翻译需要自己填写
   ```

5. 将`*.po`文件编译成`*.mo`文件

   ```shell
   python manage.py compilemessages
   ```

6. 语言切换相关的方法:

   ```django
   # 获取在settings.py的LANGUAGES=()中定义了的语言列表
   {% get_available_languages as langs %}
   {% for lang in langs %}
   {{ lang.0 }} {{ lang.1 }}
   {% endfor %}
   
   # 获取当前的用户语言，例如zh-hans
   {% get_current_language as LANGUAGE_CODE %}
   {{ LANGUAGE_CODE }}
   ```

#### 切换语言

Django根据以下顺序去决定应该使用哪种语言

- 请求的时候手动更改，这种方法仅用于当前请求:

  ```python
  django.utils.translation.active('en')
  ```

- i18n_patterns: 即直接根据url中的语言来判断

  ```python
  # 在url中这样定义，这样，在访问domain/的时候就可以以domain/zh-hans/的方式访问特定语言了
  path('<slug:slug>/'))
  ```

- request.session[translation.LANGUAGE_SESSION_KEY]，这种方式如果要切换，只需要设置以下即可

  ```python
  request.session[translation.LANGUAGE_SESSION_KEY] = language
  ```

- request.COOKIES[translation.LANGUAGE_COOKIE_NAME]

- request.META['HTTP_ACCEPT_LANGUAGE']，即http的header头中的`Accept-Language`

#### 获取当前语言

```python
request.session[translation.LANGUAGE_SESSION_KEY]	# 如果在session有设置可以从session读
request.COOKIES[translation.LANGUAGE_COOKIE_NAME]	# 如果在cookie有设置可以从cookie读
django.utils.translation.get_language()	# 返回当前使用的语言
get_language_from_request(request)	# 这才是准确的。。。
```

#### 翻译JS中的内容

要支持这种js，必须得我们自己去修改js，所以在引入第三方库时最好不要引入写死语言的，这种方式更多用于我们自己的js。详细步骤如下：

1. 按照上面的方法在js中进行标记

   ```javascript
   gettext('Next');	// js中直接使用gettext来将字符串标记起来
   ```

2. 在根url中添加一个url

   ```python
   from django.views.i18n import JavaScriptCatalog
   
   path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
   path('jsi18n/web/', JavaScriptCatalog.as_view(packages=['web']), name='javascript-catalog')	# 这种方式仅针对某个具体的app进行js文件的饭翻译
   ```

3. 每次在引入需要国际化的js之前，先引入这个js文件，这种文件中定义了gettext等几个翻译的工具。

   ```html
   <script type="text/javascript" src="{% url 'javascript-catalog' %}"></script>
   ```

## 帮助方法

- `django.utils.crypto.get_random_string(length=32, allowed_chars='abcd')`: 生成随机字符串

- 

## django-cron插件

Django下的定时任务插件，我以前用的是`django-crontab`，但是现在觉得`django-cron`更好用，好处是每次执行结果在数据库中都能存储，并且cron中要么是`laravel`定时任务那样的一条，如果要分开则是带了名字的，不再是一行看不懂的字符。

## TroubleShooting

- **如果想要直接执行_./manage.py_来启动runserver**，那么可以修改manage.py文件如下：

  ```python
  #!/usr/bin/env python
  import os
  import sys
  if __name__ == "__main__":
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
      from django.core.management import execute_from_command_line
      sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
  	execute_from_command_line(sys.argv)
  ```

- **保存用户上传的图片或文件**：使用Django自带的文件存储系统：

  ```python
  from django.core.files.storage import FileSystemStorage
  storage = FileSystemStorage(
                      location = '/var/www/site/upfiles',
                      base_url = '/upfiles'
                    )
  content = request.FILES['the_file']
  name = storage.save(None, content)
  url = storage.url(name)
  ```

- **Django模板for循环index**

  ```python
  {% for item in item_list %}
  	{{ forloop.counter }}  {# 从1开始的序号 #}
      {{ forloop.counter0 }} {# 从0开始的序号 #}
  {% endfor %}
  ```

- Django模板对HTML字符串进行转移，如果有一个HTML格式字符串，比如`<strong>haofly</strong>`那么当把它作为一个变量传递到html中区的时候，会原封不动的保留，很明显我们有时候并不想这样，而是真的想将`haofly`进行加粗，可以这样做

  ```python
  {{ variable name | safe}}
  ```

- **migrate的时候出现类似这样的错误：`django.db.utils.OperationalError: (1091, "Can't DROP 'os_id_id'; check that column/key exists")`**，原因是你在试图创建一个已经存在的column或者删除一个已经删除的column，这时候需要在migrate后面添加一个参数忽略这些：`python manage.py migrate —fake`

- **将上传的文件写入到本地，使用chunks()生成器可以将文件一块一块地写入，而不使用read方法，这样可以防止大文件写入失败**:

  ```python
  destination = open('temp/' + filename, 'wb+')
  for chunk in file.chunks():
      destination.write(chunk)
      destination.close()
  ```

- **通过Ajax发送多维数组，原生不支持的，不过可以在前端以及后端同时传输JSON格式的**

  ```javascript
  $.ajax(
    url: 'test',
    datatype: 'json',
    data: JSON.stringify({
    'one': 123,
    'two': {
    'two_one': 'test'
    }
    })
  )
  
  # 在后端使用JSON进行解析
  def test(request):
  data = json.loads(request.POST)
  或者前端不变，后端用这个来接收request.POST.getlist('taskIdList[]')
  ```

- **POST请求发生403错误：`Forbidden (403)  CSRF verification failed. Request aborted.`**: 原因是Django默认给所有的post请求都添加了CSRF验证中间件，要想对某个路由(url)忽略，可以使用csrf_exempt，关于CSRF的其它一些装饰器见https://docs.djangoproject.com/en/2.0/ref/csrf/

  ```python
  from django.views.decorators.csrf import csrf_exempt
  @csrf_exempt
  def webhook(request):
      pass
  ```
  如果要保留csrf以提高安全性，那么可以这样做:

  ```django
  // 在前端响应表单处添加以下标签以生成一个隐藏的input字段，然后前端通过js进行获取，在请求时候将它的value放入header头X-CSRFToken即可
  {% csrf_token %}
  ```

- **ValueError: The database backend does not accept 0 as a value for AutoField.** 这是因为把某个外键的默认值设置为了0，但是外键对应的字段确实一个自动增长的键，这种情况要么把默认值设成大于0的，要么设置为允许NULL

- **TemplateSyntaxError: Could not parse the remainder**: 通常原因是模板标签语法有点问题，比如:

  ```django
  {% if a=='2' %}	# 是错误的，不仅%需要有空格，==两边都得有空格
  ```

- **迁移数据库后即使输入正确的用户名密码也无法进入后台管理**: 重设密码，或者清除cookie即可

- **使用nginx代理静态文件前端静态文件能正常获取，但是管理后台的静态文件都404了**: 原因是没有使用`python manage.py collectstatic`命令将所有的静态文件提取到根目录的`/static`目录下

- **django.core.exceptions.ImproperlyConfigured: Requested setting DEBUG, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing setting**: 需要手动设置`export DJANGO_SETTINGS_MODULE=my_project.settings`，但是如果是下面这种情况依然是不行的

- **DJANGO_SETTINGS_MODULE not working**: 在项目还在初始化的时候，我们应该用`django-admin.py`命令，但是项目初始化完成后我们就应该用`python manage.py`命令来代替，这样才能正确地找到路径


##### 扩展阅读

- [Sasha's Pony Checkup](https://www.ponycheckup.com): 简单的Django网站安全检测

