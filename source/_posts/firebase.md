---
title: "Firebase/Firestore 使用手册"
date: 2021-07-15 12:30:00
updated: 2021-08-13 07:55:00
categories: frontend
---

- **一定要看英文文档，中文文档可能更新不及时**
- [官方各个模块的JS的API文档](https://firebase.google.com/docs/reference/js)

## 集成

### 前端集成

#### Web端

- 官网在新建web app的时候会给一个example，引入两个script即可。如果是npm进行管理可以直接`npm install --save firebased`
- 对于私有数据，我们需要创建规则来限制前端的访问，[通过后端生成的令牌来进行验证signInWithCustomToken](https://firebase.google.com/docs/auth/web/custom-auth?hl=zh-cn)

```javascript
import firebase from "firebase/app";	// 使用时这样引入，这句话必须有

import "firebase/firestore";	// 如果只想使用其中的一个模块，可以import其中某一个。而且要注意这里不要写成firebase/database

// firebase是一个全局的变量，这样可以防止多次初始化出现错误Firebase App named '[DEFAULT]' already exists (app/duplicate-app) [duplicate]
if (!firebase.apps.length) {
  firebase.initializeApp({
    apiKey: '<your-api-key>',
    authDomain: '<your-auth-domain>',
    databaseURL: '<your-database-url>',
    projectId: '<your-cloud-firestore-project>',
    storageBucket: '<your-storage-bucket>',
    messagingSenderId: '<your-sender-id>',
    appId: '<your-app-id>'
  })
} else {
  firebase.app()
}

const db = firebase.firestore();
```

### 后端集成

- 如果前端需要读取私有数据，那么后端需要为前端[创建自定义令牌createCustomToken](https://firebase.google.com/docs/auth/admin/create-custom-tokens?hl=zh-cn)

- 下面的认证文件`项目名-firebase-adminsdk-xxxxx.json`来自于`firebase console -> Project settings -> Service accounts -> Firebase Admin SDK -> Generate new private key`，是所有SDK都需要的

- 后端只需要`npm install --save firebase-admin`即可

```javascript
import * as admin from 'firebase-admin'
import { HttpsProxyAgent } from 'https-proxy-agent'	// 只能以这种方式使用代理，直接在命令行使用export不行

const agent = new HttpsProxyAgent('http://127.0.0.1:1080')
admin.initializeApp({
	credential: admin.credential.cert(path.join(__dirname, '../../项目名-firebase-adminsdk-xxxxxxxx.json'), agent),
      httpAgent: agent
})
```

#### PHP集成

- [php firestore 文档](https://googleapis.github.io/google-cloud-php/#/docs/cloud-firestore/v1.19.3/firestore/readme)

- 安装方式(需要ext-grpc扩展)

  ```shell
  # 如果仅仅使用firestore可以只安装某个组件
  composer require google/cloud-firestore --with-all-dependencies	# 加这个参数防止guzzlehttp/psr7版本错误
  
  # 一次安装所有
  composer require google/cloud --with-all-dependencies
  ```

- 使用方式

  ```php
  # export GOOGLE_APPLICATION_CREDENTIALS=认证文件路径
  $firestore = new FirestoreClient();
  $document = $firestore->document('users/123');
  $document->set([
    'name' => 'test'
  ]);
  ```

## Cloud Messaging(Push Notification/APNs)

### [firebase-admin-node](https://github.com/firebase/firebase-admin-node)

- 强烈建议在开发时先使用这个包进行测试，因为这个包能够返回非常详细的错误信息，特别是证书没配置对这些信息，而且这个包在使用代理的情况下工作很好，不会像移动端那样，有时候连代理不行，有时候不连代理不行

```javascript
import * as admin from 'firebase-admin'

// 参照上面的后端集成步骤，初始化admin
const payload = {
  data: {
    foo: 'bar',
    notification_foreground: 'true'	// 这样能使客户端收到消息的时候app即使在前台也同样能弹出消息，否则前台就需要自己去处理了，这里的true必须是字符串
  },
  notification: {
    title: 'Message title',
    body: 'Message body'
  }
}

admin.initializeApp({
  credential: admin.credential.cert(path.join(__dirname, '../../xxxxxx-firebase-admin-xxxxx-xxxxxx.json'), agent),
      httpAgent: agent
})

admin.messaging().sendToDevice('registrationToken', payload, { timeToLive: 120})
  .then((response) => {
      console.log(JSON.stringify(response))
  })
```

#### 证书配置

<!--more-->

- 证书配置在`firebase console -> Project settings -> Cloud Messaging -> ios app configuration`
- 证书有两种，`APNs Authentication Key`和`APNs Certificates`，两者任选其一(如果两者都有默认会使用前者)，貌似现在更建议用前者，而且前者没有过期时间，可以参考这里[How to Create an iOS APNs Auth Key](https://developer.clevertap.com/docs/how-to-create-an-ios-apns-auth-key)，也是相当简单的，创建一个Apns的key，然后下载p8证书，然后上传到firebase后台即可，后者的话过期时间是一年。需要这样做：
  1. Apple Developer后台，选择你的bundle id，然后点击里面的`Push Notification`权限的`Edit` 就能创建development和production证书了，但是创建证书需要一个Request文件，需要在你自己的电脑上创建这个文件才行
  2. Mac -> Keychain -> 左上角菜单Keychain Access -> Certificate Assistant -> Request a Certificate From a Certificate Authority...
  3. 创建后下载，然后上传到firebase后台即可
- 要获取apple的team ID，需要在`Developer`后台点击`Membership`查看，参考[Locate your Team ID](https://help.apple.com/developer-account/#/dev55c3c710c)

### 移动端配置

- 安卓端需要`google-services.json`文件，ios端需要`GoogleService-Info.plist`文件，都通过`firebase console -> Project settings -> General`中创建`Add app`添加对应平台的APP，然后下载对应文件即可

## Firestore Database

### 结构设计

- 尽量像GraphQL那样按照前端需要的来设计结构而不是直接把后端的db结构搬上去

- 可以使用嵌套的collection设计，例如，前端需要读取当前用户的notifications列表，可以这样设计:

  ```shell
  users集合
  	- username字段
  	- avatar字段
  	- notifications集合	# 嵌套集合，这样能够将notifications限制到当前user中去，而不用单独在最外层建一个collection，查询的时候还得多一个条件；另一方面，相比于直接在user里面添加一个array字段，它又能用到collection的一些语法，例如我们监听collection但是不能监听指定的字段，如果是一个子字段每次user中的任何字段变动都得返回所有东西；这样即使前端只监听user，并不会响应其notifications的事件。减少了读写次数且减少了数据里那个，而且好查询一点，前端只需要"users/{id}/notifications"即可。互相不会干扰
  		- read字段
  		- time字段
  ```

### [读写限制](https://firebase.google.com/docs/firestore/quotas)

- 开发前先看一下读写限制，至少在设计数据结构以及读写逻辑的时候能够少踩一些坑
- 文档的最大持续写入速率为1次/1秒(超过会报错`Deadline Exceeded`)
- 文档每天的免费读写次数分别为5万次，文档删除次数为2万次

### 认证规则

### 安全规则

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

### 数据读写

#### 数据写入

```javascript
const doc = db.doc('collection_name/doc_id')
await doc.set({name: 'test'})	// 不存在则新建，存在则会覆盖
await doc.set({name: 'test'}, { merge: true })	// 不存在则新建，存在则会合并
```

#### 数据读取

- `where`支持的查询运算符有: `<`、`<=`、`==`、`>`、`>=`、`!=`、`array-contains`、`array-contains-any`、`in`(数组中最多10个元素)、`not-in`(数组中最多10个元素)

- 如果要将等式运算符`==`与范围运算符(除`==`以外的几个)结合使用，必须创建复合索引，否则会报错

- 仅能对单个字段执行范围比较，并且一个复合查询中最多只能包含一个`array-contains`子句，例如`
  citiesRef.where("state", ">=", "CA").where("population", ">", 100000)
  test.firestore.js`是无效的


```javascript
var citiesRef = db.collection("cities");	// 定义要查询的集合

const doc = await db.doc(`${collectionName}/${docId}`).get()
doc.exists	// 是否存在

// 读取集合下所有的文档
db.collection('cities').get().then((querySnapshot) => {
  querySnapshot.forEach((doc) => {
    console.log(JSON.stringify(doc.data()))
  })
})

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

// PHP查询单个文档
$docRef = $db->collection('cities')->document('SF');
$snapshot = $docRef->snapshot();
if ($snapshot->exists()) {
    print_r($snapshot->data());
}
// php查询多个文档
$citiesRef = $db->collection('cities');
$query = $citiesRef->where('capital', '=', true);
$docs = $query->documents();
```

##### 侦听实时更新

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

### [在CloudFirestore中构建在线状态系统](https://firebase.google.com/docs/firestore/solutions/presence)

- 由于得依赖Cloud Functions，所以没去实践，不过我想Cloud Functions就是一个实时运行的方法，如果只是本地服务端去代替这一块感觉有可能

## TroubleShooting

- **TypeError: instance.INTERNAL.registerComponent is not a function** 需要`npm install @firebase/app --save`
- **firebase发送消息出现`firebae Requested entity was not found.`**: 一般是证书没配置好
- **MismatchSenderId**: 一边是证书选错了，可能选到了其他项目的证书，或者移动端选择了其他项目的证书