# haoflynet
[豪翔天下的博客](https://haofly.net)，采用`hexo`静态博客引擎，并全站托管至七牛云

## 安装部署

```javascript
npm install hexo-cli -g
npm install --save

npm install hexo-generator-sitemap
npm install hexo-generator-feed
```

## 博客更新

```shell
hexo g	# 生成站点静态文件
hexo s	# 预览站点
python3 sync_qiniu.py	# 同步至七牛云的仓库
```

