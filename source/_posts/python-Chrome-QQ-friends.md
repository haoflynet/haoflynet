---
title: "使用Python3和Chrome获取QQ好友列表"
date: 2014-09-28 15:22:01
categories: 就是爱玩
---
最近想获得所有QQ好友的QQ帐号列表，但是腾讯居然没有提供这个功能，这让我很苦恼。由于QQ客户端上的数据我并不知道怎么获取(有人说可以提取手机QQ的数据库来
获取，但我对那个也是一无所知)，于是我想到了通过QQ空间里的某些地方来寻找。其实QQ空间的寻找好友功能里面就能够查看到很多的好友，但是却只能查看亲密度前面2
00的好友，对于我这种QQ好友比较多的人来说实在没办法。其实我对http等不大了解，最终是通过一个很笨的方法来获取的，如下：

首先，在QQ空间顶部面板处有一个搜索好友和用户的搜索框，输入一个数字即可显示以该数字为关键词的好友，最多显示5个。于是通过Chrome的**右键->审查元素
**功能获取我的请求信息：  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_0.jpg)  
随便输入一个数字，在下面的Network监听处会出现所请求的cgi脚本的信息  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_1.jpg)  
点击JS脚本，找到Preview里面有刚才显示的QQ帐号信息的那个就是它了，然后鼠标右键，copy as
cURL即可得到curl请求信息(如果在linux下直接命令行就搞定了)

注：经过研究发现，在处理_**subprocess.check_output(args)**_的返回值时，直接_**subprocess.check_out
put(args).decode('utf-8')**_，直接将含有中文的bytes转换utf编码的str，这样可以避免很多编码问题



    #-_- coding: UTF-8 -_-
    import os, sys
    import re
    import subprocess
    import shlex
    import json
    import codecs




    # 添加curl的环境变量




    os.putenv('PATH', 'C:\\Program Files (x86)\\Git\\bin')




    # 分解原始请求




    origin = ''        # 这里粘贴从浏览器copy过来的cURL请求
    temp = origin.split('&search=1')
    temp[0] += '&search='




    # 结果集合




    qqlist = set()




    # 查找并移去含有中文的字段




    # 应该默认遇到逗号结束，如果遇到的是大括号，那么就相当于在最后




    def remove(convert, char):
        while(convert.find(char) > 0):
            pre = convert.find(char)    # pre 表示前面的位置
            now = pre + 1
            while(True):
                if(convert[now] == '\}' and convert[now+1] == ',' and convert[now+2] == '\{'):
                    break
                # \}]
                elif(convert[now] == '\}' and convert[now+1] == ']'):
                    break
                elif(convert[now] == ',' and convert[now+1] == '"'):
                    break
                else:
                    now += 1
            if(convert[now] == ','):
                if(convert[now+1] == '"' and convert[now+2] == ','):
                    now += 3
                else:
                    now += 1
            else:
                pre -= 1
            leave = convert[: pre]
            leave += convert[now :]
            convert = leave
        return convert




    def search(pre):
        for i in range(10):





            curl = temp[0] + pre + str(i) + temp[1]
            print('当前' + pre + str(i))

            # 执行curl命令并获取返回结果，并对结果字符串进行处理转换为json对象
            args = shlex.split(curl)
            result = str(subprocess.check_output(args)).replace(' ', '')
            convert = result.replace(' ', '').split('callback(')[1].split(');')[0]

            # 这一句话可以减少很多时间
            if(convert.find('100006') &lt; 0):
                continue

            # 我郁闷，我要直接把那几个字段给删除，这些人起昵称太奇葩了
            convert = remove(convert, '"CA"')
            convert = remove(convert, '"TA"')
            convert = remove(convert, '"CB"')
            convert = remove(convert, '"TB"')
            convert = remove(convert, '"hitFieldContent"')
            convert = remove(convert, '"TF"')           
            output = json.loads(convert)

            """
            如果想获取其中的中文信息，可以改变一下其编码的字符
            regex = re.compile(r'\\\\(?![/u"])')
            fixed = regex.sub(r"\\\\\\\\", convert)
            """

            if('data' not in output):
                continue
            for sub in output['data']:
                if(sub['llBoxType'] == 100006):
                    for one in sub['sData']['resultData']:
                        if(one['intimacy'] == '0'):
                            continue
                        qqlist.add(one['NM'])
                    if(len(sub['sData']['resultData']) == 5):
                        search(pre + str(i))


for i in range(10, 100): search(str(i))

# 输出最终结果

fp = codecs.open('1129029735.txt', 'a', 'utf-8') fp.write('总共搜索到' +
str(len(qqlist)) + '个QQ\\n') result = [qq + '\\n' for qq in sorted(qqlist)]
fp.writelines(result) fp.close()

由于前面两位QQ号基本上都可以搜索到大于5位的好友，所以，我从100到999逐个开始搜索，如果发现小于5个就进入下一个，如果等于5个，那就递归。这个请求所返
回的不是标准的JSON数据，总是有这样或者那样的干扰，看我的remove函数你们就可以发现其中出现的诸多问题，其实我最先还想把QQ昵称一起提取出来的，后来发
现QQ昵称里面的奇葩字符太多了，真不知道腾讯的人是怎么处理的，还是我对中文字符处理技术比较薄弱。最终，搜索我QQ上400多个好友花费时间约为9分钟(忘了统计
请求数量了，应该只有1000多次的请求)：  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_2.jpg)[  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_3.jpg)  
](http://haofly.net/wp-content/uploads/2014/09/qqlist3.jpg)
