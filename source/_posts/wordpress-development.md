---
title: "wordpressd 开发手册"
date: 2020-10-18 10:26:00
updated: 2020-10-18 15:56:00
categories: php
---

- 在本地开发的时候，由于有很多东西依赖于`cookie`，有些插件在写入`cookie`的时候可能由于没有判断服务端口导致无法写入`cookie`，功能无法正常使用，所以在开发和使用过程中最好用正常的`http`端口，即`80`或`443`

## 帮助函数

### 用户相关函数

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

### get_permalink

- 获取永久链接

#### get_post_permalink

- 获取文章的永久链接
- `get_post_permalink( *int|WP_Post* $id, *bool* $leavename = false, *bool* $sample = false )`

### 数据库相关函数

- `$wpdb`是数据库操作的全局对象

```php
global $wpdb;
$results = $wpdb->get_results( $sql );	// 执行原生SQL
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



