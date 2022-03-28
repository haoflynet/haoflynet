---
title: "Git 手册"
date: 2016-08-07 07:12:39
updated: 2022-03-17 18:21:00
categories: tools
---
# Git指南

这里所列举的通用配置无论是在Windows还是Linux，都要用到。

- **一定一定要设置好nginx或者apache的权限，保护好.git目录，防止被黑客获取到，因为这个目录下的文件包含了所有的文件内容**，例如:

  ```python
  import zlib
  import requests
  
  url = "https://domain/.git/objects/9d/6d1ae673f15900b8efd9ad875364b3a651cc0e"
  re = requests.get(url)
  content = zlib.decompress(re.content)	# 这就是文件内容
  ```

## 安装与配置

### 安装Git软件

Windows平台：[Git for Windows](http://msysgit.github.io/)(在安装的时候注意那些选项的设置)  

Linux平台：`sudo apt-get install git`

### 基础配置

打开终端，在windows平台就用上一步安装上的git bash

```shell
# 全局配置，这里的用户名和邮箱填写你自己的帐号，可以是github上的帐号信息
git config --global user.name "haoflyent"
git config --global user.email "haoflynet@gmail.com"

# 如果要同一台机器多个git账户，那么可以取消全局设置
git config --global --unset user.name
git config --global --unset user.email
git config user.email "x@xx.com"    # 在仓库里面单独设置
git config user.name "xx"
git config core.editor vim	# 设置git的默认编辑器，不然在某些系统里面会用nano，不会用

# 生成密钥
ssh-keygen -t rsa -C "haoflynet@gmail.com"
# 然后一路默认就可以，注意看其中的密钥存放位置，其中公钥文件Windows默认为/c/Users/用户名/.ssh/id_rsa.pub# Linux默认为 ~/.ssh/rsa_pub
```

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
GIT_CURL_VERBOSE=1 GIT_TRACE=1 git ...	# 相当于debug，能看到git命令执行期间的状态

git remote -v 	# 列出远程仓库地址
git remote set-url origin git@xxx.git	# 修改git远程仓库地址
git remote add author git@xxx.git	# 添加一个远程仓库地址
git pull author master:origin/master	# 从指定远程仓库拉取分支合并到本地分支

git log  # 查看提交的历史,--oneline按行显示，--graph查看分支的合并情况，--all显示所有分支的历史
git reflog	# 查看HEAD的历史情况
git log -S password	# 搜索一个字符串在所有历史中的出现记录，--all可以搜索所有分支

# 版本回退/回滚,--hard表示将该次提交之前所有的更改都丢弃，git reset是把HEAD向历史移动，之后的所有提交都会删除掉，而git revert是HEAD继续向前，新的commit就和revert的内容刚好相反，所以推荐使用revert，reset的target是要会退到的版本，而revert得target是要取消的版本
git reset --hard HEAD^  # 回退到上一个版本
git reset --hard HEAD^^ # 回退到上上个版本
git reset --hard 233333 # 指定提交ID的回退
git push -f origin master	# remote端也更新

# 回退指定文件/回退单个文件
git log 文件名	# 查询单个文件的提交记录
git reset commitID 文件名 # 可以再次commit
git reset --hard commitID 文件名 # 如果再次提交需要-f


git verify-pack -v .git/objects/pack/<SHA-1-code>.idx | sort -k 3 -n | tail -n 20 # 找出git提交历史中有大文件的提交
git rev-list --object --all | grep commit_id	# 找到某次上面列出的某次提交中提交的文件
```

#### 代码更改

```shell
git blame filename   # 查看某文件的改动历史
git diff + 分支名/commit_id   # 比较当前分支和目标分支的不同
git diff master
git diff 分支名 -- filename	# 比较不同分支的指定文件的不同
git diff origin/master HEAD	# 和远程分支对比

git reset HEAD filename		# 把已经commit了的文件取消暂存
git checkout -- filename	# 放弃指定文件的更改
git checkout <commit hash> -- filename 	# 将文件恢复到指定提交
git commit --amend			# 撤销上一次提交，并将暂存区文件重新提交。当然如果没有git add，直接执行这条命令就相当于修改message

git stash					# 暂存，常用于要切换分支，但是当前分支上面的更改并不想现在提交，需要先把当前分支的状态暂存起来。暂存起来后就可以自由切换到其他分支了。
git stash -p	# 以交互的方式确定每一个修改是否需要stash
git stash list				# 查看所有的"储藏"
git stash apply				# 应用最近一次的“储藏”
git show stash@{1}			# 查看stash
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
git merge xxx # 将制定分支合并到当前分支

## 强制覆盖本地分支
git fetch --all
git reset --hard origin/master

## 合并分支
### 在新的分支如bug-fix修改完成后，执行以下操作
git checkout dev	# 切换回dev分支
git merge bug-fix	# 将bug-fix合并到当前分支，即dev分支
```

#### 变基(rebase)

- 简单地说就是将多个`commit`合并为一个`commit`，以使提交历史变得干净整洁。
- 最好不要修改已经`push`过的提交进行修改，如果一定要修改，需要使用`git push -f origin 分支名`进行推送以覆盖历史提交，对于还没合并进主分支的提交，其实也还可以，但是一定要慎重。
- 需要注意的是变基后提交的`hash`会改变
- 可以使用`git filter-branch --treefilter 'rm -f password.txt' HEAD`命令对整个版本历史中的每次提交进行修改，可以以此来删除误提交的敏感信息

例如，我在本地新建了一个文件，并且先后对文件进行了三次修改操作，但是我想将更新操作合并。通过`git log --oneline`查看本地的提交历史如下:

```shell
4721d5f update readme file
c4cd33c update readme file
31cf944 update readme file
7c040d1 add readme file
```

为了防止合并多次或者多个冲突，在`rebase`之前最好先`git fetch origin master`将远程分支的提交log拉取下来。

接下来，我就使用`rebase`命令编辑提交历史:` git rebase -i  [startpoint]  [endpoint]`，其中`-i`参数表示交互式界面，后面两个参数表示指定一个编辑区间，如果不提供，那么`startpoint`默认为当前已经提交到远程仓库的最后一次提交，`endpoint`为当前为提交到远程仓库的最后一次提交，是一个左开右闭区间。我这里直接执行`git rebase -i 7c040d1`(一般情况下只需要`git rebase origin/master`即可)表示只合并最后三个提交。会弹出下面这个交互式页面:

```shell
pick 31cf944 update readme file
pick c4cd33c update readme file
pick 4721d5f update readme file

# Rebase 7c040e1..4721d5f onto 7c040e1 (3 commands)
#
# Commands:
# p, pick = use commit	保留该commit
# r, reword = use commit, but edit the commit message 保留该commit，但是修改commit的注释
# e, edit = use commit, but stop for amending 保留该commit，但是要停下来修改该次提交
# s, squash = use commit, but meld into previous commit	将该commit和前一个commit合并
# f, fixup = like "squash", but discard this commit's log message 将该commit和前一个commit合并，但是不保留注释信息
# x, exec = run command (the rest of the line) using shell 执行shell命令
# d, drop = remove commit 丢弃该次commit
#
# These lines can be re-ordered; they are executed from top to bottom.	需要注意的是rebase操作是从上往下执行，也就是从最新的commit到最开始的commit执行
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

其中开头几行为几次提交的信息，下面的则是操作说明。我现在直接将上面的提交信息修改为

```shell
pick 31cf944 update readme file
s c4cd33c update readme file
s 4721d5f update readme file
```

然后`:wq`保存即可。现在查看提交历史就变成了这样

```shell
2783433 update readme file
7c040e1 add readme file
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

## 钩子/hook

- 不仅仅`Github`有`webhook`钩子，`git`本身也是有钩子的
- 所有的`git hooks`都在`.git/hooks`目录下，并且所有钩子类型都在该文件有提供示例脚本文件，可以直接根据脚本文件进行修改，例如，可以这样设置钩子
- 常常可以在这里做代码检查
- 常用钩子包括: `pre-commit`提交前、`prepare-commit-msg`准备提交信息、`commit-msg`提交日志、`post-commit`提交后，`post-checkout`切换后、`pre-rebase`Rebase前

#### 禁止本地提交到master/develop分支

```shell
# .git/hooks/pre-commit
#!/bin/sh
# disable commit to master and develop branch
branch=$(git rev-parse --symbolic --abbrev-ref HEAD)
if [ "master" == "$branch" ] || [ "develop" == "$branch" ]; then
  echo ".git/hooks: can not commit to $branch branch"
  exit 1
fi
```

#### 禁止提交包含非ASCII的文件

```shell
# .git/hooks/pre-commit
#!/bin/sh
# disable commit non-ascii content
TEXT=$(git diff)
LC_CTYPE=C
if [[ $TEXT = *[![:ascii:]]* ]]; then
  echo "Contain Non-ASCII"
  exit 1
fi
```

## 贡献PR(Fork别人的项目)

如果希望给开源项目贡献代码或者直接修复bug，那么就需要涉及到fork了并提交了。步骤如下:

1. fork别人的仓库到自己这里: 直接在github里面点击fork，即可在自己的代码仓库里面创建一个一模一样的仓库。

2. 从自己的代码仓库clone下来，并开发。

3. 开发完成后，commit到自己的代码仓库

4. 在自己的项目创建Pull Request，指向到原开源项目中去。

   ![](https://haofly.net/uploads/git_1.jpg)

![](https://haofly.net/uploads/git_2.jpg)

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

   ```shell
    git add .
    git commit -m "some modification"
    git push origin dev
   ```
4. 修改并合并到master分支

   ```shell
    git checkout master # 首先切换到本地的master分支
    git merge --no-ff   # 将本地的dev分支与本地的master分支合并
    git pull            # 获取远程索引
   ```

    这一步可能这一步可能会冲突，原因当然是其他人在你之前对远程的master分支进行了修改并提交上去
    如果没有错，就直接推送
    git push origin master

## TroubleShooting

- **git checkout -b dev origin/dev出现错误fatal: cannot update paths and switch to branch 'origin/dev'** 
  原因是未在远程创建dev分支，或者未在本地更新分支信息

- **git remote add origin git@gitb.com:haoflynet/test，出现错误fatal: remote origin already exists** 
  原因是克隆别人的库下来修改后push到自己的库可能会出现这种错误，要先执行git remote rm origin  

- **.gitignore无效，该忽略的依然没有被忽略**

   ```shell
   git rm -r --cached .	# 这条命令处理不了文件夹，如果是文件夹，需要把最后的点修改为文件夹的路径
   git add .
   git commit -m "fixed untracked files"
   ```

   这样会删除github上面已经提交了的但是现在忽略了的文件，如果要在github上面保留一份，那么执行`git add -f filename`

- **There was a problem with the editor 'vi'** 
  vi编辑器的问题吧，直接换成vim
  `git config --global core.editor $(which vim)`

- **更改文件名后，远程居然没有过更新** 
  git默认对文件名的大小写不敏感，需要在仓库执行`git config core.ignorecase false`让它对大小写敏感

- **`413 request entity too large`**

  发生这个问题是因为采用的是https而不是ssh方式来push仓库，而https传输数据的大小一般是由服务器，即nginx来控制的，太大了是传不上去的，这时候只需要更改为ssh方式即可。

- **修改提交作者和邮箱**: git可以通过`git filter-branch`修改已经提交了的commit的作者和邮箱。

  - 如果仅仅想修改最近一次的，可以直接`git commit --amend --author="haoflynet <haoflynet@gmail.com>"`
  - 如果像修改最近几次的，可以使用`git base -i HEAD~5`(其中5表示最近的5次)，然后将要更改的提交的`pick`修改`e`，保存后，执行`git commit --amend --author="haoflynet <haoflynet@gmail.com>"`，然后一个后就执行`git rebase --continue`，如果还有需要继续执行`git commit --...` 这条命令，最后知道`continue`命令返回`Successfully rebased and updated...`为止，就可以`git push -f`了
  - 如果像修改所有历史的，这里有一个来自[若有所思-胡磊](http://i.dotidea.cn/2015/04/git-amend-author/)的批量修改的脚本，完成后可以check一下，然后`git push -f`即可，亲测可用:

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

- **warning: refname 'remotes/origin/dev' is ambiguous. fatal: 歧义的对象名: 'remotes/origin/dev'**: 原因是错误的新建了一个和远程分支同名的分支，在新建分支的时候一定要`-b`让本地分支与远程分支相对应，遇到这种情况，只需要先删除本地分支即可`git branch -d 分支名`

- **提交时出现`fatal: Unable to create '.git/index.lock': File exists.`**: 原因是检测到有其他的Git在同时操作该本地仓库，如果确认没有其他的，那么直接删除它即可`rm -rf .git/index.lock`

- **The project you were looking for could not be found**: 切换用户试试

- **git revert后如何将分支再次合并进去**: 有时候我们在发现合并错分支后执行了`git revert`进行分支回滚，但是之后再次上线时发现应该合并的代码合并不了了。例如有三个分支prod、master和dev，在dev分支上修改了代码，分别合并到了prod和master，但是prod执行了git revert进行了回滚，之后再想把master合并到prod发现该次的修改消失了，这时候可以再prod上执行git revert，但是revert后的分支合并到mster，而不是prod，这样master之后就能将这次的提交重新合并到prod了

- **github后台添加ssh key但是错误提示: Key is already in use**: 原因是github限制一个key只能在一个账户里面设置，该key已经在其它用户的账户设置里面了，可以用命令`ssh -T -ai ~/.ssh/id_rsa git@github.com`查看到底是谁已经在使用该key了，返回值类似这样:

   ```shell
   Hi haoflynet! You've successfully authenticated, but GitHub does not provide shell acess.
   ```

   其中，Hi后面的即是占用该key的用户名，如果响应类似于 "username/repo"，则表示密钥已作为部署密钥附加到仓库。

- **系统中存在多个key，给git指定使用哪一个key**:

   - 解决方法一，在`~/.ssh/config` 中添加这样的配置:

      ```shell
      host github.com
        HostName github.com
        IdentifyFile ~/.ssh/id_rsa_mygit
        User git
      ```

   - 解决方法二，每次执行命令都使用`GIT_SSH_COMMAND`，例如:

      ```shell
      GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsa_mygit" git pull
      ```


- **Unable to append to .git/**: 可能是因为当前目录存在当前用户无权访问的文件或文件夹，可以使用`ls -al`查看文件夹权限，然后使用`chown`改变目录所属用户

- **git rebase后在另外一端进行pull操作每次都会弹出编辑框**: 这是因为远端的仓库超前了几个commit，但是那几个commit已经不存在了，需要进行`git reset --hard ID`将分支切换到当前最新的head

- **如果想用账号密码访问，但是git pull的时候提示`Repository not found / does not exist`**: 可以将账号密码放到命令里面试试: `git clone https://账户:密码@项目地址.git`

- **仓库可以pull，但是push的时候提示`Repository not found`**: 原因可能是仓库所有者设置了不同的读写权限，可以去github上面看看能不能在线编辑文件，如果在线都不能那么应该就真的只有读权限了

- **搜索查找Git中被删除的文件**

  ```shell
  git log --all --full-history -- **/filename.*	# 模糊查找
  git checkout <SHA>^ -- <path-to-fil>	# checkout下来
  ```

- **强制push(git push -f)报错: remote: error: denying non-fast-forward**：这是因为远端没有开启`force push`权限，这时候只能去仓库托管方修改权限了，github应该是默认开启的，但是assembla没有

- **使用sourcetree等工具的时候Can't find node in PATH, trying to find a node binary on your system**: 

  ```shell
  # vim ~/.huskyrc，这个文件就是用于加载这些环境变量的，注意这是home目录不是项目目录
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  
  export PATH="/Users/haofly/.nvm/versions/node/v15.3.0/bin:$PATH"	# 上面的配置还是不行那直接加到PATH吧
  ```

- **Large files detected, ... recommended maximum file size of 50 MB**: github不允许超过50M的文件上传，只能存储在其他地方，但是已经`commit`倒本地的需要移出来，`git rm --cached 文件名 git commit --amend -CHEAD`

- **修改sourcetree保存的仓库密码**: 需要在macos的keychain中进行删除

- **The unauthenticated git protocol on port 9418 is no longer supported**: 将`git://github.com/xxx`修改为`https://github.com/xxx`

