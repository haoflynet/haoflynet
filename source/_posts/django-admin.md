---
title: "Django Admin 后台管理系统"
date: 2019-06-01 00:00:00
updated: 2020-11-21 15:32:00
categories: 编程之路
---


Django自带了强大的名为`admin`的后台管理功能，app名称为`django.contrib.admin`，它同时依赖了`django.contrib.auth`认证系统和`django.contrib.sessions`系统，当然，即使不用admin，后面两者都建议加上，不用重复造轮子。

- 为了使用它，我们需要先使用`migrate`功能去创建相应的数据库表，直接执行`python manage.py makemigrations && python manage.py migrate`即可。运行程序后，直接访问`http://127.0.0.1:8000/admin/`就能访问admin了(一般admin的路由都是定义好了的，在`urls.py`中有` url(r'^admin/', admin.site.urls),`)

- 我们需要先创建一个超级管理员`python manage.py createsuperuser`，按照提示输入用户名密码即可用来登录了

- 如果要让字段非必填，需要在定义model字段的时候就加上`blank=True`参数

- 修改超级管理员密码可以这样做:

  ```python
  # python manage.py shell
  from django.contrib.auth.models import User  
  user =User.objects.get(username='admin')  
  user.set_password('new_password')  
  user.save()  
  ```

<!--more-->

### 使用admin管理数据表

为了管理具体的某张表，我们需要在app下的`admin.py`文件里面注册相应的`model`：

```python
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from myapp.models import PostModel

class PostAdmin(admin.ModelAdmin):
  class Media:
    js = ["js/test.js"]	# 可以引入自定义的js实现更多的个性化功能(这里该js文件位于static/js/test.js下)
    css = ["css/test.css"]	# 自定义css
    
  list_display = ('id', 'name', 'created_at')	# 定义后台列表显示时需要显示哪些字段
  list_per_page = 50		# 定义后台列表显示时每页显示数量
  list_filter = ('id', 'name', )	# 定义后台列表显示时能够筛选的字段(会列出所有的可筛选值)
  search_fields = ('username', 'email',)	# 指定能搜索哪些字段
  list_editable = ['field']	# 定义可以直接在列表页进行更改的字段
  fx_fields = ('user_id', )	# 定义列表页显示的外键字段，会直接显示关联的值
  filter_horizontal = ('posts')	# 显示多对多字段
  readonly_fields = ('username')	# 设置只读字段，不允许更改
  ordering = ('-created_at', )	# 定义列表显示的顺序，负号表示降序
  fieldsets = (		# 对字段进行分类/分组设置，前端会分开显示
  	(None, {'fields': ('username', 'password', )}),
  	('Personal info', {'fields': ('firstname', )}),
    ('Permissions', {'fields': ('groups', )}),
  )
  add_fieldsets = (	# 定义添加数据时需要填写哪些字段
    (None, {'classes': ('wide',), 'fields': ('name', 'content' )}),
    )
  
  def save_model(self, request, obj, form, change):
    """定义保存对象的方式，可以在这里做一些其他的事情。这个方法不需要返回任何东西，如果要捕获其中的错误或者重定向，最好是设置一个对象字段，然后在response_change或response_add中进行处理"""
    self.has_error = True
    self.message_user(request, "友好地给用户显示错误信息", level=logging.ERROR)
    super().save_model(request, obj, form, change)
    return
  
  def response_change(self, request, obj):
    """改变记录之后的响应操作，可以捕获错误并返回应该返回的消息"""
    if self.has_error:
      return HttpResponseRedirect(request.path)
    else:
      return super().response_chage(request, obj)
  
  def respopnse_add(self, request, obj, post_url_continue=None):
    """添加记录之后的响应操作"""
    return super().response_add(request, obj, post_url_continue)
  
admin.site.register(PostModel, PostAdmin)	# 注册管理模型
admin.site.site_header = '后台页面的header'
admin.site.site_title = '后台的title'

@admin.register(UserModel)	# 也可以用装饰器直接进行注册
class UserAdmin(admin.ModelAdmin):
  pass
```

### 自定义admin管理数据创建及修改表单

```python
class MyModelCreationForm(forms.ModelForm):
    """自定义创建表单"""
    field_name = forms.CharField(label='field_name')
    
    class Meta:
        model = MyModel
        fields = ('email', 'field2')
        exclude = ('created_at', )	# 排除某些字段不用在后台管理

class MyModelChangeForm(forms.ModelForm):
    """自定义修改表单"""
    password = ReadOnlyPasswordHashField(label= ("Password"), help_text= ("Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using <a href=\"../password/\">this form</a>."))	# 如果要修改密码字段，我们需要这样提示
    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):	# 用户管理需要继承单独的Admin
    form = UserChangeForm				# 指定修改表单
    add_form = UserCreationForm	# 指定创建表单，如果不指定默认都会使用form
    
    def get_form(self, request, obj=None, **kwargs):
      """如果仅仅是某几个字段的简单修改可以直接这样写，不用定义新的Form类"""
      kwargs['widgets'] = {
        'name': forms..TextInput(attrs={'placeholder': 'this is a example'})
      }
      return super().get_form(request, obj, **kwargs)
```

#### admin中字段动态hide与show

- 目前没有找到更好的方法，不过可以直接用`class Media: js=()`来自定义js文件，通过jQuery来实现

### Django-CKeditor富文本编辑使用

`django-ckeditor`扩展，使用简单，前端也漂亮

1. 安装`pip install django-ckeditor`，如果要在富文本里添加图片还需要`pip install pillow`

2. 注册应用，`INSTALLED_APPS`里添加`ckeditor`，图片还需要添加`ckeditor_uploader`

3. 如果要使用自定义的文件存储，例如七牛云存储，可以参考[这篇文章](https://haofly.net/django-storage)进行设置

4. 如果要处理图片，还需要在`settings.py`里面添加如下设置:

   ```python
   # 前面两个可能已经设置了，是存放用户上传文件的地方
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
   CKEDITOR_UPLOAD_PATH = 'upload/'
   
   CKEDITOR_CONFIGS = {	# 添加个性化的配置
       'default': {
           'image_previewText':' ',	# 替换图片显示区域那一串搞不懂的字符串
           'tabSpaces': 4,
       }
   }
   ```

   另外还需要添加一个路由用于上传请求

   ```python
   from django.conf.urls.static import static
   
   urlpatterns = [
   	...
       path('ckeditor/', include('ckeditor_uploader.urls')),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

   模型里面对应的字段设置

   ```python
   from ckeditor.fields import RichTextField
   
   class Post(models.Model):
       content = RichTextField()
       content2 = RichTextUploadingField()	# 带有上传图片功能的富文本编辑
   ```
   
   `Django-CKeditor`目前还不支持粘贴的时候自动上传图片，我的做法是在对象的`Admin`的`save_model`方法里面对没有转换为内链的外部链接图片通过`requests`抓取下来再上传到七牛云，以达到自动替换的效果。这只是最简单的做法，当然，最好的做法还是在前端监听粘贴事件，实时上传。
   
   ### Django-MarkdownX文本编辑器使用
   
   目前，`Django-CKeditor`暂时还不支持`markdown`，所以只能用`Django-Markdownx`来代替，要兼容两者就只能用两个字段来存储了。引入步骤：
   
   1. 安装依赖，并且将`markdownx`加入`INSTALLED_APPS`中
   
      ```
      pip install django-markdownx
      ```
   
   2. 添加路由`vim app/urls.py`:
   
      ```python
      urlpatterns = [
          [...]
          url(r'^markdownx/', include('markdownx.urls')),
      ]
      ```
   
   3. 字段定义
   
      ```python
      class Post(models.Model):
        content = MarkdownxField()
      ```
   
   4. 自定义tag，`vim app/templatetags/base.py`
   
      ```python
      import markdown
      from django import template
      from django.utils.safestring import mark_safe
      
      register = template.Library()
      
      @register.filter(is_safe=True)
      def custom_markdown(value):
          return mark_safe(
              markdown.markdown(
                  value,
                  extensions=[
                      "markdown.extensions.extra",
                      "markdown.extensions.toc",
                      "markdown.extensions.sane_lists",
                      "markdown.extensions.nl2br",
                      "markdown.extensions.codehilite",
                  ],
                  safe_mode=True,
                  enable_attributes=False,
              )
          )
      
      @register.filter(is_safe=False)
      def custom_markdown_unsafe(value):
          return mark_safe(
              markdown.markdown(
                  value,
                  extensions=[
                      "markdown.extensions.extra",
                      "markdown.extensions.toc",
                      "markdown.extensions.sane_lists",
                      "markdown.extensions.nl2br",
                      "markdown.extensions.codehilite",
                  ],
                  safe_mode=False,
                  enable_attributes=False,
              )
          )
      ```
   
   4. 添加相关配置到配置文件
   
      ```python
      MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'
      MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {}
      MARKDOWNX_URLS_PATH = '/markdownx/markdownify/'
      MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/'
      MARKDOWNX_MEDIA_PATH = 'media/markdownx/img'
      MARKDOWNX_UPLOAD_MAX_SIZE = 5 * 1024 * 1024
      MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/svg+xml']
      MARKDOWNX_IMAGE_MAX_SIZE = {'size': (800, 500), 'quality': 100,}
      MARKDOWNX_EDITOR_RESIZABLE = True
      MARKDOWNX_MARKDOWN_EXTENSIONS = [
          'markdown.extensions.fenced_code',
          'markdown.extensions.codehilite',
          'markdown.extensions.smarty',
          'markdown.extensions.extra',
          'markdown.extensions.tables',
          'markdown.extensions.sane_lists',
          ]
      ```
   
6. 前端模板这样渲染
  
      ```django
      <div>
        {{ content | custom_markdown }}
      </div>
      ```
   
   ##### 左右分割显示
   
   默认的编辑器样式是上下分割，上面编辑，下面实时显示，但是对于长文本十分不方便，如果要进行左右分割，需要这样做：
   
   1. 引入`bootstrap`依赖，并且将`bootstrap3`加入`INSTALLED_APPS`中
   
      ```shell
      pip install django-bootstrap3
      ```
   
   2. 覆写原本的编辑框，`app/templates/markdownx/widget2.html`:
   
      ```django
      {% load bootstrap3 %}
      {% bootstrap_css %}
      {% bootstrap_javascript %}
      <div class="markdownx row">
          <div class="col-md-6">
              {% include 'django/forms/widgets/textarea.html' %}
          </div>
          <div class="col-md-1"></div>
          <div class="col-md-5">
              <div class="markdownx-preview"></div>
          </div>
      </div>
      ```
   
   3. 添加admin管理：
   
      ```python
      class PostAdmin(admin.ModelAdmin):
            formfield_overrides = {
              models.TextField: {'widget': AdminMarkdownxWidget},
          }
      ```
   
   
   ## TroubleShooting
   
   - **Python crashes after trying to visit admin page with exit code 245**: 每次进入admin页面程序就崩溃，可以尝试更新`python`版本或者更新`django`版本，我`3.7.0b2`遇到过这个问题，升级`Python`得以解决
   
   - **隐藏或修改Admin中的第三方APP管理**: 随便找个自己的`app`，在`admin.py`中取消该`app`的注册:
   
     ```python
     admin.site.unregister(ThirdModel)
     
     ```
   # 而如果要修改第三方的管理类，可以这样做，重新注册一个新的类
     class NewThirdModel(ThirdModel):
       pass
     admin.site.register(ThirdModel, NewThirdModel)
     ```
     
     
     ```