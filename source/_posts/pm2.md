---
title: "pm2 手册"
date: 2020-02-18 08:50:00
updated: 2021-03-09 16:00:00
categories: nodejs
---

## 安装

```shell
npm install pm2@latest -g
```

## 常用命令

- 基本上能使用程序`name`的地方也可以使用`id`(id一般是从0开始的)

```shell
pm2 start app.js	# 直接启动某个项目
pm2 start app.js --name my-app	# 设置应用名称
pm2 start app.js --no-daemon	# 以非daemon方式运行
pm2 start app.js --max-memory_restart 20M	# 当内存超过20M时就重启应用
pm2 start npm --name my-app -- run start # npm run start方式启动
pm2 stop all	# 停止所有程序
pm2 restart all	# 重启所有程序
pm2 delete 0	# 删除某个进程
pm2 delete all	# 删除所有进程

pm2 list	# 列出所有使用pm2管理的程序
pm2 prettylist	# 用json格式输出

pm2 describe 0	# 查看程序详情，比如启动命令，日志文件位置，nodejs版本，开始时间，堆栈使用情况，延迟时间
pm2 show 0	# 同上
pm2 monit	# 实时监听所有进程，和describe的输出差不多，不过这个是实时的，而且可以看到日志
pm2 monitor appname	# 查看pm2管理的所有进城的详细状态
```

<!--more-->

### 日志相关

- 默认的日志也会通过项目 `package.json -> version`分开设置

```shell
pm2 logs				# 查看所有应用的日志，如果要监听，最好用monitor命令，看得全一点
pm2 logs appname	# 查看指定app的日志输出
pm2 flush # 晴空日志文件

pm2 logrotate -u user	# 设置日志自动轮转，这条命令会写入一条轮转配置到/etc/logrotate.d/pm2-user
pm2 install pm2-logrotate	# 另一种方式实现日志轮转，默认10M
```

### 设置开机启动

```shell
pm2 startup [ubuntu|centos|gentoo|systemd]	# 这样可以自动生成开机启动脚本
pm2 startup ubuntu -u www	# 指定命令执行用户
```

### 配置文件

- 可以以文件的方式设置配置，比如在项目根目录下放一个文件: `pm2.config.js`，运行时候只需要`pm2 start pm2.config.js --env production`，如果不佳env配置就不用加`--env`参数

```javascript
module.exports = {
  apps: [
    {
      name: 'test',
      script: 'server.js',	// 相当于node server.js，如果是npm run start命令，那么script就写npm，args里面放start
      args: 'start', // npm命令参数可以放在这里
      log_date_format: 'YYYY-MM-DD HH:mm Z',
      ignoreWatch: ["[\\/\\\\]\\./", "node_modules"],
      watch: true,
      cwd: 'path/to/project'
      instances: 1,
      exec_mode: "cluster",
      env: {	 // 环境变量
        NODE_ENV: 'production',
        logging: 'on'
      },
      env_staging: {
        NODE_ENV: 'staging',
        logging: 'on'
      }
    },
  ]
}
```

## Troubleshooting

- **没有错误日志无限重启**: 可能原因是运行脚本有问题，例如配置的`npm run dev`，但是程序里面的`dev`脚本依赖的却是另外一个命令，但是那个命令却没有全局安装

