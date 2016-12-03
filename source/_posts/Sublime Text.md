---
title: "Sublime Text  使用技巧"
date: 2014-09-28 14:40:56
categories: tools
---
参考文章： [http://zh.lucida.me/blog/sublime-text-complete-guide/
](http://zh.lucida.me/blog/sublime-text-complete-
guide/)<http://blog.jobbole.com/40660/>[ ](http://zh.lucida.me/blog/sublime-
text-complete-guide/)

## 汉化

参考：[http://jingyan.baidu.com/article/a501d80ced31d5ec630f5e22.html ](http://ji
ngyan.baidu.com/article/a501d80ced31d5ec630f5e22.html)和[http://www.cnblogs.com
/kingwell/archive/2012/11/22/2782991.html ](http://www.cnblogs.com/kingwell/ar
chive/2012/11/22/2782991.html)sublime3见[http://jingyan.baidu.com/article/ce093
21b22fc7d2bff858f87.html
](http://jingyan.baidu.com/article/ce09321b22fc7d2bff858f87.html)汉化包在我的云盘上是有个的

需要注意的是，汉化版的如果直接点击Perferences里面的设置文件并修改并不会有效，真正的配置文件可以在浏览程序包里面找到`Preferences.su
blime-settings`这个文件，只有在这里面的修改才是有效的，不信，你在这儿修改一下主题试试，立马就会生效。


    {
        //"color_scheme": "Packages/Color Scheme - Default/IDLE.tmTheme",
        "color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme",
        "font_size": 11,
        "ignored_packages":
        [
        ]
    }

## 常用快捷键



    Ctrl + `                打开控制台(和QQ拼音有冲突，改一下QQ拼音的设置)
    Ctrl + ←/→         逐词移位
    Ctrl + ↑/↓             移动当前显示区域
    Ctrl + Shift + F    多文件搜索
    Ctrl + G               跳转到指定行


## Python编译系统

(注：如果是Sublime3的绿色版，可以在C:\\software\\sublime\\Data\\Packages\\User下新建Python.sublime-
build文件)默认情况下，应该是可以直接编译(即Ctrl +
B)执行的，但是由于我的电脑上python.exe的路径太多，所以需要重新设置，偏好->浏览程序包，在该文件夹下搜索_**Python.sublime-bu
ild**_该文件就是sublime编译python的配置文件，此时需要将Python的路径修改为正确的路径，比如(如果找不到该文件，那就在tools里面新
建编译系统)：



    {
        "cmd": ["python", "-u", "$file"],
        "path": "C:/Python34",
        "file_regex": "^[ ]_File \\"(..._?)\\", line ([0-9]*)",
        "selector": "source.python"
    }



如果出现_**[Decode error - output not utf-8]**_错误，那么可以在该配置文件中添加_**"encoding":"cp93
6"**_，我当时配置的时候正在用os.system执行curl命令，但是却说curl不是内部命令，关键是我已经把它加进了系统的环境变量了，在windows
的cmd中能够执行curl。之前找不到解决方案，就用直接在Terminal中执行python文件的，现在我知道了sublime里的python的环境变量(通
过_os.getenv('PATH')_获取)里的PATH的值只是它自己的执行路径，而要添加其它的路径，则要在代码中添加



    os.environ['PATH'] = os.environ['PATH'] + u'; C:\\Program Files (x86)\\Git\\bin'

另外,Linux下,如果要使用Python3,那么需要自己新建build文件,Tools->Build System>New Build
System,然后写入如下代码,保存为python3开头的build文件



    \{
        "cmd": ["python3", "$file"]
    \}



在Mac下，可能出现没有显示输出或者编码错误，例如：UnicodeEncodeError: 'ascii' codec can't encode
characters in position 0-2: ordinal not in range(128)

可以将build system改为如下：



    \{
    "cmd": ["python3", "-u", "$file"],
    "file_regex": "^[ ]_File \\"(..._?)\\", line ([0-9]*)",
    "selector": "source.python",
    "env": \{"LANG": "en_US.UTF-8"\}
    \}


并讲该文件的Build System为Python3即可.擦,要使用input,还是只能用SublimeREPL.

## 推荐插件

**Package Control**：sublime很好的插件管理器，[安装方式](https://sublime.wbond.net/installation#st2) ，之后安装插件就可以直接使用它来安装了，如果要安装插件，点击_**Preferences->Package Control**_或者Ctrl + Shift + P ，然后选择_**Package Control: Install Package**_，然后输入相应的插件名称，而某些插件的功能如git的功能也可以通过Ctrl+Shift+P来选择

**AllAutocomplete**：可以在所有打开的文件里面查找关键词来提示代码

**Anaconda**：真正可以将sublime打造成Python的IDE，功能非常全，比如语法检查、函数跳转等IDE才有的功能，当然，最好把warning提醒给去掉，做自己的项目，从头做起，遵守PEP8规范，很好，但是打开公司之前的项目，全是warning，忍无可忍了，所以需要给其添加一个user配置：



    \{
        "pep8_error_levels": \{"E": "W","V": "V"\},
    \}


**Bracket Highlighter**：匹配标签，比Sublime默认的匹配明显多了

**ConvertToUtf8**：可以解决很多编码问题，比如打开txt乱码

**Djaneiro**：支持Django模版和关键字高亮，还可以方便得到代码片，例如，输入var 可以新建`\{\{\}\}`，输入tag可以新建`\{\%\%\}`

**DocBlockr**：可快速生成代码注释，对于PHP输入/**然后回车即可

**Emmet**：十分强大的html、css代码自动补全工具，常用使用方法：


    1.适用于tr(th)/ul(li)/select(option)中
    tr>th*3 会生成如下代码：
    <tr>
        <th></th>
        <th></th>
        <th></th>
    </tr>

**HtmlPretty**：Ctrl + Shift + H快速格式化CSS、Html、Js等文件，但需要先安装上NodeJS

**Git**：Sublime也支持git，真是太好了

**IMESupport：**解决中文输入法不跟随问题(只针对win，linux下无解)

**Markdown Preview**：非常使用的markdown扩展，ctrl + shift + p，然后输入mrkdown使用相应的命令,ctrl + B构建当前文件为html

**SublimeCodeIntel**：增强Python等语言的自动完成功能(暂时不考虑了，妈蛋，顺序永远不变)

**SublimeLinter-php**：PHP代码审查工具

**SublimeREPL**：强大的Python调试工具，具体有多强大，我还没弄清楚，Sublime默认的Python终端太low了，中文总是不对，但是在>>>这里确实对的，所以以后直接用SublimeREPL的run current file功能就可以相当于在>>>中执行输出了。快捷键Ctrl+Shift+P

**SyncedSideBar**：Mac上保存打开的项目

**VAlign**：代码对齐插件，比那个alignment好用多了，快捷键是Ctrl + \\

**View in Browser**：在浏览器中预览，右键即可，注意我的谷歌是64位，要把配置文件最下面那一行的firefox改为chrome64（把default配置拷贝到user配置再修改）

**Vintage**：可以打开VIM模式，默认是安装了的，只需要用package control来enable一下即可

## 其他问题

1.Linux下Sublime text 3无法输入中文，参见<http://jingyan.baidu.com/article/f3ad7d0ff8731
609c3345b3b.html>，唯一需要注意的是，编译so文件之前得先安装gtk的dev，`sudo apt-get install
libgtk2.0-dev2`

2.打开sublime的调试模式查看哪儿出错了： 在Preferences.sublime-settings里面添加"debug":
true，这样重启后Ctrl+`即可查看启动中的错误信息
