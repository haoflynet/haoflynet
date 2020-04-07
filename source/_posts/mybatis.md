---
title: "MyBatis 手册"
date: 2020-04-06 18:00:00
categories: java
---

## 目录结构

- `Mapper.xml`文件是真实的SQL语句对应关系

`MyBatis`生成的`DAO`层文件目录如下:

```shell
.
├── entity
│   ├── Table1.java	# 这是数据Model，即使数据记录对应的Java类，里面包含对应表的字段、注释及get和set方法
│   ├── Table1Example.java	# MySQL查询相关的一些简单的语句拼接，针对每个字段都有几个常用的SQL语句拼接方法。比如等于、大于、小于等方法
│   ├── Table2.java
│   └──  Table2Example.java
└── mapper
    ├── Table1Mapper.java
    ├── Table1Mapper.xml
    ├── Table2Mapper.java
    ├── Table2Mapper.xml
    └── ext		# MyBatis并不会默认生成，可以在这里编写自定义的查询方法
        ├── MyExtMapper.java
        └── MyExtMapper.xml
```

<!--more-->

## 常用查询方法

- 如果数据库表中有`TEXT/BLOB`类型的字段，那么在获取列表的时候(`selectByExample`)默认不会返回这些字段，需要用名称中含有`BLOB`的方法才能获取到

`Mybatis`默认会生成如下几个常用的查询方法

```java
public interface Table1Mapper {
  	// COUNT查询
    int countByExample(Table1Example example);
		// 通过条件删除，返回删除的行数
    int deleteByExample(Table1Example example);
		// 通过主键删除
    int deleteByPrimaryKey(Integer id);
		// 插入新的完整的记录
    int insert(Table1 record);
		// 插入新的记录，仅部分字段
    int insertSelective(Table1 record);
		// 通过条件查找，返回list
    List<Table1> selectByExample(Table1Example example);
		// 通过主键查找一条记录
    Table1 selectByPrimaryKey(Integer id);
		// 更新记录的部分字段，返回更新的行数
    int updateByExampleSelective(@Param("record") Table1 record, @Param("example") Table1Example example);
		// 更新记录的所有字段，返回更新的行数
    int updateByExample(@Param("record") Table1 record, @Param("example") Table1Example example);
		// 通过主键更新部分字段
    int updateByPrimaryKeySelective(Table1 record);
		// 通过主键更新所有字段
    int updateByPrimaryKey(Table1 record);
  
  	// 当表中有text或blob字段的时候有如下几种单独的方法
  	List<Table1> selectByExampleWithBLOBs(Table1Example example);
  	int updateByExampleWithBLOBs(@Param("record") Table1 record, @Param("example") Table1Example example);
    int updateByPrimaryKeyWithBLOBs(ClCouponLog record);
}
```

## 复杂查询方法

- 复杂的查询方法有可能需要自己写SQL，`MyBatis`默认的SQL(xml文件里面的)其实非常少，完全比不上动态语言的ORM

### 编写自定义的查询方法

- 为了避免每次`MyBatis`执行后都覆盖自己添加的自定义方法，所以最好将自定义查询方法写在`mapper/ext`文件夹中，但是这样做有个缺点就是字段如果有修改得改一下其对应的`xml`文件以防止使用这里面的方法时字段缺失
- 首先编写XML文件，例如`MyExtMapper.xml`，该文件可以将之前该表对应的XML文件复制过来，删除掉原来XML中已经存在的方法定义，可以直接根据id判断，例如`<select id="selectByExample"...>`就是`selectByExample`方法的定义。删除完成后按照之前的语法定义自己的查询方法即可，然后把id拿到再建一个同名的接口文件`MyExtMapper.java`即可。例如一个自定义的统计接口，可以这样写:

```java
// 需要注意MyExtMappper.xml还需要将MyExtMapper的namepsace设置进到mapper的namespace属性里面去

// MyExtMapper.xml，这里仅仅写出需要添加的标签
<resultMap id="BaseResultMap" type="com.haofly.net.dao.entity.Table1">
  <id column="id" property="id" jdbcType="BIGINT"/>
  <result column="name" property="recordType" jdbcType="VARCHAR"/>
  <result column="value" property="recordType" jdbcType="VARCHAR" />
</resultMap>
<select id="countByMyCondition" parameterType="com.haofly.net.dao.entity.Table1Example" resultMap="BaseResultMap"> // 这里的resultMap时上面定义的返回结构，如果是整形这种可以直接写成resultType="java.lang.Integer"
    SELECT
  			id, name, value
  	FROM 
  		table1
    <if test="_parameter != null">	// 这里表示如果没有其它的条件就直接用Example里面的条件，类似于selectByExample
        <include refid="Example_Where_Clause_Ext"/>
    </if>
</select>
  
// MyExtMapper.java中这样定义该方法
List<Table1> countByMyCondition(Table1Example example);
```

### 复杂OR查询

```java
// 不支持a=? AND (b=? OR c=?)的语法，但是支持(a=? AND b=?) OR (a=? AND c=?)，例如
Table1Example example = new Table1Example();
Table1Example.Criteria[] criteria = new Table1Example.Criteria[2];
criteria[0] = example.createCriteria().andField1EqualTo("A").andField2EqualTo("B");
criteria[1] = example.createCriteria().andField1EqualTo("C").andField2EqualTo("D");
example.or(criteria[0]);
example.or(criteria[1]);
List<Table1> table1List = table1Mapper.selectByExample(example);

// 直接a=? OR b=?
example.or().andField1EqualTo("A")
example.or().andField2EqualTo("B");
```

