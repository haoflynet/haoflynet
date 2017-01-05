---
title: "vim 教程"
date: 2013-06-06 14:02:30
categories: tools
---
# VIM
在编辑界一直有两大传说：Vim——编辑器之神，Emacs——神之编辑器。而我是属于vim党的。平时用vim的功能用得不多，其实我只是初学者，基本入门而已。这
里不列举太多功能，用到的时候再说吧。

## 常用快捷键

	# 复制粘贴

	# 纵向编辑列
	ctrl + v 进入选择模式，选择要编辑的行
	shift + i 执行编辑操作，这时候只会在一行上编辑
	两次ESC 所有行都和那一行一样了
	
	# 插入
	o # 在下面添加一行，并进入编辑模式
	
	# 删除
	22 40 dd # 删除指定行范围的行
	gg然后dG  # 清空文件内容
	
	# 纵向删除
	ctrl + v 进入选择模式
	d 删除选择的地方
	
	# 查找替换
	:%s/源字符串/目的字符串/g    # 全局替换
	
	# 跳转
	()：跳转到行首和行尾
	Ctrl-B/Ctrl-F：上下翻页
## 动态配置

	# 行号的显示与取消显示
	:set nonu

## 配置文件/etc/vim/vimrc

    # 可添加如下这些选项
    set autoindent      ; 自动缩进
    set number          ; 显示行号
    set smartindent     ; 智能对齐
    set tabstop=4       ; tab键设置为4个空格宽度
    set background=dark ; 如果感觉太暗可以使用这个(比如deepin默认的那个主题)
    添加自动缩进： set autoindent


## 常用插件


复制粘贴：

    v       进入可视模式，然后可以用方向键进行选择
    y       复制(yank提取)
    p       粘贴
