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

### 增删改查

```javascript
// 查询
await conn.query('SELECT Id, Name FROM Account') // query语句能够实现简单的SQL(SOQL)查询
conn.sobject("Contact")	// 类似ORM的查询方式
  .find(
    // conditions in JSON object，查询条件
    { LastName : { $like : 'A%' },
      CreatedDate: { $gte : jsforce.Date.YESTERDAY },
      'Account.Name' : 'Sony, Inc.' },
    // fields in JSON object，下面是需要取的字段
    { Id: 1,
      Name: 1,
      CreatedDate: 1 }
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
await conn.sobject("Account").create(accounts, {allowRecursive: true}); // 同时创建多条记录，默认一次最多200条，可以添加allowRecursive参数


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
conn.sobject("Account").del(['0017000000hOMChAAO','0017000000iKOZTAA4']; // 删除多条
```

