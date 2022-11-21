---
title: "wordpressd 插件开发手册"
date: 2020-10-18 10:26:00
updated: 2022-11-03 22:56:00
categories: php
---

- 在本地开发的时候，由于有很多东西依赖于`cookie`，有些插件在写入`cookie`的时候可能没有判断服务端口导致无法写入`cookie`，功能无法正常使用，所以在开发和使用过程中最好用正常的`http`端口，即`80`或`443`

- 开发时最好打开调试模式:

  ```shell
  # vim wp-config.php
  define('WP_DEBUG', true);
  define('WP_DEBUG_LOG', true);
  define('SCRIPT_DEBUG', true);
  ```

## 插件开发基本概念

### 插件目录结构

- 在`wordpress`源码的`/wp-content/plugins`下，一个目录就是一个插件

- 插件内部的目录结构一般是这样的:

  ```shell
  test-plugin
    ├── assets
    │   ├── css
    │   │   └── test-plugin.css
    │   └── js
    │ 			└── test-plugin.js
    ├── include
    │		└── test-plugin.php
    └── readme.txt
  ```

## 帮助函数

### 用户相关函数

#### wp_signon

- 通过用户名密码获取用户信息

```php
$user = wp_signon(['user_login' => 'xxx', 'user_password' => 'xxx'], false);
echo $user->id
```

#### wp_update_user

- 更新用户指定字段，但不知道为什么，就是不能更新用户的`user_status`字段，最后我只能`$wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->users} SET user_status = 1 WHERE ID = %d", $user->ID ))`来吧用户spam了

```php
wp_update_user([
  'ID' => $userId,
  'user_url => 'xxx',
])
```

#### get_user_by

- 通过制定字段获取用户

```php
get_user_by( 'id', $userId );
```

#### get_user_meta

<!--more-->

- 通过用户ID获取用户元信息

- `get_user_meta( int $user_id, string $key = '', bool $single = false)`，`key`表示指定获取某个信息，默认是所有；`single`表示是否获取单个值，如果为`true`则不是返回对象，而是需要获取的`value`

#### get_users

- 获取满足条件的用户列表
- `get_users( *array* $args = array() )`

```php
get_users([
  'include' => $userIds, 	// 指定id列表
  'fields' => ['id', 'user_email', 'user_nicename'],	// 指定获取字段
]);
```

#### WP_User_Query

- 获取满足条件的用户列表

```php
$args  = array(
    'meta_key' => 'customField',
    'meta_value' => ['a', 'b'],
    'meta_compare' => 'IN'	// 支持=/!=/>/>=/</<=/LIKE/NOT/LIKE/IN/NOT/IN/BETWEEN/EXISTS/NOT EXISTS/ REGEXP/RLIKE/NOT REGEXP
);
 
$user_query = new WP_User_Query( $args );
```

### 文章相关函数

```php
# get_permalink, 获取永久链接

# get_post_permalink, 获取文章的永久链接
get_post_permalink( *int|WP_Post* $id, *bool* $leavename = false, *bool* $sample = false );

# query_posts, 查询文章列表
query_posts([
  'post_type' => 'post',	// 搜索指定类型的post
  'posts_per_page' => 100,	// 每页的数量
  'paged' => 2,	// 当前页码，可以自行从query中解析
  'order' => 'ASC',	// 升序、降序
  'orderby' => 'title ID',	// 排序字段
  'meta_query' => [	// 居然可以直接查询postmeta里面的字段
    [
      'key' => 'my_custom_field',
      'value' => 'abc',
      'compare' => '!='	// 支持很多数据库的比较操作，比如=、!=、>、>=、<、<=、LIKE、NOT LIKE
    ]
  ]
]);
$count = 1; 
while (have_posts()) {	// 遍历其结果
  the_post();
  $count += 1;	// 如果要在循环posts里面拿到索引，可以用这个方法
}
```

### 对象相关函数

#### get_the_ID()

- 获取当前遍历的对象的ID

#### get_the_title()

- 获取当前遍历的对象的title

### 全局类/全局变量

```php
# Wp类
global $wp;
home_url($wp->request); // 获取当前访问的完整路由url
$_GET['abc']; // 直接获取url中的query 参数

# Rewrite类
global $wp_rewrite;	// 要调用该类的方法需要先声明一下
$wp_rewrite->wp_rewrite_rules(); // 获取所有的rewrite规则
```

### 数据库相关函数

- `$wpdb`是数据库操作的全局对象

```php
global $wpdb;
$results = $wpdb->get_results( $sql );	// 执行原生SQL

$GLOBALS['wp_query']->request;	// 打印当前文件执行的sql语句
```

### 插件管理相关函数

#### is_plugin_active

- 验证指定插件是否激活

```php
is_plugin_active( 'plugin-directory/plugin-file.php' )
```

### 邮件相关函数

#### wp_mail

- 发送邮件
- `wp_mail( *string|array* $to, *string* $subject, *string* $message, *string|array* $headers = '', *string|array* $attachments = array() )`

```php
// 设置header
$headers = array('Content-Type: text/html; charset=UTF-8');
```

## Hooks

### Actions Hooks

- 内核在执行到指定`action`的时候会直接调用你的函数

#### new_to_publish

#### draft_to_publish

#### pending_to_publish

### Filter Hooks

- 过滤钩子，接收一个值并在可能的修改后进行返回，必须返回传入的第一个参数

#### pre_get_posts 搜索文章/获取文件列表前

```php
// 这个函数可以放到functions.php里面或者其他能够记载的地方
function my_custom_search_posts( $query) {
    if ( $query->is_search() && $query->is_main_query() && ! is_admin() ) {
        $query->set( 'posts_per_page', '50' );	// 可以设置搜索文章每一页的数量，这个可以覆盖后台的Settings > Reading设置，那个是全局的
        $query->set( 'post_type', 'post');	// 限制搜索的类型只能为post
    }
}
add_filter( 'pre_get_posts', 'my_custom_search_posts' );
```

## 接口

### 添加自定义接口

```php
<?php

function customFunc() {
  return 'this is test';
}

function customRoute() {
  register_rest_route('test/v1', 'custom', [
    'methods'   => 'GET',
    'callback'  => 'customFunc'
  ] );
}

add_action( 'rest_api_init', 'customFunc');
```

