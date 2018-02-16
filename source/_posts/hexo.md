---
title: "hexo 教程"
date: 2016-08-11 8:52:39
updated: 2018-02-11 13:51:00
categories: tools
---
### 安装hexo

```yaml
curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
yum install nodejs -y
npm install -g hexo-cli
```
##### 添加RSS

通过`npm install -g hexo-generator-feed`安装  
然后修改`hexo/_config.yml`添加如下代码：

```yaml
plugins:
- hexo-generator-feed
```

##### 添加sitemap

通过`npm install -g hexo-generator-sitemap`安装
然后修改`hexo/_config.yml`添加如下代码：

```yaml
plugins:
- hexo-generator-sitemap
```

### 全局设置

### 文章设置

文章的抬头可以指定如下信息:

```tex
title: "文章标题"
date: 2016-08-07 8:52:39		# 文章发布时间
updated: 2016-09-02 15:50:00	# 文章修改时间
categories: tools				# 文章分类
```

### TroubleShooting

- **nginx 403**:可能是因为没有在public生成`index.html`文件导致，检查是否执行过`npm install`安装完所有的模块，以及`themes`目录下是否存在该主题的文件
- **no content页面只有框架没有内容**: 可能是历史的css文件遗留所致，此时可以清空public目录下的文件再重新生成

##### 