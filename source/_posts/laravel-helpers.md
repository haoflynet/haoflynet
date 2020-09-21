---
title: "Laravel Collection及helpers帮助方法汇总"
date: 2020-09-05 16:00:00
Updated: 2020-09-19 22:24:00
categories: php
---

## 帮助方法

### 数组和对象

```php
# 返回第一个或最后一个元素
head($array);
last($array);

# 合并多个数组为一个单一的数组
Arr::collapse([[1,2,3], [4,5,6], [7,8,9]]);	// [1,2,3,4,5,6,7,8,9]

# 从数组/字典移除指定的key
$array = ['name' => 'Desk', 'price' => 100, 'products' => ['desk' => ['price' => 100]]];
Arr::except($array, ['price']); // ['name' => 'Desk']
# 还可以通过点号的方式来移出多级key
Arr::forget($array 'products.desk'); // ['name' => 'Desk', 'price' => 100]
# 使用点号获取多级的值，第三个参数为默认值
$array = ['products' => ['desk' => ['price' => 100]]];
Arr::get($array, 'products.desk.price', $defaultValue); // 100
data_get($array, 'products.desk.price', $defaultValue); // 同上
data_get($array, '*.name');// 设置支持通配符
# 可使用has来查看是否有某个key，或多个key
Arr::has($array, ['product.price', 'product.discount']);
# 查看是否包含多个key中的一个
Arr::hasAny($array, ['product.name', 'product.discount']);
# 给数组添加元素
Arr::prepend($array, 'zero');
Arr::prepend($array, 'Desk', 'name');	// 会添加一个'name' => 'Desk'
# 获取并移除一个元素
Arr::pull($array, 'name', $defaultValue)

# 检查数组是否存在某个key
Arr::exists($array, 'key');

# 查找第一个回调函数返回true的元素，第三个参数可以指定默认值
Arr::first($array, function($value, $key) {return $value >= 2;}, $defaultValue);

# 仅返回指定key组成的数组
$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];
Arr::only($array, ['name', 'price']); // ['name' => 'Desk', 'price' => 100]

# 将数组/字典所有的value组成一个单一的数组
$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];
$flattened = Arr::flatten($array); // ['Joe', 'PHP', 'Ruby']
# 将指定的key的value组成一个单一的数组
$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];
Arr::pluck($array, 'developer.name'); // ['Taylor', 'Abigail']
Arr::pluck($array, 'developer.name', 'developer.id');	// [1 => 'Taylor', 2 => 'Abigail']

// 将数组作为url的查询参数
$array = ['name' => 'Taylor', 'order' => ['column' => 'created_at', 'direction' => 'desc']];
Arr::query($array); // name=Taylor&order[column]=created_at&order[direction]=desc

// 从数组中随机取一个元素
Arr::random($array);
Arr::random($array, 2);	// 第二个参数表示随机取N个元素

// 数组排序
Arr::sort($array);
array_values(Arr::sort($array, function ($value) {	 // 如果是字段需要指定排序方式
    return $value['name'];
}));

// 返回符合条件的元素组成的数组，类似于js里面的filter
Arr::where($array, function ($value, $key) {
    return is_string($value);
});
```

<!--more-->

### 字符串

```php
// 获取某个字符串前/后面的字符串
Str::after('This is my name', 'This is');	// ' my name'
Str::before('This is my name', 'my name'); // 'This is '


// 获取某个子字符串最后出现的位置前/后面的字符串
Str::afterLast('App\Http\Controllers\Controller', '\\'); // 'Controller'
Str::beforeLast('This is my name', 'is'); // 'This '

Str::startsWith('This is my name', 'This'); // 以指定字符串开始
Str::endsWith('This is my name', 'name'); // 以字符串结束
Str::is('foo*', 'foobar'); // 简单的正则匹配

Str::length('Laravel'); // 求字符串长度

// 获取两个字符串中间的字符串
Str::between('This is my name', 'This', 'name'); // ' is my '

Str::camel('foo_bar'); // fooBar, 将字符串转换为驼峰命名
Str::lower('LARAVEL'); // 将字符串转换为小写
Str::upper('laravel'); // 将字符串转换为大写
Str::padLeft('James', 10, '-='); // 在字符串左边补齐字符，第三个参数默认为空格
Str::padRight('James', 10, ' '); // 在字符串右边补齐字符
Str::plural('car'); // cars, 将字符串转换为复数形式
Str::plural('car', 1); // 第二个参数，让函数自己决定是用复数还是单数
Str::singular('cars'); // 将复数转换为单数
Str::random(40);	// 生成随机字符串
Str::title('a nice title uses the correct case'); // A Nice Title Uses The Correct Case，将制定字符串转换为标题形式，即首字母大写
Str::ucfirst('foo bar'); // Foo Bar同上

Str::substr('The Laravel Framework', 4, 7); // 取子字符串
Str::replaceArray('?', ['8:30', '9:00'], $string); // 依次替换字符串中的问号
Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog'); // 替换字符串中出现的第一个指定字符串
Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog'); // 替换字符串中出现的第一个指定字符串

// 字符串是否包含子字符串
Str::contains('This is my name', 'my');
Str::contains('This is my name', ['my', 'foo']); // 是否包含其中一个
Str::containsAll('This is my name', ['my', 'name']);// 是否包含全部
```

### 其它方法

```php
# blank, 验证对象是否为空。filled和blank正好相反
## 下面是为true的情况
blank('');
blank(' ');
blank(null);
blank(colelct());
## 下面是为false的情况
blank(0);
blank(true);
blank(false);

# optional
optional($user->address)->street;	// 如过内部条件为空，那么不会报错
optional(User::find($id), function ($user) {
  return new DummyUser;
})
```

## Collection集合

`Illuminate\Support\Collection`类提供了一个非常方便的操作来操作数组

```php
$collection = collect([1, 2, 3]);		// 创建一个集合类
User::where('name', 'wang')->get();		// 操作数据库经常会返回一个Collection

all();					// 返回该集合所代表的底层数组[1, 2, 3]
avg();					// 返回集合中所有项目的平均值
avg('field');			// 指定键值的平均值
chunk(n);				// 拆分集合，如collect([1,2,3,4,5,6,7])，按chunk(4)拆分成[[1,2,3,4], [5,6,7]]
collapse([1,2], [2,3])	// 合并数组为一个集合, [1,2,3]
combine(collect); // 合并两个集合，collect(['name', 'age'])->combine(['George', 29])->all(); // ['name' => 'Gerge', 'age' => 29]
concat(); // 连接集合，collect(['John Doe'])->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']) 得到 ['John Doe', 'Jane Doe', 'Johnny Doe']
contains('key');		// 判断集合是否含有某个key
count();				// 返回集合总数
countBy(); // collect([1,2,2,2,3])->countBy()->all() 得到[1=>1, 2=>3, 3=>1]，也可以指定聚合方式function
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

// 取指定的key组成新的集合	
$collection = collect(['Desk' => 'Sofa', 'Chair' => 'aaa']);
$intersect = $collection->intersect(['Desk']); // ['Desk' => 'Sofa']

map(function ($value, $key) {return 'a';});		// 遍历修改集合中的值
random(n=0);				// 随机返回一个项目，n可以不填，如果n>1则会返回一个集合，注意为1的时候返回的不是集合而是里面的项目
reject(function($item){return true;});			// 从集合中移除元素，当返回true的时候，该元素会被移除
unique(function ($item) {return $item;} );		// 仅仅返回唯一的值，相当于去重
```