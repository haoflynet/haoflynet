---
title: "Django Form 表单系统"
date: 2020-11-08 15:00:00
updated: 2021-01-12 09:47:00
categories: python
---

Django自带了表单功能，可以与前端及后端完美集成，能非常方便地提供创建、更新或删除模型。

## 表单定义

```python
class Post(models.Model):
  name = models.CharField()
  subtitle = models.CharField(blank=True)
  content = models.TextField()
  created_at = models.DatetimeField()
  user = models.ForeignField(User)

class PostForm(forms.ModelForm):
  	error_css_class = 'error'	# 统一定义错误行的类
    required_css_class = 'required'	# 统一定义必填项的样式
  
    another_field = forms.DateField(
      required=True,	# 是否必填，如果是模型本身字段在Model定义时用blank=True
      label="Custom Field Name",	# 在表单中该字段展示的的label
      label_suffix=":",	# 默认情况label后面是冒号，这个参数可以指定后缀
      initial="abc", # 字段显示的初始值
      help_text="除Model本身字段以外的额外的字段",
      error_messages=[]	# 字段的错误消息列表
      validators=[]	# 验证函数列表，也可以在下面定义clean_字段名进行验证
      disabled=False	# 是否设置为disabled
      widget={	# 扩展小部件，Meta里面也能批量进行控制
      }
    )
    choice_field = forms.ModelChoiceField(queryset=MyChoices.objects.all())

    class Meta:
        model = Post	# 对应的Model
        fields = ("name", "subtitle", "content", "another_field")	# 定义前端能够编辑的字段
        labels = {"name": "Input the Name"}	# 批量定义label
        help_texts = {"name": "Enter a correct name"}	# 批量定义提示信息
        error_messages = {"name": {
          "max_length": "字段太长了"	# 定义指定错误的错误提示信息
        }}
        field_classes = {	# 批量定义字段的css类
          "name": "my_text"
        }
        widgets = {
            "created_at": forms.TextInput(attrs={	# 设置html的一些属性
              "type": "date",
              "class": "my-class custom-class"
              "placeholder": "设置placeholder"
            }),
          	"description": forms.Textarea(attrs={"rows": 1, "cols": 20})	# 设置textarea的默认行数和列数
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Post Name"	# 可以在这里修改model或者form class的字段的label或者其他值
        self.fields['user'].queryset = User.objects.filter(id__in[1,2,3])	# 自定义外键的queryset，这个queryset结果不仅用于显示，还用于验证，表单提交的时候该字段也必须在这些值里面
        self.fields['my_choice_field'] = forms.ChoiceField(choices=[1,2,3])	# 定义choice字段的可选值
        
    def clean_name(self):	# 自定义指定字段的验证，这里验证的是name字段
      data = self.cleaned_data['name']
      if 'test' in data:
      	raise ValidationError(_('Invalid name'))
      return data
```

<!--more-->

### 表单支持的字段类型

```python
BooleanField	# CheckboxInput
CharField	# TextInput，可以设置max_length/min_length/strip/empty_value
ChoiceField	# Select
TypedChoiceField	# Select
DateField	# DateInput，可以设置input_formats时间的格式
DateTimeField # DateTimeInput，可以设置input_formats
DecimalField # NumberInput，可以设置max_value/min_value/max_digits(允许的最大数字位数)/decimal_pkaces(允许的最大小数位数)
DurationField # TextInput
EmailField	# EmailInput
FileField	# ClearableFileInput
FilePathField	# Select
FloatField	# NumberInput
ImageField # ClearableFileInput
IntegerField # NumberInput，可设置max_length/min_length
GenericIPAddressField	# TextInput，Ipv4或Ipv6字段，可设置protocol/unpack_ipv4
MultipleChoiceField	# SelectMultiple
TypedMultipleChoiceField # SelectMultiple
NullBooleanField	# NullBooleanSelect
RegexField	# TextInput，必须设置regex
SlugField
TimeField
URLField
UUIDField
```

### 实现动态choice字段

- 如果一个choice的可选值需要通过另一个用户的输入来决定，可以像这样动态决定其queryset，例如地区选择字段

```python
class DynamicModelChoiceField(ModelChoiceField):
    def to_python(self, value):
        try:
            value = super(DynamicModelChoiceField, self).to_python(value)
        except ValidationError:
            key = self.to_field_name or "pk"
            value = self.queryset.model.objects.filter(**{key: value})
            if not value.exists():
                raise
            else:
                value = value.first()
        return value

class MyForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    self.fields['abc'] = DynamicModelChoiceField(queryset=States.objects.filter(country=self.instance.country)) # 根据用户输入的国家展示对应的省份
```

### 自定义model的展示名称

- 复写Field的`label_from_instance`方法能够自定义model的展示名称，而不是直接用Model的`__str__`

```python
class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.firstname + obj.lastname
UserModelChoiceField(queryset=User.objects.all())
```

## 应用表单

### 模板显示

```html
<form enctype="multipart/form-data" method='POST'>
  {% csrf_token %}
  
  {{ form }}
  
  # 手动挨个呈现字段
  <div class="row">
    <div class="col-6">
      {{ form.name }}
    </div>
    <div class="col-6">
      {{ form.email }}
    </div>
  </div>
  
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 后端保存

```python
form = PostForm(request.POST, request.FILES)	# 如果有文件字段可以直接从request传入
if form.is_valid():
  form.has_changed()	# 表单数据是否发生过改变
  obj = form.save(commit=False)	# commit为False的时候不会立马在数据库中创建对象
  obj.user = request.user
  obj.save()
else:
  print(form.errors)
  print(form.errors.as_json())	# 打印json格式的错误信息
  form.has_error(field_name)	# 指定字段是否有错误
```

## 美化表单django-crispy-forms

使用`django-crispy-forms`可以让表单自动支持`Bootstrap4`，看起来更漂亮。

安装与配置非常简单:

```shell
pip install django-crispy-forms
INSTALLED_APPS = [..., 'crispy_forms']	# 添加到INSTALLED_APPS中
CRISPY_TEMPLATE_PACK = 'bootstrap4'	# 使用bootstrap4，当然也可以使用旧版本

# 当然，依然要在html中引入css和js，可以在一个base.html中引入
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
```

在需要美化表单的时候直接这样做:

```html
{% extends 'base.html' %}

{% load crispy_forms_tags %}
<form enctype="multipart/form-data" method='POST'>
  {% csrf_token %}
  {{ form|crispy }}
  
  {{ form.name|as_crispy_field}}	# 或者这样可以手动呈现指定字段
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### crispy FormHelper

`crispy`插件还提供一些helper帮助在定义form的时候提供更多的自定义配置，例如:

```python
class MyForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
```

### crispy Layouts

可以自定义字段的更多样式，例如autocomplete、定义data、id、text input的前缀后缀、Tab字段分类等，具体文档见[Layouts](https://django-crispy-forms.readthedocs.io/en/latest/layouts.html)