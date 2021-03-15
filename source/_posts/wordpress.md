---
title: "wordpress安装使用与插件推荐"
date: 2014-08-05 11:02:30
updated: 2021-03-14 22:11:00
categories: tools
---
## 安装wordpress

### CentOS 6.x安装wordpress

```shell
# 在已经安装了php运行环境的条件下
wget http://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz 

# 建立数据库
mysql -u root -p
> CREATE DATABASE wordpress;
> CREATE USER wordpressuser@localhost;
> SET PASSWORD FOR wordpressuser@localhost= PASSWORD("password");
> GRANT ALL PRIVILEGES ON wordpress.* TO wordpressuser@localhost IDENTIFIED BY 'password';
> FLUSH PRIVILEGES;
> exit;

# 配置
cp ~/wordpress/wp-config-sample.php ~/wordpress/wp-config.php
vim ~/wordpress/wp-config.php
修改DB_NAME／DB_USER／DB_PASSWORD

sudo yum install php-gd  # 如果启动不了要安装这个
```

## 必备插件推荐

- **All-in-One WP Migration**: 一件迁移插件，能够直接打包整站所有内容，包括代码、数据库、配置等

- **Crayon Syntax Highlighter**：一款在文章中插入特定格式代码的插件，找了很久才找到这么一款可自定义很多功能，并且外观也不错，而且设置还是全中文的

- **duoshuo**：多说评论

- **Google Analyticator**：谷歌的网站行为分析工具，可统计每日浏览量，甚至可以统计用户的浏览器和操作系统等信息

- **JiaThis分享工具**：社会化分享工具

- **WP-DB-Backup**：数据库备份工具，可自定义备份时间和备份位置(网站空间、本地电脑、发送邮件)

- **WPJAM七牛镜像存储**：使用七牛云存储实现 WordPress 博客静态文件 CDN 加速

- **WP-PostViews**：文章浏览量统计工具：WP-PostViews的功能不仅能统计浏览量，还可根据浏览量的多少来排序，但是我只用来记录浏览量的，网上很多教程都说把那一句代码插入到主题的loop里面去，却没有哪一篇教程说过具体该是哪个地方，虽然wordpress的主题各种各样，但至少可以把自己的插入位置列出来吧。我是将下面这一样代码插入到content.php文件

  ```html
  <footer class="entry-meta">
  <?php twentytwelve_entry_meta(); ?>           # 这一行是本来的显示文章发布时间的地方   
  <?php if(function_exists('the_views')) { the_views(); } ?>   # 这一行即是要插入的这一行   
  <?php edit_post_link( __( 'Edit', 'twentytwelve' ), '<span class="edit-link">', '</span>' ); ?>
  ```

  插入成功后(注：如果出现语法错误，可能会导致一直错误，根本改不过来，此时要重新下载该主题压缩包然后把那个文件的内容通过ftp复制上去，才可以)

- [What WordPress Theme Is That?](http://whatwpthemeisthat.com/): 这并不是插件，而是一个很棒的网站，在这里仅需要输入目标wordpress网站的网址，你就知道目标网站所采用的wordpress的主题以及一些能检测到的部分插件。

## TroubleShooting

- **修改固定链接为文章标题后，打开文章变成404**: 如果是nginx，那么在配置文件中的location添加一句:

  ```she
  location / {
     try_files $uri $uri/ /index.php?$args;
  }
  ```




