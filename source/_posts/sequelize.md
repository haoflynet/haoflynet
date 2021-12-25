---
title: "Sequelize 使用手册"
date: 2020-09-19 17:00:00
updated: 2021-12-23 08:11:11
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
  dialect: 'mysql',	// 如果不指定这个参数，可能会报错Dialect needs to be explicitly supplied as of v4.0.0
  logging: false	// 默认会将sql查询都输出到console.log中，设置为false可以不用输出
})

// 直接执行SQL row命令
const records = await sequelize.query("SELECT * FROM `users`", { type: QueryTypes.SELECT });
```

## 模型定义

- 数据类型包括：
  - 字符串：STRING、STRING(1024)、STRING.BINARY、TEXT、TEXT('tiny')、CITEXT(仅PostgreSQL和SQLite)、TSVECTOR(仅PostgreSQL)
  - 布尔：BOOLEAN
  - 数字：INTEGER、INTEGER.UNSIGNED、INTEGER.ZEROFILL、INTEGER.UNSIGNED.ZEROFILL、BIGING、BIGING(11)、FLOAT、FLOAT(11)、FLOAT(11, 10)、REAL(仅PostgreSQL)、REAL(11)(PostgreSQL)、REAL(11, 10)(仅PostgreSQL)、DOUBLE、DOUBLE(11)、DOUBLE(11, 10)、DECIMAL、DECIMAL(10, 2)
  - 日期：DATE、DATE(6)(仅MySQL)、DATEONLY
  - UUID：可以自动为字段生成UUID，type为`UUID`，defaultValue为`UUIDV1`或者`UUIDV4`

```javascript
// 定义方式零，纯typescript的方式可以使用https://github.com/RobinBuschmann/sequelize-typescript

// 定义方式一，typescript方式
class PostModel extends Model {
  // 定义一些值可以让其增加typescript声明
  public id: number
  public name: string
  
  // 为typescript增加获取关联对象的方法声明
  public getUser! BelongsToGetAssociationMixin<BandModel>
  
  static initModel (sequelize: Sequelize): void {
    id: {
      autoIncrement: true,
      primaryKey: true,
      type: INTEGER
    },
    name: {
      type: STRING,
      allowNull: false,
      defaultValue: 'test',
      validate: {	// 数据校验
        is: /^[a-z]+$/i,	// 满足某个正则
        is: ["^[a-z]+$",'i'],	// 同上，只是正则用数组来写
        not: /^[a-z]+$/i,
        not: ["^[a-z]+$",'i'],
        isEmail: true,
        isUrl: true,
        isIP: true,
        isIPv4: true,
        isIPv6: true,
        isAlpha: true,
        isAlphanumeric: true,
        isNumeric: true,
        isInt: true,
        isFloat: true,
        isDecimal: true,
        isLowercase: true,
        isUppercase: true,
        notNull: true,
        isNull: true,	// 只允许null
        notEmpty: true,	// 不能是空字符串
        equals: 'specific value',
        contains: 'foo',
        notIn: [['foo', 'bar']],
        isIn: [['foo', 'bar']],
        notContains: 'bar',
        len: [2,10],
        isUUID: 4,
        isDate: true,
        isAfter: "2011-11-05",
        isBefore: "2011-11-05",
        max: 23,
        min: 23,
        isCreditCard: true,	// 是否是信用卡数字
        isEven(value) {	// 自定义校验
          if (parseInt(value) % 2 !== 0) {
            throw new Error('Only even values are allowed!');
          }
        }
      },
      isIn: {
        args: [['en', 'zh']],
        msg: "Must be English or Chinese"	// 上面的校验方式都能够自定义，但是min和max不知道为啥不行，如果是min或者max就改成用len吧
      }
    }
  }

 	static relate (): void {
    PostModel.belongsTo(UserModel, {
    	as: 'user',
      foreignKey: 'user_id'
  	})
  }
  
}

// 定义方式二
const Post = sequelize.define('post', {
    id: {
      autoIncrement: true,
      primaryKey: true,
      type: INTEGER
    },
    name: {
      type: STRING,
      allowNull: false,
      defaultValue: 'test'
    },
    firstName: {
      type: STRING,
      field: 'first_name'	// 自定义列名称,
      comment: '列注释' // 注释仅针对MySQL、MariaDB、PostgreSQL、MSSQL
    },
  	fullName: {
      type: VIRTUAL,	// 定义virtual字段，即实际不存在数据库中的字段
      get: function (this: UserModel) {
        return this.firstName + this.name
      },
      set: function (val) {
       	this.setDataValue('name', val)
      }
    },
    date: {
      type: DATE,
      defaultValue: NOW
    },
    // unique参数的值可以是不二值或者字符串，如果多格列具有相同的字符串unique，他们会组成一个复合唯一键
    uniqueOne: { type: DataTypes.STRING,  unique: 'compositeIndex' },
    uniqueTwo: { type: DataTypes.INTEGER, unique: 'compositeIndex' },

    data: {
      type: JSON
    },
    created_at: {
      type: DATE
    }
  }, {
    indexes: [{ unique: true, fields: ['field1']}], // 也可以在最后创建索引
  	timestamps: true, // 是否自动添加createdAt和updatedAt
  	tableName: 'MyPosts'	// 自定义table name，如果不提供，sequelize会根据模型名称自动以复数形式设置表名
    paranoid: true,	// 定义该表为偏执表，即自带软删除，使用destroy能自动软删除
    deletedAt: 'mydelete', // 偏执表软删除字段默认为deletedAt，这里可以指定自定义的字段名
  	validate: {	// 基于model的校验，可以同时校验多个字段
			bothCoordsOrNone() {
        if ((this.latitude === null) !== (this.longitude === null)) {
          throw new Error('Either both latitude and longitude, or neither!');
        }
      }
		}
	}
);

// 定义模型关系
Post.associate = () => {
	Post.User = Post.belongsTo(app.model.Post)
}

User.associate = () => {
  User.hasMany(Post)
}
  
// 定义模型类方法
Post.customQuery = () => {}

// 定义模型实例方法
Post.prototype.customQuery = () => {}
```

### 关联关系定义

- `sequelize`默认会给关联关系添加对应的读取方法，例如如果和user关联，那么会有`getUser`方法，而如果是一对多，或者多对多，那么会有`getUsers`方法，但是如果是`typescript`，就需要我们先将该方法声明一下

  ```javascript
  public getUsers: BelongsToManyGetAssociationsMixin<UserModel>
  ```

### One to One一对一

```javascript
Post.User = Post.belongsTo(app.model.Post, { foreignKey: 'post_id', as: 'Post' }),
Post.PostOwn = User.belongsTo(app.model.Post, {'foreignKey': 'id', as: 'PostOwn'})	// 如果要与当前表自身做join等操作，那么也需要定义一个与自身的关联
PostModel.belongsTo(UserModel)

// hasOne自动添加的方法
fooInstance.getBar()
fooInstance.setBar()
fooInstance.createBar()
```

### One to Many 一对多

```java
const Foo = sequelize.define('foo', { name: DataTypes.STRING });
const Bar = sequelize.define('bar', { status: DataTypes.STRING });
Foo.hasMany(Bar, {
  scope: {	// 可以通过scope限制某个关联表的字段
    status: 'open'
  },
  as: 'openBars'
});

// hasMany自动添加的方法
fooInstance.getBars()
fooInstance.countBars()
fooInstance.hasBar()
fooInstance.hasBars()
fooInstance.setBars()
fooInstance.addBar()
fooInstance.addBars()
fooInstance.removeBar()
fooInstance.removeBars()
fooInstance.createBar()
  
// belongsToMany自动添加的方法
fooInstance.getBars()
fooInstance.countBars()
fooInstance.hasBar()
fooInstance.hasBars()
fooInstance.setBars()
fooInstance.addBar()
fooInstance.addBars()
fooInstance.removeBar()
fooInstance.removeBars()
fooInstance.createBar()
```

### Many to Many 多对多

##### 多态多对多

- 有中间表，且使用`target_id`和`target_type`来表示关联的表的类型
- 除了我下面这个例子，还可以参考[Sequelize中文文档](https://www.sequelize.com.cn/advanced-association-concepts/polymorphic-associations#%E9%85%8D%E7%BD%AE%E5%A4%9A%E5%AF%B9%E5%A4%9A%E5%A4%9A%E6%80%81%E5%85%B3%E8%81%94)

```javascript
// 例如一个用户有多篇文章，多辆车，一篇文章或者一辆车也能同时属于多个用户，那么就有这么几张表: Car, Post, User, UserThings关联表
CarModel.belongsToMany(UserModel, {
  through: {
    model: UserThingModel,	// 中间表
    unique: false,	// 如果unique为true，那么表示只有一个
    scope: {
      targetType: 'car',	// 当关联的是car时，其`target_type`字段为car
    },
    foreighKey: 'target_id',
    constraints: false
  }
})

PostModel.belongsToMany(UserModel, {
  through: {
    model: UserThingModel,	// 中间表
    unique: false,	// 如果unique为true，那么表示只有一个
    scope: {
      targetType: 'post',	// 当关联的是post时，其`target_type`字段为post
    },
    foreighKey: 'target_id',
    constraints: false
  }
})
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

await User.findOrCreate({
  where:{},	// 比较的字段
  defaults: {}	// 填入的字段
})
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
    ['name', 'ASC'],
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

#### 关联查询

- 如果怎么加条件都不能出现在正确的地方，可以尝试给查询加上`subQuery: false`选项试试，这样不仅`sql`能大量简化，可能也能得到正确的结果

 ```javascript
return Message.findAndCountAll({
	where: {
    '$PostOwn.id$': null	// 如果是关联后的where条件需要写在这里，如果有Unknown column错误，首先检查一下是否正确，不行的话加上subQuery: false选项试试
  },
  order: [ ['created_at', 'desc'] ],	// 排序
  attributes: {
    include: [
      [sequelize.fn('COUNT', sequelize.col('posts.id')), 'postsCount']]	// 统计关联表的数据as 一个指定的名称 
    ]
  },
  include: [
    'user',	// 如果没有其他的条件，可以直接这样做
    {
      association: Post.PostOwn,	// 与自身进行join操作
      on: {	// 可以自定义ON关联，如果不指定则是associate中的默认查询条件
        id: where(col('post.id'), '<', col('PostOwn.id')),
        name: where(col('post.name'), '=', col('PostOwn.PostOwn'))
      },
      attributes: ['id'],	// 取出哪些字段
      required: false,	// 表示left join，如果为true那么就是inner join
      where: {status: 1},	// include的where操作，相当于left join的where，hasMany的where
    },
    {
      association: Post.Sender,
      attributes: ['id', 'type', 'email'],	// 多级关联
        include: [{
          association: User.Professional,
          attributes: ['first_name', 'last_name', 'avatar'],
          where: {	// 嵌套关联查询，如果有针对子孙的where条件，可以用literal来写，我也没找到其他写法
            [Op.and]: [
              sequelize.literal('"post->user"."id" = "user"."id"')
            ]
          }
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
// 查找或更新，注意这里不是findOne，也没有findOneOrCreate，所以返回值是一个列表
await User.findOrCreate({
  where:{},	// 比较的字段
  defaults: {}	// 填入的字段
})

await User.update({ lastName: "Doe" }, {
  where: {
    lastName: null
  }
});

await User.update({
  age: sequelize.literal('age + 1')	// 实现字段的+1操作
}, {
  where: {id}
})
```

### 删除操作

```javascript
await User.destroy({
  where: {
    firstName: "Jane"
  },
  force: true,	// 如果模型是偏执表，如果想要硬删除需要加上force参数
});

// 清空整张表
await User.destroy({
  truncate: true
});
```

## Migrate

- **生成数据库千万不要用sync方法，官方都不建议将该方法用于生产环境，因为要改之前的数据表，它只能删除后再重建，非常危险的操作，而且现在没有一个很好的工具从models生成migrations(每个工具都不好用)，所以最好一开始就别用该方法。如果用了该也不是很难，把model复制过来，加上createdAt,updatedAt,deletedAt等然后表名换另一个，生成后对比一下就行了，一张表大概5分钟**

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
    // 改变字段
    queryInterface.changeColumn('表名', '字段名', {
      type: String,
      allowNull: false
    })
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
        type: String	// STRING类型默认长度是255
      }
      created_at: {
        type: DATE,	// DATE就是DATETIME，没有DATETIME类型
      	allowNull: false,
        defaultValue: literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        type: DATE,
        allowNull: false,
        defaultValue: literal('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
      }
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

## TroubleShooting
- **Cannot read property 'length' of undefined /  Cannot convert undefined or null to object**: 可能是因为没有执行`Model.init`方法将model初始化
- **is not associated to**: 可能是没有定义模型间的关联关系，后者没有初始化关联关系
- **任何数据库操作都无响应/migrations没有执行并且都没有报错**: 可能是因为安装依赖的时候和当前使用的node版本不一致，也有可能是postgres依赖版本低造成的，可以尝试执行`npm install --save pg@latest`试试
- **include关联关系时报错xxxx must appear in GROUP BY clause**: 
  - 如果是mysql8，可能需要修改`only_full_group_by`，
  - 如果是postgres我目前只能将那个字段加入group by里面，不过还好是id字段
  - 如果是postgres且只是单纯地想把关联的对象全部取出来(例如`hasMany`关系)，如果只是单纯地把关联对象的id加入`group`，那么得到的结果是没有聚合的，而是一条关联对象一个结果，例如user has many posts，如果有两个用户，每个用户2篇文章，那么查询出来是4条数据，这时候可以把`constraints`添加到include参数中，就可以user.posts来获取了，结果是2条数据
- **ERROR: Please install mysql2 package manully**: 安装就行: `npm install --save mysql2`