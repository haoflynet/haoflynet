---
title: "Laravel Blade模板引擎"
date: 2020-09-17 22:38:00
updated: 2021-02-25 16:02:00
categories: php
---

## 常用语法

### 基本标签

```php
# 转义，显示原始html内容
{!! $name !!}

# 转义花括号，因为花括号是特殊字符，如果要直接显示{{}}等内容需要在前面加入@符号
@{{ $name }} // 会直接显示{{ $name }}

# 使用or简化三目运算符
{{ $name or 'Default'}} // {{ isset($name) ? $name : 'Default' }}

# 时间格式转换
{{ $user->created_at->format('d/m/Y') }}

# 获取当前路由
{{ url()->current() == route('/user') }}

# 获取路由参数
{{ request()->get('abc') }}

# 带路由参数的路由生成
{{ route('/users', $id)}}
{{ route('/users', [$id])}}
{{ route('/users', ['id' => $id])}}

{{-- 模板的注释语法 --}}
```

<!--more-->

### 控制语句

```php
# if else
@if()
@elseif()
@else
@endif
  
# 判断子组件是否复写section
@hasSection('title')
@else
@endif

# 需要注意的是，if else是不能写在一行的如果非要写在同一行，建议使用这样的方法
{!! isset($a) && $a['a'] == 'a' ? 'disabled': '' !!}

# 循环for
@for ($i = 0; $i < 10; $i++)
  The current value is {{ $i }}
@endfor

# 循环foreach
@foreach ($users as $user)
	$loop->index			# 循环当前的索引
  $loop->iteration	# 当前循环的指针
  $loop->remaining	# 循环剩余的指针
  $loop->count			# 循环总数量
  $loop->first			# 是否第一个元素
  $loop->last				# 是否最后一个元素
  $loop->even 			# 奇数
  $loop->odd 				# 偶数
  $loop->depth 			# 多层嵌套循环的深度
  $loop->parent			# 父循环的$loop
  
  @continue					# continue语法
  @continue(type == 1)	# 直接将条件写到continue中
  @break						# break语法
  @break($user->number == 5)	# 直接将条件写到break中
@endforeach
  
# 循环forelse，直接把为空的情况判断了
@forelse ($users as $user)
  <li>{{ $user->name }}</li>
@empty
  <p>No users</p>
@endforelse
  
# 循环while
@while (true)
  <p>I'm looping forever.</p>
@endwhile
```

### 模板关系

- 在`Laravel`中我们通常会写一个基本的`layout`模板，然后其它的页面都继承自它

下面是一个例子:


```php
// layout.blade.php
<html>
	<head>
		<title>App Name - @yield('title')</title>	
  
    @hasSection('title')	# 判断子组件是否有复写这个section
    	@yield('title') - Site Name
    @else
    	Site Name
    @endif
  @stack('css')	# 定义一个堆，子组件可以多次push内容进去，会以堆的顺序堆放
  </head>
  <body>
  	@section('sidebar')
  		This is the master sidebar.
  	@show
  
  	<div class="container">
	  	@yield('content')
  	</div>
		</body>
</html>

// home.blade.php
@inject('userService', 'App\Services\UserService')	// 服务注入
{{ $userService->getUsername() }}

@extends('layout')	// 声明该模板继承自基本的layout.blade.php模板

@section('title', 'Page Title')

@section('sidebar')
  @parent	// 可以直接使用父模版中的内容
  <p>This is appended to the master sidebar.</p>
@endsection
  
@push('css')	// 向堆stack中压入内容
@endpush
  
@section('content')	// 编写父模板中content的具体内容
    <h1>Home Page</h1>
  	@include('child')	// 引入子视图，子模板会和父模板共享变量
  	@include('child', ['data' => []])	// 可以传递额外的变量给子模板
@endsection
```

## Vue component

```vue
<my-component :user="{{ json_encode($user->toArray) }}"></my-component>	<!--传递值到vue component去-->
```

