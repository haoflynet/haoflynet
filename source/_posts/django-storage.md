---
title: "Django使用七牛云作为自定义的存储系统"
date: 2019-05-23 21:32:00
updated: 2019-05-31 17:25:00
categories: 编程之路
---

Django提供了非常方便的方法以供你自定义存储系统，只需要在项目的任意地方新建一个继承自`django.core.files.sotrage.Storage`的类即可。如果是使用七牛云，可以直接使用以下代码，当然首先要安装七牛的sdk: `pip install qiniu`:

<!--more-->

```python
# qiniu_storage.py
import datetime
import uuid

from django.core.files.storage import Storage
from qiniu import Auth, put_data

from settings import (QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BACKET_NAME, QINIU_URL)

class QiniuStorageObject(Storage):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.file = None

    def _new_name(self, name):		# 将上传的文件重新命名
        new_name = "file/{0}/{1}.{2}".format(
            self.now.strftime("%Y/%m/%d"),
            str(uuid.uuid4()).replace("-", ""),
            name.split(".").pop(),
        )
        return new_name

    def _open(self, name, mode):
        return self.file

    def _save(self, name, content):
        """
        保存文件的操作，返回值为文件的url全路径，会自动保存在需要存储的地方。
        这里的content可以是一个文件对象，也可以是一个bytes对象
        """
        q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        token = q.upload_token(QINIU_BACKET_NAME)
        self.file = content
        file_data = content.file
        ret, info = put_data(
            token,
            self._new_name(name),
            file_data if isinstance(file_data, bytes) else file_data.read(),
        )

        if info.status_code == 200:
            base_url = "%s/%s" % (QINIU_URL, ret.get("key"))
            return base_url
        else:
            raise Exception("上传七牛失败")

    def exists(self, name):
        return False

    def url(self, name):
        return name	# 由于上面返回的就是全路径，所以这里没必要再做什么操作
```

最后，只需要将默认的文件存储系统替换为你写的类即可：

```python
# settings.py
DEFAULT_FILE_STORAGE = 'utils.qiniu_storage.QiniuStorageObject'	# 替换Django默认的存储系统
CKEDITOR_STORAGE_BACKEND = 'utils.qiniu_storage.QiniuStorageObject'	# 替换CKEDITOR默认的存储系统

# models.py
class MyModel(models.Model):
  image = ImageField(storage=QiniuStorageObject())	# 或者仅在指定的字段使用该存储系统	
```

如果想手动存储文件，可以这样做:

```python
import requests
from django.core.files.storage import default_storage

response = requests.get('img_url')
url = default_storage.save('img_url'.split('/')[-1], response.content)
```

