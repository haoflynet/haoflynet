---
title: "Antd "
date: 2019-09-05 14:40:00
categories: Javascript
---

## 组件

### 表单

- 可以使用高阶函数`@Form.create()`直接将一个`React`组件变成一个新的自带表单及其相关方法的组件。会自带`this.props.form`属性

```react
@Form.create(
	mapPropsToFields: props => {}	// 直接将父组件的属性映射到表单上
	onValuesChange: (props, changedValues, allValues) => {}	// 任一表单域的值发生改变时的回调
)
export default class TicketDetail extends PureComponent {
  
handleValidator = (rule, val, callback) => {
  callback();	// 如果成功则直接返回回调函数
  callback("出错");	// 如果失败则传入提示字符串
}

// 自定义表单的排列样式，例如让label和字段左右显示
const formItemLayout = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 5 },
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 12 },
  },
};

render() {
  return
<Form 
  {...formItemLayout}
  labelAlign={"right"}	// label的对齐方式
  >
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
</Form>
}
}
this.props.form.setFieldsValue({field1: 'xxx'});	// 用这种方式可以直接给表单字段赋值
```

- 

## TroubleShooting

- ****