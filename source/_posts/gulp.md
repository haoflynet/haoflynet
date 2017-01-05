---
title: "gulp教程"
date: 2016-09-08 04:11:39
categories: frontend
---
# gulp
前端的自动化构建工具，能够自动化处理一些常见的任务：

- 搭建web服务器
- 修改文件自动刷新浏览器
- 预处理Sass、Less
- 优化资源：CSS、Javascript、图片等

## 安装方式
全局安装：`npm install gulp -g`
当前项目安装: ` npm install --save-dev gulp`
安装后，会在当前目录生成一个`node_modules`目录，然后执行`npm init`初始化当前项目，根据提示输入一些项目的基本信息，然后会生成一个`package.json`文件


## 目录结构
	app/		# 开发目录，存放源文件
		css
		fonts
		images
		js
	dist/		# 存放生产环境下的内容
	gulpfile.js
	node_modules/
	package.json

## gulpfile.js文件

	var gulp = require('gulp'),	# 去node_modules下导入相应的包
		livereload = require('gulp-livereload'),
		del = require('del'),
		notify = require('gulp-notify'),
		browserify = require('gulp-browserify'),
		jshint = require('gulp-jshint');
	
	gulp.task('scripts', function(){
	//这里可以不用把所有的.js合并成一个，而是可以按需合并，比如每个文件都需要用到的就合并成一个，其他单独的则单独合并，不许return，写两个gulp.src即可，比如gulp.src('app/js/base.js').pipe......和gulp.src('app/js/new.js').pipe...
	    .pipe(browserify({
	        insertGlobals: true,
	        debug: !gulp.env.production
	    }))
	    .pipe(concat('base.js'))        // 这是把上面所有的js文件合并为一个文件
	    .pipe(gulp.dest(DEST+'/js'))
	    .pipe(rename({suffix: '.min'}))
	    .pipe(uglify())
	    .pipe(gulp.dest(DEST+'/js'))
	    .pipe(notify({
	        message: 'Scripts task complete'
	    }));
		
	gulp.task('clean', function(cb){	# 定义任务
		del(['dist', cb]);
	});
	
	gulp.task('default', ['clean'], function(){
		gulp.start('scripts');
	});
	
	gulp.task('watch', function(){
		gulp.watch('app/js/index.js', ['scripts']);	# 见识文件，当监控的文件变化时执行相应的任务
		livereload.listen();
		gulp.watch(['dist/**']).on('change', livereload.changed);
	});

在命令行执行`gulp task_name`就可以运行该任务了


## 其他插件
- **gulp-jshint**: js代码校验
- **gulp-concat**: js代码合并
- **gulp-notify**: 更改提醒
- **gulp-uglify**: js代码压缩
- **gulp-livereload**: 自动刷新页面
- **del**: 清除文件