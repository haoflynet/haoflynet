---
title: "Wordpress自定义字段扩展ACF——Advanced Custom Fields"
date: 2020-10-05 10:26:00
categories: php
---

## PHP API

### Functions

#### get_field

- 获取字段值

#### get_field_object

- 获取字段对象，包含了字段的原名和别名

<!--more-->

### Filters

#### load_field

- 当加载某个字段的时候，对加载到的数据进行处理
- 如果前端字段编辑界面的条件无法满足我们的需求，就可以在这里设置自定义的字段加载条件

```php
function my_acf_load_field( $field ) {
    return $field;
}
add_filter('acf/load_field/name=myField', 'my_acf_load_field');
```

## Js API

### Functions

#### get_fields

- 获取当前页面字段实例列表

```javascript
var fields = acf.getFields({
    type: 'image'
});
```

### Filters

#### select2_ajax_data

- 在发送`ajax`获取请求前对请求的数据进行处理

```javascript
acf.add_filter('select2_ajax_data', function( data, args, $input, field, instance ){
    // do something to data
    return data;
});
```

