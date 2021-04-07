和eslint不同的是，editorconfig应用于不同的编辑器，不同的编码语言，不同的文件，而eslint是一个js代码的检测工具

通配符说明

```shell
	说明
*	匹配除/之外的任意字符串
**	匹配任意字符串
?	匹配任意单个字符
[name]	匹配 name 字符
[!name]	匹配非 name 字符
{s1,s3,s3}	匹配任意给定的字符串（0.11.0 起支持）
```



Jj

```shell
root = true

[*]
charset = utf-8	# 编码格式
indent_style = space
indent_size = 2
end_of_line = lf	# 定义换行符，可选lf、cr、crlf
trim_trailing_whitespace = true	# 除去换行行首的任意空白字符
insert_final_newline = true	# 在文件末尾插入空白行

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

