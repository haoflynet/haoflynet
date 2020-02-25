---
title: "使用Virtualenv搭建Python3的Django环境"
date: 2015-01-24 23:05:39
updated: 2017-06-18 09:21:21
categories: 编程之路
---
Virtualenv可用于创建独立的Python环境，在这些环境里面可以选择不同的Python版本或者不同的Packages，并且可以在没有root权限的情况下在环境里安装新套件，互相不会产生任何的影响。  

以下就是使用Virtualenv搭建`Python3.4+Django1.7.4`的过程：

## 准备工作

安装Virtualenv和Python3(因为有些Linux发行版默认没有安装Python3的)

```shell
sudo pip install virtualenv
sudo apt-get install python3
```

## 建立一个新的工作环境

```shell
virtualenv --no-site-packages --python=python3.4 test_env
# 如果出现The executable python does not exist 错误，那么可以这样使用
virtualenv --no-site-packages --python=3.4 test_env
```


其中，`--no-site-packages`表示不包括系统全局的Python安装包，这样会更令环境更干净`--python=python3.4`指定Python的版本未系统已经安装了的Python3.4 test_env是建立的环境的名称

## 进入环境测试并安装Django

使用`source test_env/bin/activate`命令进入开发环境，然后查看Python版本，再使用`pip install django`安装django


```shell
➜  virtualenv  ls
test_env
➜  virtualenv  source test_env/bin/activate  # 如果是windows则是source test_env/Script/activate
(test_env)➜  virtualenv  python
Python 3.4.0 (default, Apr 11 2014, 13:05:11)
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named 'django'
>>> exit()
(test_env)➜  virtualenv  pip install django
Collecting django
  Using cached Django-1.7.3-py2.py3-none-any.whl
Installing collected packages: django
Successfully installed django-1.7.3
(test_env)➜  virtualenv  python
Python 3.4.0 (default, Apr 11 2014, 13:05:11)
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
```


`import django`没有发生错误，证明已经成功安装Django了

## 开始第一个Django app

```shell
(test_env)➜  virtualenv  django-admin startproject mysite
(test_env)➜  virtualenv  ls
mysite  test_env
(test_env)➜  virtualenv  cd mysite     

(test_env)➜  mysite  python manage.py runserver
Performing system checks...
System check identified no issues (0 silenced).
You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.
January 24, 2015 - 14:52:09
Django version 1.7.3, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[24/Jan/2015 14:52:17] "GET / HTTP/1.1" 200 1759
```


需要注意的是，新建的项目的文件夹mysite并不是仅仅存在在那个虚拟环境里，而是在实际的文件中，只是运行它使用的是虚拟的环境而已，不信呆会儿退出该虚拟环境后，你可以用实体环境在该目录下测试。

现在就可以直接访问`http://127.0.0.1:8000`，不需要端口映射，可直接访问：

![](https://haofly.net/uploads/virtualenv-python-django_0.jpg) 

## 退出虚拟环境

最后退出，直接在该环境中使用`deactivate`命令即可退出
