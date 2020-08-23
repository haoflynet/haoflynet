---
title: "circleci 使用手册"
date: 2020-08-16 17:00:00
categories: dev
---

前两天团队接到一个新项目，我需要为其配置Circle CI，于是就又折腾了一下，不过还好，毕竟之前做过运维的，CI的基本原理是知道的，所以很快就弄好了，这里也简单的记录一下。


### 1. 为项目开启Circle CI

这一步需要在circleci后台项目列表里面为指定的项目开启配置`Set Up Project`，因为第一步已经编写好了配置文件，所以这里可以直接选择`start building`。这一步circleci会自动在对应的项目里面添加`Deploy Key`并且会自动配置到circleci的项目管理里面，如下:

![](https://haofly.net/uploads/circleci_01.png)

![](https://haofly.net/uploads/circleci_02.png)

<!--more-->

### 2. 生成ssh key

这里生成的key是为了circleci能够远程登陆到目标服务器所用的key。使用命令生成key，位置最好是`/Users/<username>/.ssh/id_rsa`，不然`git pull`的时候得单独指定拉取的key

```shell
ssh-keygen -t rsa -C "myCI"
```

然后将该key的公钥添加到Github账号下的ssh配置里面，再将其私钥配置到circle ci中去:

![](https://haofly.net/uploads/circleci_03.png)

### 3. 在代码里添加ci配置文件

在项目根目录添加这样一个文件: `.circleci/config.yml`，这是一个PHP项目的配置

```yaml
version: 2.1	# ci配置的版本号
orbs:	# 共享配置包，类似于docker的基础镜像，例如这里的php可以在这里找到其使用手册https://circleci.com/orbs/registry/orb/circleci/php，该网站还有很多的共享配置包
  php: circleci/php@1.0.1
jobs:	# 一系列的步骤单元
  build-and-test:	# job名称
    executor:	# 执行单元，可以自定义，这里的执行单元是在共享包里面配置好了的
      name: php/default
    steps:	# 该job需要执行的命令集合
      - checkout	# 将分支中的代码检出到working_directory
      - php/install-composer
  deploy-dev:
    machine:	# 以虚拟机的方式运行
      enabled: true
    working_directory: ~/repo-name
    steps:
      - add_ssh_keys:
          fingerprints:
            - "aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp"	# 这里是刚才加入circleci的私钥指纹
      - run:
          name: Adding known host
          command: ssh-keyscan 8.8.8.8 >> ~/.ssh/known_hosts
      - run:
          name: Update git And packages
          command: ssh work@8.8.8.8 'cd /var/www/html && git fetch -p && git reset --hard origin/develop && git pull && composer install'
  deploy-prod:
    machine:
      enabled: true
    working_directory: ~/repo-name
    steps:
      - add_ssh_keys:
          fingerprints:
            - "aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp"
      - run:
          name: Adding known host
          command: ssh-keyscan 8.8.8.8 >> ~/.ssh/known_hosts
      - run:
          name: Update git And packages
          command: ssh work@8.8.8.8 '集成命令'

workflows:
  build-and-test:
    jobs:
      - build-and-test
      - deploy-dev:
          requires:
            - build-and-test
          filters:
            branches:
              only: develop	# 指定该job的分支
      - deploy-prod:
          requires:
            - build-and-test
          filters:
            branches:
              only: master
```

### 4.   推送代码到指定分支检查pipeline是否成功