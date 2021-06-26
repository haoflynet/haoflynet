---
title: "Laravel Validation数据校验"
date: 2020-09-06 16:00:00
updated: 2021-05-21 22:24:00
categories: php
---

- 
默认启用了`TrimStrings`和`ConvertEmptyStringsToNull`两个中间件的，一个自动去除前后空白，一个将空字符串转换为null

## 直接验证

```php
$validatedData = $request->validate([
  'title' => 'required|unique:posts|max:255',
  'title' => ['required', 'unique:posts', 'max:255'], // 也可以写成数组的形式
	'person.*.email' => 'email|unique:users', // 校验数组
	'person.*.first_name' => 'required_with:person.*.last_name'
  'title' => ['required', function ($attribute, $value, $fail) { // 简单的自定义验证规则可以不用建验证类，直接用匿名函数
            if ($value === 'foo') {
                $fail($attribute.' is invalid.');
            }
        },],
]);

// 或者这样创建
$validator = Validator::make($request->all(), [
  'title' => 'required|unique:posts|max:255',
  'body' => 'required',
]);

// 判断请求类型，如果是ajax请求，那么返回json数据和422，如果非ajax那么重定向刷新页面
if ($validator->fails()) {
  if ($request->ajax()) {
    return response()->json($validator->messages(), Response::HTTP_BAD_REQUEST);
  } else {
      return redirect('post/create')
    ->withErrors($validator)	// 刷新session中存储的错误信息，可用在view中
    ->withInput();
  }
}

// 同样可以自定义错误信息
$messages = [
    'required' => 'The :attribute field is required.',
];
$validator = Validator::make($input, $rules, $messages);

// 满足某个条件时才验证，例如下面当游戏>=100的时候才验证指定字段
$v->sometimes('reason', 'required|max:500', function ($input) {
    return $input->games >= 100;
});
$v->sometimes(['reason', 'cost'], 'required', function ($input) {
    return $input->games >= 100;
});
```

<!--more-->

## 请求类中进行验证/接口权限认证

- Laravel可以使用`php artisan make:request MyRequest`生成一个请求类，一般会在请求类中编写验证规则以及错误信息，当然也可以直接在控制其中进行规则的定义以及校验。


```php
class MyRequest extends Request {
  // 可以在这里定义用户是否有该接口的访问权限
  public function authorize() {
    $comment = Comment::find($this->route('comment'));
    return $comment && $this->user()->can('update', $comment);
  }

  // 返回校验规则
  public function rules(){
    switch($this->method()){
      case 'POST': {
        return [
          'name' => 'required|string|max:100',
        ];
      }
      case 'PUT':{
        return [
          'name' => 'required|string|max:100',
        ];
      }
    }
  }
  
  // 自定义错误信息
  public function messages()
	{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
	}
  // 自定义错误信息中的字段名称
  public function attributes()
  {
      return [
          'email' => 'email address',
      ];
  }
  // 在验证前修改请求数据/修改request，或者增加字段
  protected function prepareForValidation()
  {
      $this->merge([
          'slug' => Str::slug($this->slug),
      ]);
  }
  // 自定义返回格式
  public function response(array $errors){
    return redirect()->back()->withInput()->withErrors($errors);
  }
  
  // 如果要验证路由中的参数，可以复写all字段，将路由参数放入即可
  public function all($keys = null) 
  {
     $data = parent::all($keys);
     $data['token'] = $this->route('token');
     return $data;
  }
}
```

## 校验规则大全

- `bail`规则表示当遇到一个错误的时候立刻停止后面的校验


```shell
# 常用框架自带的认证类型
active_url			# 该url一定能访问
after_or_equal	# 相等或者之后，常常用于同时设置开始时间和结束时间的接口，例如after_or_equal:start_date表示当前的时间字段必须在start_date字段之后，after_or_equal:now表示与当前时间对比
array				# 仅允许为数组
before_or_equal	# 和after_or_equal相反
between:min,max		# 介于最小值和最大值之间，两边都是闭区间，如果是数字，一定要先声明当前字段为integer
boolean				# 必须是true,false,1,0,"1","0"
date				# 必须是时间类型
exists:table,column	# 判断字段的值是否存在于某张表的某一列里面
exists:table,column1,column2,value	# 存在，判断字段的值是否存在于某张表的某一列里面，并且另一列的值为多少
exists:table,column1,column2,!value	# 不存在，判断字段的值是否存在于某张表的某一列里面，并且另一列的值不为多少
exists:table,column1,column2,{$field}# 判断字段的值是否存在于某张表的某一列里面，并且另一列的值和前面的某个字段提供的值一样
in:value1,value2,...# 字段值必须是这些值中的一个，枚举值
not_in:value1,value2,...	# 字段值不为这其中的任何一个
integer				# 必须是整数
ip					# 必须是IP字符串
json				# 必须是JSON字符串
max:value			# 规定最大值
min:value			# 规定最小值
numeric				# 是数字
nullable			# 非必填，可以为空
required			# 必填
required_if:anotherfield,value1,value2	# 当指定的anotherfield字段等于任何一个value时，此字段必填
required_unless:anotherfield,value1,value2 # 当指定的anotherfield字段等于任何一个value时，此字段不用必填
required_with:foo,bar,...  # 当指定的字段中任何一个有值时，此字段为必填
required_with_all:foo,bar,...	# 当指定的所有字段都有值时，此字段为必填
required_without:foo,bar,...	# 如果缺少任意一个指定的字段，则自此字段为必填
required_with_out_all:foo,bar,...	# 如果所有指定的字段你都没有值，则此字段为必填
same:foo			# 必须和指定字段的值保持一致
string				# 必须是字符串
unique:表名,字段名	# 唯一性校验
unique:表名,字段名,忽略值	# 可以忽略一个指定的值，通常用于忽略当前需要修改的值
unique:users,email_address,xxx,id,account_id,1	# 添加更多的条件，这里表示忽略email_address为xxx的并且account_id为1的值
url					# 必须是合法的url
regex				# 必须符合这个正则表达式，例如regex:/^[a-z]{1}[a-z0-9-]+$/，需要注意的是，如果正则表达式中用了|符号，必须用数组的方式来写正则表达式，否则会报错，例如['required', 'regex:/[0-9]([0-9]|-(?!-))+/']
```

### 自定义验证规则

除了上面的验证关键字外，还能自定义验证规则，可以使用`php artisan make:rule Uppercase`来生成验证类，例如

```php
class Uppercase implements Rule
{
    /**
     * Determine if the validation rule passes.
     *
     * @param  string  $attribute
     * @param  mixed  $value
     * @return bool
     */
    public function passes($attribute, $value)
    {
        return strtoupper($value) === $value;
    }

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return 'The :attribute must be uppercase.';
    }
}
```

## 验证失败返回

- `blade`模板中可以直接使用验证失败的信息
- 需要注意的是`laravel`会自动屏蔽`password`和`password_confirmation`字段，即使用`old`也无法获取到之前的输入，这也是为了安全考虑，如果一定要返回，那么可以在`app/Exceptions/Handler.php`中将这两个字段屏蔽掉

```php
// 当出错刷新页面后能够显示用户之前的输入
<input value="{{ old('username') }}"> 
```

