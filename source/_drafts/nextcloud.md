---
title: "nextCloud私有云搭建"
date: 2017-06-22 17:09:39
categories: 程序人生
---

nextCloud是由ownCloud原班人马开发，而ownCloud目前已经进入到衰落的阶段。所以现在我决定在家庭NAS里面使用它。顺便说一句，看了它的插件商店，感觉它完全可以用来做中小型企业的内部管理系统，而家庭私有云方面，其插件并不算多。

### 命令系统console.php

```shell
# 将磁盘操作的文件同步到数据库中去，这样复制到用户目录的文件也会显示在nextCloud了
sudo -u www php console.php files:scan [user_id] # 扫描某用户下的文件
sudo -u www php console.php files:scan –all #扫描所有用户下的文件
```

