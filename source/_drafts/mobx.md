## 安装配置

```shell
npm install --save mobx
npm install mobx-utils --save	# 最好同时安装这个库，提供了更多的帮助方法，例如带参数的computedFn

# 如果是Typescript，需要在编译选项中设置"useDefineForClassFields": true
```



## 状态定义

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
}
```

