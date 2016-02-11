---
title: "Python编码及注释规范"
date: 2015-04-03 12:38:08
categories: 编程之路
---
Python，我最喜欢的语言。但是，在其强大的功能以及强制的编码格式背后，也会引来一大波的编码方面的困扰，所以依然得需要进行一些规范化。

## 注释

函数或者文档的注释使用三引号，结尾空一行

**函数注释**需要注明三个参数：Args(参数)、Return(返回值)和Raises(抛出的错误)，例如：


    def exampleFunc(one, two):
        """
        这里是函数的功能





    Args:
        one: 参数一的注释
        two: 参数二的注释

    Return:返回值的解释，如果返回值比较复杂，比如是一个json数据，那么还需要将返回的格式卸载这儿

    Raises: 非必须
    """</pre>


** 类的注释**，依然得有一行文档字符串，若有共有属性，需要在注释处表名，例如：


    class exampleClass(基类):
        """
        类的注释





    Attributes:
        公有属性1: 解释
    """</pre>


** 文件注释：**一般包括了编码信息、版权、许可声明、模块头等信息，例如：


    # coding = utf-8




    # Copyright 2015 ........




    """
    这里是模块头，用一行文字概括文件或模块或脚本的作用
    """

## 命名



    module_name：模块
    package_name：包
    ClassName：类
    method_name：方法
    ExceptionName：错误
    function_name：函数
    GLOBAL_VAR_NAME：全局变量
    function_parameter_name：函数参数
    local_var_name：局部变量
    has_或is_：定义布尔类型元素

## 空行

两个函数的定义之间空两行，而方法或者语句模块之间则只空一行

## 空格

二元操作符之间添加空格

## 其它

对于常字符串，Python可以使用小括号将行隐式地连接在一起而不用在每行末尾加上加号，例如：



    a = (
        'wang'
        'hao'
    )
    print(a)




    # 打印出来就是wanghao
