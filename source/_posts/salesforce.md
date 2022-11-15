---
title: "Salesforce 中文操作手册"
date: 2022-06-30 08:02:30
updated: 2022-11-15 1740:00
categories: system
---

## salesforce后台配置

- Lightning Experience就是新版的系统，classic就是老版本，新功能以后都只会出现在Lightning Experience中

### 常用需求操作方式

#### 导出数据

- `Setup -> Data -> Data Export -> Export Now -> Start Export`，大概等个5到10分钟就能在页面下载了

#### 添加navigation菜单到首页

- `Setup -> App Manager `，然后选择自己的首页的app，一般是`Force.com`，进入编辑页面就能看到`Choose the Tabs`设置了

### Sandbox

- Sandbox的[价格表](https://www.salesforce.com/editions-pricing/platform/environments/)，没错，是按照原是数据的价格来按百分比收费的，怪不得很多用户都只是partial copy，得自己想办法去将生产数据同步到sandbox中去。
- 如果不用salesforce自己的Refresh方式，那么想要同步production到sandbox，要么借助第三方的收费工具，要么就自己去同步了，自己同步是个体力活，你必须得找到不同对象之间的关系，新插入的数据和之前的ID肯定是不一样的，整个migration程序都得维护这些ID的映射，相当麻烦
- 注意手动刷新sandbox后，相当于删除旧的创建新的，在旧的sandbox环境里面新建的用户会消失的，新的sandbox的users总是和production的一样，只不过email添加了一个后缀`.sandboxname`

### Apps

- `New Connected App` 菜单在`Apps -> App Manager`里面，而不是在`Apps -> App Manager -> Connected Apps -> Manage Connected Apps`里面
- `App Manager`和`Manage Connected Apps`里面如果有相同的app，那么可能这两个菜单点进去会是不同的设置
- 在设置里面可以设置哪些profile能访问这个app，需要注意的是，即使选择的认证方法是POST的，如果你选择了所有人都能访问app(All users may self-authorize)，那么它仍然不会去使用POST认证，会直接用GET去访问app，所以即使我们要所有人都能访问也要选择只允许选择的人(Admin approved users are pre-authorized)，你可以选择所有的profile都行
- 如果要创建`visual app / canvas app`，那么app必须要允许OAuth
- 如果要把visualforce app作为tab显示在顶部，需要现在Setup里面搜索Tabs，在visualforce里面选择它，最后再在首页的tabs里面添加即可
- 创建了带Oauth的app后就能获取到其client_id和client_secret了(也叫Consumer Key和Consumer Secret)

### Object & Fields

- 对象的Record Types只是用于前端可以根据某个值来展示不同的表单，例如根据role来确定admin和user能设置哪些字段

<!--more-->

### Report

- 一个非常方便的过滤数据的方式，report还能分享和到处excel
- 添加filter logic，首先要添加filter condition，然后在用A or B, A and (B or C)等等的逻辑控制语句来控制

### 回收站Recycle Bin

首页左上角搜索app里面有`Recycle Bin`，最近删除了的对象能在这里找到并恢复

### Debug

- 如果要对网站的用户进行debug，可以在`Setup -> Environments -> Logs -> Debug Logs`中进行设置，如果是调试sites的guest user，只需要new的时候选择指定的user即可

## [数据库客户端](https://pocketsoap.com/osx/soqlx/#Download)

- 发现好多对象在后台看不了，但是用客户端或者sdk能看到

## [jsforce sdk](https://jsforce.github.io/)

### 配置连接

```javascript
var jsforce = require('jsforce');
var conn = new jsforce.Connection({
    loginUrl: process.env.SANDBOX_LOGIN_URL,
    maxRequest: 200,	// 默认最大的并发请求数量(例如同时create多条记录)才10，超过会报错Exceeded max limit of concurrent call，但是这个值最大却只能200，否则也会报这样的错误EXCEEDED_ID_LIMIT: record limit reached. cannot submit more than 200 records into this call
});
conn.login('username@domain.com', `${password}${securityToken}`, function(err, res) {
  if (err) { return console.error(err); }
  conn.query('SELECT Id, Name FROM Account', function(err, res) {
    if (err) { return console.error(err); }
    console.log(res);	// {"totalSize":0,"done":true,"records":[]}
  });
});
```

### 数据库操作

```javascript
conn.describeSObject('Account');	// 获取对象object的数据结构，包括recordTypeInfos
```

### 增删改查

- 针对时间字段，如果是query raw sql， 记得不用加引号: `CreatedDate > 2022-07-19T00:00:00Z`，如果是sobject来查询，可以`const {SfDate} = require("jsforce"); SfDate.SfDate.toDateTimeLiteral('2022-07-19 00:00:00')`

- find方法单次默认只能查询200条记录，可以修改offset，但是最大的offset值也才2000。如果要查询所有，可以这样做

  ```javascript
  const res = await conn.query('SELECT * FROM Contacts');	// 仍然只会返回2000条数据
  const res1 = await conn.queryMore(res.nextRecordsUrl); // 类似于现在有些翻页接口，外面套一个while循环就能遍历所有了
  ```

```javascript
// 查询
await conn.query('SELECT Id, Name FROM Account') // query语句能够实现简单的SQL(SOQL)查询
await conn.sobject("Contact").count()	// 获取所有的记录数
conn.sobject('Contact').count({})	// 统计指定条件的记录数，注意这里不是find再count，而是直接把条件放到count里面
conn.sobject('Account').select('Id, Name') // 获取指定字段
conn.sobject("Contact")	// 类似ORM的查询方式
  .find(
    // conditions in JSON object，查询条件
    {
      LastName : {
      		$like : 'A%',
          $ne: null	// 不等于null
          $not: {	// 非
          	$ne: null
        	}
    	},
  		$or: [
  			{Name: {$like: "ha%"}},
  			{Name: {$like: 'fly%'}},
  		],
      CreatedDate: { $gte : jsforce.Date.YESTERDAY },
      'Account.Name' : 'Sony, Inc.' },
    // fields in JSON object，下面是需要取的字段
    { Id: 1,
      Name: 1,
      CreatedDate: 1
    },
  )
  .sort({ CreatedDate: -1, Name : 1 })
  .limit(5)
  .skip(10)
  .execute(function(err, records) {
    if (err) { return console.error(err); }
    console.log("fetched : " + records.length);
  });

// 也可以写Raw SQL
conn.sobject("Contact")
  .select('*, Account.*') // asterisk means all fields in specified level are targeted.
  .where("CreatedDate = TODAY") // conditions in raw SOQL where clause.
  .limit(10)
  .offset(20) // synonym of "skip"
  .execute(function(err, records) {
    for (var i=0; i<records.length; i++) {
      var record = records[i];
      console.log("First Name: " + record.FirstName); 
    }
  });

// 联表子查询
conn.sobject("Contact")
  .select('*, Account.*')
  .include("Cases") // include child relationship records in query result. 
     // after include() call, entering into the context of child query.
     .select("*")
     .where({
        Status: 'New',
        OwnerId : conn.userInfo.id,
     })
     .orderby("CreatedDate", "DESC")
     .end() // be sure to call end() to exit child query context
  .where("CreatedDate = TODAY")
  .limit(10)
  .offset(20)
  .execute()

conn.sobject("Contact").find({ CreatedDate: jsforce.Date.TODAY })	// 如果要查询所有字段可以不给find第二个参数
conn.sobject("Contact").find({ CreatedDate: jsforce.Date.TODAY }, '*')	// 同上

// 在所有对象上进行搜索
conn.search("FIND {Un*} IN ALL FIELDS RETURNING Account(Id, Name), Lead(Id, Name)",
  function(err, res) {
    if (err) { return console.error(err); }
    console.log(res);
  }
);

// 直接根据主Id获取对象
await conn.sobject("Account").retrieve("0017000000hOMChAAO");
await conn.sobject("Account").retrieve(["0017000000hOMChAAO", "0017000000hOMChAAO"]);	// 获取多个


// 创建记录
await conn.sobject("Account").create({ Name : 'My Account #1' });
await conn.sobject("Account").create([{ Name : 'My Account #1'}, { Name : 'My Account #2'} ]); // 同时创建多条记录
await conn.sobject("Account").create(accounts, {allowRecursive: true}); // 同时创建多条记录，默认一次最多200条，可以添加allowRecursive参数创建更多的记录


// 更新记录
await conn.sobject("Account").update({ 
  Id : '0017000000hOMChAAO',
  Name : 'Updated Account #1'
};
await conn.sobject("Account").update([	// 更新多条
  { Id : '0017000000hOMChAAO', Name : 'Updated Account #1' },
  { Id : '0017000000iKOZTAA4', Name : 'Updated Account #2' }
];
await conn.sobject('Opportunity')	// 查找并更新
    .find({ 'Account.Name' : 'Salesforce.com' })
    .update({ CloseDate: '2013-08-31' }
                                     
                                     
// 创建或者更新upsert
await conn.sobject("UpsertTable__c").upsert({ 
  Name : 'Record #1',
  ExtId__c : 'ID-0000001'
}, 'ExtId__c')
                                     
                                    
// 删除记录
await conn.sobject("Account").destroy('0017000000hOMChAAO');
await conn.sobject('Account').find({xxx}).destroy()
conn.sobject("Account").del(['0017000000hOMChAAO','0017000000iKOZTAA4']; // 删除多条
```

### 常见错误处理

- **DUPLICATES_DETECTED**: 如果在Object Manager没有发现什么唯一键，可以在`Setup -> Data -> Duplicate Management -> Duplicate Rules`里面看看有没有什么检测重复的规则

## 其他Packages配置

### Survey Force

- 一个调查问卷包，可以添加调查问卷给用户
- 如果想要允许外部用户直接访问，那么需要新建sites，新建完成后按照文档修改权限，但是最后有一点需要注意的是创建Survey的时候那个可以复制的地址是代码里面写死的，如果需要修改就要去developer console修改其源代码，且生产环境不允许直接修改。有了sites后真实的访问地址是`${sites_url?id=xxxx` ，这里的ID就是那个survey的id
- 其实其README中的配置步骤还是比较详细，就是可能salesforce后台的UI变了有些配置找不到地方，这里记录一下
  - `Public Access Settings`和文档里面的描述不一样，`View Users`现在是点进`Assigned Users`里面设置，如果要修改那几个object的权限以及Apex Classes，需要在`Public Access Settings`里面设置`Apex Class Access`和` Object Settings`
- 如果出现**Authorization Required**错误，多半是访问的url的问题，可能是id没有填

## Troubleshooting

- **The requested resource no longer exists**: 可能是使用的rest api的版本太低了导致的，可以通过这个方式获取当前支持的API版本列表: [List Available REST API Versions](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_versions.htm)
- **Unable to create/update fields: xxx. Please check the security settings of this field and verify that it is read/write for your profile or permission set**: 需要去检查一下这个字段的权限，在Setup -> Object Manager -> 选择Object再选择Fields，点击`Field Level Security`检查权限
- **Can't alter metadata in an active org**：无法在生产环境直接修改部分代码，只能现在sandbox里面修改了同步过去
