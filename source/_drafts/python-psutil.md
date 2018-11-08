---
title: "psutil"
date: 2017-11-01 21:32:00
categories: python
---

系统

进程

```python
psuti.pids()	# 打印所有进程id
psutil.pid_exists(pid)	# 判断指定进程是否存在
psutil.Process(pid)	# 得到进程对象
psuti.process_iter(attrs=['pid', 'name', 'username'])	# 返回所有进程内容，可以筛选能获取到的进程的信息。可以获取到的进程信息包括status(进程状态sleeping)、cpu_num、pid(进程id)，cmdline(进程命令)，create_time(创建时间)、cpu_percent(CPU占用率)、open_files(打开的文件列表)、name(所属用户的用户名)、num_threads(线程数)、memory_percent(内存占用率)、environ(系统变量)等
```

