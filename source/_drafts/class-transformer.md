- 用于对象(Object)与类(Class/Instance)的互相转换
- 可以非常方便地对接口输入和输出的对象进行转换，去除多余的字段，保留自己想要的字段

## 方法列表

### 类字段装饰器

```javascript
class User {
  @Expose()	// 指定在序列化的时候包括该属性
  id: number;
  
  @Expose({name: 'first_name'})	// 序列化时使用不同的名称
  firstName: string;
  
  @Expose（）	// 同样可以用它来暴露getter方法的返回值
  getFullName() {
    return this.firstName + ' ' + this.lastName;
  }
  
  @Exclude({ toPlainOnly: true})	// 只在instanceToPlain的时候被排除
  password: string;
  
  @Expose({ groups: ['admin']})	// 表示只有在group为admin的时候才暴露该字段
  email: string;
  
  @Exclude()	// 指定在序列化的时候不包括该属性
  createdAt: Date;
  
  // 暴露一个单独的需要computed的字段
  @Expose()
  @Transform(({ value, key, obj, type }) => 'yolo' )
  thisIsATest: string
}
```

### plainToInstance

- 原名`plainToClass`
- 将对象转换为实例

```javascript
const userObj = {id: 123, name: 'abc'}
const user = plainToInstance(User, userObj)

const users = plainToInstance(User, userObjs)	// 不仅可以用于单独的对象，还可以用于列表
```

### instanceToPlain

- 原名`classToPlaind/serialize`

- 将类实例转换为对象，类似于`JSON.stringify`

```javascript
const user = new User()
const userObj = instanceToPlain(user)
const userObj = instanceToPlain(user, {groups: ['admin']})	// 指定group
```

### instanceToInstance

- 原名`classToClass`
- 将类对象实例为一个新的类对实例

