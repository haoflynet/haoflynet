---
title: 如何发布一个package到PyPI
date: 2017-12-20 18:36:13
tags: python
---

最近，发布了一个Python包`pygui-macro`到PyPI上面，发布的步骤还是比较简单，但是网上的教程都有点儿复杂且过时了。这里简单记录一下:

<!--more-->

#### 注册一个PyPI帐号

虽然现在PyPI有意从`https://pypi.python.org`切换到`https://pypi.org/`，但是目前位置两者帐号是通用的，在两个网站上面，都可以进行注册与管理，当然，`pypi.org`在UI上就显得比较现代化了。

#### 更改项目目录结构

将项目源代码放到次级目录，方便包整体的管理。

```shell
.
├── LICENSE
├── README.md
├── pygui_macro
│   ├── __init__.py
│   ├── callbacks.py
│   ├── controller.py
│   ├── listener.py
│   ├── pygui_macro.py
│   ├── recoder.py
│   └── runner.py
├── setup.cfg
├── setup.py
└── tests
```

#### 添加配置文件

##### setup.cfg

内容可以就这么简单，将根目录下的`README.md`作为包的描述文件

```tex
[metadata]
description-file = README.md
```

##### setup.py

主要工作是这个文件夹里面的`setup`函数。

```python
import platform

from setuptools import setup, find_packages

VERSION = '0.1.2'

requires = ['six', 'pynput']

system = platform.system()
if system == 'Darwin':
    requires.append('pyobjc-framework-Quartz')

setup(
    name='pygui-macro',		# 指定包名
    version=VERSION,		# 指定版本号
    description='Cross-platform gui macro command tool with python, automate your keyboard and mouse.',			# 一句话描述，
    long_description='Cross-platform gui macro command tool with python, automate your keyboard and mouse. You can use it to record keyboard and mouse action, and rerun it as a script.',					# 详细介绍
    keywords='gui macro automate keyboard mouse',	# 关键字
    author='haoflynet',		# 作者
    author_email='haoflynet@gmail.com',
    maintainer='haoflynet',
    maintainer_email='haoflynet@gmail.com',
    url='https://github.com/haoflynet/pygui-macro',	# 项目目录
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=requires,		# 上层依赖的包
    entry_points={
        'console_scripts': [
            'pygui-macro=pygui_macro.pygui_macro:main'		# 我这里是一个命令行工具，所以需要这样写，pygui-macro是命令，后面的是指某个函数
        ]
    }
)
```

##### .pypirc

该文件位于用户目录`~/`下面，在这里添加你的帐号信息。

```tex
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username=haoflynet
password=password

[pypitest]
username=haoflynet
password=password
```

#### 打包上传

```shell
# 首先安装上传工具
pip3 install -U pip setuptools twine

# 打包
python3 setup.py sdist	# 会将项目打包到当前目录下面并生成相应的egg

# 上传
twine upload dist/*		# 其实就是上传的dist目录下的zip包
```

#### 以上

![](http://ojccjqhmb.bkt.clouddn.com/pypi.png)