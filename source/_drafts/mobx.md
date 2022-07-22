## 状态定义

- 可以放在`src/stores/xxxxStore.ts` 下

```javascript
import {observable, action, makeObservable} from 'mobx';

class ExampleStore {
  @observable token = '';
  
  constructor() {
    // 如果state和action没有用@observable或者@action装饰，那么这里可以单独makeObservable，一般没有必要的
    makeObservable(this, {	
      token: observable,
      setToken: action
    });
  }
  
  @action setToken(token: string) {
    this.token = token
  }
}
```

