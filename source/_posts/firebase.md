---
title: "Firebase/Firestore 使用手册"
date: 2021-07-15 12:30:00
updated: 2022-09-23 07:55:00
categories: frontend
---

- **一定要看英文文档，中文文档可能更新不及时**
- [官方各个模块的JS的API文档](https://firebase.google.com/docs/reference/js)

## 集成

### 命令行

```shell
sudo npm install -g firebase-tools
```

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

#### Nodejs集成

```shell
npm install firebase-admin
```

#### PHP集成

- [php firestore 文档](https://googleapis.github.io/google-cloud-php/#/docs/cloud-firestore/v1.19.3/firestore/readme)

- 另外一个admin sdk: [firebase-php](https://github.com/kreait/firebase-php)

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

### fcm api

- ~~最简单的测试方式~~: 这种方式已经被弃用了，现在继续使用会报错Deprecated endpoint
- 新的API见[由使用旧版HTTP改为使用HTTP v1](https://firebase.google.com/docs/cloud-messaging/migrate-v1)，新的API需要先通过凭据获取失效好像为1小时的访问令牌才能发送通知。但是这个访问令牌的获取无法简单的用CURL来实现，官方也没提供例子，所以现在最好就用他们的SDK(官方例子中有Node.js/Java/Python/Go/C#)来获取凭据

```shell
curl --location --request POST 'https://fcm.googleapis.com/fcm/send' \
--header 'Authorization: key=server_key' \	# 这里填写server_key
--header 'Content-Type: application/json' \
--data-raw '{
    "notification": {
        "title": "test",
        "body": "testbody"
    },
    "to": "用户的fcm token"
}'
```

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

### [firebase-php](https://github.com/kreait/firebase-php)

- 文档: https://firebase-php.readthedocs.io/en/7.15.0/setup.html

### 证书配置

<!--more-->

- 证书配置在`firebase console -> Project settings -> Cloud Messaging -> ios app configuration`
- 证书有两种，两者任选其一(如果两者都有默认会使用前者)，貌似现在更建议用前者，而且前者没有过期时间
  - `APNs Authentication Key`，develoepr后台`Certificates, Identifiers & Profiles -> Keys -> Create a key -> Apple Push Notifications service (APNs)`，申请完成后下载下来就是一个p8证书
  - `APNs Certificates`，申请步骤
    1. Apple Developer后台，选择你的bundle id，然后点击里面的`Push Notification`权限的`Edit` 就能创建development和production证书了，但是创建证书需要一个Request文件，需要在你自己的电脑上创建这个文件才行
    2. Mac -> Keychain -> 左上角菜单Keychain Access -> Certificate Assistant -> Request a Certificate From a Certificate Authority... -> Saved to disk
    3. Apple Developer后台 -> bundle id -> Push Notification configure -> Create Certificate -> Choose刚才创建的请求文件
    4. 创建后下载，下载下来就是一个`aps.cer`的文件，然后上传到firebase后台即可，注意过期时间是一年
- 要获取apple的team ID，需要在`Developer`后台点击`Membership`查看，参考[Locate your Team ID](https://help.apple.com/developer-account/#/dev55c3c710c)
- 对于PHP的`edujugon/push-notification`库，步骤就还要复杂一点，这里是它官方的wiki: [APNS-Certificate](https://github.com/Edujugon/PushNotification/wiki/APNS-Certificate)，其中`apns-pro-cert.p12`的生成方法是打开keychain，然后切换到左边的`login`，再双击上面的第二种证书`aps.cer`就能导入到keychain了，然后在keychain里面信任该证书，就能导出为`*.p12`文件了，而`apns-pro-key.p12`同样来自于它，不用双击，而是点击左边的下拉选项，下面就是key了，导出成`*key.p12`即可。然后代码里面肯定是不能要密码的，参考wiki用`noenc`就可以了。弄完了后记得用wiki最下面的命令测试一下。如果代码使用的时候出现`Connection problem: stream_socket_client(): unable to connect to ssl://gateway.sandbox.push.apple.com:2195 (Connection refused)`多半是证书配置错了或者没开代理，记住修改证书后可能还有缓存，我尝试过`php artisan config:clear && php artisan cache:clear`都没用，最后直接在`config/pushnotification.php`配置中将`apn.certificate`指向了另外一个文件。
  - 如果出现topic disallowed错误，可以尝试将topic修改为app的bundle id


### 移动端配置

- 安卓端需要`google-services.json`文件，ios端需要`GoogleService-Info.plist`文件，都通过`firebase console -> Project settings -> General`中创建`Add app`添加对应平台的APP，然后下载对应文件即可

## Firebase Auth管理用户

- 可以直接使用firebase的用户系统
- 需要注意的是用户相关的几个action的邮箱模版是不能改变的，例如注册等，如果要自定义，只能自己写个后端，[生成电子邮件操作链接](https://firebase.google.com/docs/auth/admin/email-action-links)

```javascript
firebase.auth().createUserWithEmailAndPassword(email, password)	// 创建用户
firebase.auth().onAuthStateChanged((user) => {})	// 获取当前登陆的用户
const user = firebase.auth().currentUser	// 获取当前用户
const {displayName, email, photoURL, emailVerified,uid} = user 	// 获取用户信息
user.sendEmailVerification()	// 发送认证邮件
user.updateProfile({displayName: 'aabb'})	// 更新用户信息
user.updateEmail('')	// 更新用户邮件
user.updatePassword('') // 更新用户密码
user.sendPasswordResetEmail(email)	// 发送重置密码邮箱
```

- 默认的几种邮件模板都是无法更改内部模板的，如果要自定义，需要自己使用第三方服务或者自己用smtp去发送指定内容的邮件。但是像注册的时候生成认证链接还是可以直接用firebase来做，只不过因为要调用邮件，所以需要在firebase function里面做
  ```javascript
  exports.sendEmailVerificationEmail = functions.https.onCall(async (data, context) => {
    const url = await admin.auth().generateEmailVerificationLink(context.auth.email); // 关键的email信息必须从context.auth里面取，name等信息可以从data里面取然后发送出去
  })
  
  // 然后在客户端调用这个函数即可
  await functions().httpsCallable('sendEmailVerificationEmail')({ username });
  ```

## Realtime Database

```javascript
const admin = require('firebase-admin');

// 替换成你的 Firebase 项目配置文件路径
const serviceAccount = require('path/to/your/firebase/serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://your-project-id.firebaseio.com', // 替换成你的项目数据库URL
});

const database = admin.database();
const ref = database.ref('/your/path/to/listen'); // 替换成你想监听的路径

ref.on('value', (snapshot) => {
  const data = snapshot.val();
  console.log('Data changed:', data);
});

// 如果需要监听其他事件，比如子节点的增加、删除等，可以使用其他事件名，如 'child_added', 'child_removed' 等。
// child_added: 如果是数组，那么每次在开始监听的时候所有的child都会触发child_added事件
```

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

// realtime database的安全规则
{
  "rules": {
    "$log_key": {
      ".validate": "$log_key.matches(/^logs-.+/)",	// 使用正则匹配
      ".read": true,
      ".write": true
    },
    ".read": false,
    ".write": false
  }
}
```

### 数据读写

#### 数据写入

```javascript
const doc = db.doc('collection_name/doc_id')
await doc.set({name: 'test'})	// 不存在则新建，存在则会覆盖
await doc.set({name: 'test'}, { merge: true })	// 不存在则新建，存在则会合并
await doc.delete()	// 删除数据
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

### [Nhost: 开源的firebase替代品](https://blog.graphqleditor.com/nhost?continueFlag=5434b3101edf4c6102e182af7801175f)

## Firebase Function

- 类似于Google cloud function或者lambda

- 常用命令：

  ```shell
  npm install -g firebase-tools	# 安装命令行工具
  export GOOGLE_APPLICATION_CREDENTIALS="path-to-project-xxxxx.json"	# 设置管理员凭证
  
  firebase emulators:start	# 本地运行
  firebase emulators:start --only functions	# 仅运行firebase function
  
  # 部署到云端
  firebase deploy 
    --only functions	# 部署所有的函数
  	--only functions:sendEmailVerificationEmail 	# 仅部署指定函数
  	--project=myproject	# 指定项目
  	
  # 环境变量
  firebase functions:config:get > .runtimeconfig.json	# 获取远端的自定义配置到本地的文件中去
  ```

- 新创建的firebae function在调用的时候可能会得到一个UNAUTHENTICATED错误，需要这样做: `firebase function -> permissions -> add principal`，在`New principals field`输入`allUsers`，然后选择role Cloud Functions ，然后选择Cloud Functions Invoker

- 函数有多种调用方式

```javascript
// 直接以http的方式访问函数
exports.date = functions.https.onRequest((req, res) => {
  // ...
});

// 在代码内以函数方式直接进行调用
exports.addMessage = functions.https.onCall((data, context) => {
  // ...
});
import { getFunctions, httpsCallable } from "firebase/functions";
const functions = getFunctions();
const addMessage = httpsCallable(functions, 'addMessage');
addMessage({ text: messageText }).then((result) => {});	// 代码里面这样调用即可

// 下面是react-native-firebase的调用方式
import functions from '@react-native-firebase/functions';
const res =  await functions().httpsCallable('addMessage', {});


// 定时执行
exports.scheduledFunction = functions.pubsub.schedule('every 5 minutes').onRun((context) => {
  console.log('This will be run every 5 minutes!');
  return null;
});

// 当firestore触发某个事件的时候
// 事件包括：onCreate、onUpdate、onDelete、onWrite
exports.myFunction = functions.firestore.document('my-collection/id1').onWrite((change, context) => { }); // 指定特定的文档
exports.myFunction = functions.firestore.document('my-collection/{docId}').onWrite((change, context) => {  context.params.docId });	// 通配符指定文档

// 身份验证触发器
// 事件包括onCreate、onDelete
exports.sendWelcomeEmail = functions.auth.user().onCreate((user) => {
  // ...
});

// 不常用的还包括实时数据库触发器、远程配置触发器、Analytics触发器、Cloud Storage触发器、Pub/Sub触发器、Test Lab触发器

// 如果要返回base64格式的pdf内容，可以这样做，注意，pdfStr是不带data:application/pdf;base64,前缀的
res.setHeader('Content-type', 'application/pdf');
res.end(Buffer.from(pdfStr, 'base64'));
```

## TroubleShooting

- **TypeError: instance.INTERNAL.registerComponent is not a function** 需要`npm install @firebase/app --save`
- **firebase发送消息出现`firebae Requested entity was not found.`**: 一般是证书没配置好
- **MismatchSenderId**: 一般是证书选错了，可能选到了其他项目的证书，或者移动端选择了其他项目的证书
- **Android更换google-services.json文件不生效**: 如果是android studio，需要`Buidl -> Rebuild Project`一下
- **如果push notification在app那边无法注册**：可能原因有
  - mobile没有开vpn
  - google-service.json文件不对
  - mobile不支持google service框架(**MISSING_INSTANCEID_SERVICE**)