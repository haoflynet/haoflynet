---
title: "MySQL source命令批量导入数据库及乱码问题的解决"
date: 2014-11-09 15:49:56
categories: 编程之路
---
参考：<http://www.111cn.net/database/mysql/46646.htm>

近日老板给了我一个数据库，让我学学人家是怎么设计的，之前从来没有导入过别人的数据库，期间遇到一些问题，特记录如下：

# 1.批量导入问题

首先老板给我的文件不是一个单独的sql文件而是一张一张单独的表对应的sql文件，加起来好几十个，我可不想一个一个的导入，所以到网上找到了一个比较方便的方法：

首先，要知道有一种sql文件是这样的：



    source file1.sql;
    source file2.sql;
    srouce file3.sql;
    ...

如果再用source命令执行这个文件的话就可以实现批量导入功能，但是怎么能直接获取全部文件名呢(由于source命令是在mysql shell里执行的，所以
要用绝对路径)，这是可以用管道了(linux下用ls，windows下用dir)。首先可以把所有sql文件放到一个文件夹内(如果同名就重命名，没有关系的)。
然后在cmd里执行



    dir foldername /b/od/s > all.sql

这条命令会列出foldername文件夹内的所有子文件的绝对路径并将结果输出到all.sql文件内。然后用文本编辑器打开该sql文件，用替换工具，将每一行替
换为



    source 绝对路径;

的形式并保存。然后在MySQL里执行



    source all.sql的绝对路径

这样就能完全导入了。

# 2.导入乱码的问题

出现乱码肯定是中文乱码，但是，虽然你把MySQL默认编码设置为utf8并且把数据库设置为utf8但依然无法避免人家导出时不用utf8的情况，我应该就是碰到这
么一个问题了，所以下次自己用命令导出的时候一定要设置编码：



    mysqldump -uroot -pmysql --default-character-set=utf8 database > xxxx.sql

而如果遇到别人的数据库导入乱码的时候就需要把所有东西全部设置为utf8就可以彻底解决问题了：



    SET character_set_client = utf8;
    SET character_set_connection = utf8;
    SET character_set_database = utf8;
    SET character_set_results = utf8;
    SET character_set_server = utf8;
    SET collation_connection = utf8_bin;
    SET collation_database = utf8_bin;
    SET collation_server = utf8_bin;




    # 然后再导入




    source all.sql
