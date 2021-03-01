---
title: "Mongoose 使用手册"
date: 2021-01-10 14:40:00
updated: 2021-02-26 08:01:00
categories: Javascript
---

## Model定义

- 如果不定义`collection`的名称，`mongoose`会自动将Model名转换为小写复数形式作为`collection`名

```javascript
import mongoose from 'mongoose';
var Schema = mongoose.Schema;

var UserSchema = new Schema(
    {
      name: String,
      is_active: {
        type: Boolean,
        default: false
      },
      created_at: {
        type: Date,
        default: Date.now
      },
      friends: [{	// 可以直接用.populate查出关联对象
        type: Schema.Types.ObjectId,
        ref: 'User'
      }],
      father: {
        type: mongoose.Schema.Types.ObjectId,
    		ref: 'User'
      },
      meta: Object,
      meta1: {	// 也可以这样定义Object
        name: String,
        age: Number
      },
      tags: {
        type: [String],
        index: true		// 定义某个字段为索引
      }
    }, {
      collection: "自定义collection名称",
      toJSON: {virtuals: true},
      toObject: {virtuals: true}
    }
)
UserSchema.index({name: 1, type: -1}); // 在最后指定索引

// 给Model添加查询帮助方法
UserShchema.query.byName = function(name) {
  return this.where({ name: new RegExp(name, 'i')})
};
UserSchema.find().byName('name').exec((err, animals) => {});

// 给实例添加自定义的方法
UserSchema.methods.myFunc = function() {
  mongoose.model('UserSchema')	// 在实例定义里面可以通过这个方法获取Schema Model
  return this	// this就是该实例本身
}

// 给Model添加静态方法
UserSchema.statics.findByName = function(name) {
  return this.find({name: new RegExp(name, 'i')});
}
// 或者这样定义，不要用ES6里面的=>，因为用=>无法通过this获取到Schema
UserSchema.static('findByName', function(name) { return ... });
const user = await UserSchema.findByName('name')

export default mongoose.model('User', UserSchema);

// 甚至可以不定义每个字段，直接用
mongoose.model('User', new Schema(), 'UserSchema');	
```

<!--more-->

### 定义关联关系Virtuals

- `virtuals`相当于外键，可以直接用它来查询关联表，类似于`Laravel`中的`belongsTo`等
- 应该算是`$lookup`的一种特殊情况

```javascript
// 各个字段的含义一目了然
UserSchema.virtual('posts', {
  ref: 'Post',
  localField: '_id',
  foreignField: 'user_id',
  justOne: false,
  options: {
    sort: {
      created_date: -1
    }
  },
  count: false // 如果设置该选项为true，那么将仅仅返回数量，user.posts=数量
})

// 在查询user时候可以直接将virtual作为populate
User.find().populate({
    path: 'posts',
    select: ['type', 'status', 'id', 'created_date']
})
```

#### 多态关联

- 例如，定义一张评论表，评论可以针对文章和产品

```javascript
const commentSchema = new Schema({
  body: { type: String, required: true },
  on: {
    type: Schema.Types.ObjectId,
    required: true,
    refPath: 'onModel'
  },
  onModel: {
    type: String,
    required: true,
    enum: ['BlogPost', 'Product']
  }
});

const Product = mongoose.model('Product', new Schema({ name: String }));
const BlogPost = mongoose.model('BlogPost', new Schema({ title: String }));
const Comment = mongoose.model('Comment', commentSchema);
```

### Schema Options

- 在定义Schema除了设置字段外，还能设置其他一些数据库层面的属性，不过一般不需要用到
- 非常有用的大概是`timestamps`

```javascript
const UserSchama = new Schema({...}, {
	autoIndex: true,
  autoCreate: false,  
  bufferCommands: true,
  bufferTimeoutMS: 10000,
  capped: 1024,	// 设置该值，表示该集合为限制大小的集合，当达到最大值时会自动覆盖最早的文档
  collection: 'data',	 // 单独指定collection名
  id: true,	// 是否可以通过.id获取._id
  _id: true,	// 是否默认添加_id
  minimize: true, // 对于空字段是否不存储
  read: "primary",
  writeConcern: {
    w: 'majority',
    j: true,
    wtimeout: 1000
  },
  shardKey: "",
  strict: true,
  strictQuery: false,
	toJSON: {
    getters: true, 
    virtuals: false                      
  },
  toObject: {
    getters: true, 
    virtuals: false 
	},
  typeKey: "$type",
  validateBeforeSave: true,
  versionKey: "__v",
  optimisticConcurrency: true,
  collation: { locale: 'en_US', strength: 1 },
  skipVersioning: true,
  timestamps: true,	// 类似于Laravel的timestamps功能，能够自动给schame添加createdAt和updatedAt字段
  useNestedStrict: true,
  selectPopulatedPaths: false,
  storeSubdocValidationError: false,
});
```

## 数据库操作

- **对象的ID字段是ObjectID类型，不能直接用于String的比较，可以使用user.userId.equals()方法来进行比较**，这一点有点迷，有些时候可以有些时候不行

### 查询记录

```javascript
User.countDocuments(filters).exec((count_error, count) => {})	// 执行count操作
User.estimatedDocumentCount()	// 同样是count不过count的整个集合，直接读取的metadata，不用扫全表

User.find(function(err, res){
    console.log(res)
})


User.find({}, 'age');	// 选择某个字段
User.find({}, {age: 1});	// 同上
User.find({}, '-age');	// 不选择某个字段
User.find({}, {age: 0}); // 同上

User.findById('abc');	// 通过ID查询

User.findOne({
  username: 'haofly',
  isActive: true,
  name: {$regex: new RegExp(keyword, "i")}},	// LIKE查询，不区分大小写
	name: {
  	last: "hao"	// 匹配嵌套对象的值
  }
  'name.last': 'hao', // 同上   
  id: {	// 比较操作符，不要针对数组，如果这些操作符用于数组，那么表示只要其中一个值满足即可，数组校验需要用到$elemMatch
    $in: ["123", "321"],	// IN
    $nin: ["123"],	// NOT IN
    $eq: 12,	// 等于
    $ne: 12, // 不等于
    $gt: 12, // 大于
    $gte: 12, // 大于等于
    $lt: 12, // 小于
    $lte: 12, // 小于等于
  },
  // 逻辑操作符
  $and: [{expression1}, {expression2}],
  $nor: [{expression1}, {expression2}],
  $or: [{expression1}, {expression2}],
  age: {
    $not: {
      $gt: 12
    }
  },
  books: {
    $all: ["abc", "def"]	// 查找该数组字段是否同时存在这两个值
  }
  ages: {
    $elemMatch: {	// 需要单个字段值满足所有查询条件
      $gt: 12,
      $lt: 15
    }
  }
  'ages.1': {$gt: 12}	// 可以根据数组下标查询指定元素
})
	.offset(0)
	.limit(10)	// 分页
	.sort('-created_at') // 排序
	.select: ["username", "email"] // 选取指定字段
	.select({"username" :1, "email": -1}) // 包含/不包含某些字段
	.populate(['father'])	// 查询关联对象，相当于left join
	.populate({
  	path: 'friends',	// 获取关联对象
  	select: 'username',	// 仅获取关联对象的某个字段
  	select: ['username', '-email'],	// select多个字段，复数表示去掉某个字段
  	match: {	// 在关联对象上使用where对象，注意这里如果不匹配只是会把关联对象设置为null，而不是把父级对象设置为null，相当于这是left join中的一个额外的ON条件，而不是where条件
  		username: {
  			$regex: '.*' + keyword + '.*',	// 正则查询
        $regex: new RegExp(keyword, "i"),	// 忽略大小写查询
			}
		},
    populate: [{	// 还能继续联合多张表
      path: 'inviteBy',
      select: ['username']
    }]
	})
  .then(user => {
  	console.log(user)
	})
  .catch((err) => {
  	console.log(err)
	})

// 除了上面的then...catch...还可以使用exec来获取查询结果
let query = User.find({}).where('age').gt(12).select('name age -_id')
query.exec((err, result) => {})

// 或者加上then
query.then(
	(res) => {console.log(res)}
  (err) => {console.log(err)}
);
```

### 创建记录

```javascript
var user = new User({
    name: 'haofly',
    date: new Date()
})
user.save(function(err, res){...}


// 或者直接create
const user = User.create({name: 'haofly'})
```

### 更新记录

```javascript
doc.name = 'foo'
await doc.save()	// mongoose其实执行的是updateOne({ _id: doc._id }, { $set: { name: 'foo' } })
doc.save().then(doc => {})	// 异步


User.findByIdAndUpdate(id, {})

User.findOneAndUpdate({
  _id: 'xxxxxxxxxxxx'
}, {
  $set: {
    'name': 'lvelvelve'
  },
  $inc: {	// 直接increment
    'count': 1 // 也可以-1
  },
  $addToSet: {	// 可以直接push进一个数组/集合
    friends: userId
  },
  $pull: {			// 从数组/集合中移出对象
    friends:: userId
  }
}, {
  new: true	// 返回更新后的数据
})

// 同时更新多条记录
User.updateMany({
  type: "xxx"
}, {
  $set: {
    status: 0
  }
})
```

### 删除记录

```javascript
User.remove({_id: 'xxxxxxxxxxxx'})	// 返回值是CommandResult对象result{n:1,ok:1}
User.deleteOne({ _id: doc._id });
```

## 数据库事件/中间件hook

### pre发生前

```javascript
// 我们可以为pre find总是添加populate
MySchema.pre('find', function() {
  this.populate('user');
});

// 保存前
MySchema.pre('save', async function() {
  await doStuff();
})
```

### post发生后

```javascript
// 在find后进行populate
MySchema.post('find', async function(docs) {
	await Promise.all(docs.map(async (doc) => {
    doc.field1 = 'value'
    await doc.save()
  }))
});
MySchema.post('findOneAndUpdate', function(doc) {})
MySchema.post('findOneAndRemove', function (doc) {})


// 在save后进行populate
MySchema.post('save', function(doc) {})
MySchema.post('save', function(doc, next) {
  doc.populate('user').execPopulate().then(function() {
    next();
  });
});

// update后
MySchema.post('update', function () {
  this.model.find(this._conditions).then(docs => {
    docs.forEach(doc => {})
  }).catch(() => {
  })
})
MySchema.post('updateOne', function () {
  this.model.find(this._conditions).then(docs => {
    docs.forEach(doc => {})
  }).catch(() => {
  })
})
MySchema.post('updateMany', function () {
  this.model.find(this._conditions).then(docs => {
    docs.forEach(doc => {})
  }).catch(() => {
  })
})


MySchema.post('init', function(doc) {})
MySchema.post('validate', function(doc){})
```

## 重要的对象

### CommandResult

- result: n表示更改的对象的条数，ok表示是否成功，nModified表示有多少次更改

## TroubleShooting

- **mongoose create的时候怎么也拿不到返回的id**: 可能是在给`create`的参数中传入了`id=null`的值，导致程序没有从数据库获取而是直接返回的传入值null
- **"co" is not defined**: `co`是另外一个库的东西`const co = require('co')`