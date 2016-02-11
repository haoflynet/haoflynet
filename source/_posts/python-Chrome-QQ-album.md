---
title: "使用Python和Chrome下载所有QQ好友相册"
date: 2014-10-08 08:23:13
categories: 就是爱玩
---
上一次用cURL获取了QQ的好友列表，跳过了验证过程，感觉特别爽，所以趁热打铁，直接又写了个获取所有QQ好友相册的代码。

环境：Python3 + Chrome + Windows7

首先得要获取到所有QQ好友的QQ号码，直接参考[《使用Python3和Chrome获取QQ好友列表》](http://haofly.net/qqlist/
"Link: http://haofly.net/qqlist/" )，当然，如果你想要指定的号码，那么直接在**_qqlist.txt_**里写上其QQ号
码即可(不过获取之后是不用处理末尾的'\\n'的，因为我当时写入的时候加入了)。

然后，和那篇文章一样，获取cURL。  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_0.png)  
首先在任意一个_**user.qzone.qq.com/QQ号码/4**_页面刷新，在审查里面的Network获取_fcg_list_album_的cURL
，然后，再随便点进一个相册获取_cgi_list_photo_的cURL，其中一个是获取相册列表的，一个是获取某相册下照片列表的。

然后将两个字符串分别替换代码16/17行的get_album和get_photo



    #-_- coding: UTF-8 -_-
    import os, sys
    import re
    import subprocess
    import shlex
    import urllib.request
    import json
    import codecs
    import datetime




    # 我最先是把get_album和get_photo的值存储在request_curl.py文件里面的




    # from request_curl import *




    # 添加curl的环境变量




    os.putenv('PATH', 'C:\\Program Files (x86)\\Git\\bin')




    # 获取原始curl请求




    origin_album = get_album
    origin_photo = get_photo




    # 获取目标QQ




    fp = open('qqlist.txt', 'r')
    qqlist = fp.readlines()
    for i in range(len(qqlist)):
        qqlist[i] = qqlist[i][:-1]
    fp.close()




    for target in qqlist:
            log = \{\}                    # 下载日志
            log['qq'] = target          # QQ号
            log['access'] = 1           # 是否允许访问
            log['time'] = datetime.datetime.now()   # 下载完成后记录花费的时间
            log['album_count'] = 0      # 相册总数
            log['photo_count'] = 0      # 照片总数





        print('当前QQ：' + target)
        try:
            os.makedirs('photos/' + target)                                             # 建立相应的文件夹
        except:
            os.removedirs('photos/' + target)
            os.makedirs('photos/' + target)
        # 先得到正确的curl，然后执行获取json数据
        curl = origin_album.replace('&amp;hostUin=1129029735', '&amp;hostUin=' + target)    # 被访问者
        curl = curl.replace('&amp;pageNumModeSort=40', '&amp;pageNumModeSort=100')          # 显示相册数量
        args = shlex.split(curl)
        result = subprocess.check_output(args).decode('utf-8')
        convert = result[result.find('(') + 1 : result.find(')', -1) -1]            # 去除不标准的json数据
        output = json.loads(convert)                                                # 最终json数据
        if(output['code'] == -4009):
            log['access'] = 0           # 是否允许访问
            fp = open('photos/' + target + '/log.txt', 'w', encoding='utf-8')       # 日志文件，记录时间与数量
            fp.writelines(str(log))
            fp.close()
            continue

        # output['data']['albumListModeSort']就是相册列表
        # 艹，也有可能output['data']['albumListModeClass'][0]['albumList']是相册列表
        # 最后才发现，output['data']['albumListModeClass']也有可能是相册列表
        try:
            if(output['data']['albumListModeSort'] == None):
                albumList = None
            else:
                albumList = output['data']['albumListModeSort']
        except:
            if(output['data']['albumListModeClass'] == None):
                albumList = None
            else:
                albumList = output['data']['albumListModeClass'][0]['albumList']

        # 我服都服了，这么大个人了，居然还有没有相册的
        if(albumList == None):
            continue

        theSameAlbumName = 0    # 防止同名相册的出现
        print(albumList)
        for album in albumList:
            log['album_count'] += 1
            print('当前相册：' + album['name'])
            if(album['allowAccess'] == 0):                  # 相册无法直接访问(需要密码或者禁止访问)
                continue

            # album['id']就是照片列表的ID
            # 获取照片列表数据
            curl = origin_photo.replace('&amp;hostUin=1129029735', '&amp;hostUin=' + target)
            curl = curl.replace('&amp;topicId=V10HYl1S33NLS5', '&amp;topicId=' + album['id'])
            curl = curl.replace('&amp;pageNum=30', '&amp;pageNum=600')  # QQ空间每个相册最大貌似不会超过512
            args = shlex.split(curl)
            result = subprocess.check_output(args).decode('utf-8')
            convert = result[result.find('(') + 1 : result.find(')', -1) -1]
            output = json.loads(convert)

            if(output['code'] == -4404):
                continue

            # 相册名里面会不会也有奇葩名字呢
            filt = re.compile(r'\\\\|/|:|\\*|\\?|&lt;|&gt;|\\||\\.')
            album['name'] = re.sub(filt, '', album['name'])
            # 我服都服了，QQ空间居然还允许同名的相册。。。
            albumname = album['name'].replace(' ', '')
            filelist = os.listdir('photos/' + target + '/')
            if (albumname in filelist) or (len(albumname) == 0):
                albumname = albumname + '_' + str(theSameAlbumName)
                theSameAlbumName += 1

            os.makedirs('photos/' + target + '/' + albumname)
            same = 0    # 防止同名

            # 获取该相册下的每一张照片，如果相册为空，那么output['data']['photoList'] = None，艹
            photoList = output['data']['photoList']
            if(photoList == None):
                continue

            for photo in photoList:
                log['photo_count'] += 1
                print('当前照片' + photo['name'])

                # 图片格式由photo['phototype']字段(整型)控制
                # 1：jpg
                # 3：png
                phototype = \{'1': '.jpg', '2': '.gif', '3': '.png', '5': '.jpg', '10': '.jpg'\}
                try:
                    format = phototype[str(photo['phototype'])]
                except:
                    format = '.jpg'

                # 建立文件夹并下载图片
                # QQ图片里面有太多的特殊字符了
                photoname = photo['name']
                filelist = os.listdir('photos/' + target + '/' + albumname)
                for i in range(len(filelist)):
                    filelist[i] = filelist[i][:-4]
                photoname = photoname.replace(' ','')

                if (photoname in filelist) or (len(photoname) == 0):
                    photoname = photoname + '_' + str(same)
                    same += 1
                # 文件名中不能有特殊字符
                filt = re.compile(r'\\\\|/|:|\\*|\\?|&lt;|&gt;|\\||\\.|\\n|\\t|\\"')
                photoname = re.sub(filt, '', photoname)

                path = 'photos\\\\' + target + '\\\\' + albumname + '\\\\' + photoname + format
                try:
                    urllib.request.urlretrieve(photo['url'], path)
                except urllib.error.ContentTooShortError as e:
                    print('啥子错误哟')

        fp = open('photos/' + target + '/log.txt', 'w', encoding='utf-8')       # 日志文件，记录时间与数量
        log['time'] = (datetime.datetime.now() - log['time']).seconds
        log['time'] = str(log['time']) + 's'
        fp.writelines(str(log))
        fp.close()
        print('当前QQ：' + target + '下载完毕')</pre>


以下是我获取到的结果，可以说，百分之九十九都成功获取到了，但是有几个好友反映貌似他们的没有获取完，我去看了下，又是获取的json数据结构的问题，我真的服了，
腾讯同一个功能搞那么多数据结构来干嘛，操蛋。  
![](http://7xnc86.com1.z0.glb.clouddn.com/python-Chrome-QQ-album_1.png)  
另外写了一个统计耗时的脚本，因为我在每个相册的日志里都记录了下载时间的，所以直接就统计了



    # 统计log.txt里面所有的数据




    # 根目录是photos




    import os
    import json
    alltime = 0
    for i in os.walk('photos'):
        if(len(i[2]) == 1 and i[2][0] == 'log.txt'):
            fp = open(i[0] + '/' + 'log.txt', 'r')
            data = fp.read()
            data = data.replace('\\'', '"')
            if(data.find('datetime') < 0):
                #print(data)
                output = json.loads(data)
                time = output['time'][:-1]
                alltime += int(time)
                fp.close()
    print(str(alltime/60/60) + 'h')

结果是13.797500000000001h，和我预计的差不多，虽然是4M的网速，但是建立连接建立过多，而且没有用到多线程，这个时间还是合情合理的。

PS：正在把这些照片上传到云盘，哈哈，要是泄漏了可不要说我是故意的 还有就是请勿模仿，我虽然总共下载了400个好友，但是停下来了十多次，都是数据结构出现问题
，请千万不要为此折腾，我纯属是为了完成自己以前的愿望罢了，下载下来也没用。
