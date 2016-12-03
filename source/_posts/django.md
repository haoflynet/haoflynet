---
title: "Django教程"
date: 2016-08-07 08:44:39
updated: 2016-11-28 17:03:00
categories: python
---
# Django教程
Python一直是我最喜欢的语言，在这个寒假打算认真学习一下Python的Web框架。在Django和Tornado之间我选择了前者，没有特别的原因，网上人云亦云的，肯定不会有一方离另一方差很远，我就直接去看了看Github上两个项目的活跃度，所以选择了前者。

应该说Django坚持自己造轮子，确实为开发者节约了不少的时间，我很看重它的扩展功能，packages数量十分丰富。Django采用的是最流行也是我最熟悉的
MVC设计模式，虽然在之前的一个PHP(Laravel)项目中也是采用的MVC模式，但一直都没怎么吃透，始终在各层分离的时候不是很清晰，所以也可趁学习Dja
ngo对MVC的概念进行强化。

Django另一个我特别喜欢的特性就是Application，它与Project的概念不同，一个APP就相当于一个功能模块，一个Project可以包含多个A
PP，一个APP可以同时被多个Project引用，App增加了代码的复用机会，提高了扩展性和松耦合性，Django中很多的packages都是以APP的形式
存在的。

另外，我学习主要参考的是开源书籍 [Django搭建简易博客教程](http://andrew-liu.gitbooks.io/django-blog/
"Link: http://andrew-liu.gitbooks.io/django-blog/" )

下面是搭建一个Django环境的基本步骤：

1. [使用Virtualenv搭建Python3的Django环境](http://haofly.net/virtualenv-python-django/)
2. 新建项目 `django-admin startproject 项目名` 这样会在当前目录新建一个目录，里面已经有一些基本的配置文件：

   	django_test
    	├── db.sqlite3
       ├── django_test
       │   ├── **init**.py
       │   ├── **pycache**
       │   ├── settings.py
       │   ├── urls.py
       │   └── wsgi.py
       └── manage.py
3. 新建APP `django-admin startapp APP名称` 如果是搭建一个非常简单的应用，那么不使用APP也行，只需要吧路由指向目标view就可以了，但是如果要搭建复杂的应用并且需要良好的隔离性，那最好使用APP。同样，使用该命令也会在当前目录下新建一个目录，里面已经包含一些配置文件：

   	django_test/testapp
   	├── admin.py
   	├── __init__.py
   	├── migrations
   	├── models.py
   	├── tests.py
   	└── views.py

   如过添加了APP，那么需要在主配置文件`settings.py`里面的`INSTALLED_APPS`里面添加该APP的名称

4. Hello World！ 所有入门教程都必须要有一个Hello World! 首先，在APP的视图文件views.py里添加函数，该函数直接返回一个字符串的响应：

   	from django.shortcuts import render
    	from django.http import HttpResponse

   	def hello(request):
   		return HttpResponse('Hello World!')
   然后添加URL，在Project目录里的`urls.py`里进行管理，添加hello的url如下：

   	from django.conf.urls import patterns, include, url
   	from django.contrib import admin
   	
   	urlpatterns = [
   		url(r'^admin/', include(admin.site.urls)),
   		url(r'^hello/', 'testapp.views.hello'),
   	]
5. 运行 `python manage.py runserver` 如果要以daemon的方式在后台运行，可以使用nohup命令 `nohup python manage.py runserver 0.0.0.0:8000 &gt; log &amp;` 使用它可以打开Django自带的默认Web引擎，可以在 <http://127.0.0.1:8000中查>看 在测试的时候可以使用该引擎，它不仅轻量，而且在打开后还会自动检测代码的更改，进行自动更新，这样就不用每次对代码变动了都来重启一次

## 配置项

	DEBUG = True		# DEBUG模式
	TEMPLATE_DEBUG = True	# TEMPLATE的DEBUG模式
	
	ALLOWED_HOSTS = []   # 设置哪些域名可以访问，当debug为false时必须为其指定一个值，['*']表示允许所有的访问
	
	INSTALLED_APPS = [默认APP+自己的APP]
	MIDDLEWARE_CLASSES = [中间件]
	
	ROOT_URLCONF = 'admin.urls'	# 读取的默认的url文件
	
	# Database 数据库的配置
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}
	
	LANGUAGE_CODE = 'en-us'  # 语言，中文可用zh-Hans、zh-CN，完整列表见：http://www.i18nguy.com/unicode/language-identifiers.html
	TIME_ZONE = 'Asia/Chongqing'        # 时区
	
	# Static files (CSS, JavaScript, Images) 静态文件目录  
	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'static') # 这个选项默认是没有的，在编码时将静态文件放在APP中的static目录下，部署时用python manage.py collectstatic就可以把静态文件收集到STATIDC_ROOT目录

在其他文件访问全局配置项，可以这样访问：

	from django.conf import settings
	settings.DEBUG

## 路由与视图
**url**: web访问请求的入口(相当于Laravel里的路由)
**view**：应用的逻辑部分，从客户端接收请求，处理并返回数据，一般返回到template模板进行渲染(相当于Laravel里的控制器)  
将`/test`定位到article这个APP里面的views里面的home方法来处理的形式

	url(r'^test$', 'article.views.home')
#### url传递参数
Django的路由是采用正则表达式来匹配的，同样能使用命名组，比如`(?P<name>)`，这样就可以通过URL给views传递参数了，例如：

	# 有如下视图
	def hello(request, name):
		return HttpResponse('name is %s', % name)
	# 在url中可以这样写
	url(r'^(?P<name>\\d+)/$', 'testapp.views.hello)
#### url命名
	url(r'^add/$', 'app.views.add', name='add')
给url命名可以方便我们进行统一修改url样式，比如之前用`a-and-b`的url可以访问到add这个方法，但现在如果想改成`a/b`的方式来访问，那么由于后端的模板渲染等都是用的其命名`add`，就无需修改后端逻辑了

#### 路由按照app分组
首先主urls.py里面使用include包含应用下的urls.py文件

	from django.conf.urls import include

	urlpatterns = [
		url(r'^app1', include('app1.urls')),
	]
然后在app1下的urls.py文件里面，进行如下设置:

	from django.conf.urls import url
	from . import views
	
	urlpatterns = [
		url(r'^/$', views.hello),
	]
这样就可以通过`/app1/`，来访问app1下的hello方法了

## Model
Django同很多框架一样使用了ORM(Object Relational Mapping，对象关系映射)的方式，每个model类代表一张数据库的表，每一个属性代表其一个字段(这种特性的实现依赖于python的元类)。 
### 数据表定义
定义model的文件是`project/app/models.py`里面，例如，要定义一张用户表：

	fromo django.db import models

	class User(models.Model):
		username = models.CharField(max_length = 20)	# 用户名字段
		create_time = models.DateTimeField(auto_now_add = True)	# 注册日期字段，如果同时有两个字段对应着同一个外键，那么久得重命名字段名了，比如：
		receiver = models.ForeignKey(Users, null=True, related_name='receiver')
		poster = models.ForeignKey(Users, null=True, related_name='poster')
		
		def __str__(self):
			'''这个函数可以用于str(obj)函数来输出该对象的信息，默认是表名'''
			return self.username


当建立好models过后，执行如下命令就可以在数据库中新建或更新数据表了：

	python manage.py makemigrations
	python manage.py migrate

注：如果是有修改的，那么新添加的数据必须要允许null或者设置默认值，否则会报错，这其实是为了保护已经存在了的数据，当然在添加完该字段后把null去掉再更新数据库就可以了。
### 字段类型
注：Django默认为每张表设置了一个int(11)的自增主键，不需要自己去定义了。
#### 字段通用参数

	primary_key = False/True   # 是否设置为主键
	blank = False/True         # 是否可为空，这其实是用于Field的判断
	null = False/True          # 是否可为空，这才是真正的数据库里面是否可以为null
	max_length = 3             # 最大长度，对整型无效
	default = ''               # 设置默认值
	verbose_name =             # 相当于备注，如果没给出那么就是该字段,当然，要指定的话，可以直接第一个参数一个字符串就可以指定了
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
		然后在定义字段的时候给个参数choices=YEAR_IN_SCHOOL_CHOICES，在插入字段的时候，使用'RF'这样的，在获取字段值的时候这样：p.get_year_in_school_display()即可显示'Freshman'
#### 常用类型

	数字类型：
	AutoField：自增长字段
	IntegerField：长度为11的整数
	PositiveIntegerField：
	SmallIntegerField
	PositiveSmallIntegerField
	BigIntegerField：
	BinaryField：
	BooleanField：
	NullBooleanField：
	DecimalField(max_digits = None, decimal_places = None)
	FloatField
	
	字符类型：
	CharField：字符串类型，可用max_length指定长度
	TextField：text类型
	CommaSeparatedIntegerField：用逗号分隔的整数，我擦，这有用
	
	时间类型：
	DateField
	TimeField：datetime.time，时间
	DateTimeField()：datetime类型，包括了日期和时间，需要注意的是Django默认的TIME_ZONE是UTC，其fixture数据(初始化数据)的时候，格式如"2015-04-27T15:01:00Z"，它属于python里面的datetime.datetime类型，可分别用year/month/day等获取时间
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

#### 数据约束

##### 外键

```python
class System(models.Model):
	name = models.CharField(max_length = 20)
    
class Server(models.Model):
    # 其中on_delete可以模拟SQL的ON DELETE CASECADE的约束行为，并且会删除包含该ForeignKey的对象。on_delete的值可以有CASCADE默认为级联删除，PROTECT抛出ProtectedError以组织被引用对象的删除，SET_NULL，把ForeignKey设置为null，SET_DEFAULT，把ForeignKey的值设置为默认值，SET()，设置ForeighKey为传递给SET()的值，如models.SET(get_sentinel_user)
	system = models.ForeignKey(System, on_delete=models.SET_NULL)	# 对应System的ID，字段名默认为system_id   

# views.py里面这样子使用
server = Server.objects.get(id=1)
server_system = server.system.name # 这样就可以获取到那个name了
```

### 数据库SQL操作

要使用model，必须先导入它，例如`from app.models import Blog`，一条记录就是一个model类的实例，要获取其字段值，直接用点号访问即可，例如有Blog对象blog，那么可以直接用blog.userName访问其值。  
如果想要在执行数据库操作的时候查看数据库的实际的SQL语句，可以这样

```python
from django.db import connection
print(Blogobjects.filter(name="").query)	# 这样可以将SQL语句打印出来

connection.queries			# 会返回一个所有执行过的SQL的列表，并且每条时一个字典，包含了SQL语句以及SQL所执行的时间
```

#### 查询记录

	Blog.objects.all()   # 获取该表的所有记录，返回的是记录对象组成的列表
	Blog.objects.get(pk=1)      # 根据主键获取数据
	Blog.objects.get(name="")  # 只会找到第一个匹配的数据
	Blog.objects.filter(name="")# 这个就会找到匹配的多个数据
	Blog.objects.filter(name__contains="")  # 模糊查找name字段的值，返回列表
	Blog.objects.order_by("字段1", "字段2")   # 排序
	Blog.objects.all().order_by("字段")
	Blog.objects.count()     # 返回记录总数
	Blog.objects.values('id', 'name')  # 相当于select id name from Blog
	Blog.objects.values('name').distinct()   # distinct在django的mysql引擎中无法对field进行distinct操作，所以需要这样做
	Blog.objects.values_list('id', flat=True) # 查询该字段的所有值并且返回的是id的列表，而不是包括了名字的字典
	Blog.objects.latest('id')  # 根据某个字段查找其最后一条记录
	Blog.objects.filter(time__gte = '2015-07-23', time**lte = '2015-07-24') # 大于等于并且小于等于，不加e表示不能等于
	Blog.objects.filter(time__isnull = True)  # 判断某个字段是否为空
	Blog.objects.all().exclude(id=7)  # 排除
	Blog.objects.filter('time__year': '2015', 'time__month': '08', 'time__day': '17')：按年月日查询日期，可仅查询其中某一个条件
	
	# Q查询，可以对关键字参数进行封装，可以使用&,|,~等操作
	from django.db.models import Q
	Blog.objects.filter( Q(name__startswith='wang') | ~Q(name__startswith='hao') )
	Blog.objects.get( Q(name__startswith='wang'), Q(name__startswith='hao')) # 逗号就可以直接表示and了


	        print(People.objects.filter(
	        (Q(birth_lunar__month=old_month) & Q(birth_lunar__day=old_day)) |
	        (Q(birth_new__month=new_month) & Q(birth_new__day=new_day))
	    ).query)
#### 新增记录

	post = Blog(userName="wanghao", userId=12)
	post.save()
	
	# 批量插入/新增
	posts = []
	for i in title:
		posts.append(Posts(title = title))
	Posts.objects.bulk_create(posts)

#### 更新记录

	post = Blog.objects.filter(id=1).update(userName="new") #1.7之前更新单条记录如果要用字典的话就只能这样了
	Blog.objects.all().update(userName="new")  # 还可以批量更新
	obj, created = Posts.objects.update_or_create(pk = 3, title='wang', defaults = updated_values)   # 1.7之后可以用这种方法来更新或者创建一个，如果没找到对象，那么就新建，新建或者更新的字典是defaults的值，返回值中，obj表示该对象，created是一个布尔值
	get_or_create(title='wang', defaults=\{\})：获取或者新建

#### 删除记录

	Blog.objects.get(userName="xiao").delete()
	Blog.objects.all().delete()
	Blog.author.through.objects.filter(author = author.id).delete()  # 删除多对多关系，仅仅是删除关系，而不是删除对象

### 数据约束
#### OneToMany(hasMany)
一对多关系，同样使用ForeighKey实现，例如

	# 在models.py中定义
	class Posts(models.Model):
		title = models.CharField('标题', max_length = 50)
	
	class Comments(models.Model):
		post = models.ForeignKey(Posts, related_name = 'comments_set', 
	
	# 在views.py中这么用
	post = Posts.objects.get(pk = 1)    # 获取一篇文章
	comments = post.comments_set.all()  # 获取该文章的所有评论，是一个列表
#### ManyToManyField
多对多关系，有一种特殊情况，如果需要对这种关系添加额外的字段，可以使用through，添加额外的表来表示，例如，用户一张表，被使用的物品一张表，用户与物品是多对多的关系，但是有时候我们需要记录下用户使用该物品的一些其他属性，比如使用了多少次什么的，这时候就需要给这个多对多关系添加额外的字段来表示，那就需要添加额外的表了，示例如下：

	class User(models.Model):
		username = models.CharField(max_length = 20)
		goods = models.ManyToManyField('物品', 'Goods', through='user_goods')
	
	class Goods(models.Model):
		goodsname = models.CharField(max_length = 20)
	
	class user_goods(models.Model):
		user = models.ForeignKey(User)
		goods = models.ForeignKey(Goods)
		clicks = models.IntegerField('点击量', default=0)

#### OneToOneField
必须是一对一，而不是多对一或一对多

### 分页
Django使用内建的paginator模块进行分页的操作，十分方便。使用方法见例子：

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

虽然contacts是一个Page对象，但是在模板中仍然可以使用for循环对其进行遍历，它其实是一个对象所组成的list。下面是分页按钮html模板例子：

	<nav>
		<ul class="pagination">
			<li class="{% if current_page == 1 %}disabled{% endif %}"><a href="#" aria-label="Previous"><span aria-hidden="true"></span></a></li>
			{% for index in page_index %}
				{% if index == current_page %}class="active"{% endif %}<a href="#";{{ index }}<span class="sr-only"(current)/</span></a></li>
				{% endfor %}
			<li class="{% if current_page == num_pages %}disabled{% endif %}<a href="#" aria-label="Previous"><span aria-hidden="true"></span></a></li>
		</ul>
	</nav>
### 初始化数据
为了方便迁移,让别人使用你的APP,有时候需要为APP里面的表提供demo数据,这时候就需要预先填充一些数据.这里使用Django的fixtures方式填充(Django提供两种[填充方式](https://docs.djangoproject.com/en/1.8/howto/initial-data/))。使用JSON格式，我们可以首先使用`manage.py dumpdata data.json`方式到处原来数据库中内容看看该格式，类似如下：

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
我们可以自己按照这个模板新建填充数据，其中pk指的是主键值。当建立好json文件过后，执行`python manage.py loaddata data.json`即可导入数据。

## Template: Django模板
和所有的MVC框架一样，模板功能是必须有的。这里介绍一下Django模板的使用方法。

### 模板定义
为了方便管理，最好在app的目录下新建templates文件夹用于存放模板文件，然后在project的配置文件settings.py中指明模板文件夹的位置:

	TEMPLATES['DIRS']这个变量中添加即可，比如
	'DIRS': [
		os.path.join(BASE_DIR, 'dashboard/templates').replace('\\', '/'),
	]

这样，在该app的view中就可以这样使用templates下的test.html模板文件了。例如：

	def test(request):
		return render(request, 'test.html')
### 参数传递
要向模板中传递参数，可以给render添加第三个参数，该参数其实是一个字典，在模板中可以直接使用该字典的key，例如：
​	
	return render(request, 'test.html', {'name1': value1, 'name2': value2} )
这样，在模板文件test.html中就可以直接`{{ name1 }}`来使用`name1`的值了。

### 继承与引用
模板方便之处就是可以使用继承将代码分块并且将重复的地方都写在一个base.html里。当要实现继承的时候在html文件第一行写上`{% extends 'base.html' %}`，然后分别实现其区块即可。 在base模板中一般这样定义区块：

	{% block 块名 %}
		这里直接写html代码
	{% endblock %}

如果子模块没有定义某个block的内容，那么就采用父模板的，如果需要使用父模板的内容可以用`{{ block.super }}`  
模板也可以通过引用其它模板的代码，例如，在要引用的地方使用：

	{% include 'nav.html' %}
	{% include 'includes/nav.html' %}

### 静态文件css、js、img
静态文件一般当然是要存放在自己的app里面，这时候，就应该指定静态文件的路径，在project的配置文件settings.py中添加如下配置：
​	
	STATICFILES_DIRS = (
		os.path.join(BASE_DIR, 'static'),
		'f:/project/app/static', # 无论是windows还是linux都要用左斜杠哟
	)
在模板中使用静态文件就这样：
​	
	{% load staticfiles %}
	<link href="{% static 'css/style.css' %}" rel="stylesheet">

### 模板标签
Django内置了一些比较常用又实用的标签：

	# 变量
	## 通过下标获取列表变量的值
	{{ names.0 }}
	
	# 注释
	{# 单行注释 #}
	{% comment %}多行注释{% endcomment %}
	
	# url路由
	有这样一个路由
	url(r'^blog/', 'myapp.views.blog'), # 博客页面
	那么就这样使用
	{% url 'digital.views.blog' %}
	或者使用别名，例如
	url(r'^blog/', 'myapp.views.blog', name='blog'),
	{% url 'blog' %}
	如果是其他app的url，那么需要带上该app的namespace，首先在定义的时候需要添加namespace，如
	url(r'^oauth/', include('oauth.urls', namespace='oauth'))
	然后在实用url的时候：
	{% url 'oauth:hello' %}
	
	# for循环
	{% for <element> in <list> %}{% endfor %}
	{% for <element> in <list> reversed%}{% endfor %} 反向迭代列表
	{% for <element> in <list> %}{% empty %}{% endfor %} 列表为空时的输出内容
	
	# if语句
	{% if <element> %}
	{% elif <element> %} 
	{% else %}
	{% endif %}
	
	{% ifequal 变量1 变量2 %}
	比较值
	{% endifequal %}
	ifnotequal同上

### 过滤器
可以直接格式化输出，是一种最便捷的转换变量输出格式的方式。

	{{ today | data: "F j, Y" }}
这里可以将today这个变量直接按照规定格式输出。  
这里是常见的过滤器：

	add：将该数字加上一个数字，例如 `{{ value|add:"2" }}`，如果原来的值为4，那么新的值就为6，不仅进可以作用与int，还能作用与列表，将列表中每个值都加
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
	last：返回列表的最后yield值
	length：返回变量的长度，也可以在if语句里面使用，例如 {% if messages|length >= 100%} ...{% endif %}
	length_is：判断一长度是否是某个值，例如`{{ vlaue|length_is:"4" }}`如果value长度是4那么就返回True
	linebreaks：替换换行符，例如如果value的值是Joel\nis a slug，那么输出就是<<p>Joel<br /> is a slug</p>
	linenumbers：在输出的tex前加上标号
	ljust：在字符串后面加上指定长度的宽度，例如`{{ value|ljust:"10" }}`
	make_list：将整型或字符串转换为单个单个的列表元素组成一个列表
	random：在列表里面随机选取一个元素
	lower：转换为小写
	rjust：在字符串前面加上指定长度的宽度
	slice：列表分片，例如`{{ some_list|slice:":2"}}`就表示前面两个元素妈
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

### 其他标签

	# autoescape标签
	{% autoescape on %}       # 去掉自动转义
	{{ body }}
	{% endautoescape %}
	
	# cycle标签：每次使用该标签，标签中的值就会变化，比如下面这个，第一次该值为row1，第二次则为row2，第三次又变为了1，感觉可以用于循环里面的奇偶什么的
	{% for o in some_list %}
	<tr class="{% cycle 'row1' 'row'2 %}
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


## 用户认证系统
Django项目默认添加了用户认证系统的，可以通过

	python manage.py makemigrations
	python manage.py migrate

将认证系统的数据表添加到数据库中去.

### 创建用户

	from django.contrib.auth.models import User
	user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
	user.save()

### 创建超级用户

	$ python manage.py createsuperuser --email=896499825@qq.com --username=wanghao
	Password:
	Password (again):
	Superuser created successfully.


### 验证用户登录
需要注意的是，为了不与login冲突，views最好不要写成login

	from django.contrib.auth import authenticate, login
	user = authenticate(username='hao', password='test')
	if user is not None:
		if user.is_activate:
			print('用户验证并登录成功')
			login(request, user)     # 这才是登录，才会写入session
		else:
			print('密码正确，但是用户无法登录')
		return HttpResponse('居然有这个用户')
	else:
		return HttpResponse('用户不存在')

若登录成功，则会返回一个user对象，否则返回None，但是Django默认的认证系统只能认证username和password，却不能认证其它的字段，比如
email字段，看似非常糟糕，但是Django却提供了十分方便的功能来扩展默认的验证组件。查看文档：[Customizing authentication
in Django](https://docs.djangoproject.com/en/1.8/topics/auth/customizing/)

如果要验证用户名或email可以这样做：首先，在myapp目录下新建一个文件，姑且取名叫`backends.py`，其内容如下：

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

然后在settings.py中添加如下代码：

	# 该字段指定了默认的验证后台，从上到下顺序验证，如果上面验证不成功就验证下面的
	AUTHENTICATION_BACKENDS = (
		'myapp.backends.EmailOrUsernameModelBackend',   # 自定义的认证后台
		'django.contrib.auth.backends.ModelBackend',    # 这是默认的认证后台
	)
这样，就可以依然使用刚才的代码对用户登录进行验证了。

## 退出登录

	from django.contrib.auth import logout

	def logout_view(request):
		logout(request)

## 限制登录用户访问路由
某些路由只能登录用户才能访问，那么只需要添加这个装饰器：

	from django.contrib.auth.decorators import login_required

	@login_required
	def my_view(request):
	    ......
 未登录的用户将会重定向到`settings.LOGIN_URL`去       




                      # TroubleShooting

                      1.for循环获取index：



                          \{\% for item in item_list \%\}
                              \{\{ forloop.counter \}\}  \{\# 从1开始的序号 \#\}
                              \{\{ forloop.counter0 \}\} \{\# 从0开始的序号 \#\}
                          \{\% endfor \%\}
    
                      2.直接将html生成成变量：



                          from django.template import Context, Template
                          t = Template("My name is \{\{ my_name \}\}.")
                          c = Context(\{"my_name": "Adrian"\})
                          output = t.render(c)
                          return HttpResponse(output)  # 还能直接将HTML返回成页面
    
                      3.使模板对HTML字符串进行转义 如果有一个HTML格式字符串，比如'<strong>haofly</strong>'，那么当把它作为一个变量传递到htm
                      l中区的时候，会原封不动的保留，很明显我们有时候并不想这样，而是真的想将'haofly'进行加粗，可以这样做：



                          \{\{ variable name | safe\}\}







            ## TroubleShooting：

              * 自定义表名：在class model名()里面指明meta类，例如：

                    class Server(models.Model):
                    object_id = models.AutoField(primary_key = True)




                    class Meta:
                    db_table = '自定义表名'


              * migrate的时候出现类似这样的错误：

                    django.db.utils.OperationalError: (1091, "Can't DROP 'os_id_id'; check that column/key exists")

            原因是你在试图创建一个已经存在的column或者删除一个已经删除的column，这时候需要在migrate后面添加一个参数忽略这些：


                    python manage.py migrate --fake


              * 通过字符串来获取model类，django的apps模块包含了所有注册的app的配置以及model信息([Application文档](https://docs.djangoproject.com/en/1.8/ref/applications/))

                    from django.apps import apps




                print(apps.get_model('myapp', 'Classify_cpu'))

              * 多个键联合unique，增加一个Meta即可：

                    class Meta:
                    db_table = 'posts'
                    unique_together = ('product_1', 'product_2')
    
              * 如果要与默认的auth_user表做外键，那么可以这样做：
    
                    from django.db import models
                from django.contrib.auth.models import User




                class UserInfo(models.Model):
                    user_id = models.ForeignKey(User)


              * 如果通过查询语句始终查询不到数据并且数据库的设置也是正确的，那么可能是model里面定义的字段名与数据库实际的字段不一致，这样既不会跑错，也不会提示，就说查找结果为空，很难debug
              * 根据对象获取model的名称：
    
                    Blog.**class**.**name** # 会输出'Blog'













# TroubleShooting

1.如果想要直接执行_./manage.py_来启动runserver，那么可以修改manage.py文件如下：



    #!/usr/bin/env python
    import os
    import sys




    if **name** == "**main**":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")





    from django.core.management import execute_from_command_line




    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)


2.保存用户上传的图片或文件：使用Django自带的文件存储系统：



    from django.core.files.storage import FileSystemStorage




    storage = FileSystemStorage(
                        location = '/var/www/site/upfiles',
                        base_url = '/upfiles'
                      )
    content = request.FILES['the_file']
    name = storage.save(None, content)
    url = storage.url(name)


##url
##model
##template
##signal
[参考](http://www.weiguda.com/blog/38/)django中signal与操作系统的signal是完全不一样的.Django的signal是一种同步的消息队列.通常在以下情况进行使用：

- signal的receiver需要同时修改对多个model时
- 将多个app的相同signal引到同一receiver中处理时
- 在某一model保存之后将cache清除时
- 无法使用其他方法, 但需要一个被调函数来处理某些问题时



            ---
            title: "Django forms表单"
            date: 2015-06-12 22:08:26
            categories: django
            ---
            Django有一个十分重要的特色功能就是将表单功能独立了出来，使得表单构造和验证更加灵活可控。其实际使用方法如下：
    
            首先，在app目录下新建`forms.py`文件，内容如下：



                from django import forms




                class LoginForm(forms.Form):
                    username = forms.CharField(label='用户名', max_length = 50)
                    password = forms.CharField(label='密码', max_length = 50)
    
            然后，在views.py有如下代码



                from .forms import LoginForm  # 引入该表单

                def login(request):
                    if request.method == 'POST':
                        form = LoginForm(request.POST)
                        if form.is_valid():     # 判断合法性
                            return HttpResponse('数据合法')
                    else:
                        form = LoginForm()
                        return render(request, 'login.html', \{'form': form\}
    
            最后，在templates里面这样使用：



                <form class="form-horizontal" method="post"}
                    {% csrf_token %}
                    {{ form }}
                    <p class="form-actions" style="margin: 0">
                        <input type="submit" value="登录" class="btn btn-primary">
                    <a href="#"><input type="button" value="注册" class="btn btn-success"></a>
                    <a href="#">忘记密码</a>
                    </p>
                </form>
    
            ## 获取表单的值



                if request.method == 'POST':
                    form = Login(request.POST)
                    if form.is_valid():
                        username = form.cleaned_data['username']   # 如果需要单独获取表单的值用这个方法
    
                    form = ProfileLoginForm(request.POST)
    
                    warning = ""
                    if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']</pre>


            ## django-bootstrap3的使用

            默认的form表单没有任何的css样式，如果要让默认的表单拥有bootstrap样式，那么可以使用django-
            bootstrap3这个库，不仅提供了表单的bootstrap样式，而且还提供了bootstrap其它组件的样式，文档见<http://django-
            bootstrap3.readthedocs.org/en/latest/templatetags.html#bootstrap-form>
    
            ## TroubleShooting
    
            1.给表单添加样式，例如：



                username = forms.CharField(label='用户名', max_length = 50, widget = forms.TextInput(attrs=\{'class': 'one'\}))


            2.Form表单可以不整个使用，而使用其中单个的field，比如form.username，这样就可以很方便地为表单中的每个field设置不同的css样式了





## Django Model

### 数据库设置 
              *
              ---
              title: "Django请求与响应"
              date: 2015-05-15 15:12:11
              categories: django
              ---
              官方文档：[Request and response
              objects](https://docs.djangoproject.com/en/1.8/ref/request-response/)
              当请求一个页面的时候，Django会建立一个HttpRequest对象，它包含了请求的一些数据，该对象就是每个views函数里面的第一个参数request.
              需要注意的是，Django的HTTP动词(get/post等)在url上没有区分，只需要在view里面进行判断即可。
    
              例子：



                  if request.method == 'GET':    # GET请求
                      do_something()
                  elif request.method == 'POST': # POST请求
                      request.POST['变量名']   # 获取请求参数
    
              ### JsonResponse
    
              如果要返回JSON数据(常见于Ajax请求)，可以在view里面这样构造json数据



                  from django.http import JsonResponse




                  reponse = JsonResponse(字典)  # JsonResponse(data, encoder=编码方式默认是utf-8
                  response = JsonResponse([1, 2, 3], safe = False)   # 如果要返回一个单纯的列表数据而不是字典类型的数据，就这样
                  return response
    
              ### HttpResponse
    
              直接响应字符串或者html



                  response = HttpResponse('响应一个字符串')
                  response.write('给那个字符串再添加东西')




                  # 如果响应一个字典类型




                  response = HttpResponse()
                  response['Age'] = 120




                  # 常用构建方法




                  HttpResponse('字符串', content_type="text/plain") # 指定content_type

              常用属性：



                  HttpRequest.method   # 请求种类
                  HttpRequest.GET      # 获取所有的GET参数(字典)
                  HttpRequest.POST     # 获取POST的参数(字典)
                  HttpRequest.scheme   # 表示请求的模式，是http还是https
                  HttpRequest.cookies  # 包含了所有的cookie信息
                  HttpRequest.session  # session信息
                  HttpRequest.FILES    # 包含了上传的文件
                  HttpRequest.meta     # 包含了http请求的各种headers
                  HttpRequest.user     # 当前的登录的用户，配合着auth使用
    
              常用方法：



                  get_host()           #不解释了吧
                  get_full_path()      # 获取路径，不包含域名
                  build_absolute_uri() # 获取完整路径
                  is_secure()          # 如果是https返回true，否则false
                  is_ajax()            # 是否是ajax请求
    
              ### StreamingHttpResponse
    
              媒体数据等
    
              ### FileResponse
    
              文件数据等
    
              # TroubleShooting
    
              1.设置GET请求的默认值：



                  date = request.GET.get('value', '2')

              2.返回状态码：



                  return JsonResponse(error, status = 422)

              3.将上传的文件写入到本地，使用chunks()生成器可以将文件一块一块地写入，而不使用read方法，这样可以防止大文件写入失败



                  destination = open('temp/' + filename, 'wb+')
                  for chunk in file.chunks():
                      destination.write(chunk)
                  destination.close()
    
              4.获取用户IP地址：



                  ip = request.META.get('REMOTE_ADDR')

              5.退出登录功能：直接添加一个URL：



                  (r'^logout$', 'django.contrib.auth.views.logout',\{'next_page': 'login'\}, name = 'logout')


              6.通过Ajax发送多维数组，原生不支持的，不过可以在前端以及后端同时传输JSON格式的


                  # 在前端使用Ajax进行传输
                  $.ajax(
                      url: 'test',
                      datatype: 'json',
                      data: JSON.stringify(\{
                          'one': 123,
                          'two': {
                              'two_one': 'test'
                          \}
                      \})
                  )
    
                  # 在后端使用JSON进行解析
                  def test(request):
                      data = json.loads(request.POST)
                   或者前端不变，后端用这个来接收request.POST.getlist('taskIdList[]')




​                          
                          # TroubleShooting

                            1. POST请求403错误：

                                  Forbidden (403)
                              CSRF verification failed. Request aborted.
    
                          原因是Django默认给所有的post请求都添加了CSRF验证中间件，要想对某个路由(url)忽略，可以使用csrf_exempt，关于CSRF的其它一些装
                          饰器见<https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/>


                                  from django.views.decorators.csrf import csrf_exempt




                              @csrf_exempt
                              def webhook(request):
                                  pass
    
                            2. 统一APP的路由 Django是以app的形式定义一个应用的，所以为了保持应用的隔离性，就需要将应用的url分离开来，相当于一个前缀，例如，先在setting.py里面添加APP
    
                                  INSTALLED_APPS = (
                                  'django.contrib.admin',
                                  'django.contrib.auth',
                                  'django.contrib.contenttypes',
                                  'django.contrib.sessions',
                                  'django.contrib.messages',
                                  'django.contrib.staticfiles',
                                  'haofly',                # 需要添加的APP名称
                              )
    
                          然后在工程的urls.py文件里定义APP的主url：


                                  from django.conf.urls import include, url




                              urlpatterns = [
                                  url(r'^前缀/', include('haofly.urls')), # haofly下的urls.py
                              ]


                          然后再在haofly这个APP下建立一个独立的urls.py：


                                  from django.conf.urls import include, url




                              urlpatterns = [
                                  url(r'^test/', 'haofly.views.test'),
                              ]
    
                            3. 在设置路由参数的时候出现如下错误：
    
                                  TypeError at /operation/servers/13/commands
                              commands() got an unexpected keyword argument 'id'
    
                          原因是没有将该参数加入views的定义中去，需要将id加入该views的第二个参数
    
                            4. 跳转功能：
    
                                  return HttpResponseRedirect('/')
