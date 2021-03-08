---
title: "Laravel 请求与响应"
date: 2020-09-06 22:29:00
updated: 2021-03-04 12:32:00
categories: php
---

## Request

```php
// 获取请求指定字段
$request->name; // 直接获取
$request->input('name');
$request->input('name', 'Sally'); // 指定默认值
$request->input('user.name'); // 可以直接用点号获取JSON格式的请求体
$request->input('products.0.name'); // 如果请求数据是数组可以用这个方法获取数组内部元素
$request->input('products.*.name'); // 同上
$request->query('name'); // 获取查询参数
$request->query('name', 'Helen'); // 带默认值
$request->all(); // 获取所有请求参数为一个数组
$request->input(); // 同上
$request->query(); // 所有查询参数转换为数组
$request->boolean('archived'); // 获取布尔值，能够自动判断1/"1"/true/"true"/"on"/"yes"，6.x开始
$request->only(['username', 'password']); // 仅获取指定字段的请求
$request->except(['credit_card']); // 仅排除指定字段的请求

// 判断请求是否包含某个key
$request->has('name'); 
$request->has(['name', 'email']);
$request->hasAny(['name', 'email']);
$request->filled('name');	// 是否包含并且不为空
$request->missing('name'); // 不包含
  
// 获取请求地址
$request->path();	// 获取请求路径，例如https://domain.com/foo/bar就会返回foo/bar
$request->is('admin/*'); // 正则匹配请求路径
$request->fullUrl(); // 包含请求参数的完整url，例如https://dmoain.com/foo/bar?abc=def
$request->url();	// 不包含请求参数的完整url，例如https://dmoain.com/foo/bar
$request->root();	// 获取域名部分，包括http，例如https://domain.com
$request()->getHost(); // 获取纯域名部分，例如domain.com

// 获取请求方法
$request->method();
$request->isMethod('post');// 判断请求方法

$request->route();	# 通过request获取Route对象

$request->cookie('name'); // 获取cookie，同Cookie::get('name');

// 动态改变或新增request的值
$request->merge([
  'keyword' => $request->search,
  'page' => 2
]);
  
// 判断请求类型
request()->ajax(); // 判断请求是否是ajax请求
request()->expectsJson(); 	// 判断客户端是否希望得到JSON响应

// 去掉路由参数
$request->route()->forgetParameter('param');
```

<!--more-->

### 文件上传请求

```php
# 获取上传的文件
$request->file('photo'); // 获取指定上传文件
$request->files; # 获取上传的所有的文件
$request->photo; # 获取上传的图片
$request->photo->path(); // 获取上传图片的路径
$request->photo->extension(); // 获取上传图片的扩展名
$request->hasFile('photo'); // 查看指定字段是否有上传文件
$request->file('photo')->isValid(); // 验证文件是否有效

# 存储上传的文件
$path = $request->photo->store('images');
$path = $request->photo->store('images', 's3');
$path = $request->photo->storeAs('images', 'filename.jpg');
$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

### 历史输入

- `Laravel`允许在`session`中保存上一次请求的请求参数

```php
$request->flash();	// 将当前的请求参数写入session
$request->flashOnly(['username', 'email']); // 仅缓存部分字段
$request->flashExcept('password'); // 排除部分字段

return redirect('form')->withInput( // 缓存输入然后重定向
    $request->except('password')
);

$request->old('username'); // 获取上一次请求的输入
// view中就能直接这样做了: 
<input type="text" name="username" value="{{ old('username') }}">
```

## Response

- 如果返回`array`，那么`laravel`能够自动转换为`JSON`响应

```php
return response('Hello World', 200)	// 指定状态码
  ->header('Content-Type', 'text/plain')
  ->withHeaders([		// 一次设置多个header头
    'Content-Type' => $type,
    'X-Header-One' => 'Header Value',
    'X-Header-Two' => 'Header Value',
  ])
  ->cookie('name', 'value', $minutes)	// 设置cookie
	->cookie($name, $value, $minutes, $path, $domain, $secure, $httpOnly); // cookie设置完整参数
    
    
# 返回重定向
return redirect('home/dashboard');
return redirect()->route('login'); // 指定路由名重定向
return redirect()->route('profile', ['id' => 1]);	// 带参数的路由重定向
return redirect()->route('profile', [$user]); // 如果路由参数是id，那么可以直接用对象作为参数
return redirect()->action('HomeController@index');	// 重定向到指定的控制器方法
return redirect()->action('UserController@profile', ['id' => 1]); # 带参数的控制器方法
return redirect()->away('https://www.google.com'); // 重定向到外部域名
return redirect('dashboard')->with('status', 'Profile updated!'); // 重定向时设置一个session，view里面就可以直接用session('status')来获取值


# 返回到之前的页面并携带用户的输入(比如form post的时候出错就不用跳转到新页面了)
return back()->withInput();

// 指定返回json响应
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);

// 指定返回jsonp响应
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));

// 响应文件
return response()->download($pathToFile);	# 直接提供文件下载
return response()->download($pathToFile, $name, $headers);	# 设置文件名和响应头
return response()->download($pathToFile)->deleteFileAfterSend(true); # 设置为下载后删除
return response()->file($pathToFile);
return response()->file($pathToFile, $headers);

// 流式响应
return response()->streamDownload(function () {
    echo GitHub::api('repo')
                ->contents()
                ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

## Cookie

- 默认在应用中获取的cookie都是解密后的cookie，返回给客户端的cookie都是加密后的，这一步是在`app/Http/Middleware/EncryptCookies.php`中做的

```php
$_COOKIE['name'];	# 获取未解密的cookie

Cookie::has('name');	// 是否存在某个cookie
Cookie::forget('name');	// 删除某个cookie

response()->withCookie(cookie('name', 'value', $minutes));	// 响应带上cookie

// 排除指定的cookie不需要加解密，在 app/Http/Middleware/EncryptCookies.php中
protected $except = ['key'];

Crypt::encrypt(key);	// 对cookie进行加密 
Crypt::decrypt(value);	// 对cookie进行解密
```

