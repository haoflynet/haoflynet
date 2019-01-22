---
title: "MyBatis 手册"
date: 2019-01-05 10:00:00
categories: java
---

int countByExample(UserExample example) thorws SQLException	按条件计数
int deleteByPrimaryKey(Integer id) thorws SQLException	按主键删除
int deleteByExample(UserExample example) thorws SQLException	按条件查询
String/Integer insert(User record) thorws SQLException	插入数据（返回值为ID）
User selectByPrimaryKey(Integer id) thorws SQLException	按主键查询
ListselectByExample(UserExample example) thorws SQLException	按条件查询
ListselectByExampleWithBLOGs(UserExample example) thorws SQLException	按条件查询（包括BLOB字段）。只有当数据表中的字段类型有为二进制的才会产生。
int updateByPrimaryKey(User record) thorws SQLException	按主键更新
int updateByPrimaryKeySelective(User record) thorws SQLException	按主键更新值不为null的字段
int updateByExample(User record, UserExample example) thorws SQLException	按条件更新
int updateByExampleSelective(User record, UserExample example) thorws SQLException	按条件更新值不为null的字段
--------------------- 
作者：biandous 
来源：CSDN 
原文：https://blog.csdn.net/biandous/article/details/65630783 
版权声明：本文为博主原创文章，转载请附上博文链接！











insert，返回值是：新插入行的主键（primary key）；需要包含<selectKey>语句，才会返回主键，否则返回值为null。

update/delete，返回值是：更新或删除的行数；无需指明resultClass；但如果有约束异常而删除失败，只能去捕捉异常。



