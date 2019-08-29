---
title: "Antd "
date: 2019-08-12 14:40:00
categories: Javascript
---



## 组件

### 表单

- 可以使用高阶函数`@Form.create()`直接将一个`React`组件变成一个新的自带表单及其相关方法的组件。会自带`this.props.form`属性

```react
handleValidator = (rule, val, callback) => {
  callback();	// 如果成功则直接返回回调函数
  callback("出错");	// 如果失败则传入提示字符串
}

<Form.Item>
	{getFieldDecorator('field1', {
    initialValue: {this.state.field1},	// 初始化值。需要注意，如果下面的字段组件是自定义字段，那么不应该给自定义value，而应该把value的赋值写在这里，否则会报错`getFieldDecorator will override value, so please don't set value directly and use setFieldValues to set it `
    rules: [{
      required: true,
      message: "请输入字段"
    }, {
      validator: this.handleValidator,	// 自定义验证函数
    }],
  }<MyItem />
  )}
</Form.Item>

this.props.form.setFieldsValue({field1: 'xxx'});	// 用这种方式可以直接给表单字段赋值
```

- 

## TroubleShooting

- ****