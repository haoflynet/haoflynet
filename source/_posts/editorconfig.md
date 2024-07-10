---
title: "EditorConfig: 在不同编辑器中实现一致的代码风格"
date: 2024-06-05 12:02:30
categories: system
---

与 ESLint 不同，EditorConfig 旨在为不同的编辑器、编码语言和文件类型提供统一的配置。ESLint 是专注于 JavaScript 代码质量和规范的检测工具，而 EditorConfig 则通过配置文件为各种编辑器设定一致的代码风格和格式要求。主流的编辑器，如 VSCode、Sublime Text、Atom 等，通常会默认支持 EditorConfig，并自动加载其规范，使得跨团队协作时代码风格更加统一，减少了因编辑器差异导致的代码格式问题。建议在无论代码是否使用eslint，都添加上`.editorconfig`文件

## 通配符说明

```shell
	说明
*	匹配除/之外的任意字符串
**	匹配任意字符串
?	匹配任意单个字符
[name]	匹配 name 字符
[!name]	匹配非 name 字符
{s1,s3,s3}	匹配任意给定的字符串（0.11.0 起支持）
```

<!--more-->

## 详细配置

```shell
root = true

[*]
charset = utf-8	# 编码格式
indent_style = space
ij_javascript_use_double_quotes = false	# 默认单引号
ij_typescript_use_double_quotes = false	# 默认单引号
ij_javascript_use_semicolon_after_statement = false	# 禁用末尾分号
ij_typescript_use_semicolon_after_statement = false
indent_size = 2
end_of_line = lf	# 定义换行符，可选lf、cr、crlf
trim_trailing_whitespace = true	# 除去换行行首的任意空白字符
insert_final_newline = true	# 在文件末尾插入空白行
max_line_length=150	# 最大行宽

[*.md]
trim_trailing_whitespace = false


[**.js]
indent_size=4
jslint_happy=false
space_after_anon_function=false
brace_style=collapse,preserve-inline
keep_array_indentation=false
keep_function_indentation=false
space_before_conditional=true
break_chained_methods=false
eval_code=false
unescape_strings=false
wrap_line_length=0

[*.{yml,yaml,js,css,scss,html,vue}]
indent_size = 2

[*.blade.php]
indent_size = 2
```

