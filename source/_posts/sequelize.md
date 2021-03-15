---
title: "Sequelize 使用手册"
date: 2020-09-19 17:00:00
updated: 2021-02-26 15:11:11
categories: Javascript
---

[官方中文文档](https://github.com/demopark/sequelize-docs-Zh-CN)

## 常用命令CLI

```shell
npm install --save-dev sequelize-cli	# 安装命令行工具npx
```

## 数据库连接

```javascript
var sequelize = new Sequelize('database', 'username', 'password', {
  logging: false	// 默认会将sql查询都输出到console.log中，设置为false可以不用输出
})
```

## 模型定义

```javascript
const Post = sequelize.define('post', {
    id: {
      autoIncrement: true,
      primaryKey: true,
      type: INTEGER
    },
    name: {
      type: STRING,
      allowNull: false
    },
    data: {
      type: JSON
    },
    created_at: {
      type: DATE
    }
  }, {
  	timestamps: true, // 是否自动添加createdAt和updatedAt
  	tableName: 'MyPosts'	// 自定义table name
	}
);

// 定义模型关系
Post.associate = () => {
  Post.User = Post.belongsTo(app.model.Post, { foreignKey: 'post_id', as: 'Post' }),
  Post.PostOwn = User.belongsTo(app.model.Post, {'foreignKey': 'id', as: 'PostOwn'})	// 如果要与当前表自身做join等操作，那么也需要定义一个与自身的关联
}
```

## 增删改查

### 创建操作

```javascript
const user = await User.create({ firstName: "Jane", lastName: "Doe" });

// 批量创建
const captains = await Captain.bulkCreate([
  { name: 'Jack Sparrow' },
  { name: 'Davy Jones' }
]);
```

<!--more-->

### 查询操作

```javascript
const users = await User.findAll();	// 查询所有
const user = await User.findOne({	// 查询单条记录
  where: {
    id: userId
  }
})

Model.findAll({			// 查询指定字段
  attributes: ['field1', 'field2', 
               ['field3', 'new_field3'],	// 对查询出来的字段重命名
               [sequelize.fn('COUNT', sequelize.col('field4'), 'count_of_field4')], // 对查询字段做聚合操作，这里是COUNT操作
              ],
  order: [
    ['title', 'DESC'], // 排序
    sequelize.fn('max', seque)
  ],
  group: 'name',	// GROUP BY name,
  limit: 10,
  offset: 10
});

const amount = await User.count({where: [...]}) // 直接COUNT得到数字

// 查询出所有字段并且添加一个聚合字段
Model.findAll({
  attributes: {
    include: [
      [sequelize.fn('COUNT', sequelize.col('field4'), 'count_of_field4')]
    ]
  }
});

// 查询所有字段，并且去掉某些字段
Model.findAll({attributes: {exclude: ['field4']}});

// 带where的查询，
const { Op } = require('sequelize');
User.findAll({
  where: {
    name: 'abc',	// 默认是等于查询，即Op.eq
    [Op.and]: [{status:1}, {id: 11}],	// and查询
    [Op.or]: [{status:1}, {id: 11}], // or 查询,
    someAttribute: {
    	{[Op.or]: [12, 13]}, // 对一个字段单独用or查询,
      [Op.ne]: 20,	// 不等于
      [Op.is]: null,	// IS NULL
      [Op.not]: true, // IS NOT TRUE
      [Op.gt]: 6, // > 6
      [Op.gte]: 6, // >= 6
      [Op.lt]: 10, // < 10
      [Op.lte]: 10, // <=10
      [Op.between]: [6, 10], // BETWEEN 6 AND 10
      [Op.notBetween]: [11, 15], // NOT BETWEEN 11 AND 15
      [Op.in]: [1, 2], // IN [1,2]
      [1, 2, 3],	// IN的简洁写法
      [Op.notIn]: [1, 2], // NOT IN [1,2]
      [Op.like]: '%hat', // LIKE '%hat',
      [Op.notLike]: '%hat',
      [Op.startsWith]: 'hat', // LIKE 'hat%'
      [Op.endsWith]: 'hat', // LIKE '%hat'
      [Op.substring]: 'hat', // LIKE '%hat%'
      [Op.iLike]: '%hat', // ILIKE '%hat'(大小写不敏感)
      [Op.regexp]: '^[h|a|t]', // REGEXP/~ '^[h|a|t]'
      [Op.notRegexp]: '^[h|a|t]',
      [Op.iRegexp]: '',
      [Op.notIRegexp]: '',
      [Op.any]: [2, 3],	// ANY ARRAY[2, 3], // 仅Postgres
  }
});
```

#### 复杂嵌套查询语句示例

##### 关联查询

 ```javascript
return Message.findAndCountAll({
	where: {
    '$PostOwn.id$': null	// 如果是关联后的where条件需要写在这里
  },
  order: [ ['created_at', 'desc'] ],	// 排序
  include: [
    {
      association: Post.PostOwn,	// 与自身进行join操作
      on: {	// 可以自定义ON关联，如果不指定则是associate中的默认查询条件
        id: where(col('post.id'), '<', col('PostOwn.id')),
        name: where(col('post.name'), '=', col('PostOwn.PostOwn'))
      },
      attributes: ['id'],	// 取出哪些字段
      required: false	// 表示left join，如果为true那么就是inner join
    },
    {
      association: Post.Sender,
      attributes: ['id', 'type', 'email'],	// 多级关联
        include: [{
          association: User.Professional,
          attributes: ['first_name', 'last_name', 'avatar']
      }, {
            association: User.Company,
            attributes: ['name', 'logo']
      }]
    }],
    group: ['name', 'name1'], // group by 操作
    offset: 50,
    limit: 50
})

// 动态查询条件
const users = await User.findall({
  where: Object.assign({
    'firstname': 'abc'
  }, lastname ? {
    'lastname': lastname
  } : {})
})

const users = await User.findall({
  attributes: ['username'],
  where: {
    status: 1,
    [Op.or]: [
      {
        username: {
          [Op.like]: `${username}%`
        }
      },
      {
        username: username
      }
    ]
  }
})
 ```

#### 查询结果处理

- 结果如果是多条记录，那么它会是一个集合，可以执行集合相关的操作，如`map`等
- 单个的记录对象，可以执行`toJSON()`操作转换为json格式

### 更新操作

```javascript
await User.update({ lastName: "Doe" }, {
  where: {
    lastName: null
  }
});
```

### 删除操作

```javascript
await User.destroy({
  where: {
    firstName: "Jane"
  }
});

// 清空整张表
await User.destroy({
  truncate: true
});
```

## Migrate

### migrate语法

```javascript
module.exports = {
  up: (queryInterface, Sequelize) => {
    const { INTEGER, DATE } = Sequelize
    // 添加字段
    queryInterface.addColumn('another_table', 'first_name', {
    	type: String,
    	after: "user_id"	// AFTER语法
    });
    // 添加key
    queryInterface.addConstraint('table_name', ['fistname', 'lastname'], {
      type: 'unique',
      name: 'key_name_unique'
    })
    // 创建表
    return queryInterface.createTable('users', {
      id: {
        autoIncrement: true,
        primaryKey: true,
        type: INTEGER
      },
      user_id: {
        type: INTEGER
      },
      user_name: {
        type: String
      }
      created_at: DATE,
      updated_at: DATE
    }, {
      uniqueKeys: {
        user_name_unique: {
          fields: ['user_name']
        }
      }
    })
  },
  down: (queryInterface, Sequelize) => {
    queryInterface.removeColumn('table_name', 'field_name');	// 删除字段
    queryInterface.removeConstraint('table_name', 'key_name'); // 删除索引
    return queryInterface.dropTable('users');	// 删除表
  }
}
```

### seed语法

```javascript
// 批量插入
queryInterface.bulkInsert('Users', [{
  firstName: 'John',
  lastName: 'Doe',
  email: 'example@example.com',
  createdAt: new Date(),
  updatedAt: new Date()
}]);

// 批量删除
queryInterface.bulkDelete('Users', null, {});
```

### migrate/seed命令

```shell
npx sequelize-cli db:migrate	# 执行所有还未执行的migrate
npx sequelize-cli migration:generate --name add_field	# 生成迁移文件
npx sequelize db:migrate:undo --name 20200925092611-xxxxxxxxxx.js	# 回滚指定的migrate

npx sequelize-cli db:seed:all	# 执行所有未执行的seed
npx sequelize-cli seed:generate --name demo-user	# 创建一个seed文件
npx sequelize-cli db:seed:undo --seed name-of-seed-as-in-data	# 取消执行指定seed
npx sequelize-cli db:seed:undo:all # 取消执行所有seed
```



