```javascript
import Ember from 'ember';

export default Ember.Route.extend({
  // 允许你为特定的控制器设置属性和执行其他必要的操作
  setupController(controller, model) { // controller表示当前路由对应的控制器实例，model表示当前路由的模型数据，感觉相似设置
  	controller.set('model', model);
	}
  currentRequest: null,

  actions: {
    willTransition(transition) { // 路由切换前调用
      // 在路由切换之前取消当前请求
      const currentRequest = this.get('currentRequest');
      if (currentRequest && currentRequest.abort) {
        currentRequest.abort();
      }
    }
  },

  model() {	// model函数用于定义当前路由所需的数据，然后该数据会传递给模板
    // 发起新的请求，并存储请求对象
    const request = Ember.$.ajax({
      // 请求参数
    });

    this.set('currentRequest', request);

    return request;
  }
});
```

## Mirage

- 是一个用于模拟服务器端行为和数据的插件，允许在开发过程中创建一个虚拟的API层

## Mixin

- 一个可重用的代码块，只要继承自它就能用它的方法等

```javascript
import Ember from 'ember';

const MyMixin = Ember.Mixin.create({
  // 定义 Mixin 的属性和方法
  property1: 'Mixin Property',
  
  method1() {
    console.log('Mixin Method');
  }
});

export default Ember.Component.extend(MyMixin, {
  // 组件的其它属性和方法
  componentProperty: 'Component Property',

  actions: {
    doSomething() {
      // 调用 Mixin 的方法
      this.method1();

      // 访问 Mixin 的属性
      console.log(this.property1);
    }
  }
});

```

