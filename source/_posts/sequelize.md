---
title: "Sequelize 使用手册"
date: 2020-09-19 17:00:00
categories: Javascript
---

[官方中文文档](https://github.com/demopark/sequelize-docs-Zh-CN)

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
})
```

#### 复杂嵌套查询语句示例

 ```javascript
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



