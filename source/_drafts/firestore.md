firestore使用手册

**一定要看英文文档，中文文档可能更新不及时**

## 认证规则

## 安全规则

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{user_id} {
      allow read: if resource.data.user == request.auth.uid; // 可以通过resource.data获取该条记录的字段
      allow read: if request.auth != null;	// 验证是否登陆
      allow create: if request.auth != null && exists(/databases/$(database)/documents/users/$(request.auth.uid))	// 通过其他文档来验证
    	allow read: if int(resource.data.number) > 1 // 数据转换为整型int
      allow read: if request.time.toMillis() >= timestamp.date(2021,1,1).toMillis();	// 验证请求时间
      
      // 还能自定义函数
      allow create: if request.time.toMillis() > getTheTime();
      function getTheTime() {
        return (getAnotherTime().seconds + duration.value(12, 'h').seconds()) * 1000;
      }
      function getAnotherTime() {
        return get(/databases/$(database)/documents/user/$(request.auth.uid)).data.lastSendNotification;
      }
      
      // 仅允许更改某些字段
      allow update: if (request.resource.data.diff(resource.data).affectedKeys()
        .hasOnly(['name', 'location', 'city', 'address', 'hours', 'cuisine']));
    }
    }

    match /users/{userid}/exchange/{exchangeid}/transactions/{transaction} {
      // Authenticated users can write to their own transactions subcollections
      // Writes must populate the user field with the correct auth id
      allow write: if userid == request.auth.uid && request.data.user == request.auth.uid
    }
  }
}
```

## 数据读写

### 数据读取

- `where`支持的查询运算符有: `<`、`<=`、`==`、`>`、`>=`、`!=`、`array-contains`、`array-contains-any`、`in`(数组中最多10个元素)、`not-in`(数组中最多10个元素)

- 如果要将等式运算符`==`与范围运算符(除`==`以外的几个)结合使用，必须创建复合索引，否则会报错

- 仅能对单个字段执行范围比较，并且一个复合查询中最多只能包含一个`array-contains`子句，例如`
  citiesRef.where("state", ">=", "CA").where("population", ">", 100000)
  test.firestore.js`是无效的


```javascript
var citiesRef = db.collection("cities");	// 定义要查询的集合

// 简单查询
var query = citiesRef.where("state", "==", "CA")
	.get()
	.then(function(querySnapshots) {
    querySnapshots.forEach(function(doc) {
      console.log(doc.data().name);
    })
  });

// 数组的包含查询
citiesRef.where("regions", "array-contains", "west_coast")

// 复合查询
citiesRef.where("state", "==", "CA").where("population", "<", 1000000)

// 排序，但是排序如果使用的是范围比较运算< <= > >=，那么排序字段必须和范围比较的字段一致才行
citiesRef.orderBy("name").limit(3);
citiesRef.orderBy("name", "desc").limit(3);
citiesRef.orderBy("state").orderBy("population", "desc");	// 多个字段排序
```

#### 侦听实时更新

- 在建立侦听的第一次会直接获取一份文档快照
- PHP客户端库不支持实时监听器

```javascript
// 监听单个文档
db.collection("cities").doc("SF")
    .onSnapshot(function(doc) {
        console.log("Current data: ", doc.data());
    });

// 使用条件监听多个文档
db.collection("cities").where("state", "==", "CA")
    .onSnapshot(function(querySnapshots) {
        querySnapshots.forEach(function(doc) {
          console.log(doc.data().name);
        });
    });
```

## [在CloudFirestore中构建在线状态系统](https://firebase.google.com/docs/firestore/solutions/presence)

- 由于得依赖Cloud Functions，所以没去实践，不过我想Cloud Functions就是一个实时运行的方法，如果只是本地服务端去代替这一块感觉有可能

##### TroubleShooting

- **TypeError: instance.INTERNAL.registerComponent is not a function** 需要`npm install @firebase/app --save`