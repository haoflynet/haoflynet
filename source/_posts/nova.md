---
title: "Laravel Nova 使用手册"
date: 2021-04-27 20:00:00
updated: 2021-12-13 20:20:00
categories: php
---

## 安装

-  [Releases Note](https://nova.laravel.com/releases)，他们的源代码没有在github上

- 因为我目前使用的是付费的，所以是把Nova目录直接放到了根目录，升级的时候只需要在后台重新下载一个包覆盖即可
- [安装步骤](https://nova.laravel.com/docs/3.0/installation.html#installing-nova)：和普通的包安装方式不一样，因为需要购买`license`，商用`$199/project`

## 资源

- `php artisan nova:resource Post`生成资源管理类，一般和`Model`名一样即可

<!--more-->

## 字段

### 字段通用参数

```php
::make('Name', 'name_column')	# 可以给make提供第二个参数指定数据库列是哪一个字段
->hideFromIndex()	# 不展示在列表页
->hideFromDetail()	# 不展示在详情页
->hideWhenCreating()
->hideWhenUpdating
->onlyOnIndex()
->onlyOnDetail()
->onlyOnForms()
->exceptOnForms()
->readonly()	# 只读字段
->rules(	# 字段校验规则
  'rquired', 
  'nullable',	# 允许为空
  'max:255'
)	
->sortable()	# 是否允许排序
->nullable()	# 是否允许为空，需要注意的是如果有rules那么这个需要加到rules里面去
->nullable(['', '0', 'null'])
->withMeta(['extraAttributes' => [
  'placeholder' => 'Please input'	# 设置placeholder
]])
->help('thsis is help text')
->help('<a href="#">help</a>')
->help(view('template', ['name' => $this->name])->render()
->resolveUsing(function ($name) {
  return strtoupper($name);
});
->displayUsing(function ($name) {
  return strtoupper($name);
});
```

### 常用字段

```php
# Boolean布尔字段
Boolean::make('Active')->trueValue('On')->falseValue('Off');	// 如果后端不是用true或false来存储，可以指定true/false的值

# Datetime日期时间字段
Datetime::make('CreatedAt');	// 需要注意的是，这个字段有个bug，不能清空，至少在3.1.6上是不行的，然后我升级到3.23.2后就会带有一个清空按钮了，中间的版本不知道从哪里开始修复的

# Select字段/枚举字段
Select::make('Status')->options([
  0 => 'Deactivated',
  1 => 'Active',
])->displayUsingLabels()	// 表示展示的时候展示label而不是原值
  
# Text字段
Text::make('name');	// text 这个input字段只占宽度的1/2，改不了，可以用textarea->rows(1)代替
  
# Textarea字段
Textarea::make('Description')->alwaysShow()->rows(3);
```

### 其他字段

```php
# Computed字段
Text::make('Name', function () {
  return $this->first_name . ' ' . $this->last_name;
});

# 还能用html来表示
Text::make('Name', function () {
  return view('status', ['is_passing' => $this->isPassing()])->render();
})->asHtml();
```

### 关联字段

```php
# BelongsTo
BelongsTo::make('User')->display(function($user) {
  return $user->name;
})

# HasMany
HasMany::make('Photos', 'Photos', UserPhoto::class)	# 第三个参数为关联表的Nova类信息
```

## Filter

- 通过命令`php artisan nova:filter UserType`新建过滤器，`--boolean`可以创建布尔类型的，但是不好用，只有`true/false`没有不选择的状态，所以我一般用默认的，默认的就是`select`下拉选择
- 然后在需要使用的资源的`filters`里面添加上即可`return [new UserType]`

- 在`app/Nova/Filters`里面有我们新建的过滤器

  ```php
  // 根据前端选择进行查询
  public function apply(Request $request, $query, $value)
  {
    if ($value === 'yes') {
      return $query->whereNotNull('field');
    }
    if ($value === 'no') {
      return $query->whereNull('field');
    }
    return $query;	// 可以默认不选择的情况
  }
  
  // 定义有哪些选项
  public function options($request)
  {
    return [
      'Yes' => 'yes',
      'No' => 'no'
    ];
  }
  ```

## Observer

- 可以在和普通model对象一样在保存前后执行一些自定义的hook，只需要`php artisan make:observer -m Post PostObserver`，会在`observer`目录下生成文件

  ```php
  # app/Observers/PostObserver
  class PostObserver {
  	public function creating(Post $post) {
  		$post->field = request()->input('abc');
  		unset($post->field);
  	}
  }
  
  # 最后需要在AppServiceProvider的boot中进行注册
  public function boot()
  {
  	Nova::serving(function () {
  		Post::observe(PostObserver::class);
  	});
  }
  ```

## 扩展字段开发

- `resources/js/components/FormField.vue`是编辑资源的时候用的

  ```vue
  <template>
  
  </template>
  <script>
  	props: ['resourceName', 'resourceId', 'field'], // 其中field.value就是原始值，field.attribute是原始字段名
    methods: {
      fill (formData) {
        formData.append( this.field.attribute, this.myValue);	// 设置提交表单的时候提交的值
        formData.append( this.field.attribute, [1, 2, 3]);	// 如果是要更新关联表的关联可以仅传递关联的对象的id
        formData.append( this.field.attribute, [{obj_id:1, name: 'test'}, {obj_id:1, name: 'test2'}, {obj_id:1, name: 'tes3'}]);	// 如果是要更新关联表的pivot，可以这样传入
      }
    }
  </script>
  ```

### 常用扩展字段

- [Nova插件仓库](https://novapackages.com/?search=ajax&tag=all)
- [搜索关联表字段](https://novapackages.com/packages/titasgailius/search-relations)
- [Cloudinary字段](https://novapackages.com/packages/silvanite/nova-field-cloudinary)
- [Nova Import](https://novapackages.com/packages/anaseqal/nova-import): Nova excel/csv导入插件，不过作者说了nova 3.10.0+以后可以不用这个库就能实现了，可以直接参考[这里](https://github.com/anaseqal/nova-import/issues/26)，非常简单
- [Nova NestedSet Tree Attach Many Field](https://novapackages.com/packages/phoenix-lib/nova-nested-tree-attach-many): 非常好用的数据库树状结构字段，但是我使用的时候在detail页面有点样式问题，修改了一下，可以参考[我的PR](https://github.com/phoenix-lib/nova-nested-tree-attach-many/pull/14)
- [Nova AJAX Field](https://novapackages.com/packages/razorcreations/ajax-field): 可以做到通过ajax进行关联查询，虽然代码写得有点死，但是够用了

## TroubleShooting

- **DateTiem field must cast to 'datetime'**，这是因为在`Nova`里面使用了DateTime字段，但是在`Model`上没有将该字段设置为`casts`，需要在`Model`上这样做

  ```php
  protected $casts = [
     '字段名' => 'datetime'
  ]
  ```

- **/public/vendor/nova下的静态文件无法访问，404**： 原因可能是文件权限的问题，看当前用户能否读取