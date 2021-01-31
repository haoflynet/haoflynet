---
title: "nextCloud私有云搭建"
date: 2017-06-22 17:09:39
updated: 2019-07-03 08:00:00
categories: 程序人生
---

nextCloud是由ownCloud原班人马开发，而ownCloud目前已经进入到衰落的阶段。所以现在我决定在家庭NAS里面使用它。顺便说一句，看了它的插件商店，感觉它完全可以用来做中小型企业的内部管理系统，而家庭私有云方面，其插件并不算多。

## 安装部署

### 虚拟机安装步骤

1. 安装依赖

   ```shell
   sudo apt-get install php7.2-intl
   ```

2. 下载并解压源码至`/var/www/nextcloud`，然后修改目录所有者`sudo chown -R www-data:www-data`

3. PHP配置

   ```shell
   # vim /etc/php/fpm/php.ini
   memory_limit = 4096M	# 将原有128M修改到你的理想值
   ```

4. nginx配置

   ```shell
   文件放到/var/www/nextcloud，然后nginx配置文件如下
   upstream php-handler {
           server unix:/var/run/php/php7.2-fpm.sock;
   }
   
   server {
           listen 80;
           listen [::]:80;
   
       # Add headers to serve security related headers
       # Before enabling Strict-Transport-Security headers please read into this
       # topic first.
       # add_header Strict-Transport-Security "max-age=15768000;
       # includeSubDomains; preload;";
       #
       # WARNING: Only add the preload option once you read about
       # the consequences in https://hstspreload.org/. This option
       # will add the domain to a hardcoded list that is shipped
       # in all major browsers and getting removed from this list
       # could take several months.
       add_header X-Content-Type-Options nosniff;
       add_header X-XSS-Protection "1; mode=block";
       add_header X-Robots-Tag none;
       add_header X-Download-Options noopen;
       add_header X-Permitted-Cross-Domain-Policies none;
       add_header Referrer-Policy no-referrer;
   
       # Remove X-Powered-By, which is an information leak
       fastcgi_hide_header X-Powered-By;
   
       # Path to the root of your installation
       root /var/www/nextcloud/;
   
       location = /robots.txt {
           allow all;
           log_not_found off;
           access_log off;
       }
       
       
       # The following 2 rules are only needed for the user_webfinger app.
       # Uncomment it if you're planning to use this app.
       #rewrite ^/.well-known/host-meta /public.php?service=host-meta last;
       #rewrite ^/.well-known/host-meta.json /public.php?service=host-meta-json
       # last;
   
       location = /.well-known/carddav {
         return 301 $scheme://$host/remote.php/dav;
       }
       location = /.well-known/caldav {
         return 301 $scheme://$host/remote.php/dav;
       }
   
       # set max upload size
       client_max_body_size 512M;
       fastcgi_buffers 64 4K;
   
       # Enable gzip but do not remove ETag headers
       gzip on;
       gzip_vary on;
       gzip_comp_level 4;
       gzip_min_length 256;
       gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
       gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;
   
       # Uncomment if your server is build with the ngx_pagespeed module
       # This module is currently not supported.
       #pagespeed off;
       
       
       location / {
           rewrite ^ /index.php$request_uri;
       }
   
       location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {
           deny all;
       }
       location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
           deny all;
       }
   
       location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+)\.php(?:$|/) {
           fastcgi_split_path_info ^(.+?\.php)(/.*)$;
           include fastcgi_params;
           fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
           fastcgi_param PATH_INFO $fastcgi_path_info;
           #fastcgi_param HTTPS on;
           #Avoid sending the security headers twice
           fastcgi_param modHeadersAvailable true;
           fastcgi_param front_controller_active true;
           fastcgi_pass php-handler;
           fastcgi_intercept_errors on;
           fastcgi_request_buffering off;
   
           fastcgi_connect_timeout 6000;
   fastcgi_send_timeout 6000;
   fastcgi_read_timeout 6000;
   proxy_connect_timeout 6000s;
   proxy_send_timeout 6000s;
   proxy_read_timeout 6000s;
   
       }
       
       location ~ ^/(?:updater|ocs-provider)(?:$|/) {
           try_files $uri/ =404;
           index index.php;
       }
   
       # Adding the cache control header for js and css files
       # Make sure it is BELOW the PHP block
       location ~ \.(?:css|js|woff|svg|gif)$ {
           try_files $uri /index.php$request_uri;
           add_header Cache-Control "public, max-age=15778463";
           # Add headers to serve security related headers (It is intended to
           # have those duplicated to the ones above)
           # Before enabling Strict-Transport-Security headers please read into
           # this topic first.
           # add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload;";
           #
           # WARNING: Only add the preload option once you read about
           # the consequences in https://hstspreload.org/. This option
           # will add the domain to a hardcoded list that is shipped
           # in all major browsers and getting removed from this list
           # could take several months.
           add_header X-Content-Type-Options nosniff;
           add_header X-XSS-Protection "1; mode=block";
           add_header X-Robots-Tag none;
           add_header X-Download-Options noopen;
           add_header X-Permitted-Cross-Domain-Policies none;
           add_header Referrer-Policy no-referrer;
   
           # Optional: Don't log access to assets
           access_log off;
       }
   
       location ~ \.(?:png|html|ttf|ico|jpg|jpeg)$ {
           try_files $uri /index.php$request_uri;
           # Optional: Don't log access to other assets
           access_log off;
       }
   }
   
   ```

5. 新建数据库用户(必须新建一个数据库用户，如果用`root`的话会因为权限太大导致安装失败)

   ```mysql
   create database nextcloud; 
    create user nextclouduser@'%' identified by 'test';
   grant all privileges on nextcloud.* to nextclouduser@'%' identified by 'test';
   flush privileges; 
   ```

### 命令系统console.php

```shell
# 将磁盘操作的文件同步到数据库中去，这样复制到用户目录的文件也会显示在nextCloud了
sudo -u www php occ files:scan [user_id] # 扫描某用户下的文件
sudo -u www php occ files:scan –all #扫描所有用户下的文件
sudo -u www php occ files:scan –all -vvv # vvv打印debug日志
sudo -u www php occ files:scan --path=user/files/目录	# 可以指定扫描某用户下的指定的目录
```

## 插件推荐



## TroubleShooting

- **无法扫描软链接关联的文件夹**: 本身为了安全性，所以不支持，解决办法是使用`mount —bind`命令将目录挂载到用户目录下
- **不想使用https**: 新版本默认强制使用`https`，想要禁止可以直接修改`nginx`的配置，把` fastcgi_params HTTPS on;`去掉即可
- **PHP的安装似乎不正确，无法访问系统环境变量。getenv("PATH")函数测试返回了一个空值**: 需要修改`/etc/php/fpm/php-fpm.conf`文件，在末尾添加`env[PATH] = /usr/local/bin:/usr/bin:/bin:/usr/local/php/bin`

