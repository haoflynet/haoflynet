---
title: "如何用七牛云托管整个静态博客网站"
date: 2018-06-28 07:32:00
categories: 编程之路
---

从Wordpress到Github，最后再到七牛云，我的网站也是命运多舛呀。随着互联网技术的发展，以后可能会选择其他的网站进行托管，但无论怎样，静态博客站点可能是我会一直坚持的。如今我把本网站全部放在七牛云，由于访问量少，所以每个月流量就几毛钱(如果仅仅是七牛云的国内HTTP流量，10G以内是完全免费的)。虽然用七牛云托管已经有一年多的时间了，但是最近才把全站的所有内容搞成HTTPS的，这里简单记录一下整个过程。

## 托管静态内容

<!--more-->

1. 首先，使用`hexo`等静态站点生成工具生成静态网站全部内容。

2. 在七牛云注册帐号并在`对象存储`里面`新建存储空间`，空间必须设置为`公开空间`

3. 由于网页版无法使用上传文件夹到空间里面去，所以需要借助专门的[上传工具](https://developer.qiniu.com/sdk#official-tool)，mac上并没有图形界面上传工具，我这里没有用命令行工具，而是用的[Python SDK](https://developer.qiniu.com/kodo/sdk/1242/python)自己写了个命令行工具，该工具能够做到删除多余的文件，只上传新建及修改过的文件[qiniu-for-static-web-hosting 同步文件夹至七牛云](https://gist.github.com/haoflynet/2cddf14c8a9b6359b2c48670421536ff/raw/342f8077637a4a66a364622a3bd5feff14840e37/qiniu_sync.py)

   ```python
   from qiniu import Auth, put_file, etag, urlsafe_base64_encode, BucketManager
   from typing import List, Dict
   import os
   from qiniu import build_batch_delete
   class Sync:
       """
       同步目录至七牛云
       """
       def __init__(
           self,
           access_key: str,
           secret_key: str,
           bucket_name: str,
           sync_dir: str,
           exclude: List,
           cover: bool,
           remove_redundant: bool,
       ):
           self.bucket_name = bucket_name
           self.q = Auth(access_key, secret_key)
           self.bucket = BucketManager(self.q)
           self.sync_dir = sync_dir
           self.exclude = exclude
           self.cover = cover
           self.remove_redundant = remove_redundant
           self.sync()
       def sync(self):
           """
           同步操作
           :return:
           """
           remote_files = self.list_remote()
           local_files = self.list_local()
           # 首先删除远端仓库中多余的文件
           remove_remote_files = []
           for remote_filename in remote_files:
               if remote_filename not in local_files:
                   remove_remote_files.append(remote_filename)
           self.bucket.batch(build_batch_delete(self.bucket_name, remove_remote_files))
           # 上传本地文件到远端(仅上传远端不存在的以及修改过的)
           for local_filename in local_files:
               if (
                   local_filename not in remote_files
                   or local_files[local_filename]["hash"]
                   != remote_files[local_filename]["hash"]
               ):
                   print("puting " + local_filename)
                   ret, info = put_file(
                       self.q.upload_token(self.bucket_name, local_filename, 3600),
                       local_filename,
                       local_files[local_filename]["fullpath"],
                   )
       def list_remote(self) -> Dict:
           """
           列出远程仓库所有的文件信息
           :return: List
           """
           result = {}
           for file in self.bucket.list(self.bucket_name)[0]["items"]:
               result[file["key"]] = file
           return result
       def list_local(self) -> Dict:
           """
           列出本地仓库所有的文件信息
           """
           files = {}
           def get_files(path):
               for filename in os.listdir(path):
                   if filename in self.exclude:
                       continue
                   fullpath = os.path.join(path, filename)
                   if os.path.isfile(fullpath):
                       key = fullpath.split(self.sync_dir)[1]
                       files[key] = {"fullpath": fullpath, "hash": etag(fullpath)}
                   else:
                       get_files(fullpath)
           get_files(self.sync_dir)
           return files
   if __name__ == "__main__":
       Sync(
           access_key="",  # access_key
           secret_key="",  # secret_key
           bucket_name="blog",  # bucket_name
           sync_dir="",  # 静态文件目录(后面必须有斜杠/)
           exclude=[".DS_Store"],
           cover=True,
           remove_redundant=True,
       )
   ```

## 绑定自定义域名

完成上面一步后还只能使用类似`xxxxx.bkt.clouddn.com`这样的测试域名进行访问，既然是自己的博客当然希望用自己的域名啦，不过需要注意的是，国内厂商的web服务要绑定自定义域名的话，域名都必须得先备案，这一点如果不能满足，我就爱莫能助了。绑定自定义域名步骤：

1. 在`存储空间->绑定域名`处`创建域名`。覆盖范围直接选择`全球`；通信协议选择`HTTPS`，此时会让你选择`SSL`证书，没有证书也没有关系，进入`证书管理`页面申请七牛提供的免费的证书即可；最好开启`强制HTTPS访问`选项；其他参数默认即可。

2. 设置域名解析。在自己的域名管理后台设置域名解析，添加CNAME记录，主机记录为`@`，记录值为七牛提供的类似`xxx.qiniudns.com`的记录值

3. 成功则如下图所示

   ![](https://haofly.net/uploads/how-to-use-qiniu-for-static-web-hosting.png)

