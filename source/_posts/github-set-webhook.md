---
title: "在Github上设置webhook钩子"
date: 2015-03-22 17:47:14
categories: 编程之路
---
又搞了一天才搞好，主要原因是没看懂错误提示信息。

**webhook**：简单地说，使用webhook可以让每次在本地push到github上去后，让服务器自动pull下来，这样就不用每次提交然后手动pull的过程了。

下面是详细配置过程(基于laravel)：

1. 首先，得在laravel里添加一个路由，然后指向某个文件，例如路由为'/webhook'，然后指向PHP文件为'webhook.php'，然后在该文件内添加如下内容，该文件即是服务器响应Github webhook请求的文件：

		<?php
			$dir = '/var/www/test';
			echo shell_exec("cd /var/www/test");
			echo shell_exec("sudo git pull -f git@github.com:haoflynet/guake.git 2>&1");
    	?>

2. 用户权限问题，由于执行该PHP文件的用户是apache的默认用户www-data，所以我在上面的命令中使用的是'sudo'，这样可以不用给www-
data用户生成ssh，然后又出现各种混乱的问题。但是www-
data又怎么免输密码执行git命令呢，还好linux提供了这么一个方面的操作，在'/etc/sudoers'文件里有如下内容：

		# User privilege specification
		root ALL=(ALL:ALL) ALL  # 默认的root用户可以在所有平台使用所有权限
		www-data ALL=NOPASSWD:/usr/bin/git # 这里给www-data赋予免密码执行git的权限

3. 在仓库中添加钩子，执行`vim .git/hooks/post-receive`，然后添加如下内容，最后还要加入可执行权限：

        GIT_WORK_TREE=/var/www git checkout -f

4. 在Github上进行设置  
![](http://7xnc86.com1.z0.glb.clouddn.com/github-set-webhook_0.png)  
如图所示添加webhook，设置中可以选择各种出发事件event，一般默认是push事件，在Payload
URL中设置自己刚才所设置的URL，最后添加即可完成。

5. 测试
测试钩子的时候，可以直接在Github上面看到执行的列表，还可以看到每一个POST的详细信息以及响应信息：  
![](http://7xnc86.com1.z0.glb.clouddn.com/github-set-webhook_2.png)  

## TroubleShooting：
- Laravel 5中如果要设置webhook，该POST路由不能使用CSRF
- Django同样要禁用csrf：

		import os
		from django.views.decorators.csrf import csrf_exempt
		from django.http import HttpResponse

		@csrf_exempt
		def webhook(request):
			os.system('cd /var/www/admin')
		os.system('git pull -f git@github.com:haoflynet/admin.git 2>&1')
			return HttpResponse('ok')
