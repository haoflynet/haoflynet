- 使用起来比`redux`好用多了，就凭这一点我就放弃`redux`了
- redux将数据保存在单一的store中，mobx则是分散在多个store中
- [react-mobx-typescript-realworld-example-app](https://github.com/7anshuai/react-mobx-typescript-realworld-example-app): 一个很好的example项目

## 安装配置

- [React集成方式](https://mobx.js.org/react-integration.html): 注意看里面的Tips，如果不是用的`mobx-react-lite`，很多东西就不用写了，比如Provider，observable props(不需要在组件外部包裹observer了，默认store变化的时候会自动重新渲染)，并且observer自动使用的就是React.memo，不需要单独为了优化性能去useMemo

```shell
npm install --save mobx
npm install mobx-utils --save	# 最好同时安装这个库，提供了更多的帮助方法，例如带参数的computedFn

# 如果实用Typescript或者https://mobx.js.org/enabling-decorators.html可以参考这个文档修改一下配置即可
```

## 状态定义

- 多种类型的store可以单独创建多个store，并且如果要互相调用时没问题的，mobx也支持这种嵌套调用方式
- [一个项目example](https://github.com/7anshuai/react-mobx-typescript-realworld-example-app)：非常实用的一个例子，它其实是在action里面调用api的，我的实际项目通常会使用[reqct-query](https://haofly.net/react-query)，所以我还是在外部用useQuery来调用的，然后在API里直接调用action来更新状态
- 可以放在`src/stores/xxxxStore.ts` 下

```javascript
import {observable, action, makeObservable} from 'mobx';

type User = {
 	id: string;
  token: string;
}

class ExampleStore {
  @observable user: User;
  
  constructor() {
    // 如果state和action没有用@observable或者@action装饰，那么这里可以单独makeObservable，一般没有必要的
    makeObservable(this, {	
      token: observable,
      setToken: action
    });
  }
  
  @action setToken(token: string) {
    this.user.token = token
  }
  
  @computed get name(): string {
    return this.user.firstName + this.user.lastName
  }

	// 带参数的computedFn，目前还不支持作为装饰器直接使用，所以只能这样定义，另外，它的参数是不支持默认值的
  test = computedFn((param) => {
    return ...
  })
}
```

