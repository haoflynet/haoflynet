---
title: "travis-ci"
date: 2016-06-07 11:06:30
categories: tools
---
# travis-ci

与github紧密联系的自动化持续集成工具。需要注意的是它仅是一个测试工具，并不能代替webhook的功能。



## .travis.yml文件

`travis.yml`是travis-ci的配置文件，具体语法如下:

```yaml
sudo: required		# 是否需要sudo权限
dist: trusty		# 目标操作系统，这是ubutnu 14.04

notifications:		# 发送构建结果的通知
	email:
		- haoflynet@gmail.com	

addons:
	apt:
		sources:	# 源，但只能是白名单内的https://github.com/travis-ci/apt-source-whitelist/blob/master/ubuntu.json
			- google-chrome
		packages:
			- google-chrome-stable

branches:		# 指定需要跑travis-ci的分支
	only:
		- master

language: node_js	# 项目所使用的语言
node_js:			# 该语言所运行的版本，可多个版本同时测试
	'4'					
	'6'	
	
# 下面几条指令会按顺序执行
before_install:
	- nvm install 6.0.0
	
install: npm install

before_script:		# 在开始测试前需要运行的指令，也可在这里执行sudo apt-get 安装一些基础trusty没有的包，当然，安装包可以直接使用addons的apt
  - npm install
  - cd tests

script: phpunit -v	# 执行脚本

after_failure:
	- cat /home/travis/build/haoflynet/haoflynet-repo/abc.log
	
after_success:
	- ...
	
before_deploy:		# 一些部署操作，比如生成APK包
	- ...
	
deploy:
	provider: script
	script: ci/deploy.sh
	skip_cleanup: true
	
after_deploy:		# 发布的一些操作，比如将包发布到fir.im上去
	- ...
```



