---
title: "Mongoose 使用手册"
date: 2019-09-05 14:40:00
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
      friends: [	// 可以直接用.populate查出关联对象
        Schema.Types.ObjectId
      ],
      father: {
        type: mongoose.Schema.Types.ObjectId,
    		ref: 'User'
      }
    }, {
      collection: "自定义collection名称"
    }
)

export default mongoose.model('User', UserSchema);

mongoose.model('User', new Schema(), 'eollectionName');	// 甚至可以不定义每个字段，直接用ß
```

## 数据库操作

### 查询记录

```javascript
User.find(function(err, res){
    console.log(res)
})

User.findOne({
  username: 'haofly',
  isActive: true,
  
  id: {
    $in: ["123", "321"]
  }
})
	.sort('-created_at') // 排序
	.select: ["username", "email"] // 选取指定字段
	.populate(['father'])	// 查询关联对象，相当于left join
	.populate({
  	path: 'friends',	// 获取关联对象
  	select: 'username',	// 仅获取关联对象的某个字段
  	select: ['username', 'email'],	// select多个字段
  	match: {	// 在关联对象上使用where对象，注意这里如果不匹配只是会把关联对象设置为null，而不是把父级对象设置为null，相当于这是left join中的一个额外的ON条件，而不是where条件
  		username: {
  			$regex: '.*' + keyword + '.*',	// 正则查询
        $regex: new RegExp(keyword, "i"),	// 忽略大小写查询
			}
		},
    options: {
      skip: (page -1) * limit,	// 分页
    	limit: limit,
      sort: '-created_date',	// 排序
    }
	})
  .then(user => {
  	console.log(user)
	})
  .catch((err) => {
  	console.log(err)
	})
```

### 创建记录

```javascript
var user = new User({
    name: 'haofly',
    date: new Date()
})
user.save(function(err, res){...}
```

### 更新记录

```javascript
User.findByIdAndUpdate(id, {})

User.findOneAndUpdate({
  _id: 'xxxxxxxxxxxx'
}, {
  $set: {
    'name': 'lvelvelve'
  },
  $inc: {	// 直接increment
    'count': 1
  },
  $addToSet: {	// 可以直接push进一个数组/集合
    friends: userId
  },
  $pull: {			// 从数组/集合中移出对象
    friends:: userId
  }
})
```

### 删除记录

```javascript
User.remove({_id: 'xxxxxxxxxxxx'})
```

