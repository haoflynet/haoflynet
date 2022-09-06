---
title: "django-celery-beat定时任务配置"
date: 2021-02-25 11:02:30
updated: 2022-09-06 09:37:00
categories: python
---

## 安装

```shell
pip install django-celery-beat
```

## 配置

1. 在`settings.py`中添加如下配置

```python
INSTALLED_APPS = (
    ...,
    'django_celery_beat',
)

CELERY_BROKER_URL = 'sqla+sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
CELERY_IMPORTS = ['schedules']	# 指定需要在哪些目录扫描定时任务，如果不添加则会出现 Received unregistered task of type 错误
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'django-db'	# 这是下面的django-celery-results保存结果使用的
```

2. 使用命令`python manage.py migrate`创建数据库迁移，会生成这几张表：

```shell
django_celery_beat.models.PeriodicTask # 周期性任务
django_celery_beat.models.IntervalSchedule # 间隔性任务
django_celery_beat.models.CrontabSchedule # 定时任务
```

3. 创建启动文件，在`manage.py`所在目录创建一个启动文件celery.py：

```shell
import os

from celery import Celery

from life_console import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "项目名.settings")
celery_app = Celery("项目名", broker=settings.CELERY_BROKER_URL)
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
```

<!--more-->

## 创建定时任务

一个定时任务可以是一个简单的函数，例如(得在`CELERY_IMPORTS`下才能在后台创建)，例如

```python
from 项目名.celery import celery_app

@celery_app.task
def my_cron_reminder():
    print(my_cron_reminder)
```

创建定时执行的任务:

1. 在admin后台创建`PeriodicTask`，选择执行周期即可

2. 或者手动插入至`PeriodicTask`:

   ```python
   schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
   PeriodicTask.objects.create(interval=schedule, name='Custom task', task='schedules.my_corn_minder')
   PeriodicTask.objects.create(interval=schedule, name='Custom task', task='schedules.my_corn_minder', args=json.dumps(['arg1', 'arg2']), kwargs=json.dumps({'abc': 12}))	# 提供参数
   ```

## 启动任务

需要使用下面的命令来启动`worker`，这样可以动态更改项目执行计划后自动生效

```shell
./venv/bin/celery -A 项目名 worker --beat --scheduler django -l debug --logfile=/var/log/celery.log --detach
# -c 1: 设置并发数量，默认是CPU的数量*2，这里设置为1其实也有两个
```

## 使用Django-Celery-Result保存定时任务执行结果

安装: `pip install django-celery-resutls && python manage.py migrate`，这会生成一张`taskresult`表，上面定时任务的结果会自动保存在表中