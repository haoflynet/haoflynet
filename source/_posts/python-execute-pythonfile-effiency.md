---
title: "在Python3代码里执行另一个python文件的几种访问及其效率的比较"
date: 2014-10-29 18:27:38
categories: 编程之路
---
最近做一个项目，需要从一个Python文件里执行其他的Python文件，因为数量可能有点大，所以考虑了一下性能的问题，就去简单地测试了一下其效率，结果如下：

首先，我的`另一个Python文件test1.py`里内容如下，执行一条command命令



    import os
    os.putenv('PATH', 'C:\\Program Files (x86)\\Git\\bin')    # 我的ls命令在git下面
    os.system('ls -ls')

# 1.使用exec函数

在Python3中无法直接使用execfile()函数，execfile被分解为了open()和exec()，[详见文档](https://docs.pyt
hon.org/3/library/functions.html#exec)，必须先将文件打开，再把文件浏览当作参数传入exec函数中去。代码如下：



    import os




    for time in range(0, 1000):
            fp = open('test1.py')
            exec(fp.read(), None, None)
            #os.popen('ls -l')

执行一千次该文件，结果如下：内存几乎无变化，CPU使用率62\%左右，耗时86.3s  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-execute-pythonfile-
effiency.png)

# 2.使用os.popen()函数

os模块的popen()函数是相当于执行的是一条command命令，并可以通过read()方法获取命令的输出，代码如下：



    import os




    for time in range(0, 1000):
            fp = open('test1.py')
            #exec(fp.read(), None, None)
            os.popen('ls -l')

执行一千次该循环，结果如下：内存几乎无变化，CPU使用率90\%左右，耗时118.1s

# ![](http://7xnc86.com1.z0.glb.clouddn.com/python-execute-pythonfile-
effiency_1.png)  

# 3.结果

从上面很明显的就能发现，使用Python3里面的exec不仅占用CPU率较低，并且执行时间也较快，而在占用内存方面两者几乎都一样。所以，还是使用exec吧。

# 4.扩展

顺便测试了一下使用os.system()函数和os.popen()函数的区别，当然这里的测试是在单个文件里执行一千次该命令，如下：



    import os




    os.putenv('PATH', 'C:\\Program Files (x86)\\Git\\bin')    # 我的ls命令在git下面




    for time in range(0, 1000):
            os.system('ls -l')
        # os.popen('ls -l')


os.system()的结果：CPU占用65\%左右，内存几乎不变，耗时83.5s  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-execute-pythonfile-
effiency_2.png)  
os.popen()的结果：CPU占用90\%左右，内存几乎不变，耗时38.4s  

![](http://7xnc86.com1.z0.glb.clouddn.com/python-execute-pythonfile-
effiency_3.png)  
