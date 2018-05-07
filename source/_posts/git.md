---
title: "Git 手册"
date: 2016-08-07 07:12:39
updated: 2018-05-06 19:59:00
categories: tools
---
# Git指南

这里所列举的通用配置无论是在Windows还是Linux，都要用到。

## 安装与配置

### 安装Git软件

Windows平台：[Git for Windows](http://msysgit.github.io/)(在安装的时候注意那些选项的设置)  

Linux平台：`sudo apt-get install git`

### 基础配置

打开终端，在windows平台就用上一步安装上的git bash

    # 全局配置，这里的用户名和邮箱填写你自己的帐号，可以是github上的帐号信息
    git config --global user.name "haoflyent"
    git config --global user.email "haoflynet@gmail.com"
    
    # 如果要同一台机器多个git账户，那么可以取消全局设置
    git config --global --unset user.name
    git config --global --unset user.email
    git config user.email "x@xx.com"    # 在仓库里面单独设置
    git config user.name "xx"
    
    # 生成密钥
    ssh-keygen -t rsa -C "haoflynet@gmail.com"
    # 然后一路默认就可以，注意看其中的密钥存放位置，其中公钥文件Windows默认为/c/Users/用户名/.ssh/id_rsa.pub# Linux默认为 ~/.ssh/rsa_pub

<!-- more -->

### Git相关文件

**.gitkeep**: 这个文件当前所在的空目录可以加入到版本控制里面去

## Github的使用

打开公钥文件，然后复制其中的内容到Github上的setting->SSH keys->Add SSH key，如下  
![](http://7xnc86.com1.z0.glb.clouddn.com/configuration-of-git_0.png)  
点击Add Key后会要求输入github密码，因为这是特别敏感的操作  
然后进行新建仓库，无论是github还是其他托管网站都可以新建远程库，新建完成后都会提示你下一步该怎么做  
![](http://7xnc86.com1.z0.glb.clouddn.com/configuration-of-git_1.png)  
按照上图给出 操作指南，有三种方法分别是
- 在本地建立一个新库，并新建一个README.md到远程库
- 直接将本地库的代码推送到远程库，不过在本地需要将文件夹编程一个库
- 从别的库导入代码到该库  
  具体的命令在途中均有给出

## 常用操作

#### 日志/历史/版本

```shell
git remote -v 	# 列出远程仓库地址

git log  # 查看提交的历史,--oneline按行显示，--graph查看分支的合并情况，--all显示所有分支的历史
git reflog	# 查看HEAD的历史情况

# 版本回退/回滚,--hard表示将该次提交之前所有的更改都丢弃，git reset是把HEAD向历史移动，而git revert是HEAD继续向前，新的commit就和revert的内容刚好相反，所以推荐使用revert，reset的target是要会退到的版本，而revert得target是要取消的版本
git reset --hard HEAD^  # 回退到上一个版本
git reset --hard HEAD^^ # 回退到上上个版本
git reset --hard 233333 # 指定提交ID的回退
git push -f origin master	# remote端也更新
```

#### 代码更改

```shell
git blame filename   # 查看某文件的改动历史
git diff + 分知名   # 比较当前分支和目标分支的不同
git diff master

git reset HEAD filename		# 把已经commit了的文件取消暂存
git checkout -- filename	# 放弃指定文件的更改
git commit --amend			# 撤销上一次提交，并将暂存区文件重新提交

git stash					# 暂存，常用于要切换分支，但是当前分支上面的更改并不想现在提交，需要先把当前分支的状态暂存起来。暂存起来后就可以自由切换到其他分支了。
git stash list				# 查看所有的"储藏"
git stash apply				# 应用最近一次的“储藏”
git stacsh apply stash@{2}	# 应用指定的"储藏"
```

#### 分支操作

分支命名规范:

- 功能(feature)分支: `feature-*`
- 预发布(release)分支: `release-版本号`
- 修补bug(fixbug)分支: `fixbug-*`

```shell
git fetch						# 取回所有分支的更新
git fetch -p					# 取回远程分支，并且在本地删除远程已经删除的分支
git branch -a  					# 查看所有分支
git branch -D dev				# 删除本地分支
git checkout -b new-branch 		# 在本地新建分支并切换到新分支
git checkout -b dev origin/dev	# 拉取远程分支到本地并命名为dev分支
git push origin :serverfix		# 直接删除远程分支

## 强制覆盖本地分支
git fetch --all
git reset --hard origin/master

## 合并分支
### 在新的分支如bug-fix修改完成后，执行以下操作
git checkout dev	# 切换回dev分支
git merge bug-fix	# 将bug-fix合并到当前分支，即dev分支
```

#### 标签

```shell
git tag 									# 查看当前所有的标签
git tag v1.0.0							# 在当前commit打一个标签
git tag -d v1.0.0						# 删除一个标签
git push origin v1.0.0					# 将打的标签推送到仓库
git push origin :refs/tags/v1.0.0		# 本地删除标签后远程也要删除
```

#### 其他功能

```shell
# 统计代码行数
git log --author="$(git config --get user.name)" --pretty=tformat: --numstat | gawk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "added lines: %s removed lines : %s total lines: %s\n",add,subs,loc }' -
```

## 贡献PR(Fork别人的项目)

如果希望给开源项目贡献代码或者直接修复bug，那么就需要涉及到fork了并提交了。步骤如下:

1. fork别人的仓库到自己这里: 直接在github里面点击fork，即可在自己的代码仓库里面创建一个一模一样的仓库。

2. 从自己的代码仓库clone下来，并开发。

3. 开发完成后，commit到自己的代码仓库

4. 在自己的项目创建Pull Request，指向到原开源项目中去。

   ![](http://ojccjqhmb.bkt.clouddn.com/git_1.jpg)

![](http://ojccjqhmb.bkt.clouddn.com/git_2.jpg)

记得添加commit说明。

## 多人协作

参考文章：[廖雪峰的官方网站](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013760174128707b935b0be6fc4fc6ace66c4f15618f8d000)
前提：已经在Github上创建了库并创建了一个新的分支，假设新分支名为dev，那么开发步骤如下：

1. 抓取远程分支到本地

   ```shell
    git clone git@github.com:haoflynet/test.git
    git branch      # 查看当前分支
    git checkout -b dev origin/dev  # 将本地的dev分支对应远程的origin/dev分支并切换到该分支
    
    git clone -b mybranch --single-branch git://sub.domain.com/repo.git # 直接拉取指定分支到本地
   ```
2. 在该分支下进行开发
3. 修改完成后推送到远程dev分支

        git add .
        git commit -m "some modification"
        git push origin dev
4. 修改并合并到master分支

        git checkout master # 首先切换到本地的master分支
        git merge --no-ff   # 将本地的dev分支与本地的master分支合并
        git pull            # 获取远程索引

    这一步可能这一步可能会冲突，原因当然是其他人在你之前对远程的master分支进行了修改并提交上去
    如果没有错，就直接推送
    git push origin master

## TroubleShooting

- **git checkout -b dev origin/dev出现错误fatal: cannot update paths and switch to branch 'origin/dev'** 
  原因是未在远程创建dev分支，或者未在本地更新分支信息

- **git remote add origin git@github.com:haoflynet/test，出现错误fatal: remote origin already exists** 
  原因是克隆别人的库下来修改后push到自己的库可能会出现这种错误，要先执行git remote rm origin  

- **.gitignore无效，该忽略的依然没有被忽略**

   ```shell
   git rm -r --cached .
   git add .
   git commit -m "fixed untracked files
   ```

   这样会删除github上面已经提交了的但是现在忽略了的文件，如果要在github上面保留一份，那么执行`git add -f filename`

- **There was a problem with the editor 'vi'** 
  vi编辑器的问题吧，直接换成vim
  `git config --global core.editor $(which vim)`

- **更改文件名后，远程居然没有过更新** 
  git默认对文件名的大小写不敏感，需要在仓库执行`git config core.ignorecase false`让它对大小写敏感

- **`413 request entity too large`**

  发生这个问题是因为采用的是https而不是ssh方式来push仓库，而https传输数据的大小一般是由服务器，即nginx来控制的，太大了是传不上去的，这时候只需要更改为ssh方式即可。

- **修改提交作者和邮箱**: git可以通过`git filter-branch`修改已经提交了的commit的作者和邮箱。如果仅仅想修改一次的，可以直接`git commit --amend --author="haoflynet <haoflynet@gmail.com>"`。这里有一个来自[若有所思-胡磊](http://i.dotidea.cn/2015/04/git-amend-author/)的批量修改的脚本:

  ```shell
  #!/bin/sh
   
  git filter-branch --env-filter '
   
  an="$GIT_AUTHOR_NAME"
  am="$GIT_AUTHOR_EMAIL"
  cn="$GIT_COMMITTER_NAME"
  cm="$GIT_COMMITTER_EMAIL"
   
  if [ "$GIT_COMMITTER_EMAIL" = "[Your Old Email]" ]
  then
      cn="[Your New Author Name]"
      cm="[Your New Email]"
  fi
  if [ "$GIT_AUTHOR_EMAIL" = "[Your Old Email]" ]
  then
      an="[Your New Author Name]"
      am="[Your New Email]"
  fi
   
  export GIT_AUTHOR_NAME="$an"
  export GIT_AUTHOR_EMAIL="$am"
  export GIT_COMMITTER_NAME="$cn"
  export GIT_COMMITTER_EMAIL="$cm"
  '
  ```

- **error: you need to resolve your current index first**: 通常是因为合并冲突所致，可以简单地使用`git reset --merge`进行恢复

- **在目录外面执行git参数，不进入目录提交git**:

   ```shell
     git --git-dir=~/foo/.git --work-tree=~/foo push
   ```

- **误删分支及恢复方法**: 项目很久以后才发现以前某个被删除的分支还没合并到主分支，看不到修改了哪些地方了。

   1. 先用`git log -g`找到之前在该分支上面的`commit`记录(所以必须要有经常`commit`的习惯，可以不`push`但是要`commit`)
   2. 从该commit处新建分支`git branch 新分支名 commit的hash值`
   3. 切换到新分支`git checkout 新分支名` 

- **两个人用同一个账号登录同一台服务器居然有一个人有git权限，另一个却没有**: 这是因为虽然是同一个用户登录的服务器，但是所带的key确实不一样的，可以使用`ssh-add -l`查看你登录的`ssh key`，看是否有权限。

   ​